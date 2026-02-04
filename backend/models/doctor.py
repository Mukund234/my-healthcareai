"""
Doctor consultation models and database
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    qualification = Column(String, nullable=False)
    experience_years = Column(Integer, nullable=False)
    rating = Column(Float, default=4.5)
    consultation_fee = Column(Integer, nullable=False)  # in rupees
    available = Column(Boolean, default=True)
    profile_image = Column(String, nullable=True)
    languages = Column(String, nullable=False)  # comma-separated
    about = Column(Text, nullable=True)
    
    # Contact info
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    
    # Availability
    available_days = Column(String, nullable=False)  # JSON string
    available_hours = Column(String, nullable=False)  # JSON string
    
    # Stats
    total_consultations = Column(Integer, default=0)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    
    created_at = Column(DateTime, default=datetime.utcnow)

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Patient info
    user_id = Column(String, nullable=False)
    patient_name = Column(String, nullable=False)
    patient_age = Column(Integer, nullable=False)
    patient_gender = Column(String, nullable=False)
    
    # Doctor
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    doctor = relationship("Doctor", back_populates="appointments")
    
    # Appointment details
    appointment_date = Column(DateTime, nullable=False)
    appointment_type = Column(String, nullable=False)  # video, audio, chat
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    
    # Medical info
    symptoms = Column(Text, nullable=True)
    ai_assessment = Column(Text, nullable=True)  # JSON string
    doctor_notes = Column(Text, nullable=True)
    prescription = Column(Text, nullable=True)
    
    # Payment
    payment_status = Column(String, default="pending")  # pending, paid, refunded
    payment_amount = Column(Integer, nullable=False)
    
    # Meeting link
    meeting_link = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
