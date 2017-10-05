# project/api/scores/models.py


import datetime

from project import db


class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(db.Integer, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(
            self, user_id, exercise_id, correct,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()):
        self.user_id = user_id
        self.exercise_id = exercise_id
        self.correct = correct
        self.created_at = created_at
        self.updated_at = updated_at
