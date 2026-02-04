"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import init_db

# Import routes
from routes import assessment, chat, conversation, doctors

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-powered early health risk prediction and prevention platform"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversation.router)
app.include_router(doctors.router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    init_db()
    print(f"✅ {settings.APP_NAME} v{settings.VERSION} started successfully!")
    print(f"📊 Database: {settings.DATABASE_URL}")
    print(f"🤖 LLM Model: {settings.LLM_MODEL if settings.OPENAI_API_KEY else 'Rule-based (no API key)'}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "endpoints": {
            "submit_assessment": "/api/assessment/submit",
            "get_assessment": "/api/assessment/{assessment_id}",
            "ask_question": "/api/chat/ask",
            "docs": "/docs"
        },
        "disclaimer": "⚠️ This application provides health risk predictions for educational and preventive purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment."
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "llm": "available" if settings.OPENAI_API_KEY else "rule-based"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
