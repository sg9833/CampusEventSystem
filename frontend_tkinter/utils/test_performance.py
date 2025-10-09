"""
Test Suite for Performance Optimization System
Tests caching, pagination, debouncing, throttling, etc.
"""

import unittest
import time
import threading
from utils.performance import (
    Cache, Paginator, Debouncer, Throttler,
    LazyLoader, PerformanceMonitor,
    cached, debounced, throttled
)


class TestCache(unittest.TestCase):
    """Test caching functionality"""
    
    def setUp(self):
        """Create cache instance for testing"""
        self.cache = Cache(default_ttl=2, max_size=5)
    
    def test_set_get(self):
        """Test basic set and get operations"""
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")
    
    def test_expiry(self):
        """Test cache expiry"""
        self.cache.set("key2", "value2", ttl=1)
        self.assertEqual(self.cache.get("key2"), "value2")
        
        # Wait for expiry
        time.sleep(1.1)
        
        # Should be expired
        self.assertIsNone(self.cache.get("key2"))
    
    def test_invalidate(self):
        """Test cache invalidation"""
        self.cache.set("key3", "value3")
        self.assertEqual(self.cache.get("key3"), "value3")
        
        self.cache.invalidate("key3")
        self.assertIsNone(self.cache.get("key3"))
    
    def test_invalidate_pattern(self):
        """Test pattern-based invalidation"""
        self.cache.set("events:1", "event1")
        self.cache.set("events:2", "event2")
        self.cache.set("users:1", "user1")
        
        self.cache.invalidate_pattern("events")
        
        # Events should be cleared
        self.assertIsNone(self.cache.get("events:1"))
        self.assertIsNone(self.cache.get("events:2"))
        
        # Users should remain
        self.assertEqual(self.cache.get("users:1"), "user1")
    
    def test_max_size(self):
        """Test cache size limit"""
        for i in range(10):
            self.cache.set(f"key{i}", f"value{i}")
        
        # Should only have 5 entries (max_size)
        stats = self.cache.get_stats()
        self.assertEqual(stats['total_entries'], 5)
    
    def test_cleanup_expired(self):
        """Test cleanup of expired entries"""
        self.cache.set("temp1", "value1", ttl=1)
        self.cache.set("temp2", "value2", ttl=1)
        self.cache.set("perm", "value3", ttl=100)
        
        # Wait for expiry
        time.sleep(1.1)
        
        # Cleanup
        self.cache.cleanup_expired()
        
        stats = self.cache.get_stats()
        self.assertEqual(stats['valid_entries'], 1)
    
    def test_thread_safety(self):
        """Test thread-safe operations"""
        def writer(key, value):
            self.cache.set(key, value)
        
        threads = []
        for i in range(10):
            t = threading.Thread(target=writer, args=(f"key{i}", f"value{i}"))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Should have entries
        stats = self.cache.get_stats()
        self.assertGreater(stats['total_entries'], 0)


class TestPaginator(unittest.TestCase):
    """Test pagination functionality"""
    
    def setUp(self):
        """Create paginator instance"""
        self.paginator = Paginator(items_per_page=10)
        self.paginator.set_total(50)  # 50 items = 5 pages
    
    def test_total_pages(self):
        """Test total pages calculation"""
        self.assertEqual(self.paginator.total_pages, 5)
    
    def test_first_page(self):
        """Test first page data"""
        page_data = self.paginator.get_page_data(1)
        
        self.assertEqual(page_data['page'], 1)
        self.assertEqual(page_data['offset'], 0)
        self.assertTrue(page_data['is_first_page'])
        self.assertFalse(page_data['is_last_page'])
        self.assertFalse(page_data['has_previous'])
        self.assertTrue(page_data['has_next'])
    
    def test_middle_page(self):
        """Test middle page data"""
        page_data = self.paginator.get_page_data(3)
        
        self.assertEqual(page_data['page'], 3)
        self.assertEqual(page_data['offset'], 20)
        self.assertFalse(page_data['is_first_page'])
        self.assertFalse(page_data['is_last_page'])
        self.assertTrue(page_data['has_previous'])
        self.assertTrue(page_data['has_next'])
    
    def test_last_page(self):
        """Test last page data"""
        page_data = self.paginator.get_page_data(5)
        
        self.assertEqual(page_data['page'], 5)
        self.assertEqual(page_data['offset'], 40)
        self.assertFalse(page_data['is_first_page'])
        self.assertTrue(page_data['is_last_page'])
        self.assertTrue(page_data['has_previous'])
        self.assertFalse(page_data['has_next'])
    
    def test_navigation(self):
        """Test page navigation"""
        # Start at page 1
        self.paginator.get_page_data(1)
        
        # Next page
        next_page = self.paginator.next_page()
        self.assertEqual(next_page['page'], 2)
        
        # Next again
        next_page = self.paginator.next_page()
        self.assertEqual(next_page['page'], 3)
        
        # Previous
        prev_page = self.paginator.previous_page()
        self.assertEqual(prev_page['page'], 2)
    
    def test_start_end_index(self):
        """Test start and end index calculation"""
        page_data = self.paginator.get_page_data(1)
        self.assertEqual(page_data['start_index'], 1)
        self.assertEqual(page_data['end_index'], 10)
        
        page_data = self.paginator.get_page_data(5)
        self.assertEqual(page_data['start_index'], 41)
        self.assertEqual(page_data['end_index'], 50)


class TestDebouncer(unittest.TestCase):
    """Test debouncing functionality"""
    
    def setUp(self):
        """Create debouncer instance"""
        self.debouncer = Debouncer(wait_ms=200)
        self.call_count = 0
    
    def test_single_call(self):
        """Test single debounced call"""
        def callback():
            self.call_count += 1
        
        self.debouncer.debounce(callback)
        
        # Wait for execution
        time.sleep(0.3)
        
        # Should have been called once
        self.assertEqual(self.call_count, 1)
    
    def test_multiple_calls_debounced(self):
        """Test multiple rapid calls are debounced"""
        def callback():
            self.call_count += 1
        
        # Make 5 rapid calls
        for _ in range(5):
            self.debouncer.debounce(callback)
            time.sleep(0.05)  # 50ms between calls
        
        # Wait for execution
        time.sleep(0.3)
        
        # Should only execute once (last call)
        self.assertEqual(self.call_count, 1)
    
    def test_cancel(self):
        """Test canceling debounced call"""
        def callback():
            self.call_count += 1
        
        self.debouncer.debounce(callback)
        self.debouncer.cancel()
        
        # Wait
        time.sleep(0.3)
        
        # Should not have been called
        self.assertEqual(self.call_count, 0)


class TestThrottler(unittest.TestCase):
    """Test throttling functionality"""
    
    def setUp(self):
        """Create throttler instance"""
        self.throttler = Throttler(wait_ms=200)
        self.call_count = 0
    
    def test_first_call_immediate(self):
        """Test first call executes immediately"""
        def callback():
            self.call_count += 1
        
        result = self.throttler.throttle(callback)
        
        # Should execute and return True
        self.assertTrue(result)
        self.assertEqual(self.call_count, 1)
    
    def test_rapid_calls_throttled(self):
        """Test rapid calls are throttled"""
        def callback():
            self.call_count += 1
        
        # First call should execute
        self.assertTrue(self.throttler.throttle(callback))
        
        # Immediate second call should be blocked
        self.assertFalse(self.throttler.throttle(callback))
        
        # Should only have executed once
        self.assertEqual(self.call_count, 1)
    
    def test_call_after_cooldown(self):
        """Test call after cooldown period"""
        def callback():
            self.call_count += 1
        
        # First call
        self.throttler.throttle(callback)
        
        # Wait for cooldown
        time.sleep(0.25)
        
        # Second call should execute
        self.assertTrue(self.throttler.throttle(callback))
        self.assertEqual(self.call_count, 2)


class TestLazyLoader(unittest.TestCase):
    """Test lazy loading functionality"""
    
    def setUp(self):
        """Create lazy loader instance"""
        self.loader = LazyLoader()
    
    def test_load_page_once(self):
        """Test page is loaded only once"""
        class TestPage:
            def __init__(self, name):
                self.name = name
        
        # Load page twice
        page1 = self.loader.load_page("test", TestPage, "Page1")
        page2 = self.loader.load_page("test", TestPage, "Page1")
        
        # Should be same instance
        self.assertIs(page1, page2)
    
    def test_unload_page(self):
        """Test unloading page"""
        class TestPage:
            def __init__(self):
                pass
            
            def cleanup(self):
                pass
        
        # Load page
        page = self.loader.load_page("test", TestPage)
        
        # Unload
        self.loader.unload_page("test")
        
        # Load again should create new instance
        page2 = self.loader.load_page("test", TestPage)
        self.assertIsNot(page, page2)
    
    def test_get_loaded_pages(self):
        """Test getting list of loaded pages"""
        class TestPage:
            pass
        
        self.loader.load_page("page1", TestPage)
        self.loader.load_page("page2", TestPage)
        
        loaded = self.loader.get_loaded_pages()
        
        self.assertIn("page1", loaded)
        self.assertIn("page2", loaded)


class TestPerformanceMonitor(unittest.TestCase):
    """Test performance monitoring"""
    
    def setUp(self):
        """Create performance monitor"""
        self.monitor = PerformanceMonitor()
    
    def test_record_metric(self):
        """Test recording metrics"""
        self.monitor.record("api_call", 100.5)
        self.monitor.record("api_call", 150.2)
        self.monitor.record("api_call", 120.8)
        
        stats = self.monitor.get_stats("api_call")
        
        self.assertEqual(stats['count'], 3)
        self.assertEqual(stats['min'], 100.5)
        self.assertEqual(stats['max'], 150.2)
        self.assertAlmostEqual(stats['avg'], 123.83, places=1)
    
    def test_multiple_metrics(self):
        """Test multiple different metrics"""
        self.monitor.record("api_call", 100)
        self.monitor.record("page_load", 200)
        
        all_stats = self.monitor.get_all_stats()
        
        self.assertIn("api_call", all_stats)
        self.assertIn("page_load", all_stats)
    
    def test_clear(self):
        """Test clearing metrics"""
        self.monitor.record("test", 100)
        self.monitor.clear()
        
        stats = self.monitor.get_stats("test")
        self.assertIsNone(stats)


class TestDecorators(unittest.TestCase):
    """Test decorator functions"""
    
    def test_cached_decorator(self):
        """Test @cached decorator"""
        call_count = [0]
        
        @cached(ttl=2, key_prefix="test")
        def expensive_function(x):
            call_count[0] += 1
            return x * 2
        
        # First call
        result1 = expensive_function(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count[0], 1)
        
        # Second call (should use cache)
        result2 = expensive_function(5)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count[0], 1)  # Not called again
    
    def test_debounced_decorator(self):
        """Test @debounced decorator"""
        call_count = [0]
        
        @debounced(wait_ms=100)
        def debounced_func():
            call_count[0] += 1
        
        # Multiple calls
        for _ in range(5):
            debounced_func()
        
        # Wait for execution
        time.sleep(0.2)
        
        # Should only execute once
        self.assertEqual(call_count[0], 1)
    
    def test_throttled_decorator(self):
        """Test @throttled decorator"""
        call_count = [0]
        
        @throttled(wait_ms=100)
        def throttled_func():
            call_count[0] += 1
            return True
        
        # First call should execute
        result1 = throttled_func()
        self.assertTrue(result1)
        self.assertEqual(call_count[0], 1)
        
        # Immediate second call should be blocked
        result2 = throttled_func()
        self.assertFalse(result2)
        self.assertEqual(call_count[0], 1)


def run_tests():
    """Run all performance tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCache))
    suite.addTests(loader.loadTestsFromTestCase(TestPaginator))
    suite.addTests(loader.loadTestsFromTestCase(TestDebouncer))
    suite.addTests(loader.loadTestsFromTestCase(TestThrottler))
    suite.addTests(loader.loadTestsFromTestCase(TestLazyLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestDecorators))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("PERFORMANCE TEST SUMMARY")
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
