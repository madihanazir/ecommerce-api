from rest_framework import serializers
from .models import User
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

        user.email_verification_token = uuid.uuid4()
        user.email_token_created_at = timezone.now()

        user.save()
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




