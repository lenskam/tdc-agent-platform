# TDC Agent Platform

A multi-agent platform for TDC Consulting that coordinates 8 specialized AI agents to handle project management, proposals, data analysis, development, DevOps, training, finance, and governance tasks.

## Overview

The TDC Agent Platform is a FastAPI-based backend with a Next.js dashboard that orchestrates multiple AI agents using LangChain and CrewAI. The platform provides task routing, approval workflows, observability, and comprehensive auditing.

### Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Dashboard  │────▶│  FastAPI     │────▶│  Orchestrator│
│  (Next.js) │     │  Backend     │     │  + Queue    │
└─────────────┘     └──────────────┘     └─────────────┘
                           │                     │
                           ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │  PostgreSQL  │     │   Redis    │
                    │  Database    │     │   Queue    │
                    └──────────────┘     └─────────────┘
```

## Features

### AI Agents
- **Project Manager Agent** - Project planning, task management, risk analysis
- **Proposal Agent** - Proposal writing, CV search, document search
- **Data Agent** - Data analysis, DHIS2 integration, statistics
- **Developer Agent** - Code generation, code review, sandbox execution
- **DevOps Agent** - Deployment, system monitoring, Git operations
- **Training Agent** - Quiz generation, manual creation, helpdesk
- **Finance Agent** - Budget analysis, donor compliance
- **Director Agent** - Strategic reports, risk summaries, system audits

### Core Capabilities
- **Task Orchestration** - Route tasks to appropriate agents
- **State Management** - Track task status through lifecycle
- **Approval Workflows** - Human-in-the-loop for high-risk actions
- **JWT Authentication** - Secure access with role-based permissions
- **Task Queue** - Redis-backed queue for async task processing

### Observability
- **Structured Logging** - JSON formatted logs with context
- **Audit Logging** - Track all user actions
- **Metrics** - Task counts, agent activity, daily stats
- **Health Checks** - Database, Redis, and service health

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Primary database
- **Redis** - Task queue and caching
- **LangChain** - LLM framework
- **CrewAI** - Multi-agent orchestration
- **PyJWT** - JWT authentication

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Python 3.12+

### Using Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd tdc-agent-platform

# Start all services
docker-compose up -d

# Access the dashboard
open http://localhost:3001

# Access the API
open http://localhost:8001
```

### Manual Setup

#### Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the API
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Dashboard

```bash
cd dashboard

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8001" > .env.local

# Run development server
npm run dev
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database user | tdc_user |
| `POSTGRES_PASSWORD` | Database password | tdc_password |
| `POSTGRES_HOST` | Database host | localhost |
| `POSTGRES_PORT` | Database port | 5432 |
| `POSTGRES_DB` | Database name | tdc_agent_db |
| `REDIS_HOST` | Redis host | localhost |
| `REDIS_PORT` | Redis port | 6379 |
| `SECRET_KEY` | JWT secret key | dev-secret-key |
| `LOG_LEVEL` | Logging level | INFO |
| `OPENAI_API_KEY` | OpenAI API key | - |

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/login-demo | Demo login |
| GET | /api/v1/tasks/ | List tasks |
| POST | /api/v1/tasks/ | Create task |
| GET | /api/v1/approvals/pending | List pending approvals |
| POST | /api/v1/approvals/{id}/approve | Approve request |
| GET | /api/v1/metrics | Get metrics |
| GET | /api/v1/audit/ | Get audit logs |
| GET | /api/v1/health | Health check |

## Project Structure

```
tdc-agent-platform/
├── dashboard/                 # Next.js dashboard
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   └── package.json
├── src/
│   ├── api/                 # FastAPI routes
│   │   └── routes/
│   ├── agents/              # AI agent implementations
│   ├── auth/                # Authentication
│   ├── core/                # Core services
│   │   ├── audit.py         # Audit logging
│   │   ├── logging.py       # Structured logging
│   │   └── metrics.py       # Metrics service
│   ├── database/            # Database models
│   ├── orchestrator/        # Task orchestration
│   ├── queue/               # Redis queue
│   └── tools/               # Agent tools
├── tests/                   # Test files
├── docs/                    # Documentation
│   └── dev/
│       ├── user-guide.md
│       ├── api-documentation.md
│       └── deployment-guide.md
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Documentation

- [User Guide](docs/dev/user-guide.md) - How to use the platform
- [API Documentation](docs/dev/api-documentation.md) - API reference
- [Deployment Guide](docs/dev/deployment-guide.md) - Deployment instructions

## Development

### Running Tests

```bash
# Python tests
pytest tests/

# JavaScript/TypeScript lint
cd dashboard
npm run lint
```

### Adding New Agents

1. Create agent class in `src/agents/`
2. Implement agent tools in `src/tools/`
3. Add task type mapping in `src/orchestrator/task_router.py`
4. Register routes in `src/api/main.py`

## Security

- JWT-based authentication
- Password hashing with salt
- Role-based access control (admin, manager, user)
- Audit logging for all sensitive actions
- Structured logging without sensitive data

## Monitoring

### Health Checks
```bash
curl http://localhost:8000/api/v1/health
```

### Metrics
```bash
curl http://localhost:8000/api/v1/metrics
```

### Audit Logs
```bash
curl http://localhost:8000/api/v1/audit/
```

## License

Proprietary - TDC Consulting

## Support

For issues and questions, please contact the development team.
