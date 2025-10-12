"""
Button Styles - Simple utility for consistent button styling across the application
"""

import tkinter as tk
from tkinter import ttk


class ButtonStyles:
    """Simple button styling utility."""
    
    # Color constants
    PRIMARY_BG = "#3047ff"
    PRIMARY_FG = "white"
    PRIMARY_HOVER = "#2038cc"
    
    SECONDARY_BG = "#6c757d"
    SECONDARY_FG = "white"
    SECONDARY_HOVER = "#5a6268"
    
    SUCCESS_BG = "#28a745"
    SUCCESS_FG = "white"
    SUCCESS_HOVER = "#218838"
    
    DANGER_BG = "#dc3545"
    DANGER_FG = "white"
    DANGER_HOVER = "#c82333"
    
    @staticmethod
    def apply_primary_style(button):
        """Apply primary button style."""
        button.config(
            bg=ButtonStyles.PRIMARY_BG,
            fg=ButtonStyles.PRIMARY_FG,
            activebackground=ButtonStyles.PRIMARY_HOVER,
            activeforeground=ButtonStyles.PRIMARY_FG,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        return button
    
    @staticmethod
    def apply_secondary_style(button):
        """Apply secondary button style."""
        button.config(
            bg=ButtonStyles.SECONDARY_BG,
            fg=ButtonStyles.SECONDARY_FG,
            activebackground=ButtonStyles.SECONDARY_HOVER,
            activeforeground=ButtonStyles.SECONDARY_FG,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        return button
    
    @staticmethod
    def apply_success_style(button):
        """Apply success button style."""
        button.config(
            bg=ButtonStyles.SUCCESS_BG,
            fg=ButtonStyles.SUCCESS_FG,
            activebackground=ButtonStyles.SUCCESS_HOVER,
            activeforeground=ButtonStyles.SUCCESS_FG,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        return button
    
    @staticmethod
    def apply_danger_style(button):
        """Apply danger button style."""
        button.config(
            bg=ButtonStyles.DANGER_BG,
            fg=ButtonStyles.DANGER_FG,
            activebackground=ButtonStyles.DANGER_HOVER,
            activeforeground=ButtonStyles.DANGER_FG,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        return button
    
    @staticmethod
    def create_styled_button(parent, text, command=None, style='primary', **kwargs):
        """Create a button with predefined style."""
        # Set default font for macOS compatibility
        if 'font' not in kwargs:
            kwargs['font'] = ("Helvetica", 12)
        
        button = tk.Button(parent, text=text, command=command, **kwargs)
        
        if style == 'primary':
            ButtonStyles.apply_primary_style(button)
        elif style == 'secondary':
            ButtonStyles.apply_secondary_style(button)
        elif style == 'success':
            ButtonStyles.apply_success_style(button)
        elif style == 'danger':
            ButtonStyles.apply_danger_style(button)
        
        return button
    
    @staticmethod
    def create_button(parent, text, command=None, variant='primary', **kwargs):
        """Create a button with predefined style (alias for create_styled_button)."""
        return ButtonStyles.create_styled_button(parent, text, command, style=variant, **kwargs)
    
    @staticmethod
    def create_icon_button(parent, icon=None, command=None, variant='secondary', text=None, **kwargs):
        """Create an icon button with predefined style."""
        # Use text parameter if icon is not provided (for compatibility)
        icon_text = icon if icon is not None else text
        button = tk.Button(parent, text=icon_text, command=command, **kwargs)
        
        if variant == 'primary':
            ButtonStyles.apply_primary_style(button)
        elif variant == 'secondary':
            ButtonStyles.apply_secondary_style(button)
        elif variant == 'success':
            ButtonStyles.apply_success_style(button)
        elif variant == 'danger':
            ButtonStyles.apply_danger_style(button)
        
        return button
