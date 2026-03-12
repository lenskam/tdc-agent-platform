# TOOL_REGISTRY.md

## Agent Tool Registry

### TDC Consulting – Multi-Agent AI Platform

---

# 1. Purpose of This Document

This document defines the **complete registry of tools that AI agents can use** inside the TDC Multi-Agent Platform.

A tool is a **controlled interface that allows an agent to interact with the system or external services**.

Examples include:

- database operations
- analytics functions
- document generation
- infrastructure management
- knowledge retrieval

Agents **must never access system resources directly**.

Instead, they must use tools defined in this registry.

This ensures:

- system security
- predictable behavior
- auditability
- safe infrastructure interaction

---

# 2. Tool Design Principles

All tools must follow these principles.

---

## 2.1 Explicit Interface

Each tool must define:

- name
- description
- allowed agents
- input schema
- output schema
- risk level

---

## 2.2 Structured Inputs

Tools must receive **structured parameters**.

Example:

```json
{
  "tool": "create_project",
  "parameters": {
    "client_id": "uuid",
    "project_name": "Health Monitoring System"
  }
}
```

Agents must **never send natural language instructions to tools**.

---

## 2.3 Structured Outputs

All tools must return structured responses.

Example:

```json
{
  "status": "success",
  "project_id": "uuid",
  "message": "Project created successfully"
}
```

---

## 2.4 Logging Requirement

Every tool call must generate a log entry containing:

- agent_id
- task_id
- tool_name
- parameters
- execution_result
- timestamp

---

## 2.5 Permission Enforcement

Each tool defines **allowed agents**.

Agents must not call tools outside their permissions.

Example:

```
Finance tools → FinanceAgent only
Infrastructure tools → DevOpsAgent only
```

---

# 3. Tool Categories

Tools are organized into the following categories.

```
Project Management Tools
Data & Analytics Tools
Document Generation Tools
Knowledge Retrieval Tools
Infrastructure & DevOps Tools
Communication Tools
Financial Tools
System Tools
```

---

# 4. Project Management Tools

These tools support **project planning and task management**.

Primarily used by:

```
ProjectManagerAgent
```

---

## Tool: create_project

Creates a new consulting project.

### Allowed Agents

```
ProjectManagerAgent
AdminAgent
```

### Input Schema

```json
{
  "client_id": "uuid",
  "project_name": "string",
  "description": "string",
  "start_date": "date",
  "end_date": "date"
}
```

### Output Schema

```json
{
  "status": "success",
  "project_id": "uuid"
}
```

---

## Tool: create_task

Creates a project task.

### Input

```json
{
  "project_id": "uuid",
  "title": "string",
  "description": "string",
  "assigned_agent": "string",
  "priority": "low | medium | high"
}
```

### Output

```json
{
  "task_id": "uuid",
  "status": "created"
}
```

---

## Tool: update_task_status

Updates the status of a task.

### Input

```json
{
  "task_id": "uuid",
  "status": "pending | in_progress | completed | failed"
}
```

---

# 5. Data & Analytics Tools

Used by:

```
DataAnalystAgent
MonitoringAgent
```

These tools process datasets and compute indicators.

---

## Tool: load_dataset

Loads dataset from storage.

### Input

```json
{
  "dataset_id": "uuid"
}
```

### Output

```
dataset_reference
```

---

## Tool: clean_dataset

Performs data cleaning.

### Input

```json
{
  "dataset_reference": "string",
  "cleaning_rules": "object"
}
```

---

## Tool: calculate_indicators

Computes metrics or indicators.

### Input

```json
{
  "dataset_reference": "string",
  "indicators": ["list"]
}
```

---

## Tool: detect_anomalies

Identifies abnormal values.

### Input

```json
{
  "dataset_reference": "string"
}
```

---

# 6. Document Generation Tools

Used for **consulting deliverables**.

Allowed agents:

```
ProposalAgent
TrainingAgent
ProjectManagerAgent
```

---

## Tool: generate_proposal

Creates a proposal draft.

### Input

```json
{
  "client_name": "string",
  "project_context": "string",
  "services": ["list"]
}
```

### Output

```
proposal_document_reference
```

---

## Tool: generate_report

Creates analytical reports.

### Input

```json
{
  "project_id": "uuid",
  "analysis_results": "object"
}
```

---

## Tool: format_document

Formats documents into final deliverables.

### Input

```
document_reference
format_type: pdf | docx | markdown
```

---

# 7. Knowledge Retrieval Tools

Used for **RAG pipelines and consulting knowledge retrieval**.

Allowed agents:

```
All agents
```

---

## Tool: search_documents

Searches internal document database.

### Input

```json
{
  "query": "string"
}
```

---

## Tool: retrieve_context

Retrieves knowledge chunks for LLM context.

### Input

```json
{
  "document_id": "uuid"
}
```

---

## Tool: vector_query

Searches vector database.

### Input

```json
{
  "query": "string",
  "top_k": 5
}
```

---

# 8. Infrastructure & DevOps Tools

These tools interact with servers and infrastructure.

Allowed agents:

```
DevOpsAgent
```

These tools are **high-risk**.

Some require **human approval**.

---

## Tool: check_server_health

Checks server status.

### Input

```json
{
  "server_id": "string"
}
```

### Output

```
cpu_usage
memory_usage
disk_usage
uptime
```

---

## Tool: deploy_application

Deploys an application.

### Risk Level

HIGH

Requires **human approval**.

### Input

```json
{
  "repository": "string",
  "branch": "string",
  "environment": "staging | production"
}
```

---

## Tool: restart_service

Restarts a service.

### Input

```json
{
  "service_name": "string"
}
```

---

# 9. Communication Tools

These tools interact with **external communications**.

Allowed agents:

```
ProjectManagerAgent
ProposalAgent
```

---

## Tool: send_email

Sends an email.

### Risk Level

Medium

### Input

```json
{
  "recipient": "string",
  "subject": "string",
  "body": "string"
}
```

Human approval may be required for **external clients**.

---

# 10. Financial Tools

Used for **financial operations**.

Allowed agents:

```
FinanceAgent
```

---

## Tool: generate_invoice

Creates invoice.

### Input

```json
{
  "client_id": "uuid",
  "project_id": "uuid",
  "amount": "number"
}
```

---

## Tool: generate_budget

Creates project budget.

### Input

```json
{
  "project_id": "uuid",
  "cost_items": ["list"]
}
```

---

# 11. System Tools

These tools are used internally by the platform.

Allowed agents:

```
Orchestrator
AdminAgent
```

---

## Tool: log_event

Creates system log entry.

### Input

```json
{
  "event_type": "string",
  "message": "string"
}
```

---

## Tool: request_human_approval

Requests approval.

### Input

```json
{
  "action_description": "string",
  "risk_level": "low | medium | high"
}
```

---

# 12. Tool Risk Levels

Each tool is assigned a **risk level**.

### Low Risk

Safe operations.

Examples:

- search_documents
- vector_query
- load_dataset

---

### Medium Risk

Operations affecting projects.

Examples:

- create_task
- send_email
- generate_report

---

### High Risk

Operations affecting infrastructure or finances.

Examples:

- deploy_application
- restart_service
- generate_invoice

These require **human approval**.

---

# 13. Tool Execution Flow

When an agent uses a tool:

```
Agent decides to use tool
       │
       ▼
Tool call generated
       │
       ▼
Orchestrator validates permission
       │
       ▼
Tool executed
       │
       ▼
Result returned to agent
       │
       ▼
Result logged in database
```

---

# 14. Adding New Tools

When adding a tool:

Developers must define:

```
tool_name
description
allowed_agents
input_schema
output_schema
risk_level
```

Tool must be added to:

```
TOOL_REGISTRY.md
tool implementation directory
```

Example directory:

```
src/tools/
    project_tools.py
    data_tools.py
    devops_tools.py
```

---

# 15. Final Rule

Agents must treat this registry as the **single source of truth for tool usage**.

Agents must:

- only use defined tools
- follow defined schemas
- respect permissions
- log every action

Tools ensure **safe collaboration between AI agents, humans, and infrastructure**.

---
