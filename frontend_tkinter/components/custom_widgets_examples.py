"""
Custom Widgets Examples and Demo

This file demonstrates all custom widgets with practical usage examples.
Run this file to see an interactive demo of all components.

Author: Campus Event System Team
"""

import tkinter as tk
from tkinter import ttk
from custom_widgets import (
    StyledButton, StyledEntry, StyledCard, ProgressBar, Toast, Theme,
    show_loading_dialog
)
import time


# ============================================================================
# DEMO APPLICATION
# ============================================================================

class WidgetDemoApp:
    """Interactive demo showcasing all custom widgets"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Widgets Demo - Campus Event System")
        self.root.geometry("900x700")
        self.root.config(bg=Theme.BG_LIGHT)
        
        # Create notebook for different widget demos
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add tabs
        self._create_buttons_tab()
        self._create_entries_tab()
        self._create_cards_tab()
        self._create_progress_tab()
        self._create_toasts_tab()
        self._create_complete_form_tab()
    
    def _create_buttons_tab(self):
        """Demo for StyledButton"""
        frame = tk.Frame(self.notebook, bg=Theme.BG_LIGHT)
        self.notebook.add(frame, text="Buttons")
        
        container = tk.Frame(frame, bg=Theme.BG_LIGHT)
        container.pack(expand=True)
        
        tk.Label(
            container,
            text="StyledButton Variants",
            font=("Segoe UI", 16, "bold"),
            bg=Theme.BG_LIGHT
        ).pack(pady=(0, 20))
        
        # Primary buttons
        tk.Label(container, text="Primary Buttons:", bg=Theme.BG_LIGHT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 5))
        btn_frame1 = tk.Frame(container, bg=Theme.BG_LIGHT)
        btn_frame1.pack(pady=5)
        
        btn1 = StyledButton(btn_frame1, text="Primary Button", variant="primary", command=lambda: self._button_clicked("Primary"))
        btn1.pack(side=tk.LEFT, padx=5)
        
        btn2 = StyledButton(btn_frame1, text="Loading...", variant="primary")
        btn2.pack(side=tk.LEFT, padx=5)
        btn2.set_loading(True)
        
        btn3 = StyledButton(btn_frame1, text="Disabled", variant="primary")
        btn3.pack(side=tk.LEFT, padx=5)
        btn3.set_disabled(True)
        
        # Secondary buttons
        tk.Label(container, text="Secondary Buttons:", bg=Theme.BG_LIGHT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(20, 5))
        btn_frame2 = tk.Frame(container, bg=Theme.BG_LIGHT)
        btn_frame2.pack(pady=5)
        
        StyledButton(btn_frame2, text="Secondary", variant="secondary", command=lambda: self._button_clicked("Secondary")).pack(side=tk.LEFT, padx=5)
        StyledButton(btn_frame2, text="Success", variant="success", command=lambda: self._button_clicked("Success")).pack(side=tk.LEFT, padx=5)
        StyledButton(btn_frame2, text="Danger", variant="danger", command=lambda: self._button_clicked("Danger")).pack(side=tk.LEFT, padx=5)
        
        # Ghost buttons
        tk.Label(container, text="Ghost Buttons:", bg=Theme.BG_LIGHT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(20, 5))
        btn_frame3 = tk.Frame(container, bg=Theme.BG_LIGHT)
        btn_frame3.pack(pady=5)
        
        StyledButton(btn_frame3, text="Ghost Button", variant="ghost", command=lambda: self._button_clicked("Ghost")).pack(side=tk.LEFT, padx=5)
        
        # Interactive demo
        tk.Label(container, text="\nInteractive Demo:", bg=Theme.BG_LIGHT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(20, 5))
        
        self.demo_btn = StyledButton(container, text="Click to Simulate Loading", variant="primary", command=self._demo_loading)
        self.demo_btn.pack(pady=10)
        
        self.status_label = tk.Label(container, text="", bg=Theme.BG_LIGHT, font=("Segoe UI", 9))
        self.status_label.pack()
    
    def _create_entries_tab(self):
        """Demo for StyledEntry"""
        frame = tk.Frame(self.notebook, bg=Theme.BG_LIGHT)
        self.notebook.add(frame, text="Text Entries")
        
        container = tk.Frame(frame, bg=Theme.BG_LIGHT)
        container.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        tk.Label(
            container,
            text="StyledEntry Examples",
            font=("Segoe UI", 16, "bold"),
            bg=Theme.BG_LIGHT
        ).pack(pady=(0, 20))
        
        # Basic entry
        tk.Label(container, text="Basic Entry:", bg=Theme.BG_LIGHT, anchor="w").pack(fill=tk.X, pady=(10, 2))
        self.entry1 = StyledEntry(container, placeholder="Enter your name")
        self.entry1.pack(fill=tk.X, pady=5)
        
        # Entry with left icon
        tk.Label(container, text="Entry with Icon:", bg=Theme.BG_LIGHT, anchor="w").pack(fill=tk.X, pady=(10, 2))
        self.entry2 = StyledEntry(container, placeholder="Enter email", icon_left="📧", clear_button=True)
        self.entry2.pack(fill=tk.X, pady=5)
        
        # Password entry
        tk.Label(container, text="Password Entry:", bg=Theme.BG_LIGHT, anchor="w").pack(fill=tk.X, pady=(10, 2))
        self.entry3 = StyledEntry(container, placeholder="Enter password", icon_right="👁️", show="•")
        self.entry3.pack(fill=tk.X, pady=5)
        
        # Search entry
        tk.Label(container, text="Search Entry:", bg=Theme.BG_LIGHT, anchor="w").pack(fill=tk.X, pady=(10, 2))
        self.entry4 = StyledEntry(container, placeholder="Search events...", icon_left="🔍", clear_button=True)
        self.entry4.pack(fill=tk.X, pady=5)
        
        # Validation demo
        tk.Label(container, text="\nValidation Demo:", bg=Theme.BG_LIGHT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(20, 5))
        
        self.email_entry = StyledEntry(container, placeholder="Enter email for validation", icon_left="📧")
        self.email_entry.pack(fill=tk.X, pady=5)
        
        btn_frame = tk.Frame(container, bg=Theme.BG_LIGHT)
        btn_frame.pack(pady=10)
        
        StyledButton(btn_frame, text="Validate Email", variant="primary", command=self._validate_email).pack(side=tk.LEFT, padx=5)
        StyledButton(btn_frame, text="Clear State", variant="secondary", command=lambda: self.email_entry.clear_state()).pack(side=tk.LEFT, padx=5)
    
    def _create_cards_tab(self):
        """Demo for StyledCard"""
        frame = tk.Frame(self.notebook, bg=Theme.BG_LIGHT)
        self.notebook.add(frame, text="Cards")
        
        # Scrollable container
        canvas = tk.Canvas(frame, bg=Theme.BG_LIGHT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Theme.BG_LIGHT)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            scrollable_frame,
            text="StyledCard Examples",
            font=("Segoe UI", 16, "bold"),
            bg=Theme.BG_LIGHT
        ).pack(pady=(0, 20))
        
        # Event card
        card1 = StyledCard(scrollable_frame, padding=20, hover=True)
        card1.pack(fill=tk.X, pady=10)
        
        tk.Label(card1.content_frame, text="Upcoming Event", font=("Segoe UI", 14, "bold"), bg=Theme.BG_CARD).pack(anchor="w")
        tk.Label(card1.content_frame, text="Tech Workshop 2025", font=("Segoe UI", 12), bg=Theme.BG_CARD, fg=Theme.PRIMARY).pack(anchor="w", pady=(5, 0))
        tk.Label(card1.content_frame, text="📅 October 15, 2025 | 📍 Lab 101", bg=Theme.BG_CARD, fg=Theme.TEXT_MUTED).pack(anchor="w", pady=(5, 0))
        tk.Label(card1.content_frame, text="Learn about the latest web technologies and frameworks.", bg=Theme.BG_CARD, wraplength=400).pack(anchor="w", pady=(10, 0))
        
        # User profile card
        card2 = StyledCard(scrollable_frame, padding=20, hover=True, click_handler=lambda: Toast.show(self.root, "Card clicked!", "info"))
        card2.pack(fill=tk.X, pady=10)
        
        profile_header = tk.Frame(card2.content_frame, bg=Theme.BG_CARD)
        profile_header.pack(fill=tk.X)
        
        tk.Label(profile_header, text="👤", font=("Segoe UI", 32), bg=Theme.BG_CARD).pack(side=tk.LEFT, padx=(0, 15))
        
        info_frame = tk.Frame(profile_header, bg=Theme.BG_CARD)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(info_frame, text="John Doe", font=("Segoe UI", 14, "bold"), bg=Theme.BG_CARD).pack(anchor="w")
        tk.Label(info_frame, text="Computer Science Student", bg=Theme.BG_CARD, fg=Theme.TEXT_MUTED).pack(anchor="w")
        tk.Label(info_frame, text="john.doe@university.edu", bg=Theme.BG_CARD, fg=Theme.PRIMARY).pack(anchor="w", pady=(5, 0))
        
        # Stats card
        card3 = StyledCard(scrollable_frame, padding=20, hover=True)
        card3.pack(fill=tk.X, pady=10)
        
        tk.Label(card3.content_frame, text="Event Statistics", font=("Segoe UI", 14, "bold"), bg=Theme.BG_CARD).pack(anchor="w", pady=(0, 15))
        
        stats_frame = tk.Frame(card3.content_frame, bg=Theme.BG_CARD)
        stats_frame.pack(fill=tk.X)
        
        for i, (label, value, color) in enumerate([
            ("Total Events", "42", Theme.PRIMARY),
            ("Registered", "28", Theme.SUCCESS),
            ("Pending", "5", Theme.WARNING)
        ]):
            stat_col = tk.Frame(stats_frame, bg=Theme.BG_CARD)
            stat_col.pack(side=tk.LEFT, expand=True, padx=10)
            
            tk.Label(stat_col, text=value, font=("Segoe UI", 24, "bold"), bg=Theme.BG_CARD, fg=color).pack()
            tk.Label(stat_col, text=label, bg=Theme.BG_CARD, fg=Theme.TEXT_MUTED).pack()
        
        # Clickable card demo
        tk.Label(
            scrollable_frame,
            text="💡 Tip: The profile card is clickable!",
            bg=Theme.BG_LIGHT,
            fg=Theme.TEXT_MUTED,
            font=("Segoe UI", 9, "italic")
        ).pack(pady=10)
    
    def _create_progress_tab(self):
        """Demo for ProgressBar"""
        frame = tk.Frame(self.notebook, bg=Theme.BG_LIGHT)
        self.notebook.add(frame, text="Progress Bars")
        
        container = tk.Frame(frame, bg=Theme.BG_LIGHT)
        container.pack(expand=True)
        
        tk.Label(
            container,
            text="ProgressBar Examples",
            font=("Segoe UI", 16, "bold"),
            bg=Theme.BG_LIGHT
        ).pack(pady=(0, 20))
        
        # Static progress bars
        tk.Label(container, text="Different Progress Levels:", bg=Theme.BG_LIGHT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        for percent, color in [(25, Theme.DANGER), (50, Theme.WARNING), (75, Theme.INFO), (100, Theme.SUCCESS)]:
            progress = ProgressBar(container, width=400, height=24, fg_color=color)
            progress.pack(pady=8)
            progress.set_progress(percent)
        
        # Animated demo
        tk.Label(container, text="\nAnimated Demo:", bg=Theme.BG_LIGHT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(20, 5))
        
        self.demo_progress = ProgressBar(container, width=400, height=28, fg_color=Theme.PRIMARY)
        self.demo_progress.pack(pady=10)
        
        btn_frame = tk.Frame(container, bg=Theme.BG_LIGHT)
        btn_frame.pack(pady=10)
        
        StyledButton(btn_frame, text="Set 25%", variant="ghost", command=lambda: self.demo_progress.set_progress(25)).pack(side=tk.LEFT, padx=3)
        StyledButton(btn_frame, text="Set 50%", variant="ghost", command=lambda: self.demo_progress.set_progress(50)).pack(side=tk.LEFT, padx=3)
        StyledButton(btn_frame, text="Set 75%", variant="ghost", command=lambda: self.demo_progress.set_progress(75)).pack(side=tk.LEFT, padx=3)
        StyledButton(btn_frame, text="Set 100%", variant="ghost", command=lambda: self.demo_progress.set_progress(100)).pack(side=tk.LEFT, padx=3)
        StyledButton(btn_frame, text="Reset", variant="secondary", command=lambda: self.demo_progress.reset()).pack(side=tk.LEFT, padx=3)
        
        # Upload simulation
        tk.Label(container, text="\nFile Upload Simulation:", bg=Theme.BG_LIGHT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(20, 5))
        
        self.upload_progress = ProgressBar(container, width=400, height=24, fg_color=Theme.SUCCESS)
        self.upload_progress.pack(pady=10)
        
        StyledButton(container, text="Simulate Upload", variant="primary", command=self._simulate_upload).pack(pady=5)
    
    def _create_toasts_tab(self):
        """Demo for Toast notifications"""
        frame = tk.Frame(self.notebook, bg=Theme.BG_LIGHT)
        self.notebook.add(frame, text="Toast Notifications")
        
        container = tk.Frame(frame, bg=Theme.BG_LIGHT)
        container.pack(expand=True)
        
        tk.Label(
            container,
            text="Toast Notification Examples",
            font=("Segoe UI", 16, "bold"),
            bg=Theme.BG_LIGHT
        ).pack(pady=(0, 20))
        
        tk.Label(
            container,
            text="Click buttons to show different toast types:",
            bg=Theme.BG_LIGHT,
            font=("Segoe UI", 10)
        ).pack(pady=10)
        
        # Toast buttons
        btn_frame = tk.Frame(container, bg=Theme.BG_LIGHT)
        btn_frame.pack(pady=20)
        
        StyledButton(
            btn_frame,
            text="Success Toast",
            variant="success",
            command=lambda: Toast.show(self.root, "Operation completed successfully!", "success")
        ).pack(pady=5)
        
        StyledButton(
            btn_frame,
            text="Error Toast",
            variant="danger",
            command=lambda: Toast.show(self.root, "An error occurred while processing your request.", "error")
        ).pack(pady=5)
        
        StyledButton(
            btn_frame,
            text="Info Toast",
            variant="primary",
            command=lambda: Toast.show(self.root, "New event added to your calendar.", "info")
        ).pack(pady=5)
        
        StyledButton(
            btn_frame,
            text="Warning Toast",
            variant="secondary",
            command=lambda: Toast.show(self.root, "Your session will expire in 5 minutes.", "warning")
        ).pack(pady=5)
        
        # Multiple toasts demo
        tk.Label(
            container,
            text="\nMultiple Toasts Demo:",
            bg=Theme.BG_LIGHT,
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(30, 5))
        
        StyledButton(
            container,
            text="Show Multiple Toasts",
            variant="ghost",
            command=self._show_multiple_toasts
        ).pack(pady=5)
    
    def _create_complete_form_tab(self):
        """Complete form example using all widgets"""
        frame = tk.Frame(self.notebook, bg=Theme.BG_LIGHT)
        self.notebook.add(frame, text="Complete Form Example")
        
        # Scrollable container
        canvas = tk.Canvas(frame, bg=Theme.BG_LIGHT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Theme.BG_LIGHT)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form card
        form_card = StyledCard(scrollable_frame, padding=30)
        form_card.pack(padx=40, pady=20, fill=tk.X)
        
        tk.Label(
            form_card.content_frame,
            text="Create New Event",
            font=("Segoe UI", 18, "bold"),
            bg=Theme.BG_CARD
        ).pack(anchor="w", pady=(0, 10))
        
        tk.Label(
            form_card.content_frame,
            text="Fill in the details to create a new campus event",
            bg=Theme.BG_CARD,
            fg=Theme.TEXT_MUTED
        ).pack(anchor="w", pady=(0, 20))
        
        # Event name
        tk.Label(form_card.content_frame, text="Event Name *", bg=Theme.BG_CARD, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 2))
        self.form_name = StyledEntry(form_card.content_frame, placeholder="Enter event name", icon_left="📝")
        self.form_name.pack(fill=tk.X, pady=5)
        
        # Event category
        tk.Label(form_card.content_frame, text="Category *", bg=Theme.BG_CARD, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 2))
        self.form_category = StyledEntry(form_card.content_frame, placeholder="e.g., Workshop, Seminar, Sports", icon_left="🏷️")
        self.form_category.pack(fill=tk.X, pady=5)
        
        # Date and time
        date_frame = tk.Frame(form_card.content_frame, bg=Theme.BG_CARD)
        date_frame.pack(fill=tk.X, pady=10)
        
        date_col = tk.Frame(date_frame, bg=Theme.BG_CARD)
        date_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        tk.Label(date_col, text="Date *", bg=Theme.BG_CARD, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 2))
        self.form_date = StyledEntry(date_col, placeholder="DD/MM/YYYY", icon_left="📅")
        self.form_date.pack(fill=tk.X, pady=5)
        
        time_col = tk.Frame(date_frame, bg=Theme.BG_CARD)
        time_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        tk.Label(time_col, text="Time *", bg=Theme.BG_CARD, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 2))
        self.form_time = StyledEntry(time_col, placeholder="HH:MM", icon_left="🕐")
        self.form_time.pack(fill=tk.X, pady=5)
        
        # Venue
        tk.Label(form_card.content_frame, text="Venue *", bg=Theme.BG_CARD, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 2))
        self.form_venue = StyledEntry(form_card.content_frame, placeholder="Enter venue", icon_left="📍", clear_button=True)
        self.form_venue.pack(fill=tk.X, pady=5)
        
        # Max participants
        tk.Label(form_card.content_frame, text="Max Participants", bg=Theme.BG_CARD, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 2))
        self.form_max = StyledEntry(form_card.content_frame, placeholder="Enter maximum capacity", icon_left="👥")
        self.form_max.pack(fill=tk.X, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(form_card.content_frame, bg=Theme.BG_CARD)
        btn_frame.pack(pady=(20, 0))
        
        StyledButton(btn_frame, text="Cancel", variant="ghost", command=self._reset_form, width=100).pack(side=tk.LEFT, padx=5)
        self.submit_btn = StyledButton(btn_frame, text="Create Event", variant="success", command=self._submit_form, width=140)
        self.submit_btn.pack(side=tk.LEFT, padx=5)
    
    # Helper methods
    
    def _button_clicked(self, variant):
        Toast.show(self.root, f"{variant} button clicked!", "info")
    
    def _demo_loading(self):
        self.demo_btn.set_loading(True)
        self.demo_btn.set_text("Processing...")
        self.status_label.config(text="⏳ Loading...")
        
        def finish_loading():
            self.demo_btn.set_loading(False)
            self.demo_btn.set_text("Click to Simulate Loading")
            self.status_label.config(text="✓ Completed!")
            Toast.show(self.root, "Operation completed successfully!", "success")
        
        self.root.after(2000, finish_loading)
    
    def _validate_email(self):
        email = self.email_entry.get()
        
        if not email:
            self.email_entry.set_error("Email is required")
        elif "@" not in email or "." not in email:
            self.email_entry.set_error("Invalid email format")
        else:
            self.email_entry.set_success()
            Toast.show(self.root, "Email is valid!", "success")
    
    def _simulate_upload(self):
        self.upload_progress.reset()
        
        def update_progress(current):
            if current <= 100:
                self.upload_progress.set_progress(current)
                self.root.after(50, lambda: update_progress(current + 5))
            else:
                Toast.show(self.root, "File uploaded successfully!", "success")
        
        update_progress(0)
    
    def _show_multiple_toasts(self):
        Toast.show(self.root, "First notification", "info")
        self.root.after(300, lambda: Toast.show(self.root, "Second notification", "success"))
        self.root.after(600, lambda: Toast.show(self.root, "Third notification", "warning"))
    
    def _submit_form(self):
        # Validate
        errors = []
        
        if not self.form_name.get():
            self.form_name.set_error("Event name is required")
            errors.append("name")
        
        if not self.form_category.get():
            self.form_category.set_error("Category is required")
            errors.append("category")
        
        if not self.form_date.get():
            self.form_date.set_error("Date is required")
            errors.append("date")
        
        if not self.form_time.get():
            self.form_time.set_error("Time is required")
            errors.append("time")
        
        if not self.form_venue.get():
            self.form_venue.set_error("Venue is required")
            errors.append("venue")
        
        if errors:
            Toast.show(self.root, "Please fill in all required fields", "error")
            return
        
        # Simulate submission
        self.submit_btn.set_loading(True)
        self.submit_btn.set_text("Creating...")
        
        def finish_submit():
            self.submit_btn.set_loading(False)
            self.submit_btn.set_text("Create Event")
            Toast.show(self.root, "Event created successfully!", "success")
            self._reset_form()
        
        self.root.after(1500, finish_submit)
    
    def _reset_form(self):
        self.form_name.clear()
        self.form_category.clear()
        self.form_date.clear()
        self.form_time.clear()
        self.form_venue.clear()
        self.form_max.clear()


# ============================================================================
# RUN DEMO
# ============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = WidgetDemoApp(root)
    root.mainloop()
