# apps/users/tests/test_email.py
import pytest
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User

@pytest.mark.django_db
def test_email_verification_success(client):
    user = User.objects.create_user(
        email="verify@test.com",
        username="verifyuser",
        password="test123"
    )

    user.email_verification_token = "test-token"
    user.email_token_created_at = timezone.now()
    user.is_verified = False
    user.save()

    url = f"/api/v1/auth/verify-email/{user.email_verification_token}/"
    response = client.get(url)

    user.refresh_from_db()

    assert response.status_code == 200
    assert user.is_verified is True
    assert user.email_verification_token is None


@pytest.mark.django_db
def test_email_verification_expired_token(client):
    user = User.objects.create_user(
        email="expired@test.com",
        username="expireduser",
        password="test123"
    )

    user.email_verification_token = "expired-token"
    user.email_token_created_at = timezone.now() - timedelta(hours=25)
    user.is_verified = False
    user.save()

    url = f"/api/v1/auth/verify-email/{user.email_verification_token}/"
    response = client.get(url)

    user.refresh_from_db()

    assert response.status_code == 400
    assert user.is_verified is False
