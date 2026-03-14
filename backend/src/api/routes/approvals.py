from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...database.postgres import get_db
from ...database.models import ApprovalRequest, ApprovalDecision, Task
from ...orchestrator.state_manager import TaskState


router = APIRouter()


class ApprovalRequestCreate(BaseModel):
    task_id: int
    title: str
    description: Optional[str] = None
    priority: str = "normal"


class ApprovalRequestResponse(BaseModel):
    id: int
    task_id: int
    requester_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True


class ApprovalDecisionCreate(BaseModel):
    decision: str  # approved, rejected
    comments: Optional[str] = None


class ApprovalDecisionResponse(BaseModel):
    id: int
    approval_request_id: int
    approver_id: int
    decision: str
    comments: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ApprovalWithDecisions(BaseModel):
    id: int
    task_id: int
    requester_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: datetime
    decisions: List[ApprovalDecisionResponse] = []

    class Config:
        from_attributes = True


def get_current_user_id() -> int:
    return 1


@router.post("/", response_model=ApprovalRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_approval_request(
    request_data: ApprovalRequestCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Create a new approval request for a task.
    """
    task = db.query(Task).filter(Task.id == request_data.task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    approval_request = ApprovalRequest(
        task_id=request_data.task_id,
        requester_id=current_user_id,
        title=request_data.title,
        description=request_data.description,
        priority=request_data.priority,
        status="pending"
    )
    
    db.add(approval_request)
    db.commit()
    db.refresh(approval_request)
    
    return ApprovalRequestResponse(
        id=approval_request.id,
        task_id=approval_request.task_id,
        requester_id=approval_request.requester_id,
        title=approval_request.title,
        description=approval_request.description,
        status=approval_request.status,
        priority=approval_request.priority,
        created_at=approval_request.created_at
    )


@router.get("/", response_model=List[ApprovalRequestResponse])
async def list_approval_requests(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    List approval requests, optionally filtered by status.
    """
    query = db.query(ApprovalRequest)
    
    if status:
        query = query.filter(ApprovalRequest.status == status)
    
    requests = query.order_by(ApprovalRequest.created_at.desc()).all()
    
    return [
        ApprovalRequestResponse(
            id=r.id,
            task_id=r.task_id,
            requester_id=r.requester_id,
            title=r.title,
            description=r.description,
            status=r.status,
            priority=r.priority,
            created_at=r.created_at
        )
        for r in requests
    ]


@router.get("/pending", response_model=List[ApprovalRequestResponse])
async def list_pending_approvals(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    List all pending approval requests.
    """
    requests = db.query(ApprovalRequest).filter(
        ApprovalRequest.status == "pending"
    ).order_by(ApprovalRequest.created_at.desc()).all()
    
    return [
        ApprovalRequestResponse(
            id=r.id,
            task_id=r.task_id,
            requester_id=r.requester_id,
            title=r.title,
            description=r.description,
            status=r.status,
            priority=r.priority,
            created_at=r.created_at
        )
        for r in requests
    ]


@router.get("/{request_id}", response_model=ApprovalWithDecisions)
async def get_approval_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Get a specific approval request with its decisions.
    """
    approval_request = db.query(ApprovalRequest).filter(
        ApprovalRequest.id == request_id
    ).first()
    
    if not approval_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found"
        )
    
    decisions = db.query(ApprovalDecision).filter(
        ApprovalDecision.approval_request_id == request_id
    ).all()
    
    return ApprovalWithDecisions(
        id=approval_request.id,
        task_id=approval_request.task_id,
        requester_id=approval_request.requester_id,
        title=approval_request.title,
        description=approval_request.description,
        status=approval_request.status,
        priority=approval_request.priority,
        created_at=approval_request.created_at,
        decisions=[
            ApprovalDecisionResponse(
                id=d.id,
                approval_request_id=d.approval_request_id,
                approver_id=d.approver_id,
                decision=d.decision,
                comments=d.comments,
                created_at=d.created_at
            )
            for d in decisions
        ]
    )


@router.post("/{request_id}/decide", response_model=ApprovalDecisionResponse)
async def make_approval_decision(
    request_id: int,
    decision_data: ApprovalDecisionCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Approve or reject an approval request.
    """
    approval_request = db.query(ApprovalRequest).filter(
        ApprovalRequest.id == request_id
    ).first()
    
    if not approval_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found"
        )
    
    if approval_request.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Approval request already {approval_request.status}"
        )
    
    if decision_data.decision not in ["approved", "rejected"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Decision must be 'approved' or 'rejected'"
        )
    
    decision = ApprovalDecision(
        approval_request_id=request_id,
        approver_id=current_user_id,
        decision=decision_data.decision,
        comments=decision_data.comments
    )
    
    approval_request.status = decision_data.decision
    
    db.add(decision)
    db.commit()
    db.refresh(decision)
    
    return ApprovalDecisionResponse(
        id=decision.id,
        approval_request_id=decision.approval_request_id,
        approver_id=decision.approver_id,
        decision=decision.decision,
        comments=decision.comments,
        created_at=decision.created_at
    )


@router.post("/{request_id}/approve", response_model=ApprovalDecisionResponse)
async def approve_request(
    request_id: int,
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Quick endpoint to approve a request.
    """
    return await make_approval_decision(
        request_id,
        ApprovalDecisionCreate(decision="approved", comments=comments),
        db,
        current_user_id
    )


@router.post("/{request_id}/reject", response_model=ApprovalDecisionResponse)
async def reject_request(
    request_id: int,
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Quick endpoint to reject a request.
    """
    return await make_approval_decision(
        request_id,
        ApprovalDecisionCreate(decision="rejected", comments=comments),
        db,
        current_user_id
    )
