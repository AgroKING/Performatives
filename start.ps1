# Quick Start Script for Windows
# Run this to start the entire platform

Write-Host "🚀 Starting Performatives Platform..." -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
$dockerRunning = docker info 2>$null
if (-not $dockerRunning) {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Docker is running" -ForegroundColor Green
Write-Host ""

# Build services
Write-Host "📦 Building services..." -ForegroundColor Yellow
docker-compose build

# Start services
Write-Host ""
Write-Host "🎬 Starting all services..." -ForegroundColor Yellow
docker-compose up -d

# Wait a bit for services to start
Write-Host ""
Write-Host "⏳ Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check status
Write-Host ""
Write-Host "📊 Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "✅ Platform is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access the platform at:" -ForegroundColor Cyan
Write-Host "   http://localhost" -ForegroundColor White
Write-Host ""
Write-Host "📚 Individual Services:" -ForegroundColor Cyan
Write-Host "   Job Discovery:    http://localhost/jobs" -ForegroundColor White
Write-Host "   Job Matching:     http://localhost/problem-1/index.html" -ForegroundColor White
Write-Host "   ATS Dashboard:    http://localhost/prob-4/frontend/index.html" -ForegroundColor White
Write-Host "   Skill Analyzer:   http://localhost/skills" -ForegroundColor White
Write-Host ""
Write-Host "📖 API Documentation:" -ForegroundColor Cyan
Write-Host "   Job Matching API: http://localhost/api/match/docs" -ForegroundColor White
Write-Host "   ATS API:          http://localhost/api/ats/docs" -ForegroundColor White
Write-Host ""
Write-Host "To stop the platform, run:" -ForegroundColor Yellow
Write-Host "   docker-compose down" -ForegroundColor White
Write-Host ""
