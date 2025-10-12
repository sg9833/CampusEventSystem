# Sample Registration Data for Testing

## Test User 1 - Student Account

Use this data to test the registration flow:

### Registration Form Fields

| Field | Value |
|-------|-------|
| **Full Name** | `John Smith` |
| **Email** | `john.smith@university.edu` |
| **Phone Number** | `+1-555-0123` or `5550123456` |
| **Username** | `johnsmith` |
| **Password** | `Test@1234` |
| **Confirm Password** | `Test@1234` |
| **Role** | `STUDENT` |
| **Department/College Name** | `Computer Science` |
| **Terms & Conditions** | ✅ Check the box |

### Login Credentials (After Registration)
- **Email:** `john.smith@university.edu`
- **Password:** `Test@1234`

**⚠️ IMPORTANT:** Login with your **EMAIL**, not username!

---

## Test User 2 - Organizer Account

### Registration Form Fields

| Field | Value |
|-------|-------|
| **Full Name** | `Jane Doe` |
| **Email** | `jane.doe@university.edu` |
| **Phone Number** | `+1-555-0124` or `5550124567` |
| **Username** | `janedoe` |
| **Password** | `Secure@2024` |
| **Confirm Password** | `Secure@2024` |
| **Role** | `ORGANIZER` |
| **Department/College Name** | `Event Management` |
| **Terms & Conditions** | ✅ Check the box |

### Login Credentials (After Registration)
- **Email:** `jane.doe@university.edu`
- **Password:** `Secure@2024`

**⚠️ IMPORTANT:** Login with your **EMAIL**, not username!

---

## Test User 3 - Another Student

### Registration Form Fields

| Field | Value |
|-------|-------|
| **Full Name** | `Alice Johnson` |
| **Email** | `alice.j@university.edu` |
| **Phone Number** | `+1-555-0125` or `5550125678` |
| **Username** | `alicej` |
| **Password** | `Alice@Pass123` |
| **Confirm Password** | `Alice@Pass123` |
| **Role** | `STUDENT` |
| **Department/College Name** | `Business Administration` |
| **Terms & Conditions** | ✅ Check the box |

### Login Credentials (After Registration)
- **Email:** `alice.j@university.edu`
- **Password:** `Alice@Pass123`

**⚠️ IMPORTANT:** Login with your **EMAIL**, not username!

---

## Password Requirements

Make sure your password meets these criteria:
- ✅ At least 8 characters long
- ✅ Contains lowercase letters (a-z)
- ✅ Contains uppercase letters (A-Z)
- ✅ Contains numbers (0-9)
- ✅ Contains special characters (!@#$%^&*...)

**Password Strength Indicator:**
- 🔴 **Weak:** Less than 40 points
- 🟡 **Medium:** 40-69 points
- 🟢 **Strong:** 70-100 points

---

## Step-by-Step Testing Process

### Step 1: Start the Application
```bash
cd /Users/garinesaiajay/Desktop/CampusEventSystem
PYTHONPATH=$(pwd) /opt/homebrew/bin/python3.11 frontend_tkinter/main.py
```

### Step 2: Navigate to Registration
1. Wait for the login page to appear
2. Click the **"Register"** link at the bottom
3. The registration form should open

### Step 3: Fill in the Registration Form
Using Test User 1 (Student) data:
1. **Full Name:** Type `John Smith`
2. **Email:** Type `john.smith@university.edu`
3. **Phone Number:** Type `5550123456`
4. **Username:** Type `johnsmith`
5. **Password:** Type `Test@1234` (watch the strength meter turn green)
6. **Confirm Password:** Type `Test@1234` again
7. **Role:** Keep as `STUDENT` (or select from dropdown)
8. **Department/College Name:** Type `Computer Science`
9. **Terms & Conditions:** Click the checkbox ✅

### Step 4: Submit Registration
1. Click the **"REGISTER"** button
2. Wait for the loading spinner
3. You should see: "Welcome - Registration successful. You are now logged in."
4. The app should automatically navigate to the dashboard

### Step 5: Test Login (After Logout)
If you need to test login separately:
1. Logout from the dashboard (if logged in)
2. On the login page, enter:
   - **Email:** `john.smith@university.edu`
   - **Password:** `Test@1234`
3. Click **"LOGIN"**
4. You should be taken to the dashboard

**⚠️ NOTE:** The backend only supports login with EMAIL, not username. The "username" field collected during registration is currently not used by the backend.

---

## Expected Behavior

### ✅ Successful Registration
- Loading spinner appears
- Success message: "Registration successful. You are now logged in."
- Automatically logged in with JWT token
- Redirected to the appropriate dashboard (Student or Organizer)

### ✅ Successful Login
- Loading spinner appears
- JWT token stored in session
- Redirected to dashboard based on role

### ❌ Common Errors

**1. Role Validation Error** ✅ FIXED
- Error: "Role must be either 'student', 'organizer', or 'admin'"
- Solution: This has been fixed! The frontend now automatically converts role to lowercase before sending to backend

**2. Username Already Taken**
- Error: "Username already taken"
- Solution: Try a different username

**3. Email Already Registered**
- Error: "Email already exists"
- Solution: Use a different email address

**4. Password Mismatch**
- Error: "Passwords do not match"
- Solution: Make sure both password fields match exactly

**5. Weak Password**
- Error: Password validation message
- Solution: Include uppercase, lowercase, numbers, and special characters

**6. Missing Required Fields**
- Error: "Please correct the highlighted fields."
- Solution: Fill in all required fields

---

## Quick Copy-Paste Data

### Student Account (Registration)
```
Full Name: John Smith
Email: john.smith@university.edu
Phone: 5550123456
Username: johnsmith (currently not used by backend)
Password: Test@1234
Department: Computer Science
Role: STUDENT
```

### Student Account (Login)
```
Email: john.smith@university.edu
Password: Test@1234
```

### Organizer Account (Registration)
```
Full Name: Jane Doe
Email: jane.doe@university.edu
Phone: 5550124567
Username: janedoe (currently not used by backend)
Password: Secure@2024
Department: Event Management
Role: ORGANIZER
```

### Organizer Account (Login)
```
Email: jane.doe@university.edu
Password: Secure@2024
```

---

## Backend Requirements

Make sure the backend is running before testing:
```bash
# Check if backend is running
lsof -ti:8080 && echo "✅ Backend running" || echo "❌ Backend not running"

# If not running, start it:
cd backend_java/backend
./mvnw spring-boot:run
```

---

## Database Note

After successful registration, the user data will be stored in the database. You can verify by checking:
- Users table should have the new user entry
- User ID should be assigned
- Password should be hashed (not stored in plain text)
- JWT token should be generated and stored in session

---

## Testing Checklist

- [ ] Backend server is running on port 8080
- [ ] Frontend application launches successfully
- [ ] Registration form loads with all fields visible
- [ ] Password strength meter works correctly
- [ ] Form validation shows appropriate error messages
- [ ] Register button becomes disabled during submission
- [ ] Success message appears after registration
- [ ] User is automatically logged in after registration
- [ ] Dashboard loads correctly for the user role
- [ ] User can logout and login again with same credentials
- [ ] JWT token is properly stored and used for API calls

---

**Ready to test? Let's go step-by-step!** 🚀
