from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models import Question, studentResponce
from app.ai import generate_question, generate_multiple_questions
import ast
import random

def safe_int(value, default=0):
    """Safely convert value to int with fallback"""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

@app.route('/student', methods=['GET', 'POST'])
def student():
    # Handle name entry
    if request.method == 'POST' and 'student_name' in request.form:
        student_name = request.form.get('student_name')
        if student_name and student_name.strip():
            session['student_name'] = student_name.strip()
            session['current_question_number'] = 1  # Ensure it's stored as int
            session['question_ids'] = []
            session['answers'] = {}
            session['score'] = 0
            
            # Get 30 random questions
            all_questions = Question.query.all()
            if len(all_questions) < 30:
                flash(f'Only {len(all_questions)} questions available. Please add more questions.', 'warning')
                session['question_ids'] = [q.id for q in all_questions]
            else:
                session['question_ids'] = random.sample([q.id for q in all_questions], 30)
            
            return redirect(url_for('student'))
        else:
            flash('Please enter your name.', 'error')
            return redirect(url_for('student'))
    
    # Check if student has started the test
    if not session.get('student_name'):
        return render_template('student.html')
    
    # Handle question submission
    if request.method == 'POST' and 'selected_option' in request.form:
        # Safe conversion of form data
        question_id = safe_int(request.form.get('question_id'))
        selected_option = request.form.get('selected_option')
        current_question_number = safe_int(session.get('current_question_number'), 1)
        
        if question_id == 0:  # Invalid question_id
            flash('Invalid question ID.', 'error')
            return redirect(url_for('student'))
        
        # Get the current question
        question = Question.query.get(question_id)
        if question:
            # Check if answer is correct
            is_correct = selected_option == question.correct_answer
            
            # Update session data
            session['answers'][str(question_id)] = {  # Use string key for consistency
                'selected': selected_option,
                'correct': is_correct
            }
            
            if is_correct:
                session['score'] = safe_int(session.get('score'), 0) + 1
            
            # Save response to database
            response = studentResponce(
                student_name=session['student_name'],
                question_id=question_id,
                selected_option=selected_option,
                is_correct=is_correct
            )
            db.session.add(response)
            db.session.commit()
            
            # Check if test is complete (ensure both values are integers)
            if current_question_number >= 30:
                # Test completed - show results
                return redirect(url_for('test_results'))
            
            # Move to next question immediately
            session['current_question_number'] = current_question_number + 1
            return redirect(url_for('student'))
    
    # Show current question
    current_question_number = safe_int(session.get('current_question_number'), 1)
    question_ids = session.get('question_ids', [])
    
    if current_question_number > len(question_ids):
        return redirect(url_for('test_results'))
    
    # Get current question
    current_question_id = question_ids[current_question_number - 1]
    question = Question.query.get(current_question_id)
    
    if question:
        options = question.options
        if isinstance(options, str):
            try:
                options = ast.literal_eval(options)
            except (ValueError, SyntaxError):
                # Fallback if options can't be parsed
                options = []
        
        question_data = {
            'id': question.id,
            'topic': question.topic,
            'question_text': question.question_text,
            'options': options,
            'correct_answer': question.correct_answer,
            'explaination': question.explaination
        }
        
        return render_template('student.html', 
                            question=question_data, 
                            current_question_number=current_question_number)
    
    return redirect(url_for('student'))

@app.route('/test-results')
def test_results():
    if not session.get('student_name'):
        return redirect(url_for('student'))
    
    score = safe_int(session.get('score'), 0)
    question_ids = session.get('question_ids', [])
    total_questions = len(question_ids)
    percentage = float((score / total_questions * 100) if total_questions > 0 else 0)
    
    return render_template('test_results.html', 
                         student_name=session.get('student_name'),
                         score=score,
                         total_questions=total_questions,
                         percentage=percentage)

@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    flash('Session ended. You can start a new test.', 'info')
    return redirect(url_for('student'))

@app.route('/teacher')
def teacher():
    questions = Question.query.all()
    questions_data = []
    for q in questions:
        options = q.options
        if isinstance(options, str):
            try:
                options = ast.literal_eval(options)
            except (ValueError, SyntaxError):
                options = []
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
    try:
        # Get parameters from form
        topic = request.form.get('topic', 'Averages')
        count = safe_int(request.form.get('count'), 1)
        difficulty = request.form.get('difficulty', 'medium')
        
        if count > 10:  # Limit to prevent abuse
            count = 10
        elif count < 1:  # Ensure minimum count
            count = 1
            
        # Generate questions using Gemini
        if count == 1:
            question_data = generate_question(topic, difficulty)
            if question_data:
                # Save to database
                new_question = Question(
                    topic=question_data['topic'],
                    question_text=question_data['question_text'],
                    options=str(question_data['options']),
                    correct_answer=question_data['correct_answer'],
                    explaination=question_data['explanation']
                )
                db.session.add(new_question)
                db.session.commit()
                flash(f'AI generated question on "{topic}" added successfully!', 'success')
            else:
                flash('Failed to generate question. Please try again.', 'error')
        else:
            # Generate multiple questions
            questions_data = generate_multiple_questions(topic, count, difficulty)
            if questions_data:
                for question_data in questions_data:
                    new_question = Question(
                        topic=question_data['topic'],
                        question_text=question_data['question_text'],
                        options=str(question_data['options']),
                        correct_answer=question_data['correct_answer'],
                        explaination=question_data['explanation']
                    )
                    db.session.add(new_question)
                db.session.commit()
                flash(f'{len(questions_data)} AI generated questions on "{topic}" added successfully!', 'success')
            else:
                flash('Failed to generate questions. Please try again.', 'error')
                
    except Exception as e:
        flash(f'Error generating AI questions: {str(e)}', 'error')
    
    return redirect(url_for('teacher'))