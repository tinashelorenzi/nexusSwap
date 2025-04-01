from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WalletBase(BaseModel):
    currency: str
    wallet_address: str

class WalletCreate(WalletBase):
    pass

class Wallet(WalletBase):
    id: int
    user_id: int
    balance: float
    is_escrow: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: float
    transaction_type: str
    reference_id: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    wallet_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class WalletBalance(BaseModel):
    currency: str
    balance: float
    wallet_address: str 