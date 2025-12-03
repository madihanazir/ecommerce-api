from django.urls import path
from .views import RegisterView, LoginView, MeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#from .views import UserRegistrationView  

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("users/me/", MeView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('auth/register/', UserRegistrationView.as_view(), name='register'),
]
