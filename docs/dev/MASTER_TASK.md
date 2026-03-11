# TDC Multi-Agent System - Master Task List

This document tracks the detailed development roadmap for the TDC Agent Platform.
Implementation Plans:
- [Phase 1: Core & PM Agent](file:///home/deployer/.gemini/antigravity/brain/0a0518ac-9b77-4981-8aa1-99bde57074af/PHASE_1_IMP_PLAN.md)
- [Phase 2: Proposal Agent](file:///home/deployer/.gemini/antigravity/brain/0a0518ac-9b77-4981-8aa1-99bde57074af/PHASE_2_IMP_PLAN.md)
- [Phase 3: Data & M&E Agent](file:///home/deployer/.gemini/antigravity/brain/0a0518ac-9b77-4981-8aa1-99bde57074af/PHASE_3_IMP_PLAN.md)
- [Phase 4: Engineering/DevOps](file:///home/deployer/.gemini/antigravity/brain/0a0518ac-9b77-4981-8aa1-99bde57074af/PHASE_4_IMP_PLAN.md)
- [Phase 5: Training Agent](file:///home/deployer/.gemini/antigravity/brain/0a0518ac-9b77-4981-8aa1-99bde57074af/PHASE_5_IMP_PLAN.md)
- [Phase 6: Security & Governance](file:///home/deployer/.gemini/antigravity/brain/0a0518ac-9b77-4981-8aa1-99bde57074af/PHASE_6_IMP_PLAN.md)

## 🧠 Phase 1: Core Framework & Project Manager Agent
- [x] **Infrastructure Foundation**
    - [x] Set up FastAPI Backbone (`src/api/main.py`)
    - [x] Configure PostgreSQL with SQLAlchemy (`src/database/`)
    - [x] Implement LLM Router (`src/core/llm_router.py`)
    - [x] Create Base Agent Class (`src/agents/base_agent.py`)
    - [x] Set up basic Dashboard (Next.js)

- [ ] **Project Manager Agent Enhancements**
    - [x] Implement Core Logic (Planning projects) (`src/agents/pm_agent.py`)
    - [x] **Tools**: Task Management (CRUD) (`src/tools/task_manager.py`)
    - [x] **Tools**: Basic Reporting (`src/tools/reporting_tool.py`)
    - [ ] **Tools**: Time Estimator (`src/tools/time_estimator.py`)
    - [ ] **Tools**: Risk Analyzer (`src/tools/risk_analyzer.py`)
    - [ ] **Tools**: PDF Report Generation

- [ ] **Testing & Quality**
    - [ ] Unit Tests for PM Agent
    - [ ] Integration Tests (Agent -> DB)
    - [ ] Dashboard E2E Tests (Playwright)

## 📄 Phase 2: Proposal & Business Development
- [ ] **Core Infrastructure**
    - [ ] RAG Engine (`src/core/rag_engine.py`)
    - [ ] PDF Ingestion Pipeline
- [ ] **Proposal Agent**
    - [ ] Implement `ProposalWriterAgent` class
    - [ ] **Tools**: Past Proposal Search
    - [ ] **Tools**: CV Matcher
    - [ ] **Tools**: Template Filler

## 📊 Phase 3: Data & M&E Department
- [ ] **Data Infrastructure**
    - [ ] DHIS2 Connector Tool (`src/tools/dhis2_tools.py`)
    - [ ] Data Cleaning Utilities (Pandas wrapper)
- [ ] **Data Analyst Agent**
    - [ ] Implement `DataAnalystAgent` class
    - [ ] **Tools**: Anomaly Detector
    - [ ] **Tools**: Descriptive Statistics Generator
- [ ] **Dashboard Integration**
    - [ ] Add Data Analysis Tab/Upload

## 💻 Phase 4: Engineering & Automation
- [ ] **Developer Agent**
    - [ ] Implement `DeveloperAgent` class
    - [ ] **Tools**: Git Operations (Branch, PR)
    - [ ] **Tools**: Code Linter/Formatter
    - [ ] Sandbox Environment (`src/core/sandbox.py`)
- [ ] **DevOps Agent**
    - [ ] Implement `DevOpsAgent` class
    - [ ] **Tools**: Log Analyzer
    - [ ] **Tools**: Docker/System status

## 🎓 Phase 5: Training & Research
- [ ] **Training Agent**
    - [ ] Implement `TrainingAgent` class
    - [ ] **Tools**: Quiz Generator
    - [ ] **Tools**: User Manual Simplifier
    - [ ] **Tools**: Knowledge Base Search

## 🛡️ Phase 6: Security & Governance
- [ ] **Finance Agent**
    - [ ] Implement `FinanceAgent` class
    - [ ] **Tools**: Budget Reader (Read-Only)
    - [ ] **Tools**: Compliance Checker
- [ ] **Director Agent**
    - [ ] Implement `DirectorAgent` class
    - [ ] **Tools**: Cross-Agent Summary
- [ ] **Security Hardening**
    - [ ] Implement RBAC for Agents (`src/core/security.py`)
    - [ ] Audit Logging