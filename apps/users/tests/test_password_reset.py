# apps/users/tests/test_password_reset.py
import pytest
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User

@pytest.mark.django_db
def test_password_reset_request(client):
    user = User.objects.create_user(
        email="reset@test.com",
        username="resetuser",
        password="oldpassword"
    )

    response = client.post(
        "/api/v1/auth/password/forgot/",
        {"email": "reset@test.com"},
        format="json"
    )

    user.refresh_from_db()

    assert response.status_code == 200
    assert user.password_reset_token is not None
    assert user.password_token_created_at is not None


@pytest.mark.django_db
def test_password_reset_confirm_success(client):
    user = User.objects.create_user(
        email="confirm@test.com",
        username="confirmuser",
        password="oldpassword"
    )

    user.password_reset_token = "reset-token"
    user.password_token_created_at = timezone.now()
    user.save()

    response = client.post(
        f"/api/v1/auth/password/reset/{user.password_reset_token}/",
        {"password": "newpassword123"},
        format="json"
    )

    user.refresh_from_db()

    assert response.status_code == 200
    assert user.password_reset_token is None
    assert user.check_password("newpassword123")


@pytest.mark.django_db
def test_password_reset_expired_token(client):
    user = User.objects.create_user(
        email="expiredreset@test.com",
        username="expiredreset",
        password="oldpassword"
    )

    user.password_reset_token = "expired-token"
    user.password_token_created_at = timezone.now() - timedelta(hours=2)
    user.save()

    response = client.post(
        f"/api/v1/auth/password/reset/{user.password_reset_token}/",
        {"password": "newpassword123"},
        format="json"
    )

    assert response.status_code == 400
