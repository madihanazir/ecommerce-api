# apps/users/views/__init__.py
from .jwt_views import RegisterView, LoginView, LogoutView
"""
try:
    from apps.users.views import MeView
except ImportError:
    # Fallback
    from ..views import MeView """
from .user_views import MeView