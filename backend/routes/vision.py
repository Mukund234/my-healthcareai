from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from services.vision_service import analyze_image_placeholder

router = APIRouter(prefix="/api/vision", tags=["vision"])


class VisionAnalysisResponse(BaseModel):
    findings: Any
    heatmap_available: bool
    disclaimer: str


@router.post("/analyze", response_model=VisionAnalysisResponse)
async def analyze_image(image: UploadFile = File(...)):
    """
    Basic image analysis endpoint (placeholder).

    Accepts an uploaded image and returns a non-diagnostic, generic analysis.
    Later you can plug in a real medical imaging model and keep the same API.
    """
    try:
        content = await image.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read image: {exc}")

    result: Dict[str, Any] = analyze_image_placeholder(content)
    return VisionAnalysisResponse(**result)

