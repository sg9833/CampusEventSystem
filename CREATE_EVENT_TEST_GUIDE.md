# 🧪 CREATE EVENT - TESTING GUIDE

## ✅ All Fixes Applied

1. ✅ Added `organizerId` from session
2. ✅ Fixed field names (camelCase: `startTime`, `endTime`)
3. ✅ Fixed datetime format (ISO 8601 with T)
4. ✅ Fixed session key issue (`user_id` vs `id`)

---

## 🎯 TESTING STEPS

### Step 1: Login 👤

You should see a login window. Enter:

```
Email:    organizer1@campus.com
Password: test123
```

**Click LOGIN**

✅ You should be redirected to the Organizer Dashboard

---

### Step 2: Navigate to Create Event 📝

You should already be on the dashboard. Look for the form that shows:
- Event Title
- Description
- Start Time
- End Time
- Venue
- Capacity

**Note:** The time fields should already have placeholder values:
- Start Time: `2025-10-20 09:00:00`
- End Time: `2025-10-20 17:00:00`

---

### Step 3: Fill in the Form ✍️

#### Option A: Quick Test (Use defaults)
Just change these two fields:

**Event Title:**
```
Test Event - Fixed Version
```

**Description:**
```
This is a test event to verify that the create event functionality works correctly after fixing the 403 error and session issues.
```

**Leave the rest as defaults** (times, venue, capacity)

**Add a venue:**
```
Main Auditorium
```

#### Option B: Custom Test
Fill in your own values, but make sure:
- Title: At least 3 characters
- Description: At least 10 characters
- Start Time: Future date in format `YYYY-MM-DD HH:MM:SS`
- End Time: After start time in format `YYYY-MM-DD HH:MM:SS`
- Venue: Required

---

### Step 4: Click "Create Event" 🚀

**Click the "Create Event" button**

---

## ✅ Expected Results

### Success Scenario:

You should see a **success popup**:

```
┌─────────────────────────────────────┐
│          Success                    │
├─────────────────────────────────────┤
│                                     │
│  Event 'Test Event - Fixed Version' │
│  created successfully!              │
│                                     │
│           [ OK ]                    │
└─────────────────────────────────────┘
```

**Then:**
- The form should clear
- You'll be redirected to "My Events" page
- Your new event should appear in the events list

---

## ❌ If You Still See Errors

### Error: "User session not found"
**This should NOT happen anymore!**

If you still see this:
1. Close the app completely
2. Run: `./stop.sh`
3. Run: `./run.sh`
4. Login again
5. Try creating event again

### Error: "Failed to create event: HTTP error: 403"
**This should NOT happen anymore!**

If you still see this:
1. Check if you're logged in as organizer (not student)
2. Make sure backend is running: `ps aux | grep java`
3. Try the API test: `python3.11 test_create_event.py`

### Error: "Failed to create event: HTTP error: 500"
This means validation or server error. Check:
- Start time is in future
- End time is after start time
- All required fields are filled
- Times are in correct format

### Error: Other validation errors
- Make sure title is 3-255 characters
- Make sure description is 10-5000 characters
- Make sure times are in format: `YYYY-MM-DD HH:MM:SS`

---

## 🔍 Verification Checklist

After creating the event:

- [ ] Success message appeared
- [ ] No error messages
- [ ] Redirected to "My Events" page
- [ ] New event visible in events list
- [ ] Event shows correct title
- [ ] Event shows correct date/time
- [ ] Event shows "Pending" status (waiting for admin approval)

---

## 🧪 Alternative: API Test

If GUI doesn't work, try the API directly:

```bash
cd /Users/garinesaiajay/Desktop/CampusEventSystem
python3.11 test_create_event.py
```

**Expected output:**
```
✅ Login successful!
   User ID: 2

✅ Event created successfully!
   Event ID: 5
   Message: Event created successfully

✅ TEST PASSED - Create Event is working!
```

---

## 📊 What's Being Sent

When you click "Create Event", this payload is sent:

```json
{
  "title": "Test Event - Fixed Version",
  "description": "This is a test event...",
  "organizerId": 2,
  "startTime": "2025-10-20T09:00:00",
  "endTime": "2025-10-20T17:00:00",
  "venue": "Main Auditorium"
}
```

**Note:** Capacity field is NOT sent (backend doesn't support it yet)

---

## 🆘 Still Having Issues?

Run these diagnostic commands:

### 1. Check backend is running:
```bash
curl http://localhost:8080/actuator/health
```
Should return: `{"status":"UP"}`

### 2. Check session diagnostic:
```bash
python3.11 test_session_diagnostic.py
```
Should show: `✅ User ID found: 2`

### 3. Check backend logs:
```bash
tail -50 backend.log
```

### 4. Check frontend logs:
Look at the terminal where frontend is running for error messages

---

## 📝 Test Summary Form

Fill this out after testing:

```
Date/Time: _______________
Tester: ___________________

Login:
[ ] Successful login as organizer1@campus.com
[ ] Redirected to dashboard

Create Event:
[ ] Form visible with all fields
[ ] Placeholder values present
[ ] Able to fill in all fields
[ ] "Create Event" button clickable

Result:
[ ] Success message appeared
[ ] Event created (ID: ____)
[ ] Redirected to My Events
[ ] Event visible in list

Errors Encountered:
_________________________________
_________________________________

Status: [ ] PASS  [ ] FAIL
```

---

## 🎉 Success Criteria

Test is **PASSED** if:
1. ✅ Login works
2. ✅ Form is accessible
3. ✅ Can fill in all fields
4. ✅ "Create Event" button works
5. ✅ Success message appears
6. ✅ Event is created (visible in "My Events")
7. ✅ No error popups

---

**Ready to test? Login and create your first event!** 🚀

**Current Status:** Frontend is running, waiting for your login!
