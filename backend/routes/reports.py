from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from database import get_db
from models.health_assessment import HealthAssessment
from models.risk_result import RiskResult
from risk_engine.risk_calculator import RiskCalculator
from services.report_builder import build_assessment_report_pdf

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/assessment/{assessment_id}.pdf")
async def get_assessment_report_pdf(
    assessment_id: int,
    db: Session = Depends(get_db),
):
    """
    Generate a PDF report for a given assessment ID.

    The PDF is built on the fly from the stored assessment + risk result and
    includes an integrity hash. It is not cached on disk for now.
    """
    assessment = (
        db.query(HealthAssessment)
        .filter(HealthAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    risk_result = (
        db.query(RiskResult)
        .filter(RiskResult.assessment_id == assessment_id)
        .first()
    )
    if not risk_result:
        raise HTTPException(status_code=404, detail="Risk results not found")

    calculator = RiskCalculator(use_ml=False)
    assessment_data = {
        "age": assessment.age,
        "gender": assessment.gender,
        "height_cm": assessment.height_cm,
        "weight_kg": assessment.weight_kg,
        "activity_level": assessment.activity_level,
        "sleep_hours": assessment.sleep_hours,
        "smoking": assessment.smoking,
        "alcohol_consumption": assessment.alcohol_consumption,
        "family_history": assessment.family_history or {},
        "stress_level": assessment.stress_level,
        "blood_pressure_systolic": assessment.blood_pressure_systolic,
        "symptoms": assessment.symptoms or [],
    }
    rebuilt = calculator.calculate_all_risks(assessment_data)

    pdf_bytes = build_assessment_report_pdf(assessment_data, rebuilt)
    filename = f"health_report_{assessment_id}.pdf"
    headers = {
        "Content-Disposition": f'inline; filename="{filename}"'
    }
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)

