import requests
import json
from config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.auth_token = None
        self.timeout = 10  # seconds
    
    def set_auth_token(self, token):
        """Set the Authorization header for all requests"""
        self.auth_token = token
    
    def _get_headers(self, headers=None):
        """Get headers including auth token if set"""
        default_headers = {'Content-Type': 'application/json'}
        if self.auth_token:
            default_headers['Authorization'] = f'Bearer {self.auth_token}'
        if headers:
            default_headers.update(headers)
        return default_headers
    
    def get(self, endpoint, headers=None):
        """Make a GET request to the API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.get(
                url, 
                headers=self._get_headers(headers), 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise requests.Timeout(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise requests.ConnectionError("Failed to connect to the server")
        except requests.HTTPError as e:
            raise requests.HTTPError(f"HTTP error: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            raise requests.RequestException(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from server")
    
    def post(self, endpoint, data, headers=None):
        """Make a POST request with JSON data"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.post(
                url, 
                json=data, 
                headers=self._get_headers(headers), 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise requests.Timeout(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise requests.ConnectionError("Failed to connect to the server")
        except requests.HTTPError as e:
            raise requests.HTTPError(f"HTTP error: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            raise requests.RequestException(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from server")
    
    def put(self, endpoint, data, headers=None):
        """Make a PUT request with JSON data"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.put(
                url, 
                json=data, 
                headers=self._get_headers(headers), 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise requests.Timeout(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise requests.ConnectionError("Failed to connect to the server")
        except requests.HTTPError as e:
            raise requests.HTTPError(f"HTTP error: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            raise requests.RequestException(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from server")
    
    def delete(self, endpoint, headers=None):
        """Make a DELETE request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.delete(
                url, 
                headers=self._get_headers(headers), 
                timeout=self.timeout
            )
            response.raise_for_status()
            # DELETE might not return JSON, so handle gracefully
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"message": "Deleted successfully"}
        except requests.Timeout:
            raise requests.Timeout(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise requests.ConnectionError("Failed to connect to the server")
        except requests.HTTPError as e:
            raise requests.HTTPError(f"HTTP error: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            raise requests.RequestException(f"Request failed: {str(e)}")