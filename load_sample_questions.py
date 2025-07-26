import json
from app import app, db
from app.models import Question

sample_questions = [
  {
    "topic": "Percentages",
    "question_text": "If the price of a shirt is increased by 20%, it becomes Rs. 600. What was the original price?",
    "options": ["Rs. 480", "Rs. 500", "Rs. 520", "Rs. 540"],
    "correct_answer": "Rs. 500",
    "explanation": "Let original = x; x + 20%x = 600 → 1.2x = 600 → x = 500"
  },
  {
    "topic": "Averages",
    "question_text": "The average of 5 numbers is 28. If one number is 20, what is the average of the other four?",
    "options": ["27", "28", "30", "32"],
    "correct_answer": "30",
    "explanation": "Total = 28×5 = 140; Remaining sum = 140 - 20 = 120; Avg = 120/4 = 30"
  },
  {
    "topic": "Ratios",
    "question_text": "The ratio of boys to girls in a class is 3:2. If there are 15 boys, how many girls are there?",
    "options": ["5", "10", "20", "25"],
    "correct_answer": "10",
    "explanation": "3x = 15 → x = 5 → girls = 2x = 10"
  },
  {
    "topic": "Algebra",
    "question_text": "If 2x + 3 = 11, then x = ?",
    "options": ["3", "4", "5", "6"],
    "correct_answer": "4",
    "explanation": "2x = 8 → x = 4"
  },
  {
    "topic": "Geometry",
    "question_text": "What is the area of a triangle with base 10 cm and height 5 cm?",
    "options": ["25", "50", "15", "30"],
    "correct_answer": "25",
    "explanation": "Area = 1/2 × base × height = 1/2 × 10 × 5 = 25"
  },
  {
    "topic": "Time & Work",
    "question_text": "A can complete a task in 5 days, B in 10 days. Working together, how long will they take?",
    "options": ["3.3 days", "2.5 days", "5 days", "7.5 days"],
    "correct_answer": "3.3 days",
    "explanation": "1/5 + 1/10 = 3/10 → Time = 10/3 = 3.3 days"
  },
  {
    "topic": "Speed & Distance",
    "question_text": "A train moves at 60 km/h. How far does it travel in 45 minutes?",
    "options": ["45 km", "30 km", "60 km", "75 km"],
    "correct_answer": "45 km",
    "explanation": "45 minutes = 0.75 hrs → 60×0.75 = 45"
  },
  {
    "topic": "Simple Interest",
    "question_text": "Find the simple interest on Rs. 1000 at 5% per annum for 3 years.",
    "options": ["Rs. 150", "Rs. 100", "Rs. 200", "Rs. 300"],
    "correct_answer": "Rs. 150",
    "explanation": "SI = PRT/100 = 1000×5×3/100 = 150"
  },
  {
    "topic": "Fractions",
    "question_text": "What is 3/4 of 16?",
    "options": ["10", "12", "14", "8"],
    "correct_answer": "12",
    "explanation": "3/4 × 16 = 12"
  },
  {
    "topic": "Number Series",
    "question_text": "What comes next in the series: 2, 4, 8, 16, ?",
    "options": ["18", "20", "32", "24"],
    "correct_answer": "32",
    "explanation": "Series doubles each time"
  },
  {
    "topic": "Algebra",
    "question_text": "If x² = 49, then x = ?",
    "options": ["7", "-7", "±7", "None"],
    "correct_answer": "±7",
    "explanation": "Square root of 49 = ±7"
  },
  {
    "topic": "Percentages",
    "question_text": "20% of what number is 40?",
    "options": ["80", "100", "200", "150"],
    "correct_answer": "200",
    "explanation": "x × 0.20 = 40 → x = 200"
  },
  {
    "topic": "Ratios",
    "question_text": "Divide Rs. 1200 in the ratio 1:3.",
    "options": ["Rs. 300 & Rs. 900", "Rs. 400 & Rs. 800", "Rs. 600 & Rs. 600", "Rs. 200 & Rs. 1000"],
    "correct_answer": "Rs. 300 & Rs. 900",
    "explanation": "Total = 1+3 = 4 → 1 part = 300, 3 parts = 900"
  },
  {
    "topic": "Linear Equations",
    "question_text": "Solve: 5x - 3 = 2x + 6",
    "options": ["x = 1", "x = 2", "x = 3", "x = 4"],
    "correct_answer": "x = 3",
    "explanation": "5x - 2x = 6 + 3 → 3x = 9 → x = 3"
  },
  {
    "topic": "Average",
    "question_text": "What is the average of first five even numbers?",
    "options": ["4", "6", "8", "10"],
    "correct_answer": "6",
    "explanation": "Even numbers: 2+4+6+8+10 = 30 → 30/5 = 6"
  },
  {
    "topic": "Geometry",
    "question_text": "The sum of interior angles of a quadrilateral is:",
    "options": ["180°", "270°", "360°", "90°"],
    "correct_answer": "360°",
    "explanation": "n=4 → Sum = (n−2)×180 = 360"
  },
  {
    "topic": "Proportions",
    "question_text": "If 5 pens cost Rs. 100, what is the cost of 8 pens?",
    "options": ["Rs. 120", "Rs. 150", "Rs. 160", "Rs. 180"],
    "correct_answer": "Rs. 160",
    "explanation": "1 pen = 20 → 8 pens = 160"
  },
  {
    "topic": "Probability",
    "question_text": "A die is rolled once. What is the probability of getting a number greater than 4?",
    "options": ["1/2", "1/3", "1/6", "2/3"],
    "correct_answer": "1/3",
    "explanation": "Numbers >4: 5,6 → 2/6 = 1/3"
  },
  {
    "topic": "Profit & Loss",
    "question_text": "A shopkeeper buys a book for Rs. 80 and sells it for Rs. 100. What is the profit percentage?",
    "options": ["20%", "25%", "30%", "40%"],
    "correct_answer": "25%",
    "explanation": "(Profit = 20; 20/80 × 100 = 25%)"
  },
  {
    "topic": "Unit Conversion",
    "question_text": "How many meters are there in 3.5 kilometers?",
    "options": ["350", "3500", "35,000", "3.5"],
    "correct_answer": "3500",
    "explanation": "1 km = 1000 m → 3.5 × 1000 = 3500"
  },
  {
    "topic": "Mixtures",
    "question_text": "A solution contains milk and water in ratio 3:2. If it has 30 liters milk, how much water?",
    "options": ["10 L", "15 L", "20 L", "25 L"],
    "correct_answer": "20 L",
    "explanation": "Milk:Water = 3:2 → If 3 parts = 30, then 1 part = 10 → Water = 2×10 = 20 L"
  },
  {
    "topic": "Time & Distance",
    "question_text": "A car travels 150 km in 3 hours. What is its speed?",
    "options": ["40 km/h", "50 km/h", "60 km/h", "70 km/h"],
    "correct_answer": "50 km/h",
    "explanation": "Speed = distance/time = 150/3 = 50"
  },
  {
    "topic": "Decimals",
    "question_text": "What is 0.25 as a fraction?",
    "options": ["1/4", "1/2", "1/5", "2/5"],
    "correct_answer": "1/4",
    "explanation": "0.25 = 25/100 = 1/4"
  },
  {
    "topic": "Inequalities",
    "question_text": "If x > 4 and x < 10, which of the following is true?",
    "options": ["x = 3", "x = 5", "x = 11", "x = 4"],
    "correct_answer": "x = 5",
    "explanation": "Only 5 lies between 4 and 10"
  },
  {
    "topic": "LCM",
    "question_text": "Find the LCM of 6 and 8.",
    "options": ["12", "24", "36", "48"],
    "correct_answer": "24",
    "explanation": "Multiples of 6 and 8 → first common = 24"
  },
  {
    "topic": "HCF",
    "question_text": "Find the HCF of 18 and 24.",
    "options": ["3", "6", "12", "9"],
    "correct_answer": "6",
    "explanation": "Common factors = 1, 2, 3, 6 → highest = 6"
  },
  {
    "topic": "Percentages",
    "question_text": "A student scores 72 out of 90. What is the percentage?",
    "options": ["80%", "85%", "90%", "95%"],
    "correct_answer": "80%",
    "explanation": "72/90 × 100 = 80%"
  },
  {
    "topic": "Linear Equations",
    "question_text": "Solve: 3(x – 2) = 9",
    "options": ["x = 5", "x = 4", "x = 3", "x = 6"],
    "correct_answer": "x = 5",
    "explanation": "3x – 6 = 9 → 3x = 15 → x = 5"
  },
  {
    "topic": "Algebraic Expressions",
    "question_text": "Simplify: (x + 2)(x – 2)",
    "options": ["x² + 4", "x² – 4", "x² – 2", "x² + 2"],
    "correct_answer": "x² – 4",
    "explanation": "Difference of squares"
  }
]

with app.app_context():
    for q in sample_questions:
        question = Question(
            topic=q["topic"],
            question_text=q["question_text"],
            options=str(q["options"]),
            correct_answer=q["correct_answer"],
            explaination=q["explanation"]
        )
        db.session.add(question)
    db.session.commit()
    print("Sample questions loaded.") 