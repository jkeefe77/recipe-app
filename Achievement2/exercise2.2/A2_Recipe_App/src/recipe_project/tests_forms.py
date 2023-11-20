from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import LoginForm


class LoginFormTestCase(TestCase):
    def test_valid_login_form(self):
        form = LoginForm(data={"username": "testuser", "password": "testpass"})
        self.assertTrue(form.is_valid())

    def test_invalid_login_form_missing_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)

    def test_invalid_login_form_missing_username(self):
        form = LoginForm(data={"password": "testpass"})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_invalid_login_form_missing_password(self):
        form = LoginForm(data={"username": "testuser"})
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)
