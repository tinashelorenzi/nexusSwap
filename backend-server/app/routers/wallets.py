from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from ..database import get_db
from ..models import models
from ..schemas import wallet_schemas
from ..core import security

router = APIRouter()

@router.post("/", response_model=wallet_schemas.Wallet)
def create_wallet(
    wallet: wallet_schemas.WalletCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    # Check if user already has a wallet for this currency
    existing_wallet = db.query(models.Wallet).filter(
        models.Wallet.user_id == current_user.id,
        models.Wallet.currency == wallet.currency
    ).first()
    
    if existing_wallet:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet for {wallet.currency} already exists"
        )
    
    db_wallet = models.Wallet(
        **wallet.dict(),
        user_id=current_user.id,
        balance=0.0
    )
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

@router.get("/", response_model=List[wallet_schemas.Wallet])
def get_wallets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    return db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).all()

@router.get("/{wallet_id}", response_model=wallet_schemas.Wallet)
def get_wallet(
    wallet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this wallet")
    
    return wallet

@router.get("/{wallet_id}/balance", response_model=wallet_schemas.WalletBalance)
def get_wallet_balance(
    wallet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this wallet")
    
    return {
        "currency": wallet.currency,
        "balance": wallet.balance,
        "wallet_address": wallet.wallet_address
    }

@router.post("/{wallet_id}/transactions", response_model=wallet_schemas.Transaction)
def create_transaction(
    wallet_id: int,
    transaction: wallet_schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create transactions for this wallet")
    
    # For withdrawals, check if there's enough balance
    if transaction.transaction_type == "withdrawal" and wallet.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    db_transaction = models.Transaction(
        **transaction.dict(),
        wallet_id=wallet_id,
        status="pending"
    )
    db.add(db_transaction)
    
    # Update wallet balance based on transaction type
    if transaction.transaction_type == "deposit":
        wallet.balance += transaction.amount
    elif transaction.transaction_type == "withdrawal":
        wallet.balance -= transaction.amount
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/{wallet_id}/transactions", response_model=List[wallet_schemas.Transaction])
def get_wallet_transactions(
    wallet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view transactions for this wallet")
    
    return wallet.transactions 