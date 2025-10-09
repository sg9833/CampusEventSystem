"""
Error Handler Module for Campus Event System

Provides centralized error handling, logging, and user-friendly error messages.
Includes decorators for authentication and authorization checks.

Author: Campus Event System Team
Version: 1.6.0
Date: October 9, 2025
"""

import logging
import traceback
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable, Any, Dict
from functools import wraps
from datetime import datetime
import requests
import os


# ============================================================================
#  CUSTOM EXCEPTIONS
# ============================================================================

class ValidationError(Exception):
    """Raised when form validation fails"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class AuthenticationError(Exception):
    """Raised when user is not authenticated"""
    pass


class AuthorizationError(Exception):
    """Raised when user lacks required permissions"""
    def __init__(self, required_role: str, user_role: Optional[str] = None):
        self.required_role = required_role
        self.user_role = user_role
        message = f"Access denied. Required role: {required_role}"
        if user_role:
            message += f", Your role: {user_role}"
        super().__init__(message)


class SessionExpiredError(Exception):
    """Raised when user session has expired"""
    pass


# ============================================================================
#  ERROR HANDLER CLASS
# ============================================================================

class ErrorHandler:
    """
    Centralized error handling system for the Campus Event System.
    
    Provides methods to handle different types of errors:
    - API/HTTP errors
    - Validation errors
    - Network errors
    - Session expiration
    - Generic exceptions
    
    Features:
    - User-friendly error messages
    - Error logging to file
    - Context-aware error handling
    - Integration with Toast notifications
    """
    
    _instance = None
    _logger = None
    _log_file = None
    _toast_callback = None
    _logout_callback = None
    _login_redirect_callback = None
    
    def __new__(cls):
        """Singleton pattern to ensure single instance"""
        if cls._instance is None:
            cls._instance = super(ErrorHandler, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the error handler"""
        # Setup logging
        self._setup_logging()
        
        # Callbacks (to be set by application)
        self._toast_callback = None
        self._logout_callback = None
        self._login_redirect_callback = None
    
    def _setup_logging(self):
        """Setup error logging to file"""
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup log file path
        self._log_file = os.path.join(log_dir, 'error.log')
        
        # Configure logger
        self._logger = logging.getLogger('CampusEventSystem')
        self._logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self._logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self._log_file, encoding='utf-8')
        file_handler.setLevel(logging.ERROR)
        
        # Console handler (for development)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    # ========================================================================
    #  CALLBACK REGISTRATION
    # ========================================================================
    
    def set_toast_callback(self, callback: Callable[[str, str], None]):
        """
        Set callback for showing toast notifications
        
        Args:
            callback: Function(message: str, type: str) -> None
                     type can be 'error', 'warning', 'info', 'success'
        """
        self._toast_callback = callback
    
    def set_logout_callback(self, callback: Callable[[], None]):
        """
        Set callback for logging out user
        
        Args:
            callback: Function() -> None
        """
        self._logout_callback = callback
    
    def set_login_redirect_callback(self, callback: Callable[[], None]):
        """
        Set callback for redirecting to login page
        
        Args:
            callback: Function() -> None
        """
        self._login_redirect_callback = callback
    
    # ========================================================================
    #  TOAST NOTIFICATION HELPER
    # ========================================================================
    
    def _show_toast(self, message: str, toast_type: str = 'error'):
        """Show toast notification if callback is set"""
        if self._toast_callback:
            try:
                self._toast_callback(message, toast_type)
            except Exception as e:
                # Fallback to messagebox if toast fails
                self._logger.warning(f"Toast callback failed: {e}")
                messagebox.showerror("Error", message)
        else:
            # Fallback to messagebox
            if toast_type == 'error':
                messagebox.showerror("Error", message)
            elif toast_type == 'warning':
                messagebox.showwarning("Warning", message)
            elif toast_type == 'info':
                messagebox.showinfo("Information", message)
            else:
                messagebox.showinfo("Success", message)
    
    # ========================================================================
    #  ERROR HANDLING METHODS
    # ========================================================================
    
    def handle_api_error(self, error: Exception, context: str = "") -> None:
        """
        Handle API/HTTP errors with user-friendly messages
        
        Args:
            error: The exception that occurred
            context: Additional context about where error occurred
        """
        user_message = "An error occurred while communicating with the server."
        
        try:
            if isinstance(error, requests.HTTPError):
                # Parse HTTP error
                status_code = None
                error_text = str(error)
                
                # Extract status code
                if hasattr(error, 'response') and error.response is not None:
                    status_code = error.response.status_code
                    try:
                        error_data = error.response.json()
                        if isinstance(error_data, dict):
                            user_message = error_data.get('message', error_data.get('error', user_message))
                    except:
                        user_message = error.response.text or user_message
                else:
                    # Try to extract from error message
                    import re
                    match = re.search(r'(\d{3})', error_text)
                    if match:
                        status_code = int(match.group(1))
                
                # Map status codes to user-friendly messages
                if status_code == 400:
                    user_message = "Invalid request. Please check your input and try again."
                elif status_code == 401:
                    user_message = "Authentication failed. Please log in again."
                    self.handle_session_expired()
                    return
                elif status_code == 403:
                    user_message = "Access denied. You don't have permission to perform this action."
                elif status_code == 404:
                    user_message = "The requested resource was not found."
                elif status_code == 409:
                    user_message = "A conflict occurred. The resource may already exist."
                elif status_code == 422:
                    user_message = "Validation failed. Please check your input."
                elif status_code == 500:
                    user_message = "Server error occurred. Please try again later."
                elif status_code == 502:
                    user_message = "Bad gateway. The server is temporarily unavailable."
                elif status_code == 503:
                    user_message = "Service unavailable. Please try again later."
                elif status_code == 504:
                    user_message = "Gateway timeout. The request took too long."
                
                # Log the error
                self.log_error(error, f"HTTP {status_code} - {context}")
                
            elif isinstance(error, requests.ConnectionError):
                # Network connection error
                self.handle_network_error()
                return
                
            elif isinstance(error, requests.Timeout):
                # Timeout error
                user_message = "Request timed out. Please check your connection and try again."
                self.log_error(error, f"Timeout - {context}")
                
            elif isinstance(error, ValueError):
                # JSON decode error or invalid response
                user_message = "Received invalid response from server. Please try again."
                self.log_error(error, f"Invalid response - {context}")
                
            else:
                # Generic error
                user_message = f"An unexpected error occurred: {str(error)}"
                self.log_error(error, context)
            
            # Show error to user
            self._show_toast(user_message, 'error')
            
        except Exception as e:
            # Error in error handler - log and show generic message
            self._logger.error(f"Error in handle_api_error: {e}")
            self._show_toast("An unexpected error occurred. Please try again.", 'error')
    
    def handle_validation_error(
        self, 
        field: str, 
        message: str, 
        widget: Optional[tk.Widget] = None
    ) -> None:
        """
        Handle form validation errors
        
        Args:
            field: Name of the field that failed validation
            message: Error message to display
            widget: Optional widget to highlight (Entry, Text, etc.)
        """
        # Format error message
        error_msg = f"{field}: {message}"
        
        # Log validation error
        self._logger.warning(f"Validation error - {error_msg}")
        
        # Highlight widget if provided
        if widget:
            try:
                # Save original style
                original_bg = widget.cget('background')
                original_fg = widget.cget('foreground')
                
                # Highlight with error color
                widget.config(
                    background='#FFEBEE',  # Light red
                    foreground='#C62828'    # Dark red
                )
                
                # Set focus to widget
                widget.focus_set()
                
                # Restore original style after 3 seconds
                def restore_style():
                    try:
                        widget.config(background=original_bg, foreground=original_fg)
                    except:
                        pass
                
                widget.after(3000, restore_style)
                
            except Exception as e:
                self._logger.warning(f"Failed to highlight widget: {e}")
        
        # Show error message
        self._show_toast(message, 'error')
    
    def handle_network_error(self) -> None:
        """Handle network connection errors"""
        message = (
            "Cannot connect to the server.\n\n"
            "Please check:\n"
            "• Your internet connection\n"
            "• The server is running\n"
            "• Firewall settings"
        )
        
        self._logger.error("Network connection error")
        self._show_toast("Network Error: Please check your internet connection.", 'error')
        
        # Also show detailed message box (only if toast callback not set - avoid GUI in tests)
        if not self._toast_callback:
            messagebox.showerror("Network Error", message)
    
    def handle_session_expired(self) -> None:
        """Handle expired user session"""
        message = "Your session has expired. Please log in again."
        
        self._logger.warning("Session expired")
        self._show_toast(message, 'warning')
        
        # Clear session and redirect to login
        if self._logout_callback:
            try:
                self._logout_callback()
            except Exception as e:
                self._logger.error(f"Logout callback failed: {e}")
        
        if self._login_redirect_callback:
            try:
                self._login_redirect_callback()
            except Exception as e:
                self._logger.error(f"Login redirect callback failed: {e}")
        else:
            # Fallback: show message
            messagebox.showinfo("Session Expired", message)
    
    def handle_authorization_error(
        self, 
        required_role: str, 
        user_role: Optional[str] = None
    ) -> None:
        """
        Handle authorization (permission) errors
        
        Args:
            required_role: Role required for the action
            user_role: Current user's role
        """
        message = f"Access denied. This action requires {required_role} role."
        if user_role:
            message += f" Your current role is {user_role}."
        
        self._logger.warning(f"Authorization error - Required: {required_role}, User: {user_role}")
        self._show_toast(message, 'error')
    
    def log_error(self, error: Exception, context: str = "") -> None:
        """
        Log error to file with context and traceback
        
        Args:
            error: The exception to log
            context: Additional context about the error
        """
        try:
            # Format error message
            error_type = type(error).__name__
            error_msg = str(error)
            
            # Get traceback
            tb = traceback.format_exc()
            
            # Build log message
            log_message = f"\n{'='*80}\n"
            log_message += f"Error Type: {error_type}\n"
            log_message += f"Error Message: {error_msg}\n"
            if context:
                log_message += f"Context: {context}\n"
            log_message += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            log_message += f"Traceback:\n{tb}"
            log_message += f"{'='*80}\n"
            
            # Log to file
            self._logger.error(log_message)
            
        except Exception as e:
            # If logging fails, at least print to console
            print(f"Failed to log error: {e}")
            print(f"Original error: {error}")
    
    def handle_exception(
        self, 
        error: Exception, 
        context: str = "",
        show_details: bool = False
    ) -> None:
        """
        Generic exception handler - routes to appropriate handler
        
        Args:
            error: The exception to handle
            context: Additional context
            show_details: Whether to show technical details to user
        """
        # Route to specific handlers
        if isinstance(error, ValidationError):
            self.handle_validation_error(error.field, error.message)
            
        elif isinstance(error, AuthenticationError):
            self.handle_session_expired()
            
        elif isinstance(error, AuthorizationError):
            self.handle_authorization_error(error.required_role, error.user_role)
            
        elif isinstance(error, SessionExpiredError):
            self.handle_session_expired()
            
        elif isinstance(error, (requests.HTTPError, requests.ConnectionError, 
                               requests.Timeout, ValueError)):
            self.handle_api_error(error, context)
            
        else:
            # Generic error
            self.log_error(error, context)
            
            user_message = "An unexpected error occurred."
            if show_details:
                user_message += f"\n\nDetails: {str(error)}"
            
            self._show_toast(user_message, 'error')
    
    # ========================================================================
    #  UTILITY METHODS
    # ========================================================================
    
    def get_log_file_path(self) -> str:
        """Get the path to the error log file"""
        return self._log_file
    
    def clear_log_file(self) -> None:
        """Clear the error log file"""
        try:
            with open(self._log_file, 'w') as f:
                f.write(f"Log cleared at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self._logger.info("Error log cleared")
        except Exception as e:
            self._logger.error(f"Failed to clear log file: {e}")


# ============================================================================
#  DECORATORS
# ============================================================================

def require_login(func: Callable) -> Callable:
    """
    Decorator to check if user is logged in before executing function.
    
    Usage:
        @require_login
        def view_dashboard(self):
            # This only executes if user is logged in
            pass
    
    Raises:
        AuthenticationError: If user is not logged in
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        from utils.session_manager import SessionManager
        
        session = SessionManager()
        if not session.is_logged_in():
            error_handler = ErrorHandler()
            error_handler.handle_session_expired()
            raise AuthenticationError("User must be logged in")
        
        return func(*args, **kwargs)
    
    return wrapper


def require_role(*allowed_roles: str) -> Callable:
    """
    Decorator to check if user has required role before executing function.
    
    Usage:
        @require_role('ADMIN')
        def delete_user(self, user_id):
            # Only ADMIN can execute this
            pass
        
        @require_role('ADMIN', 'ORGANIZER')
        def create_event(self):
            # ADMIN or ORGANIZER can execute this
            pass
    
    Args:
        *allowed_roles: One or more role names that are allowed
    
    Raises:
        AuthenticationError: If user is not logged in
        AuthorizationError: If user doesn't have required role
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            from utils.session_manager import SessionManager
            
            session = SessionManager()
            
            # Check if logged in
            if not session.is_logged_in():
                error_handler = ErrorHandler()
                error_handler.handle_session_expired()
                raise AuthenticationError("User must be logged in")
            
            # Check role
            user_role = session.get_role()
            if user_role not in allowed_roles:
                error_handler = ErrorHandler()
                error_handler.handle_authorization_error(
                    required_role='/'.join(allowed_roles),
                    user_role=user_role
                )
                raise AuthorizationError(
                    required_role='/'.join(allowed_roles),
                    user_role=user_role
                )
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def handle_errors(
    context: str = "",
    show_toast: bool = True,
    show_details: bool = False,
    return_on_error: Any = None
) -> Callable:
    """
    Decorator to wrap function with error handling.
    
    Usage:
        @handle_errors(context="Loading events", show_toast=True)
        def load_events(self):
            # Any error here will be caught and handled gracefully
            response = api_client.get('/events')
            return response
        
        @handle_errors(context="Deleting user", return_on_error=False)
        def delete_user(self, user_id):
            # Returns False if error occurs
            api_client.delete(f'/users/{user_id}')
            return True
    
    Args:
        context: Context description for error logging
        show_toast: Whether to show toast notification on error
        show_details: Whether to show technical details to user
        return_on_error: Value to return if error occurs (default: None)
    
    Returns:
        Decorated function that handles errors gracefully
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                error_handler = ErrorHandler()
                
                # Build context message
                full_context = context or f"{func.__name__}"
                
                # Handle the error
                if show_toast:
                    error_handler.handle_exception(error, full_context, show_details)
                else:
                    error_handler.log_error(error, full_context)
                
                # Return default value on error
                return return_on_error
        
        return wrapper
    
    return decorator


# ============================================================================
#  CONVENIENCE FUNCTIONS
# ============================================================================

def get_error_handler() -> ErrorHandler:
    """Get the singleton ErrorHandler instance"""
    return ErrorHandler()


def setup_error_handling(
    toast_callback: Optional[Callable[[str, str], None]] = None,
    logout_callback: Optional[Callable[[], None]] = None,
    login_redirect_callback: Optional[Callable[[], None]] = None
) -> ErrorHandler:
    """
    Setup error handling system with callbacks
    
    Args:
        toast_callback: Function to show toast notifications
        logout_callback: Function to logout user
        login_redirect_callback: Function to redirect to login
    
    Returns:
        ErrorHandler instance
    
    Example:
        from utils.error_handler import setup_error_handling
        from components.custom_widgets import Toast
        
        def show_toast(message, type):
            Toast(root, message, type).show()
        
        def logout():
            session.clear_session()
        
        def redirect_to_login():
            # Navigate to login page
            pass
        
        error_handler = setup_error_handling(
            toast_callback=show_toast,
            logout_callback=logout,
            login_redirect_callback=redirect_to_login
        )
    """
    handler = ErrorHandler()
    
    if toast_callback:
        handler.set_toast_callback(toast_callback)
    if logout_callback:
        handler.set_logout_callback(logout_callback)
    if login_redirect_callback:
        handler.set_login_redirect_callback(login_redirect_callback)
    
    return handler


# ============================================================================
#  MODULE EXPORTS
# ============================================================================

__all__ = [
    # Classes
    'ErrorHandler',
    'ValidationError',
    'AuthenticationError',
    'AuthorizationError',
    'SessionExpiredError',
    
    # Decorators
    'require_login',
    'require_role',
    'handle_errors',
    
    # Functions
    'get_error_handler',
    'setup_error_handling',
]
