from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User
import uuid


class EmailVerificationTests(TestCase):
    def test_email_verification_success(self):
        user = User.objects.create_user(
            email="verify@test.com",
            username="verifyuser",
            password="test123"
        )

        user.email_verification_token = uuid.uuid4()
        user.email_token_created_at = timezone.now()
        user.save()

        response = self.client.get(
            f"/api/v1/auth/verify-email/{user.email_verification_token}/"
        )

        user.refresh_from_db()
        self.assertTrue(user.email_verified)
