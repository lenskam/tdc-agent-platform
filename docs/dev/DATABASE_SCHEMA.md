# DATABASE_SCHEMA.md

# 1. Purpose

This document defines the **database schema** for the **TDC Multi-Agent Platform**.

The database stores all persistent system data including:

- agents and capabilities
- task definitions and execution history
- workflow state
- approvals and human interactions
- tool usage
- system logs
- monitoring metrics
- security and access control

The schema supports the **Orchestrator Engine** defined in `ORCHESTRATOR_SPEC.md`.

---

# 2. Database Technology

Recommended database:

```
PostgreSQL 15+
```

Reasons:

- strong ACID guarantees
- JSONB support for flexible data
- full-text search
- strong indexing
- mature ecosystem

Optional extensions:

```
uuid-ossp
pgcrypto
pgvector
```

---

# 3. Database High-Level Architecture

```
Database
│
├── Agent Management
│
├── Task Management
│
├── Workflow Engine
│
├── Tool Registry
│
├── Human Approval System
│
├── Security & Access Control
│
├── Monitoring & Logs
│
└── Knowledge & Documents
```

---

# 4. Agent Management Tables

## agents

Stores registered agents in the system.

```
CREATE TABLE agents (
    agent_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    agent_type TEXT,
    department TEXT,
    autonomy_level TEXT,
    status TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

Example agent types:

```
strategy_agent
engineering_agent
data_agent
sales_agent
operations_agent
monitoring_agent
```

---

## agent_capabilities

Defines what tasks an agent can perform.

```
CREATE TABLE agent_capabilities (
    capability_id UUID PRIMARY KEY,
    agent_id UUID REFERENCES agents(agent_id),
    capability_name TEXT,
    description TEXT
);
```

Example:

```
code_analysis
deployment
dataset_analysis
lead_scoring
business_analysis
```

---

## agent_status

Tracks real-time health of agents.

```
CREATE TABLE agent_status (
    status_id UUID PRIMARY KEY,
    agent_id UUID REFERENCES agents(agent_id),
    health_status TEXT,
    cpu_usage FLOAT,
    memory_usage FLOAT,
    last_heartbeat TIMESTAMP
);
```

Health states:

```
healthy
degraded
offline
failed
```

---

# 5. Task Management Tables

## tasks

Central table storing all tasks.

```
CREATE TABLE tasks (
    task_id UUID PRIMARY KEY,
    task_name TEXT,
    task_type TEXT,
    description TEXT,
    created_by TEXT,
    assigned_agent UUID REFERENCES agents(agent_id),
    status TEXT,
    priority TEXT,
    input_data JSONB,
    output_data JSONB,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

Status values:

```
pending
queued
running
waiting_approval
completed
failed
```

Priority values:

```
critical
high
normal
low
background
```

---

## task_logs

Stores detailed execution logs.

```
CREATE TABLE task_logs (
    log_id UUID PRIMARY KEY,
    task_id UUID REFERENCES tasks(task_id),
    agent_id UUID REFERENCES agents(agent_id),
    log_level TEXT,
    message TEXT,
    timestamp TIMESTAMP
);
```

Log levels:

```
INFO
WARNING
ERROR
DEBUG
```

---

## task_dependencies

Defines dependencies between tasks.

```
CREATE TABLE task_dependencies (
    dependency_id UUID PRIMARY KEY,
    task_id UUID REFERENCES tasks(task_id),
    depends_on_task UUID REFERENCES tasks(task_id)
);
```

This enables workflow chaining.

---

# 6. Workflow Engine Tables

## workflows

Stores workflow definitions.

```
CREATE TABLE workflows (
    workflow_id UUID PRIMARY KEY,
    workflow_name TEXT,
    description TEXT,
    created_by TEXT,
    created_at TIMESTAMP
);
```

---

## workflow_steps

Each workflow is composed of multiple steps.

```
CREATE TABLE workflow_steps (
    step_id UUID PRIMARY KEY,
    workflow_id UUID REFERENCES workflows(workflow_id),
    step_order INTEGER,
    task_type TEXT,
    assigned_agent_type TEXT,
    requires_approval BOOLEAN
);
```

---

## workflow_executions

Tracks runtime workflow instances.

```
CREATE TABLE workflow_executions (
    execution_id UUID PRIMARY KEY,
    workflow_id UUID REFERENCES workflows(workflow_id),
    status TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

---

## workflow_execution_steps

Tracks step execution.

```
CREATE TABLE workflow_execution_steps (
    execution_step_id UUID PRIMARY KEY,
    execution_id UUID REFERENCES workflow_executions(execution_id),
    step_id UUID REFERENCES workflow_steps(step_id),
    task_id UUID REFERENCES tasks(task_id),
    status TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

---

# 7. Human-in-the-Loop Approval System

## approval_requests

Stores approval requests.

```
CREATE TABLE approval_requests (
    approval_id UUID PRIMARY KEY,
    task_id UUID REFERENCES tasks(task_id),
    requested_by_agent UUID REFERENCES agents(agent_id),
    risk_level TEXT,
    approval_status TEXT,
    requested_at TIMESTAMP,
    decided_at TIMESTAMP
);
```

Approval status:

```
pending
approved
rejected
```

Risk levels:

```
low
medium
high
critical
```

---

## approval_decisions

Tracks who approved.

```
CREATE TABLE approval_decisions (
    decision_id UUID PRIMARY KEY,
    approval_id UUID REFERENCES approval_requests(approval_id),
    user_id UUID,
    decision TEXT,
    comments TEXT,
    timestamp TIMESTAMP
);
```

---

# 8. Tool Registry Tables

## tools

Stores registered tools available to agents.

```
CREATE TABLE tools (
    tool_id UUID PRIMARY KEY,
    name TEXT,
    description TEXT,
    tool_type TEXT,
    endpoint TEXT,
    created_at TIMESTAMP
);
```

Example tools:

```
github_api
ssh_executor
docker_runner
database_query
document_parser
```

---

## agent_tool_permissions

Defines which agents can use which tools.

```
CREATE TABLE agent_tool_permissions (
    permission_id UUID PRIMARY KEY,
    agent_id UUID REFERENCES agents(agent_id),
    tool_id UUID REFERENCES tools(tool_id),
    permission_level TEXT
);
```

Permission levels:

```
read
execute
admin
```

---

## tool_usage_logs

Tracks tool usage.

```
CREATE TABLE tool_usage_logs (
    usage_id UUID PRIMARY KEY,
    tool_id UUID REFERENCES tools(tool_id),
    agent_id UUID REFERENCES agents(agent_id),
    task_id UUID REFERENCES tasks(task_id),
    execution_status TEXT,
    execution_time FLOAT,
    timestamp TIMESTAMP
);
```

---

# 9. Security & Access Control

## users

Human users of the system.

```
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT,
    role TEXT,
    password_hash TEXT,
    created_at TIMESTAMP
);
```

Roles:

```
admin
operator
engineer
viewer
```

---

## api_keys

API authentication keys.

```
CREATE TABLE api_keys (
    key_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    api_key TEXT,
    created_at TIMESTAMP,
    expires_at TIMESTAMP
);
```

---

## audit_logs

Tracks all sensitive actions.

```
CREATE TABLE audit_logs (
    audit_id UUID PRIMARY KEY,
    actor_type TEXT,
    actor_id TEXT,
    action TEXT,
    resource TEXT,
    timestamp TIMESTAMP
);
```

Actor types:

```
agent
user
system
```

---

# 10. Monitoring & Metrics

## system_metrics

Stores system metrics.

```
CREATE TABLE system_metrics (
    metric_id UUID PRIMARY KEY,
    metric_name TEXT,
    metric_value FLOAT,
    recorded_at TIMESTAMP
);
```

Examples:

```
tasks_per_hour
agent_cpu_usage
workflow_latency
error_rate
```

---

## alerts

Stores system alerts.

```
CREATE TABLE alerts (
    alert_id UUID PRIMARY KEY,
    alert_type TEXT,
    severity TEXT,
    message TEXT,
    triggered_at TIMESTAMP,
    resolved BOOLEAN
);
```

Severity levels:

```
info
warning
critical
```

---

# 11. Knowledge Base Tables

For AI consulting and documentation tasks.

---

## documents

Stores internal documents.

```
CREATE TABLE documents (
    document_id UUID PRIMARY KEY,
    title TEXT,
    content TEXT,
    created_at TIMESTAMP
);
```

---

## knowledge_embeddings

Used for RAG search.

```
CREATE TABLE knowledge_embeddings (
    embedding_id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(document_id),
    embedding VECTOR(1536)
);
```

Requires:

```
pgvector extension
```

---

# 12. Indexing Strategy

Important indexes:

```
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_agent ON tasks(assigned_agent);
CREATE INDEX idx_workflow_execution_status ON workflow_executions(status);
CREATE INDEX idx_approval_status ON approval_requests(approval_status);
```

Indexes improve performance for:

- task queues
- workflow execution
- monitoring queries.

---

# 13. Data Retention Policies

Recommended retention:

```
task_logs: 90 days
tool_usage_logs: 180 days
audit_logs: permanent
system_metrics: aggregated after 30 days
```

---

# 14. Backup Strategy

Recommended:

```
Daily automated backups
Weekly full backup
Point-in-time recovery
```

Use:

```
pg_dump
or managed database backups
```

---

# 15. Example Data Flow

Example: **Client consulting request**

1. User submits request

```
INSERT INTO tasks
```

2. Orchestrator assigns agent

```
assigned_agent = strategy_agent
```

3. Strategy agent runs analysis

```
task_logs created
```

4. Engineering agent triggered

```
workflow step executed
```

5. Proposal generated

```
approval_request created
```

6. Human approves

```
approval_decision stored
```

7. Project created

```
workflow completed
```

---

# 16. Future Schema Extensions

Possible future tables:

```
client_accounts
project_management
billing_system
AI model registry
training datasets
agent learning feedback
```

---

✅ With this file, your system now has **the complete technical specification required to build the platform**.

Your architecture set now includes:

```
GEMINI.md
ARCHITECTURE.md
AGENT_RULES.md
AGENT_PROMPTS.md
TOOL_REGISTRY.md
AGENT_TASK_LIBRARY.md
ORCHESTRATOR_SPEC.md
DATABASE_SCHEMA.md
```

---
