from fastapi import FastAPI
from .routes import agents
from ..database.postgres import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TDC Agent Platform",
    description="API for TDC Consulting's Multi-Agent System",
    version="0.1.0"
)

app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])

@app.get("/")
def read_root():
    return {"message": "TDC Agent Platform is running"}
