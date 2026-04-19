from django.db import router
from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi_app.LMSauth.dependencies import get_current_user
from fastapi_app.LMSauth.protected_routes import router
from fastapi_app.database import Base, engine, get_db
from fastapi_app import attendance, assignments, notifications
from fastapi_app.LMSauth import auth_google, auth_facebook, auth_github, auth_otp
from fastapi import APIRouter, Depends
from django.contrib.auth import authenticate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
from fastapi.middleware.cors import CORSMiddleware
from fastapi_app.LMSauth.auth_otp import router as otp_router
from fastapi_app.LMSauth.auth_google import router as google_router
from starlette.middleware.sessions import SessionMiddleware

from fastapi_app.models import Assignment

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(attendance.router)
app.include_router(assignments.router)
app.include_router(notifications.router)


app.include_router(auth_google.router, prefix="/auth")
app.include_router(auth_facebook.router, prefix="/auth")
app.include_router(auth_github.router, prefix="/auth")
app.include_router(auth_otp.router, prefix="/auth")

app.include_router(router)
app.include_router(otp_router)




# app.include_router(google_router, prefix="/auth")

SECRET_KEY = "mysecret"

class LoginSchema(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginSchema):
    if data.username == "Divya" and data.password == "1234":
        token = jwt.encode({"user": data.username}, SECRET_KEY, algorithm="HS256")
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"message": "Access granted", "user": user}


@app.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    # Get unique course IDs from assignments
    courses = db.query(Assignment.course_id).distinct().all()
    return {"count": len(courses), "courses": [c[0] for c in courses]}

