# 🎯 SUPER SIMPLE START GUIDE

## TL;DR (Too Long; Didn't Read)

**To run EVERYTHING (Backend + Frontend):**
```bash
./run.sh
```

**To stop EVERYTHING:**
```bash
./stop.sh
```

That's it! You're done! 🎉

---

## 🤔 But What's Actually Happening?

Let me explain in simple terms:

### Your Application Has 2 Parts:

1. **Backend** (Java) - The "brain" that handles data, users, events
2. **Frontend** (Python) - The "face" that you see and click on

They need to talk to each other, so you need to run BOTH.

---

## 📚 Understanding the Different Ways to Run

You saw many different ways to start things. Here's what they all mean:

### 1️⃣ **`./run.sh`** ⭐ **BEST & EASIEST**

```bash
./run.sh
```

**What it does:**
- ✅ Starts BOTH backend AND frontend automatically
- ✅ Stops old running versions first (no conflicts)
- ✅ Waits for backend to be ready before starting frontend
- ✅ Creates log files so you can see what's happening

**When to use:** ALWAYS! This is the easiest way.

---

### 2️⃣ **Maven (`mvn`) Commands** - Backend Only

```bash
cd backend_java/backend
mvn spring-boot:run
```

**What it does:**
- ⚙️ Starts ONLY the backend (Java Spring Boot)
- ⚙️ Runs on http://localhost:8080

**When to use:** 
- When you only want to test the backend
- When you want to start backend and frontend separately

**Why Maven?**
- Maven is a tool that builds and runs Java projects
- Think of it like `npm` for Node.js or `pip` for Python

---

### 3️⃣ **Java JAR Command** - Backend Only (Alternative)

```bash
cd backend_java/backend
java -jar target/backend-0.0.1-SNAPSHOT.jar
```

**What it does:**
- ⚙️ Starts ONLY the backend from a pre-built file
- ⚙️ Faster than Maven, but you need to build it first

**When to use:**
- When you've already built the project
- For production/deployment
- If you want faster startup

**How to build the JAR first:**
```bash
cd backend_java/backend
mvn clean package
```

---

### 4️⃣ **Frontend Python Command** - Frontend Only

```bash
cd frontend_tkinter
python3 main.py
```

**What it does:**
- 🖥️ Starts ONLY the frontend (Python GUI)
- 🖥️ Opens a window you can click

**When to use:**
- When backend is already running
- When you only want to test the UI

---
cd /Users/garinesaiajay/Desktop/CampusEventSystem
PYTHONPATH=$(pwd) /opt/homebrew/bin/python3.11 frontend_tkinter/main.py
to restart the frontend

### 5️⃣ **`START_APP.sh`** - Alternative Startup

```bash
./START_APP.sh
```

**What it does:**
- Similar to `run.sh` but with more guidance
- Shows you options if auto-start fails
- Has built-in troubleshooting help

**When to use:**
- If `run.sh` isn't working
- If you want more explanations

---

## 🎓 Simple Scenarios

### Scenario 1: "I just want to use the app"
```bash
./run.sh
```
Done! Both backend and frontend will start.

---

### Scenario 2: "I'm working on backend code only"
```bash
# Terminal 1 - Backend only
cd backend_java/backend
mvn spring-boot:run

# Wait for it to start, then test:
curl http://localhost:8080/actuator/health
```

---

### Scenario 3: "I'm working on frontend code only"
```bash
# Terminal 1 - Backend (let it run)
cd backend_java/backend
mvn spring-boot:run

# Terminal 2 - Frontend (restart this when you make changes)
cd frontend_tkinter
python3 main.py
```

---

### Scenario 4: "I want to see both separately"
```bash
# Terminal 1 - Backend
cd backend_java/backend
mvn spring-boot:run

# Terminal 2 - Frontend (after backend is ready)
cd frontend_tkinter
python3 main.py
```

---

## 🛑 How to Stop

### Stop Everything
```bash
./stop.sh
```

### Stop Manually

**Stop Backend:**
```bash
# Find and kill Java process
pkill -f "spring-boot:run"

# OR press Ctrl+C in the terminal running backend
```

**Stop Frontend:**
```bash
# Find and kill Python process
pkill -f "python.*main.py"

# OR just close the GUI window
# OR press Ctrl+C in the terminal running frontend
```

---

## 📊 Quick Reference Table

| What You Want | Command | What Starts |
|---------------|---------|-------------|
| Everything (easiest) | `./run.sh` | Backend + Frontend |
| Stop everything | `./stop.sh` | Stops both |
| Backend only (Maven) | `cd backend_java/backend && mvn spring-boot:run` | Backend only |
| Backend only (JAR) | `cd backend_java/backend && java -jar target/*.jar` | Backend only |
| Frontend only | `cd frontend_tkinter && python3 main.py` | Frontend only |

---

## 🔍 How to Know If It's Working

### Check Backend:
```bash
# In browser, go to:
http://localhost:8080/actuator/health

# Or in terminal:
curl http://localhost:8080/actuator/health
```

If you see `{"status":"UP"}`, backend is working! ✅

### Check Frontend:
You should see a window pop up with a login screen. ✅

---

## 📄 Where Are the Logs?

When you use `./run.sh`, logs are saved to:

- **Backend logs:** `backend.log` (in project root)
- **Frontend logs:** `frontend.log` (in project root)

**View logs in real-time:**
```bash
# Backend
tail -f backend.log

# Frontend  
tail -f frontend.log
```

---

## 🆘 Troubleshooting

### "Port 8080 already in use"
Someone else is using that port. Kill it:
```bash
lsof -i :8080
kill -9 <PID>
```

### "mvn: command not found"
Install Maven:
```bash
brew install maven
```

### "Python not found"
Install Python:
```bash
brew install python@3.11
```

### Scripts won't run
Make them executable:
```bash
chmod +x run.sh stop.sh START_APP.sh
```

---

## 🎯 My Recommendation

**For daily development:**
```bash
# Start
./run.sh

# Stop when done
./stop.sh
```

**That's all you need to know!** 

The other commands (mvn, java -jar, etc.) are just different ways to do the same thing. The `run.sh` script does everything for you automatically.

---

## 📝 Summary

- **`run.sh`** = Easy mode (start everything)
- **`stop.sh`** = Stop everything
- **`mvn spring-boot:run`** = Manual backend start
- **`python3 main.py`** = Manual frontend start
- **`java -jar`** = Backend from pre-built file

**99% of the time, just use `run.sh`** 🎉

