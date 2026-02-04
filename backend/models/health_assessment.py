from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class HealthAssessment(Base):
    __tablename__ = "health_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Basic Info
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    
    # Lifestyle
    activity_level = Column(String)  # sedentary, light, moderate, active, very_active
    sleep_hours = Column(Float)
    smoking = Column(Boolean, default=False)
    alcohol_consumption = Column(String)  # none, occasional, moderate, heavy
    
    # Diet
    diet_type = Column(String)  # balanced, vegetarian, vegan, high_protein, etc.
    water_intake_liters = Column(Float)
    fast_food_frequency = Column(String)  # daily, weekly, monthly, rarely, never
    
    # Medical History
    family_history = Column(JSON)  # {"diabetes": true, "hypertension": true, etc.}
    existing_conditions = Column(JSON)  # List of existing conditions
    medications = Column(JSON)  # List of current medications
    
    # Symptoms (self-reported)
    symptoms = Column(JSON)  # List of current symptoms
    stress_level = Column(Integer)  # 1-10 scale
    
    # Additional Data
    blood_pressure_systolic = Column(Integer, nullable=True)
    blood_pressure_diastolic = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    risk_results = relationship("RiskResult", back_populates="assessment")
    
    def __repr__(self):
        return f"<HealthAssessment {self.id} - User: {self.user_id}>"
