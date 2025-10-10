# Dashboard Button Fix Guide

## Problem
All buttons in the dashboard (and other pages) appear as whitish-grey boxes with invisible text on macOS due to Tkinter's inability to set custom `bg` colors on macOS buttons.

## Solution
Use the new `canvas_button.py` utility to create canvas-based buttons that properly display colors on all platforms, including macOS.

## How to Fix Buttons

### Step 1: Import the Utility

At the top of any page file, add:

```python
from utils.canvas_button import (
    create_canvas_button,
    create_primary_button,
    create_secondary_button,
    create_success_button,
    create_danger_button,
    create_icon_button,
    CanvasButton
)
```

### Step 2: Replace Regular Buttons

**OLD CODE (Regular Button):**
```python
save_btn = tk.Button(
    parent,
    text="Save",
    command=self.save,
    bg='#3047ff',
    fg='white',
    font=("Helvetica", 11, "bold"),
    cursor='hand2'
)
save_btn.pack(padx=10, pady=10)
```

**NEW CODE (Canvas Button):**
```python
save_btn = create_primary_button(
    parent,
    text="Save",
    command=self.save,
    width=120,
    height=40
)
save_btn.pack(padx=10, pady=10)
```

### Step 3: Use Button Variants

Different button types for different actions:

```python
# Primary action buttons (blue)
submit_btn = create_primary_button(parent, "Submit", command=self.submit)

# Secondary actions (gray)
cancel_btn = create_secondary_button(parent, "Cancel", command=self.cancel)

# Success/positive actions (green)
approve_btn = create_success_button(parent, "Approve", command=self.approve)

# Dangerous/destructive actions (red)
delete_btn = create_danger_button(parent, "Delete", command=self.delete)

# Icon buttons (emoji/symbols)
notif_btn = create_icon_button(parent, "🔔", command=self.show_notifications, size=40)
```

### Step 4: Handle Button States

**Disable/Enable:**
```python
button.set_enabled(False)  # Disable
button.set_enabled(True)   # Enable
```

**Update Text:**
```python
button.set_text("New Text")
```

**Loading State:**
```python
button.set_loading(True, "Saving...")   # Show loading
button.set_loading(False)                # Hide loading
```

**Configuration:**
```python
button.config(text="Updated", bg='#ff0000', fg='white')
button.config(state='disabled')  # or state=tk.DISABLED
button.config(state='normal')    # or state=tk.NORMAL
```

## Common Patterns

### Search Button
```python
search_btn = create_primary_button(
    search_frame,
    "Search",
    command=self.on_search,
    width=100,
    height=35
)
search_btn.pack(side='left', padx=5)
```

### Filter Buttons
```python
all_btn = create_secondary_button(filter_frame, "All", command=lambda: self.filter('all'), width=80, height=30)
active_btn = create_secondary_button(filter_frame, "Active", command=lambda: self.filter('active'), width=80, height=30)
```

### Action Buttons in Cards
```python
# View button
view_btn = create_canvas_button(
    card,
    "View Details",
    command=lambda: self.view_details(item_id),
    variant='info',
    width=120,
    height=35
)
view_btn.pack(pady=5)

# Edit button
edit_btn = create_canvas_button(
    card,
    "Edit",
    command=lambda: self.edit(item_id),
    variant='warning',
    width=80,
    height=35
)
edit_btn.pack(pady=5)
```

### Icon Toolbar Buttons
```python
toolbar = tk.Frame(header, bg='white')
toolbar.pack(side='right')

# Notifications
notif_btn = create_icon_button(toolbar, "🔔", command=self.notifications, size=36)
notif_btn.pack(side='right', padx=5)

# Settings
settings_btn = create_icon_button(toolbar, "⚙️", command=self.settings, size=36)
settings_btn.pack(side='right', padx=5)

# Profile
profile_btn = create_icon_button(toolbar, "👤", command=self.profile, size=36)
profile_btn.pack(side='right', padx=5)
```

### Form Submit/Cancel
```python
button_frame = tk.Frame(form, bg='white')
button_frame.pack(pady=20)

cancel_btn = create_secondary_button(
    button_frame,
    "Cancel",
    command=self.cancel,
    width=100,
    height=40
)
cancel_btn.pack(side='left', padx=10)

submit_btn = create_primary_button(
    button_frame,
    "Submit",
    command=self.submit,
    width=100,
    height=40
)
submit_btn.pack(side='left', padx=10)
```

### Async Operations
```python
def on_save(self):
    # Disable button and show loading
    self.save_btn.set_loading(True, "Saving...")
    
    # Perform async operation
    thread = threading.Thread(target=self.save_thread, daemon=True)
    thread.start()

def save_thread(self):
    try:
        # Save data
        result = self.api.post("endpoint", data)
        
        # Re-enable button
        self.after(0, lambda: self.save_btn.set_loading(False))
        self.after(0, lambda: messagebox.showinfo("Success", "Saved!"))
    except Exception as e:
        self.after(0, lambda: self.save_btn.set_loading(False))
        self.after(0, lambda: messagebox.showerror("Error", str(e)))
```

## ButtonStyles Compatibility

For pages using the old `ButtonStyles` class, you can keep both:

```python
from utils.button_styles import ButtonStyles
from utils.canvas_button import create_canvas_button

# Old style (won't work properly on macOS)
old_btn = ButtonStyles.create_styled_button(parent, "Old", style='primary')

# New style (works on all platforms)
new_btn = create_canvas_button(parent, "New", variant='primary')
```

## Migration Checklist

For each page file:

- [ ] Import canvas_button utilities at the top
- [ ] Find all `tk.Button` creations
- [ ] Replace with appropriate `create_*_button()` function
- [ ] Test all button clicks work
- [ ] Test button states (disabled, loading, etc.)
- [ ] Verify colors display correctly
- [ ] Check hover effects work
- [ ] Test on macOS if possible

## Color Variants

| Variant | Color | Use Case | Example |
|---------|-------|----------|---------|
| `primary` | Blue (#3047ff) | Main actions | Submit, Save, Login |
| `secondary` | Gray (#6c757d) | Secondary actions | Cancel, Back, Close |
| `success` | Green (#28a745) | Positive actions | Approve, Confirm, Accept |
| `danger` | Red (#dc3545) | Destructive actions | Delete, Remove, Reject |
| `warning` | Yellow (#ffc107) | Warning actions | Edit, Modify, Reset |
| `info` | Cyan (#17a2b8) | Info actions | View, Details, Info |
| `light` | Light Gray (#f8f9fa) | Light buttons | - |
| `dark` | Dark Gray (#343a40) | Dark buttons | - |

## Custom Colors

If you need custom colors:

```python
custom_btn = create_canvas_button(
    parent,
    "Custom",
    command=self.action,
    variant='primary',  # Base variant
    bg_color='#ff6b6b',      # Override background
    hover_color='#ee5555',   # Override hover
    fg_color='white'         # Override text color
)
```

## Advanced: Using CanvasButton Class Directly

For more control:

```python
btn = CanvasButton(
    parent,
    text="Advanced",
    command=self.action,
    width=150,
    height=50,
    bg_color='#custom',
    fg_color='white',
    hover_color='#hover',
    disabled_color='#disabled',
    font=("Custom Font", 12, "bold")
)
btn.pack(padx=10, pady=10)

# Later...
btn.set_enabled(False)
btn.set_text("Disabled")
```

## Files to Fix

Priority order:

1. ✅ **login_page.py** - DONE (LOGIN button fixed)
2. ✅ **main.py** - DONE (Navigation bar buttons fixed)
3. ⚠️ **student_dashboard.py** - IN PROGRESS
4. ⚠️ **organizer_dashboard.py** - Needs fixing
5. ⚠️ **admin_dashboard.py** - Needs fixing
6. ⚠️ **browse_events.py** - Needs fixing
7. ⚠️ **browse_resources.py** - Needs fixing
8. ⚠️ **create_event.py** - Needs fixing
9. ⚠️ **book_resource.py** - Needs fixing
10. ⚠️ **profile_page.py** - Needs fixing
11. Other pages with buttons

## Quick Fix Script

You can search for all buttons to fix:

```bash
# Find all tk.Button usages
grep -r "tk.Button" frontend_tkinter/pages/

# Find all ButtonStyles usages
grep -r "ButtonStyles" frontend_tkinter/pages/
```

## Testing

After fixing buttons:

1. Run the app: `./run.sh`
2. Navigate to the page
3. Check all buttons display with correct colors
4. Click each button to verify functionality
5. Test hover effects
6. Test disabled states if applicable

## Documentation

- **Full Documentation**: [MACOS_BUTTON_FIX.md](../MACOS_BUTTON_FIX.md)
- **Canvas Button Source**: `utils/canvas_button.py`
- **Button Styles (Legacy)**: `utils/button_styles.py`

---

**Last Updated**: October 10, 2025  
**Status**: Login and Navigation fixed, Dashboard pages in progress
