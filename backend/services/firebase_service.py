"""
Firebase service for cloud storage and push notifications
Handles Firestore database and Firebase Cloud Messaging
"""

import firebase_admin
from firebase_admin import credentials, firestore, messaging
from typing import Dict, List, Optional
from datetime import datetime
import os
import json

class FirebaseService:
    def __init__(self):
        self.db = None
        self.initialized = False
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase credentials are available
            cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
            
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.initialized = True
                print("✅ Firebase initialized successfully")
            else:
                print("ℹ️ Firebase credentials not found - cloud storage disabled")
                print("   Set FIREBASE_CREDENTIALS_PATH in .env to enable")
        except Exception as e:
            print(f"⚠️ Firebase initialization failed: {e}")
            self.initialized = False
    
    def save_conversation(self, user_id: str, conversation_data: Dict) -> Optional[str]:
        """Save conversation to Firestore"""
        if not self.initialized:
            print("Firebase not initialized - conversation not saved to cloud")
            return None
        
        try:
            # Add metadata
            conversation_data['user_id'] = user_id
            conversation_data['created_at'] = firestore.SERVER_TIMESTAMP
            conversation_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            # Save to Firestore
            doc_ref = self.db.collection('conversations').add(conversation_data)
            conversation_id = doc_ref[1].id
            
            print(f"✅ Conversation saved to Firestore: {conversation_id}")
            return conversation_id
        
        except Exception as e:
            print(f"⚠️ Failed to save conversation: {e}")
            return None
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Retrieve conversation from Firestore"""
        if not self.initialized:
            return None
        
        try:
            doc_ref = self.db.collection('conversations').document(conversation_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
        
        except Exception as e:
            print(f"⚠️ Failed to retrieve conversation: {e}")
            return None
    
    def get_user_conversations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get all conversations for a user"""
        if not self.initialized:
            return []
        
        try:
            conversations = []
            docs = self.db.collection('conversations')\
                .where('user_id', '==', user_id)\
                .order_by('created_at', direction=firestore.Query.DESCENDING)\
                .limit(limit)\
                .stream()
            
            for doc in docs:
                conv_data = doc.to_dict()
                conv_data['id'] = doc.id
                conversations.append(conv_data)
            
            return conversations
        
        except Exception as e:
            print(f"⚠️ Failed to retrieve conversations: {e}")
            return []
    
    def save_user_profile(self, user_id: str, profile_data: Dict) -> bool:
        """Save or update user profile"""
        if not self.initialized:
            return False
        
        try:
            profile_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            self.db.collection('users').document(user_id).set(
                profile_data,
                merge=True  # Update existing fields, add new ones
            )
            
            print(f"✅ User profile saved: {user_id}")
            return True
        
        except Exception as e:
            print(f"⚠️ Failed to save user profile: {e}")
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile"""
        if not self.initialized:
            return None
        
        try:
            doc_ref = self.db.collection('users').document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
        
        except Exception as e:
            print(f"⚠️ Failed to retrieve user profile: {e}")
            return None
    
    def save_health_recommendations(self, user_id: str, recommendations: Dict) -> bool:
        """Save personalized health recommendations"""
        if not self.initialized:
            return False
        
        try:
            rec_data = {
                'user_id': user_id,
                'recommendations': recommendations,
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            self.db.collection('recommendations').add(rec_data)
            
            print(f"✅ Recommendations saved for user: {user_id}")
            return True
        
        except Exception as e:
            print(f"⚠️ Failed to save recommendations: {e}")
            return False
    
    def schedule_notification(self, user_id: str, notification: Dict) -> bool:
        """Schedule a push notification"""
        if not self.initialized:
            return False
        
        try:
            notification_data = {
                'user_id': user_id,
                'title': notification.get('title'),
                'body': notification.get('body'),
                'schedule': notification.get('schedule'),
                'status': 'pending',
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            self.db.collection('notifications').add(notification_data)
            
            print(f"✅ Notification scheduled: {notification.get('title')}")
            return True
        
        except Exception as e:
            print(f"⚠️ Failed to schedule notification: {e}")
            return False
    
    def send_push_notification(self, fcm_token: str, title: str, body: str, data: Optional[Dict] = None) -> bool:
        """Send immediate push notification via FCM"""
        if not self.initialized:
            return False
        
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=fcm_token
            )
            
            response = messaging.send(message)
            print(f"✅ Push notification sent: {response}")
            return True
        
        except Exception as e:
            print(f"⚠️ Failed to send push notification: {e}")
            return False
    
    def save_fcm_token(self, user_id: str, fcm_token: str) -> bool:
        """Save user's FCM token for push notifications"""
        if not self.initialized:
            return False
        
        try:
            self.db.collection('users').document(user_id).set({
                'fcm_token': fcm_token,
                'token_updated_at': firestore.SERVER_TIMESTAMP
            }, merge=True)
            
            print(f"✅ FCM token saved for user: {user_id}")
            return True
        
        except Exception as e:
            print(f"⚠️ Failed to save FCM token: {e}")
            return False

# Singleton instance
_firebase_service = None

def get_firebase_service() -> FirebaseService:
    """Get Firebase service instance"""
    global _firebase_service
    if _firebase_service is None:
        _firebase_service = FirebaseService()
    return _firebase_service
