"""
Button Styling Utilities for Campus Event System

Provides consistent, high-contrast button configurations for better visibility.
All buttons use explicit colors to ensure text is always visible.
"""

import tkinter as tk
from typing import Callable, Optional


class ButtonStyles:
    """Centralized button style configurations"""
    
    # Color definitions with high contrast
    COLORS = {
        'primary': {
            'bg': '#3498DB',
            'fg': '#FFFFFF',
            'active_bg': '#2980B9',
            'active_fg': '#FFFFFF'
        },
        'success': {
            'bg': '#27AE60',
            'fg': '#FFFFFF',
            'active_bg': '#229954',
            'active_fg': '#FFFFFF'
        },
        'danger': {
            'bg': '#E74C3C',
            'fg': '#FFFFFF',
            'active_bg': '#C0392B',
            'active_fg': '#FFFFFF'
        },
        'warning': {
            'bg': '#F39C12',
            'fg': '#FFFFFF',
            'active_bg': '#E67E22',
            'active_fg': '#FFFFFF'
        },
        'secondary': {
            'bg': '#95A5A6',
            'fg': '#FFFFFF',
            'active_bg': '#7F8C8D',
            'active_fg': '#FFFFFF'
        },
        'link': {
            'bg': 'white',
            'fg': '#3498DB',
            'active_bg': 'white',
            'active_fg': '#2980B9'
        },
        'dark': {
            'bg': '#2C3E50',
            'fg': '#FFFFFF',
            'active_bg': '#1A252F',
            'active_fg': '#FFFFFF'
        },
        'accent': {
            'bg': '#5DADE2',  # Lighter, friendlier blue
            'fg': '#FFFFFF',
            'active_bg': '#3498DB',
            'active_fg': '#FFFFFF'
        },
        'theme': {
            'bg': '#667eea',  # Rich purple-blue
            'fg': '#FFFFFF',
            'active_bg': '#5568d3',
            'active_fg': '#FFFFFF'
        }
    }
    
    @staticmethod
    def create_button(
        parent: tk.Widget,
        text: str,
        command: Optional[Callable] = None,
        variant: str = 'primary',
        width: Optional[int] = None,
        height: int = 2,
        **kwargs
    ) -> tk.Canvas:
        """
        Create a Canvas-based styled button with guaranteed color visibility on macOS.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Button command callback
            variant: Color variant (primary, success, danger, warning, secondary, link, dark)
            width: Button width in pixels (optional, default: 120)
            height: Button height in text lines (default: 2)
            **kwargs: Additional arguments
        
        Returns:
            Canvas widget acting as a button
        """
        colors = ButtonStyles.COLORS.get(variant, ButtonStyles.COLORS['primary'])
        
        # Calculate dimensions
        btn_width = width if width else 120
        btn_height = height * 20  # Approximate pixels per line
        
        # Create canvas
        canvas = tk.Canvas(
            parent,
            width=btn_width,
            height=btn_height,
            bg=parent.cget('bg') if hasattr(parent, 'cget') else 'white',
            highlightthickness=0,
            cursor='hand2'
        )
        
        # Draw button background (rounded rectangle)
        padding = 2
        rect = canvas.create_rectangle(
            padding, padding, 
            btn_width - padding, btn_height - padding,
            fill=colors['bg'],
            outline='',
            tags='button_bg'
        )
        
        # Draw button text
        text_item = canvas.create_text(
            btn_width // 2, btn_height // 2,
            text=text,
            fill=colors['fg'],
            font=('Helvetica', 11, 'bold'),
            tags='button_text'
        )
        
        # Store colors for hover effects
        canvas.normal_color = colors['bg']
        canvas.hover_color = colors['active_bg']
        canvas.rect_id = rect
        
        # Bind click events
        if command:
            canvas.tag_bind('button_bg', '<Button-1>', lambda e: command())
            canvas.tag_bind('button_text', '<Button-1>', lambda e: command())
            canvas.bind('<Button-1>', lambda e: command())
        
        # Hover effects
        def on_enter(e):
            canvas.itemconfig(rect, fill=canvas.hover_color)
        
        def on_leave(e):
            canvas.itemconfig(rect, fill=canvas.normal_color)
        
        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
        
        return canvas
    
    @staticmethod
    def create_icon_button(
        parent: tk.Widget,
        text: str,
        command: Optional[Callable] = None,
        **kwargs
    ) -> tk.Canvas:
        """
        Create a Canvas-based icon button.
        
        Args:
            parent: Parent widget
            text: Button text (usually emoji or icon)
            command: Button command callback
            **kwargs: Additional arguments
        
        Returns:
            Canvas widget acting as an icon button
        """
        canvas = tk.Canvas(
            parent,
            width=40,
            height=40,
            bg='white',
            highlightthickness=1,
            highlightbackground='#E0E0E0',
            cursor='hand2'
        )
        
        # Draw background circle/rectangle
        rect = canvas.create_rectangle(
            2, 2, 38, 38,
            fill='white',
            outline='',
            tags='button_bg'
        )
        
        # Draw icon text
        text_item = canvas.create_text(
            20, 20,
            text=text,
            fill='#2C3E50',
            font=('Helvetica', 14),
            tags='button_text'
        )
        
        # Bind click
        if command:
            canvas.tag_bind('button_bg', '<Button-1>', lambda e: command())
            canvas.tag_bind('button_text', '<Button-1>', lambda e: command())
            canvas.bind('<Button-1>', lambda e: command())
        
        # Hover effect
        def on_enter(e):
            canvas.itemconfig(rect, fill='#ECF0F1')
        
        def on_leave(e):
            canvas.itemconfig(rect, fill='white')
        
        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
        
        return canvas
    
    @staticmethod
    def create_link_button(
        parent: tk.Widget,
        text: str,
        command: Optional[Callable] = None,
        **kwargs
    ) -> tk.Canvas:
        """
        Create a Canvas-based text link button.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Button command callback
            **kwargs: Additional arguments
        
        Returns:
            Canvas widget acting as a link button
        """
        # Calculate text width
        temp_label = tk.Label(parent, text=text, font=('Helvetica', 10, 'bold'))
        temp_label.update_idletasks()
        text_width = temp_label.winfo_reqwidth()
        temp_label.destroy()
        
        canvas = tk.Canvas(
            parent,
            width=text_width + 4,
            height=25,
            bg=kwargs.get('bg', 'white'),
            highlightthickness=0,
            cursor='hand2'
        )
        
        # Draw text
        text_item = canvas.create_text(
            (text_width + 4) // 2, 12,
            text=text,
            fill='#3498DB',
            font=('Helvetica', 10, 'bold'),
            tags='link_text'
        )
        
        # Bind click
        if command:
            canvas.tag_bind('link_text', '<Button-1>', lambda e: command())
            canvas.bind('<Button-1>', lambda e: command())
        
        # Hover effect - change color and add underline
        def on_enter(e):
            canvas.itemconfig(text_item, fill='#2980B9')
            # Add underline
            bbox = canvas.bbox(text_item)
            if bbox:
                canvas.create_line(
                    bbox[0], bbox[3], bbox[2], bbox[3],
                    fill='#2980B9',
                    tags='underline'
                )
        
        def on_leave(e):
            canvas.itemconfig(text_item, fill='#3498DB')
            canvas.delete('underline')
        
        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
        
        return canvas


def apply_button_hover_effect(button: tk.Button, enter_color: str, leave_color: str):
    """
    Add hover effect to a button.
    
    Args:
        button: The button widget
        enter_color: Background color on hover
        leave_color: Background color when not hovering
    """
    def on_enter(e):
        button['bg'] = enter_color
    
    def on_leave(e):
        button['bg'] = leave_color
    
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)
