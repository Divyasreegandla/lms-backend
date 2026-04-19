# LMS Backend

## Overview

This project is a Learning Management System backend using:

* FastAPI (Attendance, Assignments, Notifications)
* Django (Analytics)
---------------------------------
## Setup

### Install dependencies

```
pip install -r requirements.txt
```

### Run FastAPI

```
uvicorn fastapi_app.main:app --reload
```

### Run Django

```
cd django_app
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8001
```

------------------------------------------------

## API Docs

### 📊 Attendance

* POST `/attendance/mark` → Mark attendance
* GET `/attendance/student/{student_id}?course_id=1` → Student attendance
* GET `/attendance/course/{course_id}?from_date=&to_date=` → Course attendance

---

### 📚 Assignments

* POST `/assignments/create` → Create assignment
* POST `/assignments/submit` → Submit assignment
* GET `/assignments/submissions` → View submissions
* PUT `/assignments/grade` → Grade submission

---

### 🔔 Notifications

* GET `/notifications/{user_id}` → Get notifications
* POST `/notifications/mark-read` → Mark as read

---

### 📈 Analytics (Django)

* GET `/analytics/dashboard/?course_id=1`

---------------------------------------------------

## Notes

* Run both FastAPI (8000) and Django (8001)
* Use Postman or Swagger (`/docs`) for testing

-------------------------------------------------------

LMS Authentication System (FastAPI + Django)

📌 Project Overview

This project implements a complete authentication system for an LMS using:

- Social logins (Google, Facebook, GitHub) via OAuth2
- OTP-based login/signup
- JWT-based authentication
- Django Admin panel for monitoring users and logs

The system is built using a hybrid architecture:

- FastAPI → Authentication APIs
- Django → Database & Admin Panel

---

🚀 Features Implemented

🔑 1. Social Login (OAuth2)

Users can log in using:

- Google
- Facebook
- GitHub

Flow:

1. User sends access token
2. Backend verifies token with provider
3. User is created or fetched
4. JWT token is generated

---

📱 2. OTP-Based Login/Signup

- OTP sent to user (email/phone simulation)
- OTP verification required for login/signup

Features:

- Generate OTP
- Verify OTP
- Expiry validation
- Secure authentication

---

🔐 3. JWT Authentication

- Token generated after:
  
  - Social login
  - OTP verification

- Used for:
  
  - Accessing protected APIs

---

🛠️ 4. Django Admin Panel

Admin can manage:

- Users
- Social Accounts
- OTP Logs

Access:

http://127.0.0.1:8001/admin

---

🧩 Modules Implemented

🔹 FastAPI Routes

- "auth_google.py"
- "auth_facebook.py"
- "auth_github.py"
- "auth_otp.py"

---

🔹 Django Models

SocialAccount

- user_id
- provider (google/facebook/github)
- provider_user_id
- access_token

OTPLog

- user
- otp
- is_verified
- created_at
- expiry_time

---

🏗️ Project Structure

lms_backend/
│
├── fastapi_app/
│ ├── main.py
│ ├── LMSauth/
│ │ ├── auth_google.py
│ │ ├── auth_facebook.py
│ │ ├── auth_github.py
│ │ ├── auth_otp.py
│ │ ├── jwt_handler.py
│ │ └── dependencies.py
│
├── django_app/
│ ├── manage.py
│ ├── accounts/
│ │ ├── models.py
│ │ └── admin.py
│ └── lms/
│
├── requirements.txt
└── README.md

---

⚙️ Tech Stack

- FastAPI
- Django
- MySQL / SQLite
- SQLAlchemy
- Django ORM
- JWT (PyJWT)
- OAuth2
- Postman

---

▶️ Setup Instructions

🔹 1. Clone Repository

cd lms_backend

---

🔹 2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate

---

🔹 3. Install Dependencies

pip install -r requirements.txt

---

🔐 OAuth Key Setup

🔹 Google

1. Go to Google Cloud Console
2. Create OAuth Client
3. Add redirect URI
4. Copy:
   - Token Id

---

🔹 Facebook

1. Go to Facebook Developers
2. Create App
3. Add Facebook Login
4. Copy:
   - Token Id

---

🔹 GitHub

1. Go to GitHub Developer Settings
2. Create OAuth App
3. Copy:
   - Token Id

---

🟢 Running the Project

🔸 Run Django

cd django_app
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001

---

🔸 Run FastAPI

uvicorn fastapi_app.main:app --reload --port 8000

---

🧪 API Endpoints

🔑 Social Login

Method| Endpoint| Description
POST| /auth/google| Google login
POST| /auth/facebook| Facebook login
POST| /auth/github| GitHub login

---

📱 OTP Authentication

Method| Endpoint| Description
POST| /auth/otp/send| Send OTP
POST| /auth/otp/verify| Verify OTP

---

🔒 Protected Route

GET /protected
Authorization: Bearer <token>

---

📬 Postman Collection

Include:

- Google Login
- Facebook Login
- GitHub Login
- OTP Send
- OTP Verify
- Protected API

---

🎯 Expected Outcome

- Users can log in using Google, Facebook, GitHub ✅
- OTP login/signup works ✅
- JWT authentication secured ✅
- Admin can monitor logs in Django panel ✅

---

