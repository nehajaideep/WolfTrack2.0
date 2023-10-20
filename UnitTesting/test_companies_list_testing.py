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

    def test_applied_companies_list(self):
        resp = self.app.get('/companiesList?status=Applied')
        statuscode = resp.status_code
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")

    def test_in_progress_companies_list(self):
        resp = self.app.get('/companiesList?status=In Progress')
        statuscode = resp.status_code
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")
    
    def test_wishlist_companies_list(self):
        resp = self.app.get('/companiesList?status=Wishlist')
        statuscode = resp.status_code
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")
        
    def test_offers_companies_list(self):
        resp = self.app.get('/companiesList?status=Offer')
        statuscode = resp.status_code
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")


if __name__ == "__main__":
    unittest.main()
