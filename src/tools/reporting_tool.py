from langchain_core.tools import tool
from typing import Optional
from ..database.postgres import SessionLocal
from ..database.models import Project, Task

class ReportingTool:
    @tool("generate_project_report")
    def generate_project_report(project_id: int) -> str:
        """
        Generates a text summary of the project status.
        """
        db = SessionLocal()
        try:
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                return "Project not found."
            
            tasks = db.query(Task).filter(Task.project_id == project_id).all()
            total = len(tasks)
            done = len([t for t in tasks if t.status.value == 'done'])
            
            report = f"""
# Project Status Report: {project.name}
**Client**: {project.client_name}
**Progress**: {done}/{total} Tasks Completed

## Tasks Detail
"""
            for t in tasks:
                 report += f"- {t.title}: {t.status.value}\n"
                 
            return report
        except Exception as e:
            return f"Error generating report: {e}"
        finally:
            db.close()

reporting_tools = [ReportingTool.generate_project_report]
