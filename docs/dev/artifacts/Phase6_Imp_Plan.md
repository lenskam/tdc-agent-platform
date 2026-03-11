# Phase 6: Security & Governance

## Goal Description

Implement the "Director Agent" and "Finance Agent" to ensure organizational health and compliance.
These agents operate with the highest level of restriction. They focus on monitoring, auditing, and strategic advice, rather than autonomous execution of critical actions (like money transfer).

## User Review Required

> [!CRITICAL]
>
> - **Read-Only Finance Access**: The Finance Agent must have READ-ONLY access to financial data. It cannot execute transactions.
> - **Data Sensitivity**: Strategic reports from the Director Agent may contain sensitive business intel. These logs must be encrypted/access-controlled.

## Proposed Changes

### Agents

#### [NEW] [src/agents/finance_agent.py](file:///home/deployer/projects/tdc-agent-platform/src/agents/finance_agent.py)

- Role: "Financial Controller".
- Capabilities: Budget variance analysis, expense categorization, donor reporting compliance.
- Tools: `read_budget_sheet`, `check_donor_guidelines`.

#### [NEW] [src/agents/director_agent.py](file:///home/deployer/projects/tdc-agent-platform/src/agents/director_agent.py)

- Role: "Strategic Advisor".
- Capabilities: Synthesizing reports from all other agents (PM, Data, Finance).
- Tools: `query_all_agent_logs`, `summarize_key_risks`.

### Tools Layer

#### [NEW] [src/tools/audit_tools.py](file:///home/deployer/projects/tdc-agent-platform/src/tools/audit_tools.py)

- `scan_logs_for_anomalies()`: Regex/ML search for suspicious agent behavior.
- `verify_compliance(text)`: Checks if a proposal/report matches donor keywords.

### Core Infrastructure

#### [MODIFY] [src/core/security.py](file:///home/deployer/projects/tdc-agent-platform/src/core/security.py)

- Implement Role-Based Access Control (RBAC) for Agents.
- e.g., Only Finance Agent can call `read_budget_sheet`.

## Verification Plan

### Automated Tests

- **Unit**: `pytest tests/core/test_security_rbac.py` (Verify Finance Agent cannot call deploy_code).
- **Integration**: Feed a dummy budget with overspend -> Finance Agent flags it.

### Manual Verification

- Simulate a "Monthly Strategic Review".
- Director Agent should pull data from PM Agent (Project Status) and Finance Agent (Budget Status) and produce a 1-page summary.
