import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Application Configuration
APP_NAME = "Resume Bot"
DEBUG = False
HOST = "0.0.0.0"
PORT = 8000

# File Upload Configuration
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {"pdf"}

# Cache Configuration
CACHE_TYPE = "simple"
CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # Change this in production 