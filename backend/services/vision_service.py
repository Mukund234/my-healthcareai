from typing import Dict, Any


def analyze_image_placeholder(image_bytes: bytes) -> Dict[str, Any]:
    """
    Placeholder image analysis for health-related photos.

    In production, plug in a dermatology / trauma model (CNN/ViT) here.
    For now this returns a static, safe description and a disclaimer so
    the API contract is ready without making clinical claims.
    """
    _ = image_bytes  # unused placeholder
    return {
        "findings": [
            {
                "label": "non_specific_skin_change",
                "confidence": 0.5,
                "comment": "Placeholder vision model — this is not a diagnosis.",
            }
        ],
        "heatmap_available": False,
        "disclaimer": (
            "This is a placeholder image analysis. It cannot be used to diagnose or "
            "rule out any condition. Please consult a qualified clinician for any "
            "new or worsening skin or wound changes."
        ),
    }

