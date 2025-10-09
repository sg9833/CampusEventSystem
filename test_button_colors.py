#!/usr/bin/env python3
"""
Quick test to verify button colors are working in Tkinter on macOS
"""
import tkinter as tk

root = tk.Tk()
root.title("Button Color Test")
root.geometry("400x300")

# Test different button configurations
configs = [
    ("Dark BG + White Text", "#2C3E50", "#FFFFFF", "raised", 2),
    ("Blue BG + White Text", "#3498DB", "#FFFFFF", "flat", 0),
    ("Green BG + White Text", "#27AE60", "#FFFFFF", "flat", 0),
    ("Indigo BG + White Text", "#5856D6", "#FFFFFF", "flat", 0),
    ("System Default", None, None, "raised", 2),
]

for i, (label, bg, fg, relief, bd) in enumerate(configs):
    config = {
        "text": label,
        "font": ("Helvetica", 11, "bold"),
        "relief": relief,
        "borderwidth": bd,
        "height": 2,
        "width": 30
    }
    if bg:
        config["bg"] = bg
    if fg:
        config["fg"] = fg
    
    btn = tk.Button(root, **config)
    btn.pack(pady=10, padx=20)

root.mainloop()
