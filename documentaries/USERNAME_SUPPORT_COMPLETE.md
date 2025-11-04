# Username Support Implementation - Complete Guide

## ✅ Changes Made

### Backend Changes:
1. **User Model** - Added `username` field
2. **RegisterRequest** - Added `username` with validation
3. **LoginRequest** - Modified to accept email OR username
4. **AuthController** - Updated login to check both email and username
5. **UserDao** - Added `findByUsername` method and updated all methods
6. **Database Schema** - Added username column

### Frontend Changes:
1. **Login Page** - Changed label from "Email" to "Email or Username"

---

## 🗄️ IMPORTANT: Database Migration Required!

Before starting the backend, you MUST update your database schema.

### Option 1: Fresh Database (Recommended for Development)
If you can drop and recreate the database:

```bash
# Connect to MySQL
mysql -u root -p

# Drop and recreate database
DROP DATABASE IF EXISTS campus_events;
CREATE DATABASE campus_events;
USE campus_events;

# Run the updated schema
SOURCE /Users/garinesaiajay/Desktop/CampusEventSystem/database_sql/schema.sql;

# Optional: Add sample data
SOURCE /Users/garinesaiajay/Desktop/CampusEventSystem/database_sql/sample_data.sql;
```

### Option 2: Migration Script (If you have existing data)
If you have existing users and want to keep them:

```bash
# Connect to MySQL
mysql -u root -p campus_events

# Run the migration script
SOURCE /Users/garinesaiajay/Desktop/CampusEventSystem/database_sql/add_username_migration.sql;
```

This script will:
- Add `username` column
- Add `created_at` column
- Set temporary usernames for existing users (based on email)
- Make username UNIQUE and NOT NULL

**⚠️ Important:** After running the migration, you'll need to update usernames for existing users manually or they'll have auto-generated usernames.

---

## 🚀 Starting the Application

### Step 1: Start Backend
```bash
cd /Users/garinesaiajay/Desktop/CampusEventSystem/backend_java/backend
./mvnw spring-boot:run
```

Wait for backend to start (look for "Started CampusEventSystemApplication")

### Step 2: Start Frontend
```bash
cd /Users/garinesaiajay/Desktop/CampusEventSystem
PYTHONPATH=$(pwd) /opt/homebrew/bin/python3.11 frontend_tkinter/main.py
```

---

## 🧪 Testing the Implementation

### Test 1: Registration with Username
1. Click "Register" on login page
2. Fill in the form:
   ```
   Full Name: Test User
   Email: test.user@university.edu
   Phone: 5550001234
   Username: testuser
   Password: Test@1234
   Confirm Password: Test@1234
   Role: STUDENT
   Department: Computer Science
   ✅ Terms & Conditions
   ```
3. Click "REGISTER"
4. **Expected:** Success! Auto-login and redirect to dashboard

### Test 2: Login with Email
1. Logout from dashboard
2. On login page, enter:
   ```
   Email or Username: test.user@university.edu
   Password: Test@1234
   ```
3. Click "LOGIN"
4. **Expected:** Success! Login and redirect to dashboard

### Test 3: Login with Username
1. Logout from dashboard
2. On login page, enter:
   ```
   Email or Username: testuser
   Password: Test@1234
   ```
3. Click "LOGIN"
4. **Expected:** Success! Login and redirect to dashboard

### Test 4: Duplicate Username Prevention
1. Try to register another user with username `testuser`
2. **Expected:** Error "User with username testuser already exists"

### Test 5: Duplicate Email Prevention
1. Try to register another user with email `test.user@university.edu`
2. **Expected:** Error "User with email test.user@university.edu already exists"

---

## 📝 Sample Test Data

### User 1 (Student)
**Registration:**
```
Full Name: Alice Johnson
Email: alice.j@university.edu
Phone: 5550123456
Username: alicej
Password: Alice@123
Role: STUDENT
Department: Computer Science
```

**Login Options:**
- Email: `alice.j@university.edu` + Password: `Alice@123`
- Username: `alicej` + Password: `Alice@123`

### User 2 (Organizer)
**Registration:**
```
Full Name: Bob Wilson
Email: bob.w@university.edu
Phone: 5550234567
Username: bobw
Password: Bob@2024
Role: ORGANIZER
Department: Event Management
```

**Login Options:**
- Email: `bob.w@university.edu` + Password: `Bob@2024`
- Username: `bobw` + Password: `Bob@2024`

---

## 🔍 Validation Rules

### Username Validation:
- ✅ Required field
- ✅ 3-50 characters
- ✅ Only letters, numbers, and underscores
- ✅ Must be unique
- ❌ No spaces allowed
- ❌ No special characters except underscore

Examples:
- ✅ `johnsmith`, `john_smith`, `john123`
- ❌ `jo` (too short), `john smith` (space), `john@smith` (special char)

---

## 🎯 How It Works

### Registration Flow:
1. User enters email AND username
2. Backend validates both are unique
3. Backend stores both in database
4. JWT token generated with email as identifier
5. Auto-login after registration

### Login Flow:
1. User enters email OR username
2. Backend first tries to find by email
3. If not found, tries to find by username
4. Password verified
5. JWT token generated
6. Login successful

---

## 📊 Database Schema

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ⚠️ Troubleshooting

### Backend won't start - SQL Error about username column
**Problem:** Database doesn't have username column
**Solution:** Run the migration script or recreate the database with updated schema

### Registration fails - "column 'username' not found"
**Problem:** Database migration not applied
**Solution:** Run database migration (see above)

### Login fails with username
**Problem:** Backend not restarted after code changes
**Solution:** Restart backend server

### Existing users can't login
**Problem:** Old user records don't have username
**Solution:** Run migration script to add temporary usernames

---

## ✅ Verification Checklist

- [ ] Database migration applied successfully
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can register with username
- [ ] Can login with email
- [ ] Can login with username
- [ ] Duplicate username is rejected
- [ ] Duplicate email is rejected
- [ ] Password validation works
- [ ] JWT token is generated correctly
- [ ] Dashboard loads after login

---

## 🎉 Summary

**You can now:**
- ✅ Register with both email AND username
- ✅ Login with EITHER email OR username
- ✅ All usernames are unique
- ✅ All emails are unique
- ✅ Better user experience!

**Files Changed:**
- 7 Backend Java files
- 2 Frontend Python files
- 2 Database SQL files

**Status:** Implementation Complete! Ready to test! 🚀
