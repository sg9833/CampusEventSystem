"""
Performance Optimization Utilities
Provides caching, lazy loading, debouncing, and pagination support
"""

import time
import threading
from typing import Any, Callable, Dict, Optional, List, Tuple
from datetime import datetime, timedelta
from functools import wraps
import json


class Cache:
    """
    Thread-safe cache with TTL (Time To Live) support
    
    Features:
    - Automatic expiry based on TTL
    - Thread-safe operations
    - Cache invalidation
    - Size limits
    """
    
    def __init__(self, default_ttl: int = 300, max_size: int = 100):
        """
        Initialize cache
        
        Args:
            default_ttl: Default time to live in seconds (default: 5 minutes)
            max_size: Maximum number of cached items
        """
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
        self._lock = threading.Lock()
        self.default_ttl = default_ttl
        self.max_size = max_size
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            value, expiry = self._cache[key]
            
            # Check if expired
            if datetime.now() > expiry:
                del self._cache[key]
                return None
            
            return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses default if None)
        """
        with self._lock:
            # Check size limit
            if len(self._cache) >= self.max_size and key not in self._cache:
                # Remove oldest entry
                oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
                del self._cache[oldest_key]
            
            ttl = ttl or self.default_ttl
            expiry = datetime.now() + timedelta(seconds=ttl)
            self._cache[key] = (value, expiry)
    
    def invalidate(self, key: str):
        """
        Invalidate (remove) cache entry
        
        Args:
            key: Cache key to invalidate
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def invalidate_pattern(self, pattern: str):
        """
        Invalidate all keys matching pattern
        
        Args:
            pattern: Pattern to match (simple substring match)
        """
        with self._lock:
            keys_to_remove = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_remove:
                del self._cache[key]
    
    def clear(self):
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()
    
    def cleanup_expired(self):
        """Remove all expired entries"""
        with self._lock:
            now = datetime.now()
            expired_keys = [k for k, (_, expiry) in self._cache.items() if now > expiry]
            for key in expired_keys:
                del self._cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        with self._lock:
            total = len(self._cache)
            now = datetime.now()
            expired = sum(1 for _, expiry in self._cache.values() if now > expiry)
            
            return {
                "total_entries": total,
                "expired_entries": expired,
                "valid_entries": total - expired,
                "max_size": self.max_size,
                "usage_percent": (total / self.max_size * 100) if self.max_size > 0 else 0
            }


class Debouncer:
    """
    Debounce function calls
    
    Delays execution until after wait time has elapsed since last call.
    Useful for search inputs, resize events, etc.
    """
    
    def __init__(self, wait_ms: int = 500):
        """
        Initialize debouncer
        
        Args:
            wait_ms: Wait time in milliseconds
        """
        self.wait_ms = wait_ms
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()
    
    def debounce(self, func: Callable, *args, **kwargs):
        """
        Debounce function call
        
        Args:
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
        """
        with self._lock:
            # Cancel previous timer
            if self._timer is not None:
                self._timer.cancel()
            
            # Create new timer
            self._timer = threading.Timer(
                self.wait_ms / 1000.0,
                func,
                args=args,
                kwargs=kwargs
            )
            self._timer.start()
    
    def cancel(self):
        """Cancel pending debounced call"""
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None


class Throttler:
    """
    Throttle function calls
    
    Ensures function is called at most once per time period.
    Different from debounce - executes immediately, then blocks subsequent calls.
    """
    
    def __init__(self, wait_ms: int = 1000):
        """
        Initialize throttler
        
        Args:
            wait_ms: Minimum time between calls in milliseconds
        """
        self.wait_ms = wait_ms
        self._last_call: float = 0
        self._lock = threading.Lock()
    
    def throttle(self, func: Callable, *args, **kwargs) -> bool:
        """
        Throttle function call
        
        Args:
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
        
        Returns:
            True if function was called, False if throttled
        """
        with self._lock:
            now = time.time()
            elapsed = (now - self._last_call) * 1000  # Convert to ms
            
            if elapsed >= self.wait_ms:
                self._last_call = now
                func(*args, **kwargs)
                return True
            
            return False


class Paginator:
    """
    Pagination helper for large datasets
    
    Features:
    - Page-based navigation
    - "Load more" support
    - Total count tracking
    """
    
    def __init__(self, items_per_page: int = 20):
        """
        Initialize paginator
        
        Args:
            items_per_page: Number of items per page
        """
        self.items_per_page = items_per_page
        self.current_page = 1
        self.total_items = 0
        self.total_pages = 0
    
    def set_total(self, total: int):
        """
        Set total number of items
        
        Args:
            total: Total item count
        """
        self.total_items = total
        self.total_pages = (total + self.items_per_page - 1) // self.items_per_page
    
    def get_page_data(self, page: int) -> Dict[str, Any]:
        """
        Get pagination data for specific page
        
        Args:
            page: Page number (1-indexed)
        
        Returns:
            Dictionary with pagination info
        """
        page = max(1, min(page, self.total_pages))
        self.current_page = page
        
        offset = (page - 1) * self.items_per_page
        
        return {
            "page": page,
            "limit": self.items_per_page,
            "offset": offset,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "has_previous": page > 1,
            "has_next": page < self.total_pages,
            "is_first_page": page == 1,
            "is_last_page": page == self.total_pages,
            "start_index": offset + 1 if self.total_items > 0 else 0,
            "end_index": min(offset + self.items_per_page, self.total_items)
        }
    
    def next_page(self) -> Optional[Dict[str, Any]]:
        """
        Get next page data
        
        Returns:
            Pagination data or None if on last page
        """
        if self.current_page < self.total_pages:
            return self.get_page_data(self.current_page + 1)
        return None
    
    def previous_page(self) -> Optional[Dict[str, Any]]:
        """
        Get previous page data
        
        Returns:
            Pagination data or None if on first page
        """
        if self.current_page > 1:
            return self.get_page_data(self.current_page - 1)
        return None
    
    def first_page(self) -> Dict[str, Any]:
        """Get first page data"""
        return self.get_page_data(1)
    
    def last_page(self) -> Dict[str, Any]:
        """Get last page data"""
        return self.get_page_data(self.total_pages)


class LazyLoader:
    """
    Lazy loading helper for deferred imports and page loading
    
    Features:
    - Deferred module imports
    - Page loading only when needed
    - Thread-safe loading
    """
    
    def __init__(self):
        self._loaded_modules: Dict[str, Any] = {}
        self._loaded_pages: Dict[str, Any] = {}
        self._lock = threading.Lock()
    
    def load_module(self, module_name: str, import_path: str) -> Any:
        """
        Lazy load module
        
        Args:
            module_name: Name for caching
            import_path: Python import path
        
        Returns:
            Loaded module
        """
        with self._lock:
            if module_name in self._loaded_modules:
                return self._loaded_modules[module_name]
            
            # Import module
            module = __import__(import_path, fromlist=[''])
            self._loaded_modules[module_name] = module
            return module
    
    def load_page(self, page_name: str, page_class: type, *args, **kwargs) -> Any:
        """
        Lazy load page instance
        
        Args:
            page_name: Name for caching
            page_class: Page class to instantiate
            *args: Constructor arguments
            **kwargs: Constructor keyword arguments
        
        Returns:
            Page instance
        """
        with self._lock:
            if page_name in self._loaded_pages:
                return self._loaded_pages[page_name]
            
            # Create page instance
            page = page_class(*args, **kwargs)
            self._loaded_pages[page_name] = page
            return page
    
    def unload_page(self, page_name: str):
        """
        Unload page from cache
        
        Args:
            page_name: Page to unload
        """
        with self._lock:
            if page_name in self._loaded_pages:
                # Call cleanup if available
                page = self._loaded_pages[page_name]
                if hasattr(page, 'cleanup'):
                    page.cleanup()
                del self._loaded_pages[page_name]
    
    def get_loaded_pages(self) -> List[str]:
        """
        Get list of loaded page names
        
        Returns:
            List of page names
        """
        with self._lock:
            return list(self._loaded_pages.keys())


class AsyncImageLoader:
    """
    Asynchronous image loader for Tkinter
    
    Loads images in background thread to prevent UI blocking
    """
    
    def __init__(self):
        self._loading_queue: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False
    
    def load_async(self, image_path: str, callback: Callable, size: Optional[Tuple[int, int]] = None):
        """
        Load image asynchronously
        
        Args:
            image_path: Path to image file
            callback: Function to call with loaded image
            size: Optional (width, height) to resize
        """
        with self._lock:
            self._loading_queue.append({
                "path": image_path,
                "callback": callback,
                "size": size
            })
            
            # Start worker if not running
            if not self._running:
                self._start_worker()
    
    def _start_worker(self):
        """Start background worker thread"""
        self._running = True
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()
    
    def _worker(self):
        """Background worker that loads images"""
        from PIL import Image, ImageTk
        
        while True:
            with self._lock:
                if not self._loading_queue:
                    self._running = False
                    break
                
                task = self._loading_queue.pop(0)
            
            try:
                # Load image
                image = Image.open(task["path"])
                
                # Resize if requested
                if task["size"]:
                    image = image.resize(task["size"], Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Call callback with loaded image
                task["callback"](photo)
                
            except Exception as e:
                print(f"Error loading image {task['path']}: {e}")
                # Call callback with None to indicate error
                task["callback"](None)
    
    def cancel_all(self):
        """Cancel all pending image loads"""
        with self._lock:
            self._loading_queue.clear()


# Global instances
_global_cache = Cache()
_global_lazy_loader = LazyLoader()
_global_image_loader = AsyncImageLoader()


def get_cache() -> Cache:
    """Get global cache instance"""
    return _global_cache


def get_lazy_loader() -> LazyLoader:
    """Get global lazy loader instance"""
    return _global_lazy_loader


def get_image_loader() -> AsyncImageLoader:
    """Get global async image loader instance"""
    return _global_image_loader


# Decorators

def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Decorator for caching function results
    
    Args:
        ttl: Time to live in seconds
        key_prefix: Prefix for cache key
    
    Example:
        @cached(ttl=300, key_prefix="events")
        def get_events(user_id):
            return api.get(f"events?user_id={user_id}")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]
            
            # Add positional args
            for arg in args:
                key_parts.append(str(arg))
            
            # Add keyword args (sorted for consistency)
            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}={v}")
            
            cache_key = ":".join(key_parts)
            
            # Check cache
            cache = get_cache()
            cached_value = cache.get(cache_key)
            
            if cached_value is not None:
                return cached_value
            
            # Call function
            result = func(*args, **kwargs)
            
            # Cache result
            cache.set(cache_key, result, ttl=ttl)
            
            return result
        
        return wrapper
    
    return decorator


def debounced(wait_ms: int = 500):
    """
    Decorator for debouncing function calls
    
    Args:
        wait_ms: Wait time in milliseconds
    
    Example:
        @debounced(wait_ms=500)
        def on_search(query):
            results = search_api(query)
    """
    def decorator(func: Callable) -> Callable:
        debouncer = Debouncer(wait_ms)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            debouncer.debounce(func, *args, **kwargs)
        
        return wrapper
    
    return decorator


def throttled(wait_ms: int = 1000):
    """
    Decorator for throttling function calls
    
    Args:
        wait_ms: Minimum time between calls in milliseconds
    
    Example:
        @throttled(wait_ms=1000)
        def on_button_click():
            submit_form()
    """
    def decorator(func: Callable) -> Callable:
        throttler = Throttler(wait_ms)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return throttler.throttle(func, *args, **kwargs)
        
        return wrapper
    
    return decorator


class PerformanceMonitor:
    """
    Monitor and log performance metrics
    
    Features:
    - Function execution time tracking
    - API call duration logging
    - Memory usage tracking (basic)
    """
    
    def __init__(self):
        self._metrics: Dict[str, List[float]] = {}
        self._lock = threading.Lock()
    
    def record(self, metric_name: str, value: float):
        """
        Record metric value
        
        Args:
            metric_name: Name of metric
            value: Metric value
        """
        with self._lock:
            if metric_name not in self._metrics:
                self._metrics[metric_name] = []
            self._metrics[metric_name].append(value)
            
            # Keep only last 100 values
            if len(self._metrics[metric_name]) > 100:
                self._metrics[metric_name].pop(0)
    
    def get_stats(self, metric_name: str) -> Optional[Dict[str, float]]:
        """
        Get statistics for metric
        
        Args:
            metric_name: Name of metric
        
        Returns:
            Dictionary with min, max, avg, count
        """
        with self._lock:
            if metric_name not in self._metrics or not self._metrics[metric_name]:
                return None
            
            values = self._metrics[metric_name]
            return {
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values),
                "count": len(values),
                "total": sum(values)
            }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """
        Get statistics for all metrics
        
        Returns:
            Dictionary of metric stats
        """
        with self._lock:
            return {
                name: self.get_stats(name)
                for name in self._metrics.keys()
            }
    
    def clear(self):
        """Clear all metrics"""
        with self._lock:
            self._metrics.clear()


def timed(metric_name: Optional[str] = None, monitor: Optional[PerformanceMonitor] = None):
    """
    Decorator for timing function execution
    
    Args:
        metric_name: Name for metric (uses function name if None)
        monitor: PerformanceMonitor instance
    
    Example:
        @timed("api_call")
        def fetch_data():
            return api.get("data")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = (time.time() - start_time) * 1000  # Convert to ms
            
            name = metric_name or func.__name__
            
            if monitor:
                monitor.record(name, elapsed)
            
            print(f"[PERF] {name}: {elapsed:.2f}ms")
            
            return result
        
        return wrapper
    
    return decorator


# Global performance monitor
_global_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance"""
    return _global_monitor
