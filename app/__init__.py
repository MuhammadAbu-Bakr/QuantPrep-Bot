from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2) 
db = SQLAlchemy(app)


app.jinja_env.filters['chr'] = chr

from app import routes