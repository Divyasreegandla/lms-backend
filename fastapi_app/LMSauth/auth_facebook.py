from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
import requests
from .jwt_handler import create_access_token
from .django_setup import *
from accounts.models import SocialAccount

router = APIRouter()

# Facebook OAuth settings
FACEBOOK_CLIENT_ID = "your_facebook_client_id"  # Replace with your actual client ID
FACEBOOK_CLIENT_SECRET = "your_facebook_client_secret"  # Replace with your actual secret

@router.get("/facebook")
async def facebook_login():
    """Redirect to Facebook login"""
    redirect_uri = "http://localhost:8001/auth/facebook/callback"
    facebook_auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={redirect_uri}&scope=email,public_profile"
    return RedirectResponse(url=facebook_auth_url)

@router.get("/facebook/callback")
async def facebook_callback(request: Request, code: str = None):
    """Handle Facebook callback"""
    try:
        if not code:
            return RedirectResponse(url="http://localhost:3000/index.html?error=no_code")
       
        redirect_uri = "http://localhost:8001/auth/facebook/callback"
        token_url = f"https://graph.facebook.com/v18.0/oauth/access_token?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={redirect_uri}&client_secret={FACEBOOK_CLIENT_SECRET}&code={code}"
        
        token_response = requests.get(token_url)
        token_data = token_response.json()
        
        access_token = token_data.get("access_token")
        if not access_token:
            return RedirectResponse(url="http://localhost:3000/index.html?error=no_token")
        
        user_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
        user_response = requests.get(user_url)
        user_data = user_response.json()
        
        user, created = SocialAccount.objects.get_or_create(
            provider="facebook",
            provider_id=user_data.get("id"),
            defaults={
                "email": user_data.get("email"),
                "name": user_data.get("name")
            }
        )
     
        jwt_token = create_access_token({
            "user_id": user.id,
            "email": user.email,
            "name": user.name
        })
        
        frontend_url = f"http://localhost:3000/dashboard.html?token={jwt_token}"
        return RedirectResponse(url=frontend_url)
        
    except Exception as e:
        print(f"Facebook callback error: {str(e)}")
        return RedirectResponse(url="http://localhost:3000/index.html?error=facebook_login_failed")