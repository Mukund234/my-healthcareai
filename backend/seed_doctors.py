"""
Seed database with mock doctors for hackathon demo
"""

from sqlalchemy.orm import Session
from models.doctor import Doctor
from database import SessionLocal
import json

def seed_doctors():
    """Add mock doctors to database"""
    db = SessionLocal()
    
    # Check if doctors already exist
    existing = db.query(Doctor).first()
    if existing:
        print("Doctors already seeded")
        return
    
    mock_doctors = [
        {
            "name": "Dr. Priya Sharma",
            "specialization": "General Physician",
            "qualification": "MBBS, MD (Internal Medicine)",
            "experience_years": 12,
            "rating": 4.8,
            "consultation_fee": 500,
            "available": True,
            "profile_image": "https://randomuser.me/api/portraits/women/1.jpg",
            "languages": "English, Hindi, Marathi",
            "about": "Experienced general physician specializing in preventive care and chronic disease management. Passionate about making healthcare accessible to all.",
            "email": "dr.priya@healthai.com",
            "phone": "+91 98765 43210",
            "available_days": json.dumps(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]),
            "available_hours": json.dumps({"start": "09:00", "end": "18:00"}),
            "total_consultations": 1250
        },
        {
            "name": "Dr. Rajesh Kumar",
            "specialization": "Cardiologist",
            "qualification": "MBBS, MD, DM (Cardiology)",
            "experience_years": 15,
            "rating": 4.9,
            "consultation_fee": 800,
            "available": True,
            "profile_image": "https://randomuser.me/api/portraits/men/2.jpg",
            "languages": "English, Hindi, Tamil",
            "about": "Senior cardiologist with expertise in heart disease prevention and treatment. Available for emergency consultations.",
            "email": "dr.rajesh@healthai.com",
            "phone": "+91 98765 43211",
            "available_days": json.dumps(["Monday", "Wednesday", "Friday", "Saturday"]),
            "available_hours": json.dumps({"start": "10:00", "end": "17:00"}),
            "total_consultations": 2100
        },
        {
            "name": "Dr. Anita Desai",
            "specialization": "Pediatrician",
            "qualification": "MBBS, MD (Pediatrics)",
            "experience_years": 10,
            "rating": 4.7,
            "consultation_fee": 600,
            "available": True,
            "profile_image": "https://randomuser.me/api/portraits/women/3.jpg",
            "languages": "English, Hindi, Gujarati",
            "about": "Child health specialist with a gentle approach. Expert in newborn care, vaccinations, and childhood illnesses.",
            "email": "dr.anita@healthai.com",
            "phone": "+91 98765 43212",
            "available_days": json.dumps(["Tuesday", "Thursday", "Friday", "Saturday"]),
            "available_hours": json.dumps({"start": "09:00", "end": "16:00"}),
            "total_consultations": 980
        },
        {
            "name": "Dr. Vikram Singh",
            "specialization": "Dermatologist",
            "qualification": "MBBS, MD (Dermatology)",
            "experience_years": 8,
            "rating": 4.6,
            "consultation_fee": 700,
            "available": True,
            "profile_image": "https://randomuser.me/api/portraits/men/4.jpg",
            "languages": "English, Hindi, Punjabi",
            "about": "Skin specialist treating acne, allergies, and cosmetic concerns. Offers both medical and aesthetic dermatology.",
            "email": "dr.vikram@healthai.com",
            "phone": "+91 98765 43213",
            "available_days": json.dumps(["Monday", "Tuesday", "Thursday", "Saturday"]),
            "available_hours": json.dumps({"start": "11:00", "end": "19:00"}),
            "total_consultations": 750
        },
        {
            "name": "Dr. Meera Patel",
            "specialization": "Gynecologist",
            "qualification": "MBBS, MS (Obstetrics & Gynecology)",
            "experience_years": 14,
            "rating": 4.9,
            "consultation_fee": 750,
            "available": True,
            "profile_image": "https://randomuser.me/api/portraits/women/5.jpg",
            "languages": "English, Hindi, Gujarati",
            "about": "Women's health expert specializing in pregnancy care, reproductive health, and menopause management.",
            "email": "dr.meera@healthai.com",
            "phone": "+91 98765 43214",
            "available_days": json.dumps(["Monday", "Wednesday", "Thursday", "Friday"]),
            "available_hours": json.dumps({"start": "10:00", "end": "18:00"}),
            "total_consultations": 1680
        },
        {
            "name": "Dr. Arjun Reddy",
            "specialization": "Psychiatrist",
            "qualification": "MBBS, MD (Psychiatry)",
            "experience_years": 9,
            "rating": 4.8,
            "consultation_fee": 900,
            "available": True,
            "profile_image": "https://randomuser.me/api/portraits/men/6.jpg",
            "languages": "English, Hindi, Telugu",
            "about": "Mental health specialist helping with anxiety, depression, stress management, and emotional wellbeing.",
            "email": "dr.arjun@healthai.com",
            "phone": "+91 98765 43215",
            "available_days": json.dumps(["Tuesday", "Wednesday", "Friday", "Saturday", "Sunday"]),
            "available_hours": json.dumps({"start": "14:00", "end": "21:00"}),
            "total_consultations": 1120
        },
        {
            "name": "Dr. Sneha Iyer",
            "specialization": "Nutritionist",
            "qualification": "MSc (Nutrition), PhD (Dietetics)",
            "experience_years": 7,
            "rating": 4.7,
            "consultation_fee": 400,
            "available": True,
            "profile_image": "https://randomuser.me/api/portraits/women/7.jpg",
            "languages": "English, Hindi, Malayalam",
            "about": "Certified nutritionist specializing in weight management, diabetes diet, and lifestyle nutrition counseling.",
            "email": "dr.sneha@healthai.com",
            "phone": "+91 98765 43216",
            "available_days": json.dumps(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]),
            "available_hours": json.dumps({"start": "08:00", "end": "15:00"}),
            "total_consultations": 890
        },
        {
            "name": "Dr. Amit Verma",
            "specialization": "Orthopedic",
            "qualification": "MBBS, MS (Orthopedics)",
            "experience_years": 11,
            "rating": 4.6,
            "consultation_fee": 650,
            "available": True,
            "profile_image": "https://randomuser.me/api/portraits/men/8.jpg",
            "languages": "English, Hindi",
            "about": "Bone and joint specialist treating fractures, arthritis, sports injuries, and back pain.",
            "email": "dr.amit@healthai.com",
            "phone": "+91 98765 43217",
            "available_days": json.dumps(["Monday", "Wednesday", "Thursday", "Saturday"]),
            "available_hours": json.dumps({"start": "09:00", "end": "17:00"}),
            "total_consultations": 1340
        }
    ]
    
    for doctor_data in mock_doctors:
        doctor = Doctor(**doctor_data)
        db.add(doctor)
    
    db.commit()
    print(f"✅ Seeded {len(mock_doctors)} mock doctors")
    db.close()

if __name__ == "__main__":
    seed_doctors()
