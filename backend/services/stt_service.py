from typing import Optional


def transcribe_audio_placeholder(file_bytes: bytes, language: str = "en") -> str:
    """
    Placeholder speech-to-text function.

    In production you should integrate a real STT provider (e.g., cloud API
    that supports Indian languages like Hindi, Tamil, etc.).

    For now this returns a static message so the API contract is stable.
    """
    _ = file_bytes  # unused in placeholder
    if language == "hi":
        return "यह स्पीच-टू-टेक्स्ट प्लेसहोल्डर है। असली सिस्टम में यहाँ आपकी आवाज़ का ट्रांसक्रिप्शन होगा।"
    return "This is a speech-to-text placeholder. In the real system, your audio transcription will appear here."

