from unittest.main import main
from flask import app
from flask.typing import StatusCode
import unittest
import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from main import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    #check if response is 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_add_new(self):
        resp = self.app.get('/add_New')
        statuscode = resp.status_code
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")

    def test_add_new_statuscode(self):
        resp = self.app.get('/add_New')
        statuscode = resp.status_code
        self.assertEqual(statuscode,400)

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

    def test_word_cloud_creation(self):
        input = "Technical Stack Bootstrap, JS Python, Django, Celery, Redis and MySQL Solidity, Geth and IPFS"
        os.chdir("..")
        print(os.getcwd())
        pass
    
    #check if response is 200
    def test_admin(self):
        tester = app.test_client(self)
        response = tester.get("/main_login/admin_login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #check if content returned is application/json
    def test_admin_content(self):
        tester = app.test_client(self)
        response = tester.get("/main_login/admin_login")
        self.assertEqual(response.content_type, "text/html")

    #check if response is 200
    def test_user(self):
        tester = app.test_client(self)
        response = tester.get("/main_login/user_login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    #check if content returned is application/json
    def test_user_content(self):
        tester = app.test_client(self)
        response = tester.get("/main_login/user_login")
        self.assertEqual(response.content_type, "text/html")

    #check if content returned is application/json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        self.assertEqual(response.content_type, "text/html")

    #check if content returned is application/json
    def test_main_landing_page_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
    
    #check if response is 200
    def test_main_landing_page_status(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #check data returned
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        self.assertEqual(b'WolfTrack' in response.data, True)

if __name__=="__main__":
     unittest.main()