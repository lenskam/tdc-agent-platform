# MVP Launch Plan - Updated

## Overview

This document defines the comprehensive MVP Launch Plan based on the gap analysis. It addresses all critical gaps and ensures the platform can function as described in the technical specifications.

---

## MVP Scope Definition

### What the MVP Must Do

1. **Authenticate Users** - Login/logout, role-based access
2. **Route Tasks** - Assign user requests to appropriate agents
3. **Execute Tasks** - Run agents with available tools
4. **Require Approval** - Pause high-risk actions for human review
5. **Return Results** - Display agent outputs to users
6. **Track History** - Store task logs for auditing

### What the MVP Does NOT Include (Post-Launch)

- Multi-agent workflows (future enhancement)
- Advanced monitoring (basic only)
- SSH/external server tools
- Email integration

---

## Comprehensive MVP Launch Plan

### PHASE 1: Core Infrastructure (Week 1-2)

**Goal**: Build the foundation - orchestrator, database, auth, task queue

#### 1.1 Orchestrator Module (`src/orchestrator/`)
- [ ] Task intake API endpoint
- [ ] Task router (task_type → agent mapping)
- [ ] State manager (track task status)
- [ ] Agent execution launcher
- [ ] Basic failure detection

#### 1.2 Database Schema Extension (`src/database/models.py`)
- [ ] User model (id, email, password_hash, role)
- [ ] Agent model (id, name, type, status, capabilities)
- [ ] Workflow model (id, name, steps)
- [ ] WorkflowExecution model
- [ ] ApprovalRequest model
- [ ] ApprovalDecision model
- [ ] AuditLog model

#### 1.3 Authentication System (`src/auth/`)
- [ ] User registration endpoint
- [ ] Login endpoint (returns JWT)
- [ ] JWT validation middleware
- [ ] Role-based access control

#### 1.4 Task Queue (`src/queue/`)
- [ ] Redis connection setup
- [ ] Task producer (enqueue tasks)
- [ ] Task consumer (dequeue and process)
- [ ] Basic retry logic (3 attempts)

#### 1.5 Dashboard Updates
- [ ] Login page
- [ ] Protected routes (require auth)
- [ ] Task creation form

---

### PHASE 2: Human-in-the-Loop (Week 3)

**Goal**: Implement approval workflow for high-risk actions

#### 2.1 Approval System
- [ ] Approval request creation (when agent requests approval)
- [ ] Approval status tracking
- [ ] Approval decision recording

#### 2.2 Approval Dashboard
- [ ] Approval queue display
- [ ] Approve/Reject buttons
- [ ] Task details view
- [ ] Decision history

#### 2.3 Approval Enforcement
- [ ] Block task execution until approved
- [ ] Notify users of pending approvals
- [ ] Auto-reject after timeout (optional)

#### 2.4 Agent Updates
- [ ] Flag high-risk tool calls
- [ ] Request approval before execution
- [ ] Handle approval denial

---

### PHASE 3: Observability & Logging (Week 4)

**Goal**: Enable monitoring, logging, and audit trails

#### 3.1 Logging Infrastructure
- [ ] Structured logging (JSON format)
- [ ] Log levels (DEBUG, INFO, WARN, ERROR)
- [ ] Log to file and stdout
- [ ] Request/response logging

#### 3.2 Audit Logging
- [ ] Log all authentication events
- [ ] Log all approval decisions
- [ ] Log sensitive tool executions
- [ ] Log task state changes

#### 3.3 Health Checks
- [ ] `/health` endpoint
- [ ] Database connectivity check
- [ ] Redis connectivity check
- [ ] Agent status check

#### 3.4 Basic Metrics
- [ ] Tasks created count
- [ ] Tasks completed count
- [ ] Tasks failed count
- [ ] Average execution time

#### 3.5 Dashboard Updates
- [ ] Task history view
- [ ] Basic analytics (charts)
- [ ] Audit log viewer (admin)

---

### PHASE 4: Testing & Documentation (Week 5)

**Goal**: Ensure quality and document the system

#### 4.1 Testing
- [ ] API endpoint tests
- [ ] Authentication tests
- [ ] Approval workflow tests
- [ ] E2E dashboard tests

#### 4.2 Documentation
- [ ] User Guide (login, create task, approve)
- [ ] API Documentation (OpenAPI/Swagger)
- [ ] Deployment Guide (Docker, environment)
- [ ] Architecture Overview

#### 4.3 Launch Preparation
- [ ] Production environment setup
- [ ] Backup strategy
- [ ] Runbook for common issues

---

## Task Breakdown by Component

### Components to Create/Modify

| Component | Files to Create | Files to Modify |
|-----------|-----------------|----------------|
| Orchestrator | `src/orchestrator/__init__.py` | - |
| | `src/orchestrator/task_router.py` | - |
| | `src/orchestrator/state_manager.py` | - |
| | `src/orchestrator/execution_engine.py` | - |
| Database | - | `src/database/models.py` |
| | - | `src/database/migrations/` |
| Auth | `src/auth/__init__.py` | - |
| | `src/auth/jwt_handler.py` | - |
| | `src/auth/dependencies.py` | - |
| Queue | `src/queue/__init__.py` | - |
| | `src/queue/redis_client.py` | - |
| | `src/queue/worker.py` | - |
| API | - | `src/api/main.py` |
| | `src/api/routes/auth.py` | - |
| | `src/api/routes/tasks.py` | - |
| | `src/api/routes/approvals.py` | - |
| Dashboard | - | `dashboard/app/page.tsx` |
| | `dashboard/components/Login.tsx` | - |
| | `dashboard/components/ApprovalQueue.tsx` | - |
| | `dashboard/components/TaskHistory.tsx` | - |

---

## User Journey Implementation

### How Users Will Use the MVP

```
┌─────────┐     ┌──────────┐     ┌────────────┐     ┌──────────┐
│  Login  │────▶│ Dashboard │────▶│ Create Task│────▶│  Route   │
└─────────┘     └──────────┘     └────────────┘     └──────────┘
                                                           │
       ┌──────────────────────────────────────────────────┘
       ▼
┌────────────┐     ┌──────────┐     ┌──────────┐
│  Execute   │────▶│ Approval? │────▶│  Return   │
│   Agent    │     │           │     │  Result   │
└────────────┘     └──────────┘     └──────────┘
                      │ yes
                      ▼
               ┌──────────┐
               │  Human  │
               │  Review │
               └──────────┘
```

### Step-by-Step Flow

1. **User visits dashboard** → Redirected to login if not authenticated
2. **User logs in** → JWT token stored, dashboard loads
3. **User submits task** → Task created in DB with status "pending"
4. **Orchestrator picks up task** → Routes to appropriate agent
5. **Agent executes** → Uses tools, generates output
6. **If high-risk tool called** → Status changes to "waiting_approval"
7. **Human reviews** → Approves or rejects
8. **Task completes** → Status "completed", result returned to user

---

## Dashboard Features Checklist

### Must-Have for Launch

- [ ] Login/Logout
- [ ] Create new task form
- [ ] View task list (my tasks)
- [ ] View task details
- [ ] Approval queue (for approvers)
- [ ] Task history/logs
- [ ] Agent status overview

### Nice-to-Have (Can Add Later)

- [ ] Real-time task updates (WebSocket)
- [ ] Detailed analytics charts
- [ ] Agent configuration UI
- [ ] System settings page

---

## Success Criteria for MVP Launch

### Functional Requirements

- [ ] Users can register and login
- [ ] Authenticated users can create tasks
- [ ] Tasks are routed to correct agents
- [ ] Agents execute and return results
- [ ] High-risk actions require approval
- [ ] Approvers can approve/reject tasks
- [ ] Task history is viewable

### Non-Functional Requirements

- [ ] API responds < 2s for most requests
- [ ] System handles 10 concurrent users
- [ ] Failed tasks retry up to 3 times
- [ ] All actions logged for audit

### Security Requirements

- [ ] Passwords hashed
- [ ] JWT tokens expire
- [ ] Role-based access enforced
- [ ] Sensitive data not logged

---

## Timeline Summary

| Week | Focus | Deliverables |
|------|-------|---------------|
| 1 | Orchestrator + DB | Task routing, state management, extended schema |
| 2 | Auth + Queue | JWT auth, Redis queue, worker |
| 3 | Approvals | Approval workflow, dashboard UI |
| 4 | Observability | Logging, health checks, metrics |
| 5 | Testing + Docs | Tests, user guide, deployment |

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Redis connection fails | Tasks can't queue | Fall back to sync execution |
| Auth integration complex | Delays launch | Use simple JWT, enhance later |
| Agent tool errors | Tasks fail | Implement retry logic |
| Dashboard scope creep | Miss deadline | Focus on must-have features |

---

*Updated: 2026-03-12*
