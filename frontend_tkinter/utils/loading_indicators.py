"""
Loading Indicators and UI Components for Performance
Provides spinners, progress bars, and skeleton screens
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
import threading


class LoadingSpinner(tk.Frame):
    """
    Animated loading spinner widget
    
    Shows rotating animation during loading operations
    """
    
    def __init__(self, parent, size: int = 50, color: str = "#3498db"):
        """
        Initialize loading spinner
        
        Args:
            parent: Parent widget
            size: Size of spinner in pixels
            color: Color of spinner
        """
        super().__init__(parent)
        
        self.size = size
        self.color = color
        self.angle = 0
        self.running = False
        self._animation_id = None
        
        # Create canvas for spinner
        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg=parent.cget('bg'),
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Create arc
        self.arc_id = self.canvas.create_arc(
            5, 5, size - 5, size - 5,
            start=0,
            extent=300,
            outline=color,
            width=3,
            style=tk.ARC
        )
    
    def start(self):
        """Start spinner animation"""
        if not self.running:
            self.running = True
            self._animate()
    
    def stop(self):
        """Stop spinner animation"""
        self.running = False
        if self._animation_id:
            self.after_cancel(self._animation_id)
            self._animation_id = None
    
    def _animate(self):
        """Animate spinner rotation"""
        if not self.running:
            return
        
        self.angle = (self.angle + 10) % 360
        
        # Update arc position
        self.canvas.itemconfig(self.arc_id, start=self.angle)
        
        # Schedule next frame
        self._animation_id = self.after(30, self._animate)


class ProgressBar(tk.Frame):
    """
    Progress bar widget for file uploads and long operations
    
    Shows percentage and optional text
    """
    
    def __init__(self, parent, width: int = 300, height: int = 25):
        """
        Initialize progress bar
        
        Args:
            parent: Parent widget
            width: Width of progress bar
            height: Height of progress bar
        """
        super().__init__(parent)
        
        self.width = width
        self.height = height
        self.progress = 0.0
        
        # Create ttk progress bar
        self.progressbar = ttk.Progressbar(
            self,
            orient=tk.HORIZONTAL,
            length=width,
            mode='determinate'
        )
        self.progressbar.pack(pady=5)
        
        # Create label for percentage
        self.label = tk.Label(self, text="0%", font=("Arial", 10))
        self.label.pack()
    
    def set_progress(self, value: float, text: Optional[str] = None):
        """
        Set progress value
        
        Args:
            value: Progress value (0.0 to 1.0)
            text: Optional text to display
        """
        self.progress = max(0.0, min(1.0, value))
        self.progressbar['value'] = self.progress * 100
        
        # Update label
        if text:
            self.label.config(text=text)
        else:
            self.label.config(text=f"{int(self.progress * 100)}%")
        
        self.update_idletasks()
    
    def reset(self):
        """Reset progress to 0"""
        self.set_progress(0.0)


class SkeletonScreen(tk.Frame):
    """
    Skeleton screen placeholder for loading content
    
    Shows animated placeholder boxes while content loads
    """
    
    def __init__(self, parent, rows: int = 3):
        """
        Initialize skeleton screen
        
        Args:
            parent: Parent widget
            rows: Number of skeleton rows to show
        """
        super().__init__(parent, bg="#f0f0f0")
        
        self.rows = rows
        self.skeleton_items = []
        
        # Create skeleton rows
        for i in range(rows):
            self._create_skeleton_row()
    
    def _create_skeleton_row(self):
        """Create a single skeleton row"""
        row_frame = tk.Frame(self, bg="#e0e0e0", height=60)
        row_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Title placeholder (darker)
        title = tk.Frame(row_frame, bg="#d0d0d0", height=20, width=200)
        title.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Subtitle placeholder (lighter)
        subtitle = tk.Frame(row_frame, bg="#e0e0e0", height=15, width=300)
        subtitle.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        self.skeleton_items.append(row_frame)


class LoadingOverlay(tk.Frame):
    """
    Full-screen loading overlay with spinner and message
    
    Blocks interaction while showing loading state
    """
    
    def __init__(self, parent, message: str = "Loading..."):
        """
        Initialize loading overlay
        
        Args:
            parent: Parent widget
            message: Loading message to display
        """
        super().__init__(parent, bg="white")
        
        # Configure frame to fill parent
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Create container for centered content
        container = tk.Frame(self, bg="white")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Add spinner
        self.spinner = LoadingSpinner(container, size=60)
        self.spinner.pack(pady=20)
        
        # Add message
        self.message_label = tk.Label(
            container,
            text=message,
            font=("Arial", 14),
            bg="white",
            fg="#333"
        )
        self.message_label.pack()
        
        # Start spinner
        self.spinner.start()
    
    def update_message(self, message: str):
        """
        Update loading message
        
        Args:
            message: New message to display
        """
        self.message_label.config(text=message)
    
    def show(self):
        """Show loading overlay"""
        self.lift()
        self.spinner.start()
    
    def hide(self):
        """Hide loading overlay"""
        self.spinner.stop()
        self.place_forget()
    
    def destroy(self):
        """Cleanup and destroy overlay"""
        self.spinner.stop()
        super().destroy()


class PaginationControls(tk.Frame):
    """
    Pagination controls widget
    
    Shows page numbers and navigation buttons
    """
    
    def __init__(self, parent, on_page_change: Callable[[int], None]):
        """
        Initialize pagination controls
        
        Args:
            parent: Parent widget
            on_page_change: Callback function when page changes (receives page number)
        """
        super().__init__(parent, bg="white")
        
        self.on_page_change = on_page_change
        self.current_page = 1
        self.total_pages = 1
        
        # Previous button
        self.prev_button = tk.Button(
            self,
            text="← Previous",
            command=self._previous_page,
            state=tk.DISABLED,
            padx=15,
            pady=5
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        # Page info label
        self.page_label = tk.Label(
            self,
            text="Page 1 of 1",
            font=("Arial", 11),
            bg="white"
        )
        self.page_label.pack(side=tk.LEFT, padx=20)
        
        # Next button
        self.next_button = tk.Button(
            self,
            text="Next →",
            command=self._next_page,
            state=tk.DISABLED,
            padx=15,
            pady=5
        )
        self.next_button.pack(side=tk.LEFT, padx=5)
    
    def update_pagination(self, current_page: int, total_pages: int):
        """
        Update pagination state
        
        Args:
            current_page: Current page number (1-indexed)
            total_pages: Total number of pages
        """
        self.current_page = current_page
        self.total_pages = total_pages
        
        # Update label
        self.page_label.config(text=f"Page {current_page} of {total_pages}")
        
        # Update button states
        self.prev_button.config(state=tk.NORMAL if current_page > 1 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if current_page < total_pages else tk.DISABLED)
    
    def _previous_page(self):
        """Handle previous button click"""
        if self.current_page > 1:
            self.on_page_change(self.current_page - 1)
    
    def _next_page(self):
        """Handle next button click"""
        if self.current_page < self.total_pages:
            self.on_page_change(self.current_page + 1)


class LoadMoreButton(tk.Frame):
    """
    "Load More" button for infinite scroll pattern
    
    Shows button to load next batch of items
    """
    
    def __init__(self, parent, on_load_more: Callable[[], None], text: str = "Load More"):
        """
        Initialize load more button
        
        Args:
            parent: Parent widget
            on_load_more: Callback function when button clicked
            text: Button text
        """
        super().__init__(parent, bg="white")
        
        self.on_load_more = on_load_more
        self.loading = False
        
        # Create button
        self.button = tk.Button(
            self,
            text=text,
            command=self._handle_click,
            padx=30,
            pady=10,
            font=("Arial", 11)
        )
        self.button.pack(pady=20)
        
        # Create loading indicator
        self.spinner = LoadingSpinner(self, size=30)
        self.spinner.pack_forget()
    
    def _handle_click(self):
        """Handle button click"""
        if not self.loading:
            self.loading = True
            self.button.pack_forget()
            self.spinner.pack(pady=20)
            self.spinner.start()
            
            # Call callback in thread to avoid blocking UI
            threading.Thread(target=self._load_more_thread, daemon=True).start()
    
    def _load_more_thread(self):
        """Execute load more in background thread"""
        try:
            self.on_load_more()
        finally:
            # Reset UI state
            self.after(0, self._reset_state)
    
    def _reset_state(self):
        """Reset button state after loading"""
        self.loading = False
        self.spinner.stop()
        self.spinner.pack_forget()
        self.button.pack(pady=20)
    
    def hide(self):
        """Hide load more button"""
        self.pack_forget()
    
    def show(self):
        """Show load more button"""
        self.pack(fill=tk.X)


class SearchBar(tk.Frame):
    """
    Search bar with debounced input
    
    Delays search execution until user stops typing
    """
    
    def __init__(self, parent, on_search: Callable[[str], None], 
                 placeholder: str = "Search...", debounce_ms: int = 500):
        """
        Initialize search bar
        
        Args:
            parent: Parent widget
            on_search: Callback function when search executes (receives query)
            placeholder: Placeholder text
            debounce_ms: Debounce delay in milliseconds
        """
        super().__init__(parent, bg="white")
        
        self.on_search = on_search
        self.debounce_ms = debounce_ms
        self._timer_id = None
        
        # Create search icon (using emoji for simplicity)
        icon_label = tk.Label(self, text="🔍", font=("Arial", 16), bg="white")
        icon_label.pack(side=tk.LEFT, padx=(10, 5))
        
        # Create entry
        self.entry = tk.Entry(
            self,
            font=("Arial", 12),
            relief=tk.FLAT,
            bg="#f5f5f5"
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=8)
        
        # Bind key events
        self.entry.bind('<KeyRelease>', self._on_key_release)
        
        # Add placeholder behavior
        self.placeholder = placeholder
        self._add_placeholder()
    
    def _add_placeholder(self):
        """Add placeholder text"""
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg="#999")
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Handle focus in event"""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="#000")
    
    def _on_focus_out(self, event):
        """Handle focus out event"""
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="#999")
    
    def _on_key_release(self, event):
        """Handle key release (for debouncing)"""
        # Cancel previous timer
        if self._timer_id:
            self.after_cancel(self._timer_id)
        
        # Schedule new search
        self._timer_id = self.after(self.debounce_ms, self._execute_search)
    
    def _execute_search(self):
        """Execute search callback"""
        query = self.entry.get()
        
        # Don't search if placeholder
        if query and query != self.placeholder:
            self.on_search(query)
    
    def get_query(self) -> str:
        """
        Get current search query
        
        Returns:
            Search query string
        """
        query = self.entry.get()
        return query if query != self.placeholder else ""
    
    def clear(self):
        """Clear search input"""
        self.entry.delete(0, tk.END)
        self._add_placeholder()


def show_loading(parent: tk.Widget, message: str = "Loading...") -> LoadingOverlay:
    """
    Show loading overlay on widget
    
    Args:
        parent: Parent widget
        message: Loading message
    
    Returns:
        LoadingOverlay instance (call hide() to remove)
    
    Example:
        overlay = show_loading(self, "Loading events...")
        # ... perform operation ...
        overlay.hide()
    """
    overlay = LoadingOverlay(parent, message)
    return overlay


def async_operation(func: Callable, on_complete: Optional[Callable] = None, 
                    on_error: Optional[Callable] = None):
    """
    Execute operation in background thread
    
    Args:
        func: Function to execute
        on_complete: Callback when complete (receives result)
        on_error: Callback on error (receives exception)
    
    Example:
        def load_data():
            return api.get("events")
        
        def on_done(result):
            self.display_events(result)
        
        async_operation(load_data, on_complete=on_done)
    """
    def worker():
        try:
            result = func()
            if on_complete:
                on_complete(result)
        except Exception as e:
            if on_error:
                on_error(e)
            else:
                print(f"Error in async operation: {e}")
    
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
