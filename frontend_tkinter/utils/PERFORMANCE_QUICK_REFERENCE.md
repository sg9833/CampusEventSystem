# Performance Optimization Quick Reference

## 🚀 Quick Implementation Checklist

### ✅ For Every Page with API Calls

1. **Lazy Loading** - Load only when shown
```python
def load_page(self):
    if not self.loaded:
        self.create_ui()
        self.load_data()
        self.loaded = True
```

2. **Async API Calls** - Don't block UI
```python
api.async_get(endpoint, on_success=callback, cache=True)
```

3. **Loading Indicator** - Show feedback
```python
overlay = show_loading(self, "Loading...")
# ... operation ...
overlay.hide()
```

4. **Cache Invalidation** - Clear after updates
```python
api.invalidate_cache("events")
```

---

## 📦 Import Statements

```python
# Performance utilities
from utils.performance import (
    get_cache, Paginator, Debouncer, Throttler,
    get_lazy_loader, cached, debounced, throttled
)

# Loading indicators
from utils.loading_indicators import (
    LoadingSpinner, ProgressBar, SkeletonScreen,
    PaginationControls, SearchBar, show_loading
)

# Enhanced API client
from utils.api_client import APIClient
```

---

## 🎯 Common Patterns

### Pattern 1: Cached API Call with Loading
```python
overlay = show_loading(self, "Loading events...")

def on_success(data):
    overlay.hide()
    self.display_data(data)

def on_error(error):
    overlay.hide()
    messagebox.showerror("Error", str(error))

api.async_get("events", on_success=on_success, on_error=on_error, cache=True)
```

### Pattern 2: Paginated List
```python
# Setup
self.paginator = Paginator(items_per_page=20)
self.pagination_controls = PaginationControls(self, on_page_change=self.load_page)

# Load data
response = api.get_paginated("events", page=page, limit=20, cache=True)
self.paginator.set_total(response['total'])
self.pagination_controls.update_pagination(page, self.paginator.total_pages)
```

### Pattern 3: Debounced Search
```python
self.search_bar = SearchBar(
    self,
    on_search=self.perform_search,
    debounce_ms=500
)

def perform_search(self, query):
    api.async_get(f"events?search={query}", on_success=self.show_results, cache=False)
```

### Pattern 4: Prevent Double-Submit
```python
self.throttler = Throttler(wait_ms=2000)

def on_submit(self):
    if not self.throttler.throttle(self.do_submit):
        messagebox.showwarning("Wait", "Please wait...")

def do_submit(self):
    api.async_post("events", data, on_success=self.on_created)
```

### Pattern 5: Lazy Load Page
```python
class MyPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.loaded = False
    
    def load_page(self):
        if not self.loaded:
            self._create_ui()
            self._load_data()
            self.loaded = True
    
    def cleanup(self):
        # Called when page is unloaded
        self.clear_data()
```

---

## ⚡ Performance Checklist

### Before Deployment

- [ ] All list pages use pagination (20 items/page)
- [ ] All API calls are async (non-blocking)
- [ ] GET requests use caching (5 min TTL)
- [ ] Cache invalidated after POST/PUT/DELETE
- [ ] Search inputs use debouncing (500ms)
- [ ] Submit buttons use throttling (2 sec)
- [ ] Loading indicators shown during operations
- [ ] Pages use lazy loading
- [ ] Images load asynchronously
- [ ] Heavy imports are deferred

### Testing Checklist

- [ ] Page loads in < 500ms (with cache)
- [ ] Search responds in < 500ms (after typing stops)
- [ ] No UI freezing during operations
- [ ] Loading indicators appear/disappear correctly
- [ ] Pagination works correctly
- [ ] Cache invalidates on updates
- [ ] Double-submit prevented
- [ ] Memory doesn't leak (check after navigation)

---

## 🔧 Configuration

### Cache Settings
```python
from utils.performance import Cache

cache = Cache(
    default_ttl=300,  # 5 minutes
    max_size=100      # Max 100 entries
)
```

### Debounce Timing
```python
# Search: 500ms
SearchBar(on_search=callback, debounce_ms=500)

# Autocomplete: 300ms
Debouncer(wait_ms=300)

# Resize: 200ms
Debouncer(wait_ms=200)
```

### Throttle Timing
```python
# Submit buttons: 2000ms
Throttler(wait_ms=2000)

# Click actions: 1000ms
Throttler(wait_ms=1000)
```

### Pagination
```python
Paginator(items_per_page=20)  # 20 for lists
Paginator(items_per_page=50)  # 50 for tables
```

---

## 📊 Monitoring

### Check Cache Stats
```python
from utils.performance import get_cache

cache = get_cache()
stats = cache.get_stats()
print(f"Cache entries: {stats['valid_entries']}/{stats['max_size']}")
print(f"Usage: {stats['usage_percent']:.1f}%")
```

### Track API Performance
```python
from utils.performance import timed, get_performance_monitor

monitor = get_performance_monitor()

@timed("api_call", monitor=monitor)
def call_api():
    return api.get("events")

# Get stats
stats = monitor.get_stats("api_call")
print(f"Avg: {stats['avg']:.2f}ms")
```

### Monitor Page Load
```python
import time

start = time.time()
page.load_page()
print(f"Loaded in {(time.time() - start) * 1000:.2f}ms")
```

---

## 🐛 Common Issues

### Issue: Cache Not Clearing
```python
# Solution: Invalidate with pattern
api.invalidate_cache("events")  # Clears all event caches
```

### Issue: Loading Indicator Stuck
```python
# Solution: Use try/finally
overlay = show_loading(self, "Loading...")
try:
    data = api.get("events")
finally:
    overlay.hide()
```

### Issue: Search Too Slow
```python
# Solution: Increase debounce delay
SearchBar(on_search=callback, debounce_ms=800)  # 800ms instead of 500ms
```

### Issue: Memory Growing
```python
# Solution: Implement cleanup
def cleanup(self):
    self.debouncer.cancel()
    self.data.clear()
    self.cache.clear()
```

---

## 📱 Mobile/Responsive Tips

1. **Use smaller page sizes on mobile**
```python
# Detect screen size
if screen_width < 800:
    Paginator(items_per_page=10)  # Fewer items on small screens
```

2. **Adjust debounce for touch**
```python
# Longer delay for touch keyboards
SearchBar(on_search=callback, debounce_ms=700)
```

3. **Show progress for slow connections**
```python
# Use progress bar instead of spinner
progress = ProgressBar(self)
progress.set_progress(0.5, "Loading... 50%")
```

---

## 🎨 UI/UX Guidelines

### Loading States

| Duration | Indicator |
|----------|-----------|
| < 300ms  | No indicator (feels instant) |
| 300ms-2s | Spinner |
| 2s-10s   | Skeleton screen or Progress bar |
| > 10s    | Progress bar with percentage |

### Debounce Times

| Action | Delay |
|--------|-------|
| Search | 500ms |
| Autocomplete | 300ms |
| Filters | 500ms |
| Resize | 200ms |

### Throttle Times

| Action | Cooldown |
|--------|----------|
| Submit | 2000ms |
| API calls | 1000ms |
| Clicks | 500ms |

---

## 🔗 Related Files

- `utils/performance.py` - Core utilities
- `utils/loading_indicators.py` - UI components
- `utils/api_client.py` - Enhanced API client
- `pages/optimized_events_example.py` - Full example
- `utils/PERFORMANCE_README.md` - Full documentation

---

## 📝 Code Templates

### Template 1: New Optimized Page
```python
import tkinter as tk
from utils.performance import Paginator, Debouncer
from utils.loading_indicators import SearchBar, PaginationControls, show_loading
from utils.api_client import APIClient

class MyPage(tk.Frame):
    def __init__(self, parent, navigate=None):
        super().__init__(parent, bg="white")
        self.api = APIClient()
        self.navigate = navigate
        self.loaded = False
        self.paginator = Paginator(items_per_page=20)
    
    def load_page(self):
        if not self.loaded:
            self._create_ui()
            self._load_data()
            self.loaded = True
    
    def _create_ui(self):
        # Header
        # Search bar
        # Content area
        # Pagination
        pass
    
    def _load_data(self, page=1):
        overlay = show_loading(self, "Loading...")
        
        def on_success(response):
            overlay.hide()
            self.display_data(response['data'])
            self.paginator.set_total(response['total'])
        
        def on_error(error):
            overlay.hide()
            messagebox.showerror("Error", str(error))
        
        self.api.async_get(
            endpoint=f"data?page={page}&limit=20",
            on_success=on_success,
            on_error=on_error,
            cache=True
        )
    
    def cleanup(self):
        pass
```

### Template 2: Form with Validation
```python
from utils.performance import Throttler
from utils.loading_indicators import show_loading

class MyForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.throttler = Throttler(wait_ms=2000)
        self._create_form()
    
    def _create_form(self):
        # Form fields
        submit_btn = tk.Button(self, text="Submit", command=self._on_submit)
    
    def _on_submit(self):
        if not self.throttler.throttle(self._do_submit):
            messagebox.showwarning("Wait", "Please wait...")
            return
    
    def _do_submit(self):
        if not self._validate():
            return
        
        overlay = show_loading(self, "Submitting...")
        
        def on_success(response):
            overlay.hide()
            messagebox.showinfo("Success", "Saved!")
            self.api.invalidate_cache("data")
        
        def on_error(error):
            overlay.hide()
            messagebox.showerror("Error", str(error))
        
        self.api.async_post(
            endpoint="data",
            data=self._get_form_data(),
            on_success=on_success,
            on_error=on_error
        )
    
    def _validate(self):
        # Validation logic
        return True
    
    def _get_form_data(self):
        return {}
```

---

## 🎓 Learning Path

1. **Start with caching** - Add `cache=True` to GET requests
2. **Add loading indicators** - Use `show_loading()` wrapper
3. **Implement pagination** - Use `Paginator` and `PaginationControls`
4. **Add debouncing** - Use `SearchBar` or `Debouncer`
5. **Prevent double-submit** - Use `Throttler`
6. **Enable lazy loading** - Implement `load_page()` pattern
7. **Monitor performance** - Track metrics and optimize

---

## 🏆 Performance Goals

- **Page Load**: < 500ms (cached), < 2s (uncached)
- **API Response**: < 1s
- **Search Response**: < 500ms (after debounce)
- **UI Responsiveness**: No freezing
- **Cache Hit Rate**: > 60%
- **API Call Reduction**: > 50% with caching

---

## ✨ Pro Tips

1. **Always invalidate cache after updates**
2. **Use skeleton screens for first load**
3. **Paginate everything over 30 items**
4. **Debounce all text inputs**
5. **Throttle all submit buttons**
6. **Monitor cache hit rate**
7. **Profile before optimizing**
8. **Lazy load heavy pages**
9. **Async all API calls**
10. **Show feedback immediately**

---

**Remember**: Perceived performance is as important as actual performance!
