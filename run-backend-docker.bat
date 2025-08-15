@echo off
echo Starting Academic Time Tracker Backend (Direct Docker)...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed or not running
    echo Please install Docker Desktop and make sure it's running
    pause
    exit /b 1
)

REM Create data directory if it doesn't exist
if not exist "data" mkdir data

REM Stop and remove existing container if it exists
docker stop academic-time-tracker-backend 2>nul
docker rm academic-time-tracker-backend 2>nul

echo Building Docker image...
docker build -t academic-time-tracker-backend .

if errorlevel 1 (
    echo Failed to build Docker image
    pause
    exit /b 1
)

echo Starting container...
docker run -d ^
  --name academic-time-tracker-backend ^
  -p 5000:5000 ^
  -v "%cd%\data:/app/data" ^
  -e NODE_ENV=production ^
  academic-time-tracker-backend

if errorlevel 1 (
    echo Failed to start container
    pause
    exit /b 1
)

echo Backend started successfully!
echo Container name: academic-time-tracker-backend
echo Port: 5000
echo.
echo To view logs: docker logs -f academic-time-tracker-backend
echo To stop: docker stop academic-time-tracker-backend
echo.
pause