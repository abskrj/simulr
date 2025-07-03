#!/bin/bash

# Physics Simulation Dashboard - Startup Script

set -e

echo "🚀 Starting Physics Simulation Dashboard..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    echo "# API Keys for LLM Services" > .env
    echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
    echo "ANTHROPIC_API_KEY=your_anthropic_api_key_here" >> .env
    echo "" >> .env
    echo "# Database Configuration" >> .env
    echo "DATABASE_URL=sqlite:///./simulation.db" >> .env
    echo "REDIS_URL=redis://redis:6379" >> .env
    echo "" >> .env
    echo "# Application Settings" >> .env
    echo "LOG_LEVEL=INFO" >> .env
    echo "SESSION_TIMEOUT=3600" >> .env
    echo "MAX_CHAT_HISTORY=50" >> .env
    echo "" >> .env
    echo "📝 Please edit .env file with your API keys before running again."
    exit 0
fi

# Create logs directory
mkdir -p logs/nginx

# Start services
echo "🐳 Building and starting containers..."
docker-compose up --build -d

echo "⏳ Waiting for services to be healthy..."

# Wait for backend health check
echo "Waiting for backend..."
timeout 60 bash -c 'until docker-compose exec backend curl -f http://localhost:8000/api/health > /dev/null 2>&1; do sleep 2; done' || {
    echo "❌ Backend failed to start properly"
    docker-compose logs backend
    exit 1
}

# Wait for frontend
echo "Waiting for frontend..."
timeout 30 bash -c 'until curl -f http://localhost/health > /dev/null 2>&1; do sleep 2; done' || {
    echo "❌ Frontend failed to start properly"
    docker-compose logs frontend
    exit 1
}

echo "✅ All services are running!"
echo ""
echo "🌐 Application URLs:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Redis: redis://localhost:6379"
echo ""
echo "📊 Monitoring:"
echo "   Docker logs: docker-compose logs -f"
echo "   Backend logs: docker-compose logs -f backend"
echo "   Frontend logs: docker-compose logs -f frontend"
echo ""
echo "🛑 To stop: ./scripts/stop.sh" 