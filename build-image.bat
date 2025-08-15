@echo off
echo === Building Academic Time Tracker Image ===
echo.

echo Building Docker image...
docker build -t academic-time-tracker:latest .

if %errorlevel% equ 0 (
    echo.
    echo ✅ Image built successfully!
    echo 📋 Image: academic-time-tracker:latest
    echo 🚀 You can now use Compose Manager to start the container
    echo.
    echo Next steps:
    echo 1. Go to Compose Manager in Unraid
    echo 2. Add this directory
    echo 3. Click 'Compose Up'
) else (
    echo.
    echo ❌ Build failed!
    pause
    exit /b 1
)

pause