# project/tests/utils.py


import datetime


from project import db
from project.api.scores.models import Score
from project.api.exercises.models import Exercise


def add_score(user_id, exercise_id, correct,
              created_at=datetime.datetime.utcnow()):
    score = Score(
        user_id=user_id,
        exercise_id=exercise_id,
        correct=correct,
        created_at=created_at,
        updated_at=created_at
    )
    db.session.add(score)
    db.session.commit()
    return score


def add_exercise(
        exercise_body='Define a function called sum that takes two integers as arguments and returns their sum',
        test_code='sum(2, 2)',
        test_code_solution='4',
        created_at=datetime.datetime.utcnow()):
    exercise = Exercise(
        exercise_body=exercise_body,
        test_code=test_code,
        test_code_solution=test_code_solution,
        created_at=created_at
    )
    db.session.add(exercise)
    db.session.commit()
    return exercise
