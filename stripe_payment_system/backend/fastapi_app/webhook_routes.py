from fastapi import APIRouter, Request, HTTPException
import json
from datetime import datetime
from database import SessionLocal
from models import Transaction, UserAccess

router = APIRouter()

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    
    print(f"\n📨 Webhook received at {datetime.now()}")
    
    try:
        # Get the raw body
        body = await request.body()
        
        # Check if body is empty
        if not body:
            print("❌ Empty request body")
            return {"status": "error", "message": "Empty request body"}
        
        # Try to parse JSON
        try:
            event = json.loads(body)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            print(f"Raw body: {body[:100]}...")
            return {"status": "error", "message": f"Invalid JSON: {str(e)}"}
        
        print(f"Event type: {event.get('type', 'unknown')}")
        
        # Handle checkout session completed
        if event.get("type") == "checkout.session.completed":
            session = event.get("data", {}).get("object", {})
            session_id = session.get("id")
            
            if session_id:
                print(f"✅ Processing checkout.session.completed for: {session_id}")
                
                # Update database
                db = SessionLocal()
                try:
                    # Find the transaction
                    transaction = db.query(Transaction).filter(
                        Transaction.stripe_session_id == session_id
                    ).first()
                    
                    if transaction:
                        # Update status
                        transaction.status = "completed"
                        db.commit()
                        print(f"✅ Transaction {session_id} updated to COMPLETED")
                        
                        # Grant user access
                        if transaction.item_type == "course":
                            from models import UserAccess
                            access = UserAccess(
                                user_id=transaction.user_id,
                                course_id=transaction.item_id,
                                access_type="course",
                                is_active=True
                            )
                            db.add(access)
                            db.commit()
                            print(f"✅ Course access granted to user {transaction.user_id}")
                            
                        elif transaction.item_type == "plan":
                            from models import UserAccess
                            access = UserAccess(
                                user_id=transaction.user_id,
                                plan_id=transaction.item_id,
                                access_type="plan",
                                is_active=True
                            )
                            db.add(access)
                            db.commit()
                            print(f"✅ Plan access granted to user {transaction.user_id}")
                    else:
                        print(f"⚠️ Transaction not found for session: {session_id}")
                        
                except Exception as e:
                    print(f"❌ Database error: {e}")
                    db.rollback()
                finally:
                    db.close()
            else:
                print("⚠️ No session ID in webhook")
        
        elif event.get("type") == "payment_intent.succeeded":
            print("✅ Payment intent succeeded")
        
        else:
            print(f"ℹ️ Unhandled event type: {event.get('type')}")
        
        return {"status": "success", "message": "Webhook processed"}
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return {"status": "error", "message": str(e)}