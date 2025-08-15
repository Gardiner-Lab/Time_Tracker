#!/bin/bash

# Complete deployment script for Unraid
# This handles all the common issues and deploys the container

set -e

echo "=== Academic Time Tracker - Unraid Deployment ==="
echo

# Configuration
IMAGE_NAME="academic-time-tracker"
IMAGE_TAG="latest"
CONTAINER_NAME="academic-time-tracker"
APPDATA_DIR="/mnt/user/appdata/academic-time-tracker"

# Check if we're on Unraid
if [ ! -d "/mnt/user" ]; then
    echo "⚠️  Warning: This doesn't appear to be an Unraid system"
    echo "Continuing anyway..."
fi

# Create appdata directory
echo "📁 Creating appdata directory..."
mkdir -p "$APPDATA_DIR/data"
chmod 755 "$APPDATA_DIR"
chmod 755 "$APPDATA_DIR/data"

# Stop and remove existing container if it exists
echo "🛑 Stopping existing container (if any)..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

# Build the image
echo "🔨 Building Docker image..."
docker build -t "$IMAGE_NAME:$IMAGE_TAG" .

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

# Run the container using direct docker command (bypassing compose issues)
echo "🚀 Starting container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p 5000:5000 \
    -v "$APPDATA_DIR/data:/app/data" \
    -e NODE_ENV=production \
    "$IMAGE_NAME:$IMAGE_TAG"

# Wait a moment for container to start
sleep 3

# Check if container is running
if docker ps | grep -q "$CONTAINER_NAME"; then
    echo "✅ Container started successfully!"
    
    # Get Unraid IP
    UNRAID_IP=$(hostname -I | awk '{print $1}')
    
    echo
    echo "=== Deployment Complete ==="
    echo "📋 Container: $CONTAINER_NAME"
    echo "🌐 Access: http://$UNRAID_IP:5000"
    echo "📊 Test API: http://$UNRAID_IP:5000/groups"
    echo "💾 Data: $APPDATA_DIR/data"
    echo
    echo "📝 Logs: docker logs $CONTAINER_NAME"
    echo "🛑 Stop: docker stop $CONTAINER_NAME"
    echo
    echo "🎯 Next Steps:"
    echo "1. Update your frontend app.py with: BASE_URL = \"http://$UNRAID_IP:5000\""
    echo "2. Run the Python frontend on your local machine"
    
else
    echo "❌ Container failed to start!"
    echo "Checking logs..."
    docker logs "$CONTAINER_NAME"
    exit 1
fi