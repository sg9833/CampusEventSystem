import tkinter as tk
from typing import Optional
from frontend_tkinter.styles import theme


class ModernEntry(tk.Frame):
    """A styled entry with placeholder and focus border."""

    def __init__(self, parent, placeholder: str = '', is_password: bool = False, width: int = 300, **kwargs):
        super().__init__(parent, **kwargs)
        self._theme = theme.ThemeManager()
        self.placeholder = placeholder
        self.is_password = is_password
        self.width = width

        colors = self._theme.colors()

        self.config(bg=colors['bg_card'])

        self.var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.var, bd=0, relief='flat', font=self._theme.fonts().get('input'))
        self.entry.pack(fill='both', expand=True, padx=8, pady=8)

        # Placeholder behavior
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.config(fg=colors['text_secondary'])
            self._has_placeholder = True
        else:
            self._has_placeholder = False

        if is_password:
            self._show_char = ''
        else:
            self._show_char = None

        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)

    def _on_focus_in(self, event):
        colors = self._theme.colors()
        if self._has_placeholder:
            self.entry.delete(0, 'end')
            self.entry.config(fg=colors['text_primary'])
            self._has_placeholder = False
        if self.is_password:
            self.entry.config(show='*')

    def _on_focus_out(self, event):
        colors = self._theme.colors()
        if not self.entry.get():
            if self.placeholder:
                self.entry.insert(0, self.placeholder)
                self.entry.config(fg=colors['text_secondary'])
                self._has_placeholder = True
            if self.is_password:
                self.entry.config(show='')

    def get(self) -> str:
        if self._has_placeholder:
            return ''
        return self.var.get()
