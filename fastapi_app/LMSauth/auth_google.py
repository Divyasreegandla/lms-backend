from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os
from starlette.config import Config
from .jwt_handler import create_access_token
from .django_setup import *
from accounts.models import SocialAccount

router = APIRouter()

# ENV
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
config = Config(os.path.join(BASE_DIR, ".env"))

# OAuth
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=config("GOOGLE_CLIENT_ID"),
    client_secret=config("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get("/google")
async def google_login(request: Request):
    """Redirect to Google login"""
    redirect_uri = "http://localhost:8001/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request):
    """Handle Google callback and redirect to frontend"""
    try:
        token = await oauth.google.authorize_access_token(request)
        
        resp = await oauth.google.get("userinfo", token=token)
        user_info = resp.json()
        
        user, created = SocialAccount.objects.get_or_create(
            provider="google",
            provider_id=user_info["sub"],
            defaults={
                "email": user_info.get("email"),
                "name": user_info.get("name")
            }
        )
        
        access_token = create_access_token({
            "user_id": user.id,
            "email": user.email,
            "name": user.name
        })
        
        frontend_url = f"http://localhost:3000/dashboard.html?token={access_token}"
        return RedirectResponse(url=frontend_url)
        
    except Exception as e:
        print(f"Google callback error: {str(e)}")
        return RedirectResponse(url="http://localhost:3000/index.html?error=google_login_failed")