# apps/users/views/oauth_views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import requests
from urllib.parse import urlencode
import json
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User
import uuid

def login_page(request):
    """Render login page with Google OAuth button"""
    return render(request, "users/login.html")

def google_oauth_initiate(request):
    """
    Step 1: Redirect user to Google OAuth consent screen
    GET /api/v1/auth/google/
    """
    # Generate state for CSRF protection
    state = str(uuid.uuid4())
    request.session['oauth_state'] = state
    
    # Google OAuth endpoint
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    
    # Parameters for Google OAuth
    params = {
        'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        'redirect_uri': 'http://127.0.0.1:8000/api/v1/auth/google/callback/',
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid',
        'access_type': 'offline',  # Get refresh token
        'prompt': 'consent',  # Always show consent screen
        'state': state,  # CSRF protection
    }
    
    # Build the URL
    authorization_url = f"{google_auth_url}?{urlencode(params)}"
    print(f"🔗 Redirecting to Google: {authorization_url}")
    
    return redirect(authorization_url)

def google_oauth_callback(request):
    """
    Step 2: Handle Google OAuth callback
    GET /api/v1/auth/google/callback/?code=...&state=...
    """
    print(f"📥 Received callback with params: {dict(request.GET)}")
    
    # Get parameters from callback
    code = request.GET.get('code')
    state = request.GET.get('state')
    error = request.GET.get('error')
    
    # Check for errors from Google
    if error:
        print(f"❌ Google OAuth error: {error}")
        return render(request, "users/error.html", {
            "error": f"Google OAuth error: {error}"
        })
    
    # Validate state (CSRF protection)
    session_state = request.session.get('oauth_state')
    if not session_state or state != session_state:
        print(f"❌ State mismatch: session={session_state}, received={state}")
        return render(request, "users/error.html", {
            "error": "Invalid state parameter. Possible CSRF attack."
        })
    
    # Clean up session state
    if 'oauth_state' in request.session:
        del request.session['oauth_state']
    
    # Check if we have authorization code
    if not code:
        print("❌ No authorization code received")
        return render(request, "users/error.html", {
            "error": "No authorization code received from Google"
        })
    
    print(f"✅ Received authorization code: {code[:20]}...")
    
    try:
        # Step 3: Exchange authorization code for tokens
        print("🔄 Exchanging code for access token...")
        token_response = exchange_code_for_token(code)
        
        if 'error' in token_response:
            print(f"❌ Token exchange error: {token_response}")
            return render(request, "users/error.html", {
                "error": f"Failed to exchange code: {token_response.get('error_description', 'Unknown error')}"
            })
        
        access_token = token_response.get('access_token')
        refresh_token = token_response.get('refresh_token')
        id_token = token_response.get('id_token')
        
        print(f"✅ Got access token: {access_token[:20]}...")
        if refresh_token:
            print(f"✅ Got refresh token: {refresh_token[:20]}...")
        
        # Step 4: Get user info from Google
        print("🔄 Fetching user info from Google...")
        user_info = get_google_user_info(access_token)
        
        if 'error' in user_info:
            print(f"❌ User info error: {user_info}")
            return render(request, "users/error.html", {
                "error": f"Failed to get user info: {user_info.get('error', 'Unknown error')}"
            })
        
        email = user_info.get('email')
        name = user_info.get('name', '')
        given_name = user_info.get('given_name', '')
        picture = user_info.get('picture', '')
        
        print(f"✅ Got user info - Email: {email}, Name: {name}")
        
        if not email:
            print("❌ No email in user info")
            return render(request, "users/error.html", {
                "error": "No email received from Google"
            })
        
        # Step 5: Create or get user in database
        print(f"🔄 Creating/fetching user: {email}")
        user, is_new_user = get_or_create_user(email, name, given_name)
        
        # Step 6: Generate JWT tokens
        print("🔄 Generating JWT tokens...")
        jwt_tokens = generate_jwt_tokens(user)
        
        # Step 7: Store in session (optional, for frontend)
        request.session['user_id'] = str(user.id)
        request.session['user_email'] = user.email
        request.session['access_token'] = jwt_tokens['access']
        request.session['refresh_token'] = jwt_tokens['refresh']
        
        # Step 8: Prepare success response
        print(f"🎉 Login successful! Redirecting to index page")
        
        context = {
            "user": {
                "email": user.email,
                "username": user.username,
                "name": name or user.username,
                "role": user.role,
                "is_new_user": is_new_user,
            },
            "tokens": {
                "access": jwt_tokens['access'][:50] + "...",
                "refresh": jwt_tokens['refresh'][:50] + "...",
            },
            "message": "Account created successfully! Welcome!" if is_new_user else "Welcome back!"
        }
        
        return render(request, "users/index.html", context)
        
    except Exception as e:
        print(f"💥 Exception in callback: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return render(request, "users/error.html", {
            "error": f"Internal server error: {str(e)}"
        })

def exchange_code_for_token(code):
    """
    Exchange authorization code for access token
    """
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        'code': code,
        'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        'redirect_uri': 'http://127.0.0.1:8000/api/v1/auth/google/callback/',
        'grant_type': 'authorization_code',
    }
    
    try:
        response = requests.post(token_url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Token exchange request failed: {e}")
        return {"error": str(e)}

def get_google_user_info(access_token):
    """
    Get user info from Google using access token
    """
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(userinfo_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ User info request failed: {e}")
        return {"error": str(e)}

def get_or_create_user(email, full_name, given_name):
    """
    Get existing user or create new one
    """
    try:
        user = User.objects.get(email=email)
        print(f"✅ Existing user found: {user.email}")
        return user, False
    except User.DoesNotExist:
        print(f"🆕 Creating new user: {email}")
        
        # Generate username from email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        
        # Ensure unique username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=None,  # OAuth users don't need password
            role='customer',  # Default role
            is_active=True
        )
        
        # Set name if available
        if given_name:
            user.first_name = given_name
        
        user.save()
        print(f"✅ New user created: {user.email} (ID: {user.id})")
        return user, True

def generate_jwt_tokens(user):
    """
    Generate JWT access and refresh tokens
    """
    refresh = RefreshToken.for_user(user)
    
    # Add custom claims
    refresh['email'] = user.email
    refresh['role'] = user.role
    refresh['username'] = user.username
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

@login_required
def index_page(request):
    """Protected index page"""
    user = request.user
    return render(request, "users/index.html", {
        "user": {
            "email": user.email,
            "username": user.username,
            "role": user.role,
        }
    })

def logout_view(request):
    """Clear session"""
    request.session.flush()
    return redirect('login_page')