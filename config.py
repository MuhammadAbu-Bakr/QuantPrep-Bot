import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
SQLALCHEMY_DATABASE_URI = 'sqlite:///questions.db'

TEACHER_ACCESS_CODE = os.getenv('TEACHER_ACCESS_CODE', 'TEACH2025')
STUDENT_ACCESS_CODE = os.getenv('STUDENT_ACCESS_CODE', 'STUD2025')
