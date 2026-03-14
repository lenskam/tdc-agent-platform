from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database.models import Task, AgentLog


class MetricsService:
    """Service for tracking application metrics."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_task_counts(self) -> Dict[str, int]:
        """Get count of tasks by status."""
        results = self.db.query(
            Task.status,
            func.count(Task.id)
        ).group_by(Task.status).all()
        
        return {
            "total": sum(count for _, count in results),
            "todo": sum(count for status, count in results if status == "todo"),
            "in_progress": sum(count for status, count in results if status == "in_progress"),
            "review": sum(count for status, count in results if status == "review"),
            "done": sum(count for status, count in results if status == "done"),
            "blocked": sum(count for status, count in results if status == "blocked"),
        }
    
    def get_tasks_created_today(self) -> int:
        """Get number of tasks created today."""
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        
        return self.db.query(func.count(Task.id)).filter(
            Task.created_at >= today,
            Task.created_at < tomorrow
        ).scalar() or 0
    
    def get_tasks_completed_today(self) -> int:
        """Get number of tasks completed today."""
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        
        return self.db.query(func.count(Task.id)).filter(
            Task.status == "done",
            Task.updated_at >= today,
            Task.updated_at < tomorrow
        ).scalar() or 0
    
    def get_agent_activity(self, days: int = 7) -> Dict[str, int]:
        """Get agent activity counts for the past N days."""
        since = datetime.utcnow() - timedelta(days=days)
        
        results = self.db.query(
            AgentLog.agent_name,
            func.count(AgentLog.id)
        ).filter(
            AgentLog.timestamp >= since
        ).group_by(AgentLog.agent_name).all()
        
        return {agent_name: count for agent_name, count in results}
    
    def get_average_execution_time(self) -> Optional[float]:
        """Get average task execution time in seconds (from agent logs)."""
        # This is a placeholder - would need to track execution times properly
        return None
    
    def get_all_metrics(self) -> Dict:
        """Get all metrics."""
        return {
            "tasks": self.get_task_counts(),
            "tasks_created_today": self.get_tasks_created_today(),
            "tasks_completed_today": self.get_tasks_completed_today(),
            "agent_activity_7d": self.get_agent_activity(7),
            "generated_at": datetime.utcnow().isoformat()
        }
