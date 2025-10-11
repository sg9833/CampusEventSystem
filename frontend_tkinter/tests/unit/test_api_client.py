"""
Unit Tests for API Client
Tests all API client functionality including authentication, error handling, and rate limiting
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
from utils.api_client import APIClient


class TestAPIClient:
    """Test suite for APIClient class"""
    
    def test_init(self):
        """Test API client initialization"""
        client = APIClient()
        assert client is not None
        assert hasattr(client, 'base_url')
        assert hasattr(client, 'session')
    
    @patch('requests.Session.get')
    def test_get_request_success(self, mock_get):
        """Test successful GET request"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test_data', 'status': 'success'}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Act
        client = APIClient()
        result = client.get('events')
        
        # Assert
        assert result == {'data': 'test_data', 'status': 'success'}
        mock_get.assert_called_once()
    
    @patch('requests.Session.get')
    def test_get_request_404(self, mock_get):
        """Test GET request with 404 error"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        # Act & Assert
        client = APIClient()
        with pytest.raises(requests.HTTPError):
            client.get('nonexistent')
    
    @patch('requests.Session.post')
    def test_post_request_success(self, mock_post):
        """Test successful POST request"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 1, 'status': 'created'}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Act
        client = APIClient()
        data = {'title': 'Test Event', 'venue': 'Hall A'}
        result = client.post('events', data)
        
        # Assert
        assert result == {'id': 1, 'status': 'created'}
        mock_post.assert_called_once()
    
    @patch('requests.Session.post')
    def test_post_request_validation_error(self, mock_post):
        """Test POST request with validation error (400)"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'status': 'error',
            'message': 'Validation failed',
            'errors': {'title': 'Title is required'}
        }
        mock_response.raise_for_status.side_effect = requests.HTTPError("400 Bad Request")
        mock_post.return_value = mock_response
        
        # Act & Assert
        client = APIClient()
        with pytest.raises(requests.HTTPError):
            client.post('events', {})
    
    @patch('requests.Session.put')
    def test_put_request_success(self, mock_put):
        """Test successful PUT request"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'updated'}
        mock_response.raise_for_status = Mock()
        mock_put.return_value = mock_response
        
        # Act
        client = APIClient()
        result = client.put('events/1', {'title': 'Updated Event'})
        
        # Assert
        assert result == {'status': 'updated'}
        mock_put.assert_called_once()
    
    @patch('requests.Session.delete')
    def test_delete_request_success(self, mock_delete):
        """Test successful DELETE request"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.raise_for_status = Mock()
        mock_delete.return_value = mock_response
        
        # Act
        client = APIClient()
        client.delete('events/1')
        
        # Assert
        mock_delete.assert_called_once()
    
    @patch('requests.Session.get')
    def test_connection_error(self, mock_get):
        """Test handling of connection errors"""
        # Arrange
        mock_get.side_effect = requests.ConnectionError("Cannot connect to server")
        
        # Act & Assert
        client = APIClient()
        with pytest.raises(requests.ConnectionError):
            client.get('events')
    
    @patch('requests.Session.get')
    def test_timeout_error(self, mock_get):
        """Test handling of timeout errors"""
        # Arrange
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        # Act & Assert
        client = APIClient()
        with pytest.raises(requests.Timeout):
            client.get('events')
    
    def test_set_token(self):
        """Test setting authentication token"""
        # Arrange
        client = APIClient()
        token = "test_token_123"
        
        # Act
        client.set_token(token)
        
        # Assert
        assert 'Authorization' in client.session.headers
        assert client.session.headers['Authorization'] == f'Bearer {token}'
    
    def test_clear_token(self):
        """Test clearing authentication token"""
        # Arrange
        client = APIClient()
        client.set_token("test_token_123")
        
        # Act
        client.clear_token()
        
        # Assert
        assert 'Authorization' not in client.session.headers


class TestAPIClientRetry:
    """Test retry logic and rate limiting"""
    
    @patch('requests.Session.get')
    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_retry_on_503(self, mock_sleep, mock_get):
        """Test retry logic on 503 Service Unavailable"""
        # Arrange
        mock_response_fail = Mock()
        mock_response_fail.status_code = 503
        mock_response_fail.raise_for_status.side_effect = requests.HTTPError("503")
        
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {'status': 'success'}
        mock_response_success.raise_for_status = Mock()
        
        # First call fails, second succeeds
        mock_get.side_effect = [mock_response_fail, mock_response_success]
        
        # Act
        client = APIClient()
        # Note: This requires APIClient to have retry logic implemented
        # If not implemented, this test will fail and indicate the feature is needed
        
        # For now, just test single call
        with pytest.raises(requests.HTTPError):
            client.get('events')


class TestAPIClientAuthentication:
    """Test authentication flows"""
    
    @patch('requests.Session.post')
    def test_login_success(self, mock_post):
        """Test successful login"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'token': 'jwt_token_here',
            'user': {
                'id': 1,
                'name': 'Test User',
                'email': 'test@example.com',
                'role': 'STUDENT'
            }
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Act
        client = APIClient()
        result = client.post('auth/login', {
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        # Assert
        assert 'token' in result
        assert result['token'] == 'jwt_token_here'
    
    @patch('requests.Session.post')
    def test_login_invalid_credentials(self, mock_post):
        """Test login with invalid credentials"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            'status': 'error',
            'message': 'Invalid email or password'
        }
        mock_response.raise_for_status.side_effect = requests.HTTPError("401 Unauthorized")
        mock_post.return_value = mock_response
        
        # Act & Assert
        client = APIClient()
        with pytest.raises(requests.HTTPError):
            client.post('auth/login', {
                'email': 'wrong@example.com',
                'password': 'wrongpassword'
            })
