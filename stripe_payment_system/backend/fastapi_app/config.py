import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Stripe Configuration
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./payments.db")
    
    # URLs
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    DJANGO_ADMIN_URL = os.getenv("DJANGO_ADMIN_URL", "http://localhost:8002")

class ProductConfig:
    COURSES = {
        1: {"id": 1, "name": "Python Masterclass", "price": 99.99, "currency": "usd", "type": "course"},
        2: {"id": 2, "name": "Web Development Bootcamp", "price": 149.99, "currency": "usd", "type": "course"},
        3: {"id": 3, "name": "Data Science Fundamentals", "price": 199.99, "currency": "usd", "type": "course"},
    }
    
    PLANS = {
        1: {"id": 1, "name": "Monthly Premium", "price": 29.99, "currency": "usd", "type": "plan", "duration": 30},
        2: {"id": 2, "name": "Yearly Premium", "price": 299.99, "currency": "usd", "type": "plan", "duration": 365},
    }