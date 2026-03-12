# Phase 7.1: Core Infrastructure

*Part of MVP Launch Plan - See docs/dev/artifacts/MVP_LAUNCH_PLAN.md*

## Overview
Build the foundation: orchestrator, database schema, authentication, and task queue.

## Tasks

### 1.1 Orchestrator Module (`src/orchestrator/`)

- [ ] Create `src/orchestrator/__init__.py`
- [ ] Create `src/orchestrator/task_router.py`
  - Task routing logic (task_type → agent mapping)
  - Agent selection based on capability
- [ ] Create `src/orchestrator/state_manager.py`
  - Task state CRUD operations
  - State transitions (pending → running → completed/failed)
- [ ] Create `src/orchestrator/execution_engine.py`
  - Agent execution launcher
  - Tool invocation handler
  - Result aggregation

### 1.2 Database Schema Extension (`src/database/models.py`)

- [ ] Add User model
  ```python
  class User(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key=True)
      email = Column(String, unique=True, index=True)
      password_hash = Column(String)
      role = Column(String)  # admin, operator, viewer
      created_at = Column(DateTime, server_default=func.now())
  ```
- [ ] Add Agent model
  ```python
  class Agent(Base):
      __tablename__ = "agents"
      id = Column(Integer, primary_key=True)
      name = Column(String, unique=True)
      agent_type = Column(String)  # pm, proposal, data, etc.
      status = Column(String)  # active, idle, offline
      capabilities = Column(JSON)
      created_at = Column(DateTime, server_default=func.now())
  ```
- [ ] Add Workflow model
- [ ] Add WorkflowExecution model
- [ ] Add ApprovalRequest model
- [ ] Add ApprovalDecision model
- [ ] Add AuditLog model

### 1.3 Authentication System (`src/auth/`)

- [ ] Create `src/auth/__init__.py`
- [ ] Create `src/auth/jwt_handler.py`
  - JWT token generation
  - JWT token validation
  - Token refresh
- [ ] Create `src/auth/dependencies.py`
  - FastAPI dependency for auth
  - Current user extraction
  - Role verification

### 1.4 Task Queue (`src/queue/`)

- [ ] Create `src/queue/__init__.py`
- [ ] Create `src/queue/redis_client.py`
  - Redis connection setup
  - Task enqueue/dequeue
- [ ] Create `src/queue/worker.py`
  - Background worker
  - Retry logic (3 attempts)
  - Exponential backoff

### 1.5 Dashboard Updates

- [ ] Create `dashboard/components/Login.tsx`
  - Login form
  - JWT storage
- [ ] Update `dashboard/app/page.tsx`
  - Protected routes
  - Auth state management

## Dependencies
- python-jose (JWT)
- passlib (password hashing)
- redis
- asyncpg

## Success Criteria
- [ ] Users can register and login
- [ ] Tasks are created and routed to agents
- [ ] Task state is tracked in database
- [ ] Background workers process tasks
