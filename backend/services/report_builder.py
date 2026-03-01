import io
import json
import hashlib
from typing import Dict, Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def build_assessment_report_pdf(assessment: Dict[str, Any], risk: Dict[str, Any]) -> bytes:
    """
    Build a simple PDF report for a health assessment + risk result.

    The report includes:
    - Basic profile
    - Overall risk and triage summary
    - Top risks and recommendations
    - A deterministic hash for integrity at the end
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title = "Health Risk Screening Report"
    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))

    profile_lines = [
        f"Age: {assessment.get('age')}",
        f"Gender: {assessment.get('gender')}",
        f"Height (cm): {assessment.get('height_cm')}",
        f"Weight (kg): {assessment.get('weight_kg')}",
    ]
    story.append(Paragraph("Profile", styles["Heading2"]))
    for line in profile_lines:
        story.append(Paragraph(line, styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Overall Risk", styles["Heading2"]))
    story.append(
        Paragraph(
            f"Overall score: {risk.get('overall_risk_score'):.2f} "
            f"({risk.get('overall_severity', '').upper()})",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    triage = risk.get("triage", {})
    if triage:
        story.append(Paragraph("Triage Summary", styles["Heading2"]))
        story.append(
            Paragraph(f"Level: {triage.get('risk_level', 'Unknown')}", styles["Normal"])
        )
        story.append(
            Paragraph(f"Urgency: {triage.get('urgency', 'N/A')}", styles["Normal"])
        )
        story.append(Spacer(1, 6))
        next_steps = triage.get("next_steps", [])
        if next_steps:
            story.append(Paragraph("Next Steps:", styles["Normal"]))
            for step in next_steps:
                story.append(Paragraph(f"- {step}", styles["Normal"]))
        story.append(Spacer(1, 12))

    risk_scores = risk.get("risk_scores", {})
    if risk_scores:
        story.append(Paragraph("Condition-wise Risk Scores", styles["Heading2"]))
        for key, val in risk_scores.items():
            label = key.replace("_", " ").title()
            story.append(Paragraph(f"{label}: {val:.2f}", styles["Normal"]))
        story.append(Spacer(1, 12))

    recs = risk.get("recommendations", [])
    if recs:
        story.append(Paragraph("Recommendations", styles["Heading2"]))
        for rec in recs[:8]:
            story.append(Paragraph(f"- {rec}", styles["Normal"]))
        story.append(Spacer(1, 12))

    disclaimer = (
        "This report is for preventive health education and screening. "
        "It is not a diagnosis or a substitute for consultation with a qualified clinician. "
        "In an emergency, call local services (for example 108/112 in India) or go to the nearest hospital."
    )
    story.append(Paragraph("Disclaimer", styles["Heading2"]))
    story.append(Paragraph(disclaimer, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Integrity hash over core data
    core_payload = {
        "assessment": {
            "age": assessment.get("age"),
            "gender": assessment.get("gender"),
            "height_cm": assessment.get("height_cm"),
            "weight_kg": assessment.get("weight_kg"),
        },
        "overall": {
            "score": risk.get("overall_risk_score"),
            "severity": risk.get("overall_severity"),
        },
    }
    digest = hashlib.sha256(json.dumps(core_payload, sort_keys=True).encode("utf-8")).hexdigest()
    story.append(Paragraph(f"Report Integrity Hash: {digest}", styles["Code"]))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()

