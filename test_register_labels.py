#!/usr/bin/env python3
"""Test script to verify registration page label visibility."""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add frontend_tkinter to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend_tkinter'))

# Mock controller for testing
class MockController:
    def __init__(self):
        self.colors = {
            'background': '#ECF0F1',
            'primary': '#2C3E50',
            'danger': '#E74C3C'
        }
    
    def navigate(self, page):
        print(f"Navigate to: {page}")

# Create test window
root = tk.Tk()
root.title("Registration Form Label Test")
root.geometry("700x900")
root.configure(bg='#ECF0F1')

# Create mock controller
controller = MockController()

# Import and create register page
from pages.register_page import RegisterPage

# Create container
container = tk.Frame(root, bg='#ECF0F1')
container.pack(fill='both', expand=True)

# Create register page
register_page = RegisterPage(container, controller)
register_page.pack(fill='both', expand=True)

# Add debug button to check label widgets
def debug_labels():
    print("\n=== Label Widget Debug ===")
    for widget in register_page.form.winfo_children():
        if isinstance(widget, tk.Label):
            text = widget.cget('text')
            if text and text not in ['', 'Create your account', 'Already have an account?']:
                grid_info = widget.grid_info()
                print(f"Label: '{text}'")
                print(f"  Position: row={grid_info.get('row')}, column={grid_info.get('column')}")
                print(f"  Sticky: {grid_info.get('sticky')}")
                print(f"  Padx: {grid_info.get('padx')}, Pady: {grid_info.get('pady')}")
                print(f"  Colors: fg={widget.cget('fg')}, bg={widget.cget('bg')}")
                print(f"  Font: {widget.cget('font')}")
                print(f"  Size: {widget.winfo_reqwidth()}x{widget.winfo_reqheight()}")
                print()

debug_btn = tk.Button(root, text="Debug Labels", command=debug_labels, bg='#3498DB', fg='white', padx=10, pady=5)
debug_btn.pack(pady=10)

print("Registration form loaded. Check if labels are visible.")
print("Click 'Debug Labels' button to see label widget information.")

root.mainloop()
