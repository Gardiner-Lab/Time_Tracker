#!/bin/bash

echo "=== Fixing Docker Compose Permissions on Unraid ==="
echo

# Fix Docker Compose plugin permissions
if [ -f "/root/.docker/cli-plugins/docker-compose" ]; then
    echo "Found Docker Compose plugin, fixing permissions..."
    chmod +x /root/.docker/cli-plugins/docker-compose
    echo "✅ Permissions fixed!"
else
    echo "Docker Compose plugin not found. Installing..."
    
    # Create directory if it doesn't exist
    mkdir -p /root/.docker/cli-plugins
    
    # Download Docker Compose
    COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    echo "Downloading Docker Compose $COMPOSE_VERSION..."
    
    curl -L "https://github.com/docker/compose/releases/download/$COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /root/.docker/cli-plugins/docker-compose
    
    # Make it executable
    chmod +x /root/.docker/cli-plugins/docker-compose
    
    echo "✅ Docker Compose installed and configured!"
fi

# Test Docker Compose
echo
echo "Testing Docker Compose..."
docker compose version

if [ $? -eq 0 ]; then
    echo "✅ Docker Compose is working!"
else
    echo "❌ Docker Compose still has issues. Trying alternative approach..."
    
    # Try installing to /usr/local/bin instead
    curl -L "https://github.com/docker/compose/releases/download/$COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    echo "Installed to /usr/local/bin/docker-compose"
    /usr/local/bin/docker-compose version
fi

echo
echo "=== Fix Complete ==="