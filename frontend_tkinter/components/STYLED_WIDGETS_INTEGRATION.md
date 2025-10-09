# Custom Styled Widgets Integration Guide

This guide shows how to integrate custom styled widgets into existing pages of the Campus Event System.

## Table of Contents
1. [Before & After Comparisons](#before--after-comparisons)
2. [Login Page Integration](#login-page-integration)
3. [Dashboard Integration](#dashboard-integration)
4. [Event Form Integration](#event-form-integration)
5. [Search & Filter Integration](#search--filter-integration)
6. [Notifications Integration](#notifications-integration)
7. [Best Practices](#best-practices)

## Before & After Comparisons

### Standard Tkinter Button vs StyledButton

**Before (Standard Tkinter):**
```python
import tkinter as tk

submit_btn = tk.Button(
    parent,
    text="Submit",
    bg="#3498DB",
    fg="white",
    font=("Arial", 10),
    command=submit_handler,
    relief="flat",
    padx=20,
    pady=10
)
submit_btn.pack(pady=10)

# No built-in loading state
# Manual state management required
# No hover effects
# Inconsistent styling
```

**After (StyledButton):**
```python
from components import StyledButton

submit_btn = StyledButton(
    parent,
    text="Submit",
    variant="primary",
    command=submit_handler,
    width=120,
    height=36
)
submit_btn.pack(pady=10)

# Built-in loading state
submit_btn.set_loading(True)

# Built-in disabled state
submit_btn.set_disabled(True)

# Automatic hover effects
# Consistent theming
# Spinner animation included
```

### Standard Entry vs StyledEntry

**Before (Standard Tkinter):**
```python
import tkinter as tk

email_frame = tk.Frame(parent)
email_frame.pack(fill='x', pady=5)

tk.Label(email_frame, text="📧").pack(side='left')
email_entry = tk.Entry(email_frame, width=30)
email_entry.pack(side='left', fill='x', expand=True)

# Manual placeholder management
email_entry.insert(0, "Enter email")
email_entry.config(fg='gray')

def on_focus_in(event):
    if email_entry.get() == "Enter email":
        email_entry.delete(0, 'end')
        email_entry.config(fg='black')

email_entry.bind("<FocusIn>", on_focus_in)

# Manual error handling
error_label = tk.Label(parent, text="", fg='red')
error_label.pack()

# Validation
if not email_entry.get() or email_entry.get() == "Enter email":
    error_label.config(text="Email is required")
```

**After (StyledEntry):**
```python
from components import StyledEntry

email_entry = StyledEntry(
    parent,
    placeholder="Enter email",
    icon_left="📧",
    clear_button=True
)
email_entry.pack(fill='x', pady=5)

# Automatic placeholder management
# Built-in error display
if not email_entry.get():
    email_entry.set_error("Email is required")

# Built-in success state
else:
    email_entry.set_success()

# Get value (handles placeholder automatically)
email = email_entry.get()
```

## Login Page Integration

### Original Login Page (Simplified)

```python
# pages/login_page.py (BEFORE)
import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title
        tk.Label(
            self,
            text="Campus Event System",
            font=("Arial", 24, "bold")
        ).pack(pady=20)
        
        # Email
        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack(pady=5)
        
        # Password
        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        # Login button
        self.login_btn = tk.Button(
            self,
            text="Login",
            bg="#3498DB",
            fg="white",
            command=self.login
        )
        self.login_btn.pack(pady=10)
        
        # Error label
        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email:
            self.error_label.config(text="Email is required")
            return
        
        if not password:
            self.error_label.config(text="Password is required")
            return
        
        # Disable button during login
        self.login_btn.config(state="disabled", text="Logging in...")
        
        # Simulate API call
        self.after(1000, lambda: self._finish_login(True))
    
    def _finish_login(self, success):
        self.login_btn.config(state="normal", text="Login")
        
        if success:
            # Navigate to dashboard
            pass
        else:
            self.error_label.config(text="Invalid credentials")
```

### Updated Login Page with Styled Widgets

```python
# pages/login_page.py (AFTER)
import tkinter as tk
from components import StyledButton, StyledEntry, StyledCard, Toast

class LoginPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, bg="#F8F9FA")
        self.root = root
        
        # Center container
        center_frame = tk.Frame(self, bg="#F8F9FA")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Login card
        login_card = StyledCard(center_frame, padding=40)
        login_card.pack()
        
        # Title
        tk.Label(
            login_card.content_frame,
            text="Campus Event System",
            font=("Segoe UI", 24, "bold"),
            bg="white"
        ).pack(pady=(0, 10))
        
        tk.Label(
            login_card.content_frame,
            text="Sign in to your account",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="white"
        ).pack(pady=(0, 30))
        
        # Email field
        tk.Label(
            login_card.content_frame,
            text="Email Address",
            font=("Segoe UI", 9, "bold"),
            bg="white"
        ).pack(anchor='w', pady=(10, 2))
        
        self.email_entry = StyledEntry(
            login_card.content_frame,
            placeholder="Enter your email",
            icon_left="📧",
            width=35
        )
        self.email_entry.pack(fill='x', pady=5)
        
        # Password field
        tk.Label(
            login_card.content_frame,
            text="Password",
            font=("Segoe UI", 9, "bold"),
            bg="white"
        ).pack(anchor='w', pady=(15, 2))
        
        self.password_entry = StyledEntry(
            login_card.content_frame,
            placeholder="Enter your password",
            icon_right="👁️",
            show="•",
            width=35
        )
        self.password_entry.pack(fill='x', pady=5)
        
        # Forgot password link
        forgot_link = tk.Label(
            login_card.content_frame,
            text="Forgot password?",
            font=("Segoe UI", 8),
            fg="#3498DB",
            bg="white",
            cursor="hand2"
        )
        forgot_link.pack(anchor='e', pady=(5, 0))
        
        # Login button
        self.login_btn = StyledButton(
            login_card.content_frame,
            text="Sign In",
            variant="primary",
            command=self.login,
            width=300,
            height=40
        )
        self.login_btn.pack(pady=(20, 0), fill='x')
        
        # Register link
        register_frame = tk.Frame(login_card.content_frame, bg="white")
        register_frame.pack(pady=(15, 0))
        
        tk.Label(
            register_frame,
            text="Don't have an account? ",
            font=("Segoe UI", 9),
            bg="white"
        ).pack(side='left')
        
        register_link = tk.Label(
            register_frame,
            text="Sign up",
            font=("Segoe UI", 9, "bold"),
            fg="#3498DB",
            bg="white",
            cursor="hand2"
        )
        register_link.pack(side='left')
    
    def login(self):
        # Clear previous errors
        self.email_entry.clear_state()
        self.password_entry.clear_state()
        
        # Validate
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        errors = False
        
        if not email:
            self.email_entry.set_error("Email is required")
            errors = True
        elif "@" not in email:
            self.email_entry.set_error("Invalid email format")
            errors = True
        
        if not password:
            self.password_entry.set_error("Password is required")
            errors = True
        elif len(password) < 6:
            self.password_entry.set_error("Password must be at least 6 characters")
            errors = True
        
        if errors:
            Toast.show(self.root, "Please fix the errors", type="error")
            return
        
        # Show loading state
        self.login_btn.set_loading(True)
        self.login_btn.set_text("Signing in...")
        
        # Simulate API call
        self.after(1500, lambda: self._finish_login(True))
    
    def _finish_login(self, success):
        self.login_btn.set_loading(False)
        self.login_btn.set_text("Sign In")
        
        if success:
            Toast.show(self.root, "Login successful!", type="success")
            # Navigate to dashboard
            # self.controller.show_dashboard()
        else:
            Toast.show(self.root, "Invalid email or password", type="error")
```

## Dashboard Integration

### Adding Cards to Dashboard

```python
# pages/student_dashboard.py (PARTIAL UPDATE)
from components import StyledCard, StyledButton, ProgressBar, Theme

class StudentDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F8F9FA")
        self.controller = controller
        
        # ... existing code ...
        
        # Stats section with cards
        stats_frame = tk.Frame(self, bg="#F8F9FA")
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Events Card
        events_card = StyledCard(stats_frame, padding=20, hover=True)
        events_card.pack(side='left', padx=10, fill='both', expand=True)
        
        tk.Label(
            events_card.content_frame,
            text="📅",
            font=("Segoe UI", 32),
            bg="white"
        ).pack(pady=(0, 10))
        
        tk.Label(
            events_card.content_frame,
            text="24",
            font=("Segoe UI", 28, "bold"),
            fg=Theme.PRIMARY,
            bg="white"
        ).pack()
        
        tk.Label(
            events_card.content_frame,
            text="Registered Events",
            font=("Segoe UI", 10),
            fg=Theme.TEXT_MUTED,
            bg="white"
        ).pack()
        
        # Bookings Card
        bookings_card = StyledCard(stats_frame, padding=20, hover=True)
        bookings_card.pack(side='left', padx=10, fill='both', expand=True)
        
        tk.Label(
            bookings_card.content_frame,
            text="🏫",
            font=("Segoe UI", 32),
            bg="white"
        ).pack(pady=(0, 10))
        
        tk.Label(
            bookings_card.content_frame,
            text="12",
            font=("Segoe UI", 28, "bold"),
            fg=Theme.SUCCESS,
            bg="white"
        ).pack()
        
        tk.Label(
            bookings_card.content_frame,
            text="Active Bookings",
            font=("Segoe UI", 10),
            fg=Theme.TEXT_MUTED,
            bg="white"
        ).pack()
        
        # Profile completion card
        profile_card = StyledCard(self, padding=20)
        profile_card.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(
            profile_card.content_frame,
            text="Complete Your Profile",
            font=("Segoe UI", 14, "bold"),
            bg="white"
        ).pack(anchor='w', pady=(0, 10))
        
        tk.Label(
            profile_card.content_frame,
            text="Add more information to your profile to get personalized recommendations",
            bg="white",
            fg=Theme.TEXT_MUTED,
            wraplength=500
        ).pack(anchor='w', pady=(0, 15))
        
        # Progress bar
        self.profile_progress = ProgressBar(
            profile_card.content_frame,
            width=400,
            fg_color=Theme.SUCCESS
        )
        self.profile_progress.pack(anchor='w', pady=(0, 15))
        self.profile_progress.set_progress(65)
        
        # Complete profile button
        StyledButton(
            profile_card.content_frame,
            text="Complete Profile",
            variant="primary",
            command=self.go_to_profile
        ).pack(anchor='w')
```

## Event Form Integration

### Creating Event Form with Styled Widgets

```python
# Example: Create Event Form
from components import StyledEntry, StyledButton, StyledCard, Toast, Theme

class CreateEventForm(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, bg="#F8F9FA")
        self.root = root
        
        # Scrollable frame
        canvas = tk.Canvas(self, bg="#F8F9FA", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F8F9FA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form card
        form_card = StyledCard(scrollable_frame, padding=40)
        form_card.pack(padx=40, pady=20, fill='x')
        
        # Header
        tk.Label(
            form_card.content_frame,
            text="Create New Event",
            font=("Segoe UI", 20, "bold"),
            bg="white"
        ).pack(anchor='w', pady=(0, 5))
        
        tk.Label(
            form_card.content_frame,
            text="Fill in the details below to create a campus event",
            font=("Segoe UI", 10),
            fg=Theme.TEXT_MUTED,
            bg="white"
        ).pack(anchor='w', pady=(0, 30))
        
        # Event Name
        self._add_label(form_card.content_frame, "Event Name *")
        self.name_entry = StyledEntry(
            form_card.content_frame,
            placeholder="Enter event name",
            icon_left="📝"
        )
        self.name_entry.pack(fill='x', pady=5)
        
        # Category
        self._add_label(form_card.content_frame, "Category *")
        self.category_entry = StyledEntry(
            form_card.content_frame,
            placeholder="e.g., Workshop, Seminar, Sports",
            icon_left="🏷️"
        )
        self.category_entry.pack(fill='x', pady=5)
        
        # Date and Time Row
        datetime_frame = tk.Frame(form_card.content_frame, bg="white")
        datetime_frame.pack(fill='x', pady=10)
        
        # Date
        date_col = tk.Frame(datetime_frame, bg="white")
        date_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self._add_label(date_col, "Date *")
        self.date_entry = StyledEntry(date_col, placeholder="DD/MM/YYYY", icon_left="📅")
        self.date_entry.pack(fill='x', pady=5)
        
        # Time
        time_col = tk.Frame(datetime_frame, bg="white")
        time_col.pack(side='left', fill='both', expand=True, padx=(10, 0))
        self._add_label(time_col, "Time *")
        self.time_entry = StyledEntry(time_col, placeholder="HH:MM", icon_left="🕐")
        self.time_entry.pack(fill='x', pady=5)
        
        # Venue
        self._add_label(form_card.content_frame, "Venue *")
        self.venue_entry = StyledEntry(
            form_card.content_frame,
            placeholder="Enter venue location",
            icon_left="📍",
            clear_button=True
        )
        self.venue_entry.pack(fill='x', pady=5)
        
        # Max Participants
        self._add_label(form_card.content_frame, "Maximum Participants")
        self.max_entry = StyledEntry(
            form_card.content_frame,
            placeholder="Enter maximum capacity",
            icon_left="👥"
        )
        self.max_entry.pack(fill='x', pady=5)
        
        # Description
        self._add_label(form_card.content_frame, "Description")
        # Note: StyledEntry doesn't support multiline, use Text widget here
        desc_frame = tk.Frame(form_card.content_frame, bg="white", highlightthickness=1, highlightbackground="#E0E0E0")
        desc_frame.pack(fill='x', pady=5)
        self.desc_text = tk.Text(desc_frame, height=5, font=("Segoe UI", 10), bd=0, padx=10, pady=10)
        self.desc_text.pack(fill='both')
        
        # Buttons
        btn_frame = tk.Frame(form_card.content_frame, bg="white")
        btn_frame.pack(pady=(30, 0))
        
        StyledButton(
            btn_frame,
            text="Cancel",
            variant="ghost",
            command=self.cancel,
            width=120
        ).pack(side='left', padx=5)
        
        self.submit_btn = StyledButton(
            btn_frame,
            text="Create Event",
            variant="success",
            command=self.submit,
            width=150
        )
        self.submit_btn.pack(side='left', padx=5)
    
    def _add_label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg="white"
        ).pack(anchor='w', pady=(15, 2))
    
    def submit(self):
        # Clear previous errors
        for entry in [self.name_entry, self.category_entry, self.date_entry, self.time_entry, self.venue_entry]:
            entry.clear_state()
        
        # Validate
        errors = []
        
        if not self.name_entry.get():
            self.name_entry.set_error("Event name is required")
            errors.append("name")
        
        if not self.category_entry.get():
            self.category_entry.set_error("Category is required")
            errors.append("category")
        
        if not self.date_entry.get():
            self.date_entry.set_error("Date is required")
            errors.append("date")
        
        if not self.time_entry.get():
            self.time_entry.set_error("Time is required")
            errors.append("time")
        
        if not self.venue_entry.get():
            self.venue_entry.set_error("Venue is required")
            errors.append("venue")
        
        if errors:
            Toast.show(self.root, f"Please fill in all required fields", type="error")
            return
        
        # Show loading
        self.submit_btn.set_loading(True)
        self.submit_btn.set_text("Creating Event...")
        
        # Simulate API call
        self.after(1500, self._finish_submit)
    
    def _finish_submit(self):
        self.submit_btn.set_loading(False)
        self.submit_btn.set_text("Create Event")
        
        # Show success
        Toast.show(self.root, "Event created successfully!", type="success")
        
        # Clear form
        self.name_entry.clear()
        self.category_entry.clear()
        self.date_entry.clear()
        self.time_entry.clear()
        self.venue_entry.clear()
        self.max_entry.clear()
        self.desc_text.delete("1.0", "end")
    
    def cancel(self):
        # Navigate back or clear form
        pass
```

## Notifications Integration

### Replace Messagebox with Toast Notifications

**Before:**
```python
from tkinter import messagebox

# Success message
messagebox.showinfo("Success", "Event created successfully!")

# Error message
messagebox.showerror("Error", "Failed to create event")

# Warning
messagebox.showwarning("Warning", "This action cannot be undone")

# Confirmation
result = messagebox.askyesno("Confirm", "Are you sure you want to delete?")
```

**After:**
```python
from components import Toast

# Success notification
Toast.show(root, "Event created successfully!", type="success")

# Error notification
Toast.show(root, "Failed to create event", type="error")

# Warning notification
Toast.show(root, "This action cannot be undone", type="warning")

# Info notification
Toast.show(root, "Processing your request...", type="info")

# For confirmations, still use dialog or create custom modal
# (Toast is for non-blocking notifications)
```

## Best Practices

### 1. Consistent Color Usage

```python
from components import Theme

# Always use theme colors for consistency
frame = tk.Frame(parent, bg=Theme.BG_LIGHT)
label = tk.Label(parent, fg=Theme.TEXT_DARK, bg=Theme.BG_WHITE)
error_text = tk.Label(parent, fg=Theme.DANGER)
success_text = tk.Label(parent, fg=Theme.SUCCESS)
```

### 2. Button Variant Selection

```python
# Use appropriate variants
save_btn = StyledButton(parent, text="Save", variant="primary")      # Main action
cancel_btn = StyledButton(parent, text="Cancel", variant="ghost")     # Cancel/back
approve_btn = StyledButton(parent, text="Approve", variant="success") # Positive action
delete_btn = StyledButton(parent, text="Delete", variant="danger")    # Destructive action
options_btn = StyledButton(parent, text="Options", variant="secondary") # Secondary action
```

### 3. Form Validation Pattern

```python
def submit_form(self):
    # 1. Clear previous errors
    for entry in self.all_entries:
        entry.clear_state()
    
    # 2. Validate each field
    errors = []
    
    if not self.email_entry.get():
        self.email_entry.set_error("Email is required")
        errors.append("email")
    elif not self._is_valid_email(self.email_entry.get()):
        self.email_entry.set_error("Invalid email format")
        errors.append("email")
    
    # 3. Show toast for overall error
    if errors:
        Toast.show(self.root, "Please fix the errors", type="error")
        return
    
    # 4. Show loading state
    self.submit_btn.set_loading(True)
    
    # 5. Perform action
    # ... API call ...
    
    # 6. Handle result
    self.submit_btn.set_loading(False)
    Toast.show(self.root, "Success!", type="success")
```

### 4. Card Layout Pattern

```python
# Group related content in cards
info_card = StyledCard(parent, padding=20)
info_card.pack(fill='x', padx=20, pady=10)

# Always add content to card.content_frame
tk.Label(info_card.content_frame, text="Title").pack()
tk.Label(info_card.content_frame, text="Content").pack()
```

### 5. Progress Tracking

```python
# Use progress bars for long operations
progress = ProgressBar(parent, width=400)
progress.pack(pady=10)

def upload_file():
    progress.reset()
    
    def update(current):
        if current <= 100:
            progress.set_progress(current)
            root.after(50, lambda: update(current + 5))
        else:
            Toast.show(root, "Upload complete!", type="success")
    
    update(0)
```

### 6. Entry Icons

```python
# Use appropriate icons for entry fields
email = StyledEntry(parent, placeholder="Email", icon_left="📧")
password = StyledEntry(parent, placeholder="Password", icon_right="👁️", show="•")
search = StyledEntry(parent, placeholder="Search", icon_left="🔍")
date = StyledEntry(parent, placeholder="Date", icon_left="📅")
location = StyledEntry(parent, placeholder="Location", icon_left="📍")
phone = StyledEntry(parent, placeholder="Phone", icon_left="📞")
user = StyledEntry(parent, placeholder="Username", icon_left="👤")
```

### 7. Toast Timing

```python
# Quick feedback - 3 seconds (default)
Toast.show(root, "Saved!", type="success")

# Important messages - 5 seconds
Toast.show(root, "Server connection lost", type="error", duration=5000)

# Critical warnings - 7 seconds
Toast.show(root, "Session expiring soon", type="warning", duration=7000)
```

## Migration Checklist

When updating existing pages:

- [ ] Replace standard buttons with StyledButton
- [ ] Replace entry fields with StyledEntry
- [ ] Wrap content sections in StyledCard
- [ ] Replace messagebox with Toast notifications
- [ ] Add loading states to async operations
- [ ] Use Theme colors for consistency
- [ ] Add progress bars where applicable
- [ ] Implement proper validation with error states
- [ ] Test all interactive states (hover, loading, disabled)
- [ ] Ensure responsive layout with cards

## Examples

For complete working examples, see:
- `components/custom_widgets_examples.py` - Interactive demo of all widgets
- `components/STYLED_WIDGETS_INTEGRATION.md` - This file

For questions or issues, refer to the main README.md documentation.
