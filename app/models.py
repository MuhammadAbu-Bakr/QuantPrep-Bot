from app import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100))
    question_text = db.Column(db.String(500))
    options = db.Column(db.PickableTypes)
    correct_answer = db.Column(db.String(100))
    explaination = db.Column(db.String(1000))

class studentResponce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    selected_option = db.Column(db.String(100))
    is_correct = db.Column(db.Boolean)
     