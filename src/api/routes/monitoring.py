from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database.postgres import get_db
from ...database.models import Task, User, Agent
from ...core.metrics import MetricsService
import os


router = APIRouter()


@router.get("/health")
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Health check endpoint with database connectivity.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Database check
    try:
        db.execute("SELECT 1")
        health_status["checks"]["database"] = {"status": "healthy", "message": "Connected"}
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {"status": "unhealthy", "message": str(e)}
    
    # Redis check (optional)
    try:
        import redis
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        r = redis.Redis(host=redis_host, port=redis_port, db=0)
        r.ping()
        health_status["checks"]["redis"] = {"status": "healthy", "message": "Connected"}
    except Exception as e:
        health_status["checks"]["redis"] = {"status": "unhealthy", "message": str(e)}
    
    return health_status


@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)) -> Dict[str, str]:
    """
    Readiness check for Kubernetes.
    """
    try:
        db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}


@router.get("/health/live")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check for Kubernetes.
    """
    return {"status": "alive"}


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get application metrics.
    """
    metrics_service = MetricsService(db)
    return metrics_service.get_all_metrics()


@router.get("/metrics/tasks")
async def get_task_metrics(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get task-related metrics.
    """
    metrics_service = MetricsService(db)
    return {
        "counts": metrics_service.get_task_counts(),
        "created_today": metrics_service.get_tasks_created_today(),
        "completed_today": metrics_service.get_tasks_completed_today()
    }


@router.get("/metrics/agents")
async def get_agent_metrics(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get agent-related metrics.
    """
    metrics_service = MetricsService(db)
    return {
        "activity_7d": metrics_service.get_agent_activity(7)
    }
