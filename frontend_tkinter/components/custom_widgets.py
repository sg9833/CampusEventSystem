"""
Custom Styled Widgets for Campus Event System

This module provides reusable, styled UI components including buttons, entries,
cards, progress bars, and toast notifications with consistent theming.

Author: Campus Event System Team
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Literal
import math


# ============================================================================
# COLOR PALETTE & THEME CONSTANTS
# ============================================================================

class Theme:
    """Centralized theme colors for consistent styling"""
    
    # Primary Colors
    PRIMARY = "#3498DB"
    PRIMARY_HOVER = "#2980B9"
    PRIMARY_ACTIVE = "#1F618D"
    
    # Secondary Colors
    SECONDARY = "#95A5A6"
    SECONDARY_HOVER = "#7F8C8D"
    SECONDARY_ACTIVE = "#5D6D7E"
    
    # Success Colors
    SUCCESS = "#27AE60"
    SUCCESS_HOVER = "#229954"
    SUCCESS_ACTIVE = "#1E8449"
    
    # Danger Colors
    DANGER = "#E74C3C"
    DANGER_HOVER = "#C0392B"
    DANGER_ACTIVE = "#A93226"
    
    # Warning Colors
    WARNING = "#F39C12"
    WARNING_HOVER = "#E67E22"
    WARNING_ACTIVE = "#CA6F1E"
    
    # Info Colors
    INFO = "#3498DB"
    INFO_HOVER = "#2980B9"
    
    # Ghost/Outline
    GHOST = "#FFFFFF"
    GHOST_BORDER = "#BDC3C7"
    GHOST_HOVER = "#ECF0F1"
    
    # Text Colors
    TEXT_DARK = "#2C3E50"
    TEXT_LIGHT = "#FFFFFF"
    TEXT_MUTED = "#7F8C8D"
    TEXT_PLACEHOLDER = "#95A5A6"
    
    # Background Colors
    BG_WHITE = "#FFFFFF"
    BG_LIGHT = "#F8F9FA"
    BG_DARK = "#2C3E50"
    BG_CARD = "#FFFFFF"
    
    # Border Colors
    BORDER_LIGHT = "#E0E0E0"
    BORDER_ERROR = "#E74C3C"
    BORDER_SUCCESS = "#27AE60"
    BORDER_FOCUS = "#3498DB"
    
    # Shadow
    SHADOW = "#00000020"
    SHADOW_HOVER = "#00000030"


# ============================================================================
# 1. STYLED BUTTON CLASS
# ============================================================================

class StyledButton(tk.Canvas):
    """
    A styled button widget with multiple variants and states.
    
    Variants:
        - primary: Blue button for main actions
        - secondary: Gray button for secondary actions
        - success: Green button for positive actions
        - danger: Red button for destructive actions
        - ghost: Transparent button with border
    
    States:
        - normal: Default interactive state
        - hover: Mouse over state
        - disabled: Non-interactive state
        - loading: Shows spinner animation
    
    Example:
        button = StyledButton(
            parent,
            text="Save Changes",
            variant="primary",
            command=save_handler
        )
        button.pack(pady=10)
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        text: str = "Button",
        variant: Literal["primary", "secondary", "success", "danger", "ghost"] = "primary",
        command: Optional[Callable] = None,
        width: int = 120,
        height: int = 36,
        **kwargs
    ):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.text = text
        self.variant = variant
        self.command = command
        self.btn_width = width
        self.btn_height = height
        
        self._is_disabled = False
        self._is_loading = False
        self._spinner_angle = 0
        self._spinner_job = None
        
        # Get colors based on variant
        self._colors = self._get_variant_colors()
        
        # Draw button
        self._draw_button()
        
        # Bind events
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _get_variant_colors(self) -> dict:
        """Get color scheme for the variant"""
        colors = {
            "primary": {
                "bg": Theme.PRIMARY,
                "hover": Theme.PRIMARY_HOVER,
                "active": Theme.PRIMARY_ACTIVE,
                "text": Theme.TEXT_LIGHT,
                "border": Theme.PRIMARY
            },
            "secondary": {
                "bg": Theme.SECONDARY,
                "hover": Theme.SECONDARY_HOVER,
                "active": Theme.SECONDARY_ACTIVE,
                "text": Theme.TEXT_LIGHT,
                "border": Theme.SECONDARY
            },
            "success": {
                "bg": Theme.SUCCESS,
                "hover": Theme.SUCCESS_HOVER,
                "active": Theme.SUCCESS_ACTIVE,
                "text": Theme.TEXT_LIGHT,
                "border": Theme.SUCCESS
            },
            "danger": {
                "bg": Theme.DANGER,
                "hover": Theme.DANGER_HOVER,
                "active": Theme.DANGER_ACTIVE,
                "text": Theme.TEXT_LIGHT,
                "border": Theme.DANGER
            },
            "ghost": {
                "bg": Theme.GHOST,
                "hover": Theme.GHOST_HOVER,
                "active": Theme.GHOST_HOVER,
                "text": Theme.TEXT_DARK,
                "border": Theme.GHOST_BORDER
            }
        }
        return colors.get(self.variant, colors["primary"])
    
    def _draw_button(self, state: str = "normal"):
        """Draw button with current state"""
        self.delete("all")
        
        # Determine background color
        if self._is_disabled:
            bg_color = Theme.SECONDARY
            text_color = Theme.TEXT_MUTED
        elif state == "hover" and not self._is_loading:
            bg_color = self._colors["hover"]
            text_color = self._colors["text"]
        else:
            bg_color = self._colors["bg"]
            text_color = self._colors["text"]
        
        # Draw rounded rectangle background
        radius = 6
        self.create_rounded_rect(
            2, 2, self.btn_width - 2, self.btn_height - 2,
            radius=radius,
            fill=bg_color,
            outline=self._colors["border"],
            width=2 if self.variant == "ghost" else 0
        )
        
        # Draw loading spinner or text
        if self._is_loading:
            self._draw_spinner()
        else:
            self.create_text(
                self.btn_width // 2,
                self.btn_height // 2,
                text=self.text,
                fill=text_color,
                font=("Segoe UI", 10, "bold"),
                tags="text"
            )
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Helper to create rounded rectangle"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _draw_spinner(self):
        """Draw loading spinner animation"""
        center_x = self.btn_width // 2
        center_y = self.btn_height // 2
        radius = 8
        
        # Draw spinner arc
        for i in range(8):
            angle = self._spinner_angle + (i * 45)
            rad = math.radians(angle)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            
            opacity = int(255 * (i / 8))
            color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
            
            self.create_oval(
                x - 2, y - 2, x + 2, y + 2,
                fill=color,
                outline=""
            )
    
    def _animate_spinner(self):
        """Animate the spinner"""
        if self._is_loading:
            self._spinner_angle = (self._spinner_angle + 15) % 360
            self._draw_button()
            self._spinner_job = self.after(50, self._animate_spinner)
    
    def _on_click(self, event):
        """Handle click event"""
        if not self._is_disabled and not self._is_loading and self.command:
            self.command()
    
    def _on_enter(self, event):
        """Handle mouse enter"""
        if not self._is_disabled and not self._is_loading:
            self._draw_button("hover")
            self.config(cursor="hand2")
    
    def _on_leave(self, event):
        """Handle mouse leave"""
        if not self._is_disabled:
            self._draw_button("normal")
            self.config(cursor="")
    
    # Public API
    
    def set_loading(self, loading: bool):
        """Enable/disable loading state"""
        self._is_loading = loading
        
        if loading:
            self._animate_spinner()
        else:
            if self._spinner_job:
                self.after_cancel(self._spinner_job)
                self._spinner_job = None
            self._draw_button()
    
    def set_disabled(self, disabled: bool):
        """Enable/disable button"""
        self._is_disabled = disabled
        self._draw_button()
        self.config(cursor="" if disabled else "hand2")
    
    def set_text(self, text: str):
        """Update button text"""
        self.text = text
        self._draw_button()


# ============================================================================
# 2. STYLED ENTRY CLASS
# ============================================================================

class StyledEntry(tk.Frame):
    """
    A styled entry widget with icons, states, and validation.
    
    Features:
        - Left/right icon support
        - Placeholder text
        - Error/success states with colored borders
        - Clear button (optional)
        - Password visibility toggle
    
    Example:
        entry = StyledEntry(
            parent,
            placeholder="Enter email",
            icon_left="📧",
            clear_button=True
        )
        entry.pack(pady=5)
        
        # Get value
        value = entry.get()
        
        # Set error state
        entry.set_error("Invalid email format")
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        placeholder: str = "",
        icon_left: Optional[str] = None,
        icon_right: Optional[str] = None,
        clear_button: bool = False,
        show: Optional[str] = None,
        width: int = 30,
        **kwargs
    ):
        super().__init__(parent, bg=Theme.BG_WHITE)
        
        self.placeholder = placeholder
        self.icon_left = icon_left
        self.icon_right = icon_right
        self.show_char = show
        self._has_placeholder = True
        self._error_msg = None
        self._state = "normal"  # normal, error, success
        
        # Container frame with border
        self.border_frame = tk.Frame(
            self,
            bg=Theme.BORDER_LIGHT,
            highlightthickness=0
        )
        self.border_frame.pack(fill=tk.BOTH, expand=True)
        
        # Inner frame
        self.inner_frame = tk.Frame(
            self.border_frame,
            bg=Theme.BG_WHITE
        )
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Content frame
        self.content_frame = tk.Frame(
            self.inner_frame,
            bg=Theme.BG_WHITE
        )
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        
        # Left icon
        if icon_left:
            self.left_icon_label = tk.Label(
                self.content_frame,
                text=icon_left,
                bg=Theme.BG_WHITE,
                fg=Theme.TEXT_MUTED,
                font=("Segoe UI", 12)
            )
            self.left_icon_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Entry widget
        self.entry = tk.Entry(
            self.content_frame,
            font=("Segoe UI", 10),
            bg=Theme.BG_WHITE,
            fg=Theme.TEXT_DARK,
            bd=0,
            highlightthickness=0,
            width=width,
            show=show if show else "",
            **kwargs
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Placeholder
        if placeholder:
            self._show_placeholder()
        
        # Clear button
        if clear_button:
            self.clear_btn = tk.Label(
                self.content_frame,
                text="✕",
                bg=Theme.BG_WHITE,
                fg=Theme.TEXT_MUTED,
                font=("Segoe UI", 10, "bold"),
                cursor="hand2"
            )
            self.clear_btn.pack(side=tk.RIGHT, padx=(5, 0))
            self.clear_btn.bind("<Button-1>", lambda e: self.clear())
            self.clear_btn.pack_forget()  # Hidden initially
        
        # Right icon
        if icon_right:
            self.right_icon_label = tk.Label(
                self.content_frame,
                text=icon_right,
                bg=Theme.BG_WHITE,
                fg=Theme.TEXT_MUTED,
                font=("Segoe UI", 12),
                cursor="hand2" if show else ""
            )
            self.right_icon_label.pack(side=tk.RIGHT, padx=(5, 0))
            
            # If password field, toggle visibility
            if show:
                self.right_icon_label.bind("<Button-1>", self._toggle_password)
        
        # Error label (hidden initially)
        self.error_label = tk.Label(
            self,
            text="",
            bg=Theme.BG_WHITE,
            fg=Theme.DANGER,
            font=("Segoe UI", 8),
            anchor="w"
        )
        
        # Bind events
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<KeyRelease>", self._on_key_release)
    
    def _show_placeholder(self):
        """Show placeholder text"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=Theme.TEXT_PLACEHOLDER)
        self._has_placeholder = True
    
    def _hide_placeholder(self):
        """Hide placeholder text"""
        if self._has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=Theme.TEXT_DARK)
            self._has_placeholder = False
    
    def _on_focus_in(self, event):
        """Handle focus in"""
        self._hide_placeholder()
        
        # Change border color
        if self._state == "normal":
            self.border_frame.config(bg=Theme.BORDER_FOCUS)
    
    def _on_focus_out(self, event):
        """Handle focus out"""
        if not self.get():
            self._show_placeholder()
        
        # Reset border color
        if self._state == "normal":
            self.border_frame.config(bg=Theme.BORDER_LIGHT)
    
    def _on_key_release(self, event):
        """Handle key release"""
        # Show/hide clear button
        if hasattr(self, 'clear_btn'):
            if self.get():
                self.clear_btn.pack(side=tk.RIGHT, padx=(5, 0))
            else:
                self.clear_btn.pack_forget()
    
    def _toggle_password(self, event):
        """Toggle password visibility"""
        if self.entry.cget("show") == "":
            self.entry.config(show="•")
            self.right_icon_label.config(text="👁️")
        else:
            self.entry.config(show="")
            self.right_icon_label.config(text="👁️‍🗨️")
    
    # Public API
    
    def get(self) -> str:
        """Get entry value (empty if placeholder)"""
        if self._has_placeholder:
            return ""
        return self.entry.get()
    
    def set(self, value: str):
        """Set entry value"""
        self._hide_placeholder()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def clear(self):
        """Clear entry"""
        self.entry.delete(0, tk.END)
        self._show_placeholder()
        self.clear_state()
        
        if hasattr(self, 'clear_btn'):
            self.clear_btn.pack_forget()
    
    def set_error(self, message: str):
        """Set error state"""
        self._state = "error"
        self._error_msg = message
        self.border_frame.config(bg=Theme.BORDER_ERROR)
        
        self.error_label.config(text=f"⚠ {message}")
        self.error_label.pack(fill=tk.X, padx=2, pady=(2, 0))
    
    def set_success(self):
        """Set success state"""
        self._state = "success"
        self.border_frame.config(bg=Theme.BORDER_SUCCESS)
        self.clear_error()
    
    def clear_state(self):
        """Clear error/success state"""
        self._state = "normal"
        self.border_frame.config(bg=Theme.BORDER_LIGHT)
        self.clear_error()
    
    def clear_error(self):
        """Clear error message"""
        self._error_msg = None
        self.error_label.pack_forget()
    
    def focus(self):
        """Set focus to entry"""
        self.entry.focus()


# ============================================================================
# 3. STYLED CARD CLASS
# ============================================================================

class StyledCard(tk.Frame):
    """
    A card widget with shadow, rounded corners, and hover effects.
    
    Features:
        - Elevated shadow effect
        - Rounded corners (simulated)
        - Hover state with darker shadow
        - Customizable padding
        - Optional click handler
    
    Example:
        card = StyledCard(parent, padding=20, hover=True)
        card.pack(pady=10, padx=20, fill=tk.X)
        
        # Add content to card
        tk.Label(card, text="Card Title", font=("Segoe UI", 14, "bold")).pack()
        tk.Label(card, text="Card content goes here").pack()
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        padding: int = 15,
        hover: bool = True,
        click_handler: Optional[Callable] = None,
        **kwargs
    ):
        # Shadow frame (outer)
        self.shadow_frame = tk.Frame(
            parent,
            bg=Theme.SHADOW,
            **kwargs
        )
        
        # Main frame (inner)
        super().__init__(
            self.shadow_frame,
            bg=Theme.BG_CARD,
            **kwargs
        )
        super().pack(padx=2, pady=2)
        
        self.padding = padding
        self.hover_enabled = hover
        self.click_handler = click_handler
        self._is_hovered = False
        
        # Content frame with padding
        self.content_frame = tk.Frame(
            self,
            bg=Theme.BG_CARD
        )
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=padding, pady=padding)
        
        # Bind hover events
        if hover or click_handler:
            self._bind_hover_events(self)
            self._bind_hover_events(self.content_frame)
        
        if click_handler:
            self._bind_click_events(self)
            self._bind_click_events(self.content_frame)
    
    def _bind_hover_events(self, widget):
        """Bind hover events to widget and children"""
        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        
        for child in widget.winfo_children():
            self._bind_hover_events(child)
    
    def _bind_click_events(self, widget):
        """Bind click events to widget and children"""
        widget.bind("<Button-1>", self._on_click)
        
        for child in widget.winfo_children():
            self._bind_click_events(child)
    
    def _on_enter(self, event):
        """Handle mouse enter"""
        if not self._is_hovered:
            self._is_hovered = True
            self.shadow_frame.config(bg=Theme.SHADOW_HOVER)
            super().pack(padx=3, pady=3)  # Increase shadow
            
            if self.click_handler:
                self.config(cursor="hand2")
    
    def _on_leave(self, event):
        """Handle mouse leave"""
        # Check if mouse truly left the card
        x, y = event.x_root, event.y_root
        widget_x = self.shadow_frame.winfo_rootx()
        widget_y = self.shadow_frame.winfo_rooty()
        widget_width = self.shadow_frame.winfo_width()
        widget_height = self.shadow_frame.winfo_height()
        
        if not (widget_x <= x <= widget_x + widget_width and
                widget_y <= y <= widget_y + widget_height):
            self._is_hovered = False
            self.shadow_frame.config(bg=Theme.SHADOW)
            super().pack(padx=2, pady=2)  # Reset shadow
            self.config(cursor="")
    
    def _on_click(self, event):
        """Handle click"""
        if self.click_handler:
            self.click_handler()
    
    def pack(self, **kwargs):
        """Override pack to pack shadow frame"""
        self.shadow_frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Override grid to grid shadow frame"""
        self.shadow_frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Override place to place shadow frame"""
        self.shadow_frame.place(**kwargs)


# ============================================================================
# 4. PROGRESS BAR CLASS
# ============================================================================

class ProgressBar(tk.Canvas):
    """
    An animated progress bar with percentage label.
    
    Features:
        - Colored progress bar
        - Percentage label
        - Smooth animation
        - Customizable colors
    
    Example:
        progress = ProgressBar(parent, width=300, height=24)
        progress.pack(pady=10)
        
        # Set progress (animates)
        progress.set_progress(75)
        
        # Change color
        progress.set_color("#27AE60")
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        width: int = 300,
        height: int = 24,
        bg_color: str = Theme.BG_LIGHT,
        fg_color: str = Theme.PRIMARY,
        **kwargs
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=Theme.BG_WHITE,
            highlightthickness=0,
            **kwargs
        )
        
        self.bar_width = width
        self.bar_height = height
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        self._current_progress = 0
        self._target_progress = 0
        self._animation_job = None
        
        self._draw_progress()
    
    def _draw_progress(self):
        """Draw progress bar"""
        self.delete("all")
        
        # Background bar
        self.create_rounded_rect(
            0, 0, self.bar_width, self.bar_height,
            radius=self.bar_height // 2,
            fill=self.bg_color,
            outline=""
        )
        
        # Progress bar
        if self._current_progress > 0:
            progress_width = (self.bar_width * self._current_progress) / 100
            self.create_rounded_rect(
                0, 0, progress_width, self.bar_height,
                radius=self.bar_height // 2,
                fill=self.fg_color,
                outline=""
            )
        
        # Percentage text
        self.create_text(
            self.bar_width // 2,
            self.bar_height // 2,
            text=f"{int(self._current_progress)}%",
            fill=Theme.TEXT_DARK,
            font=("Segoe UI", 9, "bold")
        )
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Helper to create rounded rectangle"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _animate_to_target(self):
        """Animate progress to target"""
        if abs(self._current_progress - self._target_progress) < 1:
            self._current_progress = self._target_progress
            self._draw_progress()
            return
        
        # Move towards target
        diff = self._target_progress - self._current_progress
        step = diff / 10
        self._current_progress += step
        
        self._draw_progress()
        self._animation_job = self.after(30, self._animate_to_target)
    
    # Public API
    
    def set_progress(self, value: float):
        """Set progress value (0-100) with animation"""
        self._target_progress = max(0, min(100, value))
        
        if self._animation_job:
            self.after_cancel(self._animation_job)
        
        self._animate_to_target()
    
    def set_color(self, color: str):
        """Change progress bar color"""
        self.fg_color = color
        self._draw_progress()
    
    def reset(self):
        """Reset progress to 0"""
        self._current_progress = 0
        self._target_progress = 0
        self._draw_progress()


# ============================================================================
# 5. TOAST NOTIFICATION CLASS
# ============================================================================

class Toast:
    """
    Toast notification system with auto-dismiss and animations.
    
    Types:
        - success: Green toast for successful operations
        - error: Red toast for errors
        - info: Blue toast for information
        - warning: Orange toast for warnings
    
    Features:
        - Auto-dismiss after 3 seconds (configurable)
        - Slide-in animation from top
        - Multiple toasts stack vertically
        - Click to dismiss
    
    Example:
        # Show success toast
        Toast.show(parent, "Changes saved successfully!", type="success")
        
        # Show error with longer duration
        Toast.show(parent, "Failed to connect", type="error", duration=5000)
    """
    
    _active_toasts = []
    
    @staticmethod
    def show(
        parent: tk.Widget,
        message: str,
        type: Literal["success", "error", "info", "warning"] = "info",
        duration: int = 3000
    ):
        """
        Show a toast notification.
        
        Args:
            parent: Parent widget (usually root window)
            message: Message to display
            type: Toast type (success/error/info/warning)
            duration: Duration in milliseconds before auto-dismiss
        """
        # Get colors for type
        colors = {
            "success": {
                "bg": Theme.SUCCESS,
                "icon": "✓"
            },
            "error": {
                "bg": Theme.DANGER,
                "icon": "✕"
            },
            "info": {
                "bg": Theme.INFO,
                "icon": "ℹ"
            },
            "warning": {
                "bg": Theme.WARNING,
                "icon": "⚠"
            }
        }
        
        color_config = colors.get(type, colors["info"])
        
        # Create toast window
        toast = tk.Toplevel(parent)
        toast.withdraw()  # Hide initially for positioning
        toast.overrideredirect(True)  # Remove window decorations
        toast.attributes("-topmost", True)  # Always on top
        
        # Try to make it transparent (platform-dependent)
        try:
            toast.attributes("-alpha", 0.95)
        except:
            pass
        
        # Toast frame
        toast_frame = tk.Frame(
            toast,
            bg=color_config["bg"],
            padx=20,
            pady=12
        )
        toast_frame.pack(fill=tk.BOTH, expand=True)
        
        # Content frame
        content_frame = tk.Frame(toast_frame, bg=color_config["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon
        icon_label = tk.Label(
            content_frame,
            text=color_config["icon"],
            bg=color_config["bg"],
            fg=Theme.TEXT_LIGHT,
            font=("Segoe UI", 14, "bold")
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Message
        message_label = tk.Label(
            content_frame,
            text=message,
            bg=color_config["bg"],
            fg=Theme.TEXT_LIGHT,
            font=("Segoe UI", 10),
            wraplength=300
        )
        message_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Close button
        close_btn = tk.Label(
            content_frame,
            text="✕",
            bg=color_config["bg"],
            fg=Theme.TEXT_LIGHT,
            font=("Segoe UI", 12),
            cursor="hand2"
        )
        close_btn.pack(side=tk.RIGHT, padx=(10, 0))
        close_btn.bind("<Button-1>", lambda e: Toast._dismiss_toast(toast))
        
        # Position toast
        toast.update_idletasks()
        window_width = toast.winfo_width()
        window_height = toast.winfo_height()
        
        # Get parent window position
        parent_x = parent.winfo_rootx()
        parent_width = parent.winfo_width()
        
        # Calculate position (top center of parent)
        x = parent_x + (parent_width - window_width) // 2
        
        # Stack toasts vertically
        y = 20
        for active_toast in Toast._active_toasts:
            if active_toast.winfo_exists():
                y += active_toast.winfo_height() + 10
        
        # Slide-in animation
        Toast._active_toasts.append(toast)
        Toast._slide_in(toast, x, y, 0)
        
        # Auto-dismiss after duration
        toast.after(duration, lambda: Toast._dismiss_toast(toast))
    
    @staticmethod
    def _slide_in(toast: tk.Toplevel, target_x: int, target_y: int, current_y: int):
        """Animate slide-in from top"""
        if current_y <= target_y:
            toast.geometry(f"+{target_x}+{current_y}")
            toast.deiconify()
            current_y += 5
            toast.after(10, lambda: Toast._slide_in(toast, target_x, target_y, current_y))
        else:
            toast.geometry(f"+{target_x}+{target_y}")
    
    @staticmethod
    def _dismiss_toast(toast: tk.Toplevel):
        """Dismiss toast with fade-out"""
        if toast in Toast._active_toasts:
            Toast._active_toasts.remove(toast)
        
        # Fade out animation
        Toast._fade_out(toast, 0.95)
    
    @staticmethod
    def _fade_out(toast: tk.Toplevel, alpha: float):
        """Animate fade-out"""
        if alpha > 0:
            try:
                toast.attributes("-alpha", alpha)
                toast.after(20, lambda: Toast._fade_out(toast, alpha - 0.05))
            except:
                toast.destroy()
        else:
            toast.destroy()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def show_loading_dialog(parent: tk.Widget, message: str = "Loading...") -> tk.Toplevel:
    """
    Show a modal loading dialog with spinner.
    
    Example:
        dialog = show_loading_dialog(root, "Fetching data...")
        # ... perform operation ...
        dialog.destroy()
    """
    dialog = tk.Toplevel(parent)
    dialog.overrideredirect(True)
    dialog.attributes("-topmost", True)
    
    # Center on parent
    dialog.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() - 200) // 2
    y = parent.winfo_y() + (parent.winfo_height() - 100) // 2
    dialog.geometry(f"200x100+{x}+{y}")
    
    # Content
    frame = tk.Frame(dialog, bg=Theme.BG_WHITE, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(
        frame,
        text=message,
        bg=Theme.BG_WHITE,
        font=("Segoe UI", 10)
    ).pack(pady=(0, 10))
    
    # Spinner (simulated with label)
    spinner = tk.Label(
        frame,
        text="⟳",
        bg=Theme.BG_WHITE,
        font=("Segoe UI", 24)
    )
    spinner.pack()
    
    # Rotate spinner
    def rotate_spinner(angle=0):
        # Unicode doesn't really rotate, but we can cycle through similar chars
        chars = ["⟳", "⟲", "⟳", "⟲"]
        spinner.config(text=chars[(angle // 90) % len(chars)])
        dialog.after(100, lambda: rotate_spinner(angle + 15))
    
    rotate_spinner()
    
    return dialog


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    'StyledButton',
    'StyledEntry',
    'StyledCard',
    'ProgressBar',
    'Toast',
    'Theme',
    'show_loading_dialog'
]

__version__ = '1.0.0'
