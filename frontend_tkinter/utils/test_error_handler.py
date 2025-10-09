#!/usr/bin/env python3
"""
Error Handler Test Script

Quick test to verify error handler is working correctly.
Run this to test basic functionality before full integration.

Usage:
    python3 test_error_handler.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.error_handler import (
    ErrorHandler,
    get_error_handler,
    setup_error_handling,
    require_login,
    require_role,
    handle_errors,
    ValidationError,
    AuthenticationError,
    AuthorizationError
)
from utils.session_manager import SessionManager
import requests


def test_singleton():
    """Test that ErrorHandler is a singleton"""
    print("\n🧪 Test 1: Singleton Pattern")
    handler1 = get_error_handler()
    handler2 = ErrorHandler()
    handler3 = get_error_handler()
    
    assert handler1 is handler2, "❌ FAIL: Handlers are not the same instance"
    assert handler2 is handler3, "❌ FAIL: Handlers are not the same instance"
    print("✅ PASS: ErrorHandler is a singleton")


def test_logging():
    """Test error logging"""
    print("\n🧪 Test 2: Error Logging")
    handler = get_error_handler()
    
    # Test logging
    try:
        result = 10 / 0
    except Exception as error:
        handler.log_error(error, context="Division test")
    
    # Check log file exists
    log_path = handler.get_log_file_path()
    if os.path.exists(log_path):
        print(f"✅ PASS: Log file created at {log_path}")
    else:
        print(f"❌ FAIL: Log file not created")
    
    # Check log content
    with open(log_path, 'r') as f:
        content = f.read()
        if "ZeroDivisionError" in content and "Division test" in content:
            print("✅ PASS: Error logged with context")
        else:
            print("❌ FAIL: Error not properly logged")


def test_custom_exceptions():
    """Test custom exception types"""
    print("\n🧪 Test 3: Custom Exceptions")
    
    # ValidationError
    try:
        raise ValidationError("email", "Invalid format")
    except ValidationError as e:
        assert e.field == "email", "❌ FAIL: ValidationError field incorrect"
        assert e.message == "Invalid format", "❌ FAIL: ValidationError message incorrect"
        print("✅ PASS: ValidationError works correctly")
    
    # AuthenticationError
    try:
        raise AuthenticationError("Not logged in")
    except AuthenticationError as e:
        assert str(e) == "Not logged in", "❌ FAIL: AuthenticationError message incorrect"
        print("✅ PASS: AuthenticationError works correctly")
    
    # AuthorizationError
    try:
        raise AuthorizationError(required_role="ADMIN", user_role="STUDENT")
    except AuthorizationError as e:
        assert e.required_role == "ADMIN", "❌ FAIL: AuthorizationError required_role incorrect"
        assert e.user_role == "STUDENT", "❌ FAIL: AuthorizationError user_role incorrect"
        print("✅ PASS: AuthorizationError works correctly")


def test_require_login_decorator():
    """Test @require_login decorator"""
    print("\n🧪 Test 4: @require_login Decorator")
    
    class TestClass:
        @require_login
        def protected_method(self):
            return "Success"
    
    test_obj = TestClass()
    session = SessionManager()
    handler = get_error_handler()
    
    # Disable GUI callbacks for testing
    handler.set_toast_callback(lambda msg, type: None)
    handler.set_logout_callback(lambda: None)
    handler.set_login_redirect_callback(lambda: None)
    
    # Test without login
    try:
        test_obj.protected_method()
        print("❌ FAIL: Method executed without login")
    except AuthenticationError:
        print("✅ PASS: @require_login blocked access when not logged in")
    
    # Test with login
    session.store_user(1, "test_user", "STUDENT", "test_token")
    try:
        result = test_obj.protected_method()
        if result == "Success":
            print("✅ PASS: @require_login allowed access when logged in")
        else:
            print("❌ FAIL: Method returned unexpected value")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {e}")
    
    # Cleanup
    session.clear_session()


def test_require_role_decorator():
    """Test @require_role decorator"""
    print("\n🧪 Test 5: @require_role Decorator")
    
    class TestClass:
        @require_role('ADMIN')
        def admin_method(self):
            return "Admin Success"
        
        @require_role('ADMIN', 'ORGANIZER')
        def multi_role_method(self):
            return "Multi Role Success"
    
    test_obj = TestClass()
    session = SessionManager()
    handler = get_error_handler()
    
    # Disable GUI callbacks for testing
    handler.set_toast_callback(lambda msg, type: None)
    
    # Test STUDENT trying ADMIN method
    session.store_user(1, "student", "STUDENT", "token1")
    try:
        test_obj.admin_method()
        print("❌ FAIL: STUDENT accessed ADMIN method")
    except AuthorizationError:
        print("✅ PASS: @require_role('ADMIN') blocked STUDENT")
    
    # Test ADMIN accessing ADMIN method
    session.store_user(2, "admin", "ADMIN", "token2")
    try:
        result = test_obj.admin_method()
        if result == "Admin Success":
            print("✅ PASS: @require_role('ADMIN') allowed ADMIN")
        else:
            print("❌ FAIL: Unexpected return value")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {e}")
    
    # Test ORGANIZER accessing multi-role method
    session.store_user(3, "organizer", "ORGANIZER", "token3")
    try:
        result = test_obj.multi_role_method()
        if result == "Multi Role Success":
            print("✅ PASS: @require_role('ADMIN', 'ORGANIZER') allowed ORGANIZER")
        else:
            print("❌ FAIL: Unexpected return value")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {e}")
    
    # Cleanup
    session.clear_session()


def test_handle_errors_decorator():
    """Test @handle_errors decorator"""
    print("\n🧪 Test 6: @handle_errors Decorator")
    
    handler = get_error_handler()
    # Disable GUI callbacks for testing
    handler.set_toast_callback(lambda msg, type: None)
    
    # Test with return_on_error
    @handle_errors(context="Test operation", return_on_error=[])
    def failing_function():
        raise ValueError("Test error")
    
    result = failing_function()
    if result == []:
        print("✅ PASS: @handle_errors returned default value on error")
    else:
        print(f"❌ FAIL: Expected [], got {result}")
    
    # Test successful execution
    @handle_errors(context="Success operation", return_on_error=None)
    def success_function():
        return "Success"
    
    result = success_function()
    if result == "Success":
        print("✅ PASS: @handle_errors allowed successful execution")
    else:
        print(f"❌ FAIL: Expected 'Success', got {result}")


def test_api_error_parsing():
    """Test API error message parsing"""
    print("\n🧪 Test 7: API Error Parsing")
    handler = get_error_handler()
    
    # Mock callback to capture messages
    messages = []
    def mock_toast(message, toast_type):
        messages.append((message, toast_type))
    
    handler.set_toast_callback(mock_toast)
    
    # Test 404 error
    error = requests.HTTPError("HTTP error: 404 - Not found")
    handler.handle_api_error(error, "Test context")
    
    if messages and "not found" in messages[-1][0].lower():
        print("✅ PASS: API error parsed 404 correctly")
    else:
        print(f"❌ FAIL: Expected 'not found' message, got: {messages}")
    
    messages.clear()
    
    # Test connection error
    error = requests.ConnectionError("Failed to connect")
    handler.handle_api_error(error, "Test context")
    
    if messages and "network" in messages[-1][0].lower():
        print("✅ PASS: Connection error handled correctly")
    else:
        print(f"❌ FAIL: Expected network error message, got: {messages}")


def test_setup_with_callbacks():
    """Test setup_error_handling function"""
    print("\n🧪 Test 8: Setup with Callbacks")
    
    toast_called = []
    logout_called = []
    redirect_called = []
    
    def mock_toast(msg, type):
        toast_called.append(True)
    
    def mock_logout():
        logout_called.append(True)
    
    def mock_redirect():
        redirect_called.append(True)
    
    # Setup
    handler = setup_error_handling(
        toast_callback=mock_toast,
        logout_callback=mock_logout,
        login_redirect_callback=mock_redirect
    )
    
    # Test toast callback
    handler._show_toast("Test", "info")
    if toast_called:
        print("✅ PASS: Toast callback registered and working")
    else:
        print("❌ FAIL: Toast callback not working")
    
    # Test session expired (should call logout and redirect)
    handler.handle_session_expired()
    if logout_called and redirect_called:
        print("✅ PASS: Logout and redirect callbacks working")
    else:
        print("❌ FAIL: Logout or redirect callback not working")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("ERROR HANDLER TEST SUITE")
    print("="*60)
    
    try:
        test_singleton()
        test_logging()
        test_custom_exceptions()
        test_require_login_decorator()
        test_require_role_decorator()
        test_handle_errors_decorator()
        test_api_error_parsing()
        test_setup_with_callbacks()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)
        print("\nCheck logs/error.log for logged errors")
        print("Run 'python3 error_handler_examples.py' for interactive demo")
        
    except Exception as e:
        print(f"\n❌ TEST SUITE FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_all_tests()
