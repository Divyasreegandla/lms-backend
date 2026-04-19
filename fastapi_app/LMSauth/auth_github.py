from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
from .jwt_handler import create_access_token
from .django_setup import *
from accounts.models import SocialAccount

router = APIRouter()

GITHUB_CLIENT_ID = "your_github_client_id" 
GITHUB_CLIENT_SECRET = "your_github_client_secret" 

@router.get("/github")
async def github_login():
    """Redirect to GitHub login"""
    redirect_uri = "http://localhost:8001/auth/github/callback"
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={redirect_uri}&scope=user:email"
    return RedirectResponse(url=github_auth_url)

@router.get("/github/callback")
async def github_callback(request: Request, code: str = None):
    """Handle GitHub callback"""
    try:
        if not code:
            return RedirectResponse(url="http://localhost:3000/index.html?error=no_code")
        
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": "http://localhost:8001/auth/github/callback"
        }
        token_headers = {"Accept": "application/json"}
        
        token_response = requests.post(token_url, data=token_data, headers=token_headers)
        token_json = token_response.json()
        
        access_token = token_json.get("access_token")
        if not access_token:
            return RedirectResponse(url="http://localhost:3000/index.html?error=no_token")
        
        user_headers = {"Authorization": f"Bearer {access_token}"}
        user_response = requests.get("https://api.github.com/user", headers=user_headers)
        user_data = user_response.json()
        
        email_response = requests.get("https://api.github.com/user/emails", headers=user_headers)
        emails = email_response.json()
        primary_email = None
        for email in emails:
            if email.get("primary"):
                primary_email = email.get("email")
                break
        
        user, created = SocialAccount.objects.get_or_create(
            provider="github",
            provider_id=str(user_data.get("id")),
            defaults={
                "email": primary_email or f"{user_data.get('login')}@github.com",
                "name": user_data.get("name") or user_data.get("login")
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
        print(f"GitHub callback error: {str(e)}")
        return RedirectResponse(url="http://localhost:3000/index.html?error=github_login_failed")