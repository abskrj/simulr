# Physics Simulation Dashboard - Windows Stop Script

Write-Host "🛑 Stopping Physics Simulation Dashboard..." -ForegroundColor Yellow

# Stop all services
docker-compose down

Write-Host "✅ All services stopped." -ForegroundColor Green
Write-Host ""
Write-Host "🔄 To restart: .\scripts\start.ps1" -ForegroundColor Cyan
Write-Host "🗑️  To remove volumes: docker-compose down -v" -ForegroundColor Yellow
Write-Host "🧹 To clean up images: docker system prune" -ForegroundColor Yellow 