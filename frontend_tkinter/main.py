"""
Campus Event & Resource Coordination System - Main Application
Version: 2.0.0
Date: October 9, 2025

Complete integrated application with:
- All pages integrated
- Navigation flow (Login → Dashboard → Sub-pages)
- Browser-like back/forward navigation
- Global state management (session, notifications, theme)
- Backend connectivity check on startup
- Window controls and preferences
- Menu bar with all options
- Accessibility support
- Performance optimizations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import json
from typing import Dict, List, Optional, Any
from collections import deque
import threading
import time

# Add utils to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import utilities
from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.error_handler import ErrorHandler
from utils.security import SecurityManager
from utils.accessibility import (
    get_keyboard_navigator,
    get_screen_reader_announcer,
    get_color_validator,
    get_font_scaler,
    get_focus_indicator,
    get_high_contrast_mode
)
from utils.performance import get_cache, get_lazy_loader, get_performance_monitor
from utils.loading_indicators import LoadingOverlay

# NOTE: Page modules can be heavy (PIL, tkcalendar). They are imported lazily inside
# _initialize_pages to allow importing this module for testing without requiring
# all UI dependencies to be present.


class GlobalState:
    """
    Global application state shared across all pages.
    
    Manages:
    - Session data (user, token)
    - Notifications state
    - Theme settings
    - Unsaved changes tracking
    """
    
    def __init__(self):
        """Initialize global state."""
        self.session = SessionManager()
        self.notifications: List[Dict[str, Any]] = []
        self.unread_notifications_count = 0
        self.theme = "light"  # "light" or "dark" or "high_contrast"
        self.unsaved_changes = False
        self.preferences = self._load_preferences()
        
        # State change listeners
        self.listeners: Dict[str, List] = {
            'session': [],
            'notifications': [],
            'theme': [],
            'unsaved_changes': []
        }
    
    def _load_preferences(self) -> Dict[str, Any]:
        """Load user preferences from file."""
        try:
            prefs_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'config',
                'preferences.json'
            )
            if os.path.exists(prefs_file):
                with open(prefs_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[PREFERENCES] Error loading: {e}")
        
        # Default preferences
        return {
            'window': {
                'width': 1200,
                'height': 700,
                'x': None,
                'y': None,
                'maximized': False
            },
            'theme': 'light',
            'font_scale': 1.0,
            'notifications_enabled': True,
            'auto_refresh': True,
            # runtime toggle for modern login page (can be changed in Settings)
            'use_modern_login': False
        }
    
    def save_preferences(self):
        """Save user preferences to file."""
        try:
            config_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'config'
            )
            os.makedirs(config_dir, exist_ok=True)
            
            prefs_file = os.path.join(config_dir, 'preferences.json')
            with open(prefs_file, 'w') as f:
                json.dump(self.preferences, f, indent=2)
            
            print("[PREFERENCES] Saved successfully")
        except Exception as e:
            print(f"[PREFERENCES] Error saving: {e}")
    
    def add_listener(self, event_type: str, callback):
        """Add state change listener."""
        if event_type in self.listeners:
            self.listeners[event_type].append(callback)
    
    def notify_listeners(self, event_type: str):
        """Notify all listeners of state change."""
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                try:
                    callback()
                except Exception as e:
                    print(f"[STATE] Error in listener: {e}")
    
    def set_theme(self, theme: str):
        """Change application theme."""
        self.theme = theme
        self.preferences['theme'] = theme
        self.notify_listeners('theme')
    
    def add_notification(self, notification: Dict[str, Any]):
        """Add new notification."""
        self.notifications.insert(0, notification)
        if not notification.get('read', False):
            self.unread_notifications_count += 1
        self.notify_listeners('notifications')
    
    def mark_notification_read(self, notification_id: str):
        """Mark notification as read."""
        for notif in self.notifications:
            if notif.get('id') == notification_id and not notif.get('read', False):
                notif['read'] = True
                self.unread_notifications_count -= 1
                self.notify_listeners('notifications')
                break
    
    def set_unsaved_changes(self, has_changes: bool):
        """Set unsaved changes flag."""
        self.unsaved_changes = has_changes
        self.notify_listeners('unsaved_changes')


class NavigationHistory:
    """
    Browser-like navigation history with back/forward support.
    """
    
    def __init__(self, max_size: int = 50):
        """Initialize navigation history."""
        self.history: deque = deque(maxlen=max_size)
        self.current_index = -1
    
    def add_page(self, page_name: str):
        """Add page to history."""
        # If we're not at the end, remove forward history
        if self.current_index < len(self.history) - 1:
            # Remove items after current position
            items_to_remove = len(self.history) - self.current_index - 1
            for _ in range(items_to_remove):
                self.history.pop()
        
        # Add new page
        self.history.append(page_name)
        self.current_index = len(self.history) - 1
    
    def can_go_back(self) -> bool:
        """Check if we can go back."""
        return self.current_index > 0
    
    def can_go_forward(self) -> bool:
        """Check if we can go forward."""
        return self.current_index < len(self.history) - 1
    
    def go_back(self) -> Optional[str]:
        """Go back in history."""
        if self.can_go_back():
            self.current_index -= 1
            return self.history[self.current_index]
        return None
    
    def go_forward(self) -> Optional[str]:
        """Go forward in history."""
        if self.can_go_forward():
            self.current_index += 1
            return self.history[self.current_index]
        return None
    
    def get_current(self) -> Optional[str]:
        """Get current page."""
        if 0 <= self.current_index < len(self.history):
            return self.history[self.current_index]
        return None


class CampusEventApp(tk.Tk):
    """
    Main application class with complete integration.
    
    Features:
    - All pages integrated
    - Navigation flow and history
    - Global state management
    - Backend connectivity check
    - Window controls and preferences
    - Menu bar
    - Accessibility support
    - Performance optimizations
    """
    
    def __init__(self):
        """Initialize application."""
        super().__init__()
        
        # Initialize global state (renamed to avoid conflict with tk.Tk.state())
        self.app_state = GlobalState()
        
        # Initialize utilities
        self.api = APIClient()
        self.session = self.app_state.session
        self.error_handler = ErrorHandler()
        self.security = SecurityManager()
        
        # Restore JWT token if user is already logged in
        if self.session.is_logged_in():
            token = self.session.get_token()
            if token:
                self.api.set_auth_token(token)
                print(f"[DEBUG] JWT token restored from session")
        
        # Set up auth error callback to handle token expiration
        def on_auth_error(status_code):
            """Handle authentication errors by clearing session and redirecting to login"""
            print(f"[DEBUG] Authentication error: {status_code}. Clearing session and redirecting to login.")
            self.session.clear_session()
            self.navigate('login')
            from tkinter import messagebox
            if status_code == 401:
                messagebox.showerror("Session Expired", "Your session has expired. Please login again.")
            else:
                messagebox.showerror("Access Denied", "You don't have permission to access this resource.")
        
        self.api.set_auth_error_callback(on_auth_error)
        
        # Navigation history
        self.nav_history = NavigationHistory()
        
        # Page registry
        self.pages: Dict[str, tk.Frame] = {}
        self.current_page = None
        
        # Window setup
        self._setup_window()
        
        # Initialize accessibility features
        self._init_accessibility()
        
        # Initialize performance features
        self._init_performance()
        
        # Create UI
        self._create_menu_bar()
        self._create_main_container()
        self._create_navigation_bar()
        
        # Show loading screen and check backend
        self._check_backend_on_startup()
    
    def _setup_window(self):
        """Set up window properties."""
        self.title("Campus Event & Resource Coordination System")
        
        # Load preferences
        prefs = self.app_state.preferences['window']
        
        # Set size
        width = prefs.get('width', 1200)
        height = prefs.get('height', 700)
        
        # Set position
        if prefs.get('x') and prefs.get('y'):
            x = prefs['x']
            y = prefs['y']
        else:
            # Center on screen
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = int((screen_width / 2) - (width / 2))
            y = int((screen_height / 2) - (height / 2))
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Handle maximized state
        if prefs.get('maximized', False):
            self.state('zoomed')
        
        # Color schemes
        self.themes = {
            'light': {
                'bg': '#FFFFFF',
                'fg': '#2c3e50',
                'primary': '#3498db',
                'secondary': '#2ecc71',
                'danger': '#e74c3c',
                'warning': '#f39c12',
                'accent': '#9b59b6',
                'border': '#bdc3c7',
                'hover': '#ecf0f1'
            },
            'dark': {
                'bg': '#1e1e1e',
                'fg': '#ffffff',
                'primary': '#0d6efd',
                'secondary': '#198754',
                'danger': '#dc3545',
                'warning': '#ffc107',
                'accent': '#6f42c1',
                'border': '#495057',
                'hover': '#343a40'
            },
            'high_contrast': {
                'bg': '#000000',
                'fg': '#FFFFFF',
                'primary': '#FFFF00',
                'secondary': '#00FF00',
                'danger': '#FF0000',
                'warning': '#FFA500',
                'accent': '#00FFFF',
                'border': '#FFFFFF',
                'hover': '#333333'
            }
        }
        
        self.colors = self.themes[self.app_state.theme]
        self.configure(bg=self.colors['bg'])
        
        # Window close protocol
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Bind window resize/move events
        self.bind("<Configure>", self._on_window_configure)
    
    def _init_accessibility(self):
        """Initialize accessibility features."""
        try:
            self.keyboard_nav = get_keyboard_navigator(self)
            self.announcer = get_screen_reader_announcer(self)
            self.color_validator = get_color_validator()
            self.font_scaler = get_font_scaler(self)
            self.focus_indicator = get_focus_indicator(self)
            self.high_contrast = get_high_contrast_mode(self)
            
            # Apply theme from preferences
            font_scale = self.app_state.preferences.get('font_scale', 1.0)
            self.font_scaler.set_scale(font_scale)
            
            if self.app_state.theme == 'high_contrast':
                self.high_contrast.enable()
            
            print("[ACCESSIBILITY] Features initialized")
        except Exception as e:
            print(f"[ACCESSIBILITY] Error initializing: {e}")
    
    def _init_performance(self):
        """Initialize performance features."""
        try:
            self.cache = get_cache()
            self.lazy_loader = get_lazy_loader()
            self.perf_monitor = get_performance_monitor()
            
            print("[PERFORMANCE] Features initialized")
        except Exception as e:
            print(f"[PERFORMANCE] Error initializing: {e}")
    
    def _create_menu_bar(self):
        """Create application menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self._show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_command(label="Exit", command=self._on_close)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Theme submenu
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_radiobutton(
            label="Light",
            command=lambda: self._change_theme('light')
        )
        theme_menu.add_radiobutton(
            label="Dark",
            command=lambda: self._change_theme('dark')
        )
        theme_menu.add_radiobutton(
            label="High Contrast",
            command=lambda: self._change_theme('high_contrast')
        )
        
        view_menu.add_separator()
        view_menu.add_command(label="Notifications", command=self._show_notifications)
        view_menu.add_separator()
        view_menu.add_command(label="Refresh", command=self._refresh_current_page)
        
        # Navigation menu
        nav_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Navigate", menu=nav_menu)
        nav_menu.add_command(
            label="Back",
            command=self._go_back,
            accelerator="Alt+Left"
        )
        nav_menu.add_command(
            label="Forward",
            command=self._go_forward,
            accelerator="Alt+Right"
        )
        nav_menu.add_separator()
        nav_menu.add_command(label="Dashboard", command=self._go_to_dashboard)
        
        # Accessibility menu
        access_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="♿ Accessibility", menu=access_menu)
        access_menu.add_command(
            label="Increase Font Size (Ctrl++)",
            command=self.font_scaler.increase_font
        )
        access_menu.add_command(
            label="Decrease Font Size (Ctrl+-)",
            command=self.font_scaler.decrease_font
        )
        access_menu.add_command(
            label="Reset Font Size (Ctrl+0)",
            command=self.font_scaler.reset_font
        )
        access_menu.add_separator()
        access_menu.add_command(
            label="Toggle High Contrast (Ctrl+H)",
            command=self._toggle_high_contrast
        )
        access_menu.add_separator()
        access_menu.add_command(
            label="Keyboard Shortcuts (F1)",
            command=self.keyboard_nav._show_help
        )
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self._show_user_guide)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Contact Support", command=self._show_support)
        
        # Register keyboard shortcuts
        self.keyboard_nav.register_shortcut('<Alt-Left>', self._go_back, "Go back")
        self.keyboard_nav.register_shortcut('<Alt-Right>', self._go_forward, "Go forward")
        self.keyboard_nav.register_shortcut('<Control-plus>', self.font_scaler.increase_font, "Increase font")
        self.keyboard_nav.register_shortcut('<Control-minus>', self.font_scaler.decrease_font, "Decrease font")
        self.keyboard_nav.register_shortcut('<Control-0>', self.font_scaler.reset_font, "Reset font")
        self.keyboard_nav.register_shortcut('<Control-h>', self._toggle_high_contrast, "Toggle high contrast")
    
    def _create_navigation_bar(self):
        """Create modern navigation bar with back/forward buttons."""
        # Modern dark navigation bar
        nav_bar = tk.Frame(self.main_container, bg='#1E293B', height=50)
        nav_bar.pack(fill=tk.X, padx=0, pady=0)
        nav_bar.pack_propagate(False)
        
        # Left side - Navigation buttons
        left_frame = tk.Frame(nav_bar, bg='#1E293B')
        left_frame.pack(side=tk.LEFT, padx=15, pady=8)
        
        # Back button - Canvas-based for macOS compatibility
        self.back_canvas = tk.Canvas(left_frame, width=90, height=34, bg='#1E293B', highlightthickness=0)
        self.back_canvas.pack(side=tk.LEFT, padx=(0, 8))
        self.back_enabled = False
        self.back_rect = self.back_canvas.create_rectangle(0, 0, 90, 34, fill='#64748B', outline='', tags='btn')
        self.back_text = self.back_canvas.create_text(45, 17, text="← Back", font=("Helvetica", 11, 'bold'), fill='#FFFFFF', tags='btn')
        self.back_canvas.tag_bind('btn', '<Button-1>', lambda e: self._go_back() if self.back_enabled else None)
        self.back_canvas.tag_bind('btn', '<Enter>', lambda e: self.back_canvas.itemconfig(self.back_rect, fill='#2563EB') if self.back_enabled else None)
        self.back_canvas.tag_bind('btn', '<Leave>', lambda e: self.back_canvas.itemconfig(self.back_rect, fill='#3B82F6') if self.back_enabled else None)
        
        # Forward button - Canvas-based for macOS compatibility
        self.forward_canvas = tk.Canvas(left_frame, width=110, height=34, bg='#1E293B', highlightthickness=0)
        self.forward_canvas.pack(side=tk.LEFT, padx=(0, 8))
        self.forward_enabled = False
        self.forward_rect = self.forward_canvas.create_rectangle(0, 0, 110, 34, fill='#64748B', outline='', tags='btn')
        self.forward_text = self.forward_canvas.create_text(55, 17, text="Forward →", font=("Helvetica", 11, 'bold'), fill='#FFFFFF', tags='btn')
        self.forward_canvas.tag_bind('btn', '<Button-1>', lambda e: self._go_forward() if self.forward_enabled else None)
        self.forward_canvas.tag_bind('btn', '<Enter>', lambda e: self.forward_canvas.itemconfig(self.forward_rect, fill='#2563EB') if self.forward_enabled else None)
        self.forward_canvas.tag_bind('btn', '<Leave>', lambda e: self.forward_canvas.itemconfig(self.forward_rect, fill='#3B82F6') if self.forward_enabled else None)
        
        # Center - Current page label
        self.page_label = tk.Label(
            nav_bar,
            text="",
            bg='#1E293B',
            fg='#F1F5F9',
            font=("Helvetica", 13, "bold")
        )
        self.page_label.pack(side=tk.LEFT, padx=20)
        
        # Right side - User actions
        right_frame = tk.Frame(nav_bar, bg='#1E293B')
        right_frame.pack(side=tk.RIGHT, padx=15, pady=8)
        
        # Notifications button - Canvas-based for macOS compatibility
        self.notif_canvas = tk.Canvas(right_frame, width=140, height=34, bg='#1E293B', highlightthickness=0)
        self.notif_canvas.pack(side=tk.RIGHT, padx=(8, 0))
        self.notif_rect = self.notif_canvas.create_rectangle(0, 0, 140, 34, fill='#2D3748', outline='', tags='btn')
        self.notif_text = self.notif_canvas.create_text(70, 17, text="🔔 Notifications", font=("Helvetica", 11), fill='#F1F5F9', tags='btn')
        self.notif_canvas.tag_bind('btn', '<Button-1>', lambda e: self._show_notifications())
        self.notif_canvas.tag_bind('btn', '<Enter>', lambda e: self.notif_canvas.itemconfig(self.notif_rect, fill='#374151'))
        self.notif_canvas.tag_bind('btn', '<Leave>', lambda e: self.notif_canvas.itemconfig(self.notif_rect, fill='#2D3748'))
        self.notif_canvas.config(cursor='hand2')
        
        # Profile button - Canvas-based for macOS compatibility
        self.profile_canvas = tk.Canvas(right_frame, width=110, height=34, bg='#1E293B', highlightthickness=0)
        self.profile_canvas.pack(side=tk.RIGHT, padx=(8, 0))
        self.profile_rect = self.profile_canvas.create_rectangle(0, 0, 110, 34, fill='#2D3748', outline='', tags='btn')
        self.profile_text = self.profile_canvas.create_text(55, 17, text="👤 Profile", font=("Helvetica", 11), fill='#F1F5F9', tags='btn')
        self.profile_canvas.tag_bind('btn', '<Button-1>', lambda e: self._show_profile())
        self.profile_canvas.tag_bind('btn', '<Enter>', lambda e: self.profile_canvas.itemconfig(self.profile_rect, fill='#374151'))
        self.profile_canvas.tag_bind('btn', '<Leave>', lambda e: self.profile_canvas.itemconfig(self.profile_rect, fill='#2D3748'))
        self.profile_canvas.config(cursor='hand2')
        
        self.nav_bar = nav_bar
    
    def _create_main_container(self):
        """Create main container for pages."""
        self.main_container = tk.Frame(self, bg=self.colors['bg'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Page container
        self.page_container = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.page_container.pack(fill=tk.BOTH, expand=True)
    
    def _check_backend_on_startup(self):
        """Check if backend is reachable on startup."""
        # Show loading overlay
        self.loading_overlay = LoadingOverlay(self, message="Checking backend connection...")
        self.loading_overlay.show()
        
        # Check backend in background thread
        def check_backend():
            time.sleep(0.5)  # Brief delay for UI
            
            try:
                # Try to reach backend - use a real endpoint that exists
                # We'll try to get events (will fail but proves backend is running)
                response = self.api.get("events")
                success = True
            except Exception as e:
                # Check if it's a connection error or just an auth/endpoint error
                error_str = str(e).lower()
                if "connection" in error_str or "timeout" in error_str:
                    print(f"[STARTUP] Backend check failed: {e}")
                    success = False
                else:
                    # Backend is responding, just needs auth or endpoint exists
                    print(f"[STARTUP] Backend is reachable (got response): {e}")
                    success = True
            
            # Update UI in main thread
            self.after(0, lambda: self._on_backend_check_complete(success))
        
        thread = threading.Thread(target=check_backend, daemon=True)
        thread.start()
    
    def _on_backend_check_complete(self, success: bool):
        """Handle backend check completion."""
        self.loading_overlay.hide()
        
        if success:
            print("[STARTUP] Backend is reachable")
            self.announcer.announce("Backend connected successfully")
            self._initialize_pages()
            self._show_login()
        else:
            # Show error with retry option
            result = messagebox.askretrycancel(
                "Backend Unreachable",
                "Cannot connect to the backend server.\n\n"
                "Please ensure the backend is running at:\n"
                f"{self.api.base_url}\n\n"
                "Click 'Retry' to try again, or 'Cancel' to exit."
            )
            
            if result:
                # Retry
                self._check_backend_on_startup()
            else:
                # Exit
                self.destroy()
    
    def _initialize_pages(self):
        """Initialize all pages."""
        print("[PAGES] Initializing all pages...")
        
        # Pass navigation callback and shared state to all pages
        page_config = {
            'navigate': self.navigate,
            'state': self.state,
            'accessibility': {
                'keyboard_nav': self.keyboard_nav,
                'announcer': self.announcer,
                'font_scaler': self.font_scaler,
                'focus_indicator': self.focus_indicator,
                'high_contrast': self.high_contrast
            }
        }
        
        # Create page_classes mapping with lazy imports. If a page module
        # cannot be imported (missing deps), we set the mapping to None and
        # defer instantiation until later; error will be shown when trying to
        # navigate to that page.
        def try_import(module_path: str, symbol: str):
            try:
                mod = __import__(module_path, fromlist=[symbol])
                return getattr(mod, symbol)
            except Exception as e:
                print(f"[PAGES] Warning: could not import {module_path}.{symbol}: {e}")
                return None

        # Determine login class using runtime preference or fallback to config
        use_modern_pref = self.app_state.preferences.get('use_modern_login', None)
        login_class = None
        if use_modern_pref is not None:
            if use_modern_pref:
                login_class = try_import('pages.login_page_modern', 'LoginPageModern')
            else:
                login_class = try_import('pages.login_page', 'LoginPage')
        else:
            cfg_use = False
            try:
                from config import USE_MODERN_LOGIN as CFG_USE_MODERN
                cfg_use = bool(CFG_USE_MODERN)
            except Exception:
                cfg_use = False

            if cfg_use:
                login_class = try_import('pages.login_page_modern', 'LoginPageModern')
            else:
                login_class = try_import('pages.login_page', 'LoginPage')

        self.page_classes = {
            'login': login_class,
            'register': try_import('pages.register_page', 'RegisterPage'),
            'student_dashboard': try_import('pages.student_dashboard', 'StudentDashboard'),
            'organizer_dashboard': try_import('pages.organizer_dashboard', 'OrganizerDashboard'),
            'admin_dashboard': try_import('pages.admin_dashboard', 'AdminDashboard'),
            'browse_events': try_import('pages.browse_events', 'BrowseEventsPage'),
            'browse_resources': try_import('pages.browse_resources', 'BrowseResourcesPage'),
            'create_event': try_import('pages.create_event', 'CreateEventPage'),
            'my_events': try_import('pages.my_events', 'MyEventsPage'),
            'my_bookings': try_import('pages.my_bookings', 'MyBookingsPage'),
            'book_resource': try_import('pages.book_resource', 'BookResourcePage'),
            'event_approvals': try_import('pages.event_approvals', 'EventApprovalsPage'),
            'booking_approvals': try_import('pages.booking_approvals', 'BookingApprovalsPage'),
            'manage_resources': try_import('pages.manage_resources', 'ManageResourcesPage'),
            'manage_users': try_import('pages.manage_users', 'ManageUsersPage'),
            'analytics': try_import('pages.analytics_page', 'AnalyticsPage'),
            'notifications': try_import('pages.notifications_page', 'NotificationsPage'),
            'profile': try_import('pages.profile_page', 'ProfilePage')
        }

        registered = sum(1 for v in self.page_classes.values() if v is not None)
        print(f"[PAGES] Registered {registered}/{len(self.page_classes)} page classes (lazy)")
    
    def _get_or_create_page(self, page_name: str) -> Optional[tk.Frame]:
        """Get existing page or create new one (lazy loading)."""
        if page_name in self.pages:
            return self.pages[page_name]
        
        if page_name not in self.page_classes:
            print(f"[PAGES] Unknown page: {page_name}")
            return None
        
        try:
            # Create page - pass self (controller) as pages expect
            page_class = self.page_classes[page_name]
            page = page_class(
                self.page_container,
                self  # Pass controller, not navigate function
            )
            
            # Store page
            self.pages[page_name] = page
            
            print(f"[PAGES] Created page: {page_name}")
            return page
            
        except Exception as e:
            print(f"[PAGES] Error creating page {page_name}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def navigate(self, page_name: str, add_to_history: bool = True, **kwargs):
        """
        Navigate to a page.
        
        Args:
            page_name: Name of page to show
            add_to_history: Whether to add to navigation history
            **kwargs: Additional arguments for the page
        """
        print(f"[NAVIGATE] To {page_name}")
        
        # Get or create page
        page = self._get_or_create_page(page_name)
        if not page:
            return
        
        # Hide current page
        if self.current_page:
            self.current_page.pack_forget()
        
        # Show new page
        page.pack(fill=tk.BOTH, expand=True)
        
        # Call load_page if available (lazy loading)
        if hasattr(page, 'load_page'):
            page.load_page()
        
        # Update state
        self.current_page = page
        
        # Add to history
        if add_to_history:
            self.nav_history.add_page(page_name)
            self._update_nav_buttons()
        
        # Update page label
        page_title = page_name.replace('_', ' ').title()
        self.page_label.config(text=page_title)
        
        # Announce page change
        self.announcer.announce_page_change(page_title)
        
        # Update title
        self.title(f"Campus Event System - {page_title}")
    
    def _show_login(self):
        """Show login page."""
        self.navigate('login', add_to_history=False)
    
    def _go_back(self):
        """Go back in navigation history."""
        if self.nav_history.can_go_back():
            page_name = self.nav_history.go_back()
            if page_name:
                self.navigate(page_name, add_to_history=False)
                self._update_nav_buttons()
    
    def _go_forward(self):
        """Go forward in navigation history."""
        if self.nav_history.can_go_forward():
            page_name = self.nav_history.go_forward()
            if page_name:
                self.navigate(page_name, add_to_history=False)
                self._update_nav_buttons()
    
    def _update_nav_buttons(self):
        """Update back/forward button states with proper styling."""
        if self.nav_history.can_go_back():
            self.back_enabled = True
            self.back_canvas.itemconfig(self.back_rect, fill='#3B82F6')
            self.back_canvas.itemconfig(self.back_text, fill='#FFFFFF')
            self.back_canvas.config(cursor='hand2')
        else:
            self.back_enabled = False
            self.back_canvas.itemconfig(self.back_rect, fill='#64748B')
            self.back_canvas.itemconfig(self.back_text, fill='#94A3B8')
            self.back_canvas.config(cursor='arrow')
        
        if self.nav_history.can_go_forward():
            self.forward_enabled = True
            self.forward_canvas.itemconfig(self.forward_rect, fill='#3B82F6')
            self.forward_canvas.itemconfig(self.forward_text, fill='#FFFFFF')
            self.forward_canvas.config(cursor='hand2')
        else:
            self.forward_enabled = False
            self.forward_canvas.itemconfig(self.forward_rect, fill='#64748B')
            self.forward_canvas.itemconfig(self.forward_text, fill='#94A3B8')
            self.forward_canvas.config(cursor='arrow')
    
    def _go_to_dashboard(self):
        """Navigate to appropriate dashboard based on user role."""
        user = self.session.get_user()
        if not user:
            self.navigate('login')
            return
        
        role = user.get('role', 'student')
        
        if role == 'admin':
            self.navigate('admin_dashboard')
        elif role == 'organizer':
            self.navigate('organizer_dashboard')
        else:
            self.navigate('student_dashboard')
    
    def _refresh_current_page(self):
        """Refresh current page."""
        if self.current_page and hasattr(self.current_page, 'refresh'):
            self.current_page.refresh()
            self.announcer.announce("Page refreshed")
    
    def _show_notifications(self):
        """Show notifications page."""
        self.navigate('notifications')
    
    def _show_profile(self):
        """Show profile page."""
        self.navigate('profile')
    
    def _show_settings(self):
        """Show settings dialog."""
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.transient(self)
        settings_window.grab_set()
        
        # Settings content
        tk.Label(
            settings_window,
            text="Settings",
            font=("Arial", 18, "bold")
        ).pack(pady=20)
        
        # Auto-refresh setting
        auto_refresh_var = tk.BooleanVar(
            value=self.app_state.preferences.get('auto_refresh', True)
        )
        tk.Checkbutton(
            settings_window,
            text="Auto-refresh data",
            variable=auto_refresh_var,
            font=("Arial", 11)
        ).pack(anchor='w', padx=40, pady=5)
        
        # Notifications setting
        notif_enabled_var = tk.BooleanVar(
            value=self.app_state.preferences.get('notifications_enabled', True)
        )
        tk.Checkbutton(
            settings_window,
            text="Enable notifications",
            variable=notif_enabled_var,
            font=("Arial", 11)
        ).pack(anchor='w', padx=40, pady=5)

        # Modern login runtime toggle
        modern_login_var = tk.BooleanVar(
            value=self.app_state.preferences.get('use_modern_login', False)
        )
        tk.Checkbutton(
            settings_window,
            text="Use modern login page (no restart required)",
            variable=modern_login_var,
            font=("Arial", 11)
        ).pack(anchor='w', padx=40, pady=5)
        
        # Save button
        def save_settings():
            self.app_state.preferences['auto_refresh'] = auto_refresh_var.get()
            self.app_state.preferences['notifications_enabled'] = notif_enabled_var.get()
            # Modern login runtime toggle
            self.app_state.preferences['use_modern_login'] = modern_login_var.get()
            # Apply login preference immediately so testers don't need to restart
            try:
                self._apply_login_preference(modern_login_var.get())
            except Exception as e:
                print(f"[SETTINGS] Failed to apply login preference: {e}")
            self.app_state.save_preferences()
            messagebox.showinfo("Settings", "Settings saved successfully")
            settings_window.destroy()
        
        tk.Button(
            settings_window,
            text="Save",
            command=save_settings,
            bg=self.colors['primary'],
            fg="white",
            font=("Arial", 11),
            padx=20,
            pady=5
        ).pack(pady=20)
        
        self.keyboard_nav.push_modal(settings_window)

    def _apply_login_preference(self, use_modern: bool):
        """Apply the runtime preference for which login page class to use.

        This updates the page_classes mapping so subsequent navigations
        will instantiate the selected login implementation.
        """
        try:
            if use_modern:
                from pages.login_page_modern import LoginPageModern
                login_class = LoginPageModern
            else:
                login_class = LoginPage

            # Update mapping
            if hasattr(self, 'page_classes'):
                self.page_classes['login'] = login_class
                print(f"[PAGES] Applied runtime login preference: {'modern' if use_modern else 'legacy'}")
            else:
                # If pages not initialized yet, ensure preferences will be used on init
                self.app_state.preferences['use_modern_login'] = use_modern

        except Exception as e:
            print(f"[PAGES] Error applying login preference: {e}")
    
    def _logout(self):
        """Logout user."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.session.clear_session()
            self.cache.clear()
            self.announcer.announce("Logged out successfully")
            self.navigate('login', add_to_history=False)
    
    def _change_theme(self, theme: str):
        """Change application theme."""
        self.app_state.set_theme(theme)
        self.colors = self.themes[theme]
        
        # Update colors
        self.configure(bg=self.colors['bg'])
        
        # Enable/disable high contrast mode
        if theme == 'high_contrast':
            self.high_contrast.enable()
        else:
            self.high_contrast.disable()
        
        self.announcer.announce(f"{theme.title()} theme activated")
        
        # Would need to refresh all widgets - simplified here
        messagebox.showinfo(
            "Theme Changed",
            "Theme changed successfully. Some changes will apply on next restart."
        )
    
    def _toggle_high_contrast(self):
        """Toggle high contrast mode."""
        self.high_contrast.toggle()
        
        if self.high_contrast.enabled:
            self.app_state.set_theme('high_contrast')
            self.announcer.announce("High contrast mode enabled")
        else:
            self.app_state.set_theme('light')
            self.announcer.announce("High contrast mode disabled")
    
    def _show_user_guide(self):
        """Show user guide."""
        guide_window = tk.Toplevel(self)
        guide_window.title("User Guide")
        guide_window.geometry("600x500")
        guide_window.transient(self)
        
        # Title
        tk.Label(
            guide_window,
            text="Campus Event System - User Guide",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        # Guide content
        guide_text = """
Welcome to the Campus Event & Resource Coordination System!

📚 Getting Started:
1. Login with your credentials
2. Navigate to your dashboard
3. Browse events and resources
4. Register for events or book resources

⌨️ Keyboard Shortcuts:
• Alt+Left/Right - Navigate back/forward
• F1 - Show all shortcuts
• Ctrl++ - Increase font size
• Ctrl+- - Decrease font size
• Ctrl+H - Toggle high contrast mode

🎯 Features:
• Browse and register for campus events
• Book resources (rooms, equipment)
• Manage your events (organizers)
• Approve events and bookings (admins)
• View analytics and reports

♿ Accessibility:
• Full keyboard navigation support
• Screen reader compatible
• High contrast mode
• Font size adjustment

📞 Need Help?
Contact support from Help → Contact Support
        """
        
        text_widget = tk.Text(
            guide_window,
            wrap=tk.WORD,
            font=("Arial", 11),
            padx=20,
            pady=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert('1.0', guide_text)
        text_widget.config(state='disabled')
        
        tk.Button(
            guide_window,
            text="Close",
            command=guide_window.destroy,
            padx=20,
            pady=5
        ).pack(pady=10)
        
        self.keyboard_nav.push_modal(guide_window)
    
    def _show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            "Campus Event & Resource Coordination System\n\n"
            "Version: 2.0.0\n"
            "Date: October 9, 2025\n\n"
            "A comprehensive system for managing campus events,\n"
            "resources, and bookings with full accessibility support.\n\n"
            "© 2025 Campus Event System"
        )
    
    def _show_support(self):
        """Show contact support dialog."""
        support_window = tk.Toplevel(self)
        support_window.title("Contact Support")
        support_window.geometry("400x300")
        support_window.transient(self)
        support_window.grab_set()
        
        tk.Label(
            support_window,
            text="Contact Support",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        tk.Label(
            support_window,
            text="Need help? Contact us:",
            font=("Arial", 11)
        ).pack(pady=10)
        
        tk.Label(
            support_window,
            text="📧 Email: support@campusevents.edu",
            font=("Arial", 11)
        ).pack(pady=5)
        
        tk.Label(
            support_window,
            text="📞 Phone: (555) 123-4567",
            font=("Arial", 11)
        ).pack(pady=5)
        
        tk.Label(
            support_window,
            text="💬 Hours: Mon-Fri 9AM-5PM",
            font=("Arial", 11)
        ).pack(pady=5)
        
        tk.Button(
            support_window,
            text="Close",
            command=support_window.destroy,
            padx=20,
            pady=5
        ).pack(pady=20)
        
        self.keyboard_nav.push_modal(support_window)
    
    def _on_window_configure(self, event):
        """Handle window resize/move events."""
        if event.widget == self:
            # Save window size and position
            if self.state() != 'zoomed':
                self.app_state.preferences['window']['width'] = self.winfo_width()
                self.app_state.preferences['window']['height'] = self.winfo_height()
                self.app_state.preferences['window']['x'] = self.winfo_x()
                self.app_state.preferences['window']['y'] = self.winfo_y()
                self.app_state.preferences['window']['maximized'] = False
            else:
                self.app_state.preferences['window']['maximized'] = True
    
    def _on_close(self):
        """Handle window close event."""
        # Check for unsaved changes
        if self.app_state.unsaved_changes:
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?"
            )
            
            if result is None:  # Cancel
                return
            elif result:  # Yes - save
                # Call save on current page if available
                if self.current_page and hasattr(self.current_page, 'save'):
                    self.current_page.save()
        
        # Save preferences
        self.app_state.save_preferences()
        
        # Save font scale
        self.app_state.preferences['font_scale'] = self.font_scaler.scale_factor
        self.app_state.save_preferences()
        
        print("[APP] Shutting down...")
        self.announcer.announce("Application closing")
        
        # Destroy window
        self.destroy()


def main():
    """Main entry point."""
    print("=" * 60)
    print("CAMPUS EVENT & RESOURCE COORDINATION SYSTEM")
    print("Version: 2.0.0")
    print("=" * 60)
    print()
    
    try:
        app = CampusEventApp()
        app.mainloop()
    except Exception as e:
        print(f"[ERROR] Application crashed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()