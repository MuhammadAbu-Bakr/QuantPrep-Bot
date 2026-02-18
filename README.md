# QuantPrep-Bot 🧮

A comprehensive web-based practice and monitoring system designed for FSC students preparing for NTS NAT quantitative questions. Features include an extensive question bank, real-time progress tracking, and optional AI-powered question generation using Google's Gemini API.

**@uthor Muhammad Abu-Bakr**

## 🌟 Features

### For Students
- **Practice Tests**: Take 30-question practice tests with randomized questions
- **Real-time Feedback**: Instant results with detailed explanations
- **Progress Tracking**: Monitor your performance across different topics
- **Secure Access**: Access-code protected student portal
- **Multiple Topics**: Questions covering Percentages, Averages, Ratios, Algebra, Geometry, and more

### For Teachers
- **Question Management**: Add, edit, and manage question banks
- **Student Monitoring**: Track student performance and progress
- **AI Question Generation**: Generate new questions using AI (optional)
- **Bulk Operations**: Add multiple questions at once
- **Analytics Dashboard**: View comprehensive student performance data

### AI-Powered Features (Optional)
- **Automatic Question Generation**: Generate questions using Google Gemini API
- **Topic-Specific Questions**: Create questions for specific mathematical topics
- **Quality Validation**: AI-generated questions are validated for accuracy

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MuhammadAbu-Bakr/QuantPrep-Bot.git
   cd QuantPrep-Bot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   ```

5. **Load sample questions**
   ```bash
   python load_sample_questions.py
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   - Student Portal: http://127.0.0.1:5000/student
   - Teacher Portal: http://127.0.0.1:5000/teacher

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Gemini API Configuration (For AI features)
GOOGLE_API_KEY=your_gemini_api_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_here

# Access Codes
TEACHER_ACCESS_CODE=your_teacher_access_code
STUDENT_ACCESS_CODE=your_student_access_code
```

### Access Codes
- **Teacher Access Code**: 789f7d8b-4b00-42bf-afb7-85101318bc41
- **Student Access Code**: 12345678-4b00-42bf-afb7-85101318bc41

## 📁 Project Structure

```
QuantPrep-Bot/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes.py            # Application routes
│   ├── models.py            # Database models
│   ├── ai.py               # AI integration (Gemini API)
│   ├── templates/          # HTML templates
│   │   ├── base.html
│   │   ├── student.html
│   │   ├── teacher.html
│   │   ├── auth_form.html
│   │   └── test_results.html
│   └── static/
│       └── style.css       # CSS styles
├── instance/
│   └── questions.db        # SQLite database
├── venv/                   # Virtual environment
├── config.py              # Configuration settings
├── run.py                 # Application entry point
├── load_sample_questions.py # Sample data loader
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .gitignore
├── LICENSE
└── README.md
```

## 🗄️ Database Schema

### Questions Table
- `id`: Primary key
- `topic`: Question topic/category
- `question_text`: The question content
- `options`: Multiple choice options (JSON)
- `correct_answer`: The correct answer
- `explanation`: Detailed explanation

### Student Responses Table
- `id`: Primary key
- `student_name`: Student identifier
- `question_id`: Foreign key to questions
- `selected_option`: Student's answer
- `is_correct`: Boolean indicating correctness

## 🤖 AI Integration

The system optionally integrates with Google's Gemini API for intelligent question generation:

### Setup AI Features
1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add your API key to the `.env` file
3. AI features will be automatically available in the teacher dashboard

### AI Capabilities
- Generate questions for specific topics
- Create multiple questions in bulk
- Validate question quality and format
- Ensure proper multiple-choice structure

## 🌐 Deployment

### Local Development
```bash
python run.py
```
The application runs on `http://127.0.0.1:5000` by default.

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (e.g., Gunicorn)
- Setting up a reverse proxy (e.g., Nginx)
- Using a more robust database (e.g., PostgreSQL)
- Implementing proper logging and monitoring

### Cloud Deployment
The application can be easily deployed on platforms like:
- Heroku
- Railway
- PythonAnywhere
- DigitalOcean App Platform

## 🔧 Usage

### For Students
1. Navigate to `/student`
2. Enter the student access code
3. Provide your name to start a practice session
4. Answer 30 randomized questions
5. View your results and explanations

### For Teachers
1. Navigate to `/teacher`
2. Enter the teacher access code
3. Access the dashboard to:
   - Add new questions manually
   - Generate questions using AI
   - View student performance data
   - Manage the question bank

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Google Gemini API for AI-powered question generation
- Flask framework for web development
- SQLAlchemy for database management
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Contact the maintainer

---

## 📷 Screenshots 



---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).