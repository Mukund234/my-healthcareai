# Medical AI Assistant

> AI-powered medical assistant for symptom analysis, health risk assessment, and doctor consultations. Built for hackathon presentation.

## 🎯 Project Vision

An accessible medical AI assistant that helps people from all backgrounds (poor to rich, urban to rural) get preliminary health guidance, especially when good hospitals are not nearby. Features ChatGPT-style conversations with medical expertise.

## ✨ Features

### Current Features (v1.0)
- ✅ **AI Health Assessment**: 14-question comprehensive health evaluation
- ✅ **WHO Guidelines**: Risk calculation based on WHO health standards
- ✅ **Personalized Recommendations**: Exercise, nutrition, and lifestyle advice
- ✅ **Doctor Consultation**: Book appointments with verified doctors
- ✅ **Bilingual Support**: English and Hindi
- ✅ **Premium UI**: Dark theme with glassmorphism and smooth animations
- ✅ **Firebase Integration**: Cloud storage for user data

### Planned Features (v2.0)
- 🔄 **Symptom Analyzer**: Natural language symptom analysis
- 🔄 **Emergency Triage**: Automatic emergency detection and guidance
- 🔄 **Treatment Recommendations**: Evidence-based treatment suggestions
- 🔄 **Home Remedies**: Curated home remedies database
- 🔄 **Video Consultations**: Real-time doctor consultations
- 🔄 **Medical AI Training**: Fine-tuned LLM on medical datasets

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLite (development), PostgreSQL (production)
- **AI/ML**: 
  - OpenAI GPT-3.5/4 (optional)
  - Custom WHO-based risk engine
  - Planned: Fine-tuned medical LLM
- **Authentication**: Firebase Auth
- **Storage**: Firebase Cloud Storage

### Frontend
- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS + Custom CSS
- **State Management**: React Hooks
- **API Client**: Fetch API

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python -c "from database import init_db; init_db()"

# Seed mock doctors (for demo)
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
cp .env.example .env.local
# Edit .env.local with backend URL

# Run development server
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/my-ai.git
cd my-ai
```

2. **Start backend** (in one terminal)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python seed_doctors.py
uvicorn main:app --reload
```

3. **Start frontend** (in another terminal)
```bash
cd frontend
npm install
npm run dev
```

4. **Open browser** → http://localhost:3000

## 📁 Project Structure

```
my-ai/
├── backend/
│   ├── ai/                      # AI engines
│   │   ├── conversation_engine.py
│   │   ├── llm_explainer.py
│   │   └── recommendation_engine.py
│   ├── models/                  # Database models
│   │   ├── user.py
│   │   ├── risk_result.py
│   │   └── doctor.py
│   ├── routes/                  # API endpoints
│   │   ├── conversation.py
│   │   └── doctors.py
│   ├── risk_engine/            # WHO-based risk calculation
│   │   ├── who_rules.py
│   │   └── risk_calculator.py
│   ├── main.py                 # FastAPI app
│   ├── database.py             # Database configuration
│   └── requirements.txt
│
├── frontend/
│   ├── app/                    # Next.js app directory
│   │   ├── page.js            # Landing page
│   │   ├── chat/              # Chat interface
│   │   ├── dashboard/         # User dashboard
│   │   ├── auth/              # Authentication
│   │   └── globals.css        # Global styles
│   ├── components/            # React components
│   ├── contexts/              # React contexts
│   └── package.json
│
└── README.md
```

## 🎨 UI Features

- **Dark Theme**: Modern dark mode with vibrant gradients
- **Glassmorphism**: Premium glass-like UI elements
- **Smooth Animations**: Message slide-ins, hover effects
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG 2.1 compliant

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./health_predictor.db
OPENAI_API_KEY=your_openai_key_here
FIREBASE_CREDENTIALS=path/to/firebase-credentials.json
DEBUG=True
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_domain
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📊 API Endpoints

### Conversation
- `POST /api/conversation/start` - Start new health assessment
- `POST /api/conversation/message` - Send message to AI
- `GET /api/conversation/history/{id}` - Get conversation history

### Doctors
- `GET /api/doctors/list` - Get available doctors
- `GET /api/doctors/{id}` - Get doctor details
- `POST /api/doctors/book-appointment` - Book appointment
- `GET /api/doctors/specializations` - Get specializations

## 🎯 Hackathon Demo Flow

1. **Landing Page** → User sees the value proposition
2. **Start Assessment** → AI asks 14 health questions
3. **Risk Analysis** → WHO-based risk calculation (< 1s)
4. **Results Display** → Risk scores with emoji indicators
5. **Recommendations** → Personalized health advice
6. **Doctor Consultation** → Book appointment with verified doctor
7. **Dashboard** → View history and track progress

## 🤝 Contributing

This is a hackathon project. Contributions welcome after the event!

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application provides general health information for educational and preventive purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions.

## 👨‍💻 Author

Built for hackathon presentation
- Focus: Accessible healthcare for all
- Goal: Bridge the gap between AI and medical expertise

## 🙏 Acknowledgments

- WHO Guidelines for health risk assessment
- OpenAI for LLM capabilities
- Firebase for backend services
- Next.js and FastAPI communities

---

**Status**: 🚧 Active Development | **Version**: 1.0.0 | **Last Updated**: Feb 2026
