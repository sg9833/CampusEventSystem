# ✅ SYSTEM IS READY - Test Username & Email Login!

## 🎉 Current Status

✅ **Database:** Migrated with username column  
✅ **Backend:** Running on port 8080  
✅ **Frontend:** Running and showing login page  

---

## 🧪 TEST PLAN

### Test 1: Register New User with Username
1. Click **"Register"** link on login page
2. Fill in the form:
   ```
   Full Name:       Alice Johnson
   Email:           alice.j@university.edu
   Phone Number:    5550123456
   Username:        alicej
   Password:        Alice@123
   Confirm Password: Alice@123
   Role:            STUDENT (default)
   Department:      Computer Science
   ✅ Terms & Conditions
   ```
3. Click **"REGISTER"**
4. **Expected Result:** 
   - ✅ Success message appears
   - ✅ Auto-login with JWT token
   - ✅ Redirected to Student Dashboard

---

### Test 2: Login with EMAIL
1. If you were auto-logged in, **logout** first
2. You'll be back at login page (it now says "Email or Username")
3. Enter:
   ```
   Email or Username: alice.j@university.edu
   Password:          Alice@123
   ```
4. Click **"LOGIN"**
5. **Expected Result:**
   - ✅ Login successful
   - ✅ Redirected to Student Dashboard

---

### Test 3: Login with USERNAME
1. **Logout** from dashboard
2. On login page, enter:
   ```
   Email or Username: alicej
   Password:          Alice@123
   ```
3. Click **"LOGIN"**
4. **Expected Result:**
   - ✅ Login successful
   - ✅ Redirected to Student Dashboard

---

## 🎯 Additional Test Data

### User 2 (Organizer)
**Registration:**
```
Full Name:       Bob Wilson
Email:           bob.w@university.edu
Phone Number:    5550234567
Username:        bobw
Password:        Bob@2024
Role:            ORGANIZER
Department:      Event Management
```

**Login Options:**
- Email: `bob.w@university.edu` + `Bob@2024`
- Username: `bobw` + `Bob@2024`

---

### User 3 (Another Student)
**Registration:**
```
Full Name:       Sarah Martinez
Email:           sarah.m@university.edu
Phone Number:    5550345678
Username:        sarahm
Password:        Sarah@Pass1
Role:            STUDENT
Department:      Engineering
```

**Login Options:**
- Email: `sarah.m@university.edu` + `Sarah@Pass1`
- Username: `sarahm` + `Sarah@Pass1`

---

## 🔍 Validation Tests

### Test 4: Duplicate Username
1. Try to register with username `alicej` (already taken)
2. **Expected:** Error message "User with username alicej already exists"

### Test 5: Duplicate Email
1. Try to register with email `alice.j@university.edu` (already taken)
2. **Expected:** Error message "User with email alice.j@university.edu already exists"

### Test 6: Invalid Username Format
Try registering with these usernames:
- `ab` (too short) - Expected: Error "Username must be between 3 and 50 characters"
- `user name` (space) - Expected: Error "Username can only contain letters, numbers, and underscores"
- `user@name` (special char) - Expected: Error "Username can only contain letters, numbers, and underscores"

### Test 7: Wrong Password
1. Try logging in with correct email/username but wrong password
2. **Expected:** Error "Invalid credentials"

### Test 8: Non-existent User
1. Try logging in with `nonexistent@email.com`
2. **Expected:** Error "Invalid credentials"

---

## 📊 What to Observe

### Login Page Changes:
- ✅ Label now says **"Email or Username"** instead of just "Email"
- ✅ You can type either email or username in that field

### Registration Page:
- ✅ Username field is collected and validated
- ✅ All previous fields still work (Full Name, Email, Phone, etc.)

### Backend Logs:
Watch the backend terminal for SQL queries:
```
Hibernate: select ... from users where email = ?
Hibernate: select ... from users where username = ?
```

This shows it's trying email first, then username!

---

## ✅ Success Criteria

After testing, you should be able to:
- [x] Register a new user with a username
- [x] Login with email address
- [x] Login with username
- [x] See error for duplicate username
- [x] See error for duplicate email
- [x] See error for invalid username format
- [x] Access appropriate dashboard based on role

---

## 🎉 YOU'RE ALL SET!

The application window is open and ready for testing!

**Start with Test 1** (Register) and work your way through the tests.

Let me know the results! 🚀
