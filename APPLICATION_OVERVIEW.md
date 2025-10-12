# 🎓 Campus Event & Resource Coordination System
## Complete Application Overview

---

## 📋 Table of Contents
1. [Purpose & Vision](#purpose--vision)
2. [System Architecture](#system-architecture)
3. [User Roles & Permissions](#user-roles--permissions)
4. [Core Features](#core-features)
5. [Application Workflows](#application-workflows)
6. [Technical Stack](#technical-stack)

---

## 🎯 Purpose & Vision

### **What is this system?**
The Campus Event & Resource Coordination System is a comprehensive platform designed to streamline the management of campus events and shared resources (classrooms, labs, equipment) in educational institutions.

### **Problems it solves:**
- ❌ **Uncoordinated Event Planning** - Multiple events scheduled at the same time/venue
- ❌ **Resource Conflicts** - Double-booking of classrooms, labs, and equipment
- ❌ **Manual Approval Processes** - Time-consuming paper-based approvals
- ❌ **Poor Communication** - Students miss events due to lack of notifications
- ❌ **No Centralized System** - Information scattered across emails and notice boards

### **Key Benefits:**
- ✅ **Centralized Management** - All events and resources in one system
- ✅ **Role-Based Access** - Different capabilities for students, organizers, and admins
- ✅ **Automated Workflows** - Streamlined approval processes
- ✅ **Real-time Updates** - Instant notifications and status changes
- ✅ **Conflict Prevention** - Automatic detection of scheduling conflicts

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                    │
│              (Python Tkinter Desktop Application)           │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Student  │  │Organizer │  │  Admin   │  │  Login   │     │
│  │Dashboard │  │Dashboard │  │Dashboard │  │  Page    │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕ REST API
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│                (Spring Boot Java Backend)                   │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   Auth   │  │  Events  │  │Resources │  │ Bookings │     │
│  │Controller│  │Controller│  │Controller│  │Controller│     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │   JWT    │  │  Email   │  │   DAO    │                   │
│  │  Auth    │  │  Notify  │  │  Layer   │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
                            ↕ JDBC
┌───────────────────────────────────────────────────────────┐
│                      DATA LAYER                           │
│                    (MySQL Database)                       │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  users   │  │  events  │  │resources │  │ bookings │   │
│  │  table   │  │  table   │  │  table   │  │  table   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────────────────────────────────────────────┘
```

---

## 👥 User Roles & Permissions

### 🎓 **STUDENT** Role

**Who they are:**
- Regular students on campus
- Event attendees and participants
- General users of the system

**What they CAN do:**
- ✅ **Browse Events** - View all upcoming campus events
- ✅ **Register for Events** - Sign up to attend events
- ✅ **View Event Details** - See complete event information (time, venue, description)
- ✅ **Search Events** - Find events by title, date, or venue
- ✅ **Manage Profile** - Update personal information
- ✅ **View Registered Events** - See their event registrations
- ✅ **Receive Notifications** - Get updates about events

**What they CANNOT do:**
- ❌ Create or organize events
- ❌ Book campus resources (classrooms, labs, equipment)
- ❌ View or manage bookings
- ❌ Approve/reject anything
- ❌ Access administrative functions
- ❌ Manage other users

**UI Access:**
```
Student Dashboard
├── Browse Events (read-only)
├── My Registered Events
├── Event Details
├── Profile Settings
└── Notifications
```

**Use Cases:**
1. *Sarah (Student)* wants to attend a tech workshop:
   - Logs in → Browse Events → Finds "AI Workshop"
   - Clicks event → Views details → Registers
   - Receives confirmation notification

2. *John (Student)* needs to check his schedule:
   - Logs in → My Registered Events
   - Views all upcoming events he's attending
   - Can unregister if plans change

---

### 🎭 **ORGANIZER** Role

**Who they are:**
- Faculty members organizing departmental events
- Student club leaders
- Event coordinators
- Activity managers

**What they CAN do:**
- ✅ **Create Events** - Schedule new campus events
- ✅ **Edit Events** - Modify event details (title, description, time, venue)
- ✅ **Delete Events** - Cancel events they created
- ✅ **View Registrations** - See who registered for their events
- ✅ **Book Resources** - Reserve classrooms, labs, equipment for events
- ✅ **Manage Bookings** - View and track their resource bookings
- ✅ **View Booking Status** - Check approval status of resource requests
- ✅ **Send Notifications** - Communicate with event attendees
- ✅ **Browse All Events** - See all campus events
- ✅ **Register for Events** - Attend other events as participants

**What they CANNOT do:**
- ❌ Approve/reject bookings (only admins can)
- ❌ Approve/reject events (only admins can)
- ❌ Manage resources (add/edit/delete)
- ❌ Manage users or change roles
- ❌ Access system-wide analytics
- ❌ Modify events created by others

**UI Access:**
```
Organizer Dashboard
├── Create Event
├── My Events (events they created)
├── Event Registrations (who signed up)
├── Book Resources ← NEW FEATURE
├── My Bookings ← NEW FEATURE
├── Browse Events
├── Profile Settings
└── Notifications
```

**Use Cases:**
1. *Prof. Smith (Organizer)* plans a seminar:
   - Logs in → Create Event
   - Fills: "Machine Learning Seminar", Date, Time, Venue
   - Needs projector → Book Resources → Selects "Projector"
   - Submits → Waits for admin approval

2. *Club President (Organizer)* manages workshop:
   - Logs in → My Events → Selects "Coding Workshop"
   - Views 50 student registrations
   - Checks My Bookings → Sees "Lab 101" approved
   - Sends notification to all registered students

---

### 👔 **ADMIN** Role

**Who they are:**
- IT administrators
- Campus facility managers
- Department heads with oversight
- System administrators

**What they CAN do:**
- ✅ **Full System Access** - Complete control over all features
- ✅ **Approve/Reject Events** - Review and authorize event requests
- ✅ **Approve/Reject Bookings** - Authorize resource allocations
- ✅ **Manage Users** - Create, edit, delete user accounts
- ✅ **Change User Roles** - Promote/demote users (student ↔ organizer)
- ✅ **Manage Resources** - Add/edit/delete campus resources
- ✅ **View Analytics** - System-wide reports and statistics
- ✅ **System Configuration** - Manage system settings
- ✅ **View All Events** - See all events across campus
- ✅ **View All Bookings** - Monitor all resource usage
- ✅ **Bulk Notifications** - Send campus-wide announcements
- ✅ **Audit Logs** - Track system activity

**What they CANNOT do:**
- ❌ Nothing - Admins have full access

**UI Access:**
```
Admin Dashboard
├── Event Approvals (pending events)
├── Booking Approvals (pending resource requests)
├── Manage Users (CRUD operations)
├── Manage Resources (CRUD operations)
├── Browse All Events
├── View All Bookings
├── Analytics & Reports
├── System Settings
└── Bulk Notifications
```

**Use Cases:**
1. *Admin Manager* reviews resource requests:
   - Logs in → Booking Approvals
   - Sees 5 pending requests
   - Reviews "Projector for ML Seminar"
   - Checks availability → Approves
   - System sends confirmation to organizer

2. *IT Admin* manages system:
   - Logs in → Manage Users
   - Creates new organizer account for faculty
   - Logs in → Manage Resources
   - Adds new "Conference Room B" with capacity 100
   - Logs in → Analytics
   - Views: 150 events this semester, 85% approval rate

---

## 🔄 Core Features

### 1️⃣ **Authentication & Authorization**

**Registration:**
- New users create accounts with name, email, password
- Default role: Student
- Email must be unique
- Password hashed with BCrypt

**Login:**
- Email + Password authentication
- JWT token generated on success
- Token stored in session
- Role-based dashboard routing

**Security:**
- JWT (JSON Web Token) authentication
- BCrypt password hashing
- Session management
- Role-based access control (RBAC)

---

### 2️⃣ **Event Management**

**Event Lifecycle:**
```
Create → [Admin Approval] → Active → Registrations → Event Date → Completed
```

**Event Properties:**
- Title (e.g., "Tech Talk 2025")
- Description (what it's about)
- Organizer (who's hosting)
- Start Time & End Time
- Venue (location)
- Status (pending/approved/rejected)

**Operations:**
- **CREATE** (Organizers) - Submit new event
- **READ** (All users) - Browse and search events
- **UPDATE** (Organizers) - Edit their own events
- **DELETE** (Organizers) - Cancel their events
- **APPROVE/REJECT** (Admins) - Review submissions

**Student View:**
- See all approved events
- Filter by date, venue
- Register/unregister
- View registration count

**Organizer View:**
- Create new events
- Edit/delete own events
- View who registered
- Track approval status

**Admin View:**
- Approve/reject pending events
- View all events system-wide
- Generate event reports

---

### 3️⃣ **Resource Management**

**Resource Types:**
- 🏛️ **Venues** - Classrooms, auditoriums, conference rooms
- 💻 **Equipment** - Projectors, laptops, microphones
- 🔬 **Labs** - Computer labs, science labs

**Resource Properties:**
- Name (e.g., "Room 301", "Projector A")
- Type (Equipment/Venue/Lab)
- Capacity (how many people/items)
- Location (building, floor)
- Availability status

**Resource Operations:**
- **ADD** (Admins only) - Create new resource
- **EDIT** (Admins only) - Update resource details
- **DELETE** (Admins only) - Remove resource
- **VIEW** (Organizers) - Browse available resources
- **BOOK** (Organizers) - Request resource for event

---

### 4️⃣ **Booking System** (Organizers Only)

**Booking Workflow:**
```
1. Organizer creates event
2. Organizer browses resources
3. Organizer books resource (e.g., projector)
4. Booking status: PENDING
5. Admin reviews booking
6. Admin approves/rejects
7. Status: APPROVED or REJECTED
8. Organizer receives notification
```

**Booking Properties:**
- Event (which event needs it)
- Resource (what's being booked)
- User (who's booking)
- Start Time & End Time
- Status (pending/approved/rejected)

**Conflict Detection:**
- System checks if resource is already booked
- Prevents double-booking
- Shows availability calendar

**Student Restriction (NEW):**
- ❌ Students cannot access "Book Resources"
- ❌ Students cannot view "My Bookings"
- ✅ Only Organizers and Admins can book resources
- 💡 Students see info message: "Booking available for organizers"

---

### 5️⃣ **Notification System**

**Email Notifications:**
- 📧 Event approval/rejection
- 📧 Booking approval/rejection
- 📧 Event reminders
- 📧 Registration confirmations
- 📧 Event updates/cancellations
- 📧 Bulk announcements (admin)

**Notification Triggers:**
- User registers for event
- Event gets approved/rejected
- Booking gets approved/rejected
- Event details change
- Event approaching (reminder)

---

## 🔄 Application Workflows

### 📌 **Workflow 1: Student Registers for Event**

```
┌─────────┐
│ Student │
│  Login  │
└────┬────┘
     │
     ▼
┌─────────────────┐
│ Browse Events   │
│ (Approved only) │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Click Event     │
│ "Tech Workshop" │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ View Details    │
│ - Date, Time    │
│ - Venue         │
│ - Description   │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Click Register  │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Confirmation    │
│ "Registered!"   │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Email Sent      │
│ to Student      │
└─────────────────┘
```

---

### 📌 **Workflow 2: Organizer Creates Event with Resource**

```
┌──────────┐
│Organizer │
│  Login   │
└────┬─────┘
     │
     ▼
┌──────────────────┐
│ Create Event     │
│ - Title          │
│ - Description    │
│ - Date/Time      │
│ - Venue          │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Submit Event     │
│ Status: PENDING  │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Book Resources   │ ← Organizers ONLY
│ Click sidebar    │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Browse Resources │
│ - Projectors     │
│ - Labs           │
│ - Equipment      │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Select Resource  │
│ "Projector A"    │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Book Resource    │
│ - Select Date    │
│ - Select Time    │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Booking Created  │
│ Status: PENDING  │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Wait for Admin   │
│ Approval         │
└──────────────────┘
```

---

### 📌 **Workflow 3: Admin Approves Event & Booking**

```
┌─────────┐
│  Admin  │
│  Login  │
└────┬────┘
     │
     ▼
┌────────────────────┐
│ Event Approvals    │
│ (5 pending)        │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│ Review Event       │
│ "Tech Workshop"    │
│ - Check details    │
│ - Verify venue     │
│ - Check conflicts  │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│ Click APPROVE      │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│ Email to Organizer │
│ "Event Approved"   │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│ Booking Approvals  │
│ (3 pending)        │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│ Review Booking     │
│ "Projector for     │
│  Tech Workshop"    │
│ - Check available  │
│ - Verify dates     │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│ Click APPROVE      │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│ Email to Organizer │
│ "Booking Approved" │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│ Event Now ACTIVE   │
│ Students Can       │
│ Register           │
└────────────────────┘
```

---

## 🔐 Permission Matrix

| Feature                    | Student | Organizer | Admin |
|----------------------------|---------|-----------|-------|
| **Authentication**         |         |           |       |
| Register Account           | ✅      | ✅        | ✅    |
| Login                      | ✅      | ✅        | ✅    |
| Update Profile             | ✅      | ✅        | ✅    |
| **Events**                 |         |           |       |
| View Events                | ✅      | ✅        | ✅    |
| Create Event               | ❌      | ✅        | ✅    |
| Edit Own Event             | ❌      | ✅        | ✅    |
| Delete Own Event           | ❌      | ✅        | ✅    |
| Approve/Reject Event       | ❌      | ❌        | ✅    |
| Register for Event         | ✅      | ✅        | ✅    |
| View Registrations         | ❌      | ✅ (own)  | ✅    |
| **Resources**              |         |           |       |
| View Resources             | ❌      | ✅        | ✅    |
| Book Resource              | ❌      | ✅        | ✅    |
| View My Bookings           | ❌      | ✅        | ✅    |
| Approve/Reject Booking     | ❌      | ❌        | ✅    |
| Add/Edit/Delete Resource   | ❌      | ❌        | ✅    |
| **Users**                  |         |           |       |
| View All Users             | ❌      | ❌        | ✅    |
| Create User                | ❌      | ❌        | ✅    |
| Edit User                  | ❌      | ❌        | ✅    |
| Delete User                | ❌      | ❌        | ✅    |
| Change User Role           | ❌      | ❌        | ✅    |
| **Notifications**          |         |           |       |
| Receive Notifications      | ✅      | ✅        | ✅    |
| Send Event Notifications   | ❌      | ✅        | ✅    |
| Send Bulk Notifications    | ❌      | ❌        | ✅    |
| **Analytics**              |         |           |       |
| View System Analytics      | ❌      | ❌        | ✅    |

---

## 💻 Technical Stack

### **Frontend** (Desktop Application)
- **Language:** Python 3.11+
- **Framework:** Tkinter (Native GUI)
- **Libraries:**
  - `requests` - API calls
  - `Pillow` - Image handling
  - `tkcalendar` - Date picker
  - `matplotlib` - Charts/graphs
  - `bcrypt` - Password hashing

### **Backend** (REST API Server)
- **Language:** Java 17+
- **Framework:** Spring Boot 3.2.x
- **Components:**
  - Spring Security (JWT authentication)
  - Spring Data JDBC
  - Spring Boot Validation
  - JavaMail (Email notifications)
- **Build Tool:** Maven

### **Database**
- **System:** MySQL 8.0+
- **Tables:**
  - `users` - User accounts
  - `events` - Event information
  - `resources` - Campus resources
  - `bookings` - Resource reservations

### **Security**
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** BCrypt ($2a$10$)
- **Authorization:** Role-Based Access Control (RBAC)
- **Session Management:** Token-based

### **Communication**
- **API:** RESTful HTTP/JSON
- **Port:** Backend on 8080
- **Endpoints:** `/api/*`

---

## 📊 Data Flow Example

### Creating Event with Resource Booking:

```
┌──────────────┐
│  Organizer   │
│  (Frontend)  │
└──────┬───────┘
       │ 1. POST /api/events
       │    {title, description, date, venue}
       ▼
┌──────────────┐
│   Backend    │
│  Controller  │
└──────┬───────┘
       │ 2. Validate data
       │ 3. Save to DB
       ▼
┌──────────────┐
│   Database   │
│ events table │
└──────┬───────┘
       │ 4. Return event_id = 42
       ▼
┌──────────────┐
│   Backend    │
│   Response   │
└──────┬───────┘
       │ 5. {"id": 42, "message": "Event created"}
       ▼
┌──────────────┐
│  Frontend    │
│  (Received)  │
└──────┬───────┘
       │ 6. Navigate to Book Resources
       │ 7. POST /api/bookings
       │    {event_id: 42, resource_id: 5}
       ▼
┌──────────────┐
│   Backend    │
│  Controller  │
└──────┬───────┘
       │ 8. Check conflicts
       │ 9. Save booking
       ▼
┌──────────────┐
│   Database   │
│bookings table│
└──────┬───────┘
       │ 10. Booking saved, status=pending
       ▼
┌──────────────┐
│   Backend    │
│   Email      │
└──────┬───────┘
       │ 11. Send notification to admin
       ▼
┌──────────────┐
│    Admin     │
│    Inbox     │
└──────────────┘
```

---

## 🎯 Summary

### **For Students:**
A simple way to discover campus events and register to attend them.

### **For Organizers:**
A powerful tool to plan events, book resources, and manage attendees - all in one place.

### **For Admins:**
Complete control and oversight of campus activities, resources, and user management.

### **For the Institution:**
A modern, efficient system that reduces conflicts, improves communication, and provides valuable data insights.

---

## 📞 Quick Reference

**Test Credentials:**
- Student: `student1@campus.com` / `test123`
- Organizer: `organizer1@campus.com` / `test123`
- Admin: `admin@campus.com` / `test123`

**URLs:**
- Backend: `http://localhost:8080`
- API Docs: `/api/*`

**Key Files:**
- Credentials: `TEST_CREDENTIALS.md`
- Startup Guide: `STARTUP_GUIDE.md`
- Recent Changes: `RESOURCE_BOOKING_ORGANIZERS_ONLY.md`

---

**Version:** 2.0.0  
**Last Updated:** October 11, 2025  
**Status:** Production Ready ✅
