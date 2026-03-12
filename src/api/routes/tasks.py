from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...database.postgres import get_db
from ...database.models import Task, Project
from ...orchestrator.execution_engine import execution_engine
from ...orchestrator.state_manager import TaskState


router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    task_type: str
    project_id: Optional[int] = None
    assigned_to: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    assigned_to: Optional[str]
    project_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


def get_current_user_id() -> int:
    return 1


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Create a new task.
    """
    if task_data.project_id:
        project = db.query(Project).filter(Project.id == task_data.project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
    
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        assigned_to=task_data.assigned_to,
        project_id=task_data.project_id,
        status="todo"
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    execution_engine.execute_task_sync(
        task_id=f"task_{task.id}",
        task_type=task_data.task_type,
        task_input={
            "title": task.title,
            "description": task.description,
            "task_id": task.id
        },
        user_id=str(current_user_id)
    )
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority,
        assigned_to=task.assigned_to,
        project_id=task.project_id,
        created_at=task.created_at
    )


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[str] = None,
    project_id: Optional[int] = None,
    assigned_to: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    List tasks with optional filters.
    """
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    
    return [
        TaskResponse(
            id=t.id,
            title=t.title,
            description=t.description,
            status=t.status.value,
            priority=t.priority,
            assigned_to=t.assigned_to,
            project_id=t.project_id,
            created_at=t.created_at
        )
        for t in tasks
    ]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Get a specific task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority,
        assigned_to=task.assigned_to,
        project_id=task.project_id,
        created_at=task.created_at
    )


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Update a task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.assigned_to is not None:
        task.assigned_to = task_data.assigned_to
    
    db.commit()
    db.refresh(task)
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority,
        assigned_to=task.assigned_to,
        project_id=task.project_id,
        created_at=task.created_at
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Delete a task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    db.delete(task)
    db.commit()
    
    return None


@router.get("/{task_id}/status")
async def get_task_status(
    task_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Get the execution status of a task.
    """
    status = execution_engine.get_task_status(f"task_{task_id}")
    
    if not status:
        return {"task_id": task_id, "state": "unknown", "message": "Task not found in execution engine"}
    
    return status
