# project/tests/scores/test_scores_api.py


import json

from project.tests.base import BaseTestCase
from project.tests.utils import add_score


class TestScoreBlueprint(BaseTestCase):

    def test_all_scores(self):
        """Ensure get all scores behaves correctly."""
        add_score(1, 11, True)
        add_score(2, 22, False)
        with self.client:
            response = self.client.get('/scores')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['scores']), 2)
            self.assertEqual(1, data['data']['scores'][0]['user_id'])
            self.assertEqual(2, data['data']['scores'][1]['user_id'])
            self.assertEqual(11, data['data']['scores'][0]['exercise_id'])
            self.assertEqual(22, data['data']['scores'][1]['exercise_id'])
            self.assertTrue(data['data']['scores'][0]['correct'])
            self.assertFalse(data['data']['scores'][1]['correct'])
            self.assertTrue('created_at' in data['data']['scores'][0])
            self.assertTrue('created_at' in data['data']['scores'][1])
            self.assertTrue('updated_at' in data['data']['scores'][0])
            self.assertTrue('updated_at' in data['data']['scores'][1])
            self.assertIn('success', data['status'])

    def test_single_score(self):
        """Ensure get single score behaves correctly."""
        score = add_score(88, 99, False)
        with self.client:
            response = self.client.get(f'/scores/{score.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(88, data['data']['user_id'])
            self.assertEqual(99, data['data']['exercise_id'])
            self.assertFalse(data['data']['correct'])
            self.assertTrue('created_at' in data['data'])
            self.assertTrue('updated_at' in data['data'])
            self.assertIn('success', data['status'])

    def test_single_score_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/scores/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Score does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_score_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/scores/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Score does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_scores_by_user_id(self):
        """Ensure get all scores by user id behaves correctly."""
        add_score(998877, 878778, True)
        with self.client:
            response = self.client.get(
                f'/scores/user',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['scores']), 1)
            self.assertEqual(998877, data['data']['scores'][0]['user_id'])
            self.assertEqual(878778, data['data']['scores'][0]['exercise_id'])
            self.assertTrue(data['data']['scores'][0]['correct'])
            self.assertTrue('created_at' in data['data']['scores'][0])
            self.assertTrue('updated_at' in data['data']['scores'][0])
            self.assertIn('success', data['status'])

    def test_all_scores_by_user_id_no_scores(self):
        """Ensure get all scores by user id behaves correctly with 0 scores."""
        with self.client:
            response = self.client.get(
                f'/scores/user',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['scores']), 0)
            self.assertIn('success', data['status'])

    def test_all_scores_by_user_id_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.get(f'/scores/user')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])

    def test_single_score_by_user_id(self):
        """Ensure get all scores by user id behaves correctly."""
        score = add_score(998877, 65479, True)
        with self.client:
            response = self.client.get(
                f'/scores/user/{score.id}',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(998877, data['data']['user_id'])
            self.assertEqual(65479, data['data']['exercise_id'])
            self.assertTrue(data['data']['correct'])
            self.assertTrue('created_at' in data['data'])
            self.assertTrue('updated_at' in data['data'])
            self.assertIn('success', data['status'])

    def test_single_score_by_user_id_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get(
                '/scores/user/blah',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Score does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_score_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get(
                '/scores/user/999',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Score does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_score_by_user_id_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.get(f'/scores/user/999')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])

    def test_add_score(self):
        """Ensure a new score can be added to the database."""
        with self.client:
            response = self.client.post(
                '/scores',
                data=json.dumps(dict(
                    exercise_id=86,
                    correct=True
                )),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('New score was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_score_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/scores',
                data=json.dumps(dict()),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_score_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object is invalid."""
        with self.client:
            response = self.client.post(
                '/scores',
                data=json.dumps(dict(correct=True)),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_score_duplicate_exercise_id(self):
        """Ensure error is thrown if the exercise already exists."""
        add_score(998877, 65479, True)
        with self.client:
            response = self.client.post(
                '/scores',
                data=json.dumps(dict(
                    exercise_id=65479,
                    correct=True
                )),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That score already exists. Please update with a PUT request.',
                data['message'])
            self.assertIn('fail', data['status'])

    def test_add_score_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.post(
            '/scores',
            data=json.dumps(dict(
                exercise_id=86,
                correct=True
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])

    def test_update_score(self):
        """Ensure an existing score can be updated in the database."""
        score = add_score(998877, 65479, True)
        with self.client:
            response = self.client.put(
                f'/scores/{score.id}',
                data=json.dumps(dict(
                    exercise_id=65479,
                    correct=False
                )),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Score was updated!', data['message'])
            self.assertIn('success', data['status'])

    def test_update_score_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.put(
                '/scores/7',
                data=json.dumps(dict()),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_score_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object is invalid."""
        with self.client:
            response = self.client.put(
                '/scores/7',
                data=json.dumps(dict(correct=True)),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_score_invalid_exercise_id(self):
        """Ensure error is thrown if the exercise does not exist."""
        add_score(998877, 65479, True)
        with self.client:
            response = self.client.put(
                '/scores/9',
                data=json.dumps(dict(
                    exercise_id=65479,
                    correct=True
                )),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That score does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_score_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.put(
            '/scores/9',
            data=json.dumps(dict(
                exercise_id=86,
                correct=True
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])

    def test_upsert_score_update(self):
        """Ensure an existing score can be updated in the database."""
        score = add_score(998877, 65479, True)
        with self.client:
            response = self.client.patch(
                f'/scores/{score.id}',
                data=json.dumps(dict(
                    exercise_id=65479,
                    correct=False
                )),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Score was updated!', data['message'])
            self.assertIn('success', data['status'])

    def test_upsert_score_insert(self):
        """Ensure a new score can be added to the database."""
        with self.client:
            response = self.client.patch(
                f'/scores',
                data=json.dumps(dict(
                    exercise_id=65479,
                    correct=False
                )),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('New score was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_upsert_score_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.patch(
                '/scores/7',
                data=json.dumps(dict()),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_upsert_score_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object is invalid."""
        with self.client:
            response = self.client.patch(
                '/scores/7',
                data=json.dumps(dict(correct=True)),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_upsert_score_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.patch(
            '/scores/9',
            data=json.dumps(dict(
                exercise_id=86,
                correct=True
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])
