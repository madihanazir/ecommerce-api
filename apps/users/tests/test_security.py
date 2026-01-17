# apps/users/tests/test_security.py
import pytest
from apps.users.models import User

@pytest.mark.django_db
def test_password_reset_does_not_leak_user_existence(client):
    response = client.post(
        "/api/v1/auth/password/forgot/",
        {"email": "doesnotexist@test.com"},
        format="json"
    )

    assert response.status_code == 200
    assert "reset link" in response.data["message"].lower()


@pytest.mark.django_db
def test_invalid_email_verification_token(client):
    response = client.get(
        "/api/v1/auth/verify-email/00000000-0000-0000-0000-000000000000/"
    )

    assert response.status_code in [400, 404]
