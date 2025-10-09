"""
Image Loader Usage Examples

This file demonstrates how to use the ImageLoader utility and IconSet
throughout the Campus Event System application.

Run this file to see a live demo of image loading capabilities.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.image_loader import ImageLoader, IconSet, get_image_loader, load_image, load_icon, load_logo


class ImageLoaderDemo(tk.Tk):
    """Demo application showcasing image loader capabilities"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Image Loader Demo - Campus Event System")
        self.geometry("1000x700")
        self.config(bg="#F8F9FA")
        
        # Get image loader instance
        self.loader = get_image_loader()
        
        # Create notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add demo tabs
        self._create_logo_tab()
        self._create_icons_tab()
        self._create_event_images_tab()
        self._create_resource_images_tab()
        self._create_avatar_tab()
        self._create_unicode_icons_tab()
        self._create_cache_info_tab()
    
    def _create_logo_tab(self):
        """Demo for loading logo"""
        frame = tk.Frame(self.notebook, bg="#F8F9FA")
        self.notebook.add(frame, text="Logo")
        
        container = tk.Frame(frame, bg="#F8F9FA")
        container.pack(expand=True)
        
        tk.Label(
            container,
            text="Application Logo",
            font=("Segoe UI", 16, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(0, 20))
        
        # Load logo at different sizes
        sizes = [(400, 200), (300, 150), (200, 100), (150, 75)]
        
        for width, height in sizes:
            logo = self.loader.load_logo(size=(width, height))
            if logo:
                logo_label = tk.Label(container, image=logo, bg="#F8F9FA")
                logo_label.image = logo  # Keep reference
                logo_label.pack(pady=10)
                
                tk.Label(
                    container,
                    text=f"Size: {width}x{height}",
                    font=("Segoe UI", 9),
                    fg="#7F8C8D",
                    bg="#F8F9FA"
                ).pack()
        
        # Alternative: using convenience function
        tk.Label(
            container,
            text="\nUsing convenience function:",
            font=("Segoe UI", 10, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(20, 5))
        
        logo2 = load_logo(size=(200, 100))
        if logo2:
            logo_label2 = tk.Label(container, image=logo2, bg="#F8F9FA")
            logo_label2.image = logo2
            logo_label2.pack(pady=5)
    
    def _create_icons_tab(self):
        """Demo for loading icons"""
        frame = tk.Frame(self.notebook, bg="#F8F9FA")
        self.notebook.add(frame, text="Icons (PNG)")
        
        # Scrollable frame
        canvas = tk.Canvas(frame, bg="#F8F9FA", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F8F9FA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            scrollable_frame,
            text="Application Icons",
            font=("Segoe UI", 16, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(0, 20))
        
        # List of all icons
        icons = [
            'dashboard', 'events', 'resources', 'bookings',
            'profile', 'settings', 'notifications', 'search',
            'add', 'edit', 'delete', 'approve', 'reject', 'logout'
        ]
        
        # Grid layout for icons
        grid_frame = tk.Frame(scrollable_frame, bg="#F8F9FA")
        grid_frame.pack()
        
        cols = 4
        for idx, icon_name in enumerate(icons):
            row = idx // cols
            col = idx % cols
            
            icon_frame = tk.Frame(grid_frame, bg="white", padx=20, pady=20)
            icon_frame.grid(row=row, column=col, padx=10, pady=10)
            
            # Load icon at different sizes
            sizes = [(48, 48), (32, 32), (24, 24)]
            
            for size in sizes:
                icon = self.loader.load_icon(icon_name, size=size)
                if icon:
                    icon_label = tk.Label(icon_frame, image=icon, bg="white")
                    icon_label.image = icon
                    icon_label.pack(pady=2)
            
            tk.Label(
                icon_frame,
                text=icon_name.capitalize(),
                font=("Segoe UI", 9),
                bg="white"
            ).pack(pady=(5, 0))
        
        # Icon usage example
        tk.Label(
            scrollable_frame,
            text="\nUsage Example:",
            font=("Segoe UI", 10, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(20, 5))
        
        code_example = """
# Load icon
icon = load_icon("dashboard", size=(24, 24))

# Use in label
label = tk.Label(parent, image=icon)
label.image = icon  # Keep reference!
label.pack()
        """
        
        tk.Label(
            scrollable_frame,
            text=code_example,
            font=("Courier", 9),
            bg="#2C3E50",
            fg="white",
            justify="left",
            padx=10,
            pady=10
        ).pack(padx=20)
    
    def _create_event_images_tab(self):
        """Demo for event images"""
        frame = tk.Frame(self.notebook, bg="#F8F9FA")
        self.notebook.add(frame, text="Event Images")
        
        container = tk.Frame(frame, bg="#F8F9FA")
        container.pack(expand=True, pady=20)
        
        tk.Label(
            container,
            text="Event Image Loading",
            font=("Segoe UI", 16, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(0, 20))
        
        # Load event placeholder
        event_img = self.loader.load_event_image(None, size=(300, 200))
        if event_img:
            img_label = tk.Label(container, image=event_img, bg="#F8F9FA")
            img_label.image = event_img
            img_label.pack(pady=10)
        
        tk.Label(
            container,
            text="Event Placeholder (auto-generated)",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="#F8F9FA"
        ).pack()
        
        # Load actual event placeholder file
        tk.Label(
            container,
            text="\nActual Event Placeholder File:",
            font=("Segoe UI", 10, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(20, 10))
        
        event_img2 = self.loader.load_image("event_placeholder.png", size=(250, 167))
        if event_img2:
            img_label2 = tk.Label(container, image=event_img2, bg="#F8F9FA")
            img_label2.image = event_img2
            img_label2.pack(pady=10)
        
        # Usage example
        tk.Label(
            container,
            text="\nUsage in Event Card:",
            font=("Segoe UI", 10, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(20, 5))
        
        code = """
# Load event image (with fallback)
event_image = loader.load_event_image(
    event.get('image_filename'),
    size=(300, 200)
)

# Display in card
img_label = tk.Label(card, image=event_image)
img_label.image = event_image  # Keep reference
img_label.pack()
        """
        
        tk.Label(
            container,
            text=code,
            font=("Courier", 9),
            bg="#2C3E50",
            fg="white",
            justify="left",
            padx=10,
            pady=10
        ).pack(padx=20)
    
    def _create_resource_images_tab(self):
        """Demo for resource images"""
        frame = tk.Frame(self.notebook, bg="#F8F9FA")
        self.notebook.add(frame, text="Resource Images")
        
        container = tk.Frame(frame, bg="#F8F9FA")
        container.pack(expand=True, pady=20)
        
        tk.Label(
            container,
            text="Resource Image Loading",
            font=("Segoe UI", 16, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(0, 20))
        
        # Load resource placeholder
        resource_img = self.loader.load_resource_image(None, size=(300, 200))
        if resource_img:
            img_label = tk.Label(container, image=resource_img, bg="#F8F9FA")
            img_label.image = resource_img
            img_label.pack(pady=10)
        
        tk.Label(
            container,
            text="Resource Placeholder (auto-generated)",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="#F8F9FA"
        ).pack()
        
        # Load actual resource placeholder file
        tk.Label(
            container,
            text="\nActual Resource Placeholder File:",
            font=("Segoe UI", 10, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(20, 10))
        
        resource_img2 = self.loader.load_image("resource_placeholder.png", size=(250, 167))
        if resource_img2:
            img_label2 = tk.Label(container, image=resource_img2, bg="#F8F9FA")
            img_label2.image = resource_img2
            img_label2.pack(pady=10)
    
    def _create_avatar_tab(self):
        """Demo for user avatars"""
        frame = tk.Frame(self.notebook, bg="#F8F9FA")
        self.notebook.add(frame, text="User Avatars")
        
        container = tk.Frame(frame, bg="#F8F9FA")
        container.pack(expand=True, pady=20)
        
        tk.Label(
            container,
            text="User Avatar Loading",
            font=("Segoe UI", 16, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(0, 20))
        
        # Different avatar sizes
        sizes = [(150, 150), (100, 100), (64, 64), (48, 48)]
        
        size_frame = tk.Frame(container, bg="#F8F9FA")
        size_frame.pack()
        
        for width, height in sizes:
            avatar = self.loader.load_user_avatar(None, size=(width, height))
            if avatar:
                avatar_label = tk.Label(size_frame, image=avatar, bg="#F8F9FA")
                avatar_label.image = avatar
                avatar_label.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            container,
            text="Avatar sizes: 150x150, 100x100, 64x64, 48x48",
            font=("Segoe UI", 9),
            fg="#7F8C8D",
            bg="#F8F9FA"
        ).pack(pady=10)
        
        # Load actual avatar placeholder file
        tk.Label(
            container,
            text="\nActual Avatar Placeholder File:",
            font=("Segoe UI", 10, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(20, 10))
        
        avatar_img = self.loader.load_image("avatar_placeholder.png", size=(150, 150))
        if avatar_img:
            img_label = tk.Label(container, image=avatar_img, bg="#F8F9FA")
            img_label.image = avatar_img
            img_label.pack(pady=10)
    
    def _create_unicode_icons_tab(self):
        """Demo for Unicode emoji icons"""
        frame = tk.Frame(self.notebook, bg="#F8F9FA")
        self.notebook.add(frame, text="Unicode Icons")
        
        # Scrollable frame
        canvas = tk.Canvas(frame, bg="#F8F9FA", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F8F9FA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            scrollable_frame,
            text="Unicode Emoji Icons (IconSet)",
            font=("Segoe UI", 16, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(0, 20))
        
        tk.Label(
            scrollable_frame,
            text="Use these icons when PNG files are not available or for quick prototyping",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="#F8F9FA",
            wraplength=600
        ).pack(pady=(0, 20))
        
        # Navigation icons
        self._add_icon_section(scrollable_frame, "Navigation Icons", [
            ('DASHBOARD', IconSet.DASHBOARD),
            ('EVENTS', IconSet.EVENTS),
            ('RESOURCES', IconSet.RESOURCES),
            ('BOOKINGS', IconSet.BOOKINGS),
            ('PROFILE', IconSet.PROFILE),
            ('SETTINGS', IconSet.SETTINGS),
            ('NOTIFICATIONS', IconSet.NOTIFICATIONS),
            ('LOGOUT', IconSet.LOGOUT)
        ])
        
        # Action icons
        self._add_icon_section(scrollable_frame, "Action Icons", [
            ('SEARCH', IconSet.SEARCH),
            ('ADD', IconSet.ADD),
            ('EDIT', IconSet.EDIT),
            ('DELETE', IconSet.DELETE),
            ('SAVE', IconSet.SAVE),
            ('CANCEL', IconSet.CANCEL),
            ('APPROVE', IconSet.APPROVE),
            ('REJECT', IconSet.REJECT),
            ('REFRESH', IconSet.REFRESH),
            ('DOWNLOAD', IconSet.DOWNLOAD),
            ('UPLOAD', IconSet.UPLOAD)
        ])
        
        # Status icons
        self._add_icon_section(scrollable_frame, "Status Icons", [
            ('SUCCESS', IconSet.SUCCESS),
            ('ERROR', IconSet.ERROR),
            ('WARNING', IconSet.WARNING),
            ('INFO', IconSet.INFO),
            ('PENDING', IconSet.PENDING),
            ('ACTIVE', IconSet.ACTIVE),
            ('INACTIVE', IconSet.INACTIVE)
        ])
        
        # Content icons
        self._add_icon_section(scrollable_frame, "Content Icons", [
            ('EMAIL', IconSet.EMAIL),
            ('PHONE', IconSet.PHONE),
            ('LOCATION', IconSet.LOCATION),
            ('CALENDAR', IconSet.CALENDAR),
            ('CLOCK', IconSet.CLOCK),
            ('USER', IconSet.USER),
            ('USERS', IconSet.USERS),
            ('BUILDING', IconSet.BUILDING)
        ])
        
        # Category icons
        self._add_icon_section(scrollable_frame, "Category Icons", [
            ('ACADEMIC', IconSet.ACADEMIC),
            ('SPORTS', IconSet.SPORTS),
            ('CULTURAL', IconSet.CULTURAL),
            ('WORKSHOP', IconSet.WORKSHOP),
            ('SEMINAR', IconSet.SEMINAR),
            ('CONFERENCE', IconSet.CONFERENCE),
            ('SOCIAL', IconSet.SOCIAL)
        ])
        
        # Usage example
        tk.Label(
            scrollable_frame,
            text="\nUsage Example:",
            font=("Segoe UI", 12, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(30, 10))
        
        code = """
from utils.image_loader import IconSet

# Use in labels
dashboard_label = tk.Label(
    parent,
    text=f"{IconSet.DASHBOARD} Dashboard",
    font=("Segoe UI", 12)
)

# Dynamic icon selection
category = "academic"
icon = IconSet.get_category_icon(category)
label = tk.Label(parent, text=f"{icon} {category.capitalize()}")

# Status icon
status = "approved"
icon = IconSet.get_status_icon(status)
label = tk.Label(parent, text=f"{icon} {status.capitalize()}")
        """
        
        tk.Label(
            scrollable_frame,
            text=code,
            font=("Courier", 9),
            bg="#2C3E50",
            fg="white",
            justify="left",
            padx=15,
            pady=15
        ).pack(padx=20, pady=(0, 20))
    
    def _add_icon_section(self, parent, title, icons):
        """Helper to add icon section"""
        section_frame = tk.Frame(parent, bg="white", padx=20, pady=15)
        section_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            section_frame,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(0, 10))
        
        grid_frame = tk.Frame(section_frame, bg="white")
        grid_frame.pack(fill=tk.X)
        
        cols = 4
        for idx, (name, icon) in enumerate(icons):
            row = idx // cols
            col = idx % cols
            
            icon_frame = tk.Frame(grid_frame, bg="#F8F9FA", padx=15, pady=10)
            icon_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            tk.Label(
                icon_frame,
                text=icon,
                font=("Segoe UI", 24),
                bg="#F8F9FA"
            ).pack()
            
            tk.Label(
                icon_frame,
                text=name,
                font=("Segoe UI", 8),
                fg="#7F8C8D",
                bg="#F8F9FA"
            ).pack()
        
        # Configure grid columns to expand equally
        for col in range(cols):
            grid_frame.columnconfigure(col, weight=1)
    
    def _create_cache_info_tab(self):
        """Demo for cache information"""
        frame = tk.Frame(self.notebook, bg="#F8F9FA")
        self.notebook.add(frame, text="Cache Info")
        
        container = tk.Frame(frame, bg="#F8F9FA")
        container.pack(expand=True, pady=20)
        
        tk.Label(
            container,
            text="Image Cache Information",
            font=("Segoe UI", 16, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(0, 20))
        
        # Cache stats
        stats_frame = tk.Frame(container, bg="white", padx=30, pady=20)
        stats_frame.pack(padx=20)
        
        cache_size = self.loader.get_cache_size()
        
        tk.Label(
            stats_frame,
            text=f"Cached Images: {cache_size}",
            font=("Segoe UI", 14),
            bg="white"
        ).pack(pady=10)
        
        tk.Label(
            stats_frame,
            text="The image loader automatically caches loaded images",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="white"
        ).pack()
        
        tk.Label(
            stats_frame,
            text="to avoid redundant file I/O operations.",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="white"
        ).pack()
        
        # Cache methods
        tk.Label(
            container,
            text="\nCache Management Methods:",
            font=("Segoe UI", 12, "bold"),
            bg="#F8F9FA"
        ).pack(pady=(30, 10))
        
        methods = """
# Get cache size
cache_size = loader.get_cache_size()

# Clear entire cache
loader.clear_cache()

# Remove specific image from cache
loader.remove_from_cache("logo.png", size=(200, 100))

# Preload icons for better performance
loader.preload_icons(
    ['dashboard', 'events', 'resources'],
    size=(24, 24)
)
        """
        
        tk.Label(
            container,
            text=methods,
            font=("Courier", 10),
            bg="#2C3E50",
            fg="white",
            justify="left",
            padx=15,
            pady=15
        ).pack(padx=20)
        
        # Refresh button
        tk.Button(
            container,
            text="Refresh Cache Info",
            command=lambda: self._refresh_cache_info(stats_frame, cache_size),
            bg="#3498DB",
            fg="white",
            font=("Segoe UI", 10),
            padx=20,
            pady=10,
            relief="flat"
        ).pack(pady=20)
    
    def _refresh_cache_info(self, stats_frame, old_size):
        """Refresh cache information"""
        new_size = self.loader.get_cache_size()
        
        # Update label
        for widget in stats_frame.winfo_children():
            if isinstance(widget, tk.Label) and "Cached Images:" in widget.cget("text"):
                widget.config(text=f"Cached Images: {new_size}")
                break


if __name__ == "__main__":
    app = ImageLoaderDemo()
    app.mainloop()
