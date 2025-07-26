from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Question, studentResponce
import ast

@app.route('/student', methods=['GET', 'POST'])
def student():
    # For demo: get the first question
    question = Question.query.first()
    if question:
        # If options are stored as a string, convert to list
        options = question.options
        if isinstance(options, str):
            options = ast.literal_eval(options)
        question.options = options
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
        return render_template('student.html', question=question, feedback=feedback, explanation=explanation)
    return render_template('student.html', question=question)

@app.route('/teacher')
def teacher():
    questions = Question.query.all()
    for q in questions:
        if isinstance(q.options, str):
            q.options = ast.literal_eval(q.options)
    attempts = studentResponce.query.all()
    return render_template('teacher.html', questions=questions, attempts=attempts)

@app.route('/generate-ai-questions', methods=['POST'])
def generate_ai_questions():
    # Placeholder for AI question generation logic
    flash('AI question generation is not implemented yet.')
    return redirect(url_for('teacher'))
