from fastapi import APIRouter, HTTPException
import random
from django.utils import timezone
from datetime import timedelta

from pydantic import BaseModel
from .jwt_handler import create_access_token
from .django_setup import *
from accounts.models import OTPLog

router = APIRouter()

def generate_otp():
    return str(random.randint(100000, 999999))

class OTPRequest(BaseModel):
    phone:str

@router.post("/send-otp")
def send_otp(data:OTPRequest):
    phone=data.phone
    otp = generate_otp()

    OTPLog.objects.create(
        phone=phone,
        otp=otp,
        expires_at=timezone.now() + timedelta(minutes=5)
    )

    print("OTP:", otp)

    return {"message": "OTP sent"}

class VerifyOTPRequest(BaseModel):
    phone:str
    otp:str

@router.post("/verify-otp")
def verify_otp(data:VerifyOTPRequest):
    phone=data.phone
    otp=data.otp
    record = OTPLog.objects.filter(phone=phone).order_by("-created_at").first()

    if not record:
        raise HTTPException(status_code=404, detail="OTP not found")

    if timezone.now() > record.expires_at:
        raise HTTPException(400, "Expired")

    record.is_verified = True
    record.save()

    token = create_access_token({"phone": phone})

    return {"message":"OTP Verified","access_token": token}