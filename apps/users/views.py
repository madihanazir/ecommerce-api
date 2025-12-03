from .models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer



class LoginView(generics.GenericAPIView):
    serializer_class = RegisterSerializer  # reuse username/password validation not needed

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        from .models import User
        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
