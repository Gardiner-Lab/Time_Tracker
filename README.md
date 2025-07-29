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
- Node.js (v14+)
- Python (3.8+)
- Required Python packages: `requests`, `matplotlib`, `tkinter`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/academic-time-tracker.git
   cd academic-time-tracker
   ```

2. Install backend dependencies:
   ```bash
   npm install express sqlite3 body-parser
   ```

3. Install frontend dependencies:
   ```bash
   pip install requests matplotlib
   ```

### Running the Application
1. Start the backend server (in terminal 1):
   ```bash
   node server.js
   ```

2. Start the frontend GUI (in terminal 2):
   ```bash
   python app.py
   ```

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
- If charts don't update, try reselecting a group
- Restart both processes if the GUI can't connect to the backend
- Ensure no other service is using port 5000
