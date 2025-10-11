import requests
import json
from typing import Optional, Dict, Any, Callable
import sys
import os

# Import API_BASE_URL from config.py (not the config module directory)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config as config_module
API_BASE_URL = config_module.API_BASE_URL

import threading


class RateLimitError(Exception):
    """Raised when rate limit is exceeded"""
    pass


class APIClient:
    """
    Enhanced API Client with security and performance features
    
    Features:
    - Rate limiting protection
    - Input sanitization
    - Token management
    - Response caching (5 minutes default)
    - Loading state callbacks
    - Pagination support
    """
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.auth_token = None
        self.timeout = 10  # seconds
        self._request_count = {}  # Track requests per user/endpoint
        self._cache = None  # Will be initialized lazily
        self._loading_callbacks = []  # Callbacks to notify of loading state
        self.on_auth_error_callback = None  # Callback for auth errors (401/403)
    
    def set_auth_token(self, token):
        """Set the Authorization header for all requests"""
        self.auth_token = token
    
    def clear_auth_token(self):
        """Clear the authentication token"""
        self.auth_token = None
    
    def set_auth_error_callback(self, callback):
        """Set callback to handle authentication errors (401/403)"""
        self.on_auth_error_callback = callback
    
    def _handle_auth_error(self, status_code: int):
        """Handle authentication/authorization errors"""
        self.clear_auth_token()
        if self.on_auth_error_callback:
            self.on_auth_error_callback(status_code)
    
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
            
            # Handle authentication errors
            if response.status_code in [401, 403]:
                self._handle_auth_error(response.status_code)
            
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise requests.Timeout(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise requests.ConnectionError("Failed to connect to the server")
        except requests.HTTPError as e:
            if 'response' in locals():
                raise requests.HTTPError(f"HTTP error: {response.status_code} - {response.text}")
            else:
                raise requests.HTTPError(f"HTTP error: {str(e)}")
        except requests.RequestException as e:
            raise requests.RequestException(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from server")
    
    def post(self, endpoint, data=None, headers=None):
        """Make a POST request to the API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.post(
                url,
                json=data,
                headers=self._get_headers(headers),
                timeout=self.timeout
            )
            
            # Handle authentication errors
            if response.status_code in [401, 403]:
                self._handle_auth_error(response.status_code)
            
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise requests.Timeout(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise requests.ConnectionError("Failed to connect to the server")
        except requests.HTTPError as e:
            if 'response' in locals():
                raise requests.HTTPError(f"HTTP error: {response.status_code} - {response.text}")
            else:
                raise requests.HTTPError(f"HTTP error: {str(e)}")
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
            
            # Handle authentication errors
            if response.status_code in [401, 403]:
                self._handle_auth_error(response.status_code)
            
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise requests.Timeout(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise requests.ConnectionError("Failed to connect to the server")
        except requests.HTTPError as e:
            if 'response' in locals():
                raise requests.HTTPError(f"HTTP error: {response.status_code} - {response.text}")
            else:
                raise requests.HTTPError(f"HTTP error: {str(e)}")
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
            
            # Handle authentication errors
            if response.status_code in [401, 403]:
                self._handle_auth_error(response.status_code)
            
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
            if 'response' in locals():
                raise requests.HTTPError(f"HTTP error: {response.status_code} - {response.text}")
            else:
                raise requests.HTTPError(f"HTTP error: {str(e)}")
        except requests.RequestException as e:
            raise requests.RequestException(f"Request failed: {str(e)}")
    
    def sanitize_data(self, data: Dict[str, Any], exclude_keys: Optional[list] = None) -> Dict[str, Any]:
        """
        Sanitize request data to prevent injection attacks
        
        Args:
            data: Dictionary to sanitize
            exclude_keys: Keys to skip sanitization (e.g., passwords)
        
        Returns:
            Sanitized dictionary
        """
        try:
            # Import security module only when needed to avoid circular imports
            from utils.security import get_security_manager
            security = get_security_manager()
            return security.sanitize_form_data(data, exclude_keys=exclude_keys or [])
        except ImportError:
            # Fall back to basic sanitization if security module not available
            return data
    
    def check_rate_limit(self, user_id: Optional[str] = None) -> bool:
        """
        Check if request is within rate limit
        
        Args:
            user_id: User identifier for rate limiting
        
        Returns:
            True if allowed, False if rate limit exceeded
        
        Raises:
            RateLimitError: If rate limit is exceeded
        """
        try:
            from utils.security import get_security_manager
            security = get_security_manager()
            
            identifier = user_id or "anonymous"
            if not security.check_rate_limit(identifier):
                remaining = security.get_remaining_requests(identifier)
                raise RateLimitError(
                    f"Rate limit exceeded. Try again later. "
                    f"Remaining requests: {remaining}"
                )
            return True
        except ImportError:
            # No rate limiting if security module not available
            return True
    
    def secure_post(self, endpoint: str, data: Dict[str, Any], user_id: Optional[str] = None, 
                   sanitize: bool = True, exclude_keys: Optional[list] = None, 
                   headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a secure POST request with rate limiting and sanitization
        
        Args:
            endpoint: API endpoint
            data: Request payload
            user_id: User identifier for rate limiting
            sanitize: Whether to sanitize input data
            exclude_keys: Keys to exclude from sanitization (e.g., passwords)
            headers: Additional headers
        
        Returns:
            Response JSON
        
        Raises:
            RateLimitError: If rate limit exceeded
        """
        # Check rate limit
        self.check_rate_limit(user_id)
        
        # Sanitize data if requested
        if sanitize:
            data = self.sanitize_data(data, exclude_keys=exclude_keys)
        
        # Make request
        return self.post(endpoint, data, headers=headers)
    
    def secure_get(self, endpoint: str, user_id: Optional[str] = None, 
                   headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a secure GET request with rate limiting
        
        Args:
            endpoint: API endpoint
            user_id: User identifier for rate limiting
            headers: Additional headers
        
        Returns:
            Response JSON
        
        Raises:
            RateLimitError: If rate limit exceeded
        """
        # Check rate limit
        self.check_rate_limit(user_id)
        
        # Make request
        return self.get(endpoint, headers=headers)
    
    def secure_put(self, endpoint: str, data: Dict[str, Any], user_id: Optional[str] = None,
                   sanitize: bool = True, exclude_keys: Optional[list] = None,
                   headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a secure PUT request with rate limiting and sanitization
        
        Args:
            endpoint: API endpoint
            data: Request payload
            user_id: User identifier for rate limiting
            sanitize: Whether to sanitize input data
            exclude_keys: Keys to exclude from sanitization
            headers: Additional headers
        
        Returns:
            Response JSON
        
        Raises:
            RateLimitError: If rate limit exceeded
        """
        # Check rate limit
        self.check_rate_limit(user_id)
        
        # Sanitize data if requested
        if sanitize:
            data = self.sanitize_data(data, exclude_keys=exclude_keys)
        
        # Make request
        return self.put(endpoint, data, headers=headers)
    
    def secure_delete(self, endpoint: str, user_id: Optional[str] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a secure DELETE request with rate limiting
        
        Args:
            endpoint: API endpoint
            user_id: User identifier for rate limiting
            headers: Additional headers
        
        Returns:
            Response JSON
        
        Raises:
            RateLimitError: If rate limit exceeded
        """
        # Check rate limit
        self.check_rate_limit(user_id)
        
        # Make request
        return self.delete(endpoint, headers=headers)
    
    def _get_cache(self):
        """Get cache instance (lazy initialization)"""
        if self._cache is None:
            try:
                from utils.performance import get_cache
                self._cache = get_cache()
            except ImportError:
                self._cache = None
        return self._cache
    
    def add_loading_callback(self, callback: Callable[[bool], None]):
        """
        Add callback to be notified of loading state changes
        
        Args:
            callback: Function that receives True when loading starts, False when done
        """
        self._loading_callbacks.append(callback)
    
    def _notify_loading(self, is_loading: bool):
        """Notify all callbacks of loading state change"""
        for callback in self._loading_callbacks:
            try:
                callback(is_loading)
            except Exception as e:
                print(f"Error in loading callback: {e}")
    
    def get_cached(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                   ttl: int = 300, user_id: Optional[str] = None,
                   headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make cached GET request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            ttl: Cache time to live in seconds (default: 5 minutes)
            user_id: User identifier for rate limiting
            headers: Additional headers
        
        Returns:
            Response JSON (from cache or API)
        
        Example:
            # Cache events for 5 minutes
            events = api.get_cached("events", ttl=300)
        """
        cache = self._get_cache()
        
        # Generate cache key
        cache_key = f"api:{endpoint}"
        if params:
            cache_key += ":" + json.dumps(params, sort_keys=True)
        
        # Check cache
        if cache:
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                print(f"[CACHE HIT] {endpoint}")
                return cached_value
        
        # Make API call
        print(f"[CACHE MISS] {endpoint}")
        
        # Add params to endpoint if provided
        if params:
            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
            endpoint = f"{endpoint}?{param_str}"
        
        response = self.secure_get(endpoint, user_id=user_id, headers=headers)
        
        # Cache response
        if cache and response:
            cache.set(cache_key, response, ttl=ttl)
        
        return response
    
    def invalidate_cache(self, pattern: str):
        """
        Invalidate cache entries matching pattern
        
        Args:
            pattern: Pattern to match (e.g., "events" invalidates all event caches)
        
        Example:
            # Invalidate all event caches after creating new event
            api.invalidate_cache("events")
        """
        cache = self._get_cache()
        if cache:
            cache.invalidate_pattern(f"api:{pattern}")
            print(f"[CACHE INVALIDATED] {pattern}")
    
    def get_paginated(self, endpoint: str, page: int = 1, limit: int = 20,
                     user_id: Optional[str] = None, cache: bool = True,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make paginated GET request
        
        Args:
            endpoint: API endpoint
            page: Page number (1-indexed)
            limit: Items per page
            user_id: User identifier for rate limiting
            cache: Whether to cache response
            headers: Additional headers
        
        Returns:
            Response JSON with pagination info
        
        Example:
            result = api.get_paginated("events", page=1, limit=20)
            events = result['data']
            total = result['total']
        """
        params = {"page": page, "limit": limit}
        
        # Add params to endpoint
        param_str = f"page={page}&limit={limit}"
        paginated_endpoint = f"{endpoint}?{param_str}" if "?" not in endpoint else f"{endpoint}&{param_str}"
        
        if cache:
            return self.get_cached(paginated_endpoint, ttl=300, user_id=user_id, headers=headers)
        else:
            return self.secure_get(paginated_endpoint, user_id=user_id, headers=headers)
    
    def async_get(self, endpoint: str, on_success: Callable[[Dict[str, Any]], None],
                  on_error: Optional[Callable[[Exception], None]] = None,
                  user_id: Optional[str] = None, cache: bool = True,
                  headers: Optional[Dict[str, str]] = None):
        """
        Make asynchronous GET request (non-blocking)
        
        Args:
            endpoint: API endpoint
            on_success: Callback function for successful response
            on_error: Callback function for errors
            user_id: User identifier for rate limiting
            cache: Whether to use caching
            headers: Additional headers
        
        Example:
            def on_done(data):
                self.display_events(data)
            
            def on_fail(error):
                messagebox.showerror("Error", str(error))
            
            api.async_get("events", on_success=on_done, on_error=on_fail)
        """
        def worker():
            self._notify_loading(True)
            try:
                if cache:
                    result = self.get_cached(endpoint, user_id=user_id, headers=headers)
                else:
                    result = self.secure_get(endpoint, user_id=user_id, headers=headers)
                
                # Call success callback
                on_success(result)
            except Exception as e:
                # Call error callback
                if on_error:
                    on_error(e)
                else:
                    print(f"Error in async GET: {e}")
            finally:
                self._notify_loading(False)
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def async_post(self, endpoint: str, data: Dict[str, Any],
                   on_success: Callable[[Dict[str, Any]], None],
                   on_error: Optional[Callable[[Exception], None]] = None,
                   user_id: Optional[str] = None, sanitize: bool = True,
                   exclude_keys: Optional[list] = None,
                   headers: Optional[Dict[str, str]] = None):
        """
        Make asynchronous POST request (non-blocking)
        
        Args:
            endpoint: API endpoint
            data: Request payload
            on_success: Callback function for successful response
            on_error: Callback function for errors
            user_id: User identifier for rate limiting
            sanitize: Whether to sanitize input
            exclude_keys: Keys to exclude from sanitization
            headers: Additional headers
        
        Example:
            def on_created(response):
                messagebox.showinfo("Success", "Event created!")
            
            api.async_post("events", event_data, on_success=on_created)
        """
        def worker():
            self._notify_loading(True)
            try:
                result = self.secure_post(
                    endpoint, data, user_id=user_id,
                    sanitize=sanitize, exclude_keys=exclude_keys,
                    headers=headers
                )
                
                # Invalidate cache for this endpoint
                self.invalidate_cache(endpoint.split('?')[0].split('/')[0])
                
                # Call success callback
                on_success(result)
            except Exception as e:
                # Call error callback
                if on_error:
                    on_error(e)
                else:
                    print(f"Error in async POST: {e}")
            finally:
                self._notify_loading(False)
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()