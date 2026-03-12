from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...database.postgres import get_db
from ...database.models import AuditLog
from ...core.audit import AuditLogger


router = APIRouter()


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    resource_type: str
    resource_id: Optional[str]
    details: Optional[dict]
    ip_address: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


def get_current_user_id() -> int:
    return 1


@router.get("/", response_model=List[AuditLogResponse])
async def list_audit_logs(
    resource_type: Optional[str] = None,
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    List audit logs with optional filters.
    """
    query = db.query(AuditLog)
    
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    if action:
        query = query.filter(AuditLog.action == action)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    return [
        AuditLogResponse(
            id=log.id,
            user_id=log.user_id,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            details=log.details,
            ip_address=log.ip_address,
            timestamp=log.timestamp
        )
        for log in logs
    ]


@router.get("/auth", response_model=List[AuditLogResponse])
async def list_auth_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    List authentication-related audit logs.
    """
    logs = db.query(AuditLog).filter(
        AuditLog.resource_type == "auth"
    ).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    return [
        AuditLogResponse(
            id=log.id,
            user_id=log.user_id,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            details=log.details,
            ip_address=log.ip_address,
            timestamp=log.timestamp
        )
        for log in logs
    ]


@router.get("/tasks", response_model=List[AuditLogResponse])
async def list_task_logs(
    task_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    List task-related audit logs.
    """
    query = db.query(AuditLog).filter(AuditLog.resource_type == "task")
    
    if task_id:
        query = query.filter(AuditLog.resource_id == str(task_id))
    
    logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    return [
        AuditLogResponse(
            id=log.id,
            user_id=log.user_id,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            details=log.details,
            ip_address=log.ip_address,
            timestamp=log.timestamp
        )
        for log in logs
    ]
