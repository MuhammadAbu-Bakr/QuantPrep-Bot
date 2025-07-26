from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Question, studentResponce
import ast

@app.route('/student', methods=['GET', 'POST'])
def student():
    # For demo: get the first question
    question = Question.query.first()
    if question:
        # If options are stored as a string, convert to list for display only
        options = question.options
        if isinstance(options, str):
            options = ast.literal_eval(options)
        # Create a copy of question data for template
        question_data = {
            'id': question.id,
            'topic': question.topic,
            'question_text': question.question_text,
            'options': options,
            'correct_answer': question.correct_answer,
            'explaination': question.explaination
        }
    else:
        question_data = None
    
    feedback = None
    explanation = None
    if request.method == 'POST':
        selected_option = request.form.get('selected_option')
        is_correct = selected_option == question.correct_answer
        feedback = 'Correct!' if is_correct else 'Incorrect.'
        explanation = question.explaination if not is_correct else None
        # Save response
        response = studentResponce(
            student_name='Anonymous',  
            question_id=question.id,
            selected_option=selected_option,
            is_correct=is_correct
        )
        db.session.add(response)
        db.session.commit()
        return render_template('student.html', question=question_data, feedback=feedback, explanation=explanation)
    return render_template('student.html', question=question_data)

@app.route('/teacher')
def teacher():
    questions = Question.query.all()
    questions_data = []
    for q in questions:
        options = q.options
        if isinstance(options, str):
            options = ast.literal_eval(options)
        questions_data.append({
            'id': q.id,
            'topic': q.topic,
            'question_text': q.question_text,
            'options': options,
            'correct_answer': q.correct_answer,
            'explaination': q.explaination
        })
    attempts = studentResponce.query.all()
    return render_template('teacher.html', questions=questions_data, attempts=attempts)

@app.route('/add-question', methods=['POST'])
def add_question():
    try:
        # Get form data
        topic = request.form.get('topic')
        question_text = request.form.get('question_text')
        correct_answer = request.form.get('correct_answer')
        explanation = request.form.get('explanation')
        
        # Get options
        options = [
            request.form.get('option1'),
            request.form.get('option2'),
            request.form.get('option3'),
            request.form.get('option4')
        ]
        
        # Create new question
        new_question = Question(
            topic=topic,
            question_text=question_text,
            options=str(options),
            correct_answer=correct_answer,
            explaination=explanation
        )
        
        db.session.add(new_question)
        db.session.commit()
        
        flash('Question added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding question: {str(e)}', 'error')
    
    return redirect(url_for('teacher'))

@app.route('/generate-ai-questions', methods=['POST'])
def generate_ai_questions():
    # Placeholder for AI question generation logic
    flash('AI question generation is not implemented yet.', 'info')
    return redirect(url_for('teacher'))
