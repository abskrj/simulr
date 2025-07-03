# Physics Simulation Dashboard - Docker Setup

This document explains how to run the Physics Simulation Dashboard using Docker containers.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│               Load Balancer                 │
│                 (Nginx)                     │
│          Frontend + API Proxy               │
├─────────────────────────────────────────────┤
│                                             │
│  React Frontend          FastAPI Backend   │
│  (Three.js + Vite)      (Python + OpenAI)  │
│                                             │
├─────────────────────────────────────────────┤
│                Redis                        │
│         (Session Storage)                   │
└─────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- 8GB+ RAM recommended
- Ports 80, 8000, 6379 available

### 1. Clone & Setup
```bash
git clone <repository>
cd phisics
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

Add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here  # optional
```

### 3. Start Services

**Linux/Mac:**
```bash
chmod +x scripts/start.sh scripts/stop.sh
./scripts/start.sh
```

**Windows:**
```powershell
.\scripts\start.ps1
```

### 4. Access Application
- **Frontend**: http://localhost
- **API Docs**: http://localhost:8000/docs  
- **Backend API**: http://localhost:8000/api/
- **Health Check**: http://localhost/health

## 🛠️ Development

### Hot Reloading
The development setup includes hot reloading for both frontend and backend:

```bash
# Development mode with code mounting
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build

# Or just use the scripts which include overrides automatically
./scripts/start.sh
```

### Development Tools
Optional development tools can be started with:

```bash
# Start with dev tools (Redis GUI, DB admin)
docker-compose --profile dev-tools up -d

# Access tools:
# - Redis Commander: http://localhost:8081
# - Adminer: http://localhost:8080
```

### Frontend Development
For faster frontend development, you can run Vite dev server locally:

```bash
# Stop frontend container
docker-compose stop frontend

# Run frontend locally
cd frontend
npm install
npm run dev
# Frontend will be available at http://localhost:5173
```

## 📦 Services

### Frontend (Nginx + React)
- **Port**: 80
- **Technology**: React + Vite + Three.js
- **Proxy**: Routes `/api/*` to backend
- **Static Files**: Served with optimized caching

### Backend (FastAPI)
- **Port**: 8000
- **Technology**: Python + FastAPI + OpenAI
- **Features**: 
  - LLM-powered simulation generation
  - Chat-based iteration
  - Session management with Redis
  - Health checks

### Redis
- **Port**: 6379
- **Purpose**: Session storage, chat history
- **Persistence**: Data persisted in Docker volume

## 🔧 Configuration

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | OpenAI API key for LLM features |
| `ANTHROPIC_API_KEY` | - | Anthropic API key (optional) |
| `DATABASE_URL` | `sqlite:///./simulation.db` | Database connection |
| `REDIS_URL` | `redis://redis:6379` | Redis connection |
| `SESSION_TIMEOUT` | `3600` | Session timeout in seconds |
| `MAX_CHAT_HISTORY` | `50` | Max chat messages per session |
| `LOG_LEVEL` | `INFO` | Application log level |

### Nginx Configuration
The Nginx configuration includes:
- Static file serving with optimized caching
- API proxy to FastAPI backend
- CORS headers for API requests
- Security headers
- Rate limiting (100 requests/minute per IP)
- Gzip compression

### Docker Volumes
- `redis_data`: Redis persistence
- `backend_data`: Backend data storage
- `./logs/nginx`: Nginx access/error logs

## 📊 Monitoring & Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis

# Nginx access logs
tail -f logs/nginx/access.log
```

### Health Checks
All services include health checks:
```bash
# Check service status
docker-compose ps

# Manual health checks
curl http://localhost/health          # Frontend
curl http://localhost:8000/api/health # Backend
```

### Resource Usage
```bash
# Container resource usage
docker stats

# System resource usage
docker system df
```

## 🛑 Management

### Stop Services
```bash
# Linux/Mac
./scripts/stop.sh

# Windows
.\scripts\stop.ps1

# Or manually
docker-compose down
```

### Clean Up
```bash
# Stop and remove volumes
docker-compose down -v

# Remove unused images and containers
docker system prune -f

# Remove all project containers and images
docker-compose down --rmi all -v
```

### Update
```bash
# Pull latest images and rebuild
docker-compose pull
docker-compose up --build -d
```

## 🔒 Production Deployment

### Security Recommendations
1. **Environment Variables**: Use Docker secrets or external secret management
2. **SSL/TLS**: Add SSL certificates to Nginx
3. **Firewall**: Restrict access to internal ports (6379, 8000)
4. **Resource Limits**: Add memory/CPU limits to services
5. **Logging**: Configure log rotation and centralized logging

### Production Override
Create `docker-compose.prod.yml`:
```yaml
version: '3.8'
services:
  backend:
    restart: always
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "0.5"
  
  frontend:
    restart: always
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.25"
```

Run with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find process using port
netstat -tulpn | grep :80
# Kill process or change port in docker-compose.yml
```

**Backend Won't Start**
```bash
# Check logs
docker-compose logs backend

# Common causes:
# - Missing .env file
# - Invalid API keys
# - Redis connection issues
```

**Frontend Build Fails**
```bash
# Check if frontend directory has package.json
ls frontend/

# Check Node.js version in container
docker-compose exec frontend node --version
```

**Redis Connection Issues**
```bash
# Test Redis connectivity
docker-compose exec redis redis-cli ping

# Check Redis logs
docker-compose logs redis
```

### Performance Tuning

**Memory Usage**
```bash
# Monitor memory usage
docker stats --no-stream

# Adjust if needed in docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 2G
```

**Build Time**
```bash
# Use build cache
docker-compose build --parallel

# Multi-stage builds already optimized in Dockerfiles
```

## 📖 API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔗 Useful Commands

```bash
# Execute commands in containers
docker-compose exec backend python -c "print('Hello from backend')"
docker-compose exec frontend ls -la

# Access container shell
docker-compose exec backend bash
docker-compose exec redis redis-cli

# Restart specific service
docker-compose restart backend

# View container details
docker-compose ps
docker inspect physics-sim-backend
``` 