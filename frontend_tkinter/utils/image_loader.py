"""
Image Loader and Caching Utility

This module provides utilities for loading, caching, and managing images and icons
throughout the Campus Event System application.

Features:
    - Image caching for performance
    - Automatic resizing
    - Icon set management
    - Placeholder image generation
    - PIL/Pillow integration
    - Fallback for missing images

Author: Campus Event System Team
Version: 1.0.0
"""

import os
import io
import base64
from typing import Optional, Tuple, Dict
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk


class ImageLoader:
    """
    Centralized image loading and caching system.
    
    Features:
        - Loads and caches images to avoid redundant file I/O
        - Automatically resizes images to specified dimensions
        - Generates placeholder images when files are missing
        - Supports PNG, JPG, GIF formats
        - Thread-safe caching
    
    Example:
        loader = ImageLoader.get_instance()
        
        # Load logo
        logo = loader.load_image("logo.png", size=(200, 100))
        
        # Load icon
        icon = loader.load_icon("dashboard", size=(24, 24))
        
        # Load event image with fallback
        event_img = loader.load_event_image("event123.jpg", size=(300, 200))
    """
    
    _instance = None
    
    def __init__(self):
        self.cache: Dict[str, ImageTk.PhotoImage] = {}
        self.base_path = self._get_base_path()
        self.icons_path = os.path.join(self.base_path, "assets", "icons")
        self.images_path = os.path.join(self.base_path, "assets", "images")
        
        # Ensure directories exist
        os.makedirs(self.icons_path, exist_ok=True)
        os.makedirs(self.images_path, exist_ok=True)
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance of ImageLoader"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _get_base_path(self) -> str:
        """Get base path of the application"""
        current_file = os.path.abspath(__file__)
        # Go up two levels from utils/image_loader.py to frontend_tkinter/
        base_path = os.path.dirname(os.path.dirname(current_file))
        return base_path
    
    def _generate_cache_key(self, path: str, size: Optional[Tuple[int, int]]) -> str:
        """Generate unique cache key for image"""
        size_str = f"{size[0]}x{size[1]}" if size else "original"
        return f"{path}_{size_str}"
    
    def load_image(
        self,
        filename: str,
        size: Optional[Tuple[int, int]] = None,
        folder: str = "images"
    ) -> Optional[ImageTk.PhotoImage]:
        """
        Load an image from assets folder with caching.
        
        Args:
            filename: Image filename (e.g., "logo.png")
            size: Optional (width, height) tuple for resizing
            folder: Subfolder in assets ("images" or "icons")
        
        Returns:
            ImageTk.PhotoImage object or None if failed
        """
        # Check cache first
        cache_key = self._generate_cache_key(filename, size)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Construct full path
        if folder == "icons":
            full_path = os.path.join(self.icons_path, filename)
        else:
            full_path = os.path.join(self.images_path, filename)
        
        try:
            # Load image
            if os.path.exists(full_path):
                image = Image.open(full_path)
            else:
                # Generate placeholder if file doesn't exist
                image = self._generate_placeholder(size or (100, 100), filename)
            
            # Resize if needed
            if size:
                image = image.resize(size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Cache it
            self.cache[cache_key] = photo
            
            return photo
        
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
            # Return placeholder on error
            placeholder = self._generate_placeholder(size or (100, 100), "Error")
            photo = ImageTk.PhotoImage(placeholder)
            self.cache[cache_key] = photo
            return photo
    
    def load_icon(
        self,
        icon_name: str,
        size: Tuple[int, int] = (24, 24)
    ) -> Optional[ImageTk.PhotoImage]:
        """
        Load an icon from icons folder.
        
        Args:
            icon_name: Icon name without extension (e.g., "dashboard")
            size: Icon size (default: 24x24)
        
        Returns:
            ImageTk.PhotoImage object
        """
        # Try PNG first, then JPG
        for ext in ['.png', '.jpg', '.jpeg', '.gif']:
            filename = f"{icon_name}{ext}"
            full_path = os.path.join(self.icons_path, filename)
            if os.path.exists(full_path):
                return self.load_image(filename, size=size, folder="icons")
        
        # If no file found, generate colored placeholder
        return self._generate_icon_placeholder(icon_name, size)
    
    def load_event_image(
        self,
        filename: Optional[str],
        size: Tuple[int, int] = (300, 200)
    ) -> ImageTk.PhotoImage:
        """
        Load event image with fallback to placeholder.
        
        Args:
            filename: Image filename or None
            size: Image size
        
        Returns:
            ImageTk.PhotoImage object
        """
        if filename:
            return self.load_image(filename, size=size, folder="images")
        else:
            # Generate event placeholder
            placeholder = self._generate_event_placeholder(size)
            cache_key = f"event_placeholder_{size[0]}x{size[1]}"
            photo = ImageTk.PhotoImage(placeholder)
            self.cache[cache_key] = photo
            return photo
    
    def load_resource_image(
        self,
        filename: Optional[str],
        size: Tuple[int, int] = (300, 200)
    ) -> ImageTk.PhotoImage:
        """
        Load resource image with fallback to placeholder.
        
        Args:
            filename: Image filename or None
            size: Image size
        
        Returns:
            ImageTk.PhotoImage object
        """
        if filename:
            return self.load_image(filename, size=size, folder="images")
        else:
            # Generate resource placeholder
            placeholder = self._generate_resource_placeholder(size)
            cache_key = f"resource_placeholder_{size[0]}x{size[1]}"
            photo = ImageTk.PhotoImage(placeholder)
            self.cache[cache_key] = photo
            return photo
    
    def load_user_avatar(
        self,
        filename: Optional[str],
        size: Tuple[int, int] = (100, 100)
    ) -> ImageTk.PhotoImage:
        """
        Load user avatar with circular crop and fallback.
        
        Args:
            filename: Image filename or None
            size: Avatar size (square)
        
        Returns:
            ImageTk.PhotoImage object
        """
        if filename:
            image = self.load_image(filename, size=size, folder="images")
            # TODO: Add circular crop
            return image
        else:
            # Generate avatar placeholder
            placeholder = self._generate_avatar_placeholder(size)
            cache_key = f"avatar_placeholder_{size[0]}x{size[1]}"
            photo = ImageTk.PhotoImage(placeholder)
            self.cache[cache_key] = photo
            return photo
    
    def _generate_placeholder(
        self,
        size: Tuple[int, int],
        text: str = "No Image"
    ) -> Image.Image:
        """Generate a simple placeholder image"""
        image = Image.new('RGB', size, color='#E0E0E0')
        draw = ImageDraw.Draw(image)
        
        # Try to use a font, fall back to default if not available
        try:
            font = ImageFont.truetype("Arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        x = (size[0] - text_width) / 2
        y = (size[1] - text_height) / 2
        
        draw.text((x, y), text, fill='#757575', font=font)
        
        return image
    
    def _generate_icon_placeholder(
        self,
        icon_name: str,
        size: Tuple[int, int]
    ) -> ImageTk.PhotoImage:
        """Generate colored placeholder for icon"""
        # Color mapping for different icon types
        color_map = {
            'dashboard': '#3498DB',
            'events': '#E74C3C',
            'resources': '#27AE60',
            'bookings': '#F39C12',
            'profile': '#9B59B6',
            'settings': '#95A5A6',
            'notifications': '#E91E63',
            'search': '#2ECC71',
            'add': '#16A085',
            'edit': '#2980B9',
            'delete': '#C0392B',
            'approve': '#27AE60',
            'reject': '#E74C3C',
            'logout': '#7F8C8D'
        }
        
        color = color_map.get(icon_name.lower(), '#3498DB')
        
        image = Image.new('RGBA', size, color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw colored circle
        margin = 2
        draw.ellipse(
            [margin, margin, size[0] - margin, size[1] - margin],
            fill=color,
            outline=None
        )
        
        cache_key = f"icon_placeholder_{icon_name}_{size[0]}x{size[1]}"
        photo = ImageTk.PhotoImage(image)
        self.cache[cache_key] = photo
        
        return photo
    
    def _generate_event_placeholder(self, size: Tuple[int, int]) -> Image.Image:
        """Generate event placeholder image"""
        image = Image.new('RGB', size, color='#3498DB')
        draw = ImageDraw.Draw(image)
        
        # Draw calendar icon representation
        icon_size = min(size[0], size[1]) // 3
        x = (size[0] - icon_size) // 2
        y = (size[1] - icon_size) // 2
        
        # Calendar body
        draw.rectangle(
            [x, y + icon_size // 4, x + icon_size, y + icon_size],
            fill='white',
            outline='white'
        )
        
        # Calendar header
        draw.rectangle(
            [x, y, x + icon_size, y + icon_size // 4],
            fill='#2980B9',
            outline='#2980B9'
        )
        
        # Add text
        try:
            font = ImageFont.truetype("Arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        text = "EVENT"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((size[0] - text_width) // 2, size[1] - 30),
            text,
            fill='white',
            font=font
        )
        
        return image
    
    def _generate_resource_placeholder(self, size: Tuple[int, int]) -> Image.Image:
        """Generate resource placeholder image"""
        image = Image.new('RGB', size, color='#27AE60')
        draw = ImageDraw.Draw(image)
        
        # Draw building icon representation
        icon_size = min(size[0], size[1]) // 3
        x = (size[0] - icon_size) // 2
        y = (size[1] - icon_size) // 2
        
        # Building body
        draw.rectangle(
            [x, y, x + icon_size, y + icon_size],
            fill='white',
            outline='white'
        )
        
        # Windows (grid)
        window_size = icon_size // 5
        for row in range(3):
            for col in range(2):
                wx = x + (col + 1) * (icon_size // 3)
                wy = y + (row + 1) * (icon_size // 4)
                draw.rectangle(
                    [wx - window_size // 2, wy - window_size // 2,
                     wx + window_size // 2, wy + window_size // 2],
                    fill='#27AE60'
                )
        
        # Add text
        try:
            font = ImageFont.truetype("Arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        text = "RESOURCE"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((size[0] - text_width) // 2, size[1] - 30),
            text,
            fill='white',
            font=font
        )
        
        return image
    
    def _generate_avatar_placeholder(self, size: Tuple[int, int]) -> Image.Image:
        """Generate user avatar placeholder"""
        image = Image.new('RGB', size, color='#9B59B6')
        draw = ImageDraw.Draw(image)
        
        # Draw simple person icon
        center_x = size[0] // 2
        center_y = size[1] // 2
        
        # Head (circle)
        head_radius = size[0] // 6
        draw.ellipse(
            [center_x - head_radius, center_y - size[1] // 4,
             center_x + head_radius, center_y - size[1] // 4 + head_radius * 2],
            fill='white'
        )
        
        # Body (partial circle/arc)
        body_radius = size[0] // 3
        draw.ellipse(
            [center_x - body_radius, center_y,
             center_x + body_radius, center_y + body_radius * 2],
            fill='white'
        )
        
        return image
    
    def load_logo(self, size: Optional[Tuple[int, int]] = None) -> ImageTk.PhotoImage:
        """
        Load application logo.
        
        Args:
            size: Optional size for logo
        
        Returns:
            ImageTk.PhotoImage object
        """
        return self.load_image("logo.png", size=size, folder="images")
    
    def clear_cache(self):
        """Clear all cached images"""
        self.cache.clear()
    
    def remove_from_cache(self, filename: str, size: Optional[Tuple[int, int]] = None):
        """Remove specific image from cache"""
        cache_key = self._generate_cache_key(filename, size)
        if cache_key in self.cache:
            del self.cache[cache_key]
    
    def preload_icons(self, icon_names: list, size: Tuple[int, int] = (24, 24)):
        """
        Preload multiple icons for better performance.
        
        Args:
            icon_names: List of icon names to preload
            size: Icon size
        """
        for icon_name in icon_names:
            self.load_icon(icon_name, size=size)
    
    def get_cache_size(self) -> int:
        """Get number of cached images"""
        return len(self.cache)


class IconSet:
    """
    Predefined icon set using Unicode emojis.
    
    This provides consistent icon usage across the application
    using Unicode emoji characters as fallback when image files
    are not available.
    
    Example:
        from utils.image_loader import IconSet
        
        # Use in labels
        tk.Label(parent, text=f"{IconSet.DASHBOARD} Dashboard")
        tk.Label(parent, text=f"{IconSet.EVENTS} Events")
    """
    
    # Navigation Icons
    DASHBOARD = "🏠"
    EVENTS = "📅"
    RESOURCES = "🏢"
    BOOKINGS = "📋"
    PROFILE = "👤"
    SETTINGS = "⚙️"
    NOTIFICATIONS = "🔔"
    LOGOUT = "🚪"
    
    # Action Icons
    SEARCH = "🔍"
    ADD = "➕"
    EDIT = "✏️"
    DELETE = "🗑️"
    SAVE = "💾"
    CANCEL = "❌"
    APPROVE = "✅"
    REJECT = "❌"
    REFRESH = "🔄"
    DOWNLOAD = "⬇️"
    UPLOAD = "⬆️"
    FILTER = "🔽"
    SORT = "⇅"
    
    # Status Icons
    SUCCESS = "✓"
    ERROR = "✕"
    WARNING = "⚠"
    INFO = "ℹ"
    PENDING = "⏳"
    ACTIVE = "🟢"
    INACTIVE = "🔴"
    
    # Content Icons
    EMAIL = "📧"
    PHONE = "📞"
    LOCATION = "📍"
    CALENDAR = "📅"
    CLOCK = "🕐"
    USER = "👤"
    USERS = "👥"
    BUILDING = "🏢"
    ROOM = "🚪"
    EQUIPMENT = "🖥️"
    
    # Category Icons
    ACADEMIC = "📚"
    SPORTS = "⚽"
    CULTURAL = "🎭"
    WORKSHOP = "🔧"
    SEMINAR = "💼"
    CONFERENCE = "🎤"
    SOCIAL = "🎉"
    
    # UI Icons
    MENU = "☰"
    CLOSE = "✕"
    BACK = "◀"
    FORWARD = "▶"
    UP = "▲"
    DOWN = "▼"
    LEFT = "◀"
    RIGHT = "▶"
    MORE = "⋯"
    EXPAND = "⊕"
    COLLAPSE = "⊖"
    
    # Document Icons
    FILE = "📄"
    PDF = "📕"
    IMAGE = "🖼️"
    VIDEO = "🎬"
    LINK = "🔗"
    ATTACHMENT = "📎"
    
    # Communication Icons
    CHAT = "💬"
    MESSAGE = "✉️"
    ANNOUNCEMENT = "📢"
    BELL = "🔔"
    
    @classmethod
    def get_category_icon(cls, category: str) -> str:
        """
        Get icon for event category.
        
        Args:
            category: Category name (case-insensitive)
        
        Returns:
            Unicode emoji icon
        """
        category_lower = category.lower()
        mapping = {
            'academic': cls.ACADEMIC,
            'sports': cls.SPORTS,
            'cultural': cls.CULTURAL,
            'workshop': cls.WORKSHOP,
            'seminar': cls.SEMINAR,
            'conference': cls.CONFERENCE,
            'social': cls.SOCIAL
        }
        return mapping.get(category_lower, cls.EVENTS)
    
    @classmethod
    def get_status_icon(cls, status: str) -> str:
        """
        Get icon for status.
        
        Args:
            status: Status name (case-insensitive)
        
        Returns:
            Unicode emoji icon
        """
        status_lower = status.lower()
        mapping = {
            'approved': cls.APPROVE,
            'rejected': cls.REJECT,
            'pending': cls.PENDING,
            'active': cls.ACTIVE,
            'inactive': cls.INACTIVE,
            'success': cls.SUCCESS,
            'error': cls.ERROR,
            'warning': cls.WARNING
        }
        return mapping.get(status_lower, cls.INFO)


# Singleton instance for easy access
_image_loader_instance = None

def get_image_loader() -> ImageLoader:
    """
    Get global ImageLoader instance.
    
    Returns:
        ImageLoader singleton instance
    """
    global _image_loader_instance
    if _image_loader_instance is None:
        _image_loader_instance = ImageLoader.get_instance()
    return _image_loader_instance


# Convenience functions

def load_image(filename: str, size: Optional[Tuple[int, int]] = None) -> Optional[ImageTk.PhotoImage]:
    """Convenience function to load image"""
    return get_image_loader().load_image(filename, size=size)

def load_icon(icon_name: str, size: Tuple[int, int] = (24, 24)) -> Optional[ImageTk.PhotoImage]:
    """Convenience function to load icon"""
    return get_image_loader().load_icon(icon_name, size=size)

def load_logo(size: Optional[Tuple[int, int]] = None) -> ImageTk.PhotoImage:
    """Convenience function to load logo"""
    return get_image_loader().load_logo(size=size)


# Export public API
__all__ = [
    'ImageLoader',
    'IconSet',
    'get_image_loader',
    'load_image',
    'load_icon',
    'load_logo'
]
