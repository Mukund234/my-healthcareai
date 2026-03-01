"""
API routes for health assessment submission and retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime

from database import get_db
from models.health_assessment import HealthAssessment
from models.risk_result import RiskResult
from risk_engine.risk_calculator import RiskCalculator
from risk_engine.questionnaire import get_questionnaire_schema
from ai.llm_explainer import get_explainer

router = APIRouter(prefix="/api/assessment", tags=["assessment"])

# Pydantic models for request/response
class AssessmentRequest(BaseModel):
    # Basic Info
    age: int = Field(..., ge=0, le=120)
    gender: str = Field(..., pattern="^(male|female|other)$")
    height_cm: float = Field(..., gt=0, le=300)
    weight_kg: float = Field(..., gt=0, le=500)
    
    # Lifestyle
    activity_level: str = Field(default="moderate")
    sleep_hours: float = Field(default=7, ge=0, le=24)
    smoking: bool = Field(default=False)
    alcohol_consumption: str = Field(default="none")
    
    # Diet
    diet_type: str = Field(default="balanced")
    water_intake_liters: float = Field(default=2, ge=0, le=10)
    fast_food_frequency: str = Field(default="rarely")
    
    # Medical History
    family_history: Dict = Field(default_factory=dict)
    existing_conditions: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    
    # Symptoms
    symptoms: List[str] = Field(default_factory=list)
    stress_level: int = Field(default=5, ge=1, le=10)
    
    # Optional BP readings
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    
    # Language preference
    language: str = Field(default="en", pattern="^(en|hi)$")
    
    # Consent
    consent_given: bool = Field(default=True)

class RiskScores(BaseModel):
    diabetes_risk: float
    hypertension_risk: float
    cardiovascular_risk: float
    obesity_risk: float
    stress_burnout_risk: float

class AssessmentResponse(BaseModel):
    assessment_id: int
    risk_scores: RiskScores
    overall_risk_score: float
    overall_severity: str
    recommendations: List[str]
    risk_explanations: List[Dict[str, Any]]
    triage: Dict[str, Any]
    explanation: str
    doctor_consult_needed: str
    created_at: datetime

@router.get("/questionnaire")
async def get_questionnaire():
    """
    Get structured assessment questions for chatbot/form rendering
    """
    return get_questionnaire_schema()

@router.post("/submit", response_model=AssessmentResponse)
async def submit_assessment(
    assessment: AssessmentRequest,
    db: Session = Depends(get_db)
):
    """
    Submit a health assessment and get risk analysis
    """
    
    # Validate consent
    if not assessment.consent_given:
        raise HTTPException(status_code=400, detail="User consent is required")
    
    # Create assessment record
    db_assessment = HealthAssessment(
        age=assessment.age,
        gender=assessment.gender,
        height_cm=assessment.height_cm,
        weight_kg=assessment.weight_kg,
        activity_level=assessment.activity_level,
        sleep_hours=assessment.sleep_hours,
        smoking=assessment.smoking,
        alcohol_consumption=assessment.alcohol_consumption,
        diet_type=assessment.diet_type,
        water_intake_liters=assessment.water_intake_liters,
        fast_food_frequency=assessment.fast_food_frequency,
        family_history=assessment.family_history,
        existing_conditions=assessment.existing_conditions,
        medications=assessment.medications,
        symptoms=assessment.symptoms,
        stress_level=assessment.stress_level,
        blood_pressure_systolic=assessment.blood_pressure_systolic,
        blood_pressure_diastolic=assessment.blood_pressure_diastolic
    )
    
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    
    # Calculate risks
    calculator = RiskCalculator(use_ml=True)
    
    assessment_data = {
        'age': assessment.age,
        'gender': assessment.gender,
        'height_cm': assessment.height_cm,
        'weight_kg': assessment.weight_kg,
        'activity_level': assessment.activity_level,
        'sleep_hours': assessment.sleep_hours,
        'smoking': assessment.smoking,
        'alcohol_consumption': assessment.alcohol_consumption,
        'family_history': assessment.family_history,
        'stress_level': assessment.stress_level,
        'blood_pressure_systolic': assessment.blood_pressure_systolic
    }
    
    risk_results = calculator.calculate_all_risks(assessment_data)
    
    # Generate explanation
    explainer = get_explainer()
    explanation = explainer.generate_explanation(
        risk_results, 
        assessment_data, 
        language=assessment.language
    )
    
    # Save risk results
    db_risk_result = RiskResult(
        assessment_id=db_assessment.id,
        diabetes_risk=risk_results['risk_scores']['diabetes_risk'],
        hypertension_risk=risk_results['risk_scores']['hypertension_risk'],
        cardiovascular_risk=risk_results['risk_scores']['cardiovascular_risk'],
        obesity_risk=risk_results['risk_scores']['obesity_risk'],
        stress_burnout_risk=risk_results['risk_scores']['stress_burnout_risk'],
        diabetes_severity=risk_results['severity_levels']['diabetes_severity'],
        hypertension_severity=risk_results['severity_levels']['hypertension_severity'],
        cardiovascular_severity=risk_results['severity_levels']['cardiovascular_severity'],
        obesity_severity=risk_results['severity_levels']['obesity_severity'],
        stress_severity=risk_results['severity_levels']['stress_severity'],
        overall_risk_score=risk_results['overall_risk_score'],
        overall_severity=risk_results['overall_severity'],
        recommendations=risk_results['recommendations'],
        doctor_consult_needed=risk_results['doctor_consult_needed'],
        explanation_text=explanation,
        explanation_language=assessment.language,
        model_version="1.0",
        calculation_method=risk_results['calculation_method']
    )
    
    db.add(db_risk_result)
    db.commit()
    db.refresh(db_risk_result)
    
    # Return response
    return AssessmentResponse(
        assessment_id=db_assessment.id,
        risk_scores=RiskScores(**risk_results['risk_scores']),
        overall_risk_score=risk_results['overall_risk_score'],
        overall_severity=risk_results['overall_severity'],
        recommendations=risk_results['recommendations'],
        risk_explanations=risk_results.get('risk_explanations', []),
        triage=risk_results.get('triage', {}),
        explanation=explanation,
        doctor_consult_needed=risk_results['doctor_consult_needed'],
        created_at=db_assessment.created_at
    )

@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a previous assessment by ID
    """
    
    # Get assessment
    assessment = db.query(HealthAssessment).filter(
        HealthAssessment.id == assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get risk result
    risk_result = db.query(RiskResult).filter(
        RiskResult.assessment_id == assessment_id
    ).first()
    
    if not risk_result:
        raise HTTPException(status_code=404, detail="Risk results not found")
    
    # Rebuild triage/explanations from stored assessment data.
    calculator = RiskCalculator(use_ml=True)
    assessment_data = {
        'age': assessment.age,
        'gender': assessment.gender,
        'height_cm': assessment.height_cm,
        'weight_kg': assessment.weight_kg,
        'activity_level': assessment.activity_level,
        'sleep_hours': assessment.sleep_hours,
        'smoking': assessment.smoking,
        'alcohol_consumption': assessment.alcohol_consumption,
        'family_history': assessment.family_history or {},
        'stress_level': assessment.stress_level,
        'blood_pressure_systolic': assessment.blood_pressure_systolic,
        'symptoms': assessment.symptoms or []
    }
    rebuilt = calculator.calculate_all_risks(assessment_data)

    return AssessmentResponse(
        assessment_id=assessment.id,
        risk_scores=RiskScores(
            diabetes_risk=risk_result.diabetes_risk,
            hypertension_risk=risk_result.hypertension_risk,
            cardiovascular_risk=risk_result.cardiovascular_risk,
            obesity_risk=risk_result.obesity_risk,
            stress_burnout_risk=risk_result.stress_burnout_risk
        ),
        overall_risk_score=risk_result.overall_risk_score,
        overall_severity=risk_result.overall_severity,
        recommendations=risk_result.recommendations,
        risk_explanations=rebuilt.get("risk_explanations", []),
        triage=rebuilt.get("triage", {}),
        explanation=risk_result.explanation_text,
        doctor_consult_needed=risk_result.doctor_consult_needed,
        created_at=assessment.created_at
    )
