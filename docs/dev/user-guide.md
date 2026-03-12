# TDC Agent Platform - User Guide

## Overview

The TDC Agent Platform is a multi-agent system designed to assist with various business operations including project management, proposal writing, data analysis, development, DevOps, training, finance, and governance.

## Getting Started

### Login

1. Open the dashboard in your browser
2. Click "Demo Login" to access with demo credentials
3. You will be redirected to the main dashboard

### Dashboard Navigation

The dashboard has several tabs:

- **Agent Chat**: Interact with AI agents
- **Task Board**: View and manage tasks
- **History**: View task history
- **Approvals**: Review pending approvals
- **Data Analysis**: Run data analysis
- **Training Center**: Access training resources
- **Governance**: View governance metrics
- **Audit Logs**: View system audit logs

## Using Agents

### Available Agents

1. **Project Manager (PM) Agent**: Project planning, task management, risk analysis
2. **Proposal Agent**: Proposal writing, CV search, document search
3. **Data Agent**: Data analysis, DHIS2 fetch, statistics
4. **Developer Agent**: Code generation, code review
5. **DevOps Agent**: Deployment, system monitoring, Git operations
6. **Training Agent**: Quiz generation, manual creation, helpdesk
7. **Finance Agent**: Budget analysis, donor compliance
8. **Director Agent**: Strategic reports, risk summaries, system audits

### Creating a Task

1. Navigate to the Task Board
2. Click "New Task"
3. Fill in the task details:
   - Title
   - Description
   - Priority (low, medium, high, critical)
   - Task Type
4. Submit the task

### Approval Workflow

Some tasks may require approval before execution:

1. When a high-risk action is triggered, an approval request is created
2. Approvers receive a notification
3. Review the approval request details
4. Click "Approve" or "Reject"
5. Add optional comments
6. The task proceeds based on the decision

## Security

### Roles

- **Admin**: Full access to all features
- **Manager**: Can approve tasks and manage users
- **User**: Can create tasks and view own tasks

### Authentication

- JWT tokens are used for authentication
- Tokens expire after 24 hours
- Use the refresh token to obtain new access tokens

## Troubleshooting

### Common Issues

**Login Failed**
- Ensure you're using valid credentials
- Check network connectivity

**Task Not Executing**
- Check task status in Task Board
- Verify approval requirements are met

**Agent Not Responding**
- Check system health in the dashboard
- Review audit logs for errors
