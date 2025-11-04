# 📧 Email Notification Quick Reference

## ✅ Implementation Checklist

### Backend
- [x] `NotificationController.java` created
- [x] `POST /api/notifications/email` endpoint
- [x] `POST /api/notifications/email/bulk` endpoint
- [x] `GET /api/notifications/email/history` endpoint
- [x] 5 email templates implemented
- [ ] Production email service integration (SendGrid/AWS SES)

### Frontend
- [x] `email_service.py` created with all methods
- [x] Event registration confirmation (event_details_modal.py)
- [x] Event approval notification (event_approvals.py)
- [x] Event rejection notification (event_approvals.py)
- [x] Booking approval notification (booking_approvals.py)
- [x] Booking rejection notification (booking_approvals.py)
- [ ] Scheduled reminder job
- [ ] Weekly digest job

---

## 🚀 Quick Start

### 1. Test Email System

```bash
cd frontend_tkinter
python test_email_notifications.py
```

### 2. Use in Your Code

```python
from utils.email_service import get_email_service

email_service = get_email_service()

# Event registration
email_service.send_event_registration_confirmation(
    user_email="user@example.com",
    event_details={"title": "Workshop", "date": "2025-10-15"}
)

# Event reminder
email_service.send_event_reminder(
    user_email="user@example.com",
    event_details={"title": "Workshop", "date": "2025-10-15"}
)

# Booking confirmation
email_service.send_booking_confirmation(
    user_email="user@example.com",
    booking_details={"resource_name": "Room A", "date": "2025-10-15"},
    status="approved"
)

# Approval/rejection
email_service.send_approval_notification(
    user_email="user@example.com",
    item_type="event",
    item_name="Workshop",
    status="approved",
    reason="Looks good!"
)

# Weekly digest
email_service.send_weekly_digest(
    user_email="user@example.com",
    events=[{"title": "Workshop", "date": "2025-10-15"}]
)
```

---

## 📋 Email Types

| Type | Trigger | Template |
|------|---------|----------|
| `event_registration` | User registers for event | Registration confirmed |
| `event_reminder` | 1 day before event | Don't forget! |
| `booking_confirmation` | Admin approves/rejects booking | Booking status |
| `approval_notification` | Admin approves/rejects event | Approval/rejection reason |
| `weekly_digest` | Weekly schedule | Upcoming events list |

---

## 🔌 Integration Points

### Already Integrated ✅

1. **Event Registration** (event_details_modal.py line ~445)
2. **Event Approval** (event_approvals.py line ~485)
3. **Event Rejection** (event_approvals.py line ~575)
4. **Booking Approval** (booking_approvals.py line ~685)
5. **Booking Rejection** (booking_approvals.py line ~735)

### To Integrate ⏳

6. **Booking Creation** - Add to book_resource.py
7. **Event Reminders** - Create scheduled job
8. **Weekly Digest** - Create scheduled job

---

## 🧪 Testing

### Test Single Email
```bash
curl -X POST http://localhost:8080/api/notifications/email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "subject": "Test",
    "type": "event_registration",
    "data": {"event_title": "Test Event"}
  }'
```

### Check Backend Console
Look for:
```
========================================
EMAIL NOTIFICATION
========================================
To: test@example.com
Subject: Test
Type: event_registration
...
```

---

## 📊 Email Data Fields

### Event Details
```python
{
    "title": "Event name",           # or "name"
    "date": "2025-10-15",            # or "start_date"
    "time": "14:00",                 # or "start_time"
    "location": "Room 301",          # or "venue"
    "user_name": "John Doe"          # Optional, uses session
}
```

### Booking Details
```python
{
    "resource_name": "Room A",       # or "name"
    "date": "2025-10-15",            # or "booking_date"
    "start_time": "14:00",           # or "time"
    "end_time": "16:00",             # Optional
    "user_name": "Jane Smith"        # Optional, uses session
}
```

### Approval Data
```python
{
    "item_type": "event|booking",    # Type of item
    "item_name": "Event name",       # Name
    "status": "approved|rejected",   # Status
    "reason": "Optional reason",     # Reason
    "user_name": "Organizer"         # Optional, uses session
}
```

---

## 🔧 Configuration

### Development (Current)
- Emails logged to backend console
- No actual email sending
- Use for testing

### Production
Add to `NotificationController.java`:

```java
// 1. Add dependency (pom.xml)
<dependency>
    <groupId>com.sendgrid</groupId>
    <artifactId>sendgrid-java</artifactId>
</dependency>

// 2. Add to application.properties
sendgrid.api.key=YOUR_API_KEY
email.from=noreply@campus.edu

// 3. Inject email service
@Autowired
private EmailService emailService;

// 4. Replace console log with:
emailService.send(to, subject, body);
```

---

## 🎯 Best Practices

1. **Always catch email errors** - Don't block main operation
2. **Use async sending** - Don't wait for email response
3. **Validate email addresses** - Check format before sending
4. **Log all emails** - Track delivery status
5. **Handle failures gracefully** - Retry or queue for later

---

## 📝 Example Integration

### Add to Any Page

```python
# 1. Import
from utils.email_service import get_email_service

# 2. Get service
email_service = get_email_service()

# 3. Send email (in try-except)
try:
    # After API success
    response = self.api.post("endpoint", data)
    
    # Send email
    user = self.session.get_user()
    if user and user.get('email'):
        email_service.send_event_registration_confirmation(
            user_email=user['email'],
            event_details=event_data,
            user_name=user.get('name')
        )
        print("[EMAIL] Notification sent")
        
except Exception as email_error:
    # Don't block main operation
    print(f"[EMAIL ERROR] {email_error}")
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No email in console | Check backend is running |
| Import error | Restart frontend app |
| User email missing | Check session data |
| API error 404 | Rebuild backend (mvn clean install) |
| Email not sending | Check backend logs for errors |

---

## 📚 Files Created/Modified

### Created
- `backend_java/.../NotificationController.java` - Email API
- `frontend_tkinter/utils/email_service.py` - Email service
- `frontend_tkinter/test_email_notifications.py` - Test script
- `EMAIL_NOTIFICATION_SYSTEM.md` - Full documentation
- `EMAIL_QUICK_REFERENCE.md` - This file

### Modified
- `pages/event_details_modal.py` - Added registration email
- `pages/event_approvals.py` - Added approval/rejection emails
- `pages/booking_approvals.py` - Added booking emails

---

## ✅ Status

**System Status:** ✅ READY FOR TESTING

**Next Steps:**
1. Restart backend to load NotificationController
2. Run test_email_notifications.py
3. Check backend console for email output
4. Test live in app (register for event, approve/reject)

---

**Last Updated:** October 2025  
**Version:** 1.0
