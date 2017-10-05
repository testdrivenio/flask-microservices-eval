# project/tests/scores/test_scores_model.py


from project import db
from project.api.scores.models import Score
from project.tests.base import BaseTestCase
from project.tests.utils import add_score


class TestScoreModel(BaseTestCase):

    def test_add_score(self):
        score = add_score(1, 1, True)
        self.assertTrue(score.id)
        self.assertEqual(score.user_id, 1)
        self.assertEqual(score.exercise_id, 1)
        self.assertTrue(score.created_at)
        self.assertTrue(score.updated_at)
