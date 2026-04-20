import stripe
import httpx
from config import Config, ProductConfig
from database import SessionLocal
from models import Transaction, UserAccess
from datetime import datetime, timedelta
from typing import Dict, Any

stripe.api_key = Config.STRIPE_SECRET_KEY

class PaymentService:
    
    @staticmethod
    async def create_checkout_session(
        user_id: int,
        user_email: str,
        item_type: str,
        item_id: int,
        success_url: str,
        cancel_url: str
    ) -> Dict[str, Any]:
        """Create Stripe checkout session"""
        
        try:
            # Get product details
            if item_type == "course":
                product = ProductConfig.COURSES.get(item_id)
            elif item_type == "plan":
                product = ProductConfig.PLANS.get(item_id)
            else:
                return {"success": False, "error": "Invalid item type"}
            
            if not product:
                return {"success": False, "error": "Product not found"}
            
            # Create Stripe session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": product["currency"],
                        "product_data": {
                            "name": product["name"],
                        },
                        "unit_amount": int(product["price"] * 100),
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=user_email,
                metadata={
                    "user_id": str(user_id),
                    "item_type": item_type,
                    "item_id": str(item_id),
                    "product_name": product["name"],
                    "amount": str(product["price"])
                }
            )
            
            # Save transaction to database
            db = SessionLocal()
            transaction = Transaction(
                stripe_session_id=checkout_session.id,
                user_id=user_id,
                user_email=user_email,
                amount=product["price"],
                currency=product["currency"],
                status="pending",
                item_type=item_type,
                item_id=item_id,
                item_name=product["name"]
            )
            db.add(transaction)
            db.commit()
            db.close()
            
            return {
                "success": True,
                "session_id": checkout_session.id,
                "session_url": checkout_session.url
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}