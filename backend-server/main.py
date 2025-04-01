from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {"message": "Welcome to NexusSwap API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 