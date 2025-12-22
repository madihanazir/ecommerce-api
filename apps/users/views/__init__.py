from .jwt_views import RegisterView, LoginView, LogoutView
from .user_views import UserProfileView
from .jwt_views import CustomTokenObtainPairView
"""
try:
    from apps.users.views import MeView
except ImportError:
    # Fallback
    from ..views import MeView """
from .user_views import MeView


__all__ = [
    'UserProfileView',
    'CustomTokenObtainPairView',
    
]