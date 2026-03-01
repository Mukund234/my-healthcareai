# Stitch: Early Health Risk Predictor

> An AI-powered medical intelligence platform ("Stitch") designed for early symptom analysis, health risk assessment, and precise preventive oversight. Built with a futuristic "Cyber Dark Mode" aesthetic.

---

## 🎯 Our Goal & The Problem We Solve

In many regions, accessible and immediate medical guidance is scarce. People from all backgrounds—from urban centers to rural communities—often struggle to understand their symptoms before deciding whether a hospital visit is necessary. 

**Stitch** solves this by acting as a "Digital Surgeon." It bridges the gap between AI capabilities and validated medical protocols (like WHO guidelines). By providing a highly intuitive, conversational interface, Stitch offers users preliminary health guidance, early risk prediction, and actionable next steps—all before they even step foot in a clinic.

## 🚀 Future Outcomes (Roadmap)

While the current version (v1.0) provides a robust foundation for health assessments and secure user profiles, our vision for Stitch extends much further:
- **Advanced Symptom Analyzer:** Deep-learning natural language analysis for complex, multi-symptom presentations.
- **Emergency Triage protocol:** Automatic emergency detection triggering immediate alerts to local emergency services (like automatically routing to 102).
- **Fine-Tuned Medical LLMs:** Transitioning from general-purpose LLMs to specialized models trained strictly on validated medical datasets.
- **Telemedicine Integration:** Seamless video consultations with verified doctors directly within the platform.
- **Wearable Device Sync:** Integrating real-time health data (heart rate, O2 levels) to proactively predict health events.

---

## 🏗️ Tech Stack: What We Use

We built Stitch using a modern, scalable, and secure architecture divided into a frontend interface and a powerful backend engine.

### Frontend (User Interface)
- **Framework:** [Next.js 14](https://nextjs.org/) (React)
- **Styling:** Custom CSS implementing a unique "Cyber Dark Mode" (glassmorphism, neon cyan accents, dark charcoal base) for a professional, clinical feel.
- **Authentication:** [Firebase Authentication](https://firebase.google.com/) for secure Email/Password and Google OAuth integrations.
- **State Management:** React Context API & React Hooks.

### Backend (Intelligence & Data)
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+) for high-performance, asynchronous API endpoints.
- **Database:** SQLite (development) and SQLAlchemy ORM for relational data management (User profiles, Consultation History).
- **AI/ML Engine:** 
  - OpenAI API integration for conversational intelligence.
  - Custom Rule-Based Risk Engine modeled after WHO clinical protocols.
- **Security:** Firebase Admin SDK for JWT token verification and protected routing.

---

## 🛠️ How We Developed It

The development of Stitch followed a meticulous, component-driven approach:

1. **Design & UX:** We started by defining the "Digital Surgeon" aesthetic. We completely overhauled the standard clinical white UI into a high-contrast Cyber Dark Mode, ensuring critical medical data is highly legible while looking futuristic.
2. **Backend Foundation:** We constructed a robust FastAPI backend, defining data models for Users, Doctors, and Risk Assessments using SQLAlchemy. We implemented custom middleware to verify Firebase authentication tokens.
3. **AI Integration:** We built a dual-engine system. An LLM handles the natural language conversation, while a deterministic rule-engine ensures risk calculations adhere strictly to established health guidelines.
4. **Frontend Implementation:** We built the interactive Chat interface, Sidebar command center, and secure Login/Registration pages using Next.js. We prioritized smooth animations and glassmorphism effects.
5. **Security & Polish:** Finally, we integrated the frontend with the backend authentication routes, ensuring robust route protection and secure data synchronization between Firebase and our local database.

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI keys and Firebase Admin credentials

# Initialize database & seed data
python -c "from database import init_db; init_db()"
python seed_doctors.py

# Run backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local with your Firebase API keys and Backend URL

# Run development server
npm run dev
```

### Access the Application
- **Frontend Dashboard:** `http://localhost:3000`
- **Backend API:** `http://localhost:8000`
- **API Swagger Docs:** `http://localhost:8000/docs`

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: Stitch provides general health information for educational and preventive purposes only. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions.

---
*Developed for the intersection of AI and preventative healthcare. Built in 2026.*
