# project/api/exercises/models.py


import datetime

from project import db


class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_body = db.Column(db.String, nullable=False)
    test_code = db.Column(db.String, nullable=False)
    test_code_solution = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(
            self, exercise_body, test_code, test_code_solution,
            created_at=datetime.datetime.utcnow()):
        self.exercise_body = exercise_body
        self.test_code = test_code
        self.test_code_solution = test_code_solution
        self.created_at = created_at
