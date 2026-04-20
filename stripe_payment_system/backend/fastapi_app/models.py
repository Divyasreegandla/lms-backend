from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    stripe_session_id = Column(String, unique=True, index=True, nullable=False)
    transaction_id = Column(String, unique=True, nullable=True)
    user_id = Column(Integer, nullable=False)
    user_email = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="usd")
    status = Column(String, default="pending")
    item_type = Column(String, nullable=False)
    item_id = Column(Integer, nullable=False)
    item_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserAccess(Base):
    __tablename__ = "user_access"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    course_id = Column(Integer, nullable=True)
    plan_id = Column(Integer, nullable=True)
    access_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    granted_at = Column(DateTime(timezone=True), server_default=func.now())