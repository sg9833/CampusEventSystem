# ⚡ QUICK START - Username Support

## ✅ What Was Fixed

Both **email** AND **username** are now fully supported for login!

---

## 🚨 BEFORE YOU START - Database Migration Required!

### Quick Migration (Choose One):

#### Option A: Fresh Start (Easiest)
```bash
mysql -u root -p

DROP DATABASE IF EXISTS campus_events;
CREATE DATABASE campus_events;
USE campus_events;
SOURCE /Users/garinesaiajay/Desktop/CampusEventSystem/database_sql/schema.sql;
exit;
```

#### Option B: Keep Existing Data
```bash
mysql -u root -p campus_events
SOURCE /Users/garinesaiajay/Desktop/CampusEventSystem/database_sql/add_username_migration.sql;
exit;
```

---

## 🚀 Start the Application

### 1. Start Backend
```bash
cd /Users/garinesaiajay/Desktop/CampusEventSystem/backend_java/backend
./mvnw spring-boot:run
```

### 2. Start Frontend (in new terminal)
```bash
cd /Users/garinesaiajay/Desktop/CampusEventSystem
PYTHONPATH=$(pwd) /opt/homebrew/bin/python3.11 frontend_tkinter/main.py
```

---

## 🧪 Test It!

### Register:
```
Full Name: Alice Johnson
Email: alice.j@university.edu
Phone: 5550123456
Username: alicej            ← NEW! This is now saved
Password: Alice@123
```

### Login (Both work!):
✅ **With Email:** `alice.j@university.edu` + `Alice@123`
✅ **With Username:** `alicej` + `Alice@123`

---

## 📝 What Changed

### Backend:
- ✅ User model now has `username` field
- ✅ Registration saves username
- ✅ Login accepts email OR username
- ✅ Both email and username must be unique

### Frontend:
- ✅ Login field now says "Email or Username"
- ✅ Registration form collects username (now actually used!)

### Database:
- ✅ New `username` column (VARCHAR(50), UNIQUE, NOT NULL)
- ✅ New `created_at` timestamp column

---

## ⚠️ Important Notes

1. **Database migration is REQUIRED** - Backend won't start without it
2. **Username rules:**
   - 3-50 characters
   - Only letters, numbers, and underscores
   - Must be unique
3. **Both email and username can be used for login**

---

## 🎯 Quick Test Steps

1. Run database migration (above)
2. Start backend
3. Start frontend
4. Register a new user with username
5. Logout
6. Login with email → Works! ✅
7. Logout
8. Login with username → Works! ✅

---

**Ready? Run the database migration first, then start the servers!** 🚀
