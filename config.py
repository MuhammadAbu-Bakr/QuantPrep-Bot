import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
SQLALCHEMY_DATABASE_URI = 'sqlite:///questions.db' 