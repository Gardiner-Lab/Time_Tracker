@echo off
echo Starting Academic Time Tracker Frontend...
echo.
echo Make sure the backend is running first!
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ and required packages:
    echo pip install requests matplotlib
    pause
    exit /b 1
)

REM Start the frontend
python app.py

echo.
echo Frontend stopped.
pause