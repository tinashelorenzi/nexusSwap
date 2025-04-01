from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, get_db
from .models import models
from .routers import users, offers, trades, wallets, admin

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NexusSwap API",
    description="Backend API for NexusSwap cryptocurrency exchange marketplace",
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
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.on_event("startup")
async def startup_event():
    # Initialize database with admin user
    db = next(get_db())
    from .database.init_db import init_db
    init_db(db)

@app.get("/")
async def root():
    return {"message": "Welcome to NexusSwap API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 