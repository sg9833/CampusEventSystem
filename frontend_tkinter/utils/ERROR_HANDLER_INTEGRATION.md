# Error Handler - Integration Checklist

Use this checklist to integrate the Error Handler system into your Campus Event System.

## ✅ Phase 1: Initial Setup (Required)

### Step 1: Update Main Application

- [ ] Open `main.py`
- [ ] Import error handler:
  ```python
  from utils.error_handler import setup_error_handling
  ```
- [ ] Add `setup_error_handler()` method to main app class
- [ ] Call `setup_error_handler()` in `__init__` BEFORE other setup
- [ ] Implement toast callback using Toast widget
- [ ] Implement logout callback using SessionManager
- [ ] Implement login redirect callback

**Example:**
```python
def setup_error_handler(self):
    from components.custom_widgets import Toast
    from utils.session_manager import SessionManager
    
    def show_toast(message, toast_type):
        Toast(self, message, toast_type).show()
    
    def logout():
        SessionManager().clear_session()
        self.clear_user_data()
    
    def redirect_to_login():
        self.show_page('login')
    
    self.error_handler = setup_error_handling(
        toast_callback=show_toast,
        logout_callback=logout,
        login_redirect_callback=redirect_to_login
    )
```

### Step 2: Test Basic Error Handling

- [ ] Run application: `python3 main.py`
- [ ] Verify no errors on startup
- [ ] Check that `logs/error.log` is created
- [ ] Test toast notifications work
- [ ] Test logout functionality
- [ ] Test login redirect

---

## ✅ Phase 2: API Integration (High Priority)

### Step 3: Update API Client

- [ ] Open `utils/api_client.py`
- [ ] Import error handler:
  ```python
  from utils.error_handler import get_error_handler
  ```
- [ ] Add error handler to `__init__`:
  ```python
  self.error_handler = get_error_handler()
  ```
- [ ] Update `get()`, `post()`, `put()`, `delete()` methods
- [ ] Replace existing error handling with `handle_api_error()`
- [ ] Add context to each error

**Example:**
```python
def get(self, endpoint, headers=None):
    url = f"{self.base_url}/{endpoint.lstrip('/')}"
    try:
        response = self.session.get(url, headers=self._get_headers(headers), timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    except Exception as error:
        self.error_handler.handle_api_error(error, f"GET {endpoint}")
        raise  # Re-raise for @handle_errors decorator
```

### Step 4: Add @handle_errors to Service Methods

- [ ] Identify all API service classes
- [ ] Import decorator:
  ```python
  from utils.error_handler import handle_errors
  ```
- [ ] Add `@handle_errors` to methods that call API
- [ ] Set appropriate `return_on_error` values
- [ ] Add context descriptions

**Example:**
```python
@handle_errors(context="Loading events", return_on_error=[])
def get_events(self):
    return api_client.get('/events')
```

---

## ✅ Phase 3: Form Validation (Medium Priority)

### Step 5: Update Login Page

- [ ] Open `pages/login_page.py`
- [ ] Import error handler:
  ```python
  from utils.error_handler import get_error_handler
  ```
- [ ] Add to `__init__`:
  ```python
  self.error_handler = get_error_handler()
  ```
- [ ] Update `validate_credentials()` method
- [ ] Replace existing error messages with `handle_validation_error()`
- [ ] Pass widget reference for highlighting

**Example:**
```python
def validate_credentials(self):
    username = self.username_entry.get()
    if not username:
        self.error_handler.handle_validation_error(
            "Username",
            "Username is required",
            self.username_entry
        )
        return False
    
    password = self.password_entry.get()
    if not password:
        self.error_handler.handle_validation_error(
            "Password",
            "Password is required",
            self.password_entry
        )
        return False
    
    return True
```

### Step 6: Update Register Page

- [ ] Open `pages/register_page.py`
- [ ] Import error handler and validators
- [ ] Add error handler to `__init__`
- [ ] Update all validation to use `handle_validation_error()`
- [ ] Use validators from `utils/validators.py`

### Step 7: Update Event Form Pages

- [ ] Identify all form pages (create event, edit event, etc.)
- [ ] Add error handler to each
- [ ] Update validation methods
- [ ] Highlight invalid fields
- [ ] Use appropriate validators

---

## ✅ Phase 4: Access Control (High Priority)

### Step 8: Protect Admin Pages

- [ ] List all admin-only pages
- [ ] Import decorator:
  ```python
  from utils.error_handler import require_role
  ```
- [ ] Add `@require_role('ADMIN')` to `__init__` method
- [ ] Test that non-admin users cannot access

**Example:**
```python
class AdminPanel:
    @require_role('ADMIN')
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
```

### Step 9: Protect Organizer Pages

- [ ] List all organizer pages
- [ ] Add `@require_role('ADMIN', 'ORGANIZER')` decorator
- [ ] Test with different user roles

### Step 10: Protect Student Pages

- [ ] List all pages requiring login
- [ ] Import decorator:
  ```python
  from utils.error_handler import require_login
  ```
- [ ] Add `@require_login` to `__init__` method
- [ ] Test that logged-out users are redirected

---

## ✅ Phase 5: Replace Existing Error Handling (Medium Priority)

### Step 11: Replace try-except Blocks

- [ ] Search for `try:` in codebase
- [ ] Identify blocks that can use `@handle_errors`
- [ ] Replace with decorator where appropriate
- [ ] Keep try-except for specific error handling

**Before:**
```python
def load_events(self):
    try:
        return api_client.get('/events')
    except Exception as e:
        print(f"Error: {e}")
        return []
```

**After:**
```python
@handle_errors(context="Loading events", return_on_error=[])
def load_events(self):
    return api_client.get('/events')
```

### Step 12: Replace print() Statements

- [ ] Search for `print("Error` in codebase
- [ ] Replace with `error_handler.log_error()`
- [ ] Add context for each error

### Step 13: Replace messagebox Errors

- [ ] Search for `messagebox.showerror` in codebase
- [ ] Replace with appropriate error handler method
- [ ] Use Toast for non-blocking notifications

---

## ✅ Phase 6: Testing (Critical)

### Step 14: Test Error Scenarios

- [ ] **Test API Errors:**
  - [ ] Stop backend server
  - [ ] Try to load events → Should show network error
  - [ ] Start backend
  - [ ] Try invalid API call → Should show appropriate error

- [ ] **Test Validation:**
  - [ ] Submit empty form → Should highlight fields
  - [ ] Enter invalid email → Should highlight email field
  - [ ] Enter short password → Should highlight password field

- [ ] **Test Authentication:**
  - [ ] Logout
  - [ ] Try to access protected page → Should redirect to login
  - [ ] Login as STUDENT
  - [ ] Try to access admin page → Should show access denied

- [ ] **Test Authorization:**
  - [ ] Login as STUDENT
  - [ ] Try to create event (if organizer-only) → Should show error
  - [ ] Login as ORGANIZER
  - [ ] Try to delete user (if admin-only) → Should show error
  - [ ] Login as ADMIN
  - [ ] Try all actions → Should work

### Step 15: Check Error Logs

- [ ] Open `logs/error.log`
- [ ] Verify errors are logged with:
  - [ ] Timestamp
  - [ ] Error type
  - [ ] Error message
  - [ ] Context
  - [ ] Traceback
- [ ] Verify log format is readable

### Step 16: Test Toast Notifications

- [ ] Trigger various errors
- [ ] Verify toast appears with correct type:
  - [ ] Error (red) for errors
  - [ ] Warning (yellow) for warnings
  - [ ] Info (blue) for info
- [ ] Verify toast auto-dismisses
- [ ] Verify multiple toasts work

---

## ✅ Phase 7: Documentation (Optional)

### Step 17: Update Code Comments

- [ ] Add docstrings to new error handling code
- [ ] Document expected error scenarios
- [ ] Add examples in comments

### Step 18: Create Developer Guide

- [ ] Document error handling patterns
- [ ] Add to project wiki/docs
- [ ] Include common scenarios
- [ ] Add troubleshooting section

---

## 🎯 Priority Summary

### Must Do (Week 1)
1. ✅ Phase 1: Initial Setup
2. ✅ Phase 2: API Integration
3. ✅ Phase 4: Access Control
4. ✅ Phase 6: Testing (basic)

### Should Do (Week 2)
5. ✅ Phase 3: Form Validation
6. ✅ Phase 5: Replace Existing Error Handling
7. ✅ Phase 6: Testing (comprehensive)

### Nice to Have (Week 3+)
8. ✅ Phase 7: Documentation

---

## 📝 Testing Checklist

### Functional Tests

- [ ] Login with valid credentials → Success
- [ ] Login with invalid credentials → Error toast
- [ ] Login without credentials → Validation errors
- [ ] Access dashboard without login → Redirect to login
- [ ] Access admin page as student → Access denied
- [ ] Access admin page as admin → Success
- [ ] Load events with backend running → Success
- [ ] Load events with backend stopped → Network error
- [ ] Submit valid form → Success
- [ ] Submit invalid form → Validation errors
- [ ] API timeout → Timeout error
- [ ] API 404 → Not found error
- [ ] API 500 → Server error

### UI Tests

- [ ] Validation errors highlight widgets
- [ ] Toast notifications appear
- [ ] Toast notifications auto-dismiss
- [ ] Multiple toasts don't overlap
- [ ] Error messages are user-friendly
- [ ] No technical error messages shown
- [ ] Session expired message appears
- [ ] Redirect to login works

### Log Tests

- [ ] Errors logged to file
- [ ] Logs include context
- [ ] Logs include traceback
- [ ] Logs include timestamp
- [ ] Log file doesn't grow too large
- [ ] Log clearing works

---

## 🐛 Common Issues & Solutions

### Issue: "ErrorHandler has no attribute '_logger'"
**Solution:** Logger is initialized in `_initialize()`. Make sure you're using `get_error_handler()` not creating new instance.

### Issue: Widget highlighting doesn't work
**Solution:** Only works with Entry/Text widgets. Check widget type before passing.

### Issue: Toast callback fails
**Solution:** Make sure Toast class is imported and available. Add try-except in callback.

### Issue: Decorators not working
**Solution:** Apply decorators in correct order (inside-out). Check imports.

### Issue: Session not clearing on 401
**Solution:** Verify logout callback is registered in setup_error_handling().

---

## 📚 Resources

- **Full Documentation:** `utils/ERROR_HANDLER_README.md`
- **Quick Reference:** `utils/ERROR_HANDLER_QUICK_REFERENCE.md`
- **Examples:** `utils/error_handler_examples.py`
- **Summary:** `utils/ERROR_HANDLER_SUMMARY.md`

---

**Version:** 1.6.0  
**Last Updated:** October 9, 2025
