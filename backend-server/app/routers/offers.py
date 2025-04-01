from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import models
from ..schemas import offer_schemas
from ..core import security

router = APIRouter()

@router.post("/", response_model=offer_schemas.Offer)
def create_offer(
    offer: offer_schemas.OfferCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    db_offer = models.Offer(
        **offer.dict(),
        seller_id=current_user.id
    )
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

@router.get("/", response_model=List[offer_schemas.Offer])
def get_offers(
    currency: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Offer).filter(models.Offer.is_active == True)
    
    if currency:
        query = query.filter(models.Offer.currency == currency)
    if min_price:
        query = query.filter(models.Offer.price_per_unit >= min_price)
    if max_price:
        query = query.filter(models.Offer.price_per_unit <= max_price)
    if min_amount:
        query = query.filter(models.Offer.min_amount >= min_amount)
    if max_amount:
        query = query.filter(models.Offer.max_amount <= max_amount)
    
    return query.all()

@router.get("/{offer_id}", response_model=offer_schemas.Offer)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.put("/{offer_id}", response_model=offer_schemas.Offer)
def update_offer(
    offer_id: int,
    offer_update: offer_schemas.OfferUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    db_offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not db_offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    if db_offer.seller_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    for field, value in offer_update.dict(exclude_unset=True).items():
        setattr(db_offer, field, value)
    
    db.commit()
    db.refresh(db_offer)
    return db_offer

@router.delete("/{offer_id}")
def delete_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    db_offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not db_offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    if db_offer.seller_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_offer)
    db.commit()
    return {"message": "Offer deleted successfully"} 