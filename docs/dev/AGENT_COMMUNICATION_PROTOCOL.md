
# AGENT_COMMUNICATION_PROTOCOL.md

## 1. Overview

This document defines the **communication architecture between agents, the orchestrator, tools, and external systems** within the TDC Multi-Agent Platform.

The communication protocol ensures:

* controlled interactions
* traceable workflows
* secure tool usage
* reliable task delegation
* observability of all agent activity

All communication is **mediated by the Orchestrator**.

Agents **cannot directly communicate with each other or access tools without orchestrator validation**.

---

# 2. Communication Architecture

The platform follows a **hub-and-spoke model**.

```
User
   │
   ▼
Frontend
   │
   ▼
Orchestrator
   │
   ├── Agent A
   ├── Agent B
   ├── Agent C
   │
   ▼
Tool Registry
   │
   ├── Internal Tools
   ├── External APIs
   └── System Services
```

The **Orchestrator acts as the central router and controller**.

---

# 3. Communication Channels

The platform supports several communication channels.

### 3.1 Task Messages

Used for assigning tasks.

Example structure:

```json
{
  "task_id": "uuid",
  "task_type": "data_analysis",
  "priority": "high",
  "assigned_agent": "data_agent",
  "input_data": {},
  "created_by": "user_id"
}
```

---

### 3.2 Agent Status Updates

Agents periodically report status.

Example:

```json
{
  "agent_id": "agent_analytics_01",
  "status": "running",
  "current_task": "task_2354",
  "cpu_usage": 22,
  "memory_usage": 512
}
```

---

### 3.3 Tool Invocation Messages

Agents request tool usage.

Example:

```json
{
  "agent_id": "research_agent",
  "tool": "web_search",
  "parameters": {
    "query": "AI automation adoption in Africa"
  }
}
```

The orchestrator verifies permissions before execution.

---

### 3.4 Task Result Messages

Agents submit results.

```json
{
  "task_id": "task_5532",
  "status": "completed",
  "result": {},
  "confidence_score": 0.82
}
```

---

# 4. Communication Protocols

Different transport mechanisms may be used depending on architecture.

### Supported protocols

| Protocol      | Purpose                              |
| ------------- | ------------------------------------ |
| REST API      | frontend interactions                |
| Message Queue | agent task routing                   |
| WebSockets    | real-time updates                    |
| gRPC          | high-performance agent communication |

---

# 5. Message Queue Architecture

Agents communicate asynchronously through **a message broker**.

Possible technologies:

* Redis Streams
* RabbitMQ
* Apache Kafka
* NATS

Queues include:

```
task_queue
agent_queue
tool_queue
result_queue
approval_queue
```

---

# 6. Task Routing Logic

When a task is created:

1. Request received
2. Orchestrator evaluates task type
3. Agent selected
4. Task placed in agent queue
5. Agent executes task
6. Result returned

---

# 7. State Management

The orchestrator maintains task states.

States include:

```
created
queued
running
awaiting_approval
completed
failed
cancelled
```

---

# 8. Inter-Agent Collaboration

Agents collaborate indirectly.

Example workflow:

```
Strategy Agent
     │
     ▼
Research Agent
     │
     ▼
Data Agent
     │
     ▼
Report Agent
```

Each step is mediated by the orchestrator.

---

# 9. Communication Security

All communications enforce:

* authentication tokens
* role permissions
* encrypted transport (TLS)
* message validation

---

# 10. Rate Limiting

Agents have limits for:

* API calls
* tool invocations
* external queries

This prevents system overload.

---

# 11. Communication Logging

Every message is logged.

Logs contain:

* sender
* receiver
* message type
* timestamp
* payload metadata

---

