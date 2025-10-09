"""
Accessibility Module for Campus Event Management System
Version: 1.9.0
Created: October 9, 2025

This module provides comprehensive accessibility features including:
1. Keyboard navigation and shortcuts
2. Screen reader support (announcements)
3. Color contrast validation (WCAG AA compliance)
4. Font scaling support
5. Focus indicators and management
6. High contrast mode
7. Accessible form validation

Features:
- KeyboardNavigator: Manages keyboard shortcuts and tab order
- ScreenReaderAnnouncer: Announces changes for screen readers
- ColorContrastValidator: Validates WCAG AA color contrast
- FontScaler: Manages font size scaling
- FocusIndicator: Visible focus rings
- AccessibleForm: Form with keyboard support
- HighContrastMode: Toggle high contrast colors
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Callable, Optional, Tuple, Any
import threading
import time
import math
from collections import deque


class KeyboardNavigator:
    """
    Manages keyboard navigation and shortcuts throughout the application.
    
    Features:
    - Tab order management
    - Enter to submit forms
    - Escape to close modals/dialogs
    - Arrow keys for navigation
    - Custom keyboard shortcuts
    
    Usage:
        navigator = KeyboardNavigator(root)
        navigator.set_tab_order([entry1, entry2, button])
        navigator.bind_escape(dialog, lambda: dialog.destroy())
        navigator.bind_enter(form, form.submit)
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize keyboard navigator.
        
        Args:
            root: Root tkinter window
        """
        self.root = root
        self.shortcuts: Dict[str, Callable] = {}
        self.modal_stack: List[tk.Toplevel] = []
        self.focus_history: deque = deque(maxlen=10)
        
        # Bind global shortcuts
        self._bind_global_shortcuts()
    
    def _bind_global_shortcuts(self):
        """Bind global keyboard shortcuts."""
        # Help dialog
        self.root.bind_all('<F1>', lambda e: self._show_help())
        
        # Navigation
        self.root.bind_all('<Control-Tab>', lambda e: self._next_focusable())
        self.root.bind_all('<Control-Shift-Tab>', lambda e: self._previous_focusable())
    
    def set_tab_order(self, widgets: List[tk.Widget]):
        """
        Set tab order for a list of widgets.
        
        Args:
            widgets: List of widgets in desired tab order
        """
        for i, widget in enumerate(widgets):
            # Remove from default tab order
            widget.lift()
            
            # Bind Tab key
            widget.bind('<Tab>', lambda e, idx=i: self._handle_tab(widgets, idx, e))
            widget.bind('<Shift-Tab>', lambda e, idx=i: self._handle_shift_tab(widgets, idx, e))
    
    def _handle_tab(self, widgets: List[tk.Widget], current_idx: int, event: tk.Event):
        """Handle Tab key press."""
        next_idx = (current_idx + 1) % len(widgets)
        next_widget = widgets[next_idx]
        
        # Skip disabled widgets
        while not self._is_focusable(next_widget) and next_idx != current_idx:
            next_idx = (next_idx + 1) % len(widgets)
            next_widget = widgets[next_idx]
        
        next_widget.focus_set()
        return "break"  # Prevent default Tab behavior
    
    def _handle_shift_tab(self, widgets: List[tk.Widget], current_idx: int, event: tk.Event):
        """Handle Shift+Tab key press."""
        prev_idx = (current_idx - 1) % len(widgets)
        prev_widget = widgets[prev_idx]
        
        # Skip disabled widgets
        while not self._is_focusable(prev_widget) and prev_idx != current_idx:
            prev_idx = (prev_idx - 1) % len(widgets)
            prev_widget = widgets[prev_idx]
        
        prev_widget.focus_set()
        return "break"
    
    def _is_focusable(self, widget: tk.Widget) -> bool:
        """Check if widget can receive focus."""
        try:
            state = widget.cget('state')
            return state != 'disabled'
        except:
            return True
    
    def bind_enter(self, widget: tk.Widget, callback: Callable):
        """
        Bind Enter key to submit action.
        
        Args:
            widget: Widget or form to bind
            callback: Function to call on Enter press
        """
        widget.bind('<Return>', lambda e: callback())
        widget.bind('<KP_Enter>', lambda e: callback())  # Numpad Enter
    
    def bind_escape(self, widget: tk.Widget, callback: Callable):
        """
        Bind Escape key to cancel/close action.
        
        Args:
            widget: Widget or dialog to bind
            callback: Function to call on Escape press
        """
        widget.bind('<Escape>', lambda e: callback())
    
    def bind_arrows(self, widget: tk.Widget, 
                    up: Optional[Callable] = None,
                    down: Optional[Callable] = None,
                    left: Optional[Callable] = None,
                    right: Optional[Callable] = None):
        """
        Bind arrow keys to navigation callbacks.
        
        Args:
            widget: Widget to bind
            up: Callback for Up arrow
            down: Callback for Down arrow
            left: Callback for Left arrow
            right: Callback for Right arrow
        """
        if up:
            widget.bind('<Up>', lambda e: up())
        if down:
            widget.bind('<Down>', lambda e: down())
        if left:
            widget.bind('<Left>', lambda e: left())
        if right:
            widget.bind('<Right>', lambda e: right())
    
    def register_shortcut(self, key: str, callback: Callable, description: str = ""):
        """
        Register custom keyboard shortcut.
        
        Args:
            key: Key combination (e.g., '<Control-s>', '<Alt-n>')
            callback: Function to call
            description: Description for help dialog
        """
        self.shortcuts[key] = {
            'callback': callback,
            'description': description
        }
        self.root.bind_all(key, lambda e: callback())
    
    def push_modal(self, modal: tk.Toplevel):
        """
        Register modal dialog for Escape handling.
        
        Args:
            modal: Modal dialog window
        """
        self.modal_stack.append(modal)
        self.bind_escape(modal, lambda: self.pop_modal(modal))
    
    def pop_modal(self, modal: tk.Toplevel):
        """Remove modal from stack and destroy it."""
        if modal in self.modal_stack:
            self.modal_stack.remove(modal)
        modal.destroy()
    
    def focus_first(self, container: tk.Widget):
        """Focus first focusable widget in container."""
        for child in container.winfo_children():
            if self._is_focusable(child) and self._can_take_focus(child):
                child.focus_set()
                return
            # Check recursively
            self.focus_first(child)
    
    def _can_take_focus(self, widget: tk.Widget) -> bool:
        """Check if widget can take keyboard focus."""
        return isinstance(widget, (tk.Entry, tk.Text, tk.Button, ttk.Entry, ttk.Button, ttk.Combobox))
    
    def _next_focusable(self):
        """Focus next focusable widget globally."""
        current = self.root.focus_get()
        if current:
            current.tk_focusNext().focus_set()
    
    def _previous_focusable(self):
        """Focus previous focusable widget globally."""
        current = self.root.focus_get()
        if current:
            current.tk_focusPrev().focus_set()
    
    def _show_help(self):
        """Show keyboard shortcuts help dialog."""
        help_window = tk.Toplevel(self.root)
        help_window.title("Keyboard Shortcuts")
        help_window.geometry("500x400")
        
        # Title
        title = tk.Label(
            help_window,
            text="Keyboard Shortcuts",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title.pack()
        
        # Scrollable shortcuts list
        frame = tk.Frame(help_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(
            frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=("Arial", 11),
            padx=10,
            pady=10
        )
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        # Add default shortcuts
        shortcuts_text = """Global Shortcuts:

F1 - Show this help dialog
Ctrl+Tab - Next focusable element
Ctrl+Shift+Tab - Previous focusable element

Form Navigation:

Tab - Next field
Shift+Tab - Previous field
Enter - Submit form
Escape - Cancel/Close dialog

Custom Shortcuts:

"""
        
        # Add registered shortcuts
        for key, info in self.shortcuts.items():
            shortcuts_text += f"{key} - {info['description']}\n"
        
        text.insert('1.0', shortcuts_text)
        text.config(state='disabled')
        
        # Close button
        close_btn = tk.Button(
            help_window,
            text="Close",
            command=help_window.destroy,
            padx=20,
            pady=5
        )
        close_btn.pack(pady=10)
        
        self.bind_escape(help_window, help_window.destroy)
        self.push_modal(help_window)


class ScreenReaderAnnouncer:
    """
    Announces changes and notifications for screen readers.
    
    Uses live regions (simulated in Tkinter) to announce:
    - Form validation errors
    - Success messages
    - Page changes
    - Loading states
    - Data updates
    
    Usage:
        announcer = ScreenReaderAnnouncer(root)
        announcer.announce("Loading events...", priority="polite")
        announcer.announce_error("Invalid email address")
        announcer.announce_success("Event created successfully")
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize screen reader announcer.
        
        Args:
            root: Root tkinter window
        """
        self.root = root
        self.announcement_queue: deque = deque(maxlen=50)
        self.last_announcement = ""
        self.announcement_label = None
        
        # Create hidden label for announcements
        self._create_live_region()
    
    def _create_live_region(self):
        """Create invisible live region for screen reader announcements."""
        # Note: Tkinter doesn't have true ARIA live regions
        # This creates a label that updates, which some screen readers may detect
        self.announcement_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 1),  # Tiny font
            fg=self.root.cget('bg')  # Same as background (invisible)
        )
        self.announcement_label.place(x=0, y=0, width=1, height=1)
    
    def announce(self, message: str, priority: str = "polite"):
        """
        Announce message for screen readers.
        
        Args:
            message: Message to announce
            priority: 'polite' (wait for pause) or 'assertive' (interrupt)
        """
        if not message or message == self.last_announcement:
            return
        
        timestamp = time.strftime("%H:%M:%S")
        self.announcement_queue.append({
            'message': message,
            'priority': priority,
            'timestamp': timestamp
        })
        
        # Update live region
        if self.announcement_label:
            self.announcement_label.config(text=message)
        
        # Log for debugging
        print(f"[SCREEN READER] [{priority.upper()}] {message}")
        
        self.last_announcement = message
        
        # Clear after delay to allow re-announcement
        self.root.after(3000, lambda: setattr(self, 'last_announcement', ''))
    
    def announce_error(self, message: str):
        """Announce error message (assertive priority)."""
        self.announce(f"Error: {message}", priority="assertive")
    
    def announce_success(self, message: str):
        """Announce success message (polite priority)."""
        self.announce(f"Success: {message}", priority="polite")
    
    def announce_loading(self, message: str = "Loading..."):
        """Announce loading state."""
        self.announce(message, priority="polite")
    
    def announce_loaded(self, message: str = "Content loaded"):
        """Announce content loaded."""
        self.announce(message, priority="polite")
    
    def announce_page_change(self, page_name: str):
        """Announce page navigation."""
        self.announce(f"Navigated to {page_name} page", priority="polite")
    
    def announce_validation(self, field_name: str, error: str):
        """Announce form validation error."""
        self.announce(f"{field_name}: {error}", priority="assertive")
    
    def describe_element(self, element_type: str, label: str, state: str = "") -> str:
        """
        Generate description for interactive element.
        
        Args:
            element_type: Type of element (button, input, etc.)
            label: Element label/text
            state: Current state (disabled, selected, etc.)
        
        Returns:
            Full description string
        """
        description = f"{label} {element_type}"
        if state:
            description += f", {state}"
        return description
    
    def get_recent_announcements(self, count: int = 10) -> List[Dict]:
        """Get recent announcements for debugging."""
        return list(self.announcement_queue)[-count:]


class ColorContrastValidator:
    """
    Validates color contrast ratios for WCAG AA compliance.
    
    WCAG AA Requirements:
    - Normal text (< 18pt): 4.5:1 contrast ratio
    - Large text (≥ 18pt or 14pt bold): 3:1 contrast ratio
    - UI components: 3:1 contrast ratio
    
    Usage:
        validator = ColorContrastValidator()
        is_valid = validator.check_contrast("#000000", "#FFFFFF")  # True (21:1)
        ratio = validator.calculate_ratio("#3498db", "#FFFFFF")  # 3.26:1
    """
    
    def __init__(self):
        """Initialize color contrast validator."""
        self.wcag_aa_normal = 4.5  # Normal text
        self.wcag_aa_large = 3.0   # Large text
        self.wcag_aaa_normal = 7.0  # AAA normal text
        self.wcag_aaa_large = 4.5   # AAA large text
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to RGB.
        
        Args:
            hex_color: Hex color string (#RRGGBB)
        
        Returns:
            RGB tuple (r, g, b)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_luminance(self, rgb: Tuple[int, int, int]) -> float:
        """
        Calculate relative luminance of RGB color.
        
        Args:
            rgb: RGB tuple (r, g, b)
        
        Returns:
            Relative luminance (0.0 to 1.0)
        """
        # Convert to sRGB
        srgb = []
        for val in rgb:
            val = val / 255.0
            if val <= 0.03928:
                val = val / 12.92
            else:
                val = ((val + 0.055) / 1.055) ** 2.4
            srgb.append(val)
        
        # Calculate luminance
        luminance = 0.2126 * srgb[0] + 0.7152 * srgb[1] + 0.0722 * srgb[2]
        return luminance
    
    def calculate_ratio(self, color1: str, color2: str) -> float:
        """
        Calculate contrast ratio between two colors.
        
        Args:
            color1: First color (hex)
            color2: Second color (hex)
        
        Returns:
            Contrast ratio (1.0 to 21.0)
        """
        rgb1 = self.hex_to_rgb(color1)
        rgb2 = self.hex_to_rgb(color2)
        
        lum1 = self.rgb_to_luminance(rgb1)
        lum2 = self.rgb_to_luminance(rgb2)
        
        # Ensure lighter color is in numerator
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        ratio = (lighter + 0.05) / (darker + 0.05)
        return ratio
    
    def check_contrast(self, fg_color: str, bg_color: str, 
                      text_size: str = "normal") -> bool:
        """
        Check if color combination meets WCAG AA standards.
        
        Args:
            fg_color: Foreground/text color (hex)
            bg_color: Background color (hex)
            text_size: 'normal' or 'large'
        
        Returns:
            True if meets WCAG AA standards
        """
        ratio = self.calculate_ratio(fg_color, bg_color)
        
        if text_size == "large":
            return ratio >= self.wcag_aa_large
        else:
            return ratio >= self.wcag_aa_normal
    
    def get_compliant_text_color(self, bg_color: str) -> str:
        """
        Get compliant text color (black or white) for background.
        
        Args:
            bg_color: Background color (hex)
        
        Returns:
            '#000000' or '#FFFFFF' with best contrast
        """
        ratio_black = self.calculate_ratio('#000000', bg_color)
        ratio_white = self.calculate_ratio('#FFFFFF', bg_color)
        
        return '#000000' if ratio_black > ratio_white else '#FFFFFF'
    
    def validate_palette(self, colors: Dict[str, str]) -> Dict[str, Any]:
        """
        Validate entire color palette.
        
        Args:
            colors: Dictionary of color pairs {'name': {'fg': '#...', 'bg': '#...'}}
        
        Returns:
            Validation results dictionary
        """
        results = {}
        
        for name, pair in colors.items():
            fg = pair.get('fg', '#000000')
            bg = pair.get('bg', '#FFFFFF')
            
            ratio = self.calculate_ratio(fg, bg)
            passes_aa = self.check_contrast(fg, bg, 'normal')
            passes_aa_large = self.check_contrast(fg, bg, 'large')
            
            results[name] = {
                'ratio': ratio,
                'passes_aa': passes_aa,
                'passes_aa_large': passes_aa_large,
                'suggestion': self.get_compliant_text_color(bg) if not passes_aa else None
            }
        
        return results


class FontScaler:
    """
    Manages font size scaling for accessibility.
    
    Features:
    - Scale all fonts by percentage
    - Save user preferences
    - Responsive layout on font change
    - Support for system accessibility settings
    
    Usage:
        scaler = FontScaler(root)
        scaler.set_scale(1.2)  # 120% font size
        scaler.increase_font()
        scaler.decrease_font()
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize font scaler.
        
        Args:
            root: Root tkinter window
        """
        self.root = root
        self.scale_factor = 1.0
        self.min_scale = 0.8
        self.max_scale = 2.0
        self.scale_step = 0.1
        self.base_fonts: Dict[str, int] = {
            'title': 24,
            'heading': 18,
            'subheading': 14,
            'body': 12,
            'small': 10,
            'tiny': 8
        }
        self.widgets_to_update: List[tk.Widget] = []
    
    def register_widget(self, widget: tk.Widget):
        """Register widget for font scaling updates."""
        self.widgets_to_update.append(widget)
    
    def set_scale(self, scale: float):
        """
        Set font scale factor.
        
        Args:
            scale: Scale factor (0.8 to 2.0)
        """
        scale = max(self.min_scale, min(scale, self.max_scale))
        self.scale_factor = scale
        self._update_all_fonts()
    
    def increase_font(self):
        """Increase font size by one step."""
        new_scale = min(self.scale_factor + self.scale_step, self.max_scale)
        self.set_scale(new_scale)
    
    def decrease_font(self):
        """Decrease font size by one step."""
        new_scale = max(self.scale_factor - self.scale_step, self.min_scale)
        self.set_scale(new_scale)
    
    def reset_font(self):
        """Reset font size to 100%."""
        self.set_scale(1.0)
    
    def get_scaled_size(self, base_size: int) -> int:
        """
        Get scaled font size.
        
        Args:
            base_size: Base font size
        
        Returns:
            Scaled font size
        """
        return int(base_size * self.scale_factor)
    
    def get_font(self, style: str, weight: str = "normal") -> Tuple[str, int, str]:
        """
        Get scaled font tuple.
        
        Args:
            style: Font style (title, heading, body, etc.)
            weight: Font weight (normal, bold)
        
        Returns:
            Font tuple (family, size, weight)
        """
        base_size = self.base_fonts.get(style, 12)
        scaled_size = self.get_scaled_size(base_size)
        return ("Arial", scaled_size, weight)
    
    def _update_all_fonts(self):
        """Update fonts for all registered widgets."""
        for widget in self.widgets_to_update:
            try:
                current_font = widget.cget('font')
                if isinstance(current_font, tuple):
                    family, size, *rest = current_font
                    weight = rest[0] if rest else "normal"
                    new_size = self.get_scaled_size(size)
                    widget.config(font=(family, new_size, weight))
            except Exception as e:
                print(f"[FONT SCALER] Error updating widget font: {e}")


class FocusIndicator:
    """
    Manages visible focus indicators for keyboard navigation.
    
    Features:
    - Visible focus rings
    - Highlight active input
    - Custom focus colors
    - Focus state tracking
    
    Usage:
        indicator = FocusIndicator(root)
        indicator.add_focus_ring(entry, color="#3498db")
        indicator.highlight_active(text_widget)
    """
    
    def __init__(self, root: tk.Tk, focus_color: str = "#3498db", 
                 focus_width: int = 2):
        """
        Initialize focus indicator.
        
        Args:
            root: Root tkinter window
            focus_color: Color for focus rings
            focus_width: Width of focus ring
        """
        self.root = root
        self.focus_color = focus_color
        self.focus_width = focus_width
        self.focused_widgets: Dict[tk.Widget, Dict] = {}
    
    def add_focus_ring(self, widget: tk.Widget, color: Optional[str] = None):
        """
        Add focus ring to widget.
        
        Args:
            widget: Widget to add focus ring
            color: Custom focus color (optional)
        """
        color = color or self.focus_color
        
        # Store original style
        original_style = {}
        try:
            if isinstance(widget, (tk.Entry, tk.Text)):
                original_style['highlightbackground'] = widget.cget('highlightbackground')
                original_style['highlightcolor'] = widget.cget('highlightcolor')
                original_style['highlightthickness'] = widget.cget('highlightthickness')
            elif isinstance(widget, tk.Button):
                original_style['highlightbackground'] = widget.cget('highlightbackground')
                original_style['highlightthickness'] = widget.cget('highlightthickness')
        except:
            pass
        
        self.focused_widgets[widget] = {
            'original': original_style,
            'focus_color': color
        }
        
        # Bind focus events
        widget.bind('<FocusIn>', lambda e: self._on_focus_in(widget))
        widget.bind('<FocusOut>', lambda e: self._on_focus_out(widget))
    
    def _on_focus_in(self, widget: tk.Widget):
        """Handle widget gaining focus."""
        if widget not in self.focused_widgets:
            return
        
        color = self.focused_widgets[widget]['focus_color']
        
        try:
            if isinstance(widget, (tk.Entry, tk.Text)):
                widget.config(
                    highlightbackground=color,
                    highlightcolor=color,
                    highlightthickness=self.focus_width
                )
            elif isinstance(widget, tk.Button):
                widget.config(
                    highlightbackground=color,
                    highlightthickness=self.focus_width
                )
        except Exception as e:
            print(f"[FOCUS] Error setting focus style: {e}")
    
    def _on_focus_out(self, widget: tk.Widget):
        """Handle widget losing focus."""
        if widget not in self.focused_widgets:
            return
        
        original = self.focused_widgets[widget]['original']
        
        try:
            widget.config(**original)
        except Exception as e:
            print(f"[FOCUS] Error restoring style: {e}")
    
    def highlight_active(self, widget: tk.Widget, bg_color: str = "#e8f4f8"):
        """
        Highlight active input with background color.
        
        Args:
            widget: Widget to highlight
            bg_color: Background color for active state
        """
        try:
            original_bg = widget.cget('bg')
            
            widget.bind('<FocusIn>', lambda e: widget.config(bg=bg_color))
            widget.bind('<FocusOut>', lambda e: widget.config(bg=original_bg))
        except:
            pass


class HighContrastMode:
    """
    Manages high contrast color scheme for better visibility.
    
    Features:
    - Toggle high contrast mode
    - WCAG AAA compliant colors
    - Save user preference
    - Apply to all widgets
    
    Usage:
        hc_mode = HighContrastMode(root)
        hc_mode.toggle()
        hc_mode.enable()
        hc_mode.disable()
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize high contrast mode.
        
        Args:
            root: Root tkinter window
        """
        self.root = root
        self.enabled = False
        
        # Normal color scheme
        self.normal_colors = {
            'bg': '#FFFFFF',
            'fg': '#2c3e50',
            'button_bg': '#3498db',
            'button_fg': '#FFFFFF',
            'entry_bg': '#FFFFFF',
            'entry_fg': '#2c3e50',
            'accent': '#3498db',
            'error': '#e74c3c',
            'success': '#2ecc71'
        }
        
        # High contrast color scheme (WCAG AAA)
        self.high_contrast_colors = {
            'bg': '#000000',
            'fg': '#FFFFFF',
            'button_bg': '#FFFF00',  # Yellow
            'button_fg': '#000000',
            'entry_bg': '#FFFFFF',
            'entry_fg': '#000000',
            'accent': '#00FFFF',  # Cyan
            'error': '#FF0000',
            'success': '#00FF00'
        }
        
        self.widgets_to_update: List[tk.Widget] = []
    
    def register_widget(self, widget: tk.Widget, widget_type: str = "default"):
        """
        Register widget for color updates.
        
        Args:
            widget: Widget to register
            widget_type: Type (default, button, entry, etc.)
        """
        self.widgets_to_update.append({
            'widget': widget,
            'type': widget_type
        })
    
    def toggle(self):
        """Toggle high contrast mode on/off."""
        if self.enabled:
            self.disable()
        else:
            self.enable()
    
    def enable(self):
        """Enable high contrast mode."""
        self.enabled = True
        self._apply_colors(self.high_contrast_colors)
        print("[HIGH CONTRAST] Enabled")
    
    def disable(self):
        """Disable high contrast mode."""
        self.enabled = False
        self._apply_colors(self.normal_colors)
        print("[HIGH CONTRAST] Disabled")
    
    def _apply_colors(self, colors: Dict[str, str]):
        """Apply color scheme to all registered widgets."""
        # Update root window
        try:
            self.root.config(bg=colors['bg'])
        except:
            pass
        
        # Update registered widgets
        for item in self.widgets_to_update:
            widget = item['widget']
            widget_type = item['type']
            
            try:
                if widget_type == "button":
                    widget.config(
                        bg=colors['button_bg'],
                        fg=colors['button_fg']
                    )
                elif widget_type == "entry":
                    widget.config(
                        bg=colors['entry_bg'],
                        fg=colors['entry_fg']
                    )
                else:
                    widget.config(
                        bg=colors['bg'],
                        fg=colors['fg']
                    )
            except Exception as e:
                print(f"[HIGH CONTRAST] Error updating widget: {e}")


class AccessibleForm(tk.Frame):
    """
    Accessible form with keyboard navigation and screen reader support.
    
    Features:
    - Automatic tab order
    - Enter to submit
    - Escape to cancel
    - Focus indicators
    - Screen reader announcements
    - Validation error announcements
    
    Usage:
        form = AccessibleForm(parent, title="Create Event")
        form.add_field("Event Name", "name", required=True)
        form.add_field("Description", "description", widget_type="text")
        form.on_submit(lambda data: print(data))
    """
    
    def __init__(self, parent: tk.Widget, title: str = "",
                 navigator: Optional[KeyboardNavigator] = None,
                 announcer: Optional[ScreenReaderAnnouncer] = None,
                 focus_indicator: Optional[FocusIndicator] = None):
        """
        Initialize accessible form.
        
        Args:
            parent: Parent widget
            title: Form title
            navigator: Keyboard navigator instance
            announcer: Screen reader announcer instance
            focus_indicator: Focus indicator instance
        """
        super().__init__(parent, bg="white")
        
        self.title = title
        self.navigator = navigator or KeyboardNavigator(parent.winfo_toplevel())
        self.announcer = announcer or ScreenReaderAnnouncer(parent.winfo_toplevel())
        self.focus_indicator = focus_indicator or FocusIndicator(parent.winfo_toplevel())
        
        self.fields: Dict[str, Dict] = {}
        self.widgets: List[tk.Widget] = []
        self.submit_callback: Optional[Callable] = None
        self.cancel_callback: Optional[Callable] = None
        
        self._create_form()
    
    def _create_form(self):
        """Create form layout."""
        # Title
        if self.title:
            title_label = tk.Label(
                self,
                text=self.title,
                font=("Arial", 18, "bold"),
                bg="white",
                fg="#2c3e50"
            )
            title_label.pack(pady=20)
            
            # Announce form title
            self.announcer.announce(f"{self.title} form")
        
        # Fields container
        self.fields_frame = tk.Frame(self, bg="white")
        self.fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Buttons container
        self.buttons_frame = tk.Frame(self, bg="white")
        self.buttons_frame.pack(pady=20)
    
    def add_field(self, label: str, name: str, widget_type: str = "entry",
                 required: bool = False, placeholder: str = "",
                 options: Optional[List[str]] = None):
        """
        Add form field.
        
        Args:
            label: Field label
            name: Field name (key in data dict)
            widget_type: Type (entry, text, combobox)
            required: Whether field is required
            placeholder: Placeholder text
            options: Options for combobox
        """
        # Field container
        field_frame = tk.Frame(self.fields_frame, bg="white")
        field_frame.pack(fill=tk.X, pady=10)
        
        # Label with required indicator
        label_text = f"{label}{'*' if required else ''}"
        label_widget = tk.Label(
            field_frame,
            text=label_text,
            font=("Arial", 12, "bold" if required else "normal"),
            bg="white",
            fg="#2c3e50",
            anchor='w'
        )
        label_widget.pack(anchor='w', pady=(0, 5))
        
        # Create input widget
        widget = None
        if widget_type == "text":
            widget = tk.Text(
                field_frame,
                height=5,
                font=("Arial", 12),
                relief=tk.SOLID,
                borderwidth=1
            )
        elif widget_type == "combobox" and options:
            widget = ttk.Combobox(
                field_frame,
                values=options,
                font=("Arial", 12),
                state='readonly'
            )
        else:  # entry
            widget = tk.Entry(
                field_frame,
                font=("Arial", 12),
                relief=tk.SOLID,
                borderwidth=1
            )
            if placeholder:
                widget.insert(0, placeholder)
                widget.config(fg='gray')
                widget.bind('<FocusIn>', lambda e: self._clear_placeholder(widget, placeholder))
                widget.bind('<FocusOut>', lambda e: self._restore_placeholder(widget, placeholder))
        
        widget.pack(fill=tk.X)
        
        # Add focus indicator
        self.focus_indicator.add_focus_ring(widget)
        
        # Store field info
        self.fields[name] = {
            'label': label,
            'widget': widget,
            'type': widget_type,
            'required': required,
            'placeholder': placeholder,
            'error_label': None
        }
        
        self.widgets.append(widget)
        
        # Error label (hidden by default)
        error_label = tk.Label(
            field_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#e74c3c",
            anchor='w'
        )
        error_label.pack(anchor='w', pady=(5, 0))
        error_label.pack_forget()  # Hide initially
        self.fields[name]['error_label'] = error_label
    
    def _clear_placeholder(self, widget: tk.Entry, placeholder: str):
        """Clear placeholder text on focus."""
        if widget.get() == placeholder:
            widget.delete(0, tk.END)
            widget.config(fg='black')
    
    def _restore_placeholder(self, widget: tk.Entry, placeholder: str):
        """Restore placeholder text on blur if empty."""
        if not widget.get():
            widget.insert(0, placeholder)
            widget.config(fg='gray')
    
    def add_buttons(self, submit_text: str = "Submit", 
                   cancel_text: str = "Cancel",
                   show_cancel: bool = True):
        """
        Add submit and cancel buttons.
        
        Args:
            submit_text: Submit button text
            cancel_text: Cancel button text
            show_cancel: Whether to show cancel button
        """
        # Submit button
        submit_btn = tk.Button(
            self.buttons_frame,
            text=submit_text,
            command=self._handle_submit,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            cursor="hand2"
        )
        submit_btn.pack(side=tk.LEFT, padx=10)
        self.widgets.append(submit_btn)
        self.focus_indicator.add_focus_ring(submit_btn)
        
        # Cancel button
        if show_cancel:
            cancel_btn = tk.Button(
                self.buttons_frame,
                text=cancel_text,
                command=self._handle_cancel,
                bg="#95a5a6",
                fg="white",
                font=("Arial", 12),
                padx=30,
                pady=10,
                cursor="hand2"
            )
            cancel_btn.pack(side=tk.LEFT, padx=10)
            self.widgets.append(cancel_btn)
            self.focus_indicator.add_focus_ring(cancel_btn)
        
        # Set up keyboard navigation
        self.navigator.set_tab_order(self.widgets)
        self.navigator.bind_enter(self, self._handle_submit)
        self.navigator.bind_escape(self, self._handle_cancel)
        
        # Focus first field
        self.navigator.focus_first(self)
    
    def on_submit(self, callback: Callable):
        """Register submit callback."""
        self.submit_callback = callback
    
    def on_cancel(self, callback: Callable):
        """Register cancel callback."""
        self.cancel_callback = callback
    
    def _handle_submit(self):
        """Handle form submission."""
        # Validate
        is_valid, errors = self._validate()
        
        if not is_valid:
            # Announce first error
            first_error = list(errors.values())[0]
            self.announcer.announce_error(first_error)
            return
        
        # Get form data
        data = self.get_data()
        
        # Call submit callback
        if self.submit_callback:
            self.submit_callback(data)
    
    def _handle_cancel(self):
        """Handle form cancellation."""
        self.announcer.announce("Form cancelled")
        
        if self.cancel_callback:
            self.cancel_callback()
    
    def _validate(self) -> Tuple[bool, Dict[str, str]]:
        """
        Validate form fields.
        
        Returns:
            (is_valid, errors_dict)
        """
        errors = {}
        
        for name, field in self.fields.items():
            # Clear previous error
            if field['error_label']:
                field['error_label'].pack_forget()
            
            if not field['required']:
                continue
            
            # Get value
            widget = field['widget']
            value = self._get_widget_value(widget, field['type'], field['placeholder'])
            
            # Check if empty
            if not value or value.strip() == "":
                error_msg = f"{field['label']} is required"
                errors[name] = error_msg
                
                # Show error label
                if field['error_label']:
                    field['error_label'].config(text=error_msg)
                    field['error_label'].pack(anchor='w', pady=(5, 0))
                
                # Announce error
                self.announcer.announce_validation(field['label'], "is required")
        
        return len(errors) == 0, errors
    
    def get_data(self) -> Dict[str, Any]:
        """
        Get form data.
        
        Returns:
            Dictionary of field values
        """
        data = {}
        
        for name, field in self.fields.items():
            widget = field['widget']
            value = self._get_widget_value(widget, field['type'], field['placeholder'])
            data[name] = value
        
        return data
    
    def _get_widget_value(self, widget: tk.Widget, widget_type: str, 
                         placeholder: str) -> str:
        """Get value from widget."""
        if widget_type == "text":
            return widget.get('1.0', tk.END).strip()
        elif widget_type == "combobox":
            return widget.get()
        else:  # entry
            value = widget.get()
            return "" if value == placeholder else value
    
    def clear(self):
        """Clear all form fields."""
        for field in self.fields.values():
            widget = field['widget']
            widget_type = field['type']
            
            if widget_type == "text":
                widget.delete('1.0', tk.END)
            elif widget_type == "combobox":
                widget.set('')
            else:  # entry
                widget.delete(0, tk.END)
                if field['placeholder']:
                    widget.insert(0, field['placeholder'])
                    widget.config(fg='gray')
            
            # Clear error
            if field['error_label']:
                field['error_label'].pack_forget()
        
        self.announcer.announce("Form cleared")


# Global instances
_keyboard_navigator = None
_screen_reader_announcer = None
_color_validator = None
_font_scaler = None
_focus_indicator = None
_high_contrast_mode = None


def get_keyboard_navigator(root: tk.Tk) -> KeyboardNavigator:
    """Get global keyboard navigator instance."""
    global _keyboard_navigator
    if _keyboard_navigator is None:
        _keyboard_navigator = KeyboardNavigator(root)
    return _keyboard_navigator


def get_screen_reader_announcer(root: tk.Tk) -> ScreenReaderAnnouncer:
    """Get global screen reader announcer instance."""
    global _screen_reader_announcer
    if _screen_reader_announcer is None:
        _screen_reader_announcer = ScreenReaderAnnouncer(root)
    return _screen_reader_announcer


def get_color_validator() -> ColorContrastValidator:
    """Get color contrast validator instance."""
    global _color_validator
    if _color_validator is None:
        _color_validator = ColorContrastValidator()
    return _color_validator


def get_font_scaler(root: tk.Tk) -> FontScaler:
    """Get global font scaler instance."""
    global _font_scaler
    if _font_scaler is None:
        _font_scaler = FontScaler(root)
    return _font_scaler


def get_focus_indicator(root: tk.Tk) -> FocusIndicator:
    """Get global focus indicator instance."""
    global _focus_indicator
    if _focus_indicator is None:
        _focus_indicator = FocusIndicator(root)
    return _focus_indicator


def get_high_contrast_mode(root: tk.Tk) -> HighContrastMode:
    """Get global high contrast mode instance."""
    global _high_contrast_mode
    if _high_contrast_mode is None:
        _high_contrast_mode = HighContrastMode(root)
    return _high_contrast_mode
