# Security System Documentation

## Version 1.7.0

Complete security system for the Campus Event Management System with encryption, rate limiting, session management, input sanitization, and secure password handling.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Components](#components)
5. [Usage Examples](#usage-examples)
6. [Integration Guide](#integration-guide)
7. [Best Practices](#best-practices)
8. [API Reference](#api-reference)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Security System provides enterprise-grade security features for protecting user data, preventing attacks, and managing sessions. It includes:

- **Data Encryption**: Fernet symmetric encryption with PBKDF2 key derivation
- **Rate Limiting**: Sliding window algorithm (100 requests/minute default)
- **Session Timeout**: Automatic logout after 30 minutes of inactivity
- **Input Sanitization**: XSS and SQL injection prevention
- **File Validation**: Size, extension, and MIME type checking
- **Secure Password Handling**: PBKDF2 hashing with 100,000 iterations
- **Token Management**: Automatic token refresh before expiry
- **CSRF Protection**: Secure token generation and validation

### Key Features

✅ **Thread-Safe**: All components support concurrent access  
✅ **Singleton Pattern**: SecurityManager provides unified access  
✅ **Zero Dependencies** (except cryptography): Works with standard library  
✅ **Production Ready**: Tested with comprehensive test suite  
✅ **Well Documented**: Complete API documentation and examples

---

## Installation

### 1. Install Dependencies

```bash
cd frontend_tkinter
pip install -r requirements.txt
```

The `requirements.txt` includes:
```
cryptography>=41.0.0
```

### 2. Import Security Module

```python
from utils.security import get_security_manager

# Get singleton instance
security = get_security_manager()
```

---

## Quick Start

### Basic Usage

```python
from utils.security import get_security_manager

# Get security manager instance
security = get_security_manager()

# Encrypt sensitive data
encrypted = security.encrypt_data("sensitive_info")
decrypted = security.decrypt_data(encrypted)

# Check rate limit
if security.check_rate_limit("user_123"):
    # Process request
    pass

# Sanitize user input
safe_input = security.sanitize_input(user_input)

# Hash password
hashed, salt = security.hash_password(password)

# Verify password
is_valid = security.verify_password(password, hashed, salt)

# Generate CSRF token
token = security.generate_csrf_token(session_id)

# Validate CSRF token
is_valid = security.validate_csrf_token(session_id, token)
```

### Session Timeout Setup

```python
def handle_logout():
    """Called when session times out"""
    print("Session expired. Logging out...")
    # Clear session and redirect to login

def show_warning():
    """Called 5 minutes before timeout"""
    print("Warning: Session will expire in 5 minutes")
    # Show warning dialog to user

# Setup session timeout
security.setup_session_timeout(
    timeout_minutes=30,
    warning_minutes=5,
    on_timeout=handle_logout,
    on_warning=show_warning
)

# Refresh session on user activity
security.refresh_session()
```

---

## Components

### 1. DataEncryption

**Purpose**: Encrypt and decrypt sensitive data using Fernet (AES-128).

**Key Features**:
- Symmetric encryption with authenticated encryption
- PBKDF2 key derivation with SHA-256
- Support for strings and dictionaries
- Base64 encoding for safe storage

**Example**:
```python
from utils.security import DataEncryption

encryption = DataEncryption()

# Encrypt string
encrypted = encryption.encrypt("secret")
decrypted = encryption.decrypt(encrypted)

# Encrypt dictionary
data = {"api_key": "secret123", "token": "abc"}
encrypted_dict = encryption.encrypt_dict(data)
decrypted_dict = encryption.decrypt_dict(encrypted_dict)
```

### 2. RateLimiter

**Purpose**: Prevent API abuse with sliding window rate limiting.

**Key Features**:
- Sliding window algorithm for accuracy
- Configurable limits (default: 100 requests/60 seconds)
- Per-user/per-IP tracking
- Thread-safe implementation

**Example**:
```python
from utils.security import RateLimiter

limiter = RateLimiter(max_requests=100, time_window=60)

# Check if request is allowed
if limiter.is_allowed("user_123"):
    # Process request
    remaining = limiter.get_remaining("user_123")
    print(f"Remaining requests: {remaining}")
else:
    print("Rate limit exceeded")

# Reset limit for user
limiter.reset("user_123")
```

### 3. SessionTimeout

**Purpose**: Automatically logout inactive users.

**Key Features**:
- Background monitoring thread
- Configurable timeout (default: 30 minutes)
- Warning callback (default: 5 minutes before)
- Pause/resume support
- Activity refresh

**Example**:
```python
from utils.security import SessionTimeout

def on_timeout():
    print("Session timed out!")

def on_warning():
    print("Warning: Session expiring soon!")

session = SessionTimeout(
    timeout_minutes=30,
    warning_minutes=5,
    on_timeout=on_timeout,
    on_warning=on_warning
)

session.start()

# User interacts with app
session.refresh()

# Check remaining time
remaining = session.get_remaining_time()
print(f"Session expires in {remaining} seconds")

# Stop monitoring
session.stop()
```

### 4. InputSanitizer

**Purpose**: Prevent XSS and SQL injection attacks.

**Key Features**:
- SQL injection pattern detection
- XSS attack pattern detection
- File upload validation
- Email sanitization
- Filename sanitization

**Example**:
```python
from utils.security import InputSanitizer

sanitizer = InputSanitizer()

# Sanitize user input
safe_text = sanitizer.sanitize_string(user_input)

# Validate email
clean_email = sanitizer.sanitize_email("user@example.com")

# Validate file upload
is_valid = sanitizer.validate_file_upload("image.jpg", "image")

# Sanitize form data
form_data = {
    "name": "John<script>alert('xss')</script>",
    "comment": "'; DROP TABLE users; --"
}
clean_data = sanitizer.sanitize_dict(form_data)
```

### 5. SecurePassword

**Purpose**: Secure password handling without exposure.

**Key Features**:
- PBKDF2-SHA256 hashing with 100,000 iterations
- Constant-time password verification
- Password masking for display
- Secure memory clearing
- Strong password generation

**Example**:
```python
from utils.security import SecurePassword

pwd = SecurePassword()

# Hash password
hashed, salt = pwd.hash_password("MyPassword123")

# Verify password
is_correct = pwd.verify_password("MyPassword123", hashed, salt)

# Mask password for display
masked = pwd.mask_password("MyPassword123")  # "M***********3"

# Generate strong password
strong_pwd = pwd.generate_strong_password(16)

# Clear password entry widget (Tkinter)
pwd.clear_entry(password_entry_widget)
```

### 6. TokenManager

**Purpose**: Manage authentication tokens with automatic refresh.

**Key Features**:
- Token expiry tracking
- Auto-refresh when < 5 minutes remaining
- Thread-safe refresh mechanism
- Token validation

**Example**:
```python
from utils.security import TokenManager

def refresh_callback():
    # Call API to get new token
    new_token = api.refresh_token()
    return new_token

token_manager = TokenManager(refresh_callback=refresh_callback)

# Set token
token_manager.set_token("abc123", expires_in=3600)

# Get token (auto-refreshes if needed)
token = token_manager.get_token()

# Check validity
if token_manager.is_valid():
    # Token is valid
    pass

# Clear token
token_manager.clear()
```

### 7. CSRFProtection

**Purpose**: Prevent Cross-Site Request Forgery attacks.

**Key Features**:
- Secure random token generation
- Constant-time validation
- Token expiry (1 hour)
- Per-session tokens

**Example**:
```python
from utils.security import CSRFProtection

csrf = CSRFProtection()

# Generate token for session
token = csrf.generate_token("session_123")

# Include token in form
# <input type="hidden" name="csrf_token" value="{token}">

# Validate token on form submission
is_valid = csrf.validate_token("session_123", submitted_token)

if not is_valid:
    raise ValueError("Invalid CSRF token")
```

### 8. SecurityManager (Unified Interface)

**Purpose**: Single entry point for all security operations.

**Key Features**:
- Singleton pattern
- Coordinates all security components
- Simplified API
- Thread-safe operations

**Example**:
```python
from utils.security import get_security_manager

security = get_security_manager()

# All security features available through one interface
encrypted = security.encrypt_data("secret")
is_allowed = security.check_rate_limit("user_123")
safe_input = security.sanitize_input(user_input)
hashed, salt = security.hash_password(password)
token = security.generate_csrf_token(session_id)
```

---

## Usage Examples

### Example 1: Secure Login Form

```python
import tkinter as tk
from utils.security import get_security_manager
from utils.session_manager import SessionManager
from utils.api_client import APIClient

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.security = get_security_manager()
        self.api = APIClient()
        self.session = SessionManager()
        
        # Username entry
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()
        
        # Password entry
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()
        
        # Login button
        tk.Button(root, text="Login", command=self.login).pack()
    
    def login(self):
        # Get credentials
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Sanitize username
        safe_username = self.security.sanitize_input(username)
        
        # Check rate limit
        if not self.security.check_rate_limit(safe_username):
            messagebox.showerror("Error", "Too many login attempts")
            return
        
        try:
            # Call login API
            response = self.api.post("auth/login", {
                "username": safe_username,
                "password": password  # Don't sanitize password
            })
            
            # Store session
            self.session.store_user(
                user_id=response["user_id"],
                username=response["username"],
                role=response["role"],
                token=response["token"],
                token_expires_in=response.get("expires_in", 3600)
            )
            
            # Setup session timeout
            self.security.setup_session_timeout(
                timeout_minutes=30,
                warning_minutes=5,
                on_timeout=self.handle_logout,
                on_warning=self.show_timeout_warning
            )
            
            # Navigate to dashboard
            self.show_dashboard()
            
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))
        finally:
            # Clear password field securely
            self.security.clear_password_field(self.password_entry)
    
    def handle_logout(self):
        """Called when session times out"""
        self.session.clear_session()
        messagebox.showinfo("Session Expired", "You have been logged out due to inactivity")
        self.show_login()
    
    def show_timeout_warning(self):
        """Called 5 minutes before timeout"""
        response = messagebox.askyesno(
            "Session Expiring",
            "Your session will expire in 5 minutes. Do you want to continue?"
        )
        if response:
            self.security.refresh_session()
```

### Example 2: Secure API Calls

```python
from utils.api_client import APIClient, RateLimitError
from utils.session_manager import SessionManager
from utils.security import get_security_manager

class EventService:
    def __init__(self):
        self.api = APIClient()
        self.session = SessionManager()
        self.security = get_security_manager()
    
    def create_event(self, event_data):
        """Create event with security features"""
        # Get user ID for rate limiting
        user = self.session.get_user()
        if not user:
            raise ValueError("Not logged in")
        
        try:
            # Use secure API call with sanitization and rate limiting
            response = self.api.secure_post(
                endpoint="events",
                data=event_data,
                user_id=str(user["user_id"]),
                sanitize=True,  # Sanitize all inputs
                exclude_keys=[]  # No exclusions for event data
            )
            
            # Refresh session on activity
            self.security.refresh_session()
            
            return response
            
        except RateLimitError as e:
            raise ValueError(f"Rate limit exceeded: {e}")
    
    def upload_event_image(self, filepath):
        """Upload event image with validation"""
        # Validate file
        is_valid = self.security.validate_file(filepath, "image")
        if not is_valid:
            raise ValueError("Invalid image file")
        
        # TODO: Upload file
        pass
```

### Example 3: Form Input Sanitization

```python
from utils.security import get_security_manager

class EventForm:
    def __init__(self):
        self.security = get_security_manager()
    
    def submit_form(self, form_data):
        """Submit form with sanitized data"""
        # Sanitize all form inputs
        safe_data = self.security.sanitize_form_data(
            data=form_data,
            exclude_keys=[]  # Sanitize all fields
        )
        
        # Validate required fields
        if not safe_data.get("title"):
            raise ValueError("Title is required")
        
        if not safe_data.get("description"):
            raise ValueError("Description is required")
        
        # Submit to API
        # ...
```

### Example 4: Password Change with Security

```python
from utils.security import get_security_manager
import tkinter as tk
from tkinter import messagebox

class PasswordChangeForm:
    def __init__(self, root):
        self.root = root
        self.security = get_security_manager()
        
        # Current password
        tk.Label(root, text="Current Password:").pack()
        self.current_pwd_entry = tk.Entry(root, show="*")
        self.current_pwd_entry.pack()
        
        # New password
        tk.Label(root, text="New Password:").pack()
        self.new_pwd_entry = tk.Entry(root, show="*")
        self.new_pwd_entry.pack()
        
        # Confirm password
        tk.Label(root, text="Confirm Password:").pack()
        self.confirm_pwd_entry = tk.Entry(root, show="*")
        self.confirm_pwd_entry.pack()
        
        # Submit button
        tk.Button(root, text="Change Password", command=self.change_password).pack()
    
    def change_password(self):
        # Get passwords
        current = self.current_pwd_entry.get()
        new_pwd = self.new_pwd_entry.get()
        confirm = self.confirm_pwd_entry.get()
        
        try:
            # Validate passwords match
            if new_pwd != confirm:
                raise ValueError("Passwords do not match")
            
            # Validate password strength (optional)
            if len(new_pwd) < 8:
                raise ValueError("Password must be at least 8 characters")
            
            # Hash new password
            hashed, salt = self.security.hash_password(new_pwd)
            
            # TODO: Verify current password and update in database
            
            messagebox.showinfo("Success", "Password changed successfully")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Clear all password fields securely
            self.security.clear_password_field(self.current_pwd_entry)
            self.security.clear_password_field(self.new_pwd_entry)
            self.security.clear_password_field(self.confirm_pwd_entry)
```

---

## Integration Guide

### Step 1: Update SessionManager

The `SessionManager` has already been updated with security features. Make sure to:

1. Call `refresh_activity()` on all user interactions
2. Check `is_logged_in()` before protected operations
3. Use `get_token()` for API authentication

```python
from utils.session_manager import SessionManager

session = SessionManager()

# On user interaction
session.refresh_activity()

# Before API call
if session.is_logged_in():
    token = session.get_token()
    # Use token for API call
```

### Step 2: Update APIClient

The `APIClient` has been enhanced with secure methods. Use them for all API calls:

```python
from utils.api_client import APIClient

api = APIClient()

# Instead of api.post()
response = api.secure_post(
    endpoint="events",
    data=event_data,
    user_id=user_id,
    sanitize=True
)

# Instead of api.get()
response = api.secure_get(
    endpoint="events",
    user_id=user_id
)
```

### Step 3: Update Form Pages

Apply security to all forms:

```python
from utils.security import get_security_manager

security = get_security_manager()

# Sanitize inputs
safe_data = security.sanitize_form_data(form_data)

# Validate files
if file_path:
    security.validate_file(file_path, "image")

# Clear password fields
security.clear_password_field(password_entry)
```

### Step 4: Setup Session Timeout

In your main application:

```python
from utils.security import get_security_manager

def main():
    root = tk.Tk()
    security = get_security_manager()
    
    # Setup session timeout
    security.setup_session_timeout(
        timeout_minutes=30,
        warning_minutes=5,
        on_timeout=lambda: handle_logout(root),
        on_warning=lambda: show_warning_dialog(root)
    )
    
    # Bind activity refresh to all interactions
    root.bind_all("<Any-KeyPress>", lambda e: security.refresh_session())
    root.bind_all("<Any-ButtonPress>", lambda e: security.refresh_session())
    
    root.mainloop()
```

---

## Best Practices

### 1. Password Security

✅ **DO**:
- Always hash passwords before storage
- Use `clear_password_field()` after submission
- Never log passwords
- Use strong password requirements

❌ **DON'T**:
- Store passwords in plaintext
- Include passwords in log messages
- Sanitize password fields (breaks validation)
- Reuse salts between passwords

### 2. Input Sanitization

✅ **DO**:
- Sanitize all user inputs before storage
- Validate file uploads
- Use `exclude_keys` for passwords
- Sanitize both client and server side

❌ **DON'T**:
- Trust client-side validation only
- Sanitize after storage (sanitize before)
- Skip validation for "trusted" users
- Remove too much (balance security and usability)

### 3. Rate Limiting

✅ **DO**:
- Apply to all public endpoints
- Use user ID for authenticated requests
- Use IP address for anonymous requests
- Provide clear error messages

❌ **DON'T**:
- Set limits too low (frustrates users)
- Skip rate limiting on login endpoints
- Use same identifier for all users
- Forget to handle RateLimitError

### 4. Session Management

✅ **DO**:
- Refresh session on every user interaction
- Show warning before auto-logout
- Clear session on manual logout
- Use token expiry checks

❌ **DON'T**:
- Set timeout too short (< 15 minutes)
- Forget to setup timeout callbacks
- Skip activity refresh
- Store session data unencrypted

### 5. CSRF Protection

✅ **DO**:
- Generate token per session
- Include in all state-changing forms
- Validate on server side
- Use hidden form fields

❌ **DON'T**:
- Reuse tokens across sessions
- Skip validation for "safe" operations
- Store tokens in cookies only
- Use predictable token values

---

## API Reference

See [SECURITY_API_REFERENCE.md](./SECURITY_API_REFERENCE.md) for complete API documentation.

---

## Testing

Run the test suite:

```bash
cd frontend_tkinter/utils
python test_security.py
```

Expected output:
```
........................................
----------------------------------------------------------------------
Ran 40 tests in 15.234s

OK

==================================================================
SECURITY TEST SUMMARY
==================================================================
Tests Run: 40
Successes: 40
Failures: 0
Errors: 0
==================================================================
```

---

## Troubleshooting

### Issue: Import Error for cryptography

**Error**: `ModuleNotFoundError: No module named 'cryptography'`

**Solution**:
```bash
pip install cryptography>=41.0.0
```

### Issue: Rate Limit Exceeded

**Error**: `RateLimitError: Rate limit exceeded`

**Solution**:
1. Wait for time window to pass (default: 1 minute)
2. Implement exponential backoff
3. Contact admin to reset limit if needed

```python
try:
    response = api.secure_post(...)
except RateLimitError:
    # Wait and retry
    time.sleep(60)
    response = api.secure_post(...)
```

### Issue: Session Timeout Not Working

**Problem**: Session doesn't timeout after inactivity

**Solution**:
1. Verify `setup_session_timeout()` was called
2. Check if `refresh_session()` is called on activity
3. Ensure timeout callbacks are defined

```python
# Verify setup
security = get_security_manager()
security.setup_session_timeout(
    timeout_minutes=30,
    warning_minutes=5,
    on_timeout=handle_logout,
    on_warning=show_warning
)

# Bind activity refresh
root.bind_all("<Any-KeyPress>", lambda e: security.refresh_session())
root.bind_all("<Any-ButtonPress>", lambda e: security.refresh_session())
```

### Issue: Encrypted Data Cannot Be Decrypted

**Error**: `InvalidToken: Invalid token`

**Solution**:
1. Ensure same encryption key is used
2. Check data wasn't corrupted in storage
3. Verify base64 encoding/decoding

```python
# Store encryption key securely
encryption = DataEncryption()
key = encryption.get_key()
# Save key to secure location

# Later, reuse same key
encryption = DataEncryption(key=key)
```

### Issue: File Upload Validation Fails

**Error**: `ValueError: Invalid file type or size`

**Solution**:
1. Check file size limits (5MB for images, 10MB for documents)
2. Verify file extension is in allowed list
3. Ensure MIME type matches extension

```python
# Check allowed extensions
from utils.security import InputSanitizer

sanitizer = InputSanitizer()
print("Allowed image extensions:", sanitizer.ALLOWED_IMAGE_EXTENSIONS)
print("Allowed document extensions:", sanitizer.ALLOWED_DOCUMENT_EXTENSIONS)

# Adjust limits if needed (not recommended for production)
sanitizer.MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
```

---

## Support

For issues or questions:
1. Check this documentation
2. Review test cases in `test_security.py`
3. See examples in code comments
4. Contact the development team

---

## Version History

### v1.7.0 (Current)
- Initial release of Security System
- Data encryption with Fernet
- Rate limiting with sliding window
- Session timeout with callbacks
- Input sanitization (XSS, SQL injection)
- Secure password handling
- Token management with auto-refresh
- CSRF protection
- Comprehensive test suite

---

## License

Part of Campus Event Management System
