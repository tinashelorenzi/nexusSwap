from pydantic import BaseModel
from typing import Optional

class OfferBase(BaseModel):
    currency: str
    min_amount: float
    max_amount: float
    price_per_unit: float

class OfferCreate(OfferBase):
    pass

class OfferUpdate(BaseModel):
    currency: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    price_per_unit: Optional[float] = None
    is_active: Optional[bool] = None

class Offer(OfferBase):
    id: int
    seller_id: int
    is_active: bool

    class Config:
        from_attributes = True 