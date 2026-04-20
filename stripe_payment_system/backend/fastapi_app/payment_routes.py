from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

from payment_service import PaymentService
from config import ProductConfig
from database import SessionLocal
from models import Transaction

router = APIRouter()

# Setup templates
templates_path = os.path.join(os.path.dirname(__file__), "../../frontend/templates")
templates = Jinja2Templates(directory=templates_path)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - redirects to dashboard"""
    return RedirectResponse(url="/dashboard", status_code=302)

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Display all courses and plans side by side"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "courses": ProductConfig.COURSES,
        "plans": ProductConfig.PLANS,
        "stripe_publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    })

@router.get("/checkout/{item_type}/{item_id}", response_class=HTMLResponse)
async def checkout_page(
    request: Request,
    item_type: str,
    item_id: int,
    user_id: int = 1,
    user_email: str = "student@example.com"
):
    """Display checkout page"""
    
    if item_type == "course":
        product = ProductConfig.COURSES.get(item_id)
    elif item_type == "plan":
        product = ProductConfig.PLANS.get(item_id)
    else:
        return HTMLResponse(content="Invalid item type", status_code=400)
    
    if not product:
        return HTMLResponse(content="Product not found", status_code=404)
    
    return templates.TemplateResponse("checkout.html", {
        "request": request,
        "product": product,
        "item_type": item_type,
        "item_id": item_id,
        "user_id": user_id,
        "user_email": user_email,
        "stripe_publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    })

@router.post("/api/create-checkout-session")
async def create_checkout_session_api(
    item_type: str = Form(...),
    item_id: int = Form(...),
    user_id: int = Form(...),
    user_email: str = Form(...)
):
    """Create checkout session API endpoint"""
    
    success_url = "http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = "http://localhost:8000/cancel"
    
    result = await PaymentService.create_checkout_session(
        user_id=user_id,
        user_email=user_email,
        item_type=item_type,
        item_id=item_id,
        success_url=success_url,
        cancel_url=cancel_url
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/success", response_class=HTMLResponse)
async def success_page(request: Request, session_id: str):
    """Payment success page"""
    return templates.TemplateResponse("success.html", {
        "request": request,
        "session_id": session_id
    })

@router.get("/cancel", response_class=HTMLResponse)
async def cancel_page(request: Request):
    """Payment cancel page"""
    return templates.TemplateResponse("cancel.html", {"request": request})

@router.get("/api/payment-status/{session_id}")
async def get_payment_status(session_id: str):
    """Get payment status"""
    db = SessionLocal()
    try:
        transaction = db.query(Transaction).filter(
            Transaction.stripe_session_id == session_id
        ).first()
        if transaction:
            return {
                "success": True,
                "status": transaction.status,
                "amount": transaction.amount,
                "user_email": transaction.user_email
            }
        return {"success": False, "error": "Transaction not found"}
    finally:
        db.close()

@router.get("/api/products")
async def list_products():
    """List all available products"""
    return {
        "courses": ProductConfig.COURSES,
        "plans": ProductConfig.PLANS
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "payment-gateway"}

@router.get("/api-docs", response_class=HTMLResponse)
async def api_documentation(request: Request):
    """Display API documentation page"""
    return templates.TemplateResponse("api_docs.html", {
        "request": request,
        "fastapi_url": "http://localhost:8000",
        "django_url": "http://localhost:8002"
    })
