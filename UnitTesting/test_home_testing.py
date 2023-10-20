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

    def test_add_new(self):
        resp = self.app.get('/add_New')
        statuscode = resp.status_code
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")

    def test_send_email(self):
        resp = self.app.get('/add_New')
        #print(resp.content_type)
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")
    
    def test_home_resume_analyzer_ui_render_routing(self):
        resp = self.app.get('/resumeAnalyzer')
        statuscode = resp.status_code
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")
    
    def test_jobfinder_ui_render_routing(self):
        resp = self.app.get('/findJobs')
        statuscode = resp.status_code
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")

    def test_resume_parser_ui_render_routing(self):
        resp = self.app.get('/analyze_resume')
        statuscode = resp.status_code
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")


if __name__ == "__main__":
    unittest.main()
