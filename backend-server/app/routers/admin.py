from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..core import security

router = APIRouter()

@router.get("/users", response_model=List[dict])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = db.query(models.User).all()
    return users

@router.post("/users/{user_id}/block")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_blocked = True
    db.commit()
    return {"message": "User blocked successfully"}

@router.post("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_blocked = False
    db.commit()
    return {"message": "User unblocked successfully"} 