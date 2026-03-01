from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from services.firebase_service import get_firebase_service

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Dependency to verify Firebase ID token and return the corresponding database User.
    """
    token = credentials.credentials
    
    # Ensure Firebase is initialized
    firebase_service = get_firebase_service()
    if not firebase_service.initialized:
        # Fallback for local development if Firebase isn't configured
        return db.query(User).first() or None
        
    try:
        # Verify the custom token using Firebase Admin SDK
        decoded_token = auth.verify_id_token(token)
        email = decoded_token.get('email')
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials (no email found)",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Find the user in our local database
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Auto-create basic user record if they exist in Firebase but not in our DB
            user = User(
                email=email,
                full_name=decoded_token.get('name', ''),
                avatar_url=decoded_token.get('picture', '')
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
