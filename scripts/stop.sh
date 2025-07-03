#!/bin/bash

# Physics Simulation Dashboard - Stop Script

echo "🛑 Stopping Physics Simulation Dashboard..."

# Stop all services
docker-compose down

echo "✅ All services stopped."
echo ""
echo "🔄 To restart: ./scripts/start.sh"
echo "🗑️  To remove volumes: docker-compose down -v"
echo "🧹 To clean up images: docker system prune" 