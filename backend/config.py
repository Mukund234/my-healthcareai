import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./health_predictor.db")
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # CORS
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # App Settings
    APP_NAME = "Early Health Risk Predictor"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # ML Models
    MODELS_DIR = os.path.join(os.path.dirname(__file__), "models", "saved_models")
    
    # LLM Settings
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    LLM_TEMPERATURE = 0.7
    MAX_TOKENS = 500
    
    # Risk Thresholds
    HIGH_RISK_THRESHOLD = 0.7
    MODERATE_RISK_THRESHOLD = 0.4

settings = Settings()
