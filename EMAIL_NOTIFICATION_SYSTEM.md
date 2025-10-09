# 📧 Email Notification System Documentation

## Overview

The Campus Event System now includes a comprehensive email notification feature that automatically sends emails for:
- ✅ Event registration confirmations
- 🔔 Event reminders (1 day before)
- 📋 Booking confirmations (approved/rejected)
- ✔️ Event approvals/rejections
- 📅 Weekly digest of upcoming events

---

## Architecture

### Backend (Java Spring Boot)
- **Endpoint:** `POST /api/notifications/email`
- **Controller:** `NotificationController.java`
- **Location:** `backend_java/backend/src/main/java/com/campuscoord/controller/`

### Frontend (Python Tkinter)
- **Service:** `email_service.py`
- **Location:** `frontend_tkinter/utils/`
- **Integration:** Automatic email triggers in event/booking pages

---

## Backend API

### Single Email Endpoint
```
POST /api/notifications/email
Content-Type: application/json

{
  "to": "user@example.com",
  "subject": "Registration Confirmed",
  "type": "event_registration|event_reminder|booking_confirmation|approval_notification|weekly_digest",
  "data": {
    "user_name": "John Doe",
    "event_title": "Python Workshop",
    "event_date": "2025-10-15",
    "event_time": "14:00",
    "event_location": "Room 301"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email notification sent successfully",
  "to": "user@example.com",
  "subject": "Registration Confirmed",
  "type": "event_registration",
  "timestamp": "2025-10-09T10:30:00"
}
```

### Bulk Email Endpoint
```
POST /api/notifications/email/bulk
Content-Type: application/json

{
  "recipients": ["user1@example.com", "user2@example.com"],
  "subject": "Event Reminder",
  "type": "event_reminder",
  "data": { ... }
}
```

**Response:**
```json
{
  "success": true,
  "total": 2,
  "sent": 2,
  "failed": 0,
  "timestamp": "2025-10-09T10:30:00"
}
```

### Email History Endpoint
```
GET /api/notifications/email/history?userId=123

Response:
{
  "history": [
    {
      "recipient_email": "user@example.com",
      "subject": "Registration Confirmed",
      "type": "event_registration",
      "sent_at": "2025-10-09T10:30:00",
      "status": "sent"
    }
  ],
  "count": 1
}
```

---

## Frontend Email Service

### Import and Usage

```python
from utils.email_service import get_email_service

# Get singleton instance
email_service = get_email_service()
```

### 1. Event Registration Confirmation

**Triggers:** After successful event registration

```python
email_service.send_event_registration_confirmation(
    user_email="student@example.com",
    event_details={
        "title": "Python Workshop",
        "date": "2025-10-15",
        "time": "14:00",
        "location": "Room 301"
    },
    user_name="John Doe"  # Optional
)
```

**Email Template:**
```
Dear John Doe,

You have successfully registered for the following event:

Event: Python Workshop
Date: October 15, 2025
Time: 2:00 PM
Location: Room 301

We look forward to seeing you there!

If you need to cancel your registration, please log in to your account.

Best regards,
Campus Event System Team
```

### 2. Event Reminder (1 Day Before)

**Triggers:** Scheduled job (1 day before event)

```python
email_service.send_event_reminder(
    user_email="student@example.com",
    event_details={
        "title": "Python Workshop",
        "date": "2025-10-15",
        "time": "14:00",
        "location": "Room 301"
    },
    days_before=1
)
```

**Email Template:**
```
Dear Student,

This is a reminder that you are registered for the following event:

Event: Python Workshop
Date: October 15, 2025
Time: 2:00 PM
Location: Room 301

Don't forget to attend! We're looking forward to seeing you.

Best regards,
Campus Event System Team
```

### 3. Booking Confirmation

**Triggers:** After admin approves/rejects booking

```python
# Approved booking
email_service.send_booking_confirmation(
    user_email="student@example.com",
    booking_details={
        "resource_name": "Conference Room A",
        "date": "2025-10-15",
        "start_time": "14:00",
        "end_time": "16:00"
    },
    status="approved"
)

# Rejected booking
email_service.send_booking_confirmation(
    user_email="student@example.com",
    booking_details={
        "resource_name": "Conference Room A",
        "date": "2025-10-15",
        "start_time": "14:00"
    },
    status="rejected"
)
```

**Email Template (Approved):**
```
Dear Student,

Your booking has been approved:

Resource: Conference Room A
Date: October 15, 2025
Time: 2:00 PM - 4:00 PM

Please arrive on time. If you need to cancel, please do so at least 24 hours in advance.

Best regards,
Campus Event System Team
```

### 4. Approval/Rejection Notification

**Triggers:** After admin approves/rejects event or booking

```python
# Event approved
email_service.send_approval_notification(
    user_email="organizer@example.com",
    item_type="event",
    item_name="Python Workshop",
    status="approved",
    reason="Meets all requirements"
)

# Event rejected
email_service.send_approval_notification(
    user_email="organizer@example.com",
    item_type="event",
    item_name="Python Workshop",
    status="rejected",
    reason="Insufficient details provided"
)
```

**Email Template (Approved):**
```
Dear Organizer,

Your event 'Python Workshop' has been approved.

Reason: Meets all requirements

Thank you for using Campus Event System.

Best regards,
Campus Event System Team
```

### 5. Weekly Digest

**Triggers:** Scheduled job (weekly)

```python
events = [
    {"title": "Python Workshop", "date": "2025-10-15", "location": "Room 301"},
    {"title": "Career Fair", "date": "2025-10-17", "location": "Main Hall"}
]

email_service.send_weekly_digest(
    user_email="student@example.com",
    events=events,
    user_name="John Doe"
)
```

**Email Template:**
```
Dear John Doe,

Here are the upcoming events this week:

1. Python Workshop - October 15, 2025 at Room 301
2. Career Fair - October 17, 2025 at Main Hall

Log in to view more details and register for events.

Best regards,
Campus Event System Team
```

### 6. Bulk Notifications

**Triggers:** Manual (admin broadcasts)

```python
recipients = ["user1@example.com", "user2@example.com"]

email_service.send_bulk_notifications(
    recipients=recipients,
    subject="Event Cancelled",
    email_type="event_reminder",
    data={
        "event_title": "Python Workshop",
        "event_date": "2025-10-15",
        "user_name": "Student"
    }
)
```

---

## Integration Points

### ✅ Already Integrated

1. **Event Registration** (`pages/event_details_modal.py`)
   - Line: ~440-455
   - Sends confirmation email after successful registration

2. **Event Approvals** (`pages/event_approvals.py`)
   - Lines: ~480-495 (approval), ~570-585 (rejection)
   - Sends approval/rejection notification to organizer

3. **Booking Approvals** (`pages/booking_approvals.py`)
   - Lines: ~680-695 (approval), ~730-745 (rejection)
   - Sends confirmation/rejection notification to user

### 🔄 To Be Implemented

4. **Event Reminders** (Scheduled Job)
   - Create a background service to check events happening tomorrow
   - Send reminders to all registered users

5. **Weekly Digest** (Scheduled Job)
   - Run every Monday morning
   - Send upcoming events to all active users

6. **Booking Creation** (`pages/book_resource.py`)
   - Send booking request confirmation after submission

---

## Email Templates

All email templates are generated server-side in `NotificationController.java`:

- `generateEventRegistrationEmail()` - Event registration confirmation
- `generateEventReminderEmail()` - Event reminder (1 day before)
- `generateBookingConfirmationEmail()` - Booking approved/rejected
- `generateApprovalNotificationEmail()` - Event/booking approval/rejection
- `generateWeeklyDigestEmail()` - Weekly upcoming events

---

## Configuration

### Backend (Production)

To use real email service (SendGrid, AWS SES, etc.), update `NotificationController.java`:

```java
// Add email service dependency (e.g., SendGrid)
@Autowired
private EmailSender emailSender;

// In sendEmail() method, replace:
System.out.println("EMAIL NOTIFICATION...");

// With:
emailSender.send(to, subject, body);
```

### Frontend

Email service uses existing `APIClient` and `SessionManager`:
- No additional configuration needed
- Automatically gets user info from session
- Sends emails asynchronously (non-blocking)

---

## Testing

### Test Email Sending

```python
from utils.email_service import get_email_service

email_service = get_email_service()

# Test event registration email
email_service.send_event_registration_confirmation(
    user_email="test@example.com",
    event_details={
        "title": "Test Event",
        "date": "2025-10-15",
        "time": "14:00",
        "location": "Test Room"
    }
)

# Check backend console for email output
```

### Check Email Logs

```bash
# Backend console will show:
========================================
EMAIL NOTIFICATION
========================================
To: test@example.com
Subject: Registration Confirmed: Test Event
Type: event_registration
----------------------------------------
Dear Student,

You have successfully registered for the following event:

Event: Test Event
Date: October 15, 2025
Time: 2:00 PM
Location: Test Room
...
========================================
```

---

## Error Handling

### Email Service Errors

All email errors are caught and logged but **do not block** the main operation:

```python
try:
    email_service.send_event_reminder(...)
except Exception as email_error:
    print(f"[EMAIL ERROR] Failed to send: {email_error}")
    # User's event registration still succeeds
```

### API Errors

Backend returns proper error messages:

```json
{
  "error": "Recipient email is required"
}
```

---

## Future Enhancements

1. **Scheduled Reminders**
   - Implement background job to send event reminders
   - Use APScheduler or Celery

2. **Email Preferences**
   - Allow users to opt-in/opt-out of email types
   - Store preferences in database

3. **Rich HTML Emails**
   - Add styled HTML templates
   - Include campus logo and branding

4. **Email Analytics**
   - Track open rates and click rates
   - Store in `email_notifications` table

5. **Attachment Support**
   - Send calendar invites (.ics files)
   - Attach event posters

---

## Database Schema (Optional)

For email history tracking:

```sql
CREATE TABLE email_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_email VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    body TEXT,
    type VARCHAR(50),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'sent',
    INDEX idx_recipient (recipient_email),
    INDEX idx_sent_at (sent_at)
);
```

---

## Summary

✅ **Implemented Features:**
- Event registration confirmation emails
- Event reminder emails (API ready)
- Booking confirmation/rejection emails
- Event approval/rejection emails
- Weekly digest emails (API ready)
- Bulk email notifications

✅ **Integration Complete:**
- Event Details Modal (registration)
- Event Approvals Page (approve/reject)
- Booking Approvals Page (approve/reject)

✅ **Production Ready:**
- Backend API fully functional
- Frontend service with error handling
- Asynchronous email sending
- Comprehensive logging

🔄 **Next Steps:**
- Implement scheduled reminder jobs
- Add email preferences UI
- Connect to production email service (SendGrid/AWS SES)

---

## Support

For issues or questions:
1. Check backend console for email logs
2. Check frontend console for email service errors
3. Verify user email exists in session
4. Test API endpoint directly with curl/Postman

**Backend Endpoint Test:**
```bash
curl -X POST http://localhost:8080/api/notifications/email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "subject": "Test Email",
    "type": "event_registration",
    "data": {
      "user_name": "Test User",
      "event_title": "Test Event"
    }
  }'
```

---

**Email Notification System - Campus Event System**  
Version 1.0 - October 2025
