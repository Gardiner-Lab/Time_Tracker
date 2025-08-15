#!/bin/bash

# Academic Time Tracker - Unraid Build Script
# This script helps build and deploy the container on Unraid

set -e

echo "=== Academic Time Tracker - Unraid Build Script ==="
echo

# Configuration
IMAGE_NAME="academic-time-tracker"
IMAGE_TAG="latest"
BUILD_DIR="/mnt/user/docker-builds/academic-time-tracker"
APPDATA_DIR="/mnt/user/appdata/academic-time-tracker"

# Check if running on Unraid
if [ ! -d "/mnt/user" ]; then
    echo "Warning: This script is designed for Unraid systems"
    echo "Continuing anyway..."
fi

# Create directories
echo "Creating directories..."
mkdir -p "$BUILD_DIR"
mkdir -p "$APPDATA_DIR/data"

# Copy files to build directory
echo "Copying files to build directory..."
cp Dockerfile "$BUILD_DIR/"
cp package.json "$BUILD_DIR/"
cp server.js "$BUILD_DIR/"

# Build the Docker image
echo "Building Docker image..."
cd "$BUILD_DIR"
docker build -t "$IMAGE_NAME:$IMAGE_TAG" .

# Check if container is already running
if docker ps -q -f name="$IMAGE_NAME" | grep -q .; then
    echo "Stopping existing container..."
    docker stop "$IMAGE_NAME"
    docker rm "$IMAGE_NAME"
fi

# Run the container
echo "Starting container..."
docker run -d \
    --name "$IMAGE_NAME" \
    --restart unless-stopped \
    -p 5000:5000 \
    -v "$APPDATA_DIR/data:/app/data" \
    -e NODE_ENV=production \
    "$IMAGE_NAME:$IMAGE_TAG"

echo
echo "=== Deployment Complete ==="
echo "Container: $IMAGE_NAME"
echo "Status: $(docker ps --format 'table {{.Status}}' -f name=$IMAGE_NAME | tail -n 1)"
echo "Access: http://$(hostname -I | awk '{print $1}'):5000"
echo "Data: $APPDATA_DIR/data"
echo
echo "To check logs: docker logs $IMAGE_NAME"
echo "To stop: docker stop $IMAGE_NAME"
echo