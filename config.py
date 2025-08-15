"""
Academic Time Tracker Configuration
Edit this file to change the backend server URL
"""

# Backend server configuration
# Change this to match your backend server location
BACKEND_URL = "http://192.168.2.19:5000"

# Alternative configurations (uncomment the one you want to use):
# BACKEND_URL = "http://localhost:5000"  # Local development
# BACKEND_URL = "http://your-unraid-ip:5000"  # Replace with your Unraid IP
# BACKEND_URL = "http://192.168.1.100:5000"  # Example different IP

# Connection timeout in seconds
CONNECTION_TIMEOUT = 3

# Show backend connection warnings
SHOW_BACKEND_WARNINGS = True