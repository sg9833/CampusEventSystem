# 🧪 Quick Test Guide - Events Disappearing Bug Fix

## ✅ Test the Fix Right Now

### **Prerequisites:**
- Backend is running on `http://localhost:8080`
- Frontend is running (Python Tkinter app)
- You have test accounts:
  - Organizer: `organizer1@campus.com` / `test123`
  - Admin: `admin@campus.com` / `admin123`

---

## 🎯 Test Scenario: The Exact Bug You Reported

### **Step 1: Login as Organizer and Create Event**
1. Open the frontend application
2. Click **Login**
3. Enter credentials:
   - Email: `organizer1@campus.com`
   - Password: `test123`
4. Click **Login** button
5. You should see **Organizer Dashboard**
6. Click **"Create Event"** in the sidebar
7. Fill in the form:
   - **Title:** `Test Event ABCD`
   - **Description:** `Testing if events disappear after logout`
   - **Start Time:** Any future date/time
   - **End Time:** Any future date/time (after start)
   - **Venue:** `Main Hall`
8. Click **"Create Event"** button
9. ✅ You should see: **"Event created successfully and pending approval"**

### **Step 2: Check My Events Before Logout**
1. In the sidebar, click **"My Events"**
2. ✅ You should see **"Test Event ABCD"** in the list with status **"pending"**
3. ✅ Note the event ID and details

### **Step 3: Logout**
1. Click **"Logout"** button in the sidebar
2. Confirm logout
3. ✅ You should be redirected to the **Login page**

### **Step 4: Login as Admin**
1. Enter credentials:
   - Email: `admin@campus.com`
   - Password: `admin123`
2. Click **Login** button
3. ✅ You should see **Admin Dashboard**
4. In the sidebar, click **"Event Approvals"** or **"Manage Events"**
5. Filter by **"Pending"** events
6. ✅ You should see **"Test Event ABCD"** with status **"pending"**
7. ✅ **THIS CONFIRMS THE FIX!** Previously, pending events were not visible to admin

### **Step 5: Logout Admin**
1. Click **"Logout"** button
2. Confirm logout
3. ✅ Back to Login page

### **Step 6: Login as Organizer Again**
1. Enter credentials:
   - Email: `organizer1@campus.com`
   - Password: `test123`
2. Click **Login** button
3. ✅ You should see **Organizer Dashboard**
4. In the sidebar, click **"My Events"**
5. ✅ **CRITICAL CHECK:** You should see **"Test Event ABCD"** in your events list
6. ✅ **THIS CONFIRMS THE FIX!** Previously, the event would disappear after re-login

---

## 🎉 Success Criteria

✅ **PASS:** If you can see your created event in "My Events" after logging back in  
❌ **FAIL:** If the event disappears from "My Events" after re-login

---

## 🐛 If Test Fails

### **Check Backend Logs:**
```bash
tail -f /tmp/backend.log
```

### **Look for:**
- JWT token validation errors
- Role-based filtering logs
- Event retrieval queries

### **Check Frontend Console:**
1. Look for error messages
2. Check if API calls are succeeding
3. Verify JWT token is being sent

### **Verify Database:**
```sql
-- Check if event was created
SELECT id, title, organizer_id, status FROM events WHERE title LIKE '%ABCD%';

-- Check user roles
SELECT id, email, role FROM users WHERE email IN ('organizer1@campus.com', 'admin@campus.com');
```

---

## 📱 Expected API Behavior

### **When Organizer Calls GET /api/events:**
```json
// Request
GET http://localhost:8080/api/events
Authorization: Bearer <organizer_jwt_token>

// Response (should include pending events!)
[
  {
    "id": 10,
    "title": "Test Event ABCD",
    "description": "Testing if events disappear after logout",
    "organizerId": 2,
    "startTime": "2025-11-10T10:00:00",
    "endTime": "2025-11-10T12:00:00",
    "venue": "Main Hall",
    "status": "pending",  // ← THIS IS KEY!
    "createdAt": "2025-11-04T12:30:00"
  },
  // ... other events
]
```

### **When Admin Calls GET /api/admin/events/pending:**
```json
// Request
GET http://localhost:8080/api/admin/events/pending
Authorization: Bearer <admin_jwt_token>

// Response
[
  {
    "id": 10,
    "title": "Test Event ABCD",
    "status": "pending",
    "organizerId": 2,
    // ...
  }
]
```

---

## ✅ Quick Backend Test (Using curl)

### **Test 1: Login as Organizer**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"organizer1@campus.com","password":"test123"}'
```

**Save the token from response!**

### **Test 2: Create Event**
```bash
ORGANIZER_TOKEN="<paste_token_here>"

curl -X POST http://localhost:8080/api/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ORGANIZER_TOKEN" \
  -d '{
    "title": "Quick Test Event",
    "description": "Testing from curl",
    "organizerId": 2,
    "startTime": "2025-11-10T10:00:00",
    "endTime": "2025-11-10T12:00:00",
    "venue": "Test Hall"
  }'
```

### **Test 3: Get All Events as Organizer**
```bash
curl -X GET http://localhost:8080/api/events \
  -H "Authorization: Bearer $ORGANIZER_TOKEN"
```

**Should see the event you just created (even though it's pending)!**

### **Test 4: Login as Admin**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@campus.com","password":"admin123"}'
```

**Save admin token!**

### **Test 5: Get Pending Events as Admin**
```bash
ADMIN_TOKEN="<paste_admin_token_here>"

curl -X GET http://localhost:8080/api/admin/events/pending \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

**Should see pending events including the one you created!**

---

## 🚀 What Was Fixed?

### **Before the Fix:**
```java
// ❌ Case-sensitive comparison
if (user != null && "STUDENT".equals(user.getRole())) {
    return ResponseEntity.ok(eventDao.findApproved());
}
return ResponseEntity.ok(eventDao.findAll());
```

**Problem:** If there were any role mismatches or case differences, organizers might only see approved events, hiding their pending events.

### **After the Fix:**
```java
// ✅ Case-insensitive comparison
if (user != null && "STUDENT".equalsIgnoreCase(user.getRole())) {
    return ResponseEntity.ok(eventDao.findApproved());
}
return ResponseEntity.ok(eventDao.findAll());
```

**Solution:** Now works regardless of how roles are stored in the database (uppercase, lowercase, or mixed case).

---

## 📞 Need Help?

If the test still fails:
1. Check `/tmp/backend.log` for errors
2. Verify database has the event
3. Check JWT token is valid
4. Ensure backend is running on port 8080
5. Review `CRITICAL_BUG_FIX_EVENTS_DISAPPEARING.md` for more details

---

**Happy Testing! 🎉**
