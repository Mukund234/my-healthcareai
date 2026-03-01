from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)  # male, female, other
    is_premium = Column(Boolean, default=False)
    
    # Consent and Privacy
    consent_given = Column(Boolean, default=False)
    data_sharing_consent = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        name_display = self.full_name or self.email or f"User {self.id}"
        return f"<{name_display} - Age: {self.age}, Premium: {self.is_premium}>"
