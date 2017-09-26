# project/tests/utils.py


import datetime


from project import db
from project.api.scores.models import Score


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
