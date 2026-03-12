from fastapi import FastAPI
from .routes import agents
from .routes import proposal_routes
from .routes import training_routes
from .routes import finance_routes
from .routes import director_routes
from .routes import auth
from .routes import tasks
from .routes import approvals
from .routes import monitoring
from .routes import audit
from ..database.postgres import engine, Base
from ..core.logging import setup_logging
import os

# Setup logging
setup_logging(
    level=os.getenv("LOG_LEVEL", "INFO"),
    json_format=os.getenv("LOG_JSON", "false").lower() == "true"
)

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
app.include_router(finance_routes.router, prefix="/api/v1/agents/finance", tags=["finance"])
app.include_router(director_routes.router, prefix="/api/v1/agents/director", tags=["director"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(approvals.router, prefix="/api/v1/approvals", tags=["approvals"])
app.include_router(monitoring.router, prefix="/api/v1", tags=["monitoring"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["audit"])

@app.get("/")
def read_root():
    return {"message": "TDC Agent Platform is running"}
