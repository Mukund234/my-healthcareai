from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.user import User
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Pydantic schema for profile updates
class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    avatar_url: Optional[str] = None

@router.get("/me")
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Get the currently authenticated user's profile.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "avatar_url": current_user.avatar_url,
        "age": current_user.age,
        "gender": current_user.gender,
        "is_premium": current_user.is_premium
    }

@router.put("/profile")
async def update_profile(
    profile_data: ProfileUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the authenticated user's profile data.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    # Update provided fields
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    if profile_data.age is not None:
        current_user.age = profile_data.age
    if profile_data.gender is not None:
        current_user.gender = profile_data.gender
    if profile_data.avatar_url is not None:
        current_user.avatar_url = profile_data.avatar_url
        
    db.commit()
    db.refresh(current_user)
    
    return {
        "status": "success",
        "message": "Profile updated successfully",
        "user": {
            "full_name": current_user.full_name,
            "age": current_user.age,
            "gender": current_user.gender
        }
    }
