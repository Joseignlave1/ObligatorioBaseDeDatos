from datetime import datetime
from config import db

class Shift(db.Model):
    __tablename__ = 'shifts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)