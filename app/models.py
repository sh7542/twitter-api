# app/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app import db

class User(db.Model):
    __table__name = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(280))
    apitoken = db.Column(db.String(36))
    children = relationship("Tweet")

    def __repr__(self):
        return f"<User #{self.id}>"

class Tweet(db.Model):
    __table__name = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f"<Tweet #{self.id}>"
