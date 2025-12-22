# apps/users/services/jwt.py

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def blacklist_refresh_token(refresh_token: str):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError:
        raise ValueError("Invalid or expired refresh token")
