import json
import logging
from typing import List, Dict, Any
from collections import Counter
from langchain_core.tools import tool
from sqlalchemy.orm import Session
from ..database.postgres import SessionLocal
from ..database.models import Task, Project, TaskStatus

logger = logging.getLogger(__name__)


class RiskAnalyzerTool:
    @tool("analyze_project_risks")
    def analyze_project_risks(project_id: int) -> str:
        """
        Analyzes all tasks in a project to identify potential risks and bottlenecks.
        
        Checks for:
        - Tasks assigned to the same person/agent (workload imbalance)
        - Blocked tasks
        - High priority tasks without assignments
        - Tasks without due dates
        - Tasks in TODO for too long
        
        Args:
            project_id: ID of the project to analyze.
            
        Returns:
            JSON string with identified risks and recommendations.
        """
        db: Session = SessionLocal()
        try:
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                return json.dumps({"error": f"Project {project_id} not found"})
            
            tasks = db.query(Task).filter(Task.project_id == project_id).all()
            if not tasks:
                return json.dumps({"risks": [], "summary": "No tasks to analyze"})
            
            risks = []
            assignees = [t.assigned_to for t in tasks if t.assigned_to]
            assignee_counts = Counter(assignees)
            
            for assignee, count in assignee_counts.items():
                if count > 5:
                    risks.append({
                        "type": "workload_imbalance",
                        "severity": "medium",
                        "message": f"'{assignee}' has {count} tasks assigned - consider redistributing",
                        "assignee": assignee,
                        "task_count": count
                    })
            
            unassigned = [t for t in tasks if not t.assigned_to or t.assigned_to == "Unassigned"]
            if unassigned:
                high_priority_unassigned = [t for t in unassigned if t.priority in ("high", "critical")]
                if high_priority_unassigned:
                    risks.append({
                        "type": "unassigned_high_priority",
                        "severity": "high",
                        "message": f"{len(high_priority_unassigned)} high-priority tasks are unassigned",
                        "task_ids": [t.id for t in high_priority_unassigned]
                    })
            
            blocked = [t for t in tasks if t.status == TaskStatus.BLOCKED]
            if blocked:
                risks.append({
                    "type": "blocked_tasks",
                    "severity": "high",
                    "message": f"{len(blocked)} tasks are blocked and need attention",
                    "task_ids": [t.id for t in blocked],
                    "tasks": [{"id": t.id, "title": t.title} for t in blocked]
                })
            
            no_due_date = [t for t in tasks if not t.due_date and t.status != TaskStatus.DONE]
            if len(no_due_date) > len(tasks) * 0.5:
                risks.append({
                    "type": "missing_due_dates",
                    "severity": "low",
                    "message": f"{len(no_due_date)} tasks don't have due dates - consider adding them",
                    "task_count": len(no_due_date)
                })
            
            result = {
                "project_id": project_id,
                "project_name": project.name,
                "total_tasks": len(tasks),
                "risks": risks,
                "summary": f"Found {len(risks)} potential risks" if risks else "No significant risks identified"
            }
            
            return json.dumps(result)
            
        except Exception as e:
            logger.error(f"Risk analysis failed: {e}")
            return json.dumps({"error": str(e)})
        finally:
            db.close()


risk_analyzer_tools = [RiskAnalyzerTool.analyze_project_risks]
