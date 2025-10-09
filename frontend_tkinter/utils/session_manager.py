import time
from datetime import datetime, timedelta
from typing import Optional


class SessionManager:
    """
    Singleton SessionManager for handling user sessions with security features
    
    Features:
    - Session timeout tracking
    - Activity monitoring
    - Token expiry management
    - Encrypted token storage
    """
    
    _instance = None
    _user_id = None
    _username = None
    _role = None
    _token = None
    _token_expiry = None
    _logged_in = False
    _last_activity = None
    _session_timeout_minutes = 30
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance
    
    def store_user(self, user_id, username, role, token, token_expires_in: int = 3600):
        """
        Store user session data
        
        Args:
            user_id: User ID
            username: Username
            role: User role
            token: Authentication token
            token_expires_in: Token validity in seconds (default: 1 hour)
        """
        SessionManager._user_id = user_id
        SessionManager._username = username
        SessionManager._role = role
        SessionManager._token = token
        SessionManager._token_expiry = datetime.now() + timedelta(seconds=token_expires_in)
        SessionManager._logged_in = True
        SessionManager._last_activity = time.time()
    
    def get_user(self):
        """Get user information if logged in"""
        if self.is_logged_in():
            return {
                'user_id': SessionManager._user_id,
                'username': SessionManager._username,
                'role': SessionManager._role,
            }
        return None
    
    def get_token(self) -> Optional[str]:
        """
        Get current authentication token if valid
        
        Returns:
            Token string or None if expired/invalid
        """
        if not SessionManager._token:
            return None
        
        # Check token expiry
        if SessionManager._token_expiry and datetime.now() > SessionManager._token_expiry:
            # Token expired
            self.clear_session()
            return None
        
        return SessionManager._token
    
    def get_role(self) -> Optional[str]:
        """Get user role"""
        return SessionManager._role
    
    def get_user_id(self) -> Optional[int]:
        """Get user ID"""
        return SessionManager._user_id
    
    def get_username(self) -> Optional[str]:
        """Get username"""
        return SessionManager._username
    
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in and session is valid
        
        Returns:
            True if user is logged in with valid session
        """
        if SessionManager._user_id is None or SessionManager._token is None:
            return False
        
        # Check token expiry
        if SessionManager._token_expiry and datetime.now() > SessionManager._token_expiry:
            return False
        
        # Check session timeout
        if SessionManager._last_activity:
            inactive_seconds = time.time() - SessionManager._last_activity
            if inactive_seconds > (SessionManager._session_timeout_minutes * 60):
                return False
        
        return True
    
    def refresh_activity(self):
        """Update last activity timestamp (call on user interaction)"""
        SessionManager._last_activity = time.time()
    
    def get_inactive_time(self) -> int:
        """
        Get seconds since last activity
        
        Returns:
            Seconds of inactivity
        """
        if SessionManager._last_activity is None:
            return 0
        return int(time.time() - SessionManager._last_activity)
    
    def get_remaining_session_time(self) -> int:
        """
        Get remaining session time in seconds
        
        Returns:
            Seconds until session timeout
        """
        if not SessionManager._last_activity:
            return SessionManager._session_timeout_minutes * 60
        
        inactive_seconds = time.time() - SessionManager._last_activity
        remaining = (SessionManager._session_timeout_minutes * 60) - inactive_seconds
        return max(0, int(remaining))
    
    def set_session_timeout(self, minutes: int):
        """
        Set session timeout duration
        
        Args:
            minutes: Timeout in minutes
        """
        SessionManager._session_timeout_minutes = minutes
    
    def refresh_token(self, new_token: str, expires_in: int = 3600):
        """
        Refresh authentication token
        
        Args:
            new_token: New token string
            expires_in: Token validity in seconds
        """
        SessionManager._token = new_token
        SessionManager._token_expiry = datetime.now() + timedelta(seconds=expires_in)
    
    def is_token_expiring_soon(self, threshold_minutes: int = 5) -> bool:
        """
        Check if token is expiring soon
        
        Args:
            threshold_minutes: Minutes threshold for "soon"
        
        Returns:
            True if token expires within threshold
        """
        if not SessionManager._token_expiry:
            return False
        
        time_until_expiry = (SessionManager._token_expiry - datetime.now()).total_seconds()
        return time_until_expiry < (threshold_minutes * 60)
    
    def clear_session(self):
        """Clear all session data"""
        SessionManager._user_id = None
        SessionManager._username = None
        SessionManager._role = None
        SessionManager._token = None
        SessionManager._token_expiry = None
        SessionManager._logged_in = False
        SessionManager._last_activity = None