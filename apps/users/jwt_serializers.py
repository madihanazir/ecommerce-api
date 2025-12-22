from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Adds custom claims to JWT
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        token["user_id"] = str(user.id)
        token["email"] = user.email
        token["role"] = user.role
        token["token_type"] = "access" 

        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to response
        data.update({
            'user_id': str(self.user.id),
            'email': self.user.email,
            'role': self.user.role,
        })
        
        return data
