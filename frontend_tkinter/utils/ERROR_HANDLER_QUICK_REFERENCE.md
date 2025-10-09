# Error Handler - Quick Reference

Quick lookup guide for the Error Handler system.

## Import

```python
from utils.error_handler import (
    ErrorHandler,
    get_error_handler,
    setup_error_handling,
    require_login,
    require_role,
    handle_errors,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    SessionExpiredError
)
```

---

## Setup (One Time)

```python
from utils.error_handler import setup_error_handling

# In main app initialization
error_handler = setup_error_handling(
    toast_callback=lambda msg, type: Toast(root, msg, type).show(),
    logout_callback=lambda: SessionManager().clear_session(),
    login_redirect_callback=lambda: app.show_page('login')
)
```

---

## Quick Usage

### Get Handler

```python
from utils.error_handler import get_error_handler

handler = get_error_handler()
```

### Handle API Error

```python
try:
    response = api_client.get('/events')
except Exception as error:
    handler.handle_api_error(error, context="Loading events")
```

### Handle Validation Error

```python
if not email:
    handler.handle_validation_error(
        field="Email",
        message="Email is required",
        widget=email_entry  # Highlights widget
    )
```

### Handle Network Error

```python
handler.handle_network_error()
```

### Log Error

```python
try:
    result = risky_operation()
except Exception as error:
    handler.log_error(error, context="Risky operation")
```

---

## Decorators

### @require_login

```python
@require_login
def view_profile(self):
    """Only logged-in users"""
    pass
```

### @require_role

```python
@require_role('ADMIN')
def delete_user(self, user_id):
    """Only ADMIN"""
    pass

@require_role('ADMIN', 'ORGANIZER')
def create_event(self):
    """ADMIN or ORGANIZER"""
    pass
```

### @handle_errors

```python
@handle_errors(context="Loading events", return_on_error=[])
def load_events(self):
    """Auto error handling"""
    return api_client.get('/events')

@handle_errors(context="Saving", return_on_error=False)
def save_event(self, data):
    """Returns False on error"""
    api_client.post('/events', data)
    return True
```

---

## Custom Exceptions

### ValidationError

```python
if len(password) < 8:
    raise ValidationError("Password", "Must be at least 8 characters")
```

### AuthenticationError

```python
if not session.is_logged_in():
    raise AuthenticationError("User must be logged in")
```

### AuthorizationError

```python
if user_role != 'ADMIN':
    raise AuthorizationError(required_role='ADMIN', user_role=user_role)
```

### SessionExpiredError

```python
if token_expired:
    raise SessionExpiredError("Session has expired")
```

---

## Common Patterns

### Pattern 1: API Call with Error Handling

```python
@handle_errors(context="Loading events", return_on_error=[])
def load_events(self):
    return api_client.get('/events')

# Usage
events = self.load_events()  # Returns [] on error
```

### Pattern 2: Form Validation

```python
def validate_form(self):
    handler = get_error_handler()
    
    # Email
    email = self.email_entry.get()
    is_valid, error_msg = validate_email(email)
    if not is_valid:
        handler.handle_validation_error("Email", error_msg, self.email_entry)
        return False
    
    # Password
    password = self.password_entry.get()
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        handler.handle_validation_error("Password", error_msg, self.password_entry)
        return False
    
    return True
```

### Pattern 3: Protected Page

```python
class AdminPanel:
    
    @require_role('ADMIN')
    def __init__(self, parent):
        """Only ADMIN can access"""
        self.parent = parent
        self.create_widgets()
```

### Pattern 4: Manual Error Handling

```python
def delete_user(self, user_id):
    try:
        api_client.delete(f'/users/{user_id}')
        Toast(self, "User deleted", "success").show()
        return True
    except requests.HTTPError as error:
        handler = get_error_handler()
        handler.handle_api_error(error, f"Deleting user {user_id}")
        return False
```

### Pattern 5: Combining Decorators

```python
@handle_errors(context="Admin action", return_on_error=False)
@require_role('ADMIN')
def admin_action(self):
    """Requires ADMIN role + automatic error handling"""
    return api_client.post('/admin/action', data)
```

---

## Status Codes → Messages

| Code | Message |
|------|---------|
| 400 | "Invalid request. Check your input." |
| 401 | "Authentication failed. Logging out..." |
| 403 | "Access denied. No permission." |
| 404 | "Resource not found." |
| 500 | "Server error. Try again later." |
| Connection | "Cannot connect. Check internet." |
| Timeout | "Request timed out." |

---

## Best Practices

### ✅ DO

```python
# Provide context
handler.handle_api_error(error, context="Creating event for Tech Week")

# Use decorators for access control
@require_role('ADMIN')
def admin_function(self):
    pass

# Highlight widgets on validation errors
handler.handle_validation_error("Email", error_msg, email_entry)

# Setup error handler early
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_error_handler()  # FIRST
        self.setup_ui()
```

### ❌ DON'T

```python
# No context
handler.handle_api_error(error)  # Bad

# Manual role checking
def admin_function(self):
    if role != 'ADMIN':
        return  # Bad

# Ignore validation errors
if not email:
    print("Error")  # Bad

# Print exceptions
try:
    something()
except Exception as e:
    print(e)  # Bad
```

---

## Files

- **Main Module**: `utils/error_handler.py`
- **Documentation**: `utils/ERROR_HANDLER_README.md`
- **Examples**: `utils/error_handler_examples.py`
- **Error Log**: `logs/error.log`

---

## Run Examples

```bash
cd utils
python3 error_handler_examples.py
```

---

## Get Log Path

```python
handler = get_error_handler()
log_path = handler.get_log_file_path()
print(f"Errors logged to: {log_path}")
```

---

## Clear Log

```python
handler = get_error_handler()
handler.clear_log_file()
```

---

## Troubleshooting

### Toast not showing

```python
# Make sure callback is set
error_handler.set_toast_callback(show_toast_function)
```

### Widget highlighting not working

```python
# Only works with Entry/Text widgets
if isinstance(widget, (tk.Entry, tk.Text)):
    handler.handle_validation_error(field, msg, widget)
```

### Decorators not working

```python
# Apply from inside out
@handle_errors(context="Action")  # Outside
@require_role('ADMIN')             # Inside
def function(self):
    pass
```

---

**Version:** 1.6.0  
**For Full Docs:** See `utils/ERROR_HANDLER_README.md`
