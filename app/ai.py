import google.generativeai as genai
import json
import re
from typing import Dict, List, Optional
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def clean_json_response(response_text: str) -> str:
    response_text = re.sub(r'```json\s*', '', response_text)
    response_text = re.sub(r'```\s*$', '', response_text)
    
    start_idx = response_text.find('{')
    end_idx = response_text.rfind('}') + 1
    
    if start_idx != -1 and end_idx != 0:
        return response_text[start_idx:end_idx]
    
    return response_text

def validate_question_data(question_data: Dict) -> bool:
    required_fields = ['topic', 'question_text', 'options', 'correct_answer', 'explanation']
    
    for field in required_fields:
        if field not in question_data:
            return False
    
    if not isinstance(question_data['options'], list) or len(question_data['options']) != 4:
        return False
    
    if question_data['correct_answer'] not in question_data['options']:
        return False
    
    return True

def generate_question(topic: str = "Averages", difficulty: str = "medium") -> Optional[Dict]:
    try:
        
        prompt = f"""
        Create 1 quantitative reasoning multiple choice question on the topic "{topic}" for FSC level NAT test.
        
        Requirements:
        - Question should be at {difficulty} difficulty level
        - Provide exactly 4 options (A, B, C, D)
        - Include detailed step-by-step explanation
        - Make sure the question tests mathematical/quantitative reasoning
        - Ensure all options are plausible but only one is correct
        
        Respond ONLY with valid JSON in this exact format:
        {{
            "topic": "{topic}",
            "question_text": "Write the complete question here with all necessary details",
            "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
            "correct_answer": "The exact text of the correct option",
            "explanation": "Detailed step-by-step solution explaining how to arrive at the correct answer"
        }}
        
        Do not include any text before or after the JSON.
        """
        
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        if not response.text:
            return None
        
        
        response_text = response.text.strip()
        json_str = clean_json_response(response_text)
        
        try:
            question_data = json.loads(json_str)
            
           
            if validate_question_data(question_data):
                return question_data
            else:
                print(f"Invalid question data structure: {question_data}")
                return create_fallback_question(topic, difficulty)
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text[:200]}...")
            return create_fallback_question(topic, difficulty)
            
    except Exception as e:
        print(f"Error generating question: {str(e)}")
        return create_fallback_question(topic, difficulty)

def create_fallback_question(topic: str, difficulty: str) -> Dict:
    fallback_questions = {
        "Averages": {
            "easy": {
                "question_text": f"Find the average of 10, 20, and 30.",
                "options": ["15", "20", "25", "30"],
                "correct_answer": "20",
                "explanation": "Average = (10 + 20 + 30) ÷ 3 = 60 ÷ 3 = 20"
            },
            "medium": {
                "question_text": f"The average of 5 numbers is 40. If 4 of the numbers are 35, 42, 38, and 45, what is the fifth number?",
                "options": ["35", "40", "42", "45"],
                "correct_answer": "40",
                "explanation": "Total = 40 × 5 = 200. Sum of 4 numbers = 35+42+38+45 = 160. Fifth number = 200-160 = 40"
            },
            "hard": {
                "question_text": f"The average age of 10 students is 20 years. If the teacher's age is included, the average becomes 22 years. What is the teacher's age?",
                "options": ["42 years", "44 years", "46 years", "48 years"],
                "correct_answer": "42 years",
                "explanation": "Total age of students = 20 × 10 = 200. Total with teacher = 22 × 11 = 242. Teacher's age = 242 - 200 = 42 years"
            }
        }
    }
    
    if topic in fallback_questions and difficulty in fallback_questions[topic]:
        fallback = fallback_questions[topic][difficulty]
    else:
        fallback = {
            "question_text": f"This is a sample {difficulty} question on {topic}. What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4",
            "explanation": "Basic addition: 2 + 2 = 4"
        }
    
    return {
        "topic": topic,
        "question_text": fallback["question_text"],
        "options": fallback["options"],
        "correct_answer": fallback["correct_answer"],
        "explanation": fallback["explanation"]
    }

def generate_multiple_questions(topic: str = "Averages", count: int = 5, difficulty: str = "medium") -> List[Dict]:
    questions = []
    max_retries = 3
    
    for i in range(count):
        question = None
        retries = 0
        
        while question is None and retries < max_retries:
            question = generate_question(topic, difficulty)
            retries += 1
        
        if question is None:
            question = create_fallback_question(topic, difficulty)
        
        questions.append(question)
    
    return questions

def test_ai_generation():
    print("Testing AI question generation...")
    
    question = generate_question("Percentages", "medium")
    if question:
        print("✅ Single question generation successful")
        print(f"Topic: {question['topic']}")
        print(f"Question: {question['question_text'][:100]}...")
    else:
        print("❌ Single question generation failed")
    
    questions = generate_multiple_questions("Algebra", 3, "easy")
    if questions and len(questions) == 3:
        print(f"✅ Multiple question generation successful ({len(questions)} questions)")
    else:
        print("❌ Multiple question generation failed")
    
    return question is not None and len(questions) == 3

if __name__ == "__main__":
    test_ai_generation()
