from unittest import TestCase
from app import app
from flask import session

class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with self.client as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('board', session)

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['C', 'A', 'T', 'S', 'Y']] * 5
            resp = client.get('/check-word?word=cat')
            self.assertEqual(resp.json['result'], 'ok')

    def test_invalid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['A'] * 5] * 5
            resp = client.get('/check-word?word=impossible')
            self.assertEqual(resp.json['result'], 'not-on-board')

