from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from ..database.models import AuditLog
from ..core.logging import get_logger


logger = get_logger(__name__)


class AuditLogger:
    """Service for creating audit log entries."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log(
        self,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """
        Create an audit log entry.
        
        Args:
            action: The action performed (e.g., "login", "create_task", "approve")
            resource_type: Type of resource (e.g., "task", "project", "user")
            resource_id: ID of the resource
            user_id: ID of the user performing the action
            details: Additional details about the action
            ip_address: IP address of the client
            
        Returns:
            Created AuditLog entry
        """
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            timestamp=datetime.utcnow()
        )
        
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        
        logger.info(
            f"Audit: {action} on {resource_type}:{resource_id} by user:{user_id}"
        )
        
        return audit_log
    
    def log_auth_event(
        self,
        event: str,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        success: bool = True,
        ip_address: Optional[str] = None
    ):
        """Log an authentication event."""
        return self.log(
            action=event,
            resource_type="auth",
            user_id=user_id,
            details={"email": email, "success": success},
            ip_address=ip_address
        )
    
    def log_task_action(
        self,
        action: str,
        task_id: int,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log a task-related action."""
        return self.log(
            action=action,
            resource_type="task",
            resource_id=str(task_id),
            user_id=user_id,
            details=details
        )
    
    def log_approval_action(
        self,
        action: str,
        approval_id: int,
        user_id: Optional[int] = None,
        decision: Optional[str] = None,
        comments: Optional[str] = None
    ):
        """Log an approval-related action."""
        return self.log(
            action=action,
            resource_type="approval",
            resource_id=str(approval_id),
            user_id=user_id,
            details={"decision": decision, "comments": comments}
        )
    
    def get_logs(
        self,
        resource_type: Optional[str] = None,
        action: Optional[str] = None,
        user_id: Optional[int] = None,
        limit: int = 100
    ):
        """Query audit logs with filters."""
        query = self.db.query(AuditLog)
        
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        if action:
            query = query.filter(AuditLog.action == action)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
