# 🧪 Comprehensive Test Cases
# Campus Event & Resource Coordination System v2.0.0
# Date: October 9, 2025

**Test Status:** ⏳ In Progress  
**Last Updated:** October 9, 2025  
**Tester:** QA Team

---

## 📋 Test Overview

| Category | Test Cases | Status |
|----------|------------|--------|
| **Authentication Flow** | 5 tests | ⏳ Pending |
| **Student Workflows** | 5 tests | ⏳ Pending |
| **Organizer Workflows** | 4 tests | ⏳ Pending |
| **Admin Workflows** | 5 tests | ⏳ Pending |
| **Edge Cases** | 5 tests | ⏳ Pending |
| **Total** | **24 tests** | **0/24 Passed** |

---

## 1️⃣ Authentication Flow Tests

### Test 1.1: Login with Valid Credentials ✅

**Test ID:** AUTH-001  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Application is running
- Backend API is accessible
- User account exists in database

**Test Data:**
```json
{
  "email": "student@example.com",
  "password": "Student123!"
}
```

**Test Steps:**
1. Launch the application
2. Navigate to Login page (should be default page)
3. Enter valid email address in Email field
4. Enter correct password in Password field
5. Click "Login" button

**Expected Results:**
- ✅ Login button becomes disabled during authentication
- ✅ Loading indicator appears
- ✅ No error message displayed
- ✅ User is redirected to appropriate dashboard (Student Dashboard)
- ✅ Welcome message shows user's name
- ✅ Navigation bar displays user info
- ✅ Logout button is visible
- ✅ Session is created and stored

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 1.2: Login with Invalid Credentials ✅

**Test ID:** AUTH-002  
**Priority:** High  
**Type:** Negative

**Test Data:**
```json
{
  "email": "invalid@example.com",
  "password": "WrongPassword123"
}
```

**Test Steps:**
1. Launch the application
2. Navigate to Login page
3. Enter non-existent email
4. Enter incorrect password
5. Click "Login" button

**Expected Results:**
- ✅ Error message displayed: "Invalid email or password"
- ✅ Error appears in red/danger color
- ✅ Email and password fields remain filled
- ✅ User stays on login page
- ✅ No session is created
- ✅ No navigation occurs
- ✅ Login button returns to enabled state

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 1.3: Registration with All Validations ✅

**Test ID:** AUTH-003  
**Priority:** High  
**Type:** Functional

**Test Data:**
```json
{
  "fullName": "John Doe",
  "email": "john.doe@example.com",
  "password": "SecurePass123!",
  "confirmPassword": "SecurePass123!",
  "role": "STUDENT"
}
```

**Test Steps:**
1. Launch the application
2. Navigate to Login page
3. Click "Register" link/button
4. Enter valid full name (alphabets and spaces only)
5. Enter valid email format
6. Enter password meeting requirements:
   - Minimum 8 characters
   - Contains uppercase letter
   - Contains lowercase letter
   - Contains number
   - Contains special character
7. Enter matching confirm password
8. Select role (Student/Organizer)
9. Click "Register" button

**Expected Results:**
- ✅ All validation messages clear as valid input is entered
- ✅ Password strength indicator shows (weak/medium/strong)
- ✅ Confirm password validation checks match
- ✅ Registration succeeds
- ✅ Success message displayed: "Registration successful!"
- ✅ User is redirected to login page OR auto-logged in
- ✅ New account is created in database

**Validation Test Cases:**
| Field | Invalid Input | Expected Error |
|-------|---------------|----------------|
| Full Name | "John123" | "Name should contain only letters and spaces" |
| Full Name | "" | "Full name is required" |
| Email | "notanemail" | "Invalid email format" |
| Email | "" | "Email is required" |
| Password | "short" | "Password must be at least 8 characters" |
| Password | "nouppercaseornumber" | "Password must contain uppercase, lowercase, number" |
| Confirm Password | "Mismatch123!" | "Passwords do not match" |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 1.4: Logout Functionality ✅

**Test ID:** AUTH-004  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- User is logged in

**Test Steps:**
1. User is logged into the application
2. Click on "Logout" button (in menu or navigation bar)
3. Confirm logout if prompted

**Expected Results:**
- ✅ Confirmation dialog appears: "Are you sure you want to logout?"
- ✅ User session is cleared
- ✅ User is redirected to login page
- ✅ Cannot access authenticated pages without re-login
- ✅ Session token is invalidated on backend
- ✅ "Remember me" preference is respected (or cleared)
- ✅ Cache is cleared appropriately

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 1.5: Session Persistence ✅

**Test ID:** AUTH-005  
**Priority:** Medium  
**Type:** Functional

**Prerequisites:**
- User has logged in previously

**Test Steps:**
1. Login to the application with "Remember Me" checked
2. Close the application completely
3. Reopen the application after 5 minutes
4. Check if session is maintained

**Expected Results:**
- ✅ User remains logged in
- ✅ User is taken to last visited page or dashboard
- ✅ Session data persists (user info, token)
- ✅ No re-authentication required
- ✅ Session expires after configured timeout (30 minutes default)

**Negative Test:**
1. Login without "Remember Me"
2. Close application
3. Reopen

**Expected:** User is taken to login page

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

## 2️⃣ Student Workflow Tests

### Test 2.1: Browse and Filter Events ✅

**Test ID:** STU-001  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Student
- Multiple events exist in database with different categories, dates, and statuses

**Test Steps:**
1. Navigate to "Browse Events" page
2. Observe initial event list (should show approved events)
3. **Test Search:**
   - Enter keyword in search box (e.g., "Workshop")
   - Observe filtered results
4. **Test Date Filter:**
   - Click on date range filter
   - Select start date and end date
   - Apply filter
5. **Test Category Filter:**
   - Select category checkboxes (Academic, Sports, Cultural, etc.)
   - Apply filter
6. **Test Status Filter:**
   - Select status (Upcoming, Ongoing, Completed)
   - Apply filter
7. **Test Sort:**
   - Sort by Date (ascending/descending)
   - Sort by Name
   - Sort by Popularity
8. **Test Combined Filters:**
   - Apply multiple filters together
   - Search + Category + Date range
9. **Test Clear Filters:**
   - Click "Clear Filters" or remove filter tags

**Expected Results:**
- ✅ Events load in grid layout (3 columns)
- ✅ Search results update with debounce (500ms delay)
- ✅ Date filter correctly filters events within range
- ✅ Category filter shows only selected categories
- ✅ Status filter shows correct event statuses
- ✅ Sort changes order correctly
- ✅ Combined filters work together (AND logic)
- ✅ Clear filters resets to all events
- ✅ Filter tags display active filters
- ✅ Pagination works if many results
- ✅ "No events found" message for empty results

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 2.2: Register for Event ✅

**Test ID:** STU-002  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Student
- Event exists with available capacity
- Student is not already registered

**Test Steps:**
1. Navigate to "Browse Events"
2. Find an event with available capacity
3. Click on event card to view details
4. Review event details (date, venue, description, capacity)
5. Click "Register" button
6. Confirm registration if prompted

**Expected Results:**
- ✅ Event details modal opens
- ✅ Current registration count and capacity shown
- ✅ "Register" button is enabled (not full)
- ✅ Registration confirmation dialog appears
- ✅ Success message: "Successfully registered for [Event Name]"
- ✅ Event card updates to show "Registered" status
- ✅ Register button changes to "Cancel Registration"
- ✅ Registration count increases by 1
- ✅ Event appears in "My Events" page

**Edge Cases to Test:**
| Scenario | Expected Behavior |
|----------|-------------------|
| Event at full capacity | "Register" button disabled, shows "Event Full" |
| Already registered | Shows "Registered" badge, button says "Cancel Registration" |
| Event in the past | Cannot register, shows "Event Ended" |
| Registration deadline passed | Cannot register, shows "Registration Closed" |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 2.3: Cancel Registration ✅

**Test ID:** STU-003  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Student
- Student is registered for an event
- Event has not started yet

**Test Steps:**
1. Navigate to "My Events" or "Browse Events"
2. Find event you are registered for
3. Click "Cancel Registration" button
4. Confirm cancellation in dialog

**Expected Results:**
- ✅ Cancellation confirmation dialog appears
- ✅ Dialog shows event details
- ✅ Success message: "Registration cancelled successfully"
- ✅ Event card updates to show "Register" button again
- ✅ Registration count decreases by 1
- ✅ Event removed from "My Events" list
- ✅ Can re-register for the event

**Edge Cases:**
| Scenario | Expected Behavior |
|----------|-------------------|
| Cancel after event started | Cannot cancel, shows "Event already started" |
| Cancel 24h before event | Warning: "Cancellation within 24 hours" |
| Cancel multiple times quickly | Only one cancellation processed |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 2.4: Book Resource ✅

**Test ID:** STU-004  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Student
- Resources exist in system
- Resource has available time slots

**Test Data:**
```json
{
  "resource": "Conference Room A",
  "date": "2025-10-15",
  "startTime": "10:00",
  "endTime": "12:00",
  "purpose": "Study group meeting"
}
```

**Test Steps:**
1. Navigate to "Browse Resources"
2. Filter resources by type (Room, Equipment, Lab, etc.)
3. Select a resource
4. Click "Book" button
5. Fill booking form:
   - Select date (future date)
   - Select start time
   - Select end time (must be after start time)
   - Enter purpose/description
6. Submit booking

**Expected Results:**
- ✅ Booking form opens in modal
- ✅ Date picker shows only future dates
- ✅ Time slots show availability (green = available, red = booked)
- ✅ End time must be after start time (validation)
- ✅ Purpose field is required (min 10 characters)
- ✅ Success message: "Booking request submitted"
- ✅ Booking appears in "My Bookings" with "Pending" status
- ✅ Cannot book same resource for overlapping time

**Validation Tests:**
| Field | Invalid Input | Expected Error |
|-------|---------------|----------------|
| Date | Past date | "Cannot book for past dates" |
| Start Time | After end time | "End time must be after start time" |
| Duration | > 4 hours | "Maximum booking duration is 4 hours" |
| Purpose | Less than 10 chars | "Purpose must be at least 10 characters" |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 2.5: View Bookings ✅

**Test ID:** STU-005  
**Priority:** Medium  
**Type:** Functional

**Prerequisites:**
- Logged in as Student
- Student has at least one booking

**Test Steps:**
1. Navigate to "My Bookings" page
2. Observe list of bookings
3. Check booking details
4. Filter by status (Pending/Approved/Rejected)
5. Search by resource name or date
6. Click on booking to view full details

**Expected Results:**
- ✅ All user's bookings displayed in list/grid
- ✅ Each booking shows:
  - Resource name
  - Date and time
  - Status (Pending/Approved/Rejected)
  - Purpose
- ✅ Color-coded status badges:
  - Orange for Pending
  - Green for Approved
  - Red for Rejected
- ✅ Filter by status works
- ✅ Search filters bookings
- ✅ Click opens detail modal with full information
- ✅ Approved bookings show calendar integration option
- ✅ Can cancel pending bookings

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

## 3️⃣ Organizer Workflow Tests

### Test 3.1: Create Event ✅

**Test ID:** ORG-001  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Organizer

**Test Data:**
```json
{
  "title": "Python Programming Workshop",
  "category": "Workshop",
  "description": "Learn Python basics with hands-on exercises",
  "venue": "Computer Lab 101",
  "date": "2025-10-20",
  "startTime": "14:00",
  "endTime": "17:00",
  "capacity": 50,
  "registrationDeadline": "2025-10-18",
  "tags": ["programming", "python", "beginners"]
}
```

**Test Steps:**
1. Navigate to "Create Event" page
2. Fill all required fields:
   - Event title
   - Category (dropdown)
   - Description (min 50 characters)
   - Venue
   - Date (future date)
   - Start time
   - End time (after start time)
   - Capacity (positive number)
   - Registration deadline (before event date)
   - Optional: Upload event image
   - Optional: Add tags
3. Click "Create Event" button

**Expected Results:**
- ✅ All fields have proper validation
- ✅ Image upload preview shows selected image
- ✅ Tag input allows adding multiple tags
- ✅ Success message: "Event created successfully!"
- ✅ Event status is "Pending" (awaiting admin approval)
- ✅ Event appears in "My Events" with "Pending" badge
- ✅ Form clears after successful submission
- ✅ Can upload event banner image

**Field Validations:**
| Field | Validation | Error Message |
|-------|------------|---------------|
| Title | Required, 5-100 chars | "Title must be between 5-100 characters" |
| Category | Required | "Please select a category" |
| Description | Required, min 50 chars | "Description must be at least 50 characters" |
| Venue | Required | "Venue is required" |
| Date | Future date only | "Event date must be in the future" |
| End Time | After start time | "End time must be after start time" |
| Capacity | Number, min 10, max 1000 | "Capacity must be between 10-1000" |
| Registration Deadline | Before event date | "Deadline must be before event date" |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 3.2: Edit Pending Event ✅

**Test ID:** ORG-002  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Organizer
- Organizer has created an event with "Pending" status

**Test Steps:**
1. Navigate to "My Events"
2. Find event with "Pending" status
3. Click "Edit" button
4. Modify event details:
   - Change title
   - Update description
   - Change venue
   - Adjust time
5. Click "Save Changes"

**Expected Results:**
- ✅ Edit form opens pre-filled with current data
- ✅ All fields are editable
- ✅ Same validations apply as create
- ✅ Success message: "Event updated successfully"
- ✅ Changes are reflected in event details
- ✅ Event remains in "Pending" status
- ✅ Timestamp shows "Last edited: [date/time]"

**Restrictions to Test:**
| Event Status | Can Edit? | Expected Behavior |
|--------------|-----------|-------------------|
| Pending | ✅ Yes | Full editing allowed |
| Approved | ❌ No | Cannot edit, shows "Contact admin to modify" |
| Rejected | ✅ Yes | Can edit and resubmit |
| Completed | ❌ No | Cannot edit past events |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 3.3: View Event Registrations ✅

**Test ID:** ORG-003  
**Priority:** Medium  
**Type:** Functional

**Prerequisites:**
- Logged in as Organizer
- Event exists with registrations

**Test Steps:**
1. Navigate to "My Events"
2. Select an event
3. Click "View Registrations" or "Attendees" button
4. Observe list of registered users

**Expected Results:**
- ✅ Modal/page shows list of registered users
- ✅ Each registration shows:
  - User name
  - User email
  - Registration date
  - Status (if applicable)
- ✅ Shows total count: "X/Y registrations"
- ✅ Progress bar shows capacity utilization
- ✅ Can export list to CSV
- ✅ Can search/filter registrations
- ✅ Shows user profile on click
- ✅ Real-time updates when new registrations arrive

**Additional Features:**
- ✅ Send notification to all attendees
- ✅ Check-in functionality (mark attendance)
- ✅ Registration statistics (graph/chart)

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 3.4: Cancel Event ✅

**Test ID:** ORG-004  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Organizer
- Event exists (approved or pending)
- Event has not started yet

**Test Steps:**
1. Navigate to "My Events"
2. Select an event
3. Click "Cancel Event" button
4. Enter cancellation reason in dialog
5. Confirm cancellation

**Expected Results:**
- ✅ Cancellation confirmation dialog appears
- ✅ Reason field is required (min 20 characters)
- ✅ Warning shows number of registered attendees
- ✅ Success message: "Event cancelled successfully"
- ✅ Event status changes to "Cancelled"
- ✅ All registered users receive notification
- ✅ Event still visible in "My Events" but marked as cancelled
- ✅ Users can no longer register
- ✅ Existing registrations are automatically cancelled

**Edge Cases:**
| Scenario | Expected Behavior |
|----------|-------------------|
| Cancel with 0 registrations | Cancels immediately |
| Cancel with registrations | Warning: "X users will be notified" |
| Cancel event within 24h of start | Extra confirmation required |
| Cancel ongoing event | Cannot cancel, shows "Event already started" |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

## 4️⃣ Admin Workflow Tests

### Test 4.1: Approve/Reject Events ✅

**Test ID:** ADM-001  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Admin
- Pending events exist in system

**Test Steps:**

**Approval Flow:**
1. Navigate to "Event Approvals" page
2. View list of pending events
3. Click on event to view details
4. Review event information
5. Click "Approve" button
6. Add approval notes (optional)
7. Confirm approval

**Rejection Flow:**
1. Navigate to "Event Approvals" page
2. Select a pending event
3. Click "Reject" button
4. Enter rejection reason (required)
5. Confirm rejection

**Expected Results:**

**Approval:**
- ✅ Event status changes to "Approved"
- ✅ Event becomes visible to all students
- ✅ Organizer receives notification
- ✅ Event moves to approved events list
- ✅ Approval timestamp recorded
- ✅ Admin name recorded as approver

**Rejection:**
- ✅ Rejection reason dialog appears
- ✅ Reason field is required (min 10 characters)
- ✅ Event status changes to "Rejected"
- ✅ Organizer receives notification with reason
- ✅ Event not visible to students
- ✅ Organizer can view reason and resubmit after editing

**Additional Features:**
- ✅ Bulk approve multiple events
- ✅ Filter by category, date, organizer
- ✅ Sort by submission date
- ✅ Flag problematic events for review
- ✅ View organizer's event history

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 4.2: Approve/Reject Bookings ✅

**Test ID:** ADM-002  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Admin
- Pending booking requests exist

**Test Steps:**

**Approval Flow:**
1. Navigate to "Booking Approvals" page
2. View pending bookings with conflict detection
3. Select a booking
4. Review booking details:
   - Resource
   - User
   - Date and time
   - Purpose
   - Any conflicts (red highlight)
5. Click "Approve" button
6. Confirm approval

**Rejection Flow:**
1. Select a pending booking
2. Click "Reject" button
3. Enter rejection reason
4. Optionally suggest alternative time slots
5. Confirm rejection

**Expected Results:**

**Approval:**
- ✅ Booking status changes to "Approved"
- ✅ User receives confirmation notification
- ✅ Time slot is blocked in calendar
- ✅ Resource availability updated
- ✅ Approval recorded with admin details

**Rejection:**
- ✅ Rejection dialog shows reason field
- ✅ Can suggest alternative time slots
- ✅ User receives notification with reason
- ✅ Time slot remains available
- ✅ User can resubmit with different time

**Conflict Detection:**
- ✅ Conflicting bookings highlighted in red
- ✅ Warning shows: "Overlaps with [X] other bookings"
- ✅ Can view conflicting bookings
- ✅ Suggest alternative times automatically
- ✅ Calendar view shows all bookings

**Additional Features:**
- ✅ Bulk approve non-conflicting bookings
- ✅ Filter by resource type, user, date
- ✅ Sort by priority (first-come-first-served)
- ✅ View user's booking history
- ✅ Override conflicts if necessary

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 4.3: Manage Resources ✅

**Test ID:** ADM-003  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Admin

**Test Data:**
```json
{
  "name": "Conference Room B",
  "type": "Room",
  "capacity": 30,
  "location": "Building A, Floor 2",
  "amenities": ["Projector", "Whiteboard", "WiFi"],
  "availability": "Monday-Friday, 8 AM - 8 PM",
  "description": "Modern conference room with AV equipment"
}
```

**Test Steps:**

**Add Resource:**
1. Navigate to "Manage Resources" page
2. Click "Add Resource" button
3. Fill resource form with all details
4. Upload resource image (optional)
5. Add amenities as tags
6. Set availability schedule
7. Click "Save"

**Edit Resource:**
1. Find existing resource
2. Click "Edit" button
3. Modify details
4. Save changes

**Delete Resource:**
1. Select a resource
2. Click "Delete" button
3. Confirm deletion
4. Check if resource has active bookings (warning)

**Expected Results:**

**Add:**
- ✅ Form has all required fields
- ✅ Amenities can be added as tags
- ✅ Image upload with preview
- ✅ Availability calendar selector
- ✅ Success message: "Resource added successfully"
- ✅ Resource appears in browse resources

**Edit:**
- ✅ Form pre-filled with current data
- ✅ All fields editable
- ✅ Changes reflect immediately
- ✅ Existing bookings remain valid

**Delete:**
- ✅ Confirmation dialog appears
- ✅ Warning if active bookings exist
- ✅ Cannot delete if future approved bookings
- ✅ Can mark as "Inactive" instead
- ✅ Success message after deletion

**Validation:**
| Field | Validation | Error Message |
|-------|------------|---------------|
| Name | Required, unique | "Resource name already exists" |
| Type | Required | "Please select resource type" |
| Capacity | Positive number | "Capacity must be greater than 0" |
| Location | Required | "Location is required" |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 4.4: Manage Users ✅

**Test ID:** ADM-004  
**Priority:** High  
**Type:** Functional

**Prerequisites:**
- Logged in as Admin
- Multiple users exist in system

**Test Steps:**

**View Users:**
1. Navigate to "Manage Users" page
2. View user table with all users
3. Search for specific user
4. Filter by role
5. Sort by registration date, name, etc.

**Edit User:**
1. Select a user
2. Click "Edit" button
3. Modify user details:
   - Change role (Student → Organizer, etc.)
   - Update email
   - Reset password
4. Save changes

**Block/Unblock User:**
1. Select user
2. Click "Block User" or "Unblock User"
3. Enter reason (for blocking)
4. Confirm action

**Delete User:**
1. Select user
2. Click "Delete User"
3. Review impact (events, bookings)
4. Confirm deletion (double confirmation)

**Expected Results:**

**View:**
- ✅ All users displayed in table (Treeview)
- ✅ Shows: Name, Email, Role, Status, Registration Date
- ✅ Search filters list
- ✅ Role filter dropdown works
- ✅ Sort by column headers
- ✅ Pagination for large lists

**Edit:**
- ✅ Edit modal opens with user data
- ✅ Role can be changed (dropdown)
- ✅ Email validation on change
- ✅ "Reset Password" sends email
- ✅ Changes saved successfully
- ✅ Audit log records changes

**Block/Unblock:**
- ✅ Block reason required
- ✅ Blocked user cannot login
- ✅ User's active sessions terminated
- ✅ Notification sent to user
- ✅ Can unblock with "Unblock" button
- ✅ Status badge shows "Blocked" in red

**Delete:**
- ✅ Warning shows user's activity:
  - X events created
  - Y bookings made
  - Z registrations
- ✅ Confirmation: "Are you sure? This cannot be undone."
- ✅ Second confirmation required
- ✅ User data anonymized or deleted
- ✅ Events/bookings handled appropriately

**Additional Features:**
- ✅ Right-click context menu for actions
- ✅ Send email to user
- ✅ View user activity log
- ✅ Export user list to CSV
- ✅ Bulk actions (block/unblock multiple)

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 4.5: View Analytics ✅

**Test ID:** ADM-005  
**Priority:** Medium  
**Type:** Functional

**Prerequisites:**
- Logged in as Admin
- System has historical data (events, bookings, users)

**Test Steps:**
1. Navigate to "Analytics" page
2. View overview cards
3. Check each chart/graph
4. Adjust date range filter
5. Export reports

**Expected Results:**

**Overview Cards:**
- ✅ Total Events (with growth %)
- ✅ Active Users (with growth %)
- ✅ Total Bookings (with growth %)
- ✅ Revenue/Usage (with growth %)
- ✅ Cards show trend arrows (↑ or ↓)
- ✅ Real-time data updates

**Charts/Graphs:**

1. **Events by Category (Pie Chart):**
   - ✅ Shows distribution of event categories
   - ✅ Color-coded segments
   - ✅ Hover shows exact count
   - ✅ Legend displays all categories

2. **Monthly Event Registrations (Line Chart):**
   - ✅ Shows trend over time
   - ✅ X-axis: Months
   - ✅ Y-axis: Registration count
   - ✅ Smooth line connecting points

3. **Resource Utilization (Bar Chart):**
   - ✅ Shows usage per resource
   - ✅ X-axis: Resource names
   - ✅ Y-axis: Utilization %
   - ✅ Color gradient (red for low, green for high)

4. **User Growth Over Time (Area Chart):**
   - ✅ Shows cumulative user growth
   - ✅ Smooth gradient fill
   - ✅ Monthly breakdown

5. **Popular Resources (Horizontal Bar):**
   - ✅ Top 10 most booked resources
   - ✅ Sorted by booking count
   - ✅ Shows exact numbers

**Filters:**
- ✅ Date range selector (last 7 days, 30 days, 3 months, year, custom)
- ✅ Filters apply to all charts
- ✅ Charts update smoothly with animation

**Export:**
- ✅ "Export Report" button available
- ✅ Can export as PDF
- ✅ Can export data as Excel
- ✅ Report includes all visible data

**Performance:**
- ✅ Charts load within 3 seconds
- ✅ Smooth animations
- ✅ Responsive to window resize
- ✅ No lag when filtering

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

## 5️⃣ Edge Case Tests

### Test 5.1: Network Failure Handling ✅

**Test ID:** EDGE-001  
**Priority:** High  
**Type:** Error Handling

**Test Steps:**
1. Start application with backend running
2. Login successfully
3. Disconnect network or stop backend
4. Attempt various actions:
   - Browse events
   - Submit a form
   - Load a page
5. Observe error handling

**Expected Results:**
- ✅ Error message appears: "Cannot connect to server"
- ✅ User-friendly error (not technical stack trace)
- ✅ Toast notification or error dialog
- ✅ "Retry" button available
- ✅ Application doesn't crash
- ✅ Previous data remains visible (from cache)
- ✅ User can navigate to other pages
- ✅ Error logged to error.log

**Reconnection Test:**
1. Restore network connection
2. Click "Retry" or perform action again
3. Verify functionality resumes

**Expected:**
- ✅ Successful reconnection
- ✅ Data syncs automatically
- ✅ Success message: "Connection restored"

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 5.2: Invalid Token Handling ✅

**Test ID:** EDGE-002  
**Priority:** High  
**Type:** Security

**Test Steps:**
1. Login successfully
2. Manually expire session token (or wait for timeout)
3. Attempt authenticated action
4. Observe behavior

**Expected Results:**
- ✅ Error detected: "Session expired" or "Invalid token"
- ✅ User logged out automatically
- ✅ Redirected to login page
- ✅ Error message: "Your session has expired. Please login again."
- ✅ Session data cleared
- ✅ Cache cleared
- ✅ No sensitive data exposed
- ✅ Audit log records forced logout

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 5.3: Concurrent Booking Attempts ✅

**Test ID:** EDGE-003  
**Priority:** High  
**Type:** Concurrency

**Scenario:** Two users try to book the same resource for the same time slot simultaneously.

**Test Steps:**
1. **User A:** Login, navigate to "Book Resource"
2. **User B:** Login (different browser/device), navigate to "Book Resource"
3. **Both:** Select same resource, same date, same time slot
4. **User A:** Submit booking first
5. **User B:** Submit booking 1 second later
6. Observe results

**Expected Results:**
- ✅ **User A:** Booking successful, status "Pending"
- ✅ **User B:** Error: "This time slot is no longer available"
- ✅ **User B:** Suggested alternative time slots shown
- ✅ Only one booking created in database
- ✅ No double-booking occurs
- ✅ Backend handles race condition correctly
- ✅ Time slot immediately marked as unavailable

**Test Variations:**
| Scenario | Expected Outcome |
|----------|------------------|
| Identical submissions | First one succeeds, second fails |
| Overlapping times (partial) | First succeeds, second shows conflict |
| Different resources same time | Both succeed |
| Same resource different times | Both succeed |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 5.4: Form Validation Errors ✅

**Test ID:** EDGE-004  
**Priority:** Medium  
**Type:** Validation

**Test Steps:**
Test all forms with invalid inputs:

**1. Registration Form:**
- Empty fields
- Invalid email format
- Weak password
- Mismatched passwords
- Special characters in name

**2. Event Creation Form:**
- Title too short/long
- Description too short
- Past date selected
- End time before start time
- Negative capacity
- Invalid deadline

**3. Booking Form:**
- Past date
- End time before start time
- Empty purpose
- Duration > max allowed

**Expected Results:**
- ✅ Inline validation (real-time as user types)
- ✅ Red border on invalid fields
- ✅ Clear error message below field
- ✅ Submit button disabled until all valid
- ✅ Error persists until corrected
- ✅ Multiple errors shown simultaneously
- ✅ Error messages are user-friendly (not technical)
- ✅ Focus automatically moves to first error on submit

**Error Message Examples:**
| Field | Invalid Input | Expected Message |
|-------|---------------|------------------|
| Email | "notanemail" | "❌ Please enter a valid email address" |
| Password | "weak" | "❌ Password must be at least 8 characters" |
| Event Title | "Ab" | "❌ Title must be between 5-100 characters" |
| Date | "2025-01-01" (past) | "❌ Date must be in the future" |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

### Test 5.5: API Timeout Handling ✅

**Test ID:** EDGE-005  
**Priority:** Medium  
**Type:** Performance

**Test Steps:**
1. Configure API to respond slowly (or simulate with network throttling)
2. Attempt action that calls API:
   - Load events (large dataset)
   - Upload image
   - Submit form
3. Observe timeout behavior

**Expected Results:**
- ✅ Loading indicator appears
- ✅ Request waits for configured timeout (30 seconds default)
- ✅ After timeout, error message appears
- ✅ Error: "Request timed out. Please try again."
- ✅ User can retry action
- ✅ Application doesn't freeze
- ✅ Timeout logged to logs
- ✅ Partial data not saved (all-or-nothing)

**Timeout Configuration:**
```ini
[API]
timeout = 30  # seconds
```

**Test Variations:**
| Action | Expected Timeout | Expected Behavior |
|--------|------------------|-------------------|
| GET /events | 30s | Show cached data if available |
| POST /events | 30s | Show error, don't save partially |
| Image upload | 60s | Longer timeout, progress bar |
| Analytics load | 30s | Show "Loading..." indefinitely until data arrives |

**Actual Results:**
- Status: ⏳ Pending
- Date Tested: 
- Notes: 

**Pass/Fail:** ⬜ Not Tested

---

## 📊 Test Execution Summary

### Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Test Cases** | 24 | 100% |
| **Passed** | 0 | 0% |
| **Failed** | 0 | 0% |
| **Blocked** | 0 | 0% |
| **Not Tested** | 24 | 100% |

### Test Coverage by Category

| Category | Total | Passed | Failed | Coverage |
|----------|-------|--------|--------|----------|
| Authentication Flow | 5 | 0 | 0 | 0% |
| Student Workflows | 5 | 0 | 0 | 0% |
| Organizer Workflows | 4 | 0 | 0 | 0% |
| Admin Workflows | 5 | 0 | 0 | 0% |
| Edge Cases | 5 | 0 | 0 | 0% |

---

## 🐛 Issues Found

*No issues found yet - testing not started*

### Template for Logging Issues:

**Issue #1:**
- **Test ID:** 
- **Severity:** Critical / High / Medium / Low
- **Description:** 
- **Steps to Reproduce:**
  1. 
  2. 
  3. 
- **Expected:** 
- **Actual:** 
- **Screenshots:** 
- **Workaround:** 
- **Status:** Open / Fixed / Won't Fix

---

## 📝 Test Execution Tracking

### Session 1: [Date]
**Tester:** [Name]  
**Environment:** Development  
**Backend Version:** [Version]  
**Frontend Version:** 2.0.0

**Tests Executed:**
- [ ] AUTH-001
- [ ] AUTH-002
- [ ] AUTH-003
- [ ] AUTH-004
- [ ] AUTH-005
- [ ] STU-001
- [ ] STU-002
- [ ] STU-003
- [ ] STU-004
- [ ] STU-005
- [ ] ORG-001
- [ ] ORG-002
- [ ] ORG-003
- [ ] ORG-004
- [ ] ADM-001
- [ ] ADM-002
- [ ] ADM-003
- [ ] ADM-004
- [ ] ADM-005
- [ ] EDGE-001
- [ ] EDGE-002
- [ ] EDGE-003
- [ ] EDGE-004
- [ ] EDGE-005

**Notes:**

**Issues Found:** 0

---

## ✅ Sign-off

### QA Team Sign-off

**QA Lead:** ___________________________  
**Date:** ___________________________  
**Signature:** ___________________________

**Status:** ⏳ Testing In Progress

---

## 📚 Additional Resources

- **Test Data:** See `test_data.json`
- **Backend API Docs:** `/backend_java/API_DOCUMENTATION.md`
- **Frontend Docs:** `/frontend_tkinter/README.md`
- **Bug Tracking:** GitHub Issues
- **Test Automation:** (Future) Selenium/pytest tests

---

**Test Plan Version:** 1.0  
**Last Updated:** October 9, 2025  
**Status:** Ready for Execution
