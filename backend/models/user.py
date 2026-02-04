from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)  # male, female, other
    
    # Consent and Privacy
    consent_given = Column(Boolean, default=False)
    data_sharing_consent = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User {self.id} - Age: {self.age}, Gender: {self.gender}>"
