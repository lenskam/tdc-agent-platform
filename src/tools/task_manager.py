from typing import List, Optional
from langchain_core.tools import tool
from sqlalchemy.orm import Session
from ..database.postgres import SessionLocal
from ..database.models import Task, Project, TaskStatus

class TaskManager:
    """
    A set of tools for the Project Manager Agent to interact with the database.
    Each method is decorated with @tool to be usable by LangChain/CrewAI.
    """

    @tool("create_project")
    def create_project(name: str, description: str, client_name: str) -> str:
        """
        Creates a new project in the database.
        Returns the ID of the created project.
        """
        db: Session = SessionLocal()
        try:
            project = Project(
                name=name,
                description=description,
                client_name=client_name
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            return f"Project created successfully. ID: {project.id}"
        except Exception as e:
            db.rollback()
            return f"Error creating project: {str(e)}"
        finally:
            db.close()

    @tool("add_task_to_project")
    def add_task_to_project(project_id: int, title: str, description: str, 
                          assigned_to: str = "Unassigned", priority: str = "medium") -> str:
        """
        Adds a single task to an existing project.
        """
        db: Session = SessionLocal()
        try:
            # check if project exists
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                return f"Error: Project with ID {project_id} not found."

            task = Task(
                title=title,
                description=description,
                project_id=project_id,
                assigned_to=assigned_to,
                priority=priority
            )
            db.add(task)
            db.commit()
            return f"Task '{title}' added to Project {project_id}."
        except Exception as e:
            return f"Error adding task: {str(e)}"
        finally:
            db.close()

    @tool("list_project_tasks")
    def list_project_tasks(project_id: int) -> str:
        """
        Lists all tasks for a specific project.
        """
        db: Session = SessionLocal()
        try:
            tasks = db.query(Task).filter(Task.project_id == project_id).all()
            if not tasks:
                return "No tasks found for this project."
            
            result = "Tasks:\n"
            for t in tasks:
                result += f"- [{t.id}] {t.title} ({t.status.value}) - Assigned: {t.assigned_to}\n"
            return result
        finally:
            db.close()

# Export a list of all tools available from this module
task_manager_tools = [
     TaskManager.create_project,
     TaskManager.add_task_to_project,
     TaskManager.list_project_tasks
]
