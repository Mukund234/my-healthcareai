"""
Conversation engine for health assessment chatbot.
Rule-based conversational AI without OpenAI dependency.
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class ConversationEngine:
    def __init__(self):
        self.conversation_state = {}
        self.question_flow = self._build_question_flow()
    
    def _build_question_flow(self) -> List[Dict]:
        """Define the conversation flow with questions"""
        return [
            {
                "id": "welcome",
                "type": "greeting",
                "message": "👋 Hi! I'm your AI health assistant. I'll help assess your health risks based on WHO guidelines.\n\nThis will take about 5-7 minutes. Your information is confidential and will help me provide personalized health insights.\n\nLet's start - what's your name?",
                "data_field": "name",
                "validation": "text"
            },
            {
                "id": "age",
                "type": "question",
                "message": "Nice to meet you, {name}! How old are you?",
                "data_field": "age",
                "validation": "number",
                "range": (0, 120)
            },
            {
                "id": "gender",
                "type": "question",
                "message": "What's your gender?",
                "data_field": "gender",
                "validation": "choice",
                "options": ["Male", "Female", "Other"],
                "quick_replies": True
            },
            {
                "id": "height",
                "type": "question",
                "message": "What's your height in centimeters?",
                "data_field": "height_cm",
                "validation": "number",
                "range": (50, 250)
            },
            {
                "id": "weight",
                "type": "question",
                "message": "And your weight in kilograms?",
                "data_field": "weight_kg",
                "validation": "number",
                "range": (20, 300)
            },
            {
                "id": "activity",
                "type": "question",
                "message": "How would you describe your physical activity level?",
                "data_field": "activity_level",
                "validation": "choice",
                "options": ["Sedentary (little to no exercise)", "Light (1-2 days/week)", "Moderate (3-5 days/week)", "Active (6-7 days/week)", "Very Active (athlete level)"],
                "quick_replies": True
            },
            {
                "id": "sleep",
                "type": "question",
                "message": "On average, how many hours do you sleep per night?",
                "data_field": "sleep_hours",
                "validation": "number",
                "range": (0, 24)
            },
            {
                "id": "smoking",
                "type": "question",
                "message": "Do you smoke or use tobacco products?",
                "data_field": "smoking",
                "validation": "boolean",
                "options": ["Yes", "No"],
                "quick_replies": True
            },
            {
                "id": "alcohol",
                "type": "question",
                "message": "How often do you consume alcohol?",
                "data_field": "alcohol_consumption",
                "validation": "choice",
                "options": ["Never", "Occasionally (1-2 times/month)", "Moderate (1-2 times/week)", "Frequently (3+ times/week)"],
                "quick_replies": True
            },
            {
                "id": "family_history",
                "type": "question",
                "message": "Does anyone in your immediate family (parents, siblings) have any of these conditions? You can mention multiple.\n\n- Diabetes\n- Hypertension (High blood pressure)\n- Heart disease\n- Cancer",
                "data_field": "family_history",
                "validation": "multi_choice",
                "extract_keywords": ["diabetes", "hypertension", "high blood pressure", "heart disease", "heart", "cancer"]
            },
            {
                "id": "existing_conditions",
                "type": "question",
                "message": "Do you have any existing health conditions or chronic illnesses? Please describe them, or type 'none' if you don't have any.",
                "data_field": "existing_conditions",
                "validation": "text"
            },
            {
                "id": "medications",
                "type": "question",
                "message": "Are you currently taking any medications? Please list them, or type 'none'.",
                "data_field": "medications",
                "validation": "text"
            },
            {
                "id": "blood_pressure",
                "type": "question",
                "message": "If you know your blood pressure, please share it (e.g., '120/80'). Otherwise, type 'unknown'.",
                "data_field": "blood_pressure",
                "validation": "blood_pressure",
                "optional": True
            },
            {
                "id": "stress",
                "type": "question",
                "message": "On a scale of 1-10, how would you rate your stress level? (1 = very relaxed, 10 = extremely stressed)",
                "data_field": "stress_level",
                "validation": "number",
                "range": (1, 10)
            },
            {
                "id": "symptoms",
                "type": "question",
                "message": "Now, please describe any symptoms or health concerns you're experiencing. Take your time and be as detailed as you'd like.\n\nFor example: fatigue, headaches, dizziness, chest pain, etc.",
                "data_field": "symptoms",
                "validation": "text"
            },
            {
                "id": "complete",
                "type": "completion",
                "message": "Thank you for sharing all this information, {name}! I'm now analyzing your health data based on WHO guidelines. This will take just a moment...",
                "action": "analyze"
            }
        ]
    
    def start_conversation(self, user_id: str) -> Dict:
        """Initialize a new conversation"""
        conversation_id = f"conv_{user_id}_{int(datetime.now().timestamp())}"
        
        self.conversation_state[conversation_id] = {
            "user_id": user_id,
            "current_step": 0,
            "collected_data": {},
            "messages": [],
            "started_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        first_question = self.question_flow[0]
        response = {
            "conversation_id": conversation_id,
            "message": first_question["message"],
            "type": first_question["type"],
            "quick_replies": self._get_quick_replies(first_question)
        }
        
        # Store AI message
        self.conversation_state[conversation_id]["messages"].append({
            "role": "assistant",
            "content": first_question["message"],
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def process_message(self, conversation_id: str, user_message: str) -> Dict:
        """Process user message and return next question"""
        if conversation_id not in self.conversation_state:
            return {"error": "Conversation not found"}
        
        state = self.conversation_state[conversation_id]
        current_step = state["current_step"]
        current_question = self.question_flow[current_step]
        
        # Store user message
        state["messages"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Extract and validate data
        extracted_data, is_valid, error_message = self._extract_and_validate(
            user_message, current_question
        )
        
        if not is_valid:
            # Ask for clarification
            response = {
                "conversation_id": conversation_id,
                "message": f"{error_message}\n\n{current_question['message']}",
                "type": "clarification",
                "quick_replies": self._get_quick_replies(current_question)
            }
            
            state["messages"].append({
                "role": "assistant",
                "content": response["message"],
                "timestamp": datetime.now().isoformat()
            })
            
            return response
        
        # Store extracted data
        state["collected_data"].update(extracted_data)
        
        # Move to next question
        state["current_step"] += 1
        
        # Check if conversation is complete
        if state["current_step"] >= len(self.question_flow):
            state["status"] = "completed"
            return {
                "conversation_id": conversation_id,
                "message": "Thank you! I have all the information I need.",
                "type": "completion",
                "action": "analyze",
                "collected_data": state["collected_data"]
            }
        
        # Get next question
        next_question = self.question_flow[state["current_step"]]
        next_message = self._format_message(next_question["message"], state["collected_data"])
        
        response = {
            "conversation_id": conversation_id,
            "message": next_message,
            "type": next_question["type"],
            "quick_replies": self._get_quick_replies(next_question)
        }
        
        state["messages"].append({
            "role": "assistant",
            "content": next_message,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def _extract_and_validate(self, user_input: str, question: Dict) -> Tuple[Dict, bool, str]:
        """Extract data from user input and validate"""
        validation_type = question["validation"]
        data_field = question["data_field"]
        
        # Text validation
        if validation_type == "text":
            if len(user_input.strip()) < 2:
                return {}, False, "Please provide a valid response."
            return {data_field: user_input.strip()}, True, ""
        
        # Number validation
        elif validation_type == "number":
            try:
                number = float(re.search(r'\d+\.?\d*', user_input).group())
                if "range" in question:
                    min_val, max_val = question["range"]
                    if not (min_val <= number <= max_val):
                        return {}, False, f"Please provide a number between {min_val} and {max_val}."
                return {data_field: number}, True, ""
            except:
                return {}, False, "Please provide a valid number."
        
        # Boolean validation
        elif validation_type == "boolean":
            user_lower = user_input.lower()
            if any(word in user_lower for word in ["yes", "y", "true", "1"]):
                return {data_field: True}, True, ""
            elif any(word in user_lower for word in ["no", "n", "false", "0", "never"]):
                return {data_field: False}, True, ""
            else:
                return {}, False, "Please answer with 'yes' or 'no'."
        
        # Choice validation
        elif validation_type == "choice":
            user_lower = user_input.lower()
            for option in question["options"]:
                if option.lower() in user_lower or user_lower in option.lower():
                    # Map to simplified value
                    value = self._map_choice_value(data_field, option)
                    return {data_field: value}, True, ""
            return {}, False, f"Please choose one of the options: {', '.join(question['options'])}"
        
        # Multi-choice validation (family history)
        elif validation_type == "multi_choice":
            user_lower = user_input.lower()
            if "none" in user_lower or "no" in user_lower:
                return {data_field: {}}, True, ""
            
            extracted = {}
            keywords = question.get("extract_keywords", [])
            for keyword in keywords:
                if keyword in user_lower:
                    if keyword in ["high blood pressure", "hypertension"]:
                        extracted["hypertension"] = True
                    elif keyword in ["heart disease", "heart"]:
                        extracted["heart_disease"] = True
                    else:
                        extracted[keyword] = True
            
            return {data_field: extracted}, True, ""
        
        # Blood pressure validation
        elif validation_type == "blood_pressure":
            if "unknown" in user_input.lower() or "don't know" in user_input.lower():
                return {}, True, ""
            
            match = re.search(r'(\d{2,3})\s*/\s*(\d{2,3})', user_input)
            if match:
                systolic = int(match.group(1))
                diastolic = int(match.group(2))
                return {
                    "blood_pressure_systolic": systolic,
                    "blood_pressure_diastolic": diastolic
                }, True, ""
            else:
                return {}, False, "Please provide blood pressure in format '120/80' or type 'unknown'."
        
        return {}, False, "Invalid input."
    
    def _map_choice_value(self, field: str, option: str) -> str:
        """Map user-friendly options to database values"""
        mappings = {
            "activity_level": {
                "Sedentary (little to no exercise)": "sedentary",
                "Light (1-2 days/week)": "light",
                "Moderate (3-5 days/week)": "moderate",
                "Active (6-7 days/week)": "active",
                "Very Active (athlete level)": "very_active"
            },
            "alcohol_consumption": {
                "Never": "none",
                "Occasionally (1-2 times/month)": "occasional",
                "Moderate (1-2 times/week)": "moderate",
                "Frequently (3+ times/week)": "heavy"
            },
            "gender": {
                "Male": "male",
                "Female": "female",
                "Other": "other"
            }
        }
        
        if field in mappings and option in mappings[field]:
            return mappings[field][option]
        return option.lower()
    
    def _get_quick_replies(self, question: Dict) -> Optional[List[str]]:
        """Get quick reply options if available"""
        if question.get("quick_replies") and "options" in question:
            return question["options"]
        return None
    
    def _format_message(self, message: str, data: Dict) -> str:
        """Format message with collected data"""
        try:
            return message.format(**data)
        except:
            return message
    
    def get_conversation_data(self, conversation_id: str) -> Optional[Dict]:
        """Get collected data from conversation"""
        if conversation_id in self.conversation_state:
            return self.conversation_state[conversation_id]["collected_data"]
        return None
    
    def get_conversation_history(self, conversation_id: str) -> Optional[List[Dict]]:
        """Get message history"""
        if conversation_id in self.conversation_state:
            return self.conversation_state[conversation_id]["messages"]
        return None
