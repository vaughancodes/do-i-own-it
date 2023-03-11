from app import app, db
from models import *
from flask_sqlalchemy import SQLAlchemy

with app.app_context():
    db.create_all()

