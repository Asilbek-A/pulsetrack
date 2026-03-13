# PowerShell script for Windows - Git repository setup and deployment preparation

Write-Host "🚀 PulseTrack Deployment Preparation" -ForegroundColor Green
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found! Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "render.yaml")) {
    Write-Host "❌ render.yaml not found! Please run this script from the project root." -ForegroundColor Red
    exit 1
}

Write-Host "✅ render.yaml found" -ForegroundColor Green
Write-Host ""

# Check if git repository exists
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Create a GitHub repository (public)" -ForegroundColor White
Write-Host "2. Run these commands:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Yellow
Write-Host "   git commit -m 'Ready for Render deployment'" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/pulsetrack.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Go to https://render.com and deploy using Blueprint" -ForegroundColor White
Write-Host ""
