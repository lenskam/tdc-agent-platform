# Deployment Guide - TDC Agent Platform

## 1. Prerequisites
- A Hostinger VPS (Ubuntu 20.04+ recommended)
- Docker & Docker Compose installed
- An OpenAI API Key (or other provider)

## 2. Server Setup (One-time)
SSH into your VPS:
```bash
ssh root@your_vps_ip
```

Install Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

## 3. Project Deployment
Clone the repository (or copy files):
```bash
git clone <repo_url> tdc-agents
cd tdc-agents
```

Configuration:
```bash
cp .env.example .env
nano .env
```
Fill in your `OPENAI_API_KEY` and adjust `POSTGRES_PASSWORD`.

## 4. Launch Services
```bash
docker-compose up -d --build
```
This will start:
- **Backend API**: Port 8000
- **PostgreSQL**: Port 5432
- **Vector DB**: Persisted volume

## 5. Verification
Check logs:
```bash
docker-compose logs -f backend
```
Test the API:
```bash
curl http://localhost:8000/
# Output: {"message": "TDC Agent Platform is running"}
```

## 6. Local LLM Setup (Optional)
If you want to use local models on the VPS (ensure >16GB RAM):
1. Install Ollama on the host: `curl -fsSL https://ollama.com/install.sh | sh`
2. Pull model: `ollama pull llama3`
3. Update `.env`:
   ```bash
   DEFAULT_LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://host.docker.internal:11434
   ```
