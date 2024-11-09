from datetime import datetime
from config import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    contact_phone = db.Column(db.String(20))
    email_address = db.Column(db.String(100))
