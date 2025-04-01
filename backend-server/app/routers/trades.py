from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from ..database import get_db
from ..models import models
from ..schemas import trade_schemas
from ..core import security

router = APIRouter()

@router.post("/", response_model=trade_schemas.Trade)
def create_trade(
    trade: trade_schemas.TradeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    # Get the offer
    offer = db.query(models.Offer).filter(models.Offer.id == trade.offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    if not offer.is_active:
        raise HTTPException(status_code=400, detail="Offer is not active")
    
    # Validate amount
    if trade.amount < offer.min_amount or trade.amount > offer.max_amount:
        raise HTTPException(
            status_code=400,
            detail=f"Amount must be between {offer.min_amount} and {offer.max_amount}"
        )
    
    # Create trade
    db_trade = models.Trade(
        trade_id=str(uuid.uuid4()),
        offer_id=trade.offer_id,
        buyer_id=current_user.id,
        seller_id=offer.seller_id,
        amount=trade.amount,
        price_per_unit=offer.price_per_unit,
        total_price=trade.amount * offer.price_per_unit,
        status=models.TradeStatus.PENDING
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

@router.get("/", response_model=List[trade_schemas.Trade])
def get_trades(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    return db.query(models.Trade).filter(
        (models.Trade.buyer_id == current_user.id) |
        (models.Trade.seller_id == current_user.id)
    ).all()

@router.get("/{trade_id}", response_model=trade_schemas.Trade)
def get_trade(
    trade_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    trade = db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    if trade.buyer_id != current_user.id and trade.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this trade")
    
    return trade

@router.put("/{trade_id}", response_model=trade_schemas.Trade)
def update_trade(
    trade_id: str,
    trade_update: trade_schemas.TradeUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    trade = db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    # Only buyer, seller, or admin can update trade
    if (trade.buyer_id != current_user.id and 
        trade.seller_id != current_user.id and 
        current_user.role != models.UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Not authorized to update this trade")
    
    for field, value in trade_update.dict(exclude_unset=True).items():
        setattr(trade, field, value)
    
    db.commit()
    db.refresh(trade)
    return trade

@router.post("/{trade_id}/messages", response_model=trade_schemas.TradeMessage)
def create_trade_message(
    trade_id: str,
    message: trade_schemas.TradeMessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    trade = db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    if trade.buyer_id != current_user.id and trade.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to send messages in this trade")
    
    db_message = models.TradeMessage(
        trade_id=trade.id,
        sender_id=current_user.id,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/{trade_id}/messages", response_model=List[trade_schemas.TradeMessage])
def get_trade_messages(
    trade_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    trade = db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    if trade.buyer_id != current_user.id and trade.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view messages in this trade")
    
    return trade.messages 