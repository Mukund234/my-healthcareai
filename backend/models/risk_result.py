from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class RiskResult(Base):
    __tablename__ = "risk_results"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("health_assessments.id"), nullable=False)
    
    # Risk Scores (0-1 scale)
    diabetes_risk = Column(Float, default=0.0)
    hypertension_risk = Column(Float, default=0.0)
    cardiovascular_risk = Column(Float, default=0.0)
    obesity_risk = Column(Float, default=0.0)
    stress_burnout_risk = Column(Float, default=0.0)
    
    # Severity Levels
    diabetes_severity = Column(String)  # low, moderate, high
    hypertension_severity = Column(String)
    cardiovascular_severity = Column(String)
    obesity_severity = Column(String)
    stress_severity = Column(String)
    
    # Overall Risk
    overall_risk_score = Column(Float, default=0.0)
    overall_severity = Column(String)
    
    # Recommendations
    recommendations = Column(JSON)  # List of personalized recommendations
    doctor_consult_needed = Column(String)  # none, suggested, urgent
    
    # Explanations (LLM-generated)
    explanation_text = Column(Text)
    explanation_language = Column(String, default="en")  # en, hi
    
    # Model Info
    model_version = Column(String)
    calculation_method = Column(String)  # who_rules, ml_model, hybrid
    
    # Explainability
    shap_values = Column(JSON, nullable=True)  # SHAP feature importance
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    assessment = relationship("HealthAssessment", back_populates="risk_results")
    
    def __repr__(self):
        return f"<RiskResult {self.id} - Assessment: {self.assessment_id}, Overall: {self.overall_severity}>"
