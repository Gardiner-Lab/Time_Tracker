# Academic Time Tracker - Unraid Setup Guide

This guide will help you deploy the Academic Time Tracker backend on Unraid using Docker.

## Method 1: Using Unraid Docker Templates (Recommended)

### Step 1: Create Docker Template
1. Go to **Docker** tab in Unraid WebUI
2. Click **Add Container**
3. Fill in the following settings:

**Basic Settings:**
- **Name**: `academic-time-tracker`
- **Repository**: `academic-time-tracker:latest` (after building locally)
- **Docker Hub URL**: Leave blank (local image)
- **WebUI**: `http://[IP]:[PORT:5000]/`
- **Icon URL**: `https://raw.githubusercontent.com/selfhosters/unRAID-CA-templates/master/templates/img/timetracker.png`

**Network Settings:**
- **Network Type**: `Bridge`
- **Port Mappings**:
  - Container Port: `5000`
  - Host Port: `5000` (or any available port)
  - Protocol: `TCP`

**Volume Mappings:**
- **Container Path**: `/app/data`
- **Host Path**: `/mnt/user/appdata/academic-time-tracker/data`
- **Access Mode**: `Read/Write`

**Environment Variables:**
- **Variable**: `NODE_ENV`
- **Value**: `production`

**Docker Settings:**
- **Privileged**: `No`
- **Console shell command**: `sh`

### Step 2: Build and Deploy
Since this uses a custom Dockerfile, you'll need to build the image first:

1. **Upload files to Unraid**:
   - Copy your project files to `/mnt/user/docker-builds/academic-time-tracker/`
   - Include: `Dockerfile`, `package.json`, `server.js`

2. **Build the image** (via Unraid terminal or SSH):
   ```bash
   cd /mnt/user/docker-builds/academic-time-tracker/
   docker build -t academic-time-tracker:latest .
   ```

3. **Start the container** from the Docker tab

## Method 2: Using Docker Compose on Unraid

### Step 1: Install Docker Compose Plugin
1. Install the **Compose Manager** plugin from Community Applications

### Step 2: Fix Docker Compose Permissions (If Needed)
If you get permission errors, run this in Unraid terminal:
```bash
cd /mnt/user/docker-compose/academic-time-tracker/
chmod +x fix-docker-compose.sh
./fix-docker-compose.sh
```

### Step 3: Build the Image First
**IMPORTANT**: You must build the image before using Compose Manager!

1. Upload all files to: `/mnt/user/docker-compose/academic-time-tracker/`
2. **Build the image** via Unraid terminal:
   ```bash
   cd /mnt/user/docker-compose/academic-time-tracker/
   chmod +x build-image.sh
   ./build-image.sh
   ```

### Step 4: Deploy with Compose Manager
1. Go to **Compose Manager** plugin
2. Add the compose file location: `/mnt/user/docker-compose/academic-time-tracker/`
3. Click **Compose Up**

### Alternative: Direct Deployment (Recommended)
If Compose Manager keeps having issues, use the direct deployment script:
```bash
cd /mnt/user/docker-compose/academic-time-tracker/
chmod +x deploy-unraid.sh
./deploy-unraid.sh
```

This bypasses Docker Compose entirely and is more reliable on Unraid.

## Method 3: Manual Docker Run Command

If you prefer command line, use this docker run command:

```bash
# Build the image first
cd /mnt/user/docker-builds/academic-time-tracker/
docker build -t academic-time-tracker:latest .

# Run the container
docker run -d \
  --name academic-time-tracker \
  --restart unless-stopped \
  -p 5000:5000 \
  -v /mnt/user/appdata/academic-time-tracker/data:/app/data \
  -e NODE_ENV=production \
  academic-time-tracker:latest
```

## Accessing the Application

### From Unraid Network:
- Backend API: `http://UNRAID-IP:5000`
- Test endpoint: `http://UNRAID-IP:5000/groups`

### From Other Devices:
Update the frontend (`app.py`) to point to your Unraid server:
```python
BASE_URL = "http://YOUR-UNRAID-IP:5000"
```

## Data Persistence

- Database location: `/mnt/user/appdata/academic-time-tracker/data/database.db`
- Backups will be stored in the same directory
- Data persists across container updates and reboots

## Updating the Application

1. **Stop the container**
2. **Rebuild the image** with new code:
   ```bash
   cd /mnt/user/docker-builds/academic-time-tracker/
   docker build -t academic-time-tracker:latest .
   ```
3. **Start the container** again

## Troubleshooting

### Docker Compose Permission Issues
If you get `permission denied` errors with Docker Compose:

```bash
# Fix Docker Compose permissions
chmod +x /root/.docker/cli-plugins/docker-compose

# Or run the fix script
chmod +x fix-docker-compose.sh
./fix-docker-compose.sh
```

### Alternative: Skip Compose Manager Entirely
If Compose Manager keeps having issues, use the direct deployment script:

```bash
chmod +x deploy-unraid.sh
./deploy-unraid.sh
```

This bypasses Docker Compose entirely and uses direct Docker commands.

### Container Won't Start:
- Check logs: `docker logs academic-time-tracker`
- Ensure port 5000 isn't used by another container
- Verify file permissions on appdata directory
- Try the direct deployment script above

### Can't Connect from Frontend:
- Update `BASE_URL` in `app.py` to use Unraid IP: `http://YOUR-UNRAID-IP:5000`
- Check Unraid firewall settings
- Ensure container is running: `docker ps | grep academic-time-tracker`

### Database Issues:
- Check `/mnt/user/appdata/academic-time-tracker/data/` permissions
- Ensure sufficient disk space on array
- Verify the data directory is properly mounted

## Security Considerations

- **Internal Use**: This setup is designed for internal network use
- **Reverse Proxy**: Consider using nginx proxy manager for external access
- **Firewall**: Configure Unraid firewall rules as needed
- **Backups**: Regular backups of the appdata directory are recommended

## Performance Tips

- **SSD Cache**: Store appdata on SSD cache for better performance
- **Resource Limits**: Set CPU/Memory limits if needed in advanced container settings
- **Monitoring**: Use Unraid monitoring tools to track container resource usage