
from flask.typing import StatusCode

import unittest
import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from main import app


# Testing template
class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
      
    def test_chat_gpt_analyzer(self):
    resp = self.app.get('/chat_gpt_analyzer/')
    status_code = resp.status_code
    self.assertEqual(resp.content_type, "text/html; charset=utf-8")
    self.assertIn(b'Expected String in Response', resp.data)

if __name__ == "__main__":
    unittest.main()
