# 💳 Stripe Payment Integration for LMS

A complete payment gateway integration for Learning Management System (LMS) to handle course purchases and premium plan upgrades securely using Stripe.

## 📋 Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Postman Collection](#postman-collection)
- [Troubleshooting](#troubleshooting)
- [Demo Video Guide](#demo-video-guide)
- [Submission Checklist](#submission-checklist)

## ✨ Features

### Frontend (FastAPI)
- ✅ Interactive checkout page for courses and plans
- ✅ Beautiful dashboard displaying all products side by side
- ✅ Stripe payment button integration
- ✅ Success and cancel payment pages
- ✅ Responsive design for all devices

### Backend (FastAPI)
- ✅ Create checkout session endpoint
- ✅ Webhook handling for Stripe events
- ✅ Payment status checking endpoint
- ✅ Automatic user access grant after successful payment
- ✅ Transaction recording in database
- ✅ Sync with Django admin panel

### Admin Panel (Django)
- ✅ Complete payment transaction management
- ✅ View Transaction ID, User, Amount, Status, Timestamp
- ✅ Filter and search payments
- ✅ Admin interface for monitoring all transactions

## 🛠 Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Backend API | FastAPI | 0.104.1 |
| Admin Panel | Django | 4.2.7 |
| Payment Gateway | Stripe | 7.5.0 |
| Database | SQLite | 3.x |
| Frontend | HTML/CSS/JS | - |
| Webhook Forwarding | Stripe CLI | 1.40.6 |

## 📁 Project Structure
stripe_payment_system/
├── backend/
│ ├── fastapi_app/
│ │ ├── init.py
│ │ ├── main.py # FastAPI application entry point
│ │ ├── config.py # Configuration settings
│ │ ├── database.py # Database connection
│ │ ├── models.py # Database models
│ │ ├── payment_routes.py # Payment API endpoints
│ │ ├── payment_service.py # Payment business logic
│ │ └── webhook_routes.py # Stripe webhook handler
│ └── requirements.txt # Python dependencies
├── frontend/
│ ├── templates/
│ │ ├── dashboard.html # Products dashboard page
│ │ ├── checkout.html # Payment checkout page
│ │ ├── success.html # Payment success page
│ │ ├── cancel.html # Payment cancel page
│ │ └── api_docs.html # API documentation page
│ └── static/
│ └── style.css # Custom styles
├── django_admin/
│ ├── manage.py # Django management script
│ ├── payment_admin/ # Django payment app
│ │ ├── init.py
│ │ ├── admin.py # Admin configuration
│ │ ├── apps.py # App configuration
│ │ ├── models.py # Django models
│ │ ├── urls.py # URL configuration
│ │ ├── views.py # API views
│ │ └── migrations/
│ │ └── init.py
│ └── payment_admin_project/
│ ├── init.py
│ ├── settings.py # Django settings
│ ├── urls.py # Main URLs
│ └── wsgi.py # WSGI configuration
├── .env # Environment variables
├── run_servers.py # One-click server starter
├── start_all.bat # Windows batch script
└── README.md # Documentation

Step 2: Create Virtual Environment
bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
Step 3: Install Dependencies
bash
# Install FastAPI dependencies
pip install fastapi uvicorn stripe sqlalchemy python-dotenv jinja2 python-multipart httpx

# Install Django dependencies
pip install django django-cors-headers djangorestframework
Step 4: Create Requirements File
bash
# Create requirements.txt
pip freeze > backend/requirements.txt
⚙️ Configuration
Step 1: Get Stripe API Keys
Go to Stripe Dashboard

Sign up for a free account (no credit card required)

Navigate to Developers → API Keys

Copy your Publishable Key (starts with pk_test_)

Copy your Secret Key (starts with sk_test_)

Step 2: Set Up Webhook
Option A: Using Stripe CLI (Recommended for Local Development)

bash
# Download Stripe CLI from:
# https://github.com/stripe/stripe-cli/releases

# Login to Stripe
stripe login

# Start webhook forwarding
stripe listen --forward-to localhost:8000/webhook/stripe

# Copy the webhook signing secret (whsec_...)
Option B: Using Stripe Dashboard

Go to Developers → Webhooks

Click "Add endpoint"

URL: https://your-domain.com/webhook/stripe

Select events: checkout.session.completed

Copy the Signing secret

Step 3: Create .env File
Create .env file in the root directory:

env
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_PUBLISHABLE_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET_HERE

# Server URLs
BACKEND_URL=http://localhost:8000
DJANGO_ADMIN_URL=http://localhost:8002

# Database
DATABASE_URL=sqlite:///./payments.db
Step 4: Setup Django Database
bash
cd django_admin

# Create migrations
python manage.py makemigrations payment_admin

# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123

cd ..
🏃 Running the Application
Method 1: One-Click Start (Recommended)
Windows:

bash
# Double-click start_all.bat
# OR run in terminal
start_all.bat
Mac/Linux:

bash
python run_servers.py
Method 2: Manual Start (Three Terminals)
Terminal 1 - Stripe CLI:

bash
cd stripe_payment_system
stripe listen --forward-to localhost:8000/webhook/stripe
Terminal 2 - FastAPI Backend:

bash
cd stripe_payment_system/backend/fastapi_app
python -m uvicorn main:app --reload --port 8000
Terminal 3 - Django Admin:

bash
cd stripe_payment_system/django_admin
python manage.py runserver 8002
Access the Application
Service	URL	Description
Checkout Page	http://localhost:8000/checkout/course/1	Buy a course
Dashboard	http://localhost:8000/dashboard	View all products
API Docs	http://localhost:8000/api-docs	API documentation
Django Admin	http://localhost:8002/admin	Admin panel
Health Check	http://localhost:8000/health	Server status
🔗 API Endpoints
FastAPI Endpoints (Port 8000)
Method	Endpoint	Description
GET	/health	Health check
GET	/api/products	List all courses and plans
POST	/api/create-checkout-session	Create Stripe checkout session
GET	/api/payment-status/{session_id}	Check payment status
POST	/webhook/stripe	Stripe webhook handler
GET	/dashboard	User dashboard
GET	/checkout/{type}/{id}	Checkout page
GET	/api-docs	API documentation
Django Endpoints (Port 8002)
Method	Endpoint	Description
GET	/admin	Admin panel
GET	/api/transactions/	List all transactions
POST	/api/sync-transaction/	Sync transaction
🧪 Testing
Test Cards (Stripe Test Mode)
Card Number	Description	Result
4242 4242 4242 4242	Standard success	✅ Payment succeeds
4000 0025 0000 3155	3D Secure	🔐 Requires authentication
4000 0000 0000 0002	Declined	❌ Payment fails
Note: Use any future expiry date (12/30) and any 3-digit CVC (123)

Testing Payment Flow
Open checkout page:

text
http://localhost:8000/checkout/course/1
Click "Pay with Stripe"

Enter test card details:

Card: 4242 4242 4242 4242

Expiry: 12/30

CVC: 123

Complete payment

Verify success:

Success page appears

Transaction in Django admin

User access granted


----------------------------------------------------------------------

 Postman Collection
Import Collection
Open Postman

Click Import → Raw text

Paste the following JSON:

json
{
  "info": {
    "name": "Stripe Payment API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/health"
      }
    },
    {
      "name": "Get Products",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/api/products"
      }
    },
    {
      "name": "Create Checkout Session",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/x-www-form-urlencoded"}],
        "body": {
          "mode": "urlencoded",
          "urlencoded": [
            {"key": "item_type", "value": "course"},
            {"key": "item_id", "value": "1"},
            {"key": "user_id", "value": "1"},
            {"key": "user_email", "value": "test@example.com"}
          ]
        },
        "url": "http://localhost:8000/api/create-checkout-session"
      }
    },
    {
      "name": "Get Transactions",
      "request": {
        "method": "GET",
        "url": "http://localhost:8002/api/transactions/"
      }
    }
  ]
}
