from django.test import TestCase
from rest_framework import status
from apps.users.models import User


class AuthTests(TestCase):
    def test_jwt_login_success(self):
        User.objects.create_user(
            email="login@test.com",
            username="loginuser",
            password="test123"
        )

        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": "login@test.com", "password": "test123"},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
