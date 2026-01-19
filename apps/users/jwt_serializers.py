from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user_id"] = str(user.id)
        token["email"] = user.email
        token["role"] = user.role
        token["token_type"] = "access" 

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        # 🔒 BLOCK LOGIN IF EMAIL NOT VERIFIED
        if not user.email_verified:
            raise serializers.ValidationError("Email not verified")

        data.update({
            'user_id': str(user.id),
            'email': user.email,
            'role': user.role,
        })

        return data
