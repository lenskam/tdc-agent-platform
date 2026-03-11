Implementation Plan - Project Manager Agent & Dashboard
Goal Description
Develop the fully functional Project Manager Agent to serve as the "Execution Coordinator" for TDC. This includes enabling it to store/retrieve tasks from the database, track deadlines, and generate reports. Additionally, we will implement a basic Web Dashboard to visualize these agents and tasks, along with a comprehensive Testing Strategy.

User Review Required
IMPORTANT

Testing Approach: We will use pytest for backend logic and Playwright for dashboard E2E tests. Agents will be tested using "Mock LLMs" for deterministic logic and "Real LLMs" (cached) for quality checks.

Proposed Changes
1. Project Manager Agent Enhancements
[MODIFY] 

src/agents/pm_agent.py
Upgrade 

plan_project
 to not just return text, but structure data into 

Project
 and 

Task
 objects.
Add create_report method to summarize project status from the DB.
[NEW] src/tools/task_manager.py
Goal: Allow agents to interact with the PostgreSQL database.
Functions: add_task, update_task_status, get_overdue_tasks.
Integration: Wrapped as LangChain/CrewAI Tools.
[NEW] src/tools/reporting_tool.py
Generates Markdown/PDF reports from project data.
2. Dashboard (Frontend)
[NEW] dashboard/
Initialize a Next.js application in tdc-agent-platform/dashboard.
Components:
AgentChat: Interface to talk to PM Agent.
TaskBoard: Kanban view of tasks created by the agent.
Integration: Calls FastAPI backend.
3. Testing Infrastructure
[NEW] tests/agents/test_pm_agent.py
Unit: Verify 

plan_project
 prompts are constructed correctly.
Integration: Run agent -> saves tasks to Test DB -> verify rows exist.
[NEW] tests/dashboard/e2e.spec.ts
Playwright test: Open Dashboard -> Type "Plan Website" -> Check if Tasks appear.
Verification Plan
Automated Tests
Backend: pytest tests/agents/
Frontend: npm run test:e2e (in dashboard dir)
Manual Verification
Flow:
User asks PM: "Create a plan for the DHIS2 Upgrade".
Check Dashboard: See "DHIS2 Upgrade" project with 5-10 subtasks.
User asks PM: "Generate a status report".
PM returns a summary string.