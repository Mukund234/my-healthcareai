"""
Conversational Assessment API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from database import get_db
from ai.conversation_engine import ConversationEngine
from risk_engine.risk_calculator import RiskCalculator
from models.user import User
from models.risk_result import RiskResult
from datetime import datetime
import json

router = APIRouter(prefix="/api/conversation", tags=["conversation"])

# Initialize conversation engine (in-memory for now)
conversation_engine = ConversationEngine()

# Request/Response Models
class ConversationStartRequest(BaseModel):
    user_id: Optional[str] = "anonymous"

class ConversationMessageRequest(BaseModel):
    conversation_id: str
    message: str

class ConversationMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str

class ConversationResponse(BaseModel):
    conversation_id: str
    message: str
    type: str
    quick_replies: Optional[List[str]] = None
    action: Optional[str] = None
    collected_data: Optional[dict] = None
    risk_results: Optional[dict] = None

@router.post("/start", response_model=ConversationResponse)
async def start_conversation(request: ConversationStartRequest, db: Session = Depends(get_db)):
    """
    Start a new conversational health assessment
    """
    try:
        response = conversation_engine.start_conversation(request.user_id)
        return ConversationResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/message", response_model=ConversationResponse)
async def send_message(request: ConversationMessageRequest, db: Session = Depends(get_db)):
    """
    Process user message and get AI response
    """
    try:
        response = conversation_engine.process_message(
            request.conversation_id,
            request.message
        )
        
        if "error" in response:
            raise HTTPException(status_code=404, detail=response["error"])
        
        # If conversation is complete, trigger analysis
        if response.get("action") == "analyze":
            collected_data = response.get("collected_data", {})
            
            # Perform risk assessment
            risk_calculator = RiskCalculator()
            risk_results = risk_calculator.calculate_all_risks(collected_data)
            
            # Generate personalized recommendations
            from ai.recommendation_engine import RecommendationEngine
            rec_engine = RecommendationEngine()
            recommendations = rec_engine.generate_recommendations(risk_results, collected_data)
            
            # Save to Firebase Cloud Storage
            try:
                from services.firebase_service import get_firebase_service
                firebase = get_firebase_service()
                
                # Get conversation history
                conversation_history = conversation_engine.get_conversation_history(request.conversation_id)
                
                # Prepare conversation data for cloud storage
                conversation_data = {
                    "conversation_id": request.conversation_id,
                    "messages": conversation_history,
                    "collected_data": collected_data,
                    "risk_results": risk_results,
                    "recommendations": recommendations,
                    "status": "completed"
                }
                
                # Save conversation to Firestore
                user_id = collected_data.get('name', 'anonymous')  # Use actual user_id when auth is implemented
                firebase_conv_id = firebase.save_conversation(user_id, conversation_data)
                
                # Save recommendations
                firebase.save_health_recommendations(user_id, recommendations)
                
                # Schedule notifications
                for notification in recommendations.get("notifications", []):
                    firebase.schedule_notification(user_id, notification)
                
                print(f"✅ Conversation saved to cloud: {firebase_conv_id}")
            
            except Exception as e:
                print(f"⚠️ Firebase save failed (continuing anyway): {e}")
            
            # Store results in database (if user is authenticated)
            # For now, just return the results
            response["risk_results"] = risk_results
            response["recommendations"] = recommendations
            response["message"] += f"\n\n✅ Analysis complete! Here's your health risk assessment:\n\n"
            
            # Format results - use correct structure
            risk_scores = risk_results.get('risk_scores', {})
            severity_levels = risk_results.get('severity_levels', {})
            
            for risk_type, score in risk_scores.items():
                severity_key = risk_type.replace('_risk', '_severity')
                severity = severity_levels.get(severity_key, 'unknown')
                emoji = "🟢" if severity == "low" else "🟡" if severity == "moderate" else "🔴"
                response["message"] += f"{emoji} **{risk_type.replace('_', ' ').title()}**: {severity.upper()} (Score: {score:.2f})\n"
            
            # Add top recommendations
            response["message"] += "\n\n💡 **Personalized Recommendations:**\n\n"
            
            if recommendations["exercise"]:
                response["message"] += "**🏃 Exercise:**\n"
                for ex in recommendations["exercise"][:2]:
                    response["message"] += f"• {ex['name']} - {ex['duration']}, {ex['frequency']}\n"
            
            if recommendations["nutrition"]:
                response["message"] += "\n**🥗 Nutrition:**\n"
                for food in recommendations["nutrition"][:2]:
                    response["message"] += f"• {food['category']}: {', '.join(food['foods'][:3])}\n"
            
            # Add doctor consultation option
            overall_severity = risk_results.get('overall_severity', 'low')
            if overall_severity in ['high', 'moderate']:
                response["message"] += "\n\n👨‍⚕️ **Consult a Doctor:**\n"
                response["message"] += "Based on your assessment, we recommend consulting with a healthcare professional.\n"
                response["message"] += "📱 Book an online consultation with our verified doctors - available 24/7!\n"
                response["show_doctor_consultation"] = True
            
            response["message"] += "\n📱 You'll receive personalized health notifications to help you stay on track!"
        
        return ConversationResponse(**response)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """
    Get conversation message history
    """
    try:
        messages = conversation_engine.get_conversation_history(conversation_id)
        
        if messages is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "conversation_id": conversation_id,
            "messages": messages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/{conversation_id}")
async def get_collected_data(conversation_id: str):
    """
    Get collected health data from conversation
    """
    try:
        data = conversation_engine.get_conversation_data(conversation_id)
        
        if data is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "conversation_id": conversation_id,
            "collected_data": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
