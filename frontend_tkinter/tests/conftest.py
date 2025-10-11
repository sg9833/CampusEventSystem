"""
Pytest Configuration and Shared Fixtures
Provides common test fixtures and setup for all tests
"""

import pytest
import tkinter as tk
from unittest.mock import Mock, MagicMock, patch
import sys
import os
from datetime import datetime, timedelta
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture(scope='function')
def root():
    """Create a Tkinter root window for testing"""
    root = tk.Tk()
    root.withdraw()  # Hide window during tests
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass  # Already destroyed


@pytest.fixture
def mock_api_client():
    """Mock API client with common responses"""
    mock = Mock()
    
    # Mock successful responses
    mock.get = Mock(return_value={'status': 'success', 'data': []})
    mock.post = Mock(return_value={'status': 'success', 'id': 1})
    mock.put = Mock(return_value={'status': 'success'})
    mock.delete = Mock(return_value={'status': 'success'})
    
    # Mock authentication
    mock.login = Mock(return_value={
        'user_id': 1,
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'STUDENT',
        'token': 'test_token_123'
    })
    
    return mock


@pytest.fixture
def mock_session():
    """Mock session manager"""
    mock = Mock()
    mock.is_logged_in = Mock(return_value=True)
    mock.get_user = Mock(return_value={
        'user_id': 1,
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'STUDENT'
    })
    mock.get_token = Mock(return_value='test_token_123')
    mock.logout = Mock()
    mock.update_session = Mock()
    return mock


@pytest.fixture
def sample_user():
    """Sample user data"""
    return {
        'id': 1,
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'STUDENT',
        'phone': '1234567890',
        'department': 'Computer Science'
    }


@pytest.fixture
def sample_event():
    """Sample event data"""
    return {
        'id': 1,
        'title': 'Test Event',
        'description': 'This is a test event description',
        'start_time': '2025-10-15T14:00:00',
        'end_time': '2025-10-15T16:00:00',
        'venue': 'Test Hall A',
        'category': 'academic',
        'capacity': 100,
        'available_seats': 50,
        'organizer_id': 1,
        'organizer_name': 'Test Organizer',
        'status': 'upcoming',
        'image_url': None
    }


@pytest.fixture
def sample_events_list(sample_event):
    """Sample list of events"""
    events = []
    for i in range(5):
        event = sample_event.copy()
        event['id'] = i + 1
        event['title'] = f'Test Event {i + 1}'
        events.append(event)
    return events


@pytest.fixture
def sample_booking():
    """Sample booking data"""
    return {
        'id': 1,
        'event_id': 1,
        'user_id': 1,
        'booking_date': '2025-10-10T10:00:00',
        'status': 'confirmed',
        'event_title': 'Test Event',
        'event_venue': 'Test Hall A',
        'event_start_time': '2025-10-15T14:00:00'
    }


@pytest.fixture
def sample_resource():
    """Sample resource data"""
    return {
        'id': 1,
        'name': 'Projector',
        'description': 'HD Projector with HDMI',
        'category': 'equipment',
        'quantity': 5,
        'available': 3,
        'status': 'available'
    }


@pytest.fixture
def sample_notification():
    """Sample notification data"""
    return {
        'id': 1,
        'user_id': 1,
        'title': 'Event Reminder',
        'message': 'Your event starts in 1 hour',
        'type': 'reminder',
        'read': False,
        'created_at': '2025-10-10T13:00:00'
    }


@pytest.fixture
def mock_error_handler():
    """Mock error handler"""
    mock = Mock()
    mock.handle_error = Mock()
    mock.handle_validation_error = Mock()
    mock.log_error = Mock()
    return mock


@pytest.fixture
def mock_logger():
    """Mock logger"""
    mock = Mock()
    mock.debug = Mock()
    mock.info = Mock()
    mock.warning = Mock()
    mock.error = Mock()
    mock.critical = Mock()
    return mock


@pytest.fixture
def temp_config_file(tmp_path):
    """Create temporary config.ini file"""
    config_content = """[API]
base_url = http://localhost:8080/api
timeout = 30

[UI]
theme = light
window_width = 1200
window_height = 700

[CACHE]
enabled = true
ttl = 300
"""
    config_file = tmp_path / "config.ini"
    config_file.write_text(config_content)
    return str(config_file)


@pytest.fixture
def mock_image():
    """Mock PIL Image for testing"""
    mock = Mock()
    mock.size = (300, 200)
    mock.resize = Mock(return_value=mock)
    mock.save = Mock()
    return mock


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests"""
    # This helps prevent test contamination from singleton patterns
    yield
    # Cleanup happens after test


@pytest.fixture
def mock_messagebox():
    """Mock tkinter messagebox"""
    with patch('tkinter.messagebox.showinfo') as mock_info, \
         patch('tkinter.messagebox.showerror') as mock_error, \
         patch('tkinter.messagebox.showwarning') as mock_warning, \
         patch('tkinter.messagebox.askyesno') as mock_yesno:
        
        mock_yesno.return_value = True  # Default to Yes
        
        yield {
            'showinfo': mock_info,
            'showerror': mock_error,
            'showwarning': mock_warning,
            'askyesno': mock_yesno
        }


@pytest.fixture
def mock_filedialog():
    """Mock tkinter filedialog"""
    with patch('tkinter.filedialog.askopenfilename') as mock_open, \
         patch('tkinter.filedialog.asksaveasfilename') as mock_save:
        
        mock_open.return_value = '/test/file.jpg'
        mock_save.return_value = '/test/output.pdf'
        
        yield {
            'askopenfilename': mock_open,
            'asksaveasfilename': mock_save
        }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "ui: marks tests as UI tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# Helper functions for tests
def create_mock_response(status_code=200, json_data=None, raise_error=None):
    """Create a mock HTTP response"""
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.json = Mock(return_value=json_data or {})
    mock_resp.text = json.dumps(json_data or {})
    
    if raise_error:
        mock_resp.raise_for_status = Mock(side_effect=raise_error)
    else:
        mock_resp.raise_for_status = Mock()
    
    return mock_resp
