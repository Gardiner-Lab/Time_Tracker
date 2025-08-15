# Academic Time Tracker - File Guide

## 🚀 **For End Users (Just want to use the app)**

**Required**: 
- `Academic Time Tracker.exe` - **Just double-click this to run the app!**

That's it! The executable is completely standalone and connects to the Unraid backend automatically.

---

## 🔧 **For Developers (Want to modify the code)**

**Core Application**:
- `app.py` - Main Python application code
- `config.py` - Configuration file (backend URL, etc.)

**To run from source**:
```bash
pip install requests matplotlib
python app.py
```

---

## 🐳 **For Backend Deployment (Unraid/Docker)**

**Docker Files**:
- `Dockerfile` - Container definition
- `docker-compose.yml` - Easy deployment
- `server.js` - Node.js backend server
- `package.json` - Node.js dependencies

**Unraid Specific**:
- `unraid-setup.md` - Complete Unraid deployment guide
- `unraid-template.xml` - Direct import template
- `deploy-unraid.sh` - Automated deployment script
- `build-for-unraid.sh` - Build script for Unraid
- `fix-docker-compose.sh` - Fix Docker Compose permissions

**Local Backend Development**:
- `run-backend.bat` - Start backend with Docker Compose
- `run-backend-docker.bat` - Start backend with direct Docker
- `stop-backend.bat` - Stop backend containers
- `build-image.bat` / `build-image.sh` - Build Docker images

**Other**:
- `.dockerignore` - Docker build exclusions
- `azure.tcl` - UI theme file
- `LICENSE` - MIT license
- `README.md` - Main documentation

---

## 📁 **File Organization**

```
Academic Time Tracker/
├── Academic Time Tracker.exe    ← **MAIN APP - Just run this!**
├── app.py                       ← Python source code
├── config.py                    ← Configuration
├── server.js                    ← Backend server
├── README.md                    ← Documentation
└── [Docker/Unraid files]        ← For backend deployment
```

**For most users**: You only need `Academic Time Tracker.exe`!