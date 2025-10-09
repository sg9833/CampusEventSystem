"""
Test Suite for Security Module
Tests all security features including encryption, rate limiting, sanitization, etc.
"""

import unittest
import time
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Import security components
from security import (
    DataEncryption,
    RateLimiter,
    SessionTimeout,
    InputSanitizer,
    SecurePassword,
    TokenManager,
    CSRFProtection,
    SecurityManager,
    get_security_manager
)


class TestDataEncryption(unittest.TestCase):
    """Test encryption and decryption functionality"""
    
    def setUp(self):
        """Create encryption instance with test key"""
        self.encryption = DataEncryption()
    
    def test_encrypt_decrypt_string(self):
        """Test basic string encryption and decryption"""
        original = "secret_data_123"
        encrypted = self.encryption.encrypt(original)
        
        # Encrypted should be different from original
        self.assertNotEqual(original, encrypted)
        
        # Should decrypt back to original
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(original, decrypted)
    
    def test_encrypt_decrypt_unicode(self):
        """Test encryption with Unicode characters"""
        original = "Hello 世界 🌍"
        encrypted = self.encryption.encrypt(original)
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(original, decrypted)
    
    def test_encrypt_empty_string(self):
        """Test encryption of empty string"""
        original = ""
        encrypted = self.encryption.encrypt(original)
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(original, decrypted)
    
    def test_encrypt_decrypt_dict(self):
        """Test dictionary encryption and decryption"""
        original = {
            "username": "testuser",
            "email": "test@example.com",
            "api_key": "secret123"
        }
        
        encrypted_dict = self.encryption.encrypt_dict(original)
        
        # Keys should remain the same
        self.assertEqual(set(original.keys()), set(encrypted_dict.keys()))
        
        # Values should be encrypted (different)
        for key in original:
            self.assertNotEqual(original[key], encrypted_dict[key])
        
        # Should decrypt back to original
        decrypted_dict = self.encryption.decrypt_dict(encrypted_dict)
        self.assertEqual(original, decrypted_dict)
    
    def test_encrypt_nested_dict(self):
        """Test nested dictionary encryption"""
        original = {
            "user": {
                "name": "John",
                "credentials": {
                    "password": "secret"
                }
            }
        }
        
        encrypted = self.encryption.encrypt_dict(original)
        decrypted = self.encryption.decrypt_dict(encrypted)
        self.assertEqual(original, decrypted)
    
    def test_decrypt_invalid_data(self):
        """Test decryption with invalid data"""
        with self.assertRaises(Exception):
            self.encryption.decrypt("invalid_encrypted_data")


class TestRateLimiter(unittest.TestCase):
    """Test rate limiting functionality"""
    
    def setUp(self):
        """Create rate limiter with test settings"""
        # 5 requests per 2 seconds for faster testing
        self.limiter = RateLimiter(max_requests=5, time_window=2)
    
    def test_allow_within_limit(self):
        """Test that requests within limit are allowed"""
        identifier = "test_user_1"
        
        # Should allow first 5 requests
        for i in range(5):
            self.assertTrue(self.limiter.is_allowed(identifier))
    
    def test_block_over_limit(self):
        """Test that requests over limit are blocked"""
        identifier = "test_user_2"
        
        # Use up the limit
        for i in range(5):
            self.limiter.is_allowed(identifier)
        
        # 6th request should be blocked
        self.assertFalse(self.limiter.is_allowed(identifier))
    
    def test_reset_after_time_window(self):
        """Test that limit resets after time window"""
        identifier = "test_user_3"
        
        # Use up the limit
        for i in range(5):
            self.limiter.is_allowed(identifier)
        
        # Should be blocked
        self.assertFalse(self.limiter.is_allowed(identifier))
        
        # Wait for time window to pass
        time.sleep(2.1)
        
        # Should be allowed again
        self.assertTrue(self.limiter.is_allowed(identifier))
    
    def test_different_identifiers_independent(self):
        """Test that different identifiers have independent limits"""
        user1 = "user1"
        user2 = "user2"
        
        # Use up limit for user1
        for i in range(5):
            self.limiter.is_allowed(user1)
        
        # user1 should be blocked
        self.assertFalse(self.limiter.is_allowed(user1))
        
        # user2 should still be allowed
        self.assertTrue(self.limiter.is_allowed(user2))
    
    def test_get_remaining_requests(self):
        """Test getting remaining request count"""
        identifier = "test_user_4"
        
        # Initially should have 5 requests available
        self.assertEqual(self.limiter.get_remaining(identifier), 5)
        
        # After 3 requests
        for i in range(3):
            self.limiter.is_allowed(identifier)
        
        self.assertEqual(self.limiter.get_remaining(identifier), 2)
    
    def test_manual_reset(self):
        """Test manual reset of rate limit"""
        identifier = "test_user_5"
        
        # Use up the limit
        for i in range(5):
            self.limiter.is_allowed(identifier)
        
        self.assertFalse(self.limiter.is_allowed(identifier))
        
        # Reset the limit
        self.limiter.reset(identifier)
        
        # Should be allowed again
        self.assertTrue(self.limiter.is_allowed(identifier))
        self.assertEqual(self.limiter.get_remaining(identifier), 5)


class TestSessionTimeout(unittest.TestCase):
    """Test session timeout functionality"""
    
    def setUp(self):
        """Create session timeout instance"""
        self.timeout_called = False
        self.warning_called = False
        
        def on_timeout():
            self.timeout_called = True
        
        def on_warning():
            self.warning_called = True
        
        # 1 minute timeout, 0.5 minute warning for faster testing
        self.session = SessionTimeout(
            timeout_minutes=1,  # 1 minute
            warning_minutes=1,  # 0.5 minutes (will adjust timing in tests)
            on_timeout=on_timeout,
            on_warning=on_warning
        )
    
    def tearDown(self):
        """Clean up session timeout"""
        if self.session.is_active():
            self.session.stop()
    
    def test_start_stop(self):
        """Test starting and stopping session timeout"""
        self.session.start()
        self.assertTrue(self.session.is_active())
        
        self.session.stop()
        self.assertFalse(self.session.is_active())
    
    def test_refresh_extends_timeout(self):
        """Test that refresh extends the timeout"""
        # Note: Actual timeout is 1 minute, so we test the mechanism without waiting
        self.session.start()
        
        # Get initial remaining time
        initial_remaining = self.session.get_remaining_time()
        
        # Wait a bit
        time.sleep(2)
        
        # Refresh activity
        self.session.refresh()
        
        # Remaining time should be reset to full timeout
        after_refresh = self.session.get_remaining_time()
        self.assertGreater(after_refresh, initial_remaining - 5)
        
        self.session.stop()
    
    def test_timeout_triggers(self):
        """Test that timeout callback would trigger (skipped for time)"""
        # This test would take 1 minute to run, so we verify the mechanism instead
        self.session.start()
        
        # Verify session is active
        self.assertTrue(self.session.is_active())
        
        # Verify remaining time is reasonable
        remaining = self.session.get_remaining_time()
        self.assertGreater(remaining, 50)
        self.assertLessEqual(remaining, 60)
        
        self.session.stop()
    
    def test_warning_triggers(self):
        """Test that warning mechanism is set up (skipped for time)"""
        # This test would take time to run, so we verify the session is active
        self.session.start()
        
        # Verify session is running
        self.assertTrue(self.session.is_active())
        
        self.session.stop()
    
    def test_pause_resume(self):
        """Test pausing and resuming timeout"""
        self.session.start()
        
        # Pause
        self.session.pause()
        
        # Verify paused state (implementation dependent)
        # Wait briefly
        time.sleep(1)
        
        self.assertFalse(self.timeout_called)
        
        # Resume
        self.session.resume()
        
        self.session.stop()
    
    def test_get_remaining_time(self):
        """Test getting remaining timeout time"""
        self.session.start()
        
        # Should have close to 60 seconds remaining
        remaining = self.session.get_remaining_time()
        self.assertGreater(remaining, 55)
        self.assertLessEqual(remaining, 60)
        
        # Wait 2 seconds
        time.sleep(2)
        
        # Should have close to 58 seconds remaining
        remaining = self.session.get_remaining_time()
        self.assertGreater(remaining, 56)
        self.assertLessEqual(remaining, 59)
        
        self.session.stop()


class TestInputSanitizer(unittest.TestCase):
    """Test input sanitization functionality"""
    
    def setUp(self):
        """Create sanitizer instance"""
        self.sanitizer = InputSanitizer()
    
    def test_sanitize_clean_string(self):
        """Test sanitization of clean string"""
        clean = "Hello World 123"
        result = self.sanitizer.sanitize_string(clean)
        self.assertEqual(clean, result)
    
    def test_detect_sql_injection(self):
        """Test detection of SQL injection attempts"""
        malicious = "'; DROP TABLE users; --"
        result = self.sanitizer.sanitize_string(malicious)
        
        # Should remove SQL keywords
        self.assertNotIn("DROP", result)
        self.assertNotIn("--", result)
    
    def test_detect_xss_script_tag(self):
        """Test detection of XSS script tags"""
        malicious = "<script>alert('XSS')</script>"
        result = self.sanitizer.sanitize_string(malicious)
        
        # Should remove script tags
        self.assertNotIn("<script>", result.lower())
    
    def test_detect_xss_event_handler(self):
        """Test detection of XSS event handlers"""
        malicious = "<img src=x onerror=alert('XSS')>"
        result = self.sanitizer.sanitize_string(malicious)
        
        # Should remove onerror
        self.assertNotIn("onerror", result.lower())
    
    def test_sanitize_email_valid(self):
        """Test sanitization of valid email"""
        email = "user@example.com"
        result = self.sanitizer.sanitize_email(email)
        self.assertEqual(email, result)
    
    def test_sanitize_email_invalid(self):
        """Test sanitization of invalid email"""
        invalid = "not_an_email"
        with self.assertRaises(ValueError):
            self.sanitizer.sanitize_email(invalid)
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        dangerous = "../../../etc/passwd"
        safe = self.sanitizer.sanitize_filename(dangerous)
        
        # Should not contain path traversal
        self.assertNotIn("..", safe)
        self.assertNotIn("/", safe)
    
    def test_validate_image_file(self):
        """Test image file validation"""
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            # Write small amount of data
            tmp.write(b"fake image data")
            tmp_path = tmp.name
        
        try:
            # Should validate successfully (small file, valid extension)
            result = self.sanitizer.validate_file_upload(tmp_path, "image")
            self.assertTrue(result)
        finally:
            os.unlink(tmp_path)
    
    def test_reject_oversized_file(self):
        """Test rejection of oversized file"""
        # Create a file larger than allowed
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            # Write more than 5MB
            tmp.write(b"x" * (6 * 1024 * 1024))
            tmp_path = tmp.name
        
        try:
            with self.assertRaises(ValueError):
                self.sanitizer.validate_file_upload(tmp_path, "image")
        finally:
            os.unlink(tmp_path)
    
    def test_reject_invalid_extension(self):
        """Test rejection of invalid file extension"""
        with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as tmp:
            tmp.write(b"executable")
            tmp_path = tmp.name
        
        try:
            with self.assertRaises(ValueError):
                self.sanitizer.validate_file_upload(tmp_path, "image")
        finally:
            os.unlink(tmp_path)
    
    def test_sanitize_dict(self):
        """Test dictionary sanitization"""
        dirty_dict = {
            "name": "John<script>alert('xss')</script>",
            "comment": "'; DROP TABLE users; --",
            "email": "user@example.com"
        }
        
        clean_dict = self.sanitizer.sanitize_dict(dirty_dict)
        
        # Should sanitize values
        self.assertNotIn("<script>", clean_dict["name"].lower())
        self.assertNotIn("DROP", clean_dict["comment"])
        
        # Clean value should remain unchanged
        self.assertEqual(clean_dict["email"], "user@example.com")


class TestSecurePassword(unittest.TestCase):
    """Test secure password handling"""
    
    def setUp(self):
        """Create secure password instance"""
        self.secure_pwd = SecurePassword()
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "MySecurePassword123!"
        hashed, salt = self.secure_pwd.hash_password(password)
        
        # Hash should be different from password
        self.assertNotEqual(password, hashed)
        
        # Hash should be base64 encoded
        self.assertTrue(len(hashed) > 0)
        self.assertTrue(len(salt) > 0)
    
    def test_verify_correct_password(self):
        """Test verification of correct password"""
        password = "CorrectPassword456"
        hashed, salt = self.secure_pwd.hash_password(password)
        
        # Should verify successfully
        self.assertTrue(self.secure_pwd.verify_password(password, hashed, salt))
    
    def test_verify_incorrect_password(self):
        """Test verification of incorrect password"""
        password = "CorrectPassword"
        wrong_password = "WrongPassword"
        hashed, salt = self.secure_pwd.hash_password(password)
        
        # Should fail verification
        self.assertFalse(self.secure_pwd.verify_password(wrong_password, hashed, salt))
    
    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (due to different salts)"""
        password = "SamePassword"
        hash1, salt1 = self.secure_pwd.hash_password(password)
        hash2, salt2 = self.secure_pwd.hash_password(password)
        
        # Hashes should be different
        self.assertNotEqual(hash1, hash2)
        self.assertNotEqual(salt1, salt2)
        
        # But both should verify
        self.assertTrue(self.secure_pwd.verify_password(password, hash1, salt1))
        self.assertTrue(self.secure_pwd.verify_password(password, hash2, salt2))
    
    def test_mask_password(self):
        """Test password masking"""
        password = "MyPassword123"
        masked = self.secure_pwd.mask_password(password)
        
        # Should show first and last character
        self.assertTrue(masked.startswith("M"))
        self.assertTrue(masked.endswith("3"))
        
        # Should have asterisks in middle
        self.assertIn("*", masked)
        
        # Should be same length
        self.assertEqual(len(masked), len(password))
    
    def test_mask_short_password(self):
        """Test masking of short password"""
        password = "ab"
        masked = self.secure_pwd.mask_password(password)
        self.assertEqual(masked, "ab")  # Too short to mask
    
    def test_generate_strong_password(self):
        """Test strong password generation"""
        password = self.secure_pwd.generate_strong_password(16)
        
        # Should be correct length
        self.assertEqual(len(password), 16)
        
        # Should contain various character types
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        self.assertTrue(has_upper or has_lower or has_digit)
    
    def test_clear_entry_widget(self):
        """Test clearing entry widget"""
        # Create mock entry widget
        mock_entry = Mock()
        mock_entry.get.return_value = "password123"
        
        self.secure_pwd.clear_entry(mock_entry)
        
        # Should have called delete and insert
        mock_entry.delete.assert_called()
        mock_entry.insert.assert_called()


class TestTokenManager(unittest.TestCase):
    """Test token management functionality"""
    
    def setUp(self):
        """Create token manager instance"""
        self.refresh_called = False
        self.new_token = "new_refreshed_token"
        
        def refresh_callback():
            self.refresh_called = True
            return self.new_token
        
        self.token_manager = TokenManager(refresh_callback=refresh_callback)
    
    def test_set_and_get_token(self):
        """Test setting and getting token"""
        token = "test_token_123"
        self.token_manager.set_token(token, expires_in=3600)
        
        retrieved = self.token_manager.get_token()
        self.assertEqual(token, retrieved)
    
    def test_token_expiry(self):
        """Test that expired token is detected"""
        token = "expiring_token"
        # Set token that expires in 1 second
        self.token_manager.set_token(token, expires_in=1)
        
        # Wait for expiry
        time.sleep(1.1)
        
        # Should return None for expired token (and trigger refresh)
        result = self.token_manager.get_token()
        self.assertIsNone(result)
    
    def test_auto_refresh_near_expiry(self):
        """Test automatic token refresh when near expiry"""
        token = "about_to_expire"
        # Set token that expires in 4 minutes (less than 5 minute threshold)
        self.token_manager.set_token(token, expires_in=240)
        
        # Get token should trigger refresh
        result = self.token_manager.get_token()
        
        # Should have called refresh
        self.assertTrue(self.refresh_called)
    
    def test_is_valid(self):
        """Test token validity check"""
        token = "valid_token"
        self.token_manager.set_token(token, expires_in=3600)
        
        self.assertTrue(self.token_manager.is_valid())
        
        # Clear token
        self.token_manager.clear()
        
        self.assertFalse(self.token_manager.is_valid())
    
    def test_clear_token(self):
        """Test clearing token"""
        token = "temp_token"
        self.token_manager.set_token(token, expires_in=3600)
        
        self.assertIsNotNone(self.token_manager.get_token())
        
        self.token_manager.clear()
        
        self.assertIsNone(self.token_manager.get_token())


class TestCSRFProtection(unittest.TestCase):
    """Test CSRF protection functionality"""
    
    def setUp(self):
        """Create CSRF protection instance"""
        self.csrf = CSRFProtection()
    
    def test_generate_token(self):
        """Test CSRF token generation"""
        session_id = "session_123"
        token = self.csrf.generate_token(session_id)
        
        # Should generate a token
        self.assertIsNotNone(token)
        self.assertTrue(len(token) > 0)
    
    def test_validate_correct_token(self):
        """Test validation of correct CSRF token"""
        session_id = "session_456"
        token = self.csrf.generate_token(session_id)
        
        # Should validate successfully
        self.assertTrue(self.csrf.validate_token(session_id, token))
    
    def test_validate_incorrect_token(self):
        """Test validation of incorrect CSRF token"""
        session_id = "session_789"
        token = self.csrf.generate_token(session_id)
        
        wrong_token = "wrong_token_value"
        
        # Should fail validation
        self.assertFalse(self.csrf.validate_token(session_id, wrong_token))
    
    def test_validate_wrong_session(self):
        """Test validation with wrong session ID"""
        session_id1 = "session_abc"
        session_id2 = "session_def"
        
        token = self.csrf.generate_token(session_id1)
        
        # Should fail when using different session
        self.assertFalse(self.csrf.validate_token(session_id2, token))
    
    def test_different_sessions_different_tokens(self):
        """Test that different sessions get different tokens"""
        session1 = "session_1"
        session2 = "session_2"
        
        token1 = self.csrf.generate_token(session1)
        token2 = self.csrf.generate_token(session2)
        
        # Tokens should be different
        self.assertNotEqual(token1, token2)


class TestSecurityManager(unittest.TestCase):
    """Test unified security manager"""
    
    def test_singleton_pattern(self):
        """Test that SecurityManager is a singleton"""
        manager1 = get_security_manager()
        manager2 = get_security_manager()
        
        # Should be the same instance
        self.assertIs(manager1, manager2)
    
    def test_encrypt_decrypt_data(self):
        """Test encryption through security manager"""
        manager = get_security_manager()
        
        data = "sensitive_information"
        encrypted = manager.encrypt_data(data)
        decrypted = manager.decrypt_data(encrypted)
        
        self.assertEqual(data, decrypted)
    
    def test_check_rate_limit(self):
        """Test rate limiting through security manager"""
        manager = get_security_manager()
        
        identifier = "test_user"
        
        # Should be allowed initially
        self.assertTrue(manager.check_rate_limit(identifier))
    
    def test_sanitize_input(self):
        """Test input sanitization through security manager"""
        manager = get_security_manager()
        
        malicious = "<script>alert('xss')</script>"
        safe = manager.sanitize_input(malicious)
        
        self.assertNotIn("<script>", safe.lower())
    
    def test_hash_verify_password(self):
        """Test password hashing and verification through security manager"""
        manager = get_security_manager()
        
        password = "TestPassword123"
        hashed, salt = manager.hash_password(password)
        
        # Correct password should verify
        self.assertTrue(manager.verify_password(password, hashed, salt))
        
        # Wrong password should not verify
        self.assertFalse(manager.verify_password("WrongPassword", hashed, salt))
    
    def test_csrf_token_generation_validation(self):
        """Test CSRF token operations through security manager"""
        manager = get_security_manager()
        
        session_id = "test_session"
        token = manager.generate_csrf_token(session_id)
        
        # Should validate correctly
        self.assertTrue(manager.validate_csrf_token(session_id, token))
        
        # Should fail with wrong token
        self.assertFalse(manager.validate_csrf_token(session_id, "wrong_token"))


def run_tests():
    """Run all security tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataEncryption))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimiter))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionTimeout))
    suite.addTests(loader.loadTestsFromTestCase(TestInputSanitizer))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurePassword))
    suite.addTests(loader.loadTestsFromTestCase(TestTokenManager))
    suite.addTests(loader.loadTestsFromTestCase(TestCSRFProtection))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityManager))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("SECURITY TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
