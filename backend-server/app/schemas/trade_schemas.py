from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.models import TradeStatus

class TradeBase(BaseModel):
    offer_id: int
    amount: float

class TradeCreate(TradeBase):
    pass

class TradeMessageBase(BaseModel):
    content: str

class TradeMessageCreate(TradeMessageBase):
    pass

class TradeMessage(TradeMessageBase):
    id: int
    trade_id: int
    sender_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Trade(TradeBase):
    id: int
    trade_id: str
    buyer_id: int
    seller_id: int
    price_per_unit: float
    total_price: float
    status: TradeStatus
    moderator_id: Optional[int] = None
    created_at: datetime
    messages: List[TradeMessage] = []

    class Config:
        from_attributes = True

class TradeUpdate(BaseModel):
    status: Optional[TradeStatus] = None
    moderator_id: Optional[int] = None 