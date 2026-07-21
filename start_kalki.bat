@echo off
title KALKI AI — IOS Bootstrap Launcher
echo =====================================================================
echo           KALKI AI — Master IOS Bootstrap Launcher (v1.5.0)
echo =====================================================================
echo.

:: Check Python
echo [*] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python 3.11+.
    goto end
)
echo [OK] Python is installed.

:: Check Node.js
echo [*] Checking Node.js installation...
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH. Please install Node.js 18+.
    goto end
)
echo [OK] Node.js is installed.

:: Install Backend Requirements
echo.
echo [*] Setting up Backend Python environment...
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Some python libraries failed to install. Falling back to native system test.
)
cd ..

:: Install Frontend Node Modules
echo.
echo [*] Setting up Frontend Node modules...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install frontend npm packages.
    cd ..
    goto end
)
cd ..

:: Launch Servers in New Windows
echo.
echo =====================================================================
echo [SUCCESS] Configuration completed! Launching KALKI AI services...
echo =====================================================================
echo.
echo [*] Starting FastAPI Backend on http://localhost:8000
start cmd /k "title KALKI Backend Server && cd backend && set PYTHONPATH=. && python -m app.main"

echo [*] Starting Next.js Frontend on http://localhost:3000
start cmd /k "title KALKI Frontend Web App && cd frontend && npm run dev"

echo.
echo All services launched! 
echo - Web Dashboard: http://localhost:3000
echo - Swagger API Specs: http://localhost:8000/docs
echo.

:end
pause
