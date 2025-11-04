# Event Registration & Approval System - Complete Implementation

## 🎯 Issues Fixed

### 1. ✅ Event Registration Not Implemented
**Problem:** Clicking "Register" button showed "Registration for 'Tech talk for web devs' is not implemented yet."

**Solution:** 
- Created `event_registrations` table in database
- Implemented backend registration endpoints
- Updated frontend to call registration API

### 2. ✅ Unapproved Events Showing in Student Dashboard
**Problem:** Events not approved by admin (like "Tech talk for web devs") were appearing in student dashboard

**Solution:**
- Added `status` field to events table
- Modified GET /api/events to return only approved events for students
- Organizers and admins can see all events

### 3. ✅ No Admin Approval System
**Problem:** No way for admins to approve/reject events

**Solution:**
- Created AdminController with approval/rejection endpoints
- Added admin endpoints for event management

---

## 📊 Database Changes

### New Table: `event_registrations`
```sql
CREATE TABLE event_registrations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_registration (event_id, user_id)
);
```

### Events Table - New Field
```sql
ALTER TABLE events 
ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'pending' AFTER venue;
```

**Status Values:**
- `pending` - Event created, awaiting admin approval
- `approved` - Event approved by admin, visible to students
- `rejected` - Event rejected by admin

---

## 🔌 New Backend Endpoints

### Student Endpoints

#### 1. Register for Event
```http
POST /api/events/{id}/register
Authorization: Bearer <token>
```
**Response:**
```json
{
  "id": 123,
  "message": "Successfully registered for event",
  "event_title": "Tech talk for web devs"
}
```

**Validations:**
- User must be authenticated
- Event must exist
- Event must be approved
- User cannot register twice for same event

#### 2. Unregister from Event
```http
DELETE /api/events/{id}/register
Authorization: Bearer <token>
```
**Response:**
```json
{
  "message": "Successfully unregistered from event"
}
```

#### 3. Get Registered Events
```http
GET /api/events/registered
Authorization: Bearer <token>
```
**Response:**
```json
[
  {
    "id": 7,
    "title": "Tech talk for web devs",
    "description": "...",
    "organizerId": 2,
    "startTime": "2025-10-20T10:00:00",
    "endTime": "2025-10-20T12:00:00",
    "venue": "Auditorium",
    "status": "approved",
    "createdAt": "2025-10-15T10:00:00"
  }
]
```

#### 4. Get Event Registrations (Organizers/Admins)
```http
GET /api/events/{id}/registrations
Authorization: Bearer <token>
```
**Response:**
```json
{
  "count": 5,
  "registrations": [
    {
      "id": 1,
      "eventId": 7,
      "userId": 3,
      "registeredAt": "2025-10-16T10:30:00",
      "status": "active"
    }
  ]
}
```

### Admin Endpoints

#### 1. Get Pending Events
```http
GET /api/admin/events/pending
Authorization: Bearer <admin_token>
```
**Response:**
```json
[
  {
    "id": 7,
    "title": "Tech talk for web devs",
    "status": "pending",
    ...
  }
]
```

#### 2. Approve Event
```http
PUT /api/admin/events/{id}/approve
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "comments": "Event approved - meets all requirements"
}
```
**Response:**
```json
{
  "message": "Event approved successfully",
  "event_id": 7,
  "event_title": "Tech talk for web devs"
}
```

#### 3. Reject Event
```http
PUT /api/admin/events/{id}/reject
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "reason": "Venue not available for selected date"
}
```
**Response:**
```json
{
  "message": "Event rejected",
  "event_id": 7,
  "event_title": "Tech talk for web devs",
  "reason": "Venue not available for selected date"
}
```

---

## 🎨 Frontend Changes

### Student Dashboard (`student_dashboard.py`)

**Before:**
```python
def _register_event(self, event):
    messagebox.showinfo('Register', 
        f"Registration for '{event.get('title', 'Event')}' is not implemented yet.")
```

**After:**
```python
def _register_event(self, event):
    """Register for an event"""
    event_id = event.get('id')
    event_title = event.get('title', 'Event')
    
    # Validation checks
    if not event_id:
        messagebox.showerror('Error', 'Invalid event')
        return
    
    # Check if already registered
    if any(e.get('id') == event_id for e in self.registered_events):
        messagebox.showinfo('Already Registered', 
            f"You are already registered for '{event_title}'")
        return
    
    # Confirm registration
    if not messagebox.askyesno('Confirm Registration', 
            f"Do you want to register for '{event_title}'?"):
        return
    
    try:
        # Call registration endpoint
        response = self.api.post(f'events/{event_id}/register', {})
        messagebox.showinfo('Success', 
            f"Successfully registered for '{event_title}'!")
        
        # Reload data to refresh the view
        self._load_all_data_then(self._render_dashboard)
    except Exception as e:
        error_msg = str(e)
        if 'already registered' in error_msg.lower():
            messagebox.showinfo('Already Registered', 
                f"You are already registered for '{event_title}'")
        elif 'not approved' in error_msg.lower():
            messagebox.showerror('Error', 
                'This event is not yet approved by admin')
        else:
            messagebox.showerror('Error', f'Failed to register: {error_msg}')
```

**Features:**
- ✅ Proper validation
- ✅ Duplicate registration prevention
- ✅ Confirmation dialog
- ✅ Error handling with user-friendly messages
- ✅ Auto-refresh after successful registration

---

## 🔒 Security & Permissions

### Event Visibility
- **Students:** Can only see approved events
- **Organizers:** Can see all events (to manage their own)
- **Admins:** Can see all events (to approve/reject)

### Registration Permissions
- **All authenticated users** can register for approved events
- **Organizers** can view registrations for their events
- **Admins** can view all registrations

### Approval Permissions
- **Only Admins** can approve/reject events

---

## 🧪 Testing Guide

### Test 1: Student Cannot See Unapproved Events
1. Login as student (`student1@campus.com` / `test123`)
2. Go to "Browse Events"
3. **Expected:** "Tech talk for web devs" should NOT appear (status is pending)
4. **Expected:** Only "Valid Event" should appear (status is approved)

### Test 2: Student Registration Flow
1. Login as student
2. Browse events and find an approved event
3. Click "Register" button
4. Confirm registration in dialog
5. **Expected:** Success message appears
6. **Expected:** Event appears in "My Registrations"
7. Try to register again for same event
8. **Expected:** "Already Registered" message

### Test 3: Organizer View
1. Login as organizer (`organizer1@campus.com` / `test123`)
2. Go to "My Events"
3. **Expected:** Can see registrations count for their events
4. Click "View (N)" to see registered users
5. **Expected:** List of registered users appears

### Test 4: Admin Approval Flow
1. Login as admin (`admin@campus.com` / `test123`)
2. Go to "Event Approvals"
3. **Expected:** "Tech talk for web devs" appears in pending list
4. Click "Approve" button
5. **Expected:** Event approved successfully
6. Login as student again
7. **Expected:** "Tech talk for web devs" now appears in browse events

---

## 📝 New Java Classes

### 1. EventRegistration.java
```java
@Entity
public class EventRegistration {
    private int id;
    private int eventId;
    private int userId;
    private LocalDateTime registeredAt;
    private String status;
    // ... getters/setters
}
```

### 2. EventRegistrationDao.java
Methods:
- `findByUserId(int userId)` - Get user's registrations
- `findByEventId(int eventId)` - Get event's registrations
- `findByEventAndUser(int eventId, int userId)` - Check if registered
- `create(EventRegistration)` - Create registration
- `delete(int eventId, int userId)` - Delete registration
- `countByEventId(int eventId)` - Count registrations

### 3. AdminController.java
Endpoints:
- `GET /api/admin/events/pending` - Get pending events
- `PUT /api/admin/events/{id}/approve` - Approve event
- `PUT /api/admin/events/{id}/reject` - Reject event

---

## 🔄 Event Lifecycle

```
┌─────────────────────┐
│  Organizer Creates  │
│      Event          │
└──────────┬──────────┘
           │
           ▼
      ┌─────────┐
      │ PENDING │ ◄─── Not visible to students
      └────┬────┘
           │
           ▼
    ┌──────────────┐
    │ Admin Review │
    └──────┬───────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
┌──────────┐  ┌──────────┐
│ APPROVED │  │ REJECTED │
└────┬─────┘  └──────────┘
     │
     │ Visible to students
     │
     ▼
┌─────────────────────┐
│ Students Register   │
└─────────────────────┘
```

---

## 🎉 Summary of Changes

### Database (1 new table + 1 field)
- ✅ Added `status` field to `events` table
- ✅ Created `event_registrations` table
- ✅ Added indexes for performance

### Backend (3 new classes + 8 endpoints)
- ✅ Created `EventRegistration` model
- ✅ Created `EventRegistrationDao` 
- ✅ Created `AdminController`
- ✅ Updated `Event` model with status field
- ✅ Updated `EventDao` with status support
- ✅ Updated `EventController` with 4 new endpoints
- ✅ Added 3 admin endpoints

### Frontend (1 update)
- ✅ Updated `student_dashboard.py` registration function
- ✅ Added proper error handling
- ✅ Added confirmation dialogs
- ✅ Auto-refresh after registration

---

## 🚀 Quick Start

### 1. Start the System
```bash
cd /Users/garinesaiajay/Desktop/CampusEventSystem
./run.sh
```

### 2. Test Student Registration
```bash
# Login as: student1@campus.com / test123
# Browse events
# Register for approved events
```

### 3. Test Admin Approval
```bash
# Login as: admin@campus.com / test123
# Go to Event Approvals
# Approve "Tech talk for web devs"
```

---

## 📞 API Testing with cURL

### Register for Event
```bash
curl -X POST http://localhost:8080/api/events/7/register \
  -H "Authorization: Bearer <student_token>" \
  -H "Content-Type: application/json"
```

### Get Registered Events
```bash
curl -X GET http://localhost:8080/api/events/registered \
  -H "Authorization: Bearer <student_token>"
```

### Approve Event (Admin)
```bash
curl -X PUT http://localhost:8080/api/admin/events/7/approve \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"comments": "Approved"}'
```

---

## ✅ All Requirements Met

1. ✅ **Registration Implementation:** Students can now register for events
2. ✅ **Admin Approval Filter:** Only approved events show in student dashboard
3. ✅ **Event Status:** "Tech talk for web devs" is now pending (unapproved)
4. ✅ **API Endpoints:** All registration and approval endpoints created
5. ✅ **Frontend Integration:** Registration button now works properly
6. ✅ **Organizer Dashboard:** Registrations reflect in organizer dashboard
7. ✅ **Error Handling:** Proper validation and error messages

---

## 📚 Related Files

- `/database_sql/add_event_status_and_registrations.sql` - Migration script
- `/backend_java/.../model/EventRegistration.java` - Registration model
- `/backend_java/.../dao/EventRegistrationDao.java` - Registration DAO
- `/backend_java/.../controller/EventController.java` - Updated with registration endpoints
- `/backend_java/.../controller/AdminController.java` - Admin approval endpoints
- `/frontend_tkinter/pages/student_dashboard.py` - Updated registration function

---

**Implementation Date:** October 16, 2025  
**Status:** ✅ Complete and Tested  
**Backend Restart Required:** Yes (already done)  
**Database Migration Required:** Yes (already done)
