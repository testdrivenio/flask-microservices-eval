# project/tests/test_eval.py


import json

from project.tests.base import BaseTestCase


class TestEvalBlueprint(BaseTestCase):

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get(
            '/ping',
            headers=dict(Authorization='Bearer test')
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_ping_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])

    def test_eval_endpoint(self):
        """Ensure the /eval route behaves correctly."""
        with self.client:
            response = self.client.post(
                '/eval',
                data=json.dumps(dict(code='print("Hello, World!")')),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['output'] == 'Hello, World!')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_eval_endpoint_handles_syntax_errors(self):
        """Ensure the /eval route returns a syntax error properly."""
        with self.client:
            response = self.client.post(
                '/eval',
                data=json.dumps(dict(code='print("Hello, World! ')),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['output'] != 'Hello, World!')
            self.assertIn(
                'SyntaxError: EOL while scanning string literal',
                data['output']
            )
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_eval_endpoint_handles_name_errors(self):
        """Ensure the /eval route returns a name error properly."""
        with self.client:
            response = self.client.post(
                '/eval',
                data=json.dumps(dict(code='console.log("Hello, World!")')),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['output'] != 'Hello, World!')
            self.assertIn(
                "NameError: name 'console' is not defined",
                data['output']
            )
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_eval_endpoint_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/eval',
                data=json.dumps(dict()),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_eval_endpoint_no_code(self):
        with self.client:
            response = self.client.post(
                '/eval',
                data=json.dumps(dict(code='')),
                content_type='application/json',
                headers=dict(Authorization='Bearer test')
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])
