"""
NexusSwap API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from .database import engine, Base, SessionLocal
from .routers import users, offers, trades, wallets
from .database.init_db import init_db
from .admin.config import ADMIN_VIEWS
import os
from dotenv import load_dotenv

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NexusSwap API",
    description="API for NexusSwap - A P2P Cryptocurrency Exchange Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(offers.router, prefix="/api/offers", tags=["offers"])
app.include_router(trades.router, prefix="/api/trades", tags=["trades"])
app.include_router(wallets.router, prefix="/api/wallets", tags=["wallets"])

# Configure admin panel
admin = Admin(app, engine)
for view in ADMIN_VIEWS:
    admin.add_view(view)

@app.on_event("startup")
async def startup_event():
    """Initialize the application."""
    # Initialize database with admin user
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to NexusSwap API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "admin_url": "/admin"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 