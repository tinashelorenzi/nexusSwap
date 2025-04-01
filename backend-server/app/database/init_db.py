"""
Database initialization functions
"""

from sqlalchemy.orm import Session
from ..models.models import User, UserRole
from ..core.security import get_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

def init_db(db: Session) -> None:
    """Initialize the database with required data."""
    # Check if admin user exists
    admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
    if not admin:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@nexusswap.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        
        admin = User(
            email=admin_email,
            username="admin",
            hashed_password=get_password_hash(admin_password),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin) 