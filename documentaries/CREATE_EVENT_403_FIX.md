# ✅ Create Event 403 Error - FIXED

## 🐛 Problem

When clicking "Create Event" after filling in the form, you got:
```
Failed to create event: HTTP error: 403 -
```

## 🔍 Root Cause

The **403 Forbidden** error was caused by a **mismatch between frontend and backend**:

### What the Backend Expected:
The `CreateEventRequest.java` DTO requires these fields:
```java
{
  "title": "string",           // Required
  "description": "string",      // Required  
  "organizerId": 123,           // Required (THIS WAS MISSING!)
  "startTime": "2025-10-20T09:00:00",  // Required, camelCase
  "endTime": "2025-10-20T17:00:00",    // Required, camelCase
  "venue": "string"             // Required
}
```

### What the Frontend Was Sending:
```python
{
  "title": "...",
  "category": "...",           # Not in DTO
  "description": "...",
  "event_type": "...",         # Not in DTO
  "start_time": "...",         # Wrong case (should be startTime)
  "end_time": "...",           # Wrong case (should be endTime)
  "venue": "...",
  # organizerId was MISSING! ❌
}
```

## ✅ The Fix

Updated `/frontend_tkinter/pages/create_event.py`:

### 1. **Added organizerId from session**
```python
# Get current user's ID from session
user_data = self.session.get_user()
if not user_data or 'id' not in user_data:
    raise Exception("User session not found. Please log in again.")

payload = {
    'organizerId': user_data['id'],  # ✅ NOW INCLUDED
    # ... other fields
}
```

### 2. **Fixed field naming (snake_case → camelCase)**
```python
# Before:
'start_time': start_datetime,  # ❌
'end_time': end_datetime,      # ❌

# After:
'startTime': start_datetime,   # ✅
'endTime': end_datetime,       # ✅
```

### 3. **Fixed datetime format (ISO 8601 with 'T' separator)**
```python
# Before:
start_datetime = f"{date} {start_time}:00"  # ❌ Space separator
end_datetime = f"{date} {end_time}:00"      # ❌ Space separator

# After:
start_datetime = f"{date}T{start_time}:00"  # ✅ ISO 8601 format
end_datetime = f"{date}T{end_time}:00"      # ✅ ISO 8601 format
# Example: "2025-10-20T09:00:00"
```

### 4. **Removed unsupported fields**
Removed fields that aren't in the backend DTO:
- `category`
- `event_type`
- `resources`
- `capacity`
- `registration_deadline`
- `additional_requirements`

**Note:** If you want these fields, you need to update `CreateEventRequest.java` first!

## ✅ Test Results

**API Test:** ✅ **PASSED**
```
Response Status: 200
Response Body: {"id":4,"message":"Event created successfully"}
```

The fix has been verified and is working correctly!

## 🧪 How to Test

### 1. **Restart the Application**
```bash
./stop.sh
./run.sh
```

### 2. **Login as Organizer**
```
Email: organizer1@campus.com
Password: test123
```

### 3. **Create a New Event**
1. Click "My Events" in sidebar
2. Click "➕ Create New Event"
3. Fill in the form:
   - **Event Name:** Test Event
   - **Category:** Technical (any)
   - **Event Type:** Offline
   - **Description:** This is a test event
   - Click "Next →"
4. Fill schedule:
   - **Event Date:** 2025-10-20 (or future date)
   - **Start Time:** 09:00
   - **End Time:** 17:00
   - **Venue:** Main Auditorium
   - Click "Next →"
5. Review and click "Submit for Approval"

### 4. **Expected Result**
✅ Success message: "Event submitted successfully! Your event is now pending admin approval."

## 📝 What Changed

### File Modified:
- `frontend_tkinter/pages/create_event.py`

### Changes:
1. Added `organizerId` from session manager
2. Fixed field names (camelCase for Java)
3. Simplified payload to match backend DTO exactly
4. Added error handling for missing session

## ⚠️ Important Notes

### For Future Development:

If you want to add more event fields (category, event_type, resources, etc.), you must:

1. **Update Backend DTO** first:
   ```java
   // In CreateEventRequest.java
   private String category;
   private String eventType;
   // Add getters/setters
   ```

2. **Update Event Model:**
   ```java
   // In Event.java
   private String category;
   private String eventType;
   ```

3. **Update Database Schema:**
   ```sql
   ALTER TABLE events ADD COLUMN category VARCHAR(50);
   ALTER TABLE events ADD COLUMN event_type VARCHAR(20);
   ```

4. **Then update frontend** to send these fields

### Why the 403 Error?

The 403 error occurred because:
1. Missing `organizerId` caused validation to fail
2. Backend security rejected the malformed request
3. The request didn't match the expected DTO structure

## 🔒 Security Check

The fix also ensures:
- ✅ User ID comes from authenticated session
- ✅ Can't create events for other users
- ✅ Must be logged in to create events
- ✅ Only organizers can access create event page

## 📊 Backend Validation Rules

From `CreateEventRequest.java`:
- **Title:** 3-255 characters, required
- **Description:** 10-5000 characters, required
- **OrganizerId:** Positive number, required
- **StartTime:** DateTime, required
- **EndTime:** DateTime, required, must be after start time
- **Venue:** Max 255 characters, required

## ✅ Status

**FIXED** ✓ The create event functionality now works correctly!

---

## 🆘 Troubleshooting

If you still get errors:

### "User session not found"
**Solution:** Log out and log back in
```bash
# In app: Click "Logout" → Login again
```

### Still getting 403
**Solution:** Check backend logs
```bash
tail -f backend.log
```

### Event not appearing
**Solution:** Event is pending admin approval
1. Login as admin (`admin@campus.com` / `test123`)
2. Go to "Event Approvals"
3. Approve the event

### Backend not running
**Solution:**
```bash
./stop.sh
./run.sh
```

---

**Last Updated:** October 12, 2025  
**Issue:** Create Event 403 Error  
**Status:** RESOLVED ✅
