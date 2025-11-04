# Quick Test: Booking Approval System

## ✅ Implementation Complete

All three components of the booking approval system have been implemented and the backend has been rebuilt and restarted.

## What Was Fixed

### 1. Frontend (book_resource.py)
- ✅ Fixed data format to match backend expectations
- ✅ Now sends: `userId`, `resourceId`, `startTime`, `endTime` in ISO-8601 format
- ✅ Increased Submit button width to 300px

### 2. Backend DAO (BookingDao.java)
- ✅ Added `findPendingBookings()` - Get all pending bookings
- ✅ Added `findById(int id)` - Get specific booking
- ✅ Added `updateStatus(int id, String status)` - Update booking status

### 3. Backend Controller (AdminController.java)
- ✅ Added `GET /api/admin/bookings/pending` - View pending bookings
- ✅ Added `PUT /api/admin/bookings/{id}/approve` - Approve booking
- ✅ Added `PUT /api/admin/bookings/{id}/reject` - Reject booking (with optional reason)

### 4. Backend Status
- ✅ Backend rebuilt successfully (mvn clean package)
- ✅ Backend restarted with new endpoints
- ✅ Running on port 8080

## Quick Test Steps

### Step 1: Test Booking Submission (Organizer)

**Login as:** `organizer1@campus.com` / `organizer123`

1. Go to "Booking Resources"
2. Click "Book Now" on Projector
3. Fill form:
   - Date: Tomorrow's date
   - Start Time: 10:00
   - End Time: 12:00
   - Purpose: "Test booking"
   - Attendees: 10
   - Priority: Medium
4. Click "Submit Booking Request"

**Expected:** Success message, no errors

### Step 2: Test API Directly (Optional)

```bash
# Login as admin to get JWT token
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@campus.com","password":"admin123"}'

# Copy the token from response, then:
curl -X GET http://localhost:8080/api/admin/bookings/pending \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Expected:** JSON array with pending bookings

### Step 3: Check Database

```sql
-- See all bookings
SELECT * FROM bookings ORDER BY created_at DESC LIMIT 5;

-- See pending bookings only
SELECT b.id, u.username, r.name, b.start_time, b.end_time, b.status
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN resources r ON b.resource_id = r.id
WHERE b.status = 'pending';
```

### Step 4: Test Approval (When Admin Frontend Ready)

**Login as:** `admin@campus.com` / `admin123`

1. Navigate to admin dashboard
2. Look for "Resource Requests" or "Pending Bookings"
3. Click "Approve" on a pending booking

**Expected:** Status updates to 'approved' in database

## API Endpoints Summary

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/api/bookings` | Submit new booking | User |
| GET | `/api/bookings/my` | Get user's bookings | User |
| GET | `/api/admin/bookings/pending` | Get pending bookings | Admin |
| PUT | `/api/admin/bookings/{id}/approve` | Approve booking | Admin |
| PUT | `/api/admin/bookings/{id}/reject` | Reject booking | Admin |

## Current Status

✅ **READY FOR TESTING**

All backend changes are implemented and running. You can now:

1. Test booking submission through the frontend
2. Test pending bookings API endpoint
3. Test approve/reject endpoints via curl
4. Integrate with admin dashboard frontend (if needed)

## Verify Backend is Running

```bash
# Check if backend is running
curl http://localhost:8080/api/health 2>/dev/null || echo "Backend not responding"

# Check if port 8080 is in use
lsof -ti:8080
```

## Next Action

**Test the complete flow:**
1. Submit a booking as organizer1@campus.com
2. Verify it appears with status='pending' in database
3. Call GET /api/admin/bookings/pending as admin
4. Call PUT /api/admin/bookings/{id}/approve as admin
5. Verify status changed to 'approved'

---

**All code changes complete. Backend restarted. System ready for testing! 🚀**
