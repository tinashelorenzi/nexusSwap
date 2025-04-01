from sqlalchemy import Column, String, Float, ForeignKey, Enum, Boolean, Text, Integer, DateTime
from sqlalchemy.orm import relationship
import enum
from .base import Base
from datetime import datetime

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_blocked = Column(Boolean, default=False)
    
    # Relationships
    wallets = relationship("Wallet", back_populates="user")
    offers = relationship("Offer", back_populates="seller")
    trades_as_buyer = relationship("Trade", back_populates="buyer", foreign_keys="Trade.buyer_id")
    trades_as_seller = relationship("Trade", back_populates="seller", foreign_keys="Trade.seller_id")

class Wallet(BaseModel):
    __tablename__ = "wallets"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    currency = Column(String)  # e.g., "BTC", "ETH"
    balance = Column(Float, default=0.0)
    wallet_address = Column(String, unique=True)
    is_escrow = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet")

class Offer(BaseModel):
    __tablename__ = "offers"
    
    seller_id = Column(Integer, ForeignKey("users.id"))
    currency = Column(String)  # e.g., "BTC", "ETH"
    min_amount = Column(Float)
    max_amount = Column(Float)
    price_per_unit = Column(Float)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    seller = relationship("User", back_populates="offers")
    trades = relationship("Trade", back_populates="offer")

class TradeStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PAID = "paid"
    COMPLETED = "completed"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"

class Trade(BaseModel):
    __tablename__ = "trades"
    
    trade_id = Column(String, unique=True, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    price_per_unit = Column(Float)
    total_price = Column(Float)
    status = Column(Enum(TradeStatus), default=TradeStatus.PENDING)
    moderator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    offer = relationship("Offer", back_populates="trades")
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="trades_as_buyer")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="trades_as_seller")
    moderator = relationship("User", foreign_keys=[moderator_id])
    messages = relationship("TradeMessage", back_populates="trade")

class TradeMessage(BaseModel):
    __tablename__ = "trade_messages"
    
    trade_id = Column(Integer, ForeignKey("trades.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    
    # Relationships
    trade = relationship("Trade", back_populates="messages")
    sender = relationship("User")

class Transaction(BaseModel):
    __tablename__ = "transactions"
    
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    amount = Column(Float)
    transaction_type = Column(String)  # "deposit", "withdrawal", "transfer", "escrow"
    status = Column(String)  # "pending", "completed", "failed"
    reference_id = Column(String, unique=True)
    
    # Relationships
    wallet = relationship("Wallet", back_populates="transactions") 