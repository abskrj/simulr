# Physics Simulation Dashboard - Windows Startup Script

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Physics Simulation Dashboard..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  No .env file found. Creating from template..." -ForegroundColor Yellow
    
    $envContent = @"
# API Keys for LLM Services
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./simulation.db
REDIS_URL=redis://redis:6379

# Application Settings
LOG_LEVEL=INFO
SESSION_TIMEOUT=3600
MAX_CHAT_HISTORY=50
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "📝 Please edit .env file with your API keys before running again." -ForegroundColor Yellow
    exit 0
}

# Create logs directory
if (-not (Test-Path "logs/nginx")) {
    New-Item -ItemType Directory -Path "logs/nginx" -Force | Out-Null
}

# Start services
Write-Host "🐳 Building and starting containers..." -ForegroundColor Blue
docker-compose up --build -d

Write-Host "⏳ Waiting for services to be healthy..." -ForegroundColor Yellow

# Wait for backend health check
Write-Host "Waiting for backend..."
$timeout = 60
$elapsed = 0
do {
    Start-Sleep 2
    $elapsed += 2
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) { break }
    } catch {
        # Continue waiting
    }
} while ($elapsed -lt $timeout)

if ($elapsed -ge $timeout) {
    Write-Host "❌ Backend failed to start properly" -ForegroundColor Red
    docker-compose logs backend
    exit 1
}

# Wait for frontend
Write-Host "Waiting for frontend..."
$timeout = 30
$elapsed = 0
do {
    Start-Sleep 2
    $elapsed += 2
    try {
        $response = Invoke-WebRequest -Uri "http://localhost/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) { break }
    } catch {
        # Continue waiting
    }
} while ($elapsed -lt $timeout)

if ($elapsed -ge $timeout) {
    Write-Host "❌ Frontend failed to start properly" -ForegroundColor Red
    docker-compose logs frontend
    exit 1
}

Write-Host "✅ All services are running!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Application URLs:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost"
Write-Host "   Backend API: http://localhost:8000"
Write-Host "   API Docs: http://localhost:8000/docs"
Write-Host "   Redis: redis://localhost:6379"
Write-Host ""
Write-Host "📊 Monitoring:" -ForegroundColor Cyan
Write-Host "   Docker logs: docker-compose logs -f"
Write-Host "   Backend logs: docker-compose logs -f backend"
Write-Host "   Frontend logs: docker-compose logs -f frontend"
Write-Host ""
Write-Host "🛑 To stop: .\scripts\stop.ps1" -ForegroundColor Yellow 