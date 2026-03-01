from datetime import datetime
from typing import Any, Dict, Optional

from mongo_client import get_mongo_db


def log_event(event_type: str, payload: Dict[str, Any]) -> None:
    """
    Lightweight audit/telemetry logger.

    Writes to MongoDB if configured, otherwise no-ops except for a debug print.
    This is intended for:
    - model inferences
    - triage/emergency decisions
    - user-facing recommendation generation
    """
    doc = {
        "event_type": event_type,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    db = get_mongo_db()
    if db is None:
        # Safe fallback: avoid breaking flows if Mongo is unavailable
        print(f"[audit_log] {doc}")
        return

    try:
        db.audit_logs.insert_one(doc)
    except Exception as exc:
        # Never raise from logging
        print(f"[audit_log_error] {exc}")

