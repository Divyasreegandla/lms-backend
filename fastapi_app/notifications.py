from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi_app.database import get_db
from fastapi_app.models import Notification
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class MarkReadRequest(BaseModel):
    notification_id: int

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    link: Optional[str] = None
    is_read: bool
    created_at: str

def create_notification(db: Session, user_id: int, message: str, link: str = None):
    """Helper function to create notifications"""
    try:
        notification = Notification(
            user_id=user_id,
            message=message,
            link=link,
            is_read=False,
            created_at=datetime.now()
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        print(f"✅ Notification created for user {user_id}: {message}")
        return notification
    except Exception as e:
        print(f"❌ Error creating notification: {e}")
        db.rollback()
        return None

@router.get("/notifications/{user_id}")
async def get_notifications(user_id: int, db: Session = Depends(get_db)):
    """Get all notifications for a user"""
    try:
        notifications = db.query(Notification).filter(
            Notification.user_id == user_id
        ).order_by(desc(Notification.created_at)).all()
        
        return [
            {
                "id": n.id,
                "user_id": n.user_id,
                "message": n.message,
                "link": n.link,
                "is_read": n.is_read,
                "created_at": n.created_at.isoformat() if n.created_at else datetime.now().isoformat()
            }
            for n in notifications
        ]
    except Exception as e:
        print(f"❌ Error fetching notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notifications/mark-read")
async def mark_notification_read(request: MarkReadRequest, db: Session = Depends(get_db)):
    """Mark a notification as read"""
    try:
        notification = db.query(Notification).filter(
            Notification.id == request.notification_id
        ).first()
        
        if not notification:
            raise HTTPException(status_code=404, detail=f"Notification {request.notification_id} not found")
        
        notification.is_read = True
        db.commit()
        
        print(f"✅ Notification {request.notification_id} marked as read")
        return {"message": f"Notification {request.notification_id} marked as read"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error marking notification as read: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notifications/create-test")
async def create_test_notification(db: Session = Depends(get_db)):
    """Create a test notification (for testing)"""
    try:
        notif = create_notification(db, 1, "Test notification from server", "/dashboard")
        if notif:
            return {"message": "Test notification created", "id": notif.id}
        return {"error": "Failed to create notification"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))