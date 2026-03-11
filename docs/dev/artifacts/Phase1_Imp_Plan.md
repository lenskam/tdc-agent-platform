# Phase 1: Core Framework & Project Manager Agent Completion

## Goal Description

Complete the "Infrastructure Foundation" and "Project Manager Agent" from the master plan.
While the basic agent and tools exist, we need to add advanced capabilities (Time Estimation, Risk Analysis), robust reporting (PDF support), and comprehensive testing (E2E).

## User Review Required

> [!IMPORTANT]
>
> - **PDF Generation Dependency**: We will need `weasyprint` or `reportlab`. Please confirm if there are system dependency constraints.
> - **LLM Costs**: Testing "Risk Analysis" with real LLMs can be costly. We will use mocks for CI/CD.

## Proposed Changes

### Core Framework

#### [MODIFY] [llm_router.py](file:///home/deployer/projects/tdc-agent-platform/src/core/llm_router.py)

- Add failover logic (e.g., if OpenAI fails, try Ollama).
- Add cost tracking logging.

### Tools Layer

#### [NEW] [time_estimator.py](file:///home/deployer/projects/tdc-agent-platform/src/tools/time_estimator.py)

- `estimate_task_duration(task_description)`: Uses LLM to guess hours/days.
- Returns structured JSON: `{ "optimistic": 4, "pessimistic": 12, "most_likely": 8 }`.

#### [NEW] [risk_analyzer.py](file:///home/deployer/projects/tdc-agent-platform/src/tools/risk_analyzer.py)

- `analyze_project_risks(project_id)`: Scans all tasks in a project.
- Identifies bottlenecks (e.g., "Data Analyst" overloaded).

#### [MODIFY] [reporting_tool.py](file:///home/deployer/projects/tdc-agent-platform/src/tools/reporting_tool.py)

- Add `generate_pdf_report(project_id)` function.
- Store PDF in a static file directory for download via Dashboard.

### Project Manager Agent

#### [MODIFY] [pm_agent.py](file:///home/deployer/projects/tdc-agent-platform/src/agents/pm_agent.py)

- Integrate `TimeEstimatorTool` and `RiskAnalyzerTool`.
- Update system prompt to proactively check for risks before finalizing a plan.

### Dashboard (Frontend)

#### [NEW] [dashboard/tests/e2e.spec.ts](file:///home/deployer/projects/tdc-agent-platform/dashboard/tests/e2e.spec.ts)

- Implement Playwright tests.
- Scenario: User triggers "Plan Project" -> waits for "Project Planned" toast -> verifies tasks appear in Board.

## Verification Plan

### Automated Tests

- **Unit**: `pytest tests/tools/test_time_estimator.py`
- **Integration**: `pytest tests/agents/test_pm_agent_full_flow.py` (Mocked LLM)
- **E2E**: `npm run test:e2e` in dashboard directory.

### Manual Verification

- Run the Agent via API: `POST /pm/plan` with "Migrate DHIS2 to Cloud".
- Check logs to see `RiskAnalyzerTool` being called.
- Download generated PDF report from Dashboard.
