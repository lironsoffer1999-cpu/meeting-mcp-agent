import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Config(BaseModel):
    """
    Application configuration validated by Pydantic.
    """
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/oauth2callback")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    POLLING_INTERVAL_MINUTES: int = 15
    TIMEZONE: str = os.getenv("TIMEZONE", "UTC")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

config = Config()
