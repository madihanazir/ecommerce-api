from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User
from datetime import timedelta


class VerifyEmailView(APIView):
    def post(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
        except User.DoesNotExist:
            return Response({"error": "Invalid token"}, status=400)

        if timezone.now() - user.email_token_created_at > timedelta(hours=24):
            return Response({"error": "Token expired"}, status=400)

        user.email_verified = True
        user.is_active = True    
        user.email_verification_token = None
        user.email_token_created_at = None
        user.save()

        return Response({"message": "Email verified successfully"})

