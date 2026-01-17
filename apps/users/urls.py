from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views.email_views import VerifyEmailView
from apps.users.views.jwt_views import (
    RegisterView, LoginView, LogoutView, 
    CustomTokenObtainPairView, AdminOnlyView
)

from apps.users.views.password_views import PasswordResetConfirmView
from apps.users.views.user_views import ( MeView, VerifyTokenView, UserProfileView, IndexView, logout_view, )
from apps.users.views.template_views import login_page, index_page
from apps.users.views.oauth_views import (
    GoogleOAuthInitView,
    GoogleOAuthCallbackView,
)

from apps.users.views.password_views import (
    ForgotPasswordView,
    ResetPasswordView
)

urlpatterns = [
    # JWT Authentication endpoints
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    
    # User endpoints
    path("users/me/", MeView.as_view(), name="me"),
    path("verify-token/", VerifyTokenView.as_view(), name="verify_token"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("admin-test/", AdminOnlyView.as_view(), name="admin_test"),
    
    # OAuth2 endpoints
    path("auth/google/", GoogleOAuthInitView.as_view(), name="google_login"),
    path("auth/google/callback/", GoogleOAuthCallbackView.as_view(), name="google_callback"),
    
    
    
    # Template pages
    path("login/", login_page, name="login_page"),
    path("index/", index_page, name="index_page"),
    path("logout/", logout_view, name="logout"),

    path("me/", MeView.as_view(), name="me"),
    path("auth/verify-email/<uuid:token>/", VerifyEmailView.as_view()),

    path("auth/reset-password/<uuid:token>/", PasswordResetConfirmView.as_view()),

    path("auth/password/forgot/", ForgotPasswordView.as_view(), name="forgot_password"),
    
    path("auth/password/reset/<uuid:token>/", ResetPasswordView.as_view(), name="reset_password"),


    
    
]