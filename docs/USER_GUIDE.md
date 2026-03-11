# User Guide - TDC Multi-Agent System

## Introduction
Welcome to your "Digital Staff". This system allows you to interact with AI agents specialized in consulting tasks.
**Current Agent**: Project Manager Agent (Beta)

## How to Interact

### Method 1: API (For Developers/Integrations)
The system exposes a REST API at `http://<your-server-ip>:8000/docs`.

**Example: Plan a New Project**
Endpoint: `POST /api/v1/agents/pm/plan`
Body:
```json
{
  "description": "Implementation of DHIS2 for the Ministry of Health in Cameroon. Timeline: 6 months. Deliverables: Server setup, Training 50 staff, Data migration."
}
```

**Response**:
The agent will return a JSON object with a list of tasks, timelines, and required resources.

### Method 2: CLI (Planned)
Future updates will allow you to run:
`./tdc-cli plan "Project description"`

## Best Practices
- **Be Specific**: The more context you give the agent, the better the plan.
- **Review**: Always review the agent's output. The status is "Human-in-the-loop".
- **Sensitive Data**: Use the Local LLM mode if pasting PII (Personally Identifiable Information).

## Troubleshooting
- **Agent seems stuck?** Check the logs `docker-compose logs backend`.
- **"Hallucinations"?** Verify the agent isn't inventing non-existent files. Provide reference docs in the prompt.
