# Academic Time Tracker

A productivity application for students and academics to track time spent on tasks and projects, with visualization tools and academic period management.

## Features
- 🕒 Time tracking with session notes
- 📚 Task organization by groups/projects
- 📊 Time distribution visualization (by group/task)
- 🗓️ Academic period management (semesters/quarters)
- 📦 Database backup/restore
- 📝 CSV data export
- 🎨 Modern dark theme UI
- ⌨️ Keyboard shortcuts (Space to start/stop timer)

## Quick Start Guide

### Prerequisites
- Docker and Docker Compose
- Python (3.8+)
- Required Python packages: `requests`, `matplotlib`, `tkinter`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/academic-time-tracker.git
   cd academic-time-tracker
   ```

2. Install frontend dependencies:
   ```bash
   pip install requests matplotlib
   ```

### Running the Application

#### Option 1: Using Batch Files (Windows)
1. **Start the backend**: Double-click `run-backend.bat`
2. **Start the frontend**: Double-click `run-frontend.bat`

#### Option 2: Manual Commands
1. **Start the backend server** (in terminal 1):
   ```bash
   docker-compose up --build
   ```

2. **Start the frontend GUI** (in terminal 2):
   ```bash
   python app.py
   ```

### Architecture
- **Backend**: Node.js server running in Docker container on port 5000
- **Frontend**: Python Tkinter GUI running locally
- **Database**: SQLite database persisted in `./data/` directory

## Basic Usage
1. **Create Groups**  
   (e.g., "Research", "Coursework", "Thesis")
2. **Add Tasks** to groups  
   (e.g., "Literature Review", "Problem Set 3")
3. **Track Time**:
   - Select a task
   - Click START (or press Space)
   - Work on your task
   - Click STOP (or press Space) and add notes
4. **Analyze Data**:
   - View time distribution charts
   - Filter by academic periods
   - See weekly/hourly breakdowns

## Database Management
- **Backup**: File → Backup Database
- **Restore**: File → Restore Database
- **Export**: File → Export CSV (for external analysis)

## Academic Periods
Create custom time periods (semesters/quarters) through Period Manager:
- Access via Period Manager → Manage Periods
- Define start/end dates
- View time distribution within specific periods

## Keyboard Shortcuts
- **Space**: Start/stop timer
- **Ctrl+Q**: Quit application (Windows/Linux)
- **Cmd+Q**: Quit application (MacOS)

## Troubleshooting

### Frontend Issues
- If charts don't update, try reselecting a group
- Restart both processes if the GUI can't connect to the backend
- Ensure no other service is using port 5000

### Docker Issues
- **"docker build requires exactly 1 argument"**: Try using `run-backend-docker.bat` instead
- **Docker Compose not found**: Use `run-backend-docker.bat` for direct Docker commands
- **Permission denied**: Make sure Docker Desktop is running
- **Port 5000 in use**: Stop other services using port 5000 or change the port in docker-compose.yml
- **Build fails**: Check that all files (Dockerfile, package.json, server.js) are present

### Alternative Startup Methods
1. **Docker Compose**: `run-backend.bat` (recommended)
2. **Direct Docker**: `run-backend-docker.bat` (if Compose fails)
3. **Manual**: See Docker Commands section below

## Docker Setup

The backend runs in a Docker container while the frontend runs locally. This provides:
- **Isolation**: Backend dependencies are containerized
- **Consistency**: Same backend environment across different machines  
- **Persistence**: Database is stored in `./data/` directory on host
- **Easy deployment**: Backend can be easily deployed to any Docker-compatible environment

### Docker Commands
```bash
# Build and start backend
docker-compose up --build

# Start backend in background
docker-compose up -d

# Stop backend
docker-compose down

# View backend logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up --build
```

### Data Persistence
- Database file: `./data/database.db`
- Backups are stored locally and persist across container restarts
- To reset data, delete the `./data/` directory