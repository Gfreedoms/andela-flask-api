
import unittest
import os
import json

from app.views import app, is_testing
from app.models import db

from app.tests.common_requests import CommonRequests

class LoginTestCase(CommonRequests):
    """This class represents the login test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        is_testing()
        self.app = app
        self.client = self.app.test_client

        self.sign_up_credentials = {'username': 'vince', "email": "vincenthokie@gmail.com", "password": "123",
                               "password2": "123"}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_login(self):
        """Test API can create a user (POST request)"""

        self.sign_up(self.sign_up_credentials)

        login_credentials = {'username': 'vince', "password": "123"}
        res = self.login(login_credentials)

        self.assertEqual(res.status_code, 200)
        self.assertIn('token', res.data)

    def test_login_password_required(self):
        """Test API can notice password is required (POST request)."""

        self.sign_up(self.sign_up_credentials)

        login_credentials = {'username': 'vince', "password": ""}
        res = self.login(login_credentials)

        self.assertEqual(res.status_code, 200)
        self.assertNotIn('token', res.data)
        self.assertIn("error", res.data)

    def test_login_username_required(self):
        """Test API can notice username is required (POST request)."""

        self.sign_up(self.sign_up_credentials)

        login_credentials = {'username': '', "password": "123"}
        res = self.login(login_credentials)

        self.assertEqual(res.status_code, 200)
        self.assertNotIn('token', res.data)
        self.assertIn("error", res.data)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()