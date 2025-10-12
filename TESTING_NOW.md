# 🧪 TESTING USERNAME & EMAIL LOGIN - READY!

## ✅ System Status

- **Backend:** ✅ Running on port 8080 (PID 50206)
- **Frontend:** ✅ Running (Tkinter GUI open)
- **Database:** ✅ `campusdb.users` table has `username` column (VARCHAR 50 NOT NULL UNIQUE)

---

## 🎯 TEST SCENARIO 1: Register New User

### Steps:
1. **Click "Register"** link on the login page
2. Fill in the registration form:
   ```
   Full Name:       Alice Johnson
   Email:           alice.j@university.edu
   Phone Number:    5550123456
   Username:        alicej          ← NEW FIELD!
   Password:        Alice@123
   Confirm Password: Alice@123
   Role:            STUDENT (default)
   Department:      Computer Science
   ✅ Accept Terms & Conditions
   ```
3. **Click REGISTER** button

### ✅ Expected Result:
- Registration succeeds
- You're automatically logged in with JWT token
- Redirected to Student Dashboard
- New user is in database with username `alicej`

---

## 🎯 TEST SCENARIO 2: Login with EMAIL

### Steps:
1. **Logout** from dashboard (if you were auto-logged in)
2. On login page (notice it says **"Email or Username"** now!)
3. Enter:
   ```
   Email or Username: alice.j@university.edu
   Password:          Alice@123
   ```
4. **Click LOGIN**

### ✅ Expected Result:
- Login succeeds using EMAIL
- JWT token generated
- Redirected to Student Dashboard

---

## 🎯 TEST SCENARIO 3: Login with USERNAME

### Steps:
1. **Logout** from dashboard
2. On login page, enter:
   ```
   Email or Username: alicej          ← Using username!
   Password:          Alice@123
   ```
3. **Click LOGIN**

### ✅ Expected Result:
- Login succeeds using USERNAME
- JWT token generated
- Redirected to Student Dashboard

---

## 📊 Backend Logic Flow

When you login, the backend:

1. **First tries EMAIL:**
   ```java
   Optional<User> userOpt = userDao.findByEmail(identifier);
   ```

2. **If email not found, tries USERNAME:**
   ```java
   if (userOpt.isEmpty()) {
       userOpt = userDao.findByUsername(identifier);
   }
   ```

3. **Validates password and returns JWT token**

---

## 🔍 How to Verify in Database

After registration, run this to see your new user:

```bash
mysql -u root -p'SAIAJAY@2005' campusdb -e "SELECT id, name, email, username, role FROM users WHERE username='alicej';"
```

You should see:
```
+----+---------------+---------------------------+----------+---------+
| id | name          | email                     | username | role    |
+----+---------------+---------------------------+----------+---------+
| 11 | Alice Johnson | alice.j@university.edu    | alicej   | student |
+----+---------------+---------------------------+----------+---------+
```

---

## 🎉 START TESTING NOW!

**The frontend window is open and ready!**

### Test Order:
1. ✅ Register with username (Alice Johnson / alicej)
2. ✅ Login with email (alice.j@university.edu)
3. ✅ Login with username (alicej)

**Let me know the results!** 🚀
