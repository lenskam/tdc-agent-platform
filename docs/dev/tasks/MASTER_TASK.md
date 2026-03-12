# TDC Multi-Agent System - Master Task List

This document tracks the detailed development roadmap for the TDC Agent Platform.
Implementation Plans:

- [Phase 1: Core & PM Agent], see @docs/dev/PHASE_1_IMP_PLAN.md
- [Phase 2: Proposal Agent], see @docs/dev/PHASE_2_IMP_PLAN.md
- [Phase 3: Data & M&E Agent], see @docs/dev/PHASE_3_IMP_PLAN.md
- [Phase 4: Engineering/DevOps], see @docs/dev/PHASE_4_IMP_PLAN.md
- [Phase 5: Training Agent], see @docs/dev/PHASE_5_IMP_PLAN.md
- [Phase 6: Security & Governance], see @docs/dev/PHASE_6_IMP_PLAN.md
- [Phase 7: MVP Launch], see @docs/dev/artifacts/MVP_LAUNCH_PLAN.md

## 🧠 Phase 1: Core Framework & Project Manager Agent

- [x] **Infrastructure Foundation**
  - [x] Set up FastAPI Backbone (`src/api/main.py`)
  - [x] Configure PostgreSQL with SQLAlchemy (`src/database/`)
  - [x] Implement LLM Router (`src/core/llm_router.py`) - with failover & cost tracking
  - [x] Create Base Agent Class (`src/agents/base_agent.py`)
  - [x] Set up basic Dashboard (Next.js)

- [x] **Project Manager Agent Enhancements**
  - [x] Implement Core Logic (Planning projects) (`src/agents/pm_agent.py`)
  - [x] **Tools**: Task Management (CRUD) (`src/tools/task_manager.py`)
  - [x] **Tools**: Basic Reporting (`src/tools/reporting_tool.py`)
  - [x] **Tools**: Time Estimator (`src/tools/time_estimator.py`)
  - [x] **Tools**: Risk Analyzer (`src/tools/risk_analyzer.py`)
  - [x] **Tools**: PDF Report Generation

- [x] **Testing & Quality**
  - [x] Unit Tests for PM Agent
  - [x] Integration Tests (Agent -> DB)
  - [x] Dashboard E2E Tests (Playwright)

## 📄 Phase 2: Proposal & Business Development

- [x] **Core Infrastructure**
  - [x] RAG Engine (`src/core/rag_engine.py`)
  - [x] PDF Ingestion Pipeline
- [x] **Proposal Agent**
  - [x] Implement `ProposalWriterAgent` class
  - [x] **Tools**: Past Proposal Search
  - [x] **Tools**: CV Matcher
  - [x] **Tools**: Template Filler

- [x] **API Routes**
  - [x] POST /proposal/draft
  - [x] POST /proposal/ingest
  - [x] GET /proposal/search
  - [x] GET /proposal/consultants
  - [x] GET /proposal/documents

## 📊 Phase 3: Data & M&E Department

- [x] **Data Infrastructure**
  - [x] DHIS2 Connector Tool (`src/tools/dhis2_tools.py`)
  - [x] Data Cleaning Utilities (Pandas wrapper)
- [x] **Data Analyst Agent**
  - [x] Implement `DataAnalystAgent` class
  - [x] **Tools**: Anomaly Detector
  - [x] **Tools**: Descriptive Statistics Generator
- [x] **Dashboard Integration**
  - [x] Add Data Analysis Tab/Upload

## 💻 Phase 4: Engineering & Automation

- [x] **Developer Agent**
  - [x] Implement `DeveloperAgent` class
  - [x] **Tools**: Git Operations (Branch, PR)
  - [x] **Tools**: Code Linter/Formatter
  - [x] Sandbox Environment (`src/core/sandbox.py`)
- [x] **DevOps Agent**
  - [x] Implement `DevOpsAgent` class
  - [x] **Tools**: Log Analyzer
  - [x] **Tools**: Docker/System status

## 🎓 Phase 5: Training & Research

- [x] **Training Agent**
  - [x] Implement `TrainingAgent` class
  - [x] **Tools**: Quiz Generator
  - [x] **Tools**: User Manual Simplifier
  - [x] **Tools**: Knowledge Base Search

## 🛡️ Phase 6: Security & Governance

- [x] **Finance Agent**
  - [x] Implement `FinanceAgent` class
  - [x] **Tools**: Budget Reader (Read-Only)
  - [x] **Tools**: Compliance Checker
- [x] **Director Agent**
  - [x] Implement `DirectorAgent` class
  - [x] **Tools**: Cross-Agent Summary
- [x] **Security Hardening**
  - [x] Implement RBAC for Agents (`src/core/security.py`)
  - [x] Audit Logging

---

## 🚀 Phase 7: MVP Launch

*See: docs/dev/artifacts/MVP_LAUNCH_PLAN.md*

### Phase 7.1: Core Infrastructure (Week 1-2)

*See: docs/dev/artifacts/MVP_PHASE_1_CORE_INFRASTRUCTURE.md*

- [ ] **Orchestrator Module** (`src/orchestrator/`)
  - [ ] Task intake API endpoint
  - [ ] Task router (task_type → agent mapping)
  - [ ] State manager (track task status)
  - [ ] Agent execution launcher
  - [ ] Basic failure detection

- [ ] **Database Schema Extension** (`src/database/models.py`)
  - [ ] User model
  - [ ] Agent model
  - [ ] Workflow model
  - [ ] WorkflowExecution model
  - [ ] ApprovalRequest model
  - [ ] ApprovalDecision model
  - [ ] AuditLog model

- [ ] **Authentication System** (`src/auth/`)
  - [ ] User registration endpoint
  - [ ] Login endpoint (returns JWT)
  - [ ] JWT validation middleware
  - [ ] Role-based access control

- [ ] **Task Queue** (`src/queue/`)
  - [ ] Redis connection setup
  - [ ] Task producer (enqueue tasks)
  - [ ] Task consumer (dequeue and process)
  - [ ] Basic retry logic (3 attempts)

- [ ] **Dashboard Updates**
  - [ ] Login page
  - [ ] Protected routes (require auth)
  - [ ] Task creation form

### Phase 7.2: Human-in-the-Loop (Week 3)

*See: docs/dev/artifacts/MVP_PHASE_2_HUMAN_IN_THE_LOOP.md*

- [ ] **Approval System**
  - [ ] Approval request creation
  - [ ] Approval status tracking
  - [ ] Approval decision recording

- [ ] **Approval Dashboard**
  - [ ] Approval queue display
  - [ ] Approve/Reject buttons
  - [ ] Task details view
  - [ ] Decision history

- [ ] **Approval Enforcement**
  - [ ] Block task execution until approved
  - [ ] Notify users of pending approvals

- [ ] **Agent Updates**
  - [ ] Flag high-risk tool calls
  - [ ] Request approval before execution

### Phase 7.3: Observability & Logging (Week 4)

*See: docs/dev/artifacts/MVP_PHASE_3_OBSERVABILITY.md*

- [ ] **Logging Infrastructure**
  - [ ] Structured logging (JSON format)
  - [ ] Log levels (DEBUG, INFO, WARN, ERROR)

- [ ] **Audit Logging**
  - [ ] Log all authentication events
  - [ ] Log all approval decisions
  - [ ] Log task state changes

- [ ] **Health Checks**
  - [ ] `/health` endpoint
  - [ ] Database connectivity check
  - [ ] Redis connectivity check

- [ ] **Dashboard Updates**
  - [ ] Task history view
  - [ ] Basic analytics

### Phase 7.4: Testing & Documentation (Week 5)

*See: docs/dev/artifacts/MVP_PHASE_4_TESTING_DOCS.md*

- [ ] **Testing**
  - [ ] API endpoint tests
  - [ ] Authentication tests
  - [ ] E2E dashboard tests

- [ ] **Documentation**
  - [ ] User Guide
  - [ ] API Documentation
  - [ ] Deployment Guide

- [ ] **Launch Preparation**
  - [ ] Production environment setup
  - [ ] Backup strategy
  - [ ] Basic runbook
