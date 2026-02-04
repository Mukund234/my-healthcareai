"""
Doctor consultation routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models.doctor import Doctor, Appointment
import json

router = APIRouter(prefix="/api/doctors", tags=["doctors"])

# Request/Response Models
class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    qualification: str
    experience_years: int
    rating: float
    consultation_fee: int
    available: bool
    profile_image: Optional[str]
    languages: str
    about: Optional[str]
    total_consultations: int
    
    class Config:
        from_attributes = True

class AppointmentRequest(BaseModel):
    doctor_id: int
    patient_name: str
    patient_age: int
    patient_gender: str
    appointment_date: str  # ISO format
    appointment_type: str  # video, audio, chat
    symptoms: Optional[str] = None
    ai_assessment: Optional[dict] = None

class AppointmentResponse(BaseModel):
    id: int
    doctor: DoctorResponse
    patient_name: str
    appointment_date: datetime
    appointment_type: str
    status: str
    payment_status: str
    payment_amount: int
    meeting_link: Optional[str]
    
    class Config:
        from_attributes = True

@router.get("/list", response_model=List[DoctorResponse])
async def get_doctors(
    specialization: Optional[str] = None,
    available_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get list of available doctors
    """
    query = db.query(Doctor)
    
    if specialization:
        query = query.filter(Doctor.specialization == specialization)
    
    if available_only:
        query = query.filter(Doctor.available == True)
    
    doctors = query.order_by(Doctor.rating.desc()).all()
    return doctors

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get doctor details
    """
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return doctor

@router.post("/book-appointment", response_model=AppointmentResponse)
async def book_appointment(
    request: AppointmentRequest,
    db: Session = Depends(get_db)
):
    """
    Book an appointment with a doctor
    """
    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == request.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Create appointment
    appointment = Appointment(
        user_id="demo_user",  # Replace with actual user ID when auth is implemented
        patient_name=request.patient_name,
        patient_age=request.patient_age,
        patient_gender=request.patient_gender,
        doctor_id=request.doctor_id,
        appointment_date=datetime.fromisoformat(request.appointment_date),
        appointment_type=request.appointment_type,
        symptoms=request.symptoms,
        ai_assessment=json.dumps(request.ai_assessment) if request.ai_assessment else None,
        payment_amount=doctor.consultation_fee,
        meeting_link=f"https://meet.example.com/{doctor.id}-{datetime.now().timestamp()}"  # Mock meeting link
    )
    
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    # Update doctor stats
    doctor.total_consultations += 1
    db.commit()
    
    return appointment

@router.get("/appointments/{user_id}", response_model=List[AppointmentResponse])
async def get_user_appointments(user_id: str, db: Session = Depends(get_db)):
    """
    Get user's appointments
    """
    appointments = db.query(Appointment).filter(
        Appointment.user_id == user_id
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return appointments

@router.get("/specializations", response_model=List[str])
async def get_specializations(db: Session = Depends(get_db)):
    """
    Get list of available specializations
    """
    specializations = db.query(Doctor.specialization).distinct().all()
    return [s[0] for s in specializations]
