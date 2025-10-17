from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    subscription_tier = Column(String, default="free")  # free, starter, growth, enterprise
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    usage_logs = relationship("UsageLog", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_name = Column(String)  # starter, growth, enterprise
    status = Column(String, default="active")  # active, cancelled, expired
    amount = Column(Float)
    currency = Column(String)
    billing_cycle = Column(String)  # monthly, annual
    payment_gateway = Column(String)  # razorpay, stripe
    gateway_subscription_id = Column(String, nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    auto_renew = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")


class UsageLog(Base):
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tool_name = Column(String)  # business_plan, pitch_deck, content_generator, etc.
    action = Column(String)  # generate, export, save
    credits_used = Column(Integer, default=1)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(Text, nullable=True)  # JSON string with additional data
    
    # Relationships
    user = relationship("User", back_populates="usage_logs")


class GeneratedContent(Base):
    __tablename__ = "generated_content"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tool_name = Column(String)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
