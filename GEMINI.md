# GEMINI.md

## TDC Consulting – Multi-Agent AI Platform

For full technical definitons and details, see the @docs/dev/TECH_DEFS.md file.

For full Master Task file, see the @docs/dev/MASTER_TASK.md file.

---

# 1. Project Overview

This repository contains the **TDC Multi-Agent Platform**, an AI-powered operational system designed for **TDC Consulting**, a technology and consulting firm specializing in:

- AI and automation
- Data systems
- Digital transformation
- Information systems consulting
- Monitoring & evaluation systems
- Software engineering and infrastructure

The platform enables **AI agents to assist or autonomously perform consulting tasks** while remaining under **human supervision and approval controls**.

The system is designed for:

- Internal operations
- Client consulting projects
- Future SaaS productization

TDC is a **high-leverage micro-firm** with:

- **2 core humans**
- **multiple AI agents acting as digital workers**

Human roles focus on:

- strategy
- architecture
- decision making
- client relationships

AI agents focus on:

- execution
- analysis
- documentation
- automation

---

# 2. System Vision

The goal is to build a **Digital Consulting Workforce Platform**.

Instead of a large consulting team, TDC operates with:

```
Human Core
    ↓
Agent Orchestrator
    ↓
Specialized AI Agents
    ↓
Tools / APIs / Databases
```

AI agents behave like **junior consultants or technical staff**, while humans act as:

- supervisors
- reviewers
- decision authorities

Human approval is required for **high-risk operations**.

---

# 3. Core Architecture

The system follows a **multi-layer architecture**.

### AI Brain Layer

LLM providers:

- Gemini
- GPT
- Claude
- open-source models

LLMs are accessed through an **LLM Router**.

Example file:

```
src/core/llm_router.py
```

---

### Agent Layer

Each AI worker is implemented as an **Agent Class**.

Example:

```
src/agents/base_agent.py
src/agents/pm_agent.py
src/agents/proposal_agent.py
src/agents/data_agent.py
```

Each agent contains:

- role definition
- tools
- decision policies
- autonomy level

---

### Orchestration Layer

The **Agent Orchestrator** coordinates tasks.

Responsibilities:

- assign tasks
- track agent states
- enforce approval gates
- manage retries
- log actions

Agents **do not communicate directly**.

All communication flows through the orchestrator.

---

### Tool Layer

Agents interact with tools such as:

- database operations
- APIs
- file system
- analytics tools
- development tools

Example tools:

```
src/tools/task_manager.py
src/tools/reporting_tool.py
src/tools/time_estimator.py
src/tools/risk_analyzer.py
```

---

### Data Layer

Primary database:

```
PostgreSQL
```

Vector storage:

```
Chroma / Weaviate
```

Used for:

- knowledge retrieval
- agent memory
- RAG pipelines

---

### API Layer

Backend API:

```
FastAPI
```

Provides:

- agent execution endpoints
- project operations
- dashboard data
- approval workflows

---

### Frontend Layer

Dashboard built using:

```
Next.js
```

Used for:

- agent monitoring
- human approvals
- system configuration
- analytics

---

# 4. Core Agent Types

The platform supports multiple **specialized agents aligned with consulting functions**.

---

## Project Manager Agent

Responsibilities:

- create project plans
- assign tasks
- track progress
- produce reports

Tools:

- task manager
- reporting engine
- risk analyzer
- time estimator

Uses database tables:

- projects
- tasks
- agent_runs

---

## Proposal Agent

Supports business development.

Capabilities:

- analyze Terms of Reference
- search past proposals
- match staff CVs
- generate proposal drafts

Tools:

- proposal templates
- knowledge base
- document retrieval

---

## Data Analyst / M&E Agent

Performs analytics for consulting projects.

Capabilities:

- data cleaning
- indicator calculations
- anomaly detection
- report narratives

Tools:

- Python analytics
- DHIS2 APIs
- CSV / Excel processing

Autonomy:

semi-autonomous.

---

## Developer Agent

Supports engineering work.

Capabilities:

- code generation
- refactoring
- API scaffolding
- test generation
- code review

Autonomy:

assistive only.

---

## DevOps Agent

Responsible for infrastructure.

Capabilities:

- monitor servers
- analyze logs
- generate deployment scripts
- detect anomalies

Autonomy:

semi-autonomous in staging.

Production changes require approval.

---

## Training Agent

Creates educational materials.

Capabilities:

- generate training manuals
- convert system specs to simple explanations
- create quizzes
- answer user questions

Used for:

- client capacity building
- system documentation

---

## Finance Agent

Supports administrative functions.

Capabilities:

- budget drafts
- expense monitoring
- financial reports
- compliance checks

Autonomy:

assistive only due to financial risk.

---

# 5. Agent Communication Protocol

Agents communicate using **structured task messages**, not free text.

Example message:

```
{
  "task_id": "uuid",
  "from_agent": "ProjectManagerAgent",
  "to_agent": "DataAnalystAgent",
  "task_type": "DATA_ANALYSIS",
  "context": {
      "project_id": "uuid",
      "dataset_id": "uuid"
  },
  "priority": "high"
}
```

Agents operate in defined states:

- IDLE
- PLANNING
- EXECUTING
- WAITING
- COMPLETED
- FAILED

State is recorded in:

```
agent_runs.status
```

---

# 6. Database Architecture

Core database tables include:

### Clients

Stores client organizations.

Fields include:

- name
- sector
- contact details

---

### Projects

Tracks consulting engagements.

Fields include:

- client_id
- project name
- description
- status

---

### Tasks

Operational work items.

Fields include:

- assigned_agent
- assigned_user
- priority
- due_date

---

### Agents

Defines each AI worker.

Fields include:

- name
- role
- autonomy level
- active status

---

### Agent Runs

Records each execution.

Fields include:

- agent_id
- input prompt
- output summary
- execution status

---

### Agent Actions

Logs tool usage.

Includes:

- action type
- parameters
- result

Provides **full auditability**.

---

### Knowledge System

Two key tables:

```
documents
knowledge_chunks
```

Used for:

- RAG retrieval
- vector search
- consulting knowledge base

---

### Agent Memory

Stores long-term learning for agents.

---

# 7. Human-in-the-Loop Approval System

High-risk actions require human review.

Approval records stored in:

```
approvals table
```

Fields include:

- agent_run_id
- action summary
- risk level
- status
- reviewer notes

---

Approval flow:

```
Agent → Request Approval → Human Decision → Continue / Abort
```

Possible actions:

- approve
- modify
- reject

---

# 8. Failure Handling & Recovery

Agents can fail due to:

- tool errors
- missing data
- API failures
- LLM hallucinations

Recovery mechanisms include:

Retry logic.

Fallback agents.

Example:

```
Data Agent fails
→ Backup statistical agent executes
```

Rollback capability:

If a process partially completes:

- revert database changes
- restore previous state

Failure records stored in:

```
agent_failures
```

---

# 9. Monitoring & Observability

A real-time dashboard tracks system health.

Key panels include:

### Agent Status Board

Displays:

- current task
- execution state
- confidence score

---

### Task Flow Visualizer

Shows pipeline DAG:

```
PM → Data → Dev → Reporting
```

---

### Failure Panel

Displays errors and retries.

---

### Performance Metrics

Tracks:

- success rate
- average task duration
- approval rate

---

Monitoring stack:

- Prometheus
- Grafana
- Loki / ELK
- PostgreSQL logs

---

# 10. Security Architecture

Security rules apply to both humans and agents.

Key controls include:

Authentication.

Role-based access control.

Agent permission policies.

Example table:

```
agent_permissions
```

Defines:

- allowed tools
- operational restrictions

Agents cannot execute tools outside their permissions.

---

Protection mechanisms:

- prompt injection filters
- tool sandboxing
- secret management
- audit logging

---

# 11. Master Implementation Tasks

Development tasks are tracked in:

```
MASTER_TASK.md
```

The roadmap includes phases:

1. Core Framework & PM Agent
2. Proposal Agent
3. Data & M&E Agent
4. Engineering / DevOps Agents
5. Training Agent
6. Security & Governance

Each phase introduces:

- new agents
- new tools
- expanded automation

---

# 12. Development Principles

When contributing to this repository:

Follow these rules.

### Rule 1 — Agents must be deterministic when possible.

Use structured outputs.

Avoid ambiguous LLM responses.

---

### Rule 2 — All agent actions must be logged.

Use:

```
agent_runs
agent_actions
```

---

### Rule 3 — High-risk operations require approval.

Never bypass approval gates.

---

### Rule 4 — Tools must be modular.

Each tool should be implemented as an independent module.

---

### Rule 5 — Agents must remain replaceable.

Agent logic should be modular so models can be swapped.

---

# 13. Long-Term Vision

This system will evolve into:

A **Consulting AI Operating System**.

Capabilities will expand to include:

- automated consulting pipelines
- SaaS products
- industry-specific agent bundles
- knowledge-driven consulting automation

The ultimate objective:

```
Human experts
+
AI workforce
=
Hyper-scalable consulting firm
```

---
