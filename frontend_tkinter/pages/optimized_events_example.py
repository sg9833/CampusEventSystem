"""
Example: Optimized Events Page with Performance Features

Demonstrates:
1. Lazy loading - page loads only when navigated to
2. Caching - API responses cached for 5 minutes
3. Loading indicators - spinners and skeleton screens
4. Pagination - 20 items per page with controls
5. Debounced search - 500ms delay
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Optional
import threading

# Performance utilities
from utils.performance import (
    get_cache, Paginator, Debouncer,
    get_lazy_loader, get_performance_monitor
)
from utils.loading_indicators import (
    LoadingSpinner, SkeletonScreen, PaginationControls,
    SearchBar, show_loading
)
from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.security import get_security_manager


class OptimizedEventsPage(tk.Frame):
    """
    Optimized Events Page with all performance features
    
    Features:
    - Lazy loading of page content
    - Cached API responses (5 min TTL)
    - Loading spinner during API calls
    - Skeleton screen for initial load
    - Pagination (20 events per page)
    - Debounced search (500ms delay)
    - Async API calls (non-blocking UI)
    """
    
    def __init__(self, parent, navigate_callback=None):
        """
        Initialize optimized events page
        
        Args:
            parent: Parent widget
            navigate_callback: Function to navigate to other pages
        """
        super().__init__(parent, bg="white")
        
        # Dependencies
        self.api = APIClient()
        self.session = SessionManager()
        self.security = get_security_manager()
        self.cache = get_cache()
        self.navigate = navigate_callback
        
        # State
        self.paginator = Paginator(items_per_page=20)
        self.search_debouncer = Debouncer(wait_ms=500)
        self.current_search_query = ""
        self.events_data: List[Dict[str, Any]] = []
        self.loaded = False
        
        # Performance monitoring
        self.perf_monitor = get_performance_monitor()
        
        # UI will be created lazily
        self.container = None
        self.search_bar = None
        self.events_container = None
        self.pagination_controls = None
        self.skeleton = None
        self.loading_overlay = None
    
    def load_page(self):
        """
        Lazy load page content (called when page is first shown)
        
        This prevents loading heavy UI elements until needed
        """
        if self.loaded:
            return
        
        print("[LAZY LOAD] Loading Events Page...")
        
        # Create UI
        self._create_ui()
        
        # Load initial data
        self._load_events(page=1)
        
        self.loaded = True
    
    def _create_ui(self):
        """Create page UI components"""
        # Main container
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(self.container, bg="#3498db", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="📅 Events",
            font=("Arial", 18, "bold"),
            bg="#3498db",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Add Event button
        add_button = tk.Button(
            header,
            text="+ Add Event",
            command=self._on_add_event,
            bg="white",
            fg="#3498db",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        add_button.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Search bar with debouncing
        search_frame = tk.Frame(self.container, bg="white")
        search_frame.pack(fill=tk.X, padx=20, pady=15)
        
        self.search_bar = SearchBar(
            search_frame,
            on_search=self._on_search,
            placeholder="Search events...",
            debounce_ms=500  # 500ms delay before search
        )
        self.search_bar.pack(fill=tk.X)
        
        # Events container with scrollbar
        canvas_frame = tk.Frame(self.container, bg="white")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        
        self.events_container = tk.Frame(canvas, bg="white")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas_window = canvas.create_window((0, 0), window=self.events_container, anchor=tk.NW)
        
        # Update scroll region when container size changes
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)
        
        self.events_container.bind('<Configure>', on_frame_configure)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Pagination controls
        self.pagination_controls = PaginationControls(
            self.container,
            on_page_change=self._on_page_change
        )
        self.pagination_controls.pack(fill=tk.X, padx=20, pady=20)
        
        # Show skeleton screen initially
        self.skeleton = SkeletonScreen(self.events_container, rows=5)
        self.skeleton.pack(fill=tk.BOTH, expand=True)
    
    def _load_events(self, page: int = 1, use_cache: bool = True):
        """
        Load events from API with caching
        
        Args:
            page: Page number to load
            use_cache: Whether to use cached data
        """
        user = self.session.get_user()
        if not user:
            messagebox.showerror("Error", "Please login first")
            return
        
        # Hide skeleton if present
        if self.skeleton:
            self.skeleton.destroy()
            self.skeleton = None
        
        # Show loading indicator
        self.loading_overlay = show_loading(self.events_container, "Loading events...")
        
        # Prepare API call
        def on_success(response):
            """Handle successful API response"""
            self.loading_overlay.hide()
            
            # Update events data
            self.events_data = response.get('data', [])
            total = response.get('total', 0)
            
            # Update paginator
            self.paginator.set_total(total)
            page_info = self.paginator.get_page_data(page)
            
            # Update pagination controls
            self.pagination_controls.update_pagination(
                current_page=page,
                total_pages=self.paginator.total_pages
            )
            
            # Display events
            self._display_events()
            
            # Refresh session
            self.security.refresh_session()
        
        def on_error(error):
            """Handle API error"""
            self.loading_overlay.hide()
            messagebox.showerror("Error", f"Failed to load events: {error}")
        
        # Make async API call
        endpoint = "events"
        if self.current_search_query:
            endpoint += f"?search={self.current_search_query}"
        
        if use_cache:
            # Use cached GET with 5 minute TTL
            self.api.async_get(
                endpoint=self.api.get_paginated.__name__,  # Use method for cache key
                on_success=on_success,
                on_error=on_error,
                user_id=str(user['user_id']),
                cache=True
            )
            
            # Actually call paginated endpoint
            threading.Thread(
                target=lambda: self._load_events_sync(page, on_success, on_error),
                daemon=True
            ).start()
        else:
            # Force refresh without cache
            self.cache.invalidate_pattern("events")
            threading.Thread(
                target=lambda: self._load_events_sync(page, on_success, on_error),
                daemon=True
            ).start()
    
    def _load_events_sync(self, page: int, on_success, on_error):
        """Synchronous event loading (runs in thread)"""
        try:
            user = self.session.get_user()
            response = self.api.get_paginated(
                endpoint="events",
                page=page,
                limit=20,
                user_id=str(user['user_id']),
                cache=True
            )
            self.after(0, lambda: on_success(response))
        except Exception as e:
            self.after(0, lambda: on_error(e))
    
    def _display_events(self):
        """Display events in UI"""
        # Clear existing events
        for widget in self.events_container.winfo_children():
            widget.destroy()
        
        if not self.events_data:
            # Show empty state
            empty_label = tk.Label(
                self.events_container,
                text="No events found",
                font=("Arial", 14),
                fg="#999",
                bg="white"
            )
            empty_label.pack(pady=50)
            return
        
        # Display each event
        for event in self.events_data:
            self._create_event_card(event)
    
    def _create_event_card(self, event: Dict[str, Any]):
        """
        Create event card widget
        
        Args:
            event: Event data dictionary
        """
        card = tk.Frame(
            self.events_container,
            bg="white",
            relief=tk.SOLID,
            borderwidth=1,
            highlightbackground="#e0e0e0",
            highlightthickness=1
        )
        card.pack(fill=tk.X, pady=10, ipady=15, ipadx=15)
        
        # Event title
        title = tk.Label(
            card,
            text=event.get('title', 'Untitled Event'),
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#333",
            anchor=tk.W
        )
        title.pack(fill=tk.X, pady=(0, 5))
        
        # Event details
        details_text = f"📍 {event.get('location', 'TBD')} | 📅 {event.get('date', 'TBD')} | ⏰ {event.get('time', 'TBD')}"
        details = tk.Label(
            card,
            text=details_text,
            font=("Arial", 10),
            bg="white",
            fg="#666",
            anchor=tk.W
        )
        details.pack(fill=tk.X, pady=(0, 5))
        
        # Event description
        description = tk.Label(
            card,
            text=event.get('description', 'No description'),
            font=("Arial", 11),
            bg="white",
            fg="#444",
            anchor=tk.W,
            wraplength=600,
            justify=tk.LEFT
        )
        description.pack(fill=tk.X, pady=(0, 10))
        
        # Action buttons
        button_frame = tk.Frame(card, bg="white")
        button_frame.pack(fill=tk.X)
        
        view_button = tk.Button(
            button_frame,
            text="View Details",
            command=lambda e=event: self._on_view_event(e),
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        view_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Register button (prevent double-click with throttling)
        register_button = tk.Button(
            button_frame,
            text="Register",
            command=lambda e=event: self._on_register_event(e),
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        register_button.pack(side=tk.LEFT)
        
        # Bind hover effects
        def on_enter(e):
            card.configure(highlightbackground="#3498db", highlightthickness=2)
        
        def on_leave(e):
            card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
    
    def _on_search(self, query: str):
        """
        Handle search input (debounced)
        
        Args:
            query: Search query string
        """
        print(f"[SEARCH] Query: {query}")
        self.current_search_query = query
        
        # Reload events with search query (page 1)
        self._load_events(page=1, use_cache=False)
    
    def _on_page_change(self, page: int):
        """
        Handle page change
        
        Args:
            page: New page number
        """
        print(f"[PAGINATION] Loading page {page}")
        self._load_events(page=page, use_cache=True)
    
    def _on_add_event(self):
        """Handle add event button click"""
        print("[ACTION] Add Event")
        if self.navigate:
            self.navigate("create_event")
    
    def _on_view_event(self, event: Dict[str, Any]):
        """
        Handle view event button click
        
        Args:
            event: Event data
        """
        print(f"[ACTION] View Event: {event.get('title')}")
        if self.navigate:
            self.navigate("event_details", event_id=event.get('id'))
    
    def _on_register_event(self, event: Dict[str, Any]):
        """
        Handle register button click (throttled to prevent double-submit)
        
        Args:
            event: Event data
        """
        # Use throttler to prevent double-click
        from utils.performance import Throttler
        
        if not hasattr(self, '_register_throttler'):
            self._register_throttler = Throttler(wait_ms=2000)  # 2 second cooldown
        
        def do_register():
            print(f"[ACTION] Register for Event: {event.get('title')}")
            
            # Show loading
            overlay = show_loading(self, "Registering...")
            
            def on_success(response):
                overlay.hide()
                messagebox.showinfo("Success", f"Registered for {event.get('title')}!")
                
                # Invalidate cache to refresh data
                self.api.invalidate_cache("events")
                self._load_events(page=self.paginator.current_page, use_cache=False)
            
            def on_error(error):
                overlay.hide()
                messagebox.showerror("Error", f"Registration failed: {error}")
            
            # Make async API call
            user = self.session.get_user()
            self.api.async_post(
                endpoint=f"events/{event.get('id')}/register",
                data={},
                on_success=on_success,
                on_error=on_error,
                user_id=str(user['user_id'])
            )
        
        # Throttle the registration
        was_executed = self._register_throttler.throttle(do_register)
        if not was_executed:
            print("[THROTTLED] Registration click ignored (too soon)")
    
    def refresh(self):
        """Refresh page data (invalidate cache and reload)"""
        print("[REFRESH] Refreshing events...")
        self._load_events(page=self.paginator.current_page, use_cache=False)
    
    def cleanup(self):
        """Cleanup resources when page is unloaded"""
        print("[CLEANUP] Cleaning up Events Page")
        
        # Cancel any pending debounced calls
        if self.search_debouncer:
            self.search_debouncer.cancel()
        
        # Clear references
        self.events_data.clear()


# Example usage in main application
def example_usage():
    """
    Example of how to use OptimizedEventsPage in main app
    """
    root = tk.Tk()
    root.title("Optimized Events Page Example")
    root.geometry("900x700")
    
    # Create container
    container = tk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)
    
    # Lazy loader for pages
    lazy_loader = get_lazy_loader()
    
    def navigate(page_name, **kwargs):
        """Navigate to different pages"""
        print(f"[NAVIGATE] To {page_name} with {kwargs}")
    
    # Create page (not loaded yet)
    events_page = OptimizedEventsPage(container, navigate_callback=navigate)
    events_page.pack(fill=tk.BOTH, expand=True)
    
    # Simulate navigation - load page when shown
    def show_events_page():
        events_page.load_page()
    
    # Add button to trigger page load
    load_button = tk.Button(
        root,
        text="Load Events Page",
        command=show_events_page,
        padx=20,
        pady=10
    )
    load_button.pack(pady=20)
    
    root.mainloop()


if __name__ == "__main__":
    example_usage()
