import tkinter as tk
from typing import Callable
from frontend_tkinter.styles import theme


class ModernButton(tk.Canvas):
    """A modern button implemented on a Canvas with rounded corners and hover."""

    def __init__(self, parent, text: str, command: Callable = None,
                 style: str = 'primary', width: int = 140, height: int = 40, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)

        self._theme = theme.ThemeManager()
        self.text = text
        self.command = command
        self.style = style
        self.width = width
        self.height = height
        self._disabled = False

        self._colors = self._resolve_style_colors(style)

        # Create visual elements
        self._rect = None
        self._text_id = None

        # Draw initial
        self.draw()
        self.bind_events()

    def _resolve_style_colors(self, style_name: str):
        colors = self._theme.colors()
        styles = {
            'primary': {'bg': colors['primary'], 'hover': colors['primary_hover'], 'fg': colors['bg_main']},
            'secondary': {'bg': '#6B7280', 'hover': '#4B5563', 'fg': colors['bg_main']},
            'success': {'bg': colors['success'], 'hover': '#059669', 'fg': colors['bg_main']},
            'danger': {'bg': colors['error'], 'hover': '#DC2626', 'fg': colors['bg_main']},
            'ghost': {'bg': colors['bg_card'], 'hover': colors['bg_tertiary'], 'fg': colors['text_primary']},
        }
        return styles.get(style_name, styles['primary'])

    def draw(self):
        self.delete('all')
        r = 8  # radius
        w = self.width
        h = self.height

        # Draw rounded rect
        points = [
            r, 0, w - r, 0,
            w, 0, w, r,
            w, h - r, w, h,
            w - r, h, r, h,
            0, h, 0, h - r,
            0, r, 0, 0
        ]
        self._rect = self.create_polygon(points, smooth=True, fill=self._colors['bg'], outline='')

        # Text
        self._text_id = self.create_text(w // 2, h // 2, text=self.text, fill=self._colors['fg'],
                                         font=self._theme.fonts().get('button', ('Segoe UI', 12, 'bold')))

    def bind_events(self):
        self.tag_bind(self._rect, '<Enter>', self._on_enter)
        self.tag_bind(self._text_id, '<Enter>', self._on_enter)
        self.tag_bind(self._rect, '<Leave>', self._on_leave)
        self.tag_bind(self._text_id, '<Leave>', self._on_leave)
        self.tag_bind(self._rect, '<Button-1>', self._on_click)
        self.tag_bind(self._text_id, '<Button-1>', self._on_click)

    def _on_enter(self, event):
        if not self._disabled:
            self.itemconfig(self._rect, fill=self._colors['hover'])

    def _on_leave(self, event):
        if not self._disabled:
            self.itemconfig(self._rect, fill=self._colors['bg'])

    def _on_click(self, event):
        if not self._disabled and callable(self.command):
            try:
                self.command()
            except Exception:
                # Keep widget robust; higher-level code handles errors
                pass

    def set_disabled(self, disabled: bool = True):
        self._disabled = disabled
        if disabled:
            self.itemconfig(self._rect, fill='#A1A1AA')
            self.itemconfig(self._text_id, fill='#F3F4F6')
        else:
            self.itemconfig(self._rect, fill=self._colors['bg'])
            self.itemconfig(self._text_id, fill=self._colors['fg'])
