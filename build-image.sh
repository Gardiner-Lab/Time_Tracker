#!/bin/bash

# Build script for Unraid - Run this BEFORE using Compose Manager
echo "=== Building Academic Time Tracker Image ==="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build the image
echo "Building Docker image..."
cd "$SCRIPT_DIR"
docker build -t academic-time-tracker:latest .

if [ $? -eq 0 ]; then
    echo "✅ Image built successfully!"
    echo "📋 Image: academic-time-tracker:latest"
    echo "🚀 You can now use Compose Manager to start the container"
    echo ""
    echo "Next steps:"
    echo "1. Go to Compose Manager in Unraid"
    echo "2. Add this directory: $(pwd)"
    echo "3. Click 'Compose Up'"
else
    echo "❌ Build failed!"
    exit 1
fi