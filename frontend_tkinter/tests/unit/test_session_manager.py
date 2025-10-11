"""
Unit Tests for Session Manager
Tests session management, authentication state, and user data handling
"""

import pytest
from unittest.mock import Mock, patch, mock_open
import json
from datetime import datetime, timedelta
from utils.session_manager import SessionManager


class TestSessionManager:
    """Test suite for SessionManager class"""
    
    def test_singleton_pattern(self):
        """Test that SessionManager follows singleton pattern"""
        # Arrange & Act
        session1 = SessionManager()
        session2 = SessionManager()
        
        # Assert
        assert session1 is session2
    
    def test_initial_state_not_logged_in(self):
        """Test initial state is not logged in"""
        # Arrange & Act
        session = SessionManager()
        session._user = None  # Reset state
        
        # Assert
        assert session.is_logged_in() == False
        assert session.get_user() is None
    
    def test_login_sets_user_data(self):
        """Test login method sets user data correctly"""
        # Arrange
        session = SessionManager()
        user_data = {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com',
            'role': 'STUDENT',
            'token': 'test_token'
        }
        
        # Act
        session.login(user_data)
        
        # Assert
        assert session.is_logged_in() == True
        assert session.get_user()['email'] == 'test@example.com'
        assert session.get_token() == 'test_token'
    
    def test_logout_clears_user_data(self):
        """Test logout method clears user data"""
        # Arrange
        session = SessionManager()
        session.login({
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com',
            'token': 'test_token'
        })
        
        # Act
        session.logout()
        
        # Assert
        assert session.is_logged_in() == False
        assert session.get_user() is None
        assert session.get_token() is None
    
    def test_get_user_id(self):
        """Test getting user ID"""
        # Arrange
        session = SessionManager()
        session.login({
            'id': 42,
            'name': 'Test User',
            'email': 'test@example.com'
        })
        
        # Act
        user_id = session.get_user_id()
        
        # Assert
        assert user_id == 42
    
    def test_get_user_role(self):
        """Test getting user role"""
        # Arrange
        session = SessionManager()
        session.login({
            'id': 1,
            'name': 'Test User',
            'role': 'ORGANIZER'
        })
        
        # Act
        role = session.get_role()
        
        # Assert
        assert role == 'ORGANIZER'
    
    def test_update_user_data(self):
        """Test updating user data"""
        # Arrange
        session = SessionManager()
        session.login({
            'id': 1,
            'name': 'Old Name',
            'email': 'test@example.com'
        })
        
        # Act
        session.update_user({'name': 'New Name', 'phone': '1234567890'})
        
        # Assert
        user = session.get_user()
        assert user['name'] == 'New Name'
        assert user['phone'] == '1234567890'
    
    def test_is_student_role(self):
        """Test checking if user is a student"""
        # Arrange
        session = SessionManager()
        session.login({
            'id': 1,
            'role': 'STUDENT'
        })
        
        # Act & Assert
        assert session.is_student() == True
        assert session.is_organizer() == False
        assert session.is_admin() == False
    
    def test_is_organizer_role(self):
        """Test checking if user is an organizer"""
        # Arrange
        session = SessionManager()
        session.login({
            'id': 1,
            'role': 'ORGANIZER'
        })
        
        # Act & Assert
        assert session.is_student() == False
        assert session.is_organizer() == True
        assert session.is_admin() == False
    
    def test_is_admin_role(self):
        """Test checking if user is an admin"""
        # Arrange
        session = SessionManager()
        session.login({
            'id': 1,
            'role': 'ADMIN'
        })
        
        # Act & Assert
        assert session.is_student() == False
        assert session.is_organizer() == False
        assert session.is_admin() == True


class TestSessionPersistence:
    """Test session persistence and storage"""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_save_session_to_file(self, mock_exists, mock_file):
        """Test saving session to file"""
        # Arrange
        mock_exists.return_value = True
        session = SessionManager()
        session.login({
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com',
            'token': 'test_token'
        })
        
        # Act
        session.save_to_file()
        
        # Assert
        mock_file.assert_called()
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"id": 1, "name": "Test User"}')
    @patch('os.path.exists')
    def test_load_session_from_file(self, mock_exists, mock_file):
        """Test loading session from file"""
        # Arrange
        mock_exists.return_value = True
        session = SessionManager()
        
        # Act
        session.load_from_file()
        
        # Assert
        # Verify file was read
        mock_file.assert_called()


class TestSessionTimeout:
    """Test session timeout functionality"""
    
    def test_session_expired(self):
        """Test detecting expired session"""
        # Arrange
        session = SessionManager()
        session.login({'id': 1})
        
        # Simulate old last activity time
        session._last_activity = datetime.now() - timedelta(hours=2)
        session._timeout = 1800  # 30 minutes
        
        # Act
        is_expired = session.is_session_expired()
        
        # Assert
        assert is_expired == True
    
    def test_session_not_expired(self):
        """Test detecting active session"""
        # Arrange
        session = SessionManager()
        session.login({'id': 1})
        session._last_activity = datetime.now()
        session._timeout = 1800
        
        # Act
        is_expired = session.is_session_expired()
        
        # Assert
        assert is_expired == False
    
    def test_refresh_activity(self):
        """Test refreshing session activity"""
        # Arrange
        session = SessionManager()
        session.login({'id': 1})
        old_time = session._last_activity
        
        # Act
        import time
        time.sleep(0.1)  # Small delay
        session.refresh_activity()
        
        # Assert
        assert session._last_activity > old_time
