@echo off
echo Stopping Academic Time Tracker Backend...
echo.

REM Try Docker Compose first
docker-compose down 2>nul
if not errorlevel 1 (
    echo Backend stopped via Docker Compose
    goto :end
)

REM Try newer Docker Compose syntax
docker compose down 2>nul
if not errorlevel 1 (
    echo Backend stopped via Docker Compose
    goto :end
)

REM Try direct Docker command
docker stop academic-time-tracker-backend 2>nul
if not errorlevel 1 (
    echo Backend stopped via Docker
    docker rm academic-time-tracker-backend 2>nul
    goto :end
)

echo No running backend containers found

:end
echo.
pause