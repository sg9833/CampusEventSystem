"""
Error Handler Examples - Campus Event System

This file demonstrates how to use the ErrorHandler class and decorators.

Author: Campus Event System Team
Version: 1.6.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.error_handler import (
    ErrorHandler,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    SessionExpiredError,
    require_login,
    require_role,
    handle_errors,
    get_error_handler,
    setup_error_handling
)
from utils.session_manager import SessionManager
import requests


# ============================================================================
#  EXAMPLE 1: BASIC ERROR HANDLING
# ============================================================================

def example_basic_error_handling():
    """Basic error handling with ErrorHandler"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Error Handling")
    print("="*80)
    
    handler = get_error_handler()
    
    # Handle API error
    print("\n1. Handling API Error:")
    try:
        raise requests.HTTPError("HTTP error: 404 - Resource not found")
    except Exception as e:
        handler.handle_api_error(e, context="Fetching user data")
    
    # Handle validation error
    print("\n2. Handling Validation Error:")
    handler.handle_validation_error("email", "Invalid email format")
    
    # Handle network error
    print("\n3. Handling Network Error:")
    handler.handle_network_error()
    
    # Log error
    print("\n4. Logging Error:")
    try:
        result = 10 / 0
    except Exception as e:
        handler.log_error(e, context="Division calculation")
    
    print(f"\nError log file: {handler.get_log_file_path()}")


# ============================================================================
#  EXAMPLE 2: USING DECORATORS
# ============================================================================

class UserService:
    """Example service class with decorated methods"""
    
    @require_login
    def view_profile(self):
        """Only logged-in users can view profile"""
        print("✓ Viewing profile (user is logged in)")
        return {"name": "John Doe", "email": "john@example.com"}
    
    @require_role('ADMIN')
    def delete_user(self, user_id):
        """Only ADMIN can delete users"""
        print(f"✓ Deleting user {user_id} (admin permission)")
        return True
    
    @require_role('ADMIN', 'ORGANIZER')
    def create_event(self, event_name):
        """ADMIN or ORGANIZER can create events"""
        print(f"✓ Creating event '{event_name}' (has permission)")
        return {"event_id": 123, "name": event_name}
    
    @handle_errors(context="Loading events from API", return_on_error=[])
    def load_events(self):
        """Load events with error handling"""
        print("✓ Loading events...")
        # Simulate API call
        # If this fails, returns [] instead of crashing
        return [
            {"id": 1, "title": "Tech Talk"},
            {"id": 2, "title": "Workshop"}
        ]
    
    @handle_errors(context="Saving event", return_on_error=False)
    def save_event(self, event_data):
        """Save event with error handling"""
        print(f"✓ Saving event: {event_data}")
        # If this fails, returns False
        return True


def example_decorators():
    """Demonstrate decorator usage"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Using Decorators")
    print("="*80)
    
    service = UserService()
    session = SessionManager()
    
    # Test 1: Without login
    print("\n1. Trying to access protected method without login:")
    try:
        service.view_profile()
    except AuthenticationError as e:
        print(f"✗ Caught: {e}")
    
    # Login as STUDENT
    print("\n2. Login as STUDENT:")
    session.store_user(user_id=1, username="student1", role="STUDENT", token="token123")
    print(f"✓ Logged in as {session.get_role()}")
    
    # Test 2: With login (STUDENT role)
    print("\n3. Accessing profile (should work):")
    result = service.view_profile()
    print(f"Result: {result}")
    
    # Test 3: Try ADMIN-only action as STUDENT
    print("\n4. Trying ADMIN action as STUDENT:")
    try:
        service.delete_user(user_id=5)
    except AuthorizationError as e:
        print(f"✗ Caught: {e}")
    
    # Login as ADMIN
    print("\n5. Login as ADMIN:")
    session.store_user(user_id=2, username="admin1", role="ADMIN", token="token456")
    print(f"✓ Logged in as {session.get_role()}")
    
    # Test 4: ADMIN action with ADMIN role
    print("\n6. Trying ADMIN action as ADMIN:")
    result = service.delete_user(user_id=5)
    print(f"Result: {result}")
    
    # Test 5: Using @handle_errors decorator
    print("\n7. Using @handle_errors decorator:")
    events = service.load_events()
    print(f"Loaded {len(events)} events")
    
    success = service.save_event({"title": "New Event"})
    print(f"Save result: {success}")
    
    # Cleanup
    session.clear_session()


# ============================================================================
#  EXAMPLE 3: ERROR TYPES
# ============================================================================

def example_error_types():
    """Demonstrate different error types"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Custom Error Types")
    print("="*80)
    
    handler = get_error_handler()
    
    # ValidationError
    print("\n1. ValidationError:")
    try:
        raise ValidationError("password", "Password must be at least 8 characters")
    except ValidationError as e:
        print(f"Field: {e.field}")
        print(f"Message: {e.message}")
        handler.handle_validation_error(e.field, e.message)
    
    # AuthenticationError
    print("\n2. AuthenticationError:")
    try:
        raise AuthenticationError("User must be logged in")
    except AuthenticationError as e:
        print(f"Error: {e}")
    
    # AuthorizationError
    print("\n3. AuthorizationError:")
    try:
        raise AuthorizationError(required_role="ADMIN", user_role="STUDENT")
    except AuthorizationError as e:
        print(f"Required: {e.required_role}")
        print(f"User role: {e.user_role}")
        handler.handle_authorization_error(e.required_role, e.user_role)
    
    # SessionExpiredError
    print("\n4. SessionExpiredError:")
    try:
        raise SessionExpiredError("Session has expired")
    except SessionExpiredError as e:
        print(f"Error: {e}")


# ============================================================================
#  EXAMPLE 4: API ERROR SCENARIOS
# ============================================================================

def example_api_errors():
    """Demonstrate handling different API error scenarios"""
    print("\n" + "="*80)
    print("EXAMPLE 4: API Error Scenarios")
    print("="*80)
    
    handler = get_error_handler()
    
    # 400 Bad Request
    print("\n1. HTTP 400 - Bad Request:")
    handler.handle_api_error(
        requests.HTTPError("HTTP error: 400 - Invalid input"),
        context="Creating event"
    )
    
    # 401 Unauthorized
    print("\n2. HTTP 401 - Unauthorized:")
    # Note: This will trigger session expiration
    
    # 403 Forbidden
    print("\n3. HTTP 403 - Forbidden:")
    handler.handle_api_error(
        requests.HTTPError("HTTP error: 403 - Access denied"),
        context="Deleting resource"
    )
    
    # 404 Not Found
    print("\n4. HTTP 404 - Not Found:")
    handler.handle_api_error(
        requests.HTTPError("HTTP error: 404 - Event not found"),
        context="Fetching event details"
    )
    
    # 500 Internal Server Error
    print("\n5. HTTP 500 - Server Error:")
    handler.handle_api_error(
        requests.HTTPError("HTTP error: 500 - Internal server error"),
        context="Processing booking"
    )
    
    # Connection Error
    print("\n6. Connection Error:")
    handler.handle_api_error(
        requests.ConnectionError("Failed to connect to server"),
        context="Fetching events"
    )
    
    # Timeout Error
    print("\n7. Timeout Error:")
    handler.handle_api_error(
        requests.Timeout("Request timed out after 10 seconds"),
        context="Loading resources"
    )


# ============================================================================
#  EXAMPLE 5: GUI INTEGRATION
# ============================================================================

class ErrorHandlerDemo(tk.Tk):
    """Demo application showing error handler integration with GUI"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Error Handler Demo")
        self.geometry("800x600")
        
        # Setup error handler with callbacks
        self.setup_error_handler()
        
        # Create UI
        self.create_widgets()
    
    def setup_error_handler(self):
        """Setup error handler with GUI callbacks"""
        
        # Toast callback
        def show_toast(message, toast_type):
            print(f"[TOAST {toast_type.upper()}] {message}")
            # In real app, show actual toast notification
        
        # Logout callback
        def logout():
            print("[LOGOUT] User logged out")
            session = SessionManager()
            session.clear_session()
        
        # Login redirect callback
        def redirect_to_login():
            print("[REDIRECT] Redirecting to login page")
            # In real app, navigate to login page
        
        # Setup error handler
        self.error_handler = setup_error_handling(
            toast_callback=show_toast,
            logout_callback=logout,
            login_redirect_callback=redirect_to_login
        )
    
    def create_widgets(self):
        """Create demo widgets"""
        
        # Main frame
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title = ttk.Label(
            main_frame,
            text="Error Handler Demo",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=(0, 20))
        
        # Notebook for examples
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Tab 1: API Errors
        api_frame = self._create_api_errors_tab()
        notebook.add(api_frame, text="API Errors")
        
        # Tab 2: Validation Errors
        validation_frame = self._create_validation_tab()
        notebook.add(validation_frame, text="Validation")
        
        # Tab 3: Authentication
        auth_frame = self._create_auth_tab()
        notebook.add(auth_frame, text="Authentication")
        
        # Tab 4: Decorators
        decorator_frame = self._create_decorators_tab()
        notebook.add(decorator_frame, text="Decorators")
    
    def _create_api_errors_tab(self):
        """Create API errors demo tab"""
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(
            frame,
            text="Simulate API Errors",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))
        
        # Buttons for different error codes
        errors = [
            ("400 - Bad Request", 400),
            ("401 - Unauthorized", 401),
            ("403 - Forbidden", 403),
            ("404 - Not Found", 404),
            ("500 - Server Error", 500),
            ("Connection Error", "connection"),
            ("Timeout Error", "timeout")
        ]
        
        for label, error_type in errors:
            btn = ttk.Button(
                frame,
                text=label,
                command=lambda e=error_type: self._simulate_api_error(e)
            )
            btn.pack(fill='x', pady=5)
        
        return frame
    
    def _create_validation_tab(self):
        """Create validation demo tab"""
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(
            frame,
            text="Form Validation Demo",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))
        
        # Email field
        ttk.Label(frame, text="Email:").pack(anchor='w')
        email_entry = ttk.Entry(frame, width=40)
        email_entry.pack(fill='x', pady=(0, 10))
        
        # Password field
        ttk.Label(frame, text="Password:").pack(anchor='w')
        password_entry = ttk.Entry(frame, width=40, show='*')
        password_entry.pack(fill='x', pady=(0, 10))
        
        # Validate button
        def validate_form():
            email = email_entry.get()
            password = password_entry.get()
            
            if not email:
                self.error_handler.handle_validation_error(
                    "Email",
                    "Email is required",
                    email_entry
                )
                return
            
            if '@' not in email:
                self.error_handler.handle_validation_error(
                    "Email",
                    "Invalid email format",
                    email_entry
                )
                return
            
            if len(password) < 8:
                self.error_handler.handle_validation_error(
                    "Password",
                    "Password must be at least 8 characters",
                    password_entry
                )
                return
            
            messagebox.showinfo("Success", "Validation passed!")
        
        ttk.Button(
            frame,
            text="Validate Form",
            command=validate_form
        ).pack(pady=10)
        
        return frame
    
    def _create_auth_tab(self):
        """Create authentication demo tab"""
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(
            frame,
            text="Authentication Demo",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))
        
        # Session info
        session = SessionManager()
        
        def update_session_info():
            info_label.config(
                text=f"Logged in: {session.is_logged_in()}\n"
                     f"Role: {session.get_role() or 'None'}"
            )
        
        info_label = ttk.Label(frame, text="", justify='left')
        info_label.pack(pady=10)
        update_session_info()
        
        # Login as STUDENT
        def login_student():
            session.store_user(1, "student1", "STUDENT", "token123")
            update_session_info()
        
        ttk.Button(frame, text="Login as STUDENT", command=login_student).pack(fill='x', pady=5)
        
        # Login as ADMIN
        def login_admin():
            session.store_user(2, "admin1", "ADMIN", "token456")
            update_session_info()
        
        ttk.Button(frame, text="Login as ADMIN", command=login_admin).pack(fill='x', pady=5)
        
        # Logout
        def logout():
            session.clear_session()
            update_session_info()
        
        ttk.Button(frame, text="Logout", command=logout).pack(fill='x', pady=5)
        
        # Test session expiration
        def test_expired():
            self.error_handler.handle_session_expired()
            update_session_info()
        
        ttk.Button(frame, text="Simulate Session Expired", command=test_expired).pack(fill='x', pady=20)
        
        return frame
    
    def _create_decorators_tab(self):
        """Create decorators demo tab"""
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(
            frame,
            text="Decorator Demo",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))
        
        service = UserService()
        
        # Test @require_login
        def test_require_login():
            try:
                result = service.view_profile()
                messagebox.showinfo("Success", f"Profile: {result}")
            except AuthenticationError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(frame, text="Test @require_login", command=test_require_login).pack(fill='x', pady=5)
        
        # Test @require_role
        def test_require_role():
            try:
                result = service.delete_user(5)
                messagebox.showinfo("Success", f"Deleted: {result}")
            except (AuthenticationError, AuthorizationError) as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(frame, text="Test @require_role('ADMIN')", command=test_require_role).pack(fill='x', pady=5)
        
        # Test @handle_errors
        def test_handle_errors():
            events = service.load_events()
            messagebox.showinfo("Success", f"Loaded {len(events)} events")
        
        ttk.Button(frame, text="Test @handle_errors", command=test_handle_errors).pack(fill='x', pady=5)
        
        return frame
    
    def _simulate_api_error(self, error_type):
        """Simulate different API errors"""
        if error_type == "connection":
            error = requests.ConnectionError("Failed to connect")
        elif error_type == "timeout":
            error = requests.Timeout("Request timed out")
        else:
            error = requests.HTTPError(f"HTTP error: {error_type}")
        
        self.error_handler.handle_api_error(error, "Demo API call")


# ============================================================================
#  MAIN EXECUTION
# ============================================================================

def main():
    """Run all examples"""
    
    print("\n" + "="*80)
    print("ERROR HANDLER EXAMPLES - CAMPUS EVENT SYSTEM")
    print("="*80)
    
    # Run console examples
    example_basic_error_handling()
    example_decorators()
    example_error_types()
    example_api_errors()
    
    print("\n" + "="*80)
    print("Starting GUI Demo...")
    print("="*80)
    
    # Run GUI demo
    app = ErrorHandlerDemo()
    app.mainloop()


if __name__ == '__main__':
    main()
