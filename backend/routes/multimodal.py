from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
from typing import Any, Dict

from services.stt_service import transcribe_audio_placeholder

router = APIRouter(prefix="/api/multimodal", tags=["multimodal"])


class STTResponse(BaseModel):
    transcript: str
    language: str


@router.post("/stt", response_model=STTResponse)
async def speech_to_text(
    audio: UploadFile = File(...),
    language: str = Form("en"),
):
    """
    Basic speech-to-text endpoint.

    Currently uses a placeholder that returns a fixed message but keeps the
    contract ready for plugging in a real STT backend that supports Indian
    languages.
    """
    try:
        content = await audio.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read audio: {exc}")

    transcript = transcribe_audio_placeholder(content, language=language)
    return STTResponse(transcript=transcript, language=language)

