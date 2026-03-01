"""
Structured questionnaire schema for low-resource health risk screening.
"""

from typing import Dict, List


def get_questionnaire_schema() -> Dict:
    questions: List[Dict] = [
        {
            "id": "age",
            "question": "What is your age?",
            "type": "number",
            "required": True,
            "min": 0,
            "max": 120
        },
        {
            "id": "gender",
            "question": "What is your gender?",
            "type": "single_choice",
            "required": True,
            "options": ["male", "female", "other"]
        },
        {
            "id": "height_cm",
            "question": "What is your height in centimeters?",
            "type": "number",
            "required": True,
            "min": 50,
            "max": 250
        },
        {
            "id": "weight_kg",
            "question": "What is your weight in kilograms?",
            "type": "number",
            "required": True,
            "min": 20,
            "max": 300
        },
        {
            "id": "activity_level",
            "question": "How active are you in a typical week?",
            "type": "single_choice",
            "required": True,
            "options": ["sedentary", "light", "moderate", "active", "very_active"]
        },
        {
            "id": "sleep_hours",
            "question": "How many hours do you sleep at night?",
            "type": "number",
            "required": True,
            "min": 0,
            "max": 24
        },
        {
            "id": "smoking",
            "question": "Do you smoke or use tobacco?",
            "type": "boolean",
            "required": True
        },
        {
            "id": "alcohol_consumption",
            "question": "How often do you consume alcohol?",
            "type": "single_choice",
            "required": False,
            "options": ["none", "occasional", "moderate", "heavy", "unknown"]
        },
        {
            "id": "family_history",
            "question": "Any family history of diabetes, high blood pressure, or heart disease?",
            "type": "multi_choice",
            "required": False,
            "options": ["diabetes", "hypertension", "heart_disease", "none", "unknown"]
        },
        {
            "id": "blood_pressure_systolic",
            "question": "Do you know your latest upper blood pressure value (systolic)?",
            "type": "number",
            "required": False,
            "min": 70,
            "max": 240
        },
        {
            "id": "stress_level",
            "question": "Rate your stress from 1 (low) to 10 (high).",
            "type": "number",
            "required": True,
            "min": 1,
            "max": 10
        },
        {
            "id": "symptoms",
            "question": "What symptoms are you feeling now?",
            "type": "free_text",
            "required": False,
            "placeholder": "e.g., fever, cough, dizziness, chest pain"
        }
    ]

    return {
        "name": "Early Health Risk Screening Questionnaire",
        "version": "1.0",
        "target_user": "community screening in low-resource settings",
        "estimated_time_minutes": 4,
        "questions": questions
    }
