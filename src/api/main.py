from fastapi import FastAPI
from .routes import agents
from .routes import proposal_routes
from .routes import training_routes
from ..database.postgres import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TDC Agent Platform",
    description="API for TDC Consulting's Multi-Agent System",
    version="0.1.0"
)

app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(proposal_routes.router, prefix="/api/v1/proposal", tags=["proposal"])
app.include_router(training_routes.router, prefix="/api/v1/agents/training", tags=["training"])

@app.get("/")
def read_root():
    return {"message": "TDC Agent Platform is running"}
