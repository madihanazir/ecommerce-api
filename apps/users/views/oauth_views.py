# apps/users/views/oauth_views.py

import secrets
import requests
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User


class GoogleOAuthInitView(APIView):
    """
    Redirect user to Google OAuth consent screen
    """
    permission_classes = [AllowAny]

    def get(self, request):
        state = secrets.token_urlsafe(16)
        request.session["oauth_state"] = state

        params = {
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }

        url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
        return redirect(url)


class GoogleOAuthCallbackView(APIView):
    """
    Step 2: Google redirects back here
    """
    permission_classes = [AllowAny]
    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")

        if not code or state != request.session.get("oauth_state"):
           return redirect("/api/v1/login/?error=oauth_state")

        # Exchange code for access token
        token_res = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            timeout=10,
        )

        token_res.raise_for_status()
        access_token = token_res.json()["access_token"]

        # Fetch user profile
        profile_res = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )

        profile_res.raise_for_status()
        profile = profile_res.json()

        email = profile.get("email")
        if not email:
            return redirect("/api/v1/login/?error=no_email")

        # Create or fetch user
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "role": "customer",
                "is_active": True,
            },
        )

        # Issue JWT
        
        refresh = RefreshToken.for_user(user)

            # Store something minimal in session for logged-in state
        request.session["oauth_user"] = user.email

            # Redirect to index page 
        response=  redirect("/api/v1/index/")
        
        #here im setting jwt cookie to make sure JWT is issued and stored securely for stateless API access
        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            secure=False,   # True in production
            samesite="Lax",
        )
        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        return response

