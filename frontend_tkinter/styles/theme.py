"""Simple ThemeManager for frontend_tkinter

This module provides a minimal runtime API for retrieving color/font/spacing
tokens depending on a light/dark theme. Kept intentionally small and dependency-free.
"""

from dataclasses import dataclass
from .colors import COLORS_LIGHT, COLORS_DARK
from .fonts import FONTS
from .spacing import SPACING


@dataclass
class ThemeManager:
    mode: str = 'light'  # 'light' | 'dark'

    def colors(self):
        return COLORS_DARK if self.mode == 'dark' else COLORS_LIGHT

    def fonts(self):
        return FONTS

    def spacing(self):
        return SPACING

    def set_mode(self, mode: str):
        if mode not in ('light', 'dark'):
            raise ValueError('mode must be "light" or "dark"')
        self.mode = mode
