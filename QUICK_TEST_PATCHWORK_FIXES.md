# Quick Testing Guide - Patchwork Fixes

## How to Test All 4 Fixes

### Prerequisites
1. Start the application: `./run_app.sh`
2. Have test credentials ready:
   - Student: `ajay.test@test.com` / `test123`
   - Or use any other valid credentials

---

## 🧪 Test 1: Active Bookings Card Removed

**Steps:**
1. Login as a **student** (e.g., `ajay.test@test.com` / `test123`)
2. Navigate to Dashboard (should already be there after login)

**Expected Result:**
✅ Should see only **2 cards** at the top:
   - "Total Events" (left)
   - "Registered Events" (right)

❌ Should **NOT** see:
   - "Active Bookings" card

**Status:** `PASS / FAIL`

---

## 🧪 Test 2: Scrolling with Trackpad/Mousewheel

**Test on 3 pages:**

### A. Student Dashboard
1. Login as student
2. Go to Dashboard
3. Try scrolling with:
   - Two-finger swipe up/down (macOS trackpad)
   - Mousewheel (if using mouse)

**Expected:** ✅ Page scrolls smoothly

### B. Profile Page
1. Click "Profile Settings" in sidebar
2. Try scrolling with trackpad/mousewheel
3. Switch to "Account Settings" tab
4. Try scrolling again

**Expected:** ✅ Both tabs scroll smoothly

### C. Notifications Page
1. Click "🔔" icon in top-right navigation bar
2. Try scrolling with trackpad/mousewheel

**Expected:** ✅ Notifications list scrolls smoothly

**Overall Status:** `PASS / FAIL`

---

## 🧪 Test 3: Profile Data Correctness

**Test with multiple users:**

### User 1: Student (ajay.test@test.com)
1. Logout if logged in
2. Login as: `ajay.test@test.com` / `test123`
3. Navigate to "Profile Settings"
4. Check displayed data:
   - Name
   - Email
   - Username
   - Role
   - Department (if any)

**Expected:** ✅ All data matches Ajay's account

### User 2: Different Account
1. Logout
2. Login as a different user (student/organizer/admin)
3. Navigate to "Profile Settings"
4. Check displayed data

**Expected:** ✅ Data matches the NEW logged-in user, NOT Ajay's data

### Verification Points:
- [ ] Email address is correct for current user
- [ ] Username is correct for current user
- [ ] Role is correct (student/organizer/admin)
- [ ] No data from previous user is shown

**Status:** `PASS / FAIL`

---

## 🧪 Test 4: Notifications Page

### A. Button Visibility (macOS)
1. Click "🔔" icon to open notifications
2. Check if all buttons are visible:
   - "🔄 Refresh" button (gray, top-right)
   - "✓ Mark All Read" button (blue, top-right)
   - "All" button (blue, below count)
   - "Unread" button (gray, below count)
   - "Read" button (gray, below count)

**Expected:** ✅ All buttons visible with correct colors

### B. Loading Issue
1. Open Notifications page
2. Observe loading behavior

**Expected:** ✅ Page loads within 1-2 seconds
**Expected:** ✅ Shows notifications (sample data if API fails)
❌ Should **NOT** be stuck on "Loading notifications..." forever

### C. Button Functionality
1. Click "Unread" button
   - **Expected:** ✅ Button turns blue, shows unread notifications
2. Click "Read" button
   - **Expected:** ✅ Button turns blue, shows read notifications
3. Click "All" button
   - **Expected:** ✅ Button turns blue, shows all notifications
4. Click "🔄 Refresh" button
   - **Expected:** ✅ Refreshes notification list

**Status:** `PASS / FAIL`

---

## Summary Report

| Test | Status | Notes |
|------|--------|-------|
| 1. Active Bookings Removed | ☐ | |
| 2. Scrolling Works | ☐ | |
| 3. Profile Data Correct | ☐ | |
| 4. Notifications Fixed | ☐ | |

---

## If Any Test Fails

### Active Bookings Still Shows
- Check: `frontend_tkinter/pages/student_dashboard.py` line ~210
- Should have only 2 cards, not 3

### Scrolling Not Working
- Check: Canvas widget has `bind_mousewheel()` called
- Try restarting the application
- Verify you're using trackpad/mousewheel correctly

### Profile Shows Wrong Data
- Check: `frontend_tkinter/pages/profile_page.py` line ~125
- Verify session token is set correctly after login
- Try logout and login again

### Notifications Stuck Loading
- Check: Internet connection (API might be down)
- Sample data should still load even if API fails
- Check console for error messages

---

## Quick Fix Commands

If application is not running:
```bash
cd /Users/garinesaiajay/Desktop/CampusEventSystem
./run_app.sh
```

If you need to restart:
```bash
./stop.sh
./run_app.sh
```

---

**Testing Date:** __________  
**Tester:** __________  
**Platform:** macOS / Windows / Linux  
**Overall Result:** PASS / FAIL
