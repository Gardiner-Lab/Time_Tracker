@echo off
echo Starting Academic Time Tracker Backend...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed or not running
    echo Please install Docker Desktop and make sure it's running
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Docker Compose is not available
    echo Trying with 'docker compose' command instead...
    docker compose --version >nul 2>&1
    if errorlevel 1 (
        echo Neither 'docker-compose' nor 'docker compose' is available
        pause
        exit /b 1
    )
    set COMPOSE_CMD=docker compose
) else (
    set COMPOSE_CMD=docker-compose
)

REM Create data directory if it doesn't exist
if not exist "data" mkdir data

echo Using command: %COMPOSE_CMD%
echo.

REM Start the backend using Docker Compose
%COMPOSE_CMD% up --build

echo.
echo Backend stopped.
pause