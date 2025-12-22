from rest_framework import generics, permissions
from apps.users.serializers import UserSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response




class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class VerifyTokenView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Token is already validated, user is attached to request
        return Response({
            'message': 'Token is valid',
            'user': {
                'id': str(request.user.id),
                'email': request.user.email,
                'role': request.user.role,
                'username': request.user.username
            },
            # Raw claims from token (if you need them)
            'token_claims': {
                'user_id': str(request.user.id),
                'email': request.user.email,
                'role': request.user.role
            }
        })
    



class UserProfileView(APIView):
    """Get current user's profile from JWT token"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Access user from request (automatically populated by JWT)
        user = request.user
        
        return Response({
            'user_id': str(user.id),
            'email': user.email,
            'role': user.role,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
        })
