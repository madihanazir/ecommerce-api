from rest_framework import serializers
from .models import User
from django.core.mail import send_mail 
from django.conf import settings
import uuid
from django.utils import timezone


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "password"]

    def create(self, validated_data):
        #validated_data['role'] = 'customer'
        #return User.objects.create_user(**validated_data)
        user = User.objects.create_user(**validated_data)
        user.role = "user"
        user.is_active = False
        user.email_verified = False

  
        user.email_verification_token = uuid.uuid4()
        user.email_token_created_at = timezone.now()

        user.save()
        # building verify link
        verification_link = (
            f"http://127.0.0.1:8000/api/v1/auth/verify-email/?token={user.email_verification_token}"
        )

        # Send email (console)
        send_mail(
            subject="Verify your email",
            message=f"Click this link to verify your email:\n\n{verification_link}\n\nThis link will expire in 24 hours.\n\nBest regards,\nE-Commerce Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "role", "created_at"]




