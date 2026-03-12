# TDC Agent Platform - API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Health & Monitoring

#### GET /api/v1/health

Health check with database and Redis connectivity.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-12T12:00:00Z",
  "checks": {
    "database": {"status": "healthy", "message": "Connected"},
    "redis": {"status": "healthy", "message": "Connected"}
  }
}
```

#### GET /api/v1/metrics

Get application metrics.

**Response:**
```json
{
  "tasks": {"total": 10, "todo": 5, "done": 3, "in_progress": 2},
  "tasks_created_today": 2,
  "tasks_completed_today": 1,
  "agent_activity_7d": {"pm_agent": 5, "data_agent": 3},
  "generated_at": "2026-03-12T12:00:00Z"
}
```

### Authentication

#### POST /api/v1/auth/login-demo

Demo login for testing.

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "userId": "1",
    "email": "admin@tdc.com",
    "username": "admin",
    "role": "admin"
  }
}
```

### Tasks

#### GET /api/v1/tasks/

List tasks with optional filters.

**Query Parameters:**
- `status` (optional): Filter by status
- `project_id` (optional): Filter by project
- `assigned_to` (optional): Filter by assignee
- `limit` (optional): Limit results (default 100)

#### POST /api/v1/tasks/

Create a new task.

**Request:**
```json
{
  "title": "Task Title",
  "description": "Task description",
  "priority": "medium",
  "task_type": "proposal_writing",
  "project_id": 1
}
```

#### GET /api/v1/tasks/{id}

Get task details.

#### PATCH /api/v1/tasks/{id}

Update a task.

#### DELETE /api/v1/tasks/{id}

Delete a task.

#### GET /api/v1/tasks/{id}/status

Get task execution status.

### Approvals

#### GET /api/v1/approvals/

List approval requests.

**Query Parameters:**
- `status` (optional): Filter by status

#### GET /api/v1/approvals/pending

List pending approval requests.

#### POST /api/v1/approvals/{id}/approve

Quick approve endpoint.

#### POST /api/v1/approvals/{id}/reject

Quick reject endpoint.

### Audit Logs

#### GET /api/v1/audit/

List audit logs.

**Query Parameters:**
- `resource_type` (optional): Filter by resource type
- `action` (optional): Filter by action
- `user_id` (optional): Filter by user
- `limit` (optional): Limit results

#### GET /api/v1/audit/auth

List authentication audit logs.

#### GET /api/v1/audit/tasks

List task audit logs.

## Error Responses

All endpoints may return error responses:

```json
{
  "detail": "Error message"
}
```

### Common Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error
