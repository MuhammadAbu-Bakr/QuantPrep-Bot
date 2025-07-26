from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # Sessions expire after 2 hours
db = SQLAlchemy(app)

from app import routes