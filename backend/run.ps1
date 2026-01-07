# Startup script for the Interactive Web Novels Backend
Write-Host "Starting Interactive Web Novels Backend..." -ForegroundColor Green

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Start the server
Write-Host "Server starting at http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs available at http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000

