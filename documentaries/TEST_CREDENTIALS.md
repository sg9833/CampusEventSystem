# Test Account Credentials - Campus Event System

**Date:** October 11, 2025  
**Purpose:** Test accounts for development and testing

## 🔐 Test Accounts

### 1. Organizer Account (NEW - For Resource Booking)
**Username:** `organizer1@campus.com`  
**Password:** `test123`  
**Role:** Organizer  
**Name:** Organizer One

**What you can access:**
- ✅ Create events
- ✅ View my events
- ✅ View event registrations
- ✅ **Book Resources** (NEW)
- ✅ **My Bookings** (NEW)
- ✅ View resource requests
- ✅ View analytics
- ✅ Profile settings

---

### 2. Student Account
**Username:** `student1@campus.com`  
**Password:** `test123`  
**Role:** Student  
**Name:** Student One

**What you can access:**
- ✅ Browse events
- ✅ Register for events
- ✅ View my registrations
- ❌ Book resources (removed - organizers only)
- ❌ My bookings (removed - organizers only)
- ✅ Profile settings

---

### 3. Admin Account
**Username:** `admin@campus.com`  
**Password:** `test123`  
**Role:** Admin  
**Name:** Admin User

**What you can access:**
- ✅ All event management features
- ✅ User management
- ✅ Event approvals
- ✅ Booking approvals
- ✅ Manage resources
- ✅ System analytics
- ✅ Full system access

---

## 🧪 How to Test Resource Booking Changes

### Test as Organizer (Recommended):
1. **Login:**
   ```
   Email: organizer1@campus.com
   Password: test123
   ```

2. **Verify Sidebar:**
   - Look for "Book Resources" button (📚)
   - Look for "My Bookings" button (📅)

3. **Test Book Resources:**
   - Click "Book Resources"
   - Browse available resources
   - Click "Book Now" on any resource
   - Complete the booking form
   - Submit booking

4. **Test My Bookings:**
   - Click "My Bookings"
   - View list of your resource bookings
   - Check booking status and details

### Test as Student:
1. **Login:**
   ```
   Email: student1@campus.com
   Password: test123
   ```

2. **Verify Sidebar:**
   - Confirm "Book Resources" is NOT visible
   - Confirm "My Bookings" is NOT visible

3. **Try to Access Browse Resources:**
   - If you can access it (via other means)
   - Verify "Book Now" buttons show info messages instead
   - See: "Booking available for organizers"

---

## 🔑 Password Hash Information

All test accounts use the same password hash:
```
$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG
```

This corresponds to the plain text password: `test123`

**Password Requirements:**
- Minimum 6 characters (for test accounts)
- Production should use stronger passwords

---

## 📊 Database Location

Test data is defined in:
```
database_sql/sample_data.sql
```

To reset test data:
1. Stop the backend
2. Run the SQL script to reload sample data
3. Restart the backend

---

## 🚀 Quick Login Commands (for testing)

### Via Frontend GUI:
- Open the Tkinter app
- Enter email and password
- Click LOGIN

### Via API (curl):
```bash
# Login as Organizer
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"organizer1@campus.com","password":"test123"}'

# Login as Student
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student1@campus.com","password":"test123"}'

# Login as Admin
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@campus.com","password":"test123"}'
```

---

## 📝 Notes

1. **All accounts share the same password** (`test123`) for easy testing
2. **User IDs in database:**
   - Admin: ID 1
   - Organizer One: ID 2
   - Student One: ID 3

3. **Sample events** are created by Organizer One (ID 2):
   - "Tech Talk" - October 15, 2025
   - "Workshop on AI" - October 20, 2025

4. **Sample resources:**
   - Projector (ID 1)
   - Laptops (ID 2)

5. **Sample bookings** exist for Student One to test booking views

---

## 🔒 Security Note

⚠️ **These are TEST credentials only!**  
- Never use `test123` in production
- Change all default passwords before deploying
- Use strong, unique passwords for production accounts
- Enable proper password policies (minimum length, complexity, etc.)

---

## 🎯 Testing Checklist

### Organizer Account Testing:
- [ ] Login successfully
- [ ] See "Book Resources" in sidebar
- [ ] See "My Bookings" in sidebar
- [ ] Can access book resources page
- [ ] Can see "Book Now" buttons on resources
- [ ] Can complete a resource booking
- [ ] Can view bookings in "My Bookings" page

### Student Account Testing:
- [ ] Login successfully
- [ ] Do NOT see "Book Resources" in sidebar
- [ ] Do NOT see "My Bookings" in sidebar
- [ ] If accessing browse resources, see info messages instead of booking buttons
- [ ] Can browse and view event registrations normally

---

For more details, see:
- `RESOURCE_BOOKING_ORGANIZERS_ONLY.md` - Documentation of booking restrictions
- `database_sql/sample_data.sql` - Sample data SQL script
- `COMPLETE_TESTING_GUIDE.md` - Full testing guide
