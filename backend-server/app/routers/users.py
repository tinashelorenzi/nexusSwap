from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..schemas import user_schemas
from ..core import security

router = APIRouter()

@router.post("/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=user_schemas.User)
def read_users_me(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return current_user

@router.get("/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=user_schemas.User)
def update_user(
    user_id: int,
    user: user_schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    if current_user.id != user_id and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user 