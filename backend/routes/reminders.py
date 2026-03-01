from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models.medication_reminder import MedicationReminder

router = APIRouter(prefix="/api/reminders", tags=["reminders"])


class ReminderCreateRequest(BaseModel):
    user_id: Optional[int] = None
    name: str = Field(..., min_length=1)
    dosage: Optional[str] = None
    frequency: str = Field(..., min_length=3)
    time_of_day: Optional[str] = Field(
        default=None,
        description="24h time like '08:00' or '21:30'",
    )


class ReminderResponse(BaseModel):
    id: int
    user_id: Optional[int]
    name: str
    dosage: Optional[str]
    frequency: str
    time_of_day: Optional[str]
    active: bool

    class Config:
        from_attributes = True


@router.post("/", response_model=ReminderResponse)
async def create_reminder(
    payload: ReminderCreateRequest,
    db: Session = Depends(get_db),
):
    reminder = MedicationReminder(
        user_id=payload.user_id,
        name=payload.name,
        dosage=payload.dosage,
        frequency=payload.frequency,
        time_of_day=payload.time_of_day,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


@router.get("/", response_model=List[ReminderResponse])
async def list_reminders(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(MedicationReminder).filter(MedicationReminder.active == True)
    if user_id is not None:
        query = query.filter(MedicationReminder.user_id == user_id)
    reminders = query.order_by(MedicationReminder.created_at.desc()).all()
    return reminders


@router.post("/{reminder_id}/deactivate", response_model=ReminderResponse)
async def deactivate_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
):
    reminder = (
        db.query(MedicationReminder)
        .filter(MedicationReminder.id == reminder_id)
        .first()
    )
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    reminder.active = False
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

