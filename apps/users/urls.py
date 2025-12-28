from django.urls import path
from apps.users.views.jwt_views import AdminOnlyView, RegisterView, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.views import MeView 
from apps.users.views.jwt_views import CustomTokenObtainPairView
from apps.users.views.user_views import VerifyTokenView
from .views.user_views import UserProfileView 
from apps.users.views.oauth_views import login_page, index_page

#from .views import UserRegistrationView  


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    #path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("users/me/", MeView.as_view(), name="me"),
    #path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("auth/logout/", LogoutView.as_view(), name= "logout"),
    
    path('verify-token/', VerifyTokenView.as_view(), name='verify_token'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('admin-test/', AdminOnlyView.as_view(), name='admin_test'),
     # DEMO OAuth endpoints
    path("auth/google/", google_oauth_simple, name="google_login"),
    path("auth/google/callback/", google_oauth_callback_simple, name="google_callback"),
    path("demo-login/", lambda r: redirect("/api/v1/index/?demo=true")),
   
]

urlpatterns += [
    path("login/", login_page, name="login_page"),
    path("index/", index_page, name="index_page"),
]
