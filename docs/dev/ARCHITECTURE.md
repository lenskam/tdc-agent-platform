# ARCHITECTURE.md

_TDC AI Agent Platform System Architecture_

Version: 1.0
Status: Core Technical Specification

---

## 1. Purpose of this Document

This document defines the **technical architecture of the TDC AI Agent Platform**, including:

- core system services
- data flow
- execution architecture
- agent orchestration model
- database interactions
- security boundaries
- infrastructure layout
- deployment model
- scaling strategy

The purpose is to ensure that:

- all developers and AI agents follow the same architecture
- the system remains modular and scalable
- components remain loosely coupled
- AI agents can safely interact with system resources

This architecture enables the platform to:

- run **AI agents for consulting workflows**
- automate **data systems and business processes**
- manage **task execution and approvals**
- provide **observability and control**

The system is designed to support **enterprise automation and consulting services developed by TDC Consulting Sarl**.

---

## 2. Architectural Philosophy

The platform follows five core principles.

### 2.1 Modular Monolith First

Initial deployment uses a **single backend service** with modular internal components.

Benefits:

- faster development
- easier debugging
- lower infrastructure cost
- simpler deployment

Later, modules can be extracted into **microservices**.

---

### 2.2 Agent-Oriented Architecture

The platform is built around **AI agents performing specialized tasks**.

Examples:

- Data Integration Agent
- Metadata Sync Agent
- Automation Agent
- Research Agent
- Reporting Agent

Agents execute **tasks defined in `AGENT_TASK_LIBRARY.md`**.

---

### 2.3 Orchestrated Task Execution

Agents do not operate independently.

All execution is coordinated through the **Orchestrator**, which:

- assigns tasks
- manages dependencies
- handles approvals
- tracks results

Defined in:

```
ORCHESTRATOR_SPEC.md
```

---

### 2.4 Tool-Based Intelligence

Agents do not rely purely on LLM reasoning.

They use **structured tools**, including:

- APIs
- data connectors
- automation workflows
- system commands

Defined in:

```
TOOL_REGISTRY.md
```

---

### 2.5 Human Oversight

Critical operations require **human validation**.

This is implemented through:

- the **Permission Model**
- the **Approval System**

Defined in:

```
PERMISSION_MODEL.md
```

---

## 3. Core System Services (6 Core Services)

The entire platform is structured around **six core services**, inspired by modern AI agent infrastructures.

| Service               | Role                              |
| --------------------- | --------------------------------- |
| API Gateway           | Entry point for all requests      |
| Orchestrator          | Coordinates agent tasks           |
| Task Execution Engine | Runs and schedules tasks          |
| Agent Runtime         | Executes agent logic              |
| Tool Execution Layer  | Executes tools and integrations   |
| Data Layer            | Stores system state and knowledge |

---

## 4. High-Level System Architecture

Initial deployment architecture:

```
Users
   │
   ▼
Web Dashboard
   │
   ▼
API Gateway
   │
   ▼
Core Backend
 ┌──────────────────────────────┐
 │                              │
 │  Orchestrator                │
 │  Task Execution Engine       │
 │  Agent Runtime               │
 │  Tool Execution Layer        │
 │  Permission Manager          │
 │                              │
 └──────────────────────────────┘
   │
   ├──────────────┬──────────────┐
   ▼              ▼              ▼
PostgreSQL       Redis        Vector DB
(System DB)     (Queue)       (Knowledge)
```

Everything runs initially on **one server**.

---

## 5. Core Components

---

### 5.0 Layer 1 — User Interface Layer

This layer provides **human interaction with the platform**.

#### Responsibilities

- display system state
- allow task creation
- manage approvals
- monitor agents
- display logs and metrics

#### Technology

Recommended stack:

```
Next.js
React
TypeScript
TailwindCSS
```

#### Key Features

The dashboard includes:

1. Agent monitoring
2. Task management
3. Approval workflow interface
4. system configuration
5. analytics dashboards

#### Example UI Modules

```
frontend/
    dashboard/
    agents/
    tasks/
    approvals/
    analytics/
```

---

### 5.1 API Gateway

The **API Gateway** provides the entry point for all platform interactions.

Responsibilities:

- authentication
- request validation
- routing
- rate limiting
- audit logging

Typical endpoints:

```
POST /tasks
GET /tasks
POST /agents/run
POST /approvals
GET /logs
GET /agents
```

Technologies:

- FastAPI
- Express.js
- Go (optional)

---

### 5.2 Orchestrator

The **Orchestrator** coordinates the entire agent ecosystem.

Defined in:

```
ORCHESTRATOR_SPEC.md
```

Responsibilities:

- interpret user requests
- break requests into tasks
- assign agents
- manage dependencies
- request approvals
- monitor execution

Example flow:

```
User Request
     │
     ▼
Orchestrator
     │
     ├─ create task
     ├─ select agent
     ├─ schedule execution
     └─ monitor progress
```

---

### 5.3 Task Execution Engine

Defined in:

```
TASK_EXECUTION_ENGINE.md
```

The Task Execution Engine is responsible for:

- scheduling tasks
- running tasks asynchronously
- retrying failed tasks
- managing execution queues

Queue examples:

```
task_queue
agent_queue
tool_queue
approval_queue
```

Technology:

```
Redis
Celery / RQ / BullMQ
```

Agents tasks are defined in:

```
AGENT_TASK_LIBRARY.md
```

---

### 5.4 Agent Runtime

The **Agent Runtime** executes the AI agents.

Responsibilities:

- load agent prompts
- select LLM models
- execute reasoning loops
- call tools
- generate outputs

Prompts are defined in:

```
AGENT_PROMPTS.md
```

Rules are defined in:

```
AGENT_RULES.md
```

Agents may include:

- Data Engineering Agent
- Metadata Sync Agent
- Automation Agent
- Business Analyst Agent
- Research Agent

Defined in:

```
AGENT_ECOSYSTEM.md
```

---

### 5.5 Tool Execution Layer

The Tool Layer allows agents to interact with systems.

Examples:

```
database_query
api_call
web_search
file_analysis
workflow_trigger
script_execution
```

Tools may interact with:

- DHIS2
- Business systems
- Data pipelines
- APIs
- automation platforms (n8n)

This layer isolates **external integrations from agent logic**

Tools are defined in:

```
TOOL_REGISTRY.md
```

#### Tool Categories

The platform includes several tool categories.

---

#### Data Tools

Used for analytics and processing.

Examples:

```
data_cleaner
indicator_calculator
anomaly_detector
dataset_loader
```

---

#### Project Management Tools

Used by the Project Manager Agent.

Examples:

```
create_project
create_task
update_task_status
generate_report
```

---

#### Document Tools

Used to generate consulting deliverables.

Examples:

```
proposal_generator
report_writer
document_formatter
```

---

#### Infrastructure Tools

Used by the DevOps agent.

Examples:

```
check_server_health
deploy_application
monitor_logs
restart_service
```

These tools require **approval gates** before production execution.

---

#### Knowledge Tools

Used for knowledge retrieval.

Examples:

```
search_documents
retrieve_context
vector_query
```

---

---

### 5.6 Permission System

Defined in:

```
PERMISSION_MODEL.md
```

The Permission System controls:

- agent capabilities
- user permissions
- approval workflows
- restricted actions

Example restrictions:

```
read_data
modify_data
execute_script
deploy_system
access_external_api
```

Critical tasks require **human approval**.

---

## 6. Data Layer

The platform uses three main data stores.

---

### 6.1 PostgreSQL (System Database)

Stores:

```
users
tasks
agents
task_runs
logs
approvals
permissions
workflows
```

Schema defined in:

```
DATABASE_SCHEMA.md
```

---

### 6.2 Redis (Execution Queue)

Used for:

```
task queues
agent scheduling
temporary caching
session state
```

Benefits:

- fast
- reliable
- asynchronous execution

---

### 6.3 Vector Database

Stores:

```
embeddings
knowledge base
documents
agent memory
```

Possible technologies:

- pgvector
- Qdrant
- Weaviate

Recommended for initial deployment:

```
PostgreSQL + pgvector
```

### 6.4 File Storage

Stores:

- documents
- datasets
- reports

Recommended:

```
S3 compatible storage
MinIO
```

---

## 7. Agent Execution Lifecycle

Typical task execution flow:

```
User submits task
       │
       ▼
API receives request
       │
       ▼
Orchestrator creates task
       │
       ▼
Task assigned to agent
       │
       ▼
Agent generates execution plan
       │
       ▼
Agent calls tools
       │
       ▼
Results stored in database
       │
       ▼
Output returned to user
```

Example execution process:

---

### Step 1 — Request

User submits a task.

Example:

```
Analyze DHIS2 data imports
```

---

### Step 2 — Task Creation

API Gateway sends request to Orchestrator.

Orchestrator creates a **task record**.

---

### Step 3 — Agent Selection

The orchestrator selects an appropriate agent.

Example:

```
Data Integration Agent
```

---

### Step 4 — Task Queue

Task is placed into:

```
task_queue
```

---

### Step 5 — Agent Execution

Agent Worker retrieves task.

Agent:

```
load prompt
reason
call tools
produce output
```

---

### Step 6 — Tool Calls

Agent may call tools such as:

```
dhis2_import
data_validation
api_query
database_analysis
```

---

### Step 7 — Results Storage

Outputs stored in database.

---

### Step 8 — Completion

System updates dashboard and logs.

---

## 8. Agent Communication Architecture

Agents do **not communicate directly with each other**.

All communication passes through the orchestrator.

Communication flow:

```
Agent A
   │
   ▼
Orchestrator
   │
   ▼
Agent B
```

This ensures:

- centralized monitoring
- policy enforcement
- execution logging

Defined in:

```
AGENT_COMMUNICATION_PROTOCOL.md
```

---

## 9. Human-in-the-Loop Architecture

Certain actions require **human approval before execution**.

These include:

- financial actions
- production infrastructure changes
- client communications
- external publishing

Approval workflow:

```
Agent requests approval
       │
       ▼
Approval record created
       │
       ▼
Human reviews request
       │
       ▼
Approve / Reject
       │
       ▼
Agent continues or aborts
```

Approval requests are stored in the **approvals table**.

---

## 10. Dashboard

The dashboard allows operators to:

- monitor agents
- approve actions
- inspect logs
- manage workflows

Key pages:

```
Task Manager
Agent Monitor
Execution Logs
Approval Queue
System Health
```

Technology:

```
React / Next.js
```

---

## 11. Deployment Architecture

Initial deployment uses **Docker Compose**.

Example services:

```
nginx
backend
redis
postgres
vector-db
dashboard
```

Directory structure:

```
/tdc-ai-platform
    /backend
    /agents
    /tools
    /dashboard
    /configs
    docker-compose.yml
```

Defined in:

```
SYSTEM_DEPLOYMENT_ARCHITECTURE.md
```

---

## 12. Scaling Strategy

The system is designed to scale progressively.

---

### Stage 1 — Single Server

All services run together.

```
1 backend
1 database
1 queue
```

---

### Stage 2 — Worker Separation

Agent workers move to separate machines.

```
Server 1 → API + Orchestrator
Server 2 → Agent Workers
```

---

### Stage 3 — Distributed Platform

Full microservice architecture.

```
Gateway
Orchestrator
Agent Workers
Tool Service
Database Cluster
Monitoring System
```

---

## 13. Security Model

Security measures include:

- API authentication
- permission-based actions
- audit logging
- role-based access

Sensitive actions require:

```
human approval
```

Examples:

```
system deployment
database modification
external API calls
```

Persmissions are defined in:
PERMISSION_MODEL.md

Security is also defined in:
FAILURE_HANDLING_AND_RECOVERY.md

---

## 14. Observability

Monitoring features include:

```
task logs
agent activity logs
system metrics
error tracking
```

Recommended tools:

```
Prometheus
Grafana
ELK stack
```

Defined in:

```
OBSERVABILITY_AND_MONITORING.md
```

---

## 15. Integration Capabilities

The platform can integrate with:

```
DHIS2
Business ERPs
Automation tools (n8n)
Cloud services
Data pipelines
APIs
```

This enables TDC to provide **automation and AI consulting services**.

---

## 16. Future Enhancements

Possible platform extensions include:

- multi-agent collaboration
- reinforcement learning agents
- automated consulting workflows
- enterprise automation pipelines
- domain-specific agent ecosystems

---

## 17. Summary

The TDC AI Platform architecture provides:

- modular agent infrastructure
- scalable execution engine
- orchestration-based automation
- strong security and governance
- enterprise-grade integration capabilities

This architecture enables TDC Consulting Sarl to build a **powerful AI-driven automation platform for consulting, data systems, and business intelligence**.

---
