#!/usr/bin/env python3
"""Test if Tkinter works"""
import sys
print("Python version:", sys.version)

try:
    import tkinter as tk
    print("Tkinter imported successfully!")
    print("Tkinter version:", tk.TkVersion)
    
    # Try to create a window
    root = tk.Tk()
    root.title("Test")
    label = tk.Label(root, text="Tkinter works!")
    label.pack()
    print("Window created successfully! Close the window to continue.")
    root.mainloop()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
