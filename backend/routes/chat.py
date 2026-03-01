"""
Health chatbot APIs.
Includes both follow-up Q&A by assessment_id and ChatGPT-style session chat.
"""

import re
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ai.llm_explainer import get_explainer
from services.audit_logger import log_event
from database import get_db
from models.health_assessment import HealthAssessment
from models.risk_result import RiskResult
from risk_engine.risk_calculator import RiskCalculator

router = APIRouter(prefix="/api/chat", tags=["chat"])

# In-memory chat sessions for MVP. Replace with DB/Redis in production.
chat_sessions: Dict[str, Dict[str, Any]] = {}


class ChatRequest(BaseModel):
    assessment_id: int
    question: str
    language: str = "en"


class ChatResponse(BaseModel):
    answer: str
    language: str


class SessionStartRequest(BaseModel):
    user_id: Optional[str] = "anonymous"
    language: str = Field(default="en", pattern="^(en|hi)$")


class SessionStartResponse(BaseModel):
    session_id: str
    message: str
    disclaimer: str


class HealthChatMessageRequest(BaseModel):
    session_id: str
    message: str


class HealthChatMessageResponse(BaseModel):
    session_id: str
    reply: str
    collected_data: Dict[str, Any]
    missing_fields: List[str]
    assessment_ready: bool
    risk_snapshot: Optional[Dict[str, Any]] = None
    triage: Optional[Dict[str, Any]] = None


@router.post("/ask", response_model=ChatResponse)
async def ask_question(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Ask a follow-up question about assessment results.
    """
    assessment = db.query(HealthAssessment).filter(
        HealthAssessment.id == chat_request.assessment_id
    ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    risk_result = db.query(RiskResult).filter(
        RiskResult.assessment_id == chat_request.assessment_id
    ).first()

    if not risk_result:
        raise HTTPException(status_code=404, detail="Risk results not found")

    explainer = get_explainer()

    if explainer.client:
        try:
            answer = _generate_llm_answer(
                chat_request.question,
                assessment,
                risk_result,
                chat_request.language,
                explainer
            )
        except Exception:
            answer = _generate_fallback_answer(chat_request.language)
    else:
        answer = _generate_fallback_answer(chat_request.language)

    return ChatResponse(answer=answer, language=chat_request.language)


@router.post("/start-session", response_model=SessionStartResponse)
async def start_session(request: SessionStartRequest):
    """
    Start a ChatGPT-style health chat session.
    """
    session_id = f"health_{request.user_id}_{uuid.uuid4().hex[:10]}"
    chat_sessions[session_id] = {
        "user_id": request.user_id,
        "language": request.language,
        "messages": [],
        "collected_data": {},
    }

    opening = (
        "I am your health assistant. Tell me your symptoms or share your profile, "
        "and I will estimate early health risk and next steps. "
        "Start with age, gender, height, and weight."
    )

    return SessionStartResponse(
        session_id=session_id,
        message=opening,
        disclaimer="This chatbot is for screening only and not a medical diagnosis."
    )


@router.post("/message", response_model=HealthChatMessageResponse)
async def send_health_message(request: HealthChatMessageRequest):
    """
    Multi-turn health chat message endpoint.
    """
    session = chat_sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session["messages"].append({"role": "user", "content": request.message})

    extracted = _extract_health_data(request.message)
    session["collected_data"].update(extracted)

    missing_fields = _missing_fields(session["collected_data"])
    ready = len(missing_fields) == 0

    if not ready:
        follow_up = _next_question(missing_fields)
        reply = (
            "Thanks, I noted that. "
            f"To improve your risk prediction, I still need: {', '.join(missing_fields[:3])}. {follow_up}"
        )
        session["messages"].append({"role": "assistant", "content": reply})
        return HealthChatMessageResponse(
            session_id=request.session_id,
            reply=reply,
            collected_data=session["collected_data"],
            missing_fields=missing_fields,
            assessment_ready=False,
        )

    calculator = RiskCalculator(use_ml=True)
    risk_results = calculator.calculate_all_risks(session["collected_data"])

    risk_snapshot = {
        "overall_risk_score": risk_results["overall_risk_score"],
        "overall_severity": risk_results["overall_severity"],
        "top_risks": sorted(
            risk_results["risk_scores"].items(),
            key=lambda item: item[1],
            reverse=True
        )[:3],
        "recommendations": risk_results["recommendations"][:5],
    }

    triage = risk_results.get("triage", {})

    # Log triage and risk snapshot for monitoring / future model training
    try:
        log_event(
            "chat_triage_completed",
            {
                "session_id": request.session_id,
                "collected_data": session["collected_data"],
                "risk_snapshot": risk_snapshot,
                "triage": triage,
            },
        )
    except Exception:
        # Logging should never break user flow
        pass
    reply = (
        f"Your current screening risk is {risk_snapshot['overall_severity'].upper()} "
        f"({risk_snapshot['overall_risk_score']:.2f}). "
        f"Triage level: {triage.get('risk_level', 'Unknown')}. "
        "I can now answer follow-up questions about symptoms, prevention, and when to seek care."
    )

    session["messages"].append({"role": "assistant", "content": reply})

    return HealthChatMessageResponse(
        session_id=request.session_id,
        reply=reply,
        collected_data=session["collected_data"],
        missing_fields=[],
        assessment_ready=True,
        risk_snapshot=risk_snapshot,
        triage=triage,
    )


def _extract_health_data(message: str) -> Dict[str, Any]:
    text = message.lower()
    data: Dict[str, Any] = {}

    age_match = re.search(r"\b(?:i am|i'm|age)\s*(\d{1,3})\b", text)
    if not age_match:
        age_match = re.search(r"\b(\d{1,3})\s*(?:years|year|yrs|yo)\b", text)
    if age_match:
        age = int(age_match.group(1))
        if 0 < age <= 120:
            data["age"] = age

    if "male" in text:
        data["gender"] = "male"
    elif "female" in text:
        data["gender"] = "female"
    elif "other" in text or "non-binary" in text:
        data["gender"] = "other"

    height_match = re.search(r"(\d{2,3})\s*cm", text)
    if height_match:
        data["height_cm"] = float(height_match.group(1))

    weight_match = re.search(r"(\d{2,3})\s*kg", text)
    if weight_match:
        data["weight_kg"] = float(weight_match.group(1))

    sleep_match = re.search(r"(\d{1,2}(?:\.\d+)?)\s*hours?\s*(?:sleep|of sleep)?", text)
    if sleep_match:
        data["sleep_hours"] = float(sleep_match.group(1))

    stress_match = re.search(r"stress\s*(?:is|level)?\s*(\d{1,2})", text)
    if stress_match:
        stress = int(stress_match.group(1))
        if 1 <= stress <= 10:
            data["stress_level"] = stress

    if any(token in text for token in ["sedentary", "no exercise", "inactive"]):
        data["activity_level"] = "sedentary"
    elif any(token in text for token in ["light activity", "1-2 days", "little exercise"]):
        data["activity_level"] = "light"
    elif any(token in text for token in ["moderate", "3-5 days"]):
        data["activity_level"] = "moderate"
    elif any(token in text for token in ["active", "6-7 days"]):
        data["activity_level"] = "active"
    elif any(token in text for token in ["athlete", "very active"]):
        data["activity_level"] = "very_active"

    if any(token in text for token in ["i smoke", "smoker", "tobacco", "cigarette"]):
        data["smoking"] = True
    if any(token in text for token in ["non smoker", "don't smoke", "do not smoke", "never smoke"]):
        data["smoking"] = False

    if "blood pressure" in text:
        bp_match = re.search(r"(\d{2,3})\s*/\s*(\d{2,3})", text)
        if bp_match:
            data["blood_pressure_systolic"] = int(bp_match.group(1))
            data["blood_pressure_diastolic"] = int(bp_match.group(2))

    family_history = {}
    if "family" in text or "mother" in text or "father" in text:
        if "diabetes" in text:
            family_history["diabetes"] = True
        if "hypertension" in text or "high blood pressure" in text:
            family_history["hypertension"] = True
        if "heart" in text:
            family_history["heart_disease"] = True
    if family_history:
        data["family_history"] = family_history

    symptom_keywords = [
        "fever", "cough", "fatigue", "headache", "chest pain", "breath",
        "dizziness", "nausea", "vomit", "diarrhea", "weakness"
    ]
    found = [sym for sym in symptom_keywords if sym in text]
    if found:
        data["symptoms"] = found

    # defaults for optional values
    if "alcohol" in text:
        if "none" in text or "never" in text:
            data["alcohol_consumption"] = "none"
        elif "occasional" in text:
            data["alcohol_consumption"] = "occasional"
        elif "moderate" in text:
            data["alcohol_consumption"] = "moderate"
        elif "heavy" in text or "daily" in text:
            data["alcohol_consumption"] = "heavy"

    return data


def _missing_fields(data: Dict[str, Any]) -> List[str]:
    required = [
        "age", "gender", "height_cm", "weight_kg",
        "activity_level", "sleep_hours", "smoking", "stress_level"
    ]
    return [field for field in required if field not in data]


def _next_question(missing_fields: List[str]) -> str:
    prompts = {
        "age": "Please share your age.",
        "gender": "Please share your gender (male/female/other).",
        "height_cm": "Please share your height in cm.",
        "weight_kg": "Please share your weight in kg.",
        "activity_level": "How active are you weekly (sedentary/light/moderate/active)?",
        "sleep_hours": "How many hours do you sleep at night?",
        "smoking": "Do you smoke or use tobacco?",
        "stress_level": "On a 1-10 scale, what is your stress level?",
    }
    for field in missing_fields:
        if field in prompts:
            return prompts[field]
    return "Tell me more about your health status."


def _generate_llm_answer(question, assessment, risk_result, language, explainer):
    """Generate answer using LLM."""

    from config import settings

    lang_instruction = "in Hindi (Devanagari script)" if language == 'hi' else "in English"

    context = f"""
Assessment Context:
- Age: {assessment.age}
- Gender: {assessment.gender}
- Overall Risk: {risk_result.overall_severity}
- Diabetes Risk: {risk_result.diabetes_severity}
- Hypertension Risk: {risk_result.hypertension_severity}
- Cardiovascular Risk: {risk_result.cardiovascular_severity}
- Recommendations: {', '.join(risk_result.recommendations[:3])}

User Question: {question}

Instructions:
1. Answer the question {lang_instruction} based on the assessment context.
2. Keep the answer concise (under 120 words).
3. Do not provide diagnosis or prescriptions.
4. Include care escalation guidance when red-flag symptoms are mentioned.
5. End with: "This is not medical advice. Consult a qualified healthcare provider."
"""

    response = explainer.client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a health service assistant focused on screening, triage, prevention, and care navigation."
            },
            {"role": "user", "content": context}
        ],
        temperature=0.4,
        max_tokens=350
    )

    return response.choices[0].message.content.strip()


def _generate_fallback_answer(language):
    """Generate fallback answer when LLM is not available."""

    if language == 'hi':
        return (
            "मैं अभी विस्तृत उत्तर देने में असमर्थ हूं। कृपया अपने जोखिम परिणाम देखें और "
            "गंभीर लक्षण होने पर तुरंत डॉक्टर से संपर्क करें।\n\n"
            "यह चिकित्सा सलाह नहीं है।"
        )

    return (
        "I cannot provide a detailed answer right now. Please review your risk summary, "
        "and seek urgent care if severe symptoms are present.\n\n"
        "This is not medical advice."
    )
