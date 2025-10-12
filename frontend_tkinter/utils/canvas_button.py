"""
Canvas Button Utilities - macOS Compatible Buttons
Creates canvas-based buttons that properly display colors on macOS
"""

import tkinter as tk
from typing import Callable, Optional


class CanvasButton:
    """
    Canvas-based button for macOS compatibility.
    Regular tk.Button ignores bg color on macOS, so we use canvas instead.
    """
    
    def __init__(self, parent, text: str, command: Optional[Callable] = None,
                 width: int = 120, height: int = 40,
                 bg_color: str = '#3047ff', fg_color: str = 'white',
                 hover_color: str = '#1e3acc', disabled_color: str = '#64748B',
                 font: tuple = ("Helvetica", 11, "bold"),
                 **kwargs):
        """
        Create a canvas-based button.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Function to call on click
            width: Button width in pixels
            height: Button height in pixels
            bg_color: Background color
            fg_color: Text color
            hover_color: Background color on hover
            disabled_color: Background color when disabled
            font: Font tuple (family, size, weight)
        """
        self.parent = parent
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self.font = font
        self.enabled = True
        
        # Get parent background for transparent canvas
        parent_bg = kwargs.get('canvas_bg', parent.cget('bg') if hasattr(parent, 'cget') else '#ffffff')
        
        # Create canvas
        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg=parent_bg,
            highlightthickness=0
        )
        
        # Draw button
        self.rect = self.canvas.create_rectangle(
            0, 0, width, height,
            fill=bg_color,
            outline='',
            tags='btn'
        )
        
        self.text_item = self.canvas.create_text(
            width/2, height/2,
            text=text,
            font=font,
            fill=fg_color,
            tags='btn'
        )
        
        # Bind events
        if command:
            self.canvas.tag_bind('btn', '<Button-1>', self._on_click)
        self.canvas.tag_bind('btn', '<Enter>', self._on_enter)
        self.canvas.tag_bind('btn', '<Leave>', self._on_leave)
        self.canvas.config(cursor='hand2' if command else 'arrow')
    
    def _on_click(self, event):
        """Handle button click."""
        if self.enabled and self.command:
            self.command()
    
    def _on_enter(self, event):
        """Handle mouse enter."""
        if self.enabled:
            self.canvas.itemconfig(self.rect, fill=self.hover_color)
    
    def _on_leave(self, event):
        """Handle mouse leave."""
        if self.enabled:
            self.canvas.itemconfig(self.rect, fill=self.bg_color)
        else:
            self.canvas.itemconfig(self.rect, fill=self.disabled_color)
    
    def pack(self, **kwargs):
        """Pack the canvas."""
        self.canvas.pack(**kwargs)
        return self
    
    def grid(self, **kwargs):
        """Grid the canvas."""
        self.canvas.grid(**kwargs)
        return self
    
    def place(self, **kwargs):
        """Place the canvas."""
        self.canvas.place(**kwargs)
        return self
    
    def config(self, **kwargs):
        """Configure button properties."""
        if 'text' in kwargs:
            self.text = kwargs['text']
            self.canvas.itemconfig(self.text_item, text=self.text)
        if 'state' in kwargs:
            state = kwargs['state']
            if state == 'disabled' or state == tk.DISABLED:
                self.set_enabled(False)
            elif state == 'normal' or state == tk.NORMAL:
                self.set_enabled(True)
        if 'bg' in kwargs:
            self.bg_color = kwargs['bg']
            if self.enabled:
                self.canvas.itemconfig(self.rect, fill=self.bg_color)
        if 'fg' in kwargs:
            self.fg_color = kwargs['fg']
            self.canvas.itemconfig(self.text_item, fill=self.fg_color)
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the button."""
        self.enabled = enabled
        if enabled:
            self.canvas.itemconfig(self.rect, fill=self.bg_color)
            self.canvas.itemconfig(self.text_item, fill=self.fg_color)
            self.canvas.config(cursor='hand2')
        else:
            self.canvas.itemconfig(self.rect, fill=self.disabled_color)
            self.canvas.itemconfig(self.text_item, fill='#94A3B8')
            self.canvas.config(cursor='arrow')
    
    def set_text(self, text: str):
        """Update button text."""
        self.text = text
        self.canvas.itemconfig(self.text_item, text=text)
    
    def set_loading(self, loading: bool, loading_text: str = "Loading..."):
        """Set loading state."""
        if loading:
            self.set_enabled(False)
            self.set_text(loading_text)
            self.canvas.itemconfig(self.rect, fill=self.disabled_color)
        else:
            self.set_enabled(True)
            self.canvas.itemconfig(self.rect, fill=self.bg_color)


# Color presets for different button variants
class ButtonColors:
    """Color presets for canvas buttons."""
    
    PRIMARY = {
        'bg_color': '#3047ff',
        'hover_color': '#1e3acc',
        'fg_color': 'white'
    }
    
    SECONDARY = {
        'bg_color': '#F3F4F6',
        'hover_color': '#E5E7EB',
        'fg_color': '#1F2937'
    }
    
    SUCCESS = {
        'bg_color': '#28a745',
        'hover_color': '#218838',
        'fg_color': 'white'
    }
    
    DANGER = {
        'bg_color': '#dc3545',
        'hover_color': '#c82333',
        'fg_color': 'white'
    }
    
    WARNING = {
        'bg_color': '#ffc107',
        'hover_color': '#e0a800',
        'fg_color': 'black'
    }
    
    INFO = {
        'bg_color': '#17a2b8',
        'hover_color': '#138496',
        'fg_color': 'white'
    }
    
    LIGHT = {
        'bg_color': '#f8f9fa',
        'hover_color': '#e2e6ea',
        'fg_color': 'black'
    }
    
    DARK = {
        'bg_color': '#343a40',
        'hover_color': '#23272b',
        'fg_color': 'white'
    }


def create_canvas_button(parent, text: str, command: Optional[Callable] = None,
                        variant: str = 'primary', width: int = 120, height: int = 40,
                        **kwargs) -> CanvasButton:
    """
    Factory function to create a canvas button with preset colors.
    
    Args:
        parent: Parent widget
        text: Button text
        command: Function to call on click
        variant: Color variant (primary, secondary, success, danger, warning, info, light, dark)
        width: Button width
        height: Button height
        **kwargs: Additional arguments passed to CanvasButton
    
    Returns:
        CanvasButton instance
    
    Example:
        # Primary button
        btn = create_canvas_button(frame, "Save", command=save_func, variant='primary')
        btn.pack(padx=10, pady=10)
        
        # Success button with custom size
        btn = create_canvas_button(frame, "Submit", command=submit, variant='success', width=150, height=45)
        btn.grid(row=0, column=0)
    """
    # Get color preset
    color_map = {
        'primary': ButtonColors.PRIMARY,
        'secondary': ButtonColors.SECONDARY,
        'success': ButtonColors.SUCCESS,
        'danger': ButtonColors.DANGER,
        'warning': ButtonColors.WARNING,
        'info': ButtonColors.INFO,
        'light': ButtonColors.LIGHT,
        'dark': ButtonColors.DARK
    }
    
    colors = color_map.get(variant.lower(), ButtonColors.PRIMARY)
    
    # Merge colors with kwargs
    button_kwargs = {**colors, **kwargs}
    
    return CanvasButton(parent, text, command, width, height, **button_kwargs)


# Convenience functions for common button types
def create_primary_button(parent, text, command=None, width=120, height=40, **kwargs):
    """Create a primary (blue) button."""
    return create_canvas_button(parent, text, command, 'primary', width, height, **kwargs)


def create_secondary_button(parent, text, command=None, width=120, height=40, **kwargs):
    """Create a secondary (gray) button."""
    return create_canvas_button(parent, text, command, 'secondary', width, height, **kwargs)


def create_success_button(parent, text, command=None, width=120, height=40, **kwargs):
    """Create a success (green) button."""
    return create_canvas_button(parent, text, command, 'success', width, height, **kwargs)


def create_danger_button(parent, text, command=None, width=120, height=40, **kwargs):
    """Create a danger (red) button."""
    return create_canvas_button(parent, text, command, 'danger', width, height, **kwargs)


def create_warning_button(parent, text, command=None, width=120, height=40, **kwargs):
    """Create a warning (orange/yellow) button."""
    return create_canvas_button(parent, text, command, 'warning', width, height, **kwargs)


def create_icon_button(parent, icon, command=None, size=40, variant='secondary', **kwargs):
    """
    Create a small icon button (emoji or symbol).
    
    Args:
        parent: Parent widget
        icon: Icon character (emoji or symbol)
        command: Function to call on click
        size: Button size (width and height)
        variant: Color variant
    
    Returns:
        CanvasButton instance
    """
    return create_canvas_button(parent, icon, command, variant, size, size, 
                                font=('Arial', 14), **kwargs)
