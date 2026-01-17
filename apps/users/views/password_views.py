import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User
from apps.users.serializers import ForgotPasswordSerializer
from apps.users.services.password_service import PasswordService
from django.core.mail import send_mail


from apps.users.serializers import ResetPasswordSerializer

import uuid
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import User
from apps.users.serializers import ForgotPasswordSerializer


class PasswordResetConfirmView(APIView):
    def post(self, request, token):
        password = request.data.get("password")

        try:
            user = User.objects.get(password_reset_token=token)
        except User.DoesNotExist:
            return Response({"error": "Invalid token"}, status=400)

        user.set_password(password)
        user.password_reset_token = None
        user.save()

        return Response({"message": "Password reset successful"})
    





class ForgotPasswordView(APIView):
    def post(self, request):
        print("🔥 FORGOT PASSWORD VIEW HIT")

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
            PasswordService.send_reset_email(user, request)
            print("📧 PASSWORD RESET EMAIL SENT")
        except User.DoesNotExist:
            pass  # security

        return Response(
            {"message": "If the email exists, a reset link has been sent"},
            status=status.HTTP_200_OK
        )

class ResetPasswordView(APIView):
    def post(self, request, token):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(password_reset_token=token)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not PasswordService.is_token_valid(user):
            return Response(
                {"error": "Token expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data["password"])
        user.password_reset_token = None
        user.password_token_created_at = None
        user.save()

        return Response({
            "success": True,
            "message": "Password reset successful"
        }, status=status.HTTP_200_OK)

