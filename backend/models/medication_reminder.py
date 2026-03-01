from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from database import Base


class MedicationReminder(Base):
    __tablename__ = "medication_reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    name = Column(String, nullable=False)  # e.g. "Metformin 500mg"
    dosage = Column(String, nullable=True)
    frequency = Column(String, nullable=False)  # e.g. "once_daily", "twice_daily"
    time_of_day = Column(String, nullable=True)  # e.g. "08:00", "21:00"

    # Simple adherence tracking
    active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

