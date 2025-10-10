# Campus Event System - Quick Start Scripts

## 🚀 Running the Application

### Start Everything
To start both backend and frontend with a single command:

```bash
./run.sh
```

This will:
1. ✅ Stop any existing instances
2. ✅ Start the Spring Boot backend on port 8080
3. ✅ Wait for backend to be ready
4. ✅ Start the Tkinter frontend GUI
5. ✅ Display status and log file locations

### Stop Everything
To stop both backend and frontend:

```bash
./stop.sh
```

This will gracefully stop both services.

## 📋 What the Scripts Do

### `run.sh`
- **Stops existing processes** to avoid conflicts
- **Starts backend** (Spring Boot on port 8080)
  - Uses Maven Wrapper (`./mvnw`) if available
  - Falls back to system Maven if installed
  - Waits for backend to initialize (up to 60 seconds)
  - Checks health endpoint to confirm backend is ready
- **Starts frontend** (Python Tkinter GUI)
  - Uses Python 3.11 if available, otherwise Python 3
  - Launches GUI application
- **Logs output** to `backend.log` and `frontend.log`
- **Saves PIDs** for the stop script

### `stop.sh`
- **Stops frontend** (Python GUI)
- **Stops backend** (Spring Boot)
- **Cleans up PID files**
- **Graceful shutdown** with fallback to force kill if needed

## 📄 Log Files

Both scripts create log files in the project root:

- `backend.log` - Backend (Spring Boot) output
- `frontend.log` - Frontend (Tkinter) output

View logs in real-time:

```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log
```

## 🔍 Checking Status

### Backend
```bash
# Check if backend is running
curl http://localhost:8080/actuator/health

# Or visit in browser
open http://localhost:8080
```

### Frontend
The GUI application will open automatically. If it doesn't appear:

```bash
# Check if process is running
ps aux | grep "python.*main.py"

# Check logs for errors
cat frontend.log
```

## 🛠️ Troubleshooting

### Backend won't start

**Problem:** Maven not found
```bash
# Solution: Install Maven
brew install maven

# Or use Maven Wrapper (already in project)
cd backend_java/backend
chmod +x mvnw
```

**Problem:** Port 8080 already in use
```bash
# Find process using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>
```

### Frontend won't start

**Problem:** Python not found
```bash
# Solution: Install Python 3.11
brew install python@3.11

# Or use Python 3
python3 --version
```

**Problem:** Missing dependencies
```bash
# Solution: Install requirements
cd frontend_tkinter
pip3 install -r requirements.txt
```

**Problem:** Tkinter not available
```bash
# Solution: Install tkinter
brew install python-tk@3.11
```

### Scripts won't execute

**Problem:** Permission denied
```bash
# Solution: Make scripts executable
chmod +x run.sh stop.sh
```

## 📦 Manual Startup (Alternative)

If you prefer to start services manually:

### Start Backend
```bash
cd backend_java/backend
./mvnw spring-boot:run
# or
mvn spring-boot:run
```

### Start Frontend
```bash
cd frontend_tkinter
python3.11 main.py
# or
python3 main.py
```

### Stop Services
```bash
# Stop frontend
pkill -f "python.*main.py"

# Stop backend
pkill -f "spring-boot:run"
```

## 🎯 Best Practices

1. **Always use `./run.sh`** to start the system
   - Ensures clean startup
   - Stops old processes
   - Checks for errors

2. **Check logs** if something doesn't work
   - `backend.log` for backend issues
   - `frontend.log` for frontend issues

3. **Use `./stop.sh`** to stop cleanly
   - Prevents resource leaks
   - Ensures proper shutdown

4. **Wait for backend** before using frontend
   - The script waits automatically
   - Backend needs ~10-20 seconds to start

## 📍 URLs & Ports

| Service | URL | Port |
|---------|-----|------|
| Backend API | http://localhost:8080 | 8080 |
| Frontend GUI | Desktop Application | N/A |
| Backend Health | http://localhost:8080/actuator/health | 8080 |

## 🔄 Development Workflow

```bash
# Morning - Start everything
./run.sh

# During development - restart after changes
./stop.sh
./run.sh

# Evening - Stop everything
./stop.sh
```

## 💡 Tips

- The scripts are **colorized** for easy reading
- Log files are **automatically created** and rotated
- PIDs are **tracked** for clean shutdown
- Health checks ensure backend is **fully ready** before continuing
- Both services can run in the **background**

## 🆘 Need Help?

If you encounter issues:

1. Check the log files: `backend.log` and `frontend.log`
2. Ensure all dependencies are installed
3. Verify ports 8080 is available
4. Try manual startup to identify the issue
5. Check the troubleshooting section above

---

**Happy Coding! 🚀**
