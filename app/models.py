# app/models.py
from datetime import datetime

from app import db

class Tweet(db.Model):
    __table__name = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tweet #{self.id}>"
