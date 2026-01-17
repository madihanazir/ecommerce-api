# apps/users/tests/test_auth.py
import pytest
from django.urls import reverse
from rest_framework import status
from apps.users.models import User

@pytest.mark.django_db
def test_jwt_login_success(client):
    user = User.objects.create_user(
        email="login@test.com",
        username="loginuser",
        password="test123"
    )

    response = client.post(
        "/api/v1/auth/login/",
        {"email": "login@test.com", "password": "test123"},
        format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data["data"]
    assert "refresh" in response.data["data"]
    assert response.data["data"]["email"] == "login@test.com"


@pytest.mark.django_db
def test_jwt_login_invalid_password(client):
    user = User.objects.create_user(
        email="badlogin@test.com",
        username="badlogin",
        password="test123"
    )

    response = client.post(
        "/api/v1/auth/login/",
        {"email": "badlogin@test.com", "password": "wrong"},
        format="json"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["success"] is False


@pytest.mark.django_db
def test_user_registration(client):
    response = client.post(
        "/api/v1/auth/register/",
        {
            "email": "new@test.com",
            "username": "newuser",
            "password": "test123",
            "phone": "1234567890"
        },
        format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="new@test.com").exists()
