# TDC Agent Platform - Deployment Guide

## Prerequisites

- Docker and Docker Compose
- PostgreSQL database
- Redis
- Python 3.12+
- Node.js 18+

## Environment Variables

### Backend (.env)

```env
# Database
POSTGRES_USER=tdc_user
POSTGRES_PASSWORD=tdc_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=tdc_agent_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Security
SECRET_KEY=your-secret-key-change-in-production

# Logging
LOG_LEVEL=INFO
LOG_JSON=false

# LLM Providers
OPENAI_API_KEY=sk-...
DEFAULT_LLM_PROVIDER=openai
```

### Dashboard (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Docker Deployment

### Using Docker Compose

1. Create `.env` file with required variables
2. Run:

```bash
docker-compose up -d
```

### Services

- **API**: FastAPI server (port 8000)
- **Dashboard**: Next.js app (port 3000)
- **PostgreSQL**: Database (port 5432)
- **Redis**: Cache/Queue (port 6379)

## Manual Deployment

### Backend

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run database migrations:
```bash
# Tables are auto-created on startup
```

3. Start the API:
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Dashboard

1. Install dependencies:
```bash
cd dashboard
npm install
```

2. Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start development server:
```bash
npm run dev
```

## Production Considerations

### Security

1. Change `SECRET_KEY` to a secure random value
2. Enable HTTPS
3. Set up proper CORS configuration
4. Use strong database passwords

### Performance

1. Configure Redis for caching
2. Set up connection pooling for PostgreSQL
3. Use a reverse proxy (nginx)
4. Enable caching headers

### Monitoring

1. Set up log aggregation
2. Configure health checks
3. Monitor metrics endpoint

## Health Checks

- API Health: `GET /api/v1/health`
- Readiness: `GET /api/v1/health/ready`
- Liveness: `GET /api/v1/health/live`

## Troubleshooting

### Database Connection Failed

1. Check PostgreSQL is running
2. Verify credentials in `.env`
3. Check network connectivity

### Redis Connection Failed

1. Check Redis is running
2. Verify host/port in configuration
3. Queue operations will fall back to sync mode

### API Returns 401

1. Check JWT token is valid
2. Verify token hasn't expired
3. Check Authorization header format
