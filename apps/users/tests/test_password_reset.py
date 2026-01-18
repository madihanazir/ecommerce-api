from django.test import TestCase
from django.utils import timezone
from apps.users.models import User
import uuid


class PasswordResetTests(TestCase):
    def test_password_reset_request(self):
        user = User.objects.create_user(
            email="reset@test.com",
            username="resetuser",
            password="oldpassword"
        )

        response = self.client.post(
            "/api/v1/auth/password/forgot/",
            {"email": "reset@test.com"},
            content_type="application/json"
        )

        user.refresh_from_db()
        self.assertIsNotNone(user.password_reset_token)
