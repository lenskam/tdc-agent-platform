# Phase 7.2: Human-in-the-Loop

*Part of MVP Launch Plan - See docs/dev/artifacts/MVP_LAUNCH_PLAN.md*

## Overview
Implement approval workflow for high-risk agent actions.

## Tasks

### 2.1 Approval System

- [ ] Add `requires_approval` field to tools
- [ ] Create approval request when high-risk tool called
- [ ] Track approval status (pending, approved, rejected)
- [ ] Record approval decisions with user info

### 2.2 Approval API Routes (`src/api/routes/approvals.py`)

- [ ] GET /api/v1/approvals - List pending approvals
- [ ] POST /api/v1/approvals/{id}/approve
- [ ] POST /api/v1/approvals/{id}/reject
- [ ] GET /api/v1/approvals/{id} - Get approval details

### 2.3 Approval Dashboard (`dashboard/components/ApprovalQueue.tsx`)

- [ ] List pending approvals
- [ ] Show task details
- [ ] Approve/Reject buttons
- [ ] Decision history

### 2.4 Agent Updates

- [ ] Flag high-risk tools in tool definitions
- [ ] Check approval status before tool execution
- [ ] Handle approval denial gracefully
- [ ] Resume execution after approval

## Tool Risk Levels

| Tool | Risk Level |
|------|------------|
| read_budget_sheet | LOW |
| check_donor_guidelines | LOW |
| search_proposals | LOW |
| generate_proposal | MEDIUM |
| deploy_service | HIGH |
| execute_code | HIGH |
| write_file | HIGH |

## Success Criteria
- [ ] High-risk actions pause for approval
- [ ] Approvers can approve/reject via dashboard
- [ ] Task execution resumes after approval
