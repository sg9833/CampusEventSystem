# 🎓 Campus Event System

A comprehensive campus event and resource management system with role-based access control, built with Spring Boot (Java 21) backend and Python Tkinter frontend.

## 👥 Team

**Creator & Lead Developer:** Garine Sai Ajay

## ⚠️ FIRST TIME SETUP?

**→ READ [CLEANUP_BEFORE_SETUP.md](CLEANUP_BEFORE_SETUP.md) FIRST!**

Before running the application, you MUST:
1. Delete unnecessary developer files (test scripts, logs, etc.)
2. **Edit `application.properties` to replace the developer's MySQL password**
3. Then follow [CLIENT_SETUP_GUIDE.md](CLIENT_SETUP_GUIDE.md)

**DO NOT skip this step or the application will NOT work!**

---

## 🚀 Quick Start (After Cleanup & Setup)

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

## 🧪 Testing & API Documentation

### Quick Health Check
```bash
# Check backend is running
curl http://localhost:8080/actuator/health

# Check if port is in use
lsof -ti:8080
```

---

## 📡 Complete API Testing Guide

### 1. Authentication APIs

#### Register New User
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@campus.com",
    "password": "password123",
    "role": "STUDENT"
  }'
```

**Roles:** `STUDENT`, `ORGANIZER`, `ADMIN`

#### Login
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student1@campus.com",
    "password": "student123"
  }'
```

**Response:** Returns JWT token - copy this for authenticated requests

**Test Credentials:**
- Student: `student1@campus.com` / `student123`
- Organizer: `organizer1@campus.com` / `organizer123`
- Admin: `admin@campus.com` / `admin123`

---

### 2. Event APIs

#### Get All Events (Public)
```bash
curl -X GET http://localhost:8080/api/events
```

#### Get Event by ID
```bash
curl -X GET http://localhost:8080/api/events/1
```

#### Create Event (Organizer/Admin only)
```bash
# First login to get token, then:
curl -X POST http://localhost:8080/api/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Tech Workshop",
    "description": "Introduction to Spring Boot",
    "date": "2025-11-15",
    "time": "10:00",
    "venue": "Room 101",
    "maxAttendees": 50,
    "category": "WORKSHOP"
  }'
```

**Categories:** `WORKSHOP`, `SEMINAR`, `CONFERENCE`, `CULTURAL`, `SPORTS`, `OTHER`

#### Update Event
```bash
curl -X PUT http://localhost:8080/api/events/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Updated Tech Workshop",
    "description": "Advanced Spring Boot Topics",
    "date": "2025-11-15",
    "time": "14:00",
    "venue": "Room 201",
    "maxAttendees": 75,
    "category": "WORKSHOP"
  }'
```

#### Delete Event
```bash
curl -X DELETE http://localhost:8080/api/events/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Get My Events (Organizer)
```bash
curl -X GET http://localhost:8080/api/events/my \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Event Registration APIs

#### Register for Event
```bash
curl -X POST http://localhost:8080/api/registrations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "eventId": 1
  }'
```

#### Get My Registrations
```bash
curl -X GET http://localhost:8080/api/registrations/my \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Cancel Registration
```bash
curl -X DELETE http://localhost:8080/api/registrations/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Get Registrations for Event (Organizer)
```bash
curl -X GET http://localhost:8080/api/registrations/event/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 4. Resource APIs

#### Get All Resources
```bash
curl -X GET http://localhost:8080/api/resources
```

#### Get Resource by ID
```bash
curl -X GET http://localhost:8080/api/resources/1
```

#### Create Resource (Admin only)
```bash
curl -X POST http://localhost:8080/api/resources \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Projector",
    "type": "EQUIPMENT",
    "capacity": 1,
    "location": "Media Room",
    "description": "HD Projector for presentations",
    "available": true
  }'
```

**Resource Types:** `CLASSROOM`, `LAB`, `AUDITORIUM`, `EQUIPMENT`, `OTHER`

#### Update Resource
```bash
curl -X PUT http://localhost:8080/api/resources/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "HD Projector",
    "type": "EQUIPMENT",
    "capacity": 1,
    "location": "Media Room A",
    "description": "4K HD Projector with HDMI",
    "available": true
  }'
```

#### Delete Resource
```bash
curl -X DELETE http://localhost:8080/api/resources/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Check Resource Availability
```bash
curl -X GET "http://localhost:8080/api/resources/1/availability?date=2025-11-15" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 5. Booking APIs

#### Create Booking
```bash
curl -X POST http://localhost:8080/api/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "userId": 2,
    "resourceId": 1,
    "startTime": "2025-11-15T10:00:00",
    "endTime": "2025-11-15T12:00:00",
    "eventId": 1
  }'
```

**Note:** Times must be in ISO-8601 format: `YYYY-MM-DDTHH:MM:SS`

#### Get My Bookings
```bash
curl -X GET http://localhost:8080/api/bookings/my \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Get Booked Slots for Resource
```bash
curl -X GET "http://localhost:8080/api/bookings/resource/1/date/2025-11-15" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 6. Admin - Event Approval APIs

#### Get Pending Events
```bash
curl -X GET http://localhost:8080/api/admin/events/pending \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN"
```

#### Approve Event
```bash
curl -X PUT http://localhost:8080/api/admin/events/1/approve \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN"
```

**Response:**
```json
{
  "message": "Event approved successfully",
  "event_id": 1
}
```

#### Reject Event
```bash
curl -X PUT http://localhost:8080/api/admin/events/1/reject \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN" \
  -d '{
    "reason": "Insufficient details provided"
  }'
```

**Response:**
```json
{
  "message": "Event rejected",
  "event_id": 1,
  "reason": "Insufficient details provided"
}
```

---

### 7. Admin - Booking Approval APIs

#### Get Pending Bookings
```bash
curl -X GET http://localhost:8080/api/admin/bookings/pending \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN"
```

**Response:** Array of pending bookings with full details

#### Approve Booking
```bash
curl -X PUT http://localhost:8080/api/admin/bookings/1/approve \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN"
```

**Response:**
```json
{
  "message": "Booking approved successfully",
  "booking_id": 1
}
```

#### Reject Booking
```bash
curl -X PUT http://localhost:8080/api/admin/bookings/1/reject \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN" \
  -d '{
    "reason": "Resource unavailable at requested time"
  }'
```

**Response:**
```json
{
  "message": "Booking rejected",
  "booking_id": 1,
  "reason": "Resource unavailable at requested time"
}
```

---

### 8. User Management APIs

#### Get User Profile
```bash
curl -X GET http://localhost:8080/api/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Update User Profile
```bash
curl -X PUT http://localhost:8080/api/users/me \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "username": "john_doe_updated",
    "email": "john.new@campus.com"
  }'
```

#### Get All Users (Admin only)
```bash
curl -X GET http://localhost:8080/api/admin/users \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN"
```

---

## 🔑 Working with JWT Tokens

### Step-by-Step Authentication Flow

**Step 1: Login and Save Token**
```bash
# Login and extract token
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student1@campus.com","password":"student123"}' \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# Verify token was saved
echo $TOKEN
```

**Step 2: Use Token in Requests**
```bash
# Now use the token for authenticated requests
curl -X GET http://localhost:8080/api/events/my \
  -H "Authorization: Bearer $TOKEN"
```

**Step 3: Complete Example - Create and Register for Event**
```bash
# 1. Login as organizer
ORG_TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"organizer1@campus.com","password":"organizer123"}' \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# 2. Create event
EVENT_ID=$(curl -s -X POST http://localhost:8080/api/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ORG_TOKEN" \
  -d '{
    "title": "Spring Boot Masterclass",
    "description": "Learn Spring Boot from scratch",
    "date": "2025-12-01",
    "time": "14:00",
    "venue": "Lab 3",
    "maxAttendees": 30,
    "category": "WORKSHOP"
  }' | grep -o '"id":[0-9]*' | cut -d':' -f2)

echo "Created event ID: $EVENT_ID"

# 3. Login as student
STU_TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student1@campus.com","password":"student123"}' \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# 4. Register for event
curl -X POST http://localhost:8080/api/registrations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STU_TOKEN" \
  -d "{\"eventId\": $EVENT_ID}"
```

---

## 📊 API Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource (e.g., already registered) |
| 500 | Server Error | Internal server error |

---

## 🔒 Role-Based Access Control

| Endpoint | Student | Organizer | Admin |
|----------|---------|-----------|-------|
| GET /api/events | ✅ | ✅ | ✅ |
| POST /api/events | ❌ | ✅ | ✅ |
| PUT /api/events/{id} | ❌ | ✅ (own) | ✅ |
| DELETE /api/events/{id} | ❌ | ✅ (own) | ✅ |
| POST /api/registrations | ✅ | ✅ | ✅ |
| GET /api/resources | ✅ | ✅ | ✅ |
| POST /api/resources | ❌ | ❌ | ✅ |
| POST /api/bookings | ✅ | ✅ | ✅ |
| GET /api/admin/events/pending | ❌ | ❌ | ✅ |
| PUT /api/admin/events/{id}/approve | ❌ | ❌ | ✅ |
| GET /api/admin/bookings/pending | ❌ | ❌ | ✅ |
| PUT /api/admin/bookings/{id}/approve | ❌ | ❌ | ✅ |

---

## 🧪 Testing Scenarios

### Scenario 1: Student Workflow
```bash
# 1. Register new student
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@campus.com",
    "password": "alice123",
    "role": "STUDENT"
  }'

# 2. Login
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@campus.com","password":"alice123"}' \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# 3. Browse events
curl -X GET http://localhost:8080/api/events

# 4. Register for event
curl -X POST http://localhost:8080/api/registrations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"eventId": 1}'

# 5. View my registrations
curl -X GET http://localhost:8080/api/registrations/my \
  -H "Authorization: Bearer $TOKEN"
```

### Scenario 2: Organizer Workflow
```bash
# 1. Login as organizer
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"organizer1@campus.com","password":"organizer123"}' \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# 2. Create event
curl -X POST http://localhost:8080/api/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Hackathon 2025",
    "description": "24-hour coding marathon",
    "date": "2025-11-20",
    "time": "09:00",
    "venue": "Main Auditorium",
    "maxAttendees": 100,
    "category": "CONFERENCE"
  }'

# 3. View my events
curl -X GET http://localhost:8080/api/events/my \
  -H "Authorization: Bearer $TOKEN"

# 4. Book resource
curl -X POST http://localhost:8080/api/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "userId": 2,
    "resourceId": 1,
    "startTime": "2025-11-20T09:00:00",
    "endTime": "2025-11-21T09:00:00"
  }'
```

### Scenario 3: Admin Workflow
```bash
# 1. Login as admin
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@campus.com","password":"admin123"}' \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# 2. View pending events
curl -X GET http://localhost:8080/api/admin/events/pending \
  -H "Authorization: Bearer $TOKEN"

# 3. Approve event
curl -X PUT http://localhost:8080/api/admin/events/1/approve \
  -H "Authorization: Bearer $TOKEN"

# 4. View pending bookings
curl -X GET http://localhost:8080/api/admin/bookings/pending \
  -H "Authorization: Bearer $TOKEN"

# 5. Approve booking
curl -X PUT http://localhost:8080/api/admin/bookings/1/approve \
  -H "Authorization: Bearer $TOKEN"

# 6. Create new resource
curl -X POST http://localhost:8080/api/resources \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Conference Room A",
    "type": "CLASSROOM",
    "capacity": 50,
    "location": "Building 2, Floor 3",
    "description": "Large conference room with AV equipment",
    "available": true
  }'
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

---

## 🗄️ Database Quick Reference

### Common SQL Queries

```sql
-- View all events
SELECT * FROM events ORDER BY created_at DESC;

-- View pending events
SELECT e.*, u.username as organizer 
FROM events e 
JOIN users u ON e.organizer_id = u.id 
WHERE e.status = 'pending';

-- View all bookings with details
SELECT b.*, u.username, r.name as resource_name 
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN resources r ON b.resource_id = r.id
ORDER BY b.created_at DESC;

-- View pending bookings
SELECT * FROM bookings WHERE status = 'pending';

-- View event registrations
SELECT r.*, e.title, u.username 
FROM registrations r
JOIN events e ON r.event_id = e.id
JOIN users u ON r.user_id = u.id;

-- Count events by status
SELECT status, COUNT(*) as count FROM events GROUP BY status;

-- Count bookings by status
SELECT status, COUNT(*) as count FROM bookings GROUP BY status;

-- Check resource availability for a date
SELECT * FROM bookings 
WHERE resource_id = 1 
AND DATE(start_time) = '2025-11-15'
ORDER BY start_time;
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Python Tkinter)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Login   │  │  Events  │  │ Bookings │  │  Admin   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │ HTTP/REST
                           │ JWT Authentication
┌─────────────────────────────────────────────────────────────┐
│              Backend (Spring Boot 3.2.2 / Java 21)           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Controllers (REST APIs)                    │  │
│  │  • AuthController      • EventController              │  │
│  │  • AdminController     • BookingController            │  │
│  │  • ResourceController  • RegistrationController       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Security Layer                             │  │
│  │  • JWT Filter          • Role Authorization           │  │
│  │  • Password Encoding   • CORS Configuration           │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Business Logic (Services)                  │  │
│  │  • UserService         • EventService                 │  │
│  │  • BookingService      • ValidationService            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Data Access Layer (DAOs)                   │  │
│  │  • UserDao             • EventDao                     │  │
│  │  • BookingDao          • ResourceDao                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │ JDBC
┌─────────────────────────────────────────────────────────────┐
│                    Database (MySQL 8.0)                      │
│  • users               • events              • bookings      │
│  • resources           • registrations                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Performance & Scalability

### Current Configuration
- **Backend**: Spring Boot with embedded Tomcat
- **Connection Pool**: HikariCP (default)
- **Max Connections**: 10 (configurable in `application.properties`)
- **JWT Expiration**: 24 hours (configurable)

### Optimization Tips
```properties
# application.properties
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.jpa.properties.hibernate.jdbc.batch_size=20
spring.jpa.properties.hibernate.order_inserts=true
```

---

## 🔐 Security Features

✅ **JWT Authentication** - Secure token-based auth  
✅ **Password Encryption** - BCrypt hashing  
✅ **Role-Based Access Control** - Fine-grained permissions  
✅ **CORS Configuration** - Cross-origin protection  
✅ **SQL Injection Prevention** - Parameterized queries  
✅ **Input Validation** - Server-side validation  
✅ **Audit Logging** - Track admin actions  

---

## � Additional Documentation

### Comprehensive Guides
- **[STARTUP_GUIDE.md](STARTUP_GUIDE.md)** - Detailed startup instructions
- **[EMAIL_FEATURE_SUMMARY.md](EMAIL_FEATURE_SUMMARY.md)** - Email notification system
- **[JWT_IMPLEMENTATION_COMPLETE.md](JWT_IMPLEMENTATION_COMPLETE.md)** - JWT security details
- **[DARK_MODE_FIX_COMPLETE_DOCUMENTATION.md](DARK_MODE_FIX_COMPLETE_DOCUMENTATION.md)** - Dark mode implementation
- **[RESOURCE_BOOKING_COMPLETE.md](RESOURCE_BOOKING_COMPLETE.md)** - Booking system details
- **[MY_EVENTS_TRANSFORMATION_SUMMARY.md](MY_EVENTS_TRANSFORMATION_SUMMARY.md)** - Event management features

### Frontend Documentation
- **[frontend_tkinter/README.md](frontend_tkinter/README.md)** - Frontend architecture
- **[MACOS_BUTTON_FIX.md](frontend_tkinter/MACOS_BUTTON_FIX.md)** - macOS compatibility fixes

### Testing & Validation
- **[COMPLETE_TESTING_GUIDE.md](COMPLETE_TESTING_GUIDE.md)** - Full testing procedures
- **[INPUT_VALIDATION_COMPLETE.md](INPUT_VALIDATION_COMPLETE.md)** - Input validation guide

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly with `./run.sh`
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style Guidelines
- **Java**: Follow Google Java Style Guide
- **Python**: Follow PEP 8
- **SQL**: Use uppercase for keywords
- **Documentation**: Update README for new features

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

For issues or questions:
1. Check the [STARTUP_GUIDE.md](STARTUP_GUIDE.md)
2. Review log files (`backend.log`, `frontend.log`)
3. Search existing documentation files
4. Check API responses for error messages
5. Verify JWT token is valid and not expired

### Common Issues & Solutions

**Backend won't start:**
```bash
# Check if port is in use
lsof -ti:8080 && kill -9 $(lsof -ti:8080)

# Check Java version
java -version  # Should be Java 17 or higher

# Rebuild
cd backend_java/backend && mvn clean package
```

**Frontend crashes:**
```bash
# Check Python version
python3 --version  # Should be 3.11+

# Reinstall dependencies
cd frontend_tkinter && pip3 install -r requirements.txt --upgrade
```

**Database connection error:**
```bash
# Check MySQL is running
mysql.server status

# Test connection
mysql -u root -p campusdb
```

**401 Unauthorized errors:**
- Verify JWT token is included in Authorization header
- Check token hasn't expired (24 hour expiration)
- Login again to get fresh token

**403 Forbidden errors:**
- Verify user has correct role for endpoint
- Check role-based access control table above
- Admin endpoints require ADMIN role

---

## 🎯 Quick Command Reference

```bash
# Start everything
./run.sh

# Stop everything
./stop.sh

# Check status
./status.sh

# View logs
tail -f backend.log
tail -f frontend.log

# Restart backend only
lsof -ti:8080 && kill -9 $(lsof -ti:8080)
cd backend_java/backend && java -jar target/backend-0.0.1-SNAPSHOT.jar &

# Test API
curl http://localhost:8080/actuator/health

# Get JWT token
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@campus.com","password":"admin123"}' \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# Use token
curl -X GET http://localhost:8080/api/admin/events/pending \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🌟 Features Implemented

### Core Features ✅
- [x] User authentication & authorization (JWT)
- [x] Role-based access control (Student, Organizer, Admin)
- [x] Event creation and management
- [x] Event registration system
- [x] Resource booking system
- [x] Admin approval workflows (events & bookings)
- [x] Email notifications (configurable)
- [x] Dark mode support
- [x] Input validation
- [x] Audit logging

### UI Features ✅
- [x] Responsive Tkinter GUI
- [x] macOS compatibility (Canvas buttons)
- [x] Calendar view for bookings
- [x] Real-time status updates
- [x] Tabbed navigation
- [x] Form validation with visual feedback

### Security Features ✅
- [x] JWT token authentication
- [x] Password hashing (BCrypt)
- [x] SQL injection prevention
- [x] CORS configuration
- [x] Session management
- [x] Role validation on all endpoints

---

## 🔄 Version History

### v1.0.0 (November 2025)
- ✅ Initial release
- ✅ Complete authentication system
- ✅ Event management
- ✅ Resource booking
- ✅ Admin approval workflows
- ✅ Email notifications
- ✅ Dark mode support

### Recent Updates
- ✅ Fixed booking approval system (Nov 4, 2025)
- ✅ Added comprehensive API documentation
- ✅ Enhanced macOS compatibility
- ✅ Improved calendar rendering
- ✅ Added input validation

---

## 🚀 Deployment

### Production Checklist

**Backend:**
```bash
# 1. Update application.properties
spring.jpa.hibernate.ddl-auto=validate
spring.profiles.active=production
jwt.secret=YOUR_SECURE_SECRET_KEY_HERE

# 2. Build production JAR
cd backend_java/backend
mvn clean package -DskipTests

# 3. Run with production profile
java -jar target/backend-0.0.1-SNAPSHOT.jar --spring.profiles.active=production
```

**Frontend:**
```bash
# Package as executable (optional)
cd frontend_tkinter
pyinstaller --onefile --windowed main.py

# Or distribute as Python app
pip install -r requirements.txt
python3 main.py
```

**Database:**
```sql
-- Create production database
CREATE DATABASE campusdb_prod;

-- Run migrations
source database_sql/schema.sql;
source database_sql/sample_data.sql;

-- Create database user
CREATE USER 'campusapp'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON campusdb_prod.* TO 'campusapp'@'localhost';
FLUSH PRIVILEGES;
```

---

## 📊 Project Statistics

- **Backend Lines of Code**: ~15,000
- **Frontend Lines of Code**: ~8,000
- **Total API Endpoints**: 30+
- **Database Tables**: 6
- **Documentation Files**: 40+
- **Test Scenarios**: 15+

---

## 🙏 Acknowledgments

Built with:
- **Spring Boot** - Backend framework
- **MySQL** - Database
- **Python Tkinter** - Frontend GUI
- **JWT** - Authentication
- **HikariCP** - Connection pooling
- **BCrypt** - Password hashing

---

**Version**: 1.0.0  
**Last Updated**: November 4, 2025  
**Creator**: Garine Sai Ajay  
**Status**: Production Ready ✅
