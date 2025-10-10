# Campus Event System

A comprehensive campus event and resource management system with role-based access control.

## 🚀 Quick Start

### One-Command Startup

Start both backend and frontend with a single command:

```bash
./run.sh
```

This will:
- ✅ Start Spring Boot backend (port 8080)
- ✅ Start Tkinter frontend GUI
- ✅ Display status and log locations

### Stop Everything

```bash
./stop.sh
```

### Check Status

```bash
./status.sh
```

## 📋 Project Structure

```
CampusEventSystem/
├── backend_java/          # Spring Boot backend (Java)
│   └── backend/
│       ├── src/
│       ├── pom.xml
│       └── mvnw
│
├── frontend_tkinter/      # Tkinter frontend (Python)
│   ├── main.py
│   ├── pages/
│   ├── components/
│   └── utils/
│
├── database_sql/          # Database schemas and sample data
│   ├── schema.sql
│   └── sample_data.sql
│
├── run.sh                 # Start both services
├── stop.sh                # Stop both services
├── status.sh              # Check system status
└── STARTUP_GUIDE.md       # Detailed startup documentation
```

## 🛠️ Manual Setup

### Prerequisites

- **Java 17+** - For backend
- **Maven 3.8+** - For building backend
- **Python 3.11+** - For frontend
- **MySQL 8.0+** - For database

### Backend Setup

```bash
cd backend_java/backend
./mvnw spring-boot:run
```

Backend will start on `http://localhost:8080`

### Frontend Setup

```bash
cd frontend_tkinter
pip3 install -r requirements.txt
python3.11 main.py
```

## 📚 Documentation

- **[STARTUP_GUIDE.md](STARTUP_GUIDE.md)** - Detailed startup and troubleshooting guide
- **[frontend_tkinter/README.md](frontend_tkinter/README.md)** - Frontend documentation
- **[frontend_tkinter/MACOS_BUTTON_FIX.md](frontend_tkinter/MACOS_BUTTON_FIX.md)** - macOS UI fix documentation

## 🎯 Features

### For Students
- 🔍 Browse and search campus events
- 📚 Book resources (classrooms, labs, equipment)
- ✅ Register for events
- 📅 Manage bookings
- 🔔 Receive notifications

### For Organizers
- ➕ Create and manage events
- 📊 Track event registrations
- 📝 Update event details
- 🎫 Manage attendees

### For Admins
- ✅ Approve/reject events and bookings
- 👥 Manage users and roles
- 🏢 Manage resources
- 📈 View analytics and reports
- 📧 System notifications

## 🔍 System Status

Check if services are running:

```bash
./status.sh
```

Output shows:
- Backend status and port
- Frontend status
- Process IDs
- Log file sizes

## 📄 Logs

Log files are created in the project root:

```bash
# View backend logs
tail -f backend.log

# View frontend logs
tail -f frontend.log
```

## 🌐 API Endpoints

- **Backend API**: http://localhost:8080/api
- **Health Check**: http://localhost:8080/actuator/health
- **API Documentation**: (Configure Swagger if needed)

## 🧪 Testing

### Test Backend
```bash
curl http://localhost:8080/actuator/health
```

### Test API Endpoints
```bash
# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# Get events
curl http://localhost:8080/api/events
```

## 🐛 Troubleshooting

### Port 8080 already in use

```bash
# Find process
lsof -i :8080

# Kill process
kill -9 <PID>
```

### Backend won't start

```bash
# Check Java version
java -version

# Check Maven
mvn -version

# View logs
cat backend.log
```

### Frontend won't start

```bash
# Check Python version
python3 --version

# Install dependencies
cd frontend_tkinter
pip3 install -r requirements.txt

# View logs
cat frontend.log
```

### Buttons appear grey on macOS

See [frontend_tkinter/MACOS_BUTTON_FIX.md](frontend_tkinter/MACOS_BUTTON_FIX.md) for the solution.

## 🔄 Development Workflow

```bash
# Start development
./run.sh

# Make changes to code...

# Restart services
./stop.sh
./run.sh

# Check status
./status.sh

# View logs
tail -f backend.log
tail -f frontend.log
```

## 📦 Building for Production

### Backend JAR

```bash
cd backend_java/backend
./mvnw clean package
java -jar target/backend-0.0.1-SNAPSHOT.jar
```

### Frontend Distribution

```bash
cd frontend_tkinter
# Package with PyInstaller or similar
pyinstaller --onefile main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `./run.sh`
5. Submit a pull request

## 📝 License

[Your License Here]

## 👥 Team

[Your Team Information Here]

## 📞 Support

For issues or questions:
- Check the [STARTUP_GUIDE.md](STARTUP_GUIDE.md)
- Review log files (`backend.log`, `frontend.log`)
- Check documentation in respective directories

---

**Version**: 1.0.0  
**Last Updated**: October 2025
