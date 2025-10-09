"""
Security Module for Campus Event System

Provides comprehensive security features:
- Token refresh logic
- Data encryption/decryption
- Rate limiting for API calls
- Session timeout with auto-logout
- Input sanitization (XSS, SQL injection prevention)
- Secure password handling
- File upload validation
- CSRF protection

Author: Campus Event System Team
Version: 1.7.0
Date: October 9, 2025
"""

import os
import time
import hashlib
import secrets
import base64
import re
import threading
import mimetypes
from typing import Optional, Dict, List, Tuple, Any, Callable
from datetime import datetime, timedelta
from collections import deque
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import tkinter as tk
from tkinter import messagebox


# ============================================================================
#  ENCRYPTION & DECRYPTION
# ============================================================================

class DataEncryption:
    """
    Handle encryption and decryption of sensitive data using Fernet (symmetric encryption)
    """
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize encryption with a key
        
        Args:
            key: Encryption key (32 bytes). If None, generates a new key.
        """
        if key is None:
            # Generate a key from a password
            password = secrets.token_urlsafe(32).encode()
            salt = secrets.token_bytes(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
        
        self.cipher = Fernet(key)
        self._key = key
    
    def get_key(self) -> bytes:
        """Get the encryption key (store this securely!)"""
        return self._key
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt string data
        
        Args:
            data: Plain text to encrypt
        
        Returns:
            Encrypted data as base64 string
        """
        if not data:
            return ""
        
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted data
        
        Args:
            encrypted_data: Encrypted data as base64 string
        
        Returns:
            Decrypted plain text
        """
        if not encrypted_data:
            return ""
        
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    def encrypt_dict(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Encrypt dictionary values
        
        Args:
            data: Dictionary with string values
        
        Returns:
            Dictionary with encrypted values
        """
        encrypted = {}
        for key, value in data.items():
            if isinstance(value, str):
                encrypted[key] = self.encrypt(value)
            else:
                encrypted[key] = self.encrypt(str(value))
        return encrypted
    
    def decrypt_dict(self, encrypted_data: Dict[str, str]) -> Dict[str, str]:
        """
        Decrypt dictionary values
        
        Args:
            encrypted_data: Dictionary with encrypted values
        
        Returns:
            Dictionary with decrypted values
        """
        decrypted = {}
        for key, value in encrypted_data.items():
            decrypted[key] = self.decrypt(value)
        return decrypted


# ============================================================================
#  RATE LIMITING
# ============================================================================

class RateLimiter:
    """
    Rate limiting for API calls to prevent abuse
    Implements sliding window rate limiting
    """
    
    def __init__(self, max_requests: int = 100, time_window: int = 60):
        """
        Initialize rate limiter
        
        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds (default: 60s)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: deque = deque()
        self.lock = threading.Lock()
    
    def is_allowed(self, identifier: str = "default") -> bool:
        """
        Check if request is allowed
        
        Args:
            identifier: Unique identifier for the requester (e.g., user_id, IP)
        
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        with self.lock:
            current_time = time.time()
            
            # Remove requests outside the time window
            while self.requests and self.requests[0][1] < current_time - self.time_window:
                self.requests.popleft()
            
            # Count requests for this identifier
            count = sum(1 for req_id, _ in self.requests if req_id == identifier)
            
            if count >= self.max_requests:
                return False
            
            # Add current request
            self.requests.append((identifier, current_time))
            return True
    
    def get_remaining(self, identifier: str = "default") -> int:
        """
        Get remaining requests allowed
        
        Args:
            identifier: Unique identifier for the requester
        
        Returns:
            Number of remaining requests
        """
        with self.lock:
            current_time = time.time()
            
            # Remove old requests
            while self.requests and self.requests[0][1] < current_time - self.time_window:
                self.requests.popleft()
            
            # Count requests for this identifier
            count = sum(1 for req_id, _ in self.requests if req_id == identifier)
            return max(0, self.max_requests - count)
    
    def reset(self, identifier: Optional[str] = None):
        """
        Reset rate limit for identifier or all
        
        Args:
            identifier: Specific identifier to reset, or None to reset all
        """
        with self.lock:
            if identifier is None:
                self.requests.clear()
            else:
                self.requests = deque(
                    [(req_id, timestamp) for req_id, timestamp in self.requests 
                     if req_id != identifier]
                )


# ============================================================================
#  SESSION TIMEOUT
# ============================================================================

class SessionTimeout:
    """
    Automatic session timeout with warning dialog
    Auto-logout after period of inactivity
    """
    
    def __init__(
        self,
        timeout_minutes: int = 30,
        warning_minutes: int = 5,
        on_timeout: Optional[Callable] = None,
        on_warning: Optional[Callable] = None
    ):
        """
        Initialize session timeout
        
        Args:
            timeout_minutes: Minutes of inactivity before logout (default: 30)
            warning_minutes: Minutes before timeout to show warning (default: 5)
            on_timeout: Callback when session times out
            on_warning: Callback when warning should be shown
        """
        self.timeout_seconds = timeout_minutes * 60
        self.warning_seconds = warning_minutes * 60
        self.on_timeout = on_timeout
        self.on_warning = on_warning
        
        self.last_activity = time.time()
        self.warning_shown = False
        self.timer_thread = None
        self.running = False
        self.paused = False
    
    def start(self):
        """Start the timeout timer"""
        if not self.running:
            self.running = True
            self.paused = False
            self.last_activity = time.time()
            self.warning_shown = False
            self.timer_thread = threading.Thread(target=self._monitor, daemon=True)
            self.timer_thread.start()
    
    def stop(self):
        """Stop the timeout timer"""
        self.running = False
        self.paused = False
    
    def pause(self):
        """Pause the timeout timer"""
        self.paused = True
    
    def resume(self):
        """Resume the timeout timer"""
        self.paused = False
        self.refresh()
    
    def refresh(self):
        """Refresh activity timestamp (call on user interaction)"""
        self.last_activity = time.time()
        self.warning_shown = False
    
    def _monitor(self):
        """Monitor thread that checks for timeout"""
        while self.running:
            if not self.paused:
                current_time = time.time()
                inactive_seconds = current_time - self.last_activity
                
                # Check if timeout reached
                if inactive_seconds >= self.timeout_seconds:
                    self.running = False
                    if self.on_timeout:
                        self.on_timeout()
                    break
                
                # Check if warning should be shown
                elif inactive_seconds >= (self.timeout_seconds - self.warning_seconds):
                    if not self.warning_shown:
                        self.warning_shown = True
                        if self.on_warning:
                            remaining = int((self.timeout_seconds - inactive_seconds) / 60)
                            self.on_warning(remaining)
            
            time.sleep(1)  # Check every second
    
    def get_remaining_time(self) -> int:
        """
        Get remaining time before timeout in seconds
        
        Returns:
            Seconds remaining before timeout
        """
        if self.paused:
            return self.timeout_seconds
        
        inactive_seconds = time.time() - self.last_activity
        remaining = self.timeout_seconds - inactive_seconds
        return max(0, int(remaining))
    
    def is_active(self) -> bool:
        """Check if timeout monitoring is active"""
        return self.running and not self.paused


# ============================================================================
#  INPUT SANITIZATION
# ============================================================================

class InputSanitizer:
    """
    Sanitize user input to prevent XSS, SQL injection, and other attacks
    """
    
    # Dangerous patterns
    SQL_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
        r"(--|;|\/\*|\*\/)",
        r"(\bOR\b.*=.*|'\s*OR\s*')",
        r"(\bUNION\b.*\bSELECT\b)",
    ]
    
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
    ]
    
    # Allowed file extensions for uploads
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.csv'}
    
    # Maximum file sizes (in bytes)
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10 MB
    
    @staticmethod
    def sanitize_string(text: str, allow_html: bool = False) -> str:
        """
        Sanitize string input
        
        Args:
            text: Input text to sanitize
            allow_html: If False, removes all HTML tags
        
        Returns:
            Sanitized string
        """
        if not text:
            return ""
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Check for SQL injection patterns
        for pattern in InputSanitizer.SQL_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                # Remove the dangerous content
                text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Check for XSS patterns
        for pattern in InputSanitizer.XSS_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        if not allow_html:
            # Remove all HTML tags
            text = re.sub(r'<[^>]+>', '', text)
        
        # Encode special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#x27;')
        
        return text.strip()
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        """
        Sanitize email address
        
        Args:
            email: Email address
        
        Returns:
            Sanitized email
        """
        if not email:
            return ""
        
        # Remove whitespace
        email = email.strip().lower()
        
        # Remove any HTML or SQL patterns
        email = InputSanitizer.sanitize_string(email)
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return ""
        
        return email
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for safe storage
        
        Args:
            filename: Original filename
        
        Returns:
            Safe filename
        """
        if not filename:
            return "unnamed_file"
        
        # Remove path separators
        filename = os.path.basename(filename)
        
        # Remove dangerous characters
        filename = re.sub(r'[^\w\s.-]', '', filename)
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Limit length
        name, ext = os.path.splitext(filename)
        if len(name) > 50:
            name = name[:50]
        
        return name + ext
    
    @staticmethod
    def validate_file_upload(
        filepath: str,
        file_type: str = 'image',
        max_size: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Validate file upload
        
        Args:
            filepath: Path to the file
            file_type: Type of file ('image' or 'document')
            max_size: Maximum file size in bytes (optional)
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file exists
        if not os.path.exists(filepath):
            return False, "File does not exist"
        
        # Check file size
        file_size = os.path.getsize(filepath)
        
        if max_size is None:
            if file_type == 'image':
                max_size = InputSanitizer.MAX_IMAGE_SIZE
            else:
                max_size = InputSanitizer.MAX_DOCUMENT_SIZE
        
        if file_size > max_size:
            max_mb = max_size / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_mb:.1f} MB"
        
        if file_size == 0:
            return False, "File is empty"
        
        # Check file extension
        _, ext = os.path.splitext(filepath)
        ext = ext.lower()
        
        if file_type == 'image':
            if ext not in InputSanitizer.ALLOWED_IMAGE_EXTENSIONS:
                return False, f"Invalid image format. Allowed: {', '.join(InputSanitizer.ALLOWED_IMAGE_EXTENSIONS)}"
        elif file_type == 'document':
            if ext not in InputSanitizer.ALLOWED_DOCUMENT_EXTENSIONS:
                return False, f"Invalid document format. Allowed: {', '.join(InputSanitizer.ALLOWED_DOCUMENT_EXTENSIONS)}"
        
        # Verify MIME type matches extension
        mime_type, _ = mimetypes.guess_type(filepath)
        if mime_type:
            if file_type == 'image' and not mime_type.startswith('image/'):
                return False, "File content does not match image extension"
            elif file_type == 'document' and not (mime_type.startswith('application/') or mime_type.startswith('text/')):
                return False, "File content does not match document extension"
        
        return True, ""
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any], exclude_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Sanitize all string values in a dictionary
        
        Args:
            data: Dictionary to sanitize
            exclude_keys: Keys to exclude from sanitization (e.g., ['password'])
        
        Returns:
            Sanitized dictionary
        """
        if exclude_keys is None:
            exclude_keys = []
        
        sanitized = {}
        for key, value in data.items():
            if key in exclude_keys:
                sanitized[key] = value
            elif isinstance(value, str):
                sanitized[key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = InputSanitizer.sanitize_dict(value, exclude_keys)
            elif isinstance(value, list):
                sanitized[key] = [
                    InputSanitizer.sanitize_string(item) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        
        return sanitized


# ============================================================================
#  SECURE PASSWORD HANDLING
# ============================================================================

class SecurePassword:
    """
    Secure password handling - never log passwords, mask in memory, clear after use
    """
    
    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[str, bytes]:
        """
        Hash password using PBKDF2
        
        Args:
            password: Plain text password
            salt: Salt for hashing (generates if None)
        
        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_bytes(16)
        
        # Use PBKDF2 with SHA-256
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        key = kdf.derive(password.encode())
        hashed = base64.b64encode(key).decode()
        
        return hashed, salt
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: bytes) -> bool:
        """
        Verify password against hash
        
        Args:
            password: Plain text password to verify
            hashed: Stored hashed password
            salt: Salt used for hashing
        
        Returns:
            True if password matches
        """
        new_hashed, _ = SecurePassword.hash_password(password, salt)
        return secrets.compare_digest(new_hashed, hashed)
    
    @staticmethod
    def mask_password(password: str) -> str:
        """
        Mask password for display (e.g., in logs)
        
        Args:
            password: Password to mask
        
        Returns:
            Masked password string
        """
        if not password:
            return ""
        
        if len(password) <= 2:
            return "*" * len(password)
        
        # Show first and last character
        return password[0] + "*" * (len(password) - 2) + password[-1]
    
    @staticmethod
    def clear_entry(entry_widget: tk.Entry):
        """
        Securely clear password entry widget
        
        Args:
            entry_widget: Tkinter Entry widget
        """
        # Overwrite with random data first
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, secrets.token_urlsafe(32))
        entry_widget.delete(0, tk.END)
    
    @staticmethod
    def generate_strong_password(length: int = 16) -> str:
        """
        Generate a strong random password
        
        Args:
            length: Length of password (default: 16)
        
        Returns:
            Strong random password
        """
        # Use secrets for cryptographically strong random
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password


# ============================================================================
#  TOKEN MANAGEMENT
# ============================================================================

class TokenManager:
    """
    Manage authentication tokens with refresh logic
    """
    
    def __init__(self, refresh_callback: Optional[Callable] = None):
        """
        Initialize token manager
        
        Args:
            refresh_callback: Callback function to refresh token
                             Should return new token or None if refresh fails
        """
        self.token = None
        self.token_expiry = None
        self.refresh_callback = refresh_callback
        self.refresh_lock = threading.Lock()
    
    def set_token(self, token: str, expires_in: int = 3600):
        """
        Set authentication token
        
        Args:
            token: Authentication token
            expires_in: Token validity in seconds (default: 1 hour)
        """
        self.token = token
        self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
    
    def get_token(self) -> Optional[str]:
        """
        Get current token, refresh if expired
        
        Returns:
            Current valid token or None
        """
        # Check if token is expired or about to expire (within 5 minutes)
        if self.token and self.token_expiry:
            time_until_expiry = (self.token_expiry - datetime.now()).total_seconds()
            
            if time_until_expiry < 300:  # Less than 5 minutes
                # Try to refresh
                if self.refresh_callback:
                    with self.refresh_lock:
                        # Double-check after acquiring lock
                        if (self.token_expiry - datetime.now()).total_seconds() < 300:
                            new_token = self.refresh_callback(self.token)
                            if new_token:
                                self.set_token(new_token)
                            else:
                                self.token = None
                                self.token_expiry = None
                                return None
        
        return self.token
    
    def is_valid(self) -> bool:
        """Check if token is valid"""
        if not self.token or not self.token_expiry:
            return False
        
        return datetime.now() < self.token_expiry
    
    def clear(self):
        """Clear token"""
        self.token = None
        self.token_expiry = None


# ============================================================================
#  CSRF PROTECTION
# ============================================================================

class CSRFProtection:
    """
    CSRF (Cross-Site Request Forgery) protection
    """
    
    def __init__(self):
        """Initialize CSRF protection"""
        self.tokens: Dict[str, Tuple[str, datetime]] = {}
        self.token_expiry_seconds = 3600  # 1 hour
    
    def generate_token(self, session_id: str) -> str:
        """
        Generate CSRF token for session
        
        Args:
            session_id: Session identifier
        
        Returns:
            CSRF token
        """
        token = secrets.token_urlsafe(32)
        expiry = datetime.now() + timedelta(seconds=self.token_expiry_seconds)
        self.tokens[session_id] = (token, expiry)
        
        # Clean up expired tokens
        self._cleanup_expired()
        
        return token
    
    def validate_token(self, session_id: str, token: str) -> bool:
        """
        Validate CSRF token
        
        Args:
            session_id: Session identifier
            token: Token to validate
        
        Returns:
            True if token is valid
        """
        if session_id not in self.tokens:
            return False
        
        stored_token, expiry = self.tokens[session_id]
        
        # Check expiry
        if datetime.now() > expiry:
            del self.tokens[session_id]
            return False
        
        # Compare tokens
        return secrets.compare_digest(stored_token, token)
    
    def _cleanup_expired(self):
        """Remove expired tokens"""
        current_time = datetime.now()
        expired = [
            session_id for session_id, (_, expiry) in self.tokens.items()
            if current_time > expiry
        ]
        for session_id in expired:
            del self.tokens[session_id]


# ============================================================================
#  SECURITY MANAGER (Main Class)
# ============================================================================

class SecurityManager:
    """
    Main security manager that coordinates all security features
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(SecurityManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize security manager"""
        if self._initialized:
            return
        
        # Initialize components
        self.encryption = DataEncryption()
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)
        self.session_timeout = None  # Will be initialized with callbacks
        self.sanitizer = InputSanitizer()
        self.password_handler = SecurePassword()
        self.token_manager = TokenManager()
        self.csrf = CSRFProtection()
        
        self._initialized = True
    
    # Encryption methods
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.encryption.encrypt(data)
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.encryption.decrypt(encrypted_data)
    
    # Rate limiting methods
    def check_rate_limit(self, identifier: str = "default") -> bool:
        """Check if request is allowed under rate limit"""
        return self.rate_limiter.is_allowed(identifier)
    
    def get_remaining_requests(self, identifier: str = "default") -> int:
        """Get remaining API requests allowed"""
        return self.rate_limiter.get_remaining(identifier)
    
    # Session timeout methods
    def setup_session_timeout(
        self,
        timeout_minutes: int = 30,
        warning_minutes: int = 5,
        on_timeout: Optional[Callable] = None,
        on_warning: Optional[Callable] = None
    ):
        """Setup session timeout monitoring"""
        self.session_timeout = SessionTimeout(
            timeout_minutes=timeout_minutes,
            warning_minutes=warning_minutes,
            on_timeout=on_timeout,
            on_warning=on_warning
        )
        self.session_timeout.start()
    
    def refresh_session(self):
        """Refresh session activity"""
        if self.session_timeout:
            self.session_timeout.refresh()
    
    # Input sanitization methods
    def sanitize_input(self, text: str, allow_html: bool = False) -> str:
        """Sanitize user input"""
        return self.sanitizer.sanitize_string(text, allow_html)
    
    def sanitize_form_data(self, data: Dict[str, Any], exclude_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """Sanitize form data dictionary"""
        return self.sanitizer.sanitize_dict(data, exclude_keys)
    
    def validate_file(self, filepath: str, file_type: str = 'image') -> Tuple[bool, str]:
        """Validate file upload"""
        return self.sanitizer.validate_file_upload(filepath, file_type)
    
    # Password methods
    def hash_password(self, password: str) -> Tuple[str, bytes]:
        """Hash password securely"""
        return self.password_handler.hash_password(password)
    
    def verify_password(self, password: str, hashed: str, salt: bytes) -> bool:
        """Verify password"""
        return self.password_handler.verify_password(password, hashed, salt)
    
    def mask_password(self, password: str) -> str:
        """Mask password for display"""
        return self.password_handler.mask_password(password)
    
    def clear_password_field(self, entry_widget: tk.Entry):
        """Securely clear password entry"""
        self.password_handler.clear_entry(entry_widget)
    
    # Token methods
    def set_token(self, token: str, expires_in: int = 3600):
        """Set authentication token"""
        self.token_manager.set_token(token, expires_in)
    
    def get_token(self) -> Optional[str]:
        """Get current valid token"""
        return self.token_manager.get_token()
    
    # CSRF methods
    def generate_csrf_token(self, session_id: str) -> str:
        """Generate CSRF token"""
        return self.csrf.generate_token(session_id)
    
    def validate_csrf_token(self, session_id: str, token: str) -> bool:
        """Validate CSRF token"""
        return self.csrf.validate_token(session_id, token)


# ============================================================================
#  CONVENIENCE FUNCTIONS
# ============================================================================

def get_security_manager() -> SecurityManager:
    """Get singleton SecurityManager instance"""
    return SecurityManager()


# ============================================================================
#  MODULE EXPORTS
# ============================================================================

__all__ = [
    # Main classes
    'SecurityManager',
    'DataEncryption',
    'RateLimiter',
    'SessionTimeout',
    'InputSanitizer',
    'SecurePassword',
    'TokenManager',
    'CSRFProtection',
    
    # Functions
    'get_security_manager',
]
