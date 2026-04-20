from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from payment_routes import router as payment_router
from webhook_routes import router as webhook_router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from payment_routes import router as payment_router


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LMS Stripe Payment Integration", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(payment_router)
app.include_router(webhook_router)


# Make sure you have this in main.py
app.include_router(payment_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "payment-gateway"}


templates = Jinja2Templates(directory="templates")

@app.get("/api-docs", response_class=HTMLResponse)
async def api_docs(request: Request):
    """API Documentation Page"""
    return templates.TemplateResponse("api_docs.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)