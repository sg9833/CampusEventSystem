# Error Handler Documentation

Complete guide for the Error Handler system in Campus Event System.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [ErrorHandler Class](#errorhandler-class)
5. [Custom Exceptions](#custom-exceptions)
6. [Decorators](#decorators)
7. [Error Types](#error-types)
8. [Integration Guide](#integration-guide)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Error Handler system provides centralized error handling, logging, and user-friendly error messages for the Campus Event System. It handles:

- **API/HTTP errors** (401, 403, 404, 500, etc.)
- **Validation errors** (form field validation)
- **Network errors** (connection issues)
- **Session management** (authentication, authorization)
- **Generic exceptions** (unexpected errors)

### Key Features

- ✅ Singleton pattern for global access
- ✅ Automatic error logging to file
- ✅ User-friendly error messages
- ✅ Toast notification integration
- ✅ Widget highlighting for validation errors
- ✅ Authentication decorators (@require_login)
- ✅ Authorization decorators (@require_role)
- ✅ Generic error handler decorator (@handle_errors)
- ✅ Session expiration handling
- ✅ Comprehensive error logging with context

---

## Installation

The error handler is already included in the utils package. No additional installation required.

```python
from utils.error_handler import (
    ErrorHandler,
    get_error_handler,
    setup_error_handling,
    require_login,
    require_role,
    handle_errors
)
```

---

## Quick Start

### Basic Usage

```python
from utils.error_handler import get_error_handler

# Get error handler instance
handler = get_error_handler()

# Handle API error
try:
    response = api_client.get('/events')
except Exception as error:
    handler.handle_api_error(error, context="Loading events")

# Handle validation error
if not email:
    handler.handle_validation_error("Email", "Email is required", email_entry)

# Handle network error
handler.handle_network_error()

# Log error
handler.log_error(error, context="Processing booking")
```

### Setup with Callbacks

```python
from utils.error_handler import setup_error_handling
from components.custom_widgets import Toast

def show_toast(message, toast_type):
    Toast(root, message, toast_type).show()

def logout():
    session = SessionManager()
    session.clear_session()

def redirect_to_login():
    # Navigate to login page
    app.show_page('login')

# Setup error handler
error_handler = setup_error_handling(
    toast_callback=show_toast,
    logout_callback=logout,
    login_redirect_callback=redirect_to_login
)
```

### Using Decorators

```python
from utils.error_handler import require_login, require_role, handle_errors

class EventService:
    
    @require_login
    def view_events(self):
        """Only logged-in users can view events"""
        return api_client.get('/events')
    
    @require_role('ADMIN', 'ORGANIZER')
    def create_event(self, event_data):
        """Only ADMIN or ORGANIZER can create events"""
        return api_client.post('/events', event_data)
    
    @handle_errors(context="Loading user profile", return_on_error={})
    def load_profile(self, user_id):
        """Load profile with automatic error handling"""
        return api_client.get(f'/users/{user_id}')
```

---

## ErrorHandler Class

### Singleton Instance

```python
from utils.error_handler import ErrorHandler, get_error_handler

# Get singleton instance (both are equivalent)
handler1 = ErrorHandler()
handler2 = get_error_handler()

# Both reference the same instance
assert handler1 is handler2  # True
```

### Methods

#### 1. `handle_api_error(error, context="")`

Handle API/HTTP errors with user-friendly messages.

**Parameters:**
- `error` (Exception): The exception that occurred
- `context` (str): Additional context about where error occurred

**Handles:**
- HTTP status codes (400, 401, 403, 404, 500, etc.)
- Connection errors
- Timeout errors
- Invalid responses

**Example:**

```python
try:
    response = api_client.post('/events', event_data)
except Exception as error:
    handler.handle_api_error(error, context="Creating event")
```

**User Messages by Status Code:**

| Status Code | User Message |
|-------------|--------------|
| 400 | Invalid request. Please check your input and try again. |
| 401 | Authentication failed. Please log in again. |
| 403 | Access denied. You don't have permission to perform this action. |
| 404 | The requested resource was not found. |
| 409 | A conflict occurred. The resource may already exist. |
| 422 | Validation failed. Please check your input. |
| 500 | Server error occurred. Please try again later. |
| 502 | Bad gateway. The server is temporarily unavailable. |
| 503 | Service unavailable. Please try again later. |
| 504 | Gateway timeout. The request took too long. |

#### 2. `handle_validation_error(field, message, widget=None)`

Handle form validation errors with optional widget highlighting.

**Parameters:**
- `field` (str): Name of the field that failed validation
- `message` (str): Error message to display
- `widget` (tk.Widget, optional): Widget to highlight

**Example:**

```python
from utils.validators import validate_email

email = email_entry.get()
is_valid, error_msg = validate_email(email)

if not is_valid:
    handler.handle_validation_error(
        field="Email",
        message=error_msg,
        widget=email_entry  # Will be highlighted in red
    )
```

**Widget Highlighting:**
- Changes background to light red (#FFEBEE)
- Changes text color to dark red (#C62828)
- Sets focus to the widget
- Restores original style after 3 seconds

#### 3. `handle_network_error()`

Handle network connection errors.

**Example:**

```python
try:
    response = api_client.get('/events')
except requests.ConnectionError:
    handler.handle_network_error()
```

**Shows:**
- Toast notification: "Network Error: Please check your internet connection."
- Detailed messagebox with checklist:
  - Check internet connection
  - Verify server is running
  - Check firewall settings

#### 4. `handle_session_expired()`

Handle expired user session.

**Actions:**
1. Shows toast notification
2. Calls logout callback (clears session)
3. Calls login redirect callback (navigates to login)

**Example:**

```python
# Automatically called on 401 errors
# Can also be called manually
handler.handle_session_expired()
```

#### 5. `handle_authorization_error(required_role, user_role=None)`

Handle authorization (permission) errors.

**Parameters:**
- `required_role` (str): Role required for the action
- `user_role` (str, optional): Current user's role

**Example:**

```python
session = SessionManager()
user_role = session.get_role()

if user_role != 'ADMIN':
    handler.handle_authorization_error(
        required_role='ADMIN',
        user_role=user_role
    )
```

#### 6. `log_error(error, context="")`

Log error to file with context and traceback.

**Parameters:**
- `error` (Exception): The exception to log
- `context` (str): Additional context

**Example:**

```python
try:
    result = complex_calculation()
except Exception as error:
    handler.log_error(error, context="Calculating event capacity")
    # Continue execution or handle gracefully
```

**Log Format:**
```
================================================================================
Error Type: ValueError
Error Message: invalid literal for int() with base 10: 'abc'
Context: Calculating event capacity
Timestamp: 2025-10-09 14:30:45
Traceback:
  File "main.py", line 123, in calculate
    capacity = int(capacity_str)
ValueError: invalid literal for int() with base 10: 'abc'
================================================================================
```

#### 7. `handle_exception(error, context="", show_details=False)`

Generic exception handler - routes to appropriate handler.

**Parameters:**
- `error` (Exception): The exception to handle
- `context` (str): Additional context
- `show_details` (bool): Whether to show technical details to user

**Example:**

```python
try:
    process_booking(booking_data)
except Exception as error:
    handler.handle_exception(
        error,
        context="Processing booking",
        show_details=True  # Show error details in development
    )
```

#### 8. Callback Registration

```python
# Set toast notification callback
handler.set_toast_callback(show_toast_function)

# Set logout callback
handler.set_logout_callback(logout_function)

# Set login redirect callback
handler.set_login_redirect_callback(redirect_function)
```

#### 9. Utility Methods

```python
# Get log file path
log_path = handler.get_log_file_path()
print(f"Errors logged to: {log_path}")

# Clear log file
handler.clear_log_file()
```

---

## Custom Exceptions

### ValidationError

Raised when form validation fails.

```python
from utils.error_handler import ValidationError

if len(password) < 8:
    raise ValidationError(
        field="Password",
        message="Password must be at least 8 characters"
    )
```

**Attributes:**
- `field` (str): Field name
- `message` (str): Error message

### AuthenticationError

Raised when user is not authenticated.

```python
from utils.error_handler import AuthenticationError

if not session.is_logged_in():
    raise AuthenticationError("User must be logged in")
```

### AuthorizationError

Raised when user lacks required permissions.

```python
from utils.error_handler import AuthorizationError

if user_role != 'ADMIN':
    raise AuthorizationError(
        required_role='ADMIN',
        user_role=user_role
    )
```

**Attributes:**
- `required_role` (str): Required role
- `user_role` (str): User's current role

### SessionExpiredError

Raised when user session has expired.

```python
from utils.error_handler import SessionExpiredError

if token_expired:
    raise SessionExpiredError("Session has expired")
```

---

## Decorators

### @require_login

Check if user is logged in before executing function.

**Usage:**

```python
from utils.error_handler import require_login

class DashboardPage:
    
    @require_login
    def __init__(self, parent):
        """Only logged-in users can access dashboard"""
        # This only executes if user is logged in
        self.create_widgets()
    
    @require_login
    def load_data(self):
        """Load user-specific data"""
        session = SessionManager()
        user = session.get_user()
        # Load data for user
```

**Behavior:**
- Checks `SessionManager().is_logged_in()`
- If not logged in:
  - Calls `handle_session_expired()`
  - Raises `AuthenticationError`
- If logged in: Executes function normally

### @require_role

Check if user has required role before executing function.

**Single Role:**

```python
from utils.error_handler import require_role

class AdminPanel:
    
    @require_role('ADMIN')
    def delete_user(self, user_id):
        """Only ADMIN can delete users"""
        api_client.delete(f'/users/{user_id}')
```

**Multiple Roles:**

```python
@require_role('ADMIN', 'ORGANIZER')
def create_event(self, event_data):
    """ADMIN or ORGANIZER can create events"""
    return api_client.post('/events', event_data)
```

**Behavior:**
- Checks if user is logged in (same as @require_login)
- Checks if user's role matches one of the allowed roles
- If role doesn't match:
  - Calls `handle_authorization_error()`
  - Raises `AuthorizationError`
- If role matches: Executes function normally

### @handle_errors

Wrap function with automatic error handling.

**Basic Usage:**

```python
from utils.error_handler import handle_errors

@handle_errors(context="Loading events")
def load_events():
    """Automatically handles any errors"""
    return api_client.get('/events')
```

**With Return Value:**

```python
@handle_errors(context="Saving event", return_on_error=False)
def save_event(event_data):
    """Returns False if error occurs"""
    api_client.post('/events', event_data)
    return True
```

**With Details:**

```python
@handle_errors(
    context="Processing booking",
    show_toast=True,
    show_details=True,  # Show technical details (for debugging)
    return_on_error=None
)
def process_booking(booking_data):
    # Complex processing
    pass
```

**Parameters:**
- `context` (str): Context description for logging
- `show_toast` (bool): Whether to show toast notification (default: True)
- `show_details` (bool): Whether to show technical details to user (default: False)
- `return_on_error` (Any): Value to return if error occurs (default: None)

---

## Error Types

### 1. API/HTTP Errors

**Types:**
- `requests.HTTPError` - HTTP status code errors
- `requests.ConnectionError` - Network connection failures
- `requests.Timeout` - Request timeout
- `ValueError` - Invalid JSON response

**Handling:**

```python
try:
    response = api_client.get('/events')
except requests.HTTPError as error:
    handler.handle_api_error(error, "Loading events")
except requests.ConnectionError:
    handler.handle_network_error()
except requests.Timeout as error:
    handler.handle_api_error(error, "Loading events")
```

### 2. Validation Errors

**Types:**
- Form field validation failures
- Data format errors
- Required field errors

**Handling:**

```python
from utils.validators import validate_email, validate_password

email = email_entry.get()
is_valid, error_msg = validate_email(email)

if not is_valid:
    handler.handle_validation_error("Email", error_msg, email_entry)
    return

password = password_entry.get()
is_valid, error_msg = validate_password(password)

if not is_valid:
    handler.handle_validation_error("Password", error_msg, password_entry)
    return
```

### 3. Authentication Errors

**Types:**
- User not logged in
- Invalid credentials
- Session expired

**Handling:**

```python
session = SessionManager()

if not session.is_logged_in():
    handler.handle_session_expired()
    return
```

### 4. Authorization Errors

**Types:**
- Insufficient permissions
- Role mismatch
- Access denied

**Handling:**

```python
session = SessionManager()
user_role = session.get_role()

if user_role not in ['ADMIN', 'ORGANIZER']:
    handler.handle_authorization_error(
        required_role='ADMIN/ORGANIZER',
        user_role=user_role
    )
    return
```

---

## Integration Guide

### Step 1: Setup Error Handler in Main Application

```python
# main.py

from utils.error_handler import setup_error_handling
from utils.session_manager import SessionManager
from components.custom_widgets import Toast

class CampusEventApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        # Setup error handler FIRST
        self.setup_error_handler()
        
        # Then setup rest of app
        self.setup_ui()
    
    def setup_error_handler(self):
        """Setup error handler with callbacks"""
        
        def show_toast(message, toast_type):
            Toast(self, message, toast_type).show()
        
        def logout():
            session = SessionManager()
            session.clear_session()
            # Clear any user-specific data
            self.clear_user_data()
        
        def redirect_to_login():
            self.show_page('login')
        
        self.error_handler = setup_error_handling(
            toast_callback=show_toast,
            logout_callback=logout,
            login_redirect_callback=redirect_to_login
        )
```

### Step 2: Use in API Calls

```python
# utils/api_client.py or service classes

from utils.error_handler import get_error_handler, handle_errors

class EventService:
    
    def __init__(self):
        self.api_client = APIClient()
        self.error_handler = get_error_handler()
    
    @handle_errors(context="Loading events", return_on_error=[])
    def get_events(self, filters=None):
        """Load events with automatic error handling"""
        endpoint = '/events'
        if filters:
            endpoint += f'?{urlencode(filters)}'
        return self.api_client.get(endpoint)
    
    def create_event(self, event_data):
        """Create event with manual error handling"""
        try:
            response = self.api_client.post('/events', event_data)
            return response
        except Exception as error:
            self.error_handler.handle_api_error(error, "Creating event")
            return None
```

### Step 3: Use in Form Validation

```python
# pages/event_form.py

from utils.error_handler import get_error_handler
from utils.validators import validate_required_field, validate_date

class EventFormPage:
    
    def __init__(self, parent):
        self.error_handler = get_error_handler()
        self.create_form()
    
    def validate_form(self):
        """Validate form fields"""
        
        # Title
        title = self.title_entry.get()
        is_valid, error_msg = validate_required_field(title)
        if not is_valid:
            self.error_handler.handle_validation_error(
                "Title", error_msg, self.title_entry
            )
            return False
        
        # Date
        date = self.date_entry.get()
        is_valid, error_msg = validate_date(date)
        if not is_valid:
            self.error_handler.handle_validation_error(
                "Date", error_msg, self.date_entry
            )
            return False
        
        return True
    
    def submit_form(self):
        """Submit form if valid"""
        if not self.validate_form():
            return
        
        # Proceed with submission
        event_data = self.get_form_data()
        # ... submit to API
```

### Step 4: Use Decorators for Protected Pages

```python
# pages/admin_panel.py

from utils.error_handler import require_login, require_role

class AdminPanel:
    
    @require_role('ADMIN')
    def __init__(self, parent):
        """Only ADMIN can access this page"""
        self.parent = parent
        self.create_widgets()
    
    @require_role('ADMIN')
    def delete_user(self, user_id):
        """Only ADMIN can delete users"""
        # Deletion logic
        pass
```

```python
# pages/student_dashboard.py

from utils.error_handler import require_login

class StudentDashboard:
    
    @require_login
    def __init__(self, parent):
        """All logged-in users can access dashboard"""
        self.parent = parent
        self.load_data()
        self.create_widgets()
    
    @require_login
    def load_data(self):
        """Load user-specific data"""
        # Data loading logic
        pass
```

---

## Best Practices

### 1. Use Decorators for Access Control

✅ **DO:**
```python
@require_role('ADMIN')
def admin_function(self):
    pass
```

❌ **DON'T:**
```python
def admin_function(self):
    if session.get_role() != 'ADMIN':
        # Manual check
        pass
```

### 2. Always Provide Context

✅ **DO:**
```python
handler.handle_api_error(error, context="Creating event for Tech Week")
```

❌ **DON'T:**
```python
handler.handle_api_error(error)  # No context
```

### 3. Use @handle_errors for API Calls

✅ **DO:**
```python
@handle_errors(context="Loading events", return_on_error=[])
def load_events(self):
    return api_client.get('/events')
```

❌ **DON'T:**
```python
def load_events(self):
    try:
        return api_client.get('/events')
    except Exception as e:
        print(e)  # Bad error handling
        return []
```

### 4. Highlight Widgets on Validation Errors

✅ **DO:**
```python
handler.handle_validation_error("Email", error_msg, email_entry)
```

❌ **DON'T:**
```python
handler.handle_validation_error("Email", error_msg)  # No widget highlight
```

### 5. Setup Callbacks Early

✅ **DO:**
```python
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_error_handler()  # FIRST
        self.setup_ui()
```

❌ **DON'T:**
```python
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_error_handler()  # TOO LATE
```

### 6. Log Errors Even When Handled

✅ **DO:**
```python
try:
    result = risky_operation()
except Exception as error:
    handler.log_error(error, "Risky operation")
    # Handle gracefully
    result = default_value
```

### 7. Use Appropriate Error Types

✅ **DO:**
```python
if not valid:
    raise ValidationError("email", "Invalid format")
```

❌ **DON'T:**
```python
if not valid:
    raise Exception("Invalid email")  # Generic
```

### 8. Clear Error Logs Periodically

```python
# In maintenance function
handler = get_error_handler()
log_path = handler.get_log_file_path()

# Archive old logs
if os.path.getsize(log_path) > 10_000_000:  # 10 MB
    archive_log(log_path)
    handler.clear_log_file()
```

---

## Troubleshooting

### Error: "Toast callback failed"

**Problem:** Toast notification callback raises exception.

**Solution:**
```python
def show_toast(message, toast_type):
    try:
        Toast(root, message, toast_type).show()
    except Exception as e:
        # Fallback to messagebox
        print(f"Toast failed: {e}")
```

### Error: Widget highlighting not working

**Problem:** Widget doesn't support `config()` method.

**Solution:** Only pass Entry, Text, or ttk widgets:
```python
if isinstance(widget, (tk.Entry, tk.Text, ttk.Entry)):
    handler.handle_validation_error(field, message, widget)
else:
    handler.handle_validation_error(field, message)  # No widget
```

### Error: "Logger is None"

**Problem:** Error handler not properly initialized.

**Solution:** Always use singleton pattern:
```python
# ✅ Correct
handler = get_error_handler()

# ❌ Wrong
handler = ErrorHandler.__new__(ErrorHandler)  # Don't do this
```

### Decorators not working

**Problem:** Decorators applied in wrong order.

**Solution:** Apply from inside out:
```python
# ✅ Correct
@handle_errors(context="Admin action")
@require_role('ADMIN')
def admin_function(self):
    pass

# ❌ Wrong
@require_role('ADMIN')
@handle_errors(context="Admin action")
def admin_function(self):
    pass
```

### Log file too large

**Problem:** error.log grows too large.

**Solution:** Implement log rotation:
```python
import shutil
from datetime import datetime

handler = get_error_handler()
log_path = handler.get_log_file_path()

# Rotate if > 10 MB
if os.path.getsize(log_path) > 10_000_000:
    # Archive
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_path = f"{log_path}.{timestamp}"
    shutil.copy(log_path, archive_path)
    
    # Clear current log
    handler.clear_log_file()
```

---

## Additional Resources

- **Examples:** See `utils/error_handler_examples.py` for comprehensive examples
- **Validators:** See `utils/validators.py` for validation functions
- **Session Manager:** See `utils/session_manager.py` for session handling
- **API Client:** See `utils/api_client.py` for API integration
- **Custom Widgets:** See `components/custom_widgets.py` for Toast component

---

**Version:** 1.6.0  
**Last Updated:** October 9, 2025  
**Author:** Campus Event System Team
