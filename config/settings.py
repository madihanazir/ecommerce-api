from decouple import config
from pathlib import Path
import os
import sys
from datetime import timedelta


# ---- BASE PROJECT CONFIG ----
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

SECRET_KEY = "django-insecure-9x2&@l!f3$5p7d!jw#z9r!q2y_@k0^n1v&b4c9u_l$"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ---- INSTALLED APPS ----
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',

# Local apps 
'apps.users.apps.UsersConfig',
# 'users',                 
    # 'apps.users',            
    # 'apps.users.apps.UsersConfig',  
    
    'products.apps.ProductsConfig',
    'apps.cart.apps.CartConfig',
    'apps.orders.apps.OrdersConfig',

    
    # 'cart',                  
    # 'orders',               
    # 'common',    
    'rest_framework_simplejwt.token_blacklist',  

    "social_django", 

]

# ---- REST FRAMEWORK CONFIG ----
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        #'rest_framework.authentication.TokenAuthentication',
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # As per requirements
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    
    "USERNAME_FIELD": "email",
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
]
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_JSONFIELD_ENABLED = True

LOGIN_REDIRECT_URL = "/index/"
LOGOUT_REDIRECT_URL = "/login/"



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# ---- SPECTACULAR OPENAPI ----
SPECTACULAR_SETTINGS = {
    "TITLE": "E-Commerce API",
    "VERSION": "1.0.0",
}

# ---- CUSTOM USER MODEL ----
AUTH_USER_MODEL = "users.User"


# ---- MIDDLEWARE ----
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'django.middleware.common.CommonMiddleware',
     'config.middleware.ResponseWrapperMiddleware',
     'django.contrib.auth.middleware.AuthenticationMiddleware',
     'allauth.account.middleware.AccountMiddleware',  

]
CORS_ALLOW_ALL_ORIGINS = True

# ---- TEMPLATES (Minimal - just for admin) ----
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "apps" / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

LOGIN_REDIRECT_URL = "/index/"
LOGOUT_REDIRECT_URL = "/login/"




# ---- INTERNATIONALIZATION ----
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---- STATIC FILES ----
STATIC_URL = 'static/'

# ---- URL CONFIG ----
ROOT_URLCONF = 'config.urls'

# ---- DEFAULT AUTO FIELD ----
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'