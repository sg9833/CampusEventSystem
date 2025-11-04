# 🧪 Quick Test Guide - Edit Event & Display Fixes

## ⚡ Fast Testing (5 minutes)

### Test 1: View Event Details (Fixed Display)
```bash
1. Run frontend: python3 frontend_tkinter/main.py
2. Login: organizer1@campus.com / password
3. Click "My Events" tab
4. Click "View Details" on "abcd" event
5. ✅ Check: Start and End times show correctly (not "N/A")
6. ✅ Check: Registration count is accurate
```

### Test 2: Edit Event Form
```bash
1. Still on "My Events" tab
2. Click "Edit" button on "abcd" event
3. ✅ Check: Modal opens with pre-filled data
4. Make changes:
   - Change title to "abcd - UPDATED"
   - Change venue to "New Location"
5. Click "Save Changes"
6. ✅ Check: Success message appears
7. ✅ Check: Event shows as "Pending" in list
```

### Test 3: Admin Re-Approval
```bash
1. Logout from organizer account
2. Login: admin@campus.com / password
3. Click "Pending Approvals" tab
4. ✅ Check: "abcd - UPDATED" appears in pending list
5. Click "Approve"
6. ✅ Check: Event approved successfully
```

### Test 4: Student Sees Updated Event
```bash
1. Logout from admin account
2. Login: student1@campus.com / password
3. Click "Browse Events" tab
4. ✅ Check: "abcd - UPDATED" appears with new venue
5. ✅ Check: Can register for the updated event
```

---

## 🔍 Validation Testing (2 minutes)

### Test Invalid Inputs:
```bash
1. Login as organizer1@campus.com
2. Click Edit on any event
3. Try these:
   - Clear title → Error: "Title must be at least 3 characters"
   - Clear description → Error: "Description must be at least 10 characters"
   - Clear venue → Error: "Venue is required"
   - Enter "abc" in date field → Error: "Invalid date/time format"
   - Enter "25:99" in time field → Error: "Invalid date/time format"
4. ✅ All validations working correctly
```

---

## 🔒 Security Testing (3 minutes)

### Test Permission Checks:
```bash
1. Get event ID and organizer2 token:
   curl -X POST http://localhost:8080/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"organizer2@campus.com","password":"password"}'
   
   # Copy the token

2. Try to edit organizer1's event:
   curl -X PUT http://localhost:8080/api/events/13 \
     -H "Authorization: Bearer ORGANIZER2_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Hacked Event",
       "description": "This should not work",
       "organizerId": 3,
       "startTime": "2025-12-01T10:00:00",
       "endTime": "2025-12-01T14:00:00",
       "venue": "Hacked Venue"
     }'
   
   # ✅ Should return 403 Forbidden
```

---

## 📱 Backend Health Check

```bash
# Check if backend is running
curl http://localhost:8080/api/events

# Check specific endpoint (needs auth)
curl -X GET http://localhost:8080/api/events \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test PUT endpoint
curl -X PUT http://localhost:8080/api/events/13 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Updated Title",
    "description": "Test updated description with more details",
    "organizerId": 2,
    "startTime": "2025-12-01T10:00:00",
    "endTime": "2025-12-01T14:00:00",
    "venue": "Test Updated Venue"
  }'
```

---

## ✅ Expected Results Checklist

### Display Fixes:
- [ ] Start time shows correctly (not "N/A")
- [ ] End time shows correctly (not "N/A")
- [ ] Times formatted nicely (space instead of 'T')
- [ ] Registration count accurate

### Edit Functionality:
- [ ] Edit button opens form
- [ ] All fields pre-filled with current data
- [ ] Can modify all fields
- [ ] Validation works for all fields
- [ ] Save button triggers update
- [ ] Success message appears
- [ ] Event list refreshes

### Re-Approval Workflow:
- [ ] Edited event status changes to "pending"
- [ ] Event appears in admin pending list
- [ ] Admin can approve edited event
- [ ] After approval, event visible to students
- [ ] Updated details show correctly

### Security:
- [ ] Only organizer can edit their own events
- [ ] Other organizers get 403 error
- [ ] Students cannot edit events
- [ ] Admin cannot edit (only approve/reject)

---

## 🐛 Common Issues & Solutions

### Issue: Edit button still shows "coming soon"
**Solution:** Make sure frontend was restarted after code changes

### Issue: 403 error when trying to edit
**Solution:** Check that JWT token is valid and user is the event organizer

### Issue: Times still show "N/A"
**Solution:** Backend must return camelCase (startTime, endTime). Check backend logs.

### Issue: Event doesn't refresh after edit
**Solution:** Check that `_load_all_data_then()` is being called after successful edit

### Issue: Backend 404 error
**Solution:** Verify backend is running on port 8080. Check with `curl http://localhost:8080/api/events`

---

## 🎯 Quick Success Criteria

**All features working if:**
1. ✅ Event details show correct start/end times
2. ✅ Edit form opens with pre-filled data
3. ✅ Can save changes successfully
4. ✅ Event goes to pending status
5. ✅ Admin can see and approve edited event
6. ✅ Students see updated event details
7. ✅ Validation prevents invalid inputs
8. ✅ Security prevents unauthorized edits

---

## 📞 Test Credentials

```
Organizer 1:
  Email: organizer1@campus.com
  Password: password

Organizer 2:
  Email: organizer2@campus.com
  Password: password

Admin:
  Email: admin@campus.com
  Password: password

Student 1:
  Email: student1@campus.com
  Password: password
```

---

## 🚀 Start Testing Now!

```bash
# Terminal 1: Check backend is running
curl http://localhost:8080/api/events

# Terminal 2: Start frontend
cd /Users/garinesaiajay/Desktop/CampusEventSystem
python3 frontend_tkinter/main.py

# Then follow Test 1-4 above!
```

**Estimated Testing Time:** 10-15 minutes for complete workflow ✅
