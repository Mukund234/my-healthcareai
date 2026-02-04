"""
API routes for chat/follow-up questions about assessment results.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import get_db
from models.health_assessment import HealthAssessment
from models.risk_result import RiskResult
from ai.llm_explainer import get_explainer

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    assessment_id: int
    question: str
    language: str = "en"

class ChatResponse(BaseModel):
    answer: str
    language: str

@router.post("/ask", response_model=ChatResponse)
async def ask_question(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Ask a follow-up question about assessment results
    """
    
    # Get assessment and risk results
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
    
    # Generate answer using LLM
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
        except Exception as e:
            answer = _generate_fallback_answer(chat_request.language)
    else:
        answer = _generate_fallback_answer(chat_request.language)
    
    return ChatResponse(
        answer=answer,
        language=chat_request.language
    )

def _generate_llm_answer(question, assessment, risk_result, language, explainer):
    """Generate answer using LLM"""
    
    from config import settings
    
    lang_instruction = "in Hindi (Devanagari script)" if language == 'hi' else "in English"
    
    # Prepare context
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
1. Answer the question {lang_instruction} based on the assessment context
2. Keep the answer concise (under 100 words)
3. Be supportive and educational
4. If the question is about specific medical treatment, remind them to consult a doctor
5. Always end with the disclaimer: "⚠️ This is not medical advice. Consult a qualified healthcare provider."
"""
    
    response = explainer.client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a health education assistant. Answer questions about health risk assessments in a supportive, educational manner. Never provide medical diagnoses or treatment advice."},
            {"role": "user", "content": context}
        ],
        temperature=0.7,
        max_tokens=300
    )
    
    return response.choices[0].message.content.strip()

def _generate_fallback_answer(language):
    """Generate fallback answer when LLM is not available"""
    
    if language == 'hi':
        return """मैं आपके प्रश्न का विस्तृत उत्तर देने में असमर्थ हूं। कृपया अपने मूल्यांकन परिणामों और सिफारिशों की समीक्षा करें। विशिष्ट चिकित्सा सलाह के लिए, कृपया स्वास्थ्य सेवा प्रदाता से परामर्श लें।

⚠️ यह चिकित्सा सलाह नहीं है। चिकित्सा निर्णयों के लिए योग्य स्वास्थ्य सेवा प्रदाता से परामर्श लें।"""
    
    return """I'm unable to provide a detailed answer to your question at this time. Please review your assessment results and recommendations. For specific medical advice, please consult with a healthcare provider.

⚠️ This is not medical advice. Consult a qualified healthcare provider for medical decisions."""
