# Custom Styled Widgets - Quick Reference

## Overview

Custom styled widgets library for Campus Event System with consistent theming, animations, and modern UI patterns.

**Version:** 1.4.0  
**Package:** `components.custom_widgets`  
**Total Widgets:** 5 main components + Theme + utilities

---

## Quick Import

```python
from components import (
    StyledButton,
    StyledEntry,
    StyledCard,
    ProgressBar,
    Toast,
    Theme,
    show_loading_dialog
)
```

---

## 1. StyledButton

### Quick Example
```python
button = StyledButton(parent, text="Save", variant="primary", command=handler)
button.pack(pady=10)
button.set_loading(True)  # Show spinner
```

### Variants
| Variant | Color | Use Case |
|---------|-------|----------|
| `primary` | Blue | Main actions |
| `secondary` | Gray | Secondary actions |
| `success` | Green | Positive actions |
| `danger` | Red | Destructive actions |
| `ghost` | Transparent | Subtle actions |

### Methods
```python
button.set_loading(True/False)    # Loading state
button.set_disabled(True/False)   # Disabled state
button.set_text("New Text")       # Update text
```

---

## 2. StyledEntry

### Quick Example
```python
entry = StyledEntry(parent, placeholder="Email", icon_left="📧", clear_button=True)
entry.pack(fill='x', pady=5)

email = entry.get()                # Get value
entry.set_error("Invalid email")   # Show error
entry.set_success()                # Show success
```

### Icons
```python
icon_left="📧"   # Email
icon_left="🔍"   # Search
icon_left="📅"   # Date
icon_left="📍"   # Location
icon_left="👤"   # User
icon_right="👁️"  # Password toggle
```

### Methods
```python
entry.get()                  # Get value
entry.set("value")           # Set value
entry.clear()                # Clear + show placeholder
entry.set_error("message")   # Error state
entry.set_success()          # Success state
entry.clear_state()          # Remove state
entry.focus()                # Set focus
```

---

## 3. StyledCard

### Quick Example
```python
card = StyledCard(parent, padding=20, hover=True)
card.pack(pady=10, fill='x')

# Add content to card.content_frame
tk.Label(card.content_frame, text="Title").pack()
```

### Features
- Elevated shadow effect
- Hover state (darker shadow)
- Optional click handler
- Customizable padding

### Important
⚠️ Always add children to `card.content_frame`, not `card` directly!

---

## 4. ProgressBar

### Quick Example
```python
progress = ProgressBar(parent, width=400, fg_color=Theme.SUCCESS)
progress.pack(pady=10)

progress.set_progress(75)      # Animates to 75%
progress.set_color("#27AE60")  # Change color
progress.reset()               # Reset to 0%
```

### Animation Example
```python
def animate_upload():
    progress.reset()
    
    def update(val):
        if val <= 100:
            progress.set_progress(val)
            root.after(50, lambda: update(val + 5))
        else:
            Toast.show(root, "Complete!", "success")
    
    update(0)
```

---

## 5. Toast Notifications

### Quick Example
```python
Toast.show(root, "Success!", type="success")
Toast.show(root, "Error occurred", type="error", duration=5000)
```

### Types

| Type | Color | Icon | Use Case |
|------|-------|------|----------|
| `success` | Green | ✓ | Successful operations |
| `error` | Red | ✕ | Errors and failures |
| `info` | Blue | ℹ | Information messages |
| `warning` | Orange | ⚠ | Warnings and alerts |

### Features
- Auto-dismiss (default: 3 seconds)
- Slide-in animation
- Stack multiple toasts
- Click to dismiss
- Always on top

---

## Theme Colors

```python
from components import Theme

# Primary
Theme.PRIMARY           # #3498DB
Theme.PRIMARY_HOVER     # #2980B9

# Success
Theme.SUCCESS           # #27AE60

# Danger
Theme.DANGER            # #E74C3C

# Text
Theme.TEXT_DARK         # #2C3E50
Theme.TEXT_MUTED        # #7F8C8D

# Background
Theme.BG_LIGHT          # #F8F9FA
Theme.BG_WHITE          # #FFFFFF

# Border
Theme.BORDER_LIGHT      # #E0E0E0
Theme.BORDER_ERROR      # #E74C3C
Theme.BORDER_SUCCESS    # #27AE60
```

[See all colors in README.md]

---

## Common Patterns

### Login Form
```python
# Email
email = StyledEntry(parent, placeholder="Email", icon_left="📧")
email.pack(fill='x', pady=5)

# Password
password = StyledEntry(parent, placeholder="Password", icon_right="👁️", show="•")
password.pack(fill='x', pady=5)

# Login button
login_btn = StyledButton(parent, text="Sign In", variant="primary", command=login)
login_btn.pack(pady=10)

def login():
    if not email.get():
        email.set_error("Email required")
        Toast.show(root, "Fill in all fields", "error")
        return
    
    login_btn.set_loading(True)
    # ... API call ...
    login_btn.set_loading(False)
    Toast.show(root, "Login successful!", "success")
```

### Form Validation
```python
def submit():
    # Clear errors
    for entry in [name_entry, email_entry, phone_entry]:
        entry.clear_state()
    
    # Validate
    errors = []
    if not name_entry.get():
        name_entry.set_error("Required")
        errors.append("name")
    
    if errors:
        Toast.show(root, "Fix errors", "error")
        return
    
    # Success
    for entry in [name_entry, email_entry]:
        entry.set_success()
    
    Toast.show(root, "Saved!", "success")
```

### Dashboard Cards
```python
# Stats card
card = StyledCard(parent, padding=20, hover=True)
card.pack(padx=20, pady=10, fill='x')

tk.Label(card.content_frame, text="24", font=("Segoe UI", 28, "bold")).pack()
tk.Label(card.content_frame, text="Total Events").pack()
```

### Upload Progress
```python
progress = ProgressBar(parent, width=400)
progress.pack(pady=10)

upload_btn = StyledButton(parent, text="Upload", variant="primary", command=upload)
upload_btn.pack()

def upload():
    upload_btn.set_disabled(True)
    progress.reset()
    
    def update(val):
        if val <= 100:
            progress.set_progress(val)
            root.after(50, lambda: update(val + 5))
        else:
            upload_btn.set_disabled(False)
            Toast.show(root, "Upload complete!", "success")
    
    update(0)
```

---

## Best Practices

### ✅ Do's

```python
# Use theme colors
frame = tk.Frame(parent, bg=Theme.BG_LIGHT)

# Clear errors before validation
entry.clear_state()

# Show loading during async operations
button.set_loading(True)

# Use appropriate button variants
save_btn = StyledButton(parent, text="Save", variant="primary")
cancel_btn = StyledButton(parent, text="Cancel", variant="ghost")

# Add content to card.content_frame
tk.Label(card.content_frame, text="Title").pack()

# Use toast for feedback
Toast.show(root, "Saved!", "success")
```

### ❌ Don'ts

```python
# Don't use hardcoded colors
frame = tk.Frame(parent, bg="#3498DB")  # ❌ Use Theme.PRIMARY

# Don't forget to stop loading
button.set_loading(True)
# ... operation ...
# ❌ FORGOT: button.set_loading(False)

# Don't add to card directly
tk.Label(card, text="Title").pack()  # ❌ Use card.content_frame

# Don't use messagebox for simple feedback
messagebox.showinfo("Success", "Saved")  # ❌ Use Toast
```

---

## File Locations

```
components/
├── custom_widgets.py                   # Main widgets library
├── custom_widgets_examples.py          # Interactive demo
├── STYLED_WIDGETS_INTEGRATION.md       # Integration guide
└── STYLED_WIDGETS_QUICK_REF.md         # This file
```

---

## Resources

- **Full Documentation:** `README.md`
- **Interactive Demo:** Run `python3 components/custom_widgets_examples.py`
- **Integration Examples:** `components/STYLED_WIDGETS_INTEGRATION.md`
- **Changelog:** `CHANGELOG.md` (v1.4.0)

---

## Quick Start Checklist

- [ ] Import widgets: `from components import StyledButton, StyledEntry, ...`
- [ ] Replace standard buttons with `StyledButton`
- [ ] Replace entries with `StyledEntry` (with icons and validation)
- [ ] Wrap content in `StyledCard` for better visual hierarchy
- [ ] Replace `messagebox` with `Toast.show()`
- [ ] Use `Theme` colors for consistency
- [ ] Add loading states to async buttons
- [ ] Add progress bars for long operations
- [ ] Test all states (hover, loading, disabled, error, success)

---

**Version:** 1.4.0  
**Last Updated:** October 9, 2025  
**Author:** Campus Event System Team
