# macOS Tkinter Button Color Issue - Fix Documentation

## Problem Description

### The Issue
On **macOS**, Tkinter buttons ignore the `bg` (background) parameter and use the system's default appearance instead. This causes buttons to appear in a **whitish-grey color** regardless of the specified background color, making white text invisible or very hard to read.

### Symptoms
- Buttons appear whitish-grey instead of the specified color (e.g., blue #3047ff)
- Button text is white/light colored and becomes invisible against the light grey background
- The issue only occurs on macOS, not on Windows or Linux
- Setting `bg='#3047ff'` or any other color has no effect
- Even with `relief=tk.FLAT`, `bd=0`, and `highlightthickness=0`, the grey appearance persists

### Example of Problematic Code
```python
# This DOES NOT WORK on macOS - button will appear grey!
login_btn = tk.Button(
    parent,
    text='LOGIN',
    bg='#3047ff',      # ❌ Ignored on macOS
    fg='white',         # ❌ Hard to see on grey background
    relief=tk.FLAT,
    bd=0,
    cursor='hand2'
)
```

---

## The Solution: Canvas-Based Buttons

The solution is to **replace Tkinter Button widgets with Canvas-based custom buttons**. Canvas widgets properly respect color settings on all platforms, including macOS.

### How It Works
1. Create a `tk.Canvas` widget instead of `tk.Button`
2. Draw a rectangle on the canvas with the desired background color
3. Add text on top of the rectangle
4. Bind mouse events to the canvas for click and hover functionality
5. Track button state (enabled/disabled) manually

---

## Implementation Guide

### Basic Canvas Button Template

```python
# Create canvas for button
button_canvas = tk.Canvas(
    parent,
    width=300,           # Button width
    height=50,           # Button height
    bg='#040405',        # Match parent background
    highlightthickness=0 # Remove border
)
button_canvas.place(x=550, y=460)

# Draw button rectangle
button_rect = button_canvas.create_rectangle(
    0, 0, 300, 50,
    fill='#3047ff',      # ✅ Button background color
    outline='',          # No outline
    tags='button'        # Tag for event binding
)

# Add button text
button_text = button_canvas.create_text(
    150, 25,             # Center position (width/2, height/2)
    text='LOGIN',
    font=("yu gothic ui", 13, "bold"),
    fill='white',        # ✅ Text color (visible!)
    tags='button'
)

# Bind click event
button_canvas.tag_bind('button', '<Button-1>', lambda e: on_click())

# Bind hover events
button_canvas.tag_bind('button', '<Enter>', hover_enter_handler)
button_canvas.tag_bind('button', '<Leave>', hover_leave_handler)

# Set cursor
button_canvas.config(cursor='hand2')
```

### Hover Effect Handlers

```python
def hover_enter(event):
    """Handle mouse hover over button."""
    if button_enabled:  # Only if button is active
        button_canvas.itemconfig(button_rect, fill='#1e3acc')  # Darker shade

def hover_leave(event):
    """Handle mouse leaving button."""
    if button_enabled:
        button_canvas.itemconfig(button_rect, fill='#3047ff')  # Original color
    else:
        button_canvas.itemconfig(button_rect, fill='#475569')  # Disabled color
```

### Button State Management

```python
# Track button state
button_enabled = True  # Initialize as enabled

# To disable button
button_enabled = False
button_canvas.itemconfig(button_rect, fill='#475569')  # Grey out
button_canvas.itemconfig(button_text, fill='#94A3B8')  # Grey text
button_canvas.config(cursor='arrow')  # Normal cursor

# To enable button
button_enabled = True
button_canvas.itemconfig(button_rect, fill='#3047ff')  # Blue
button_canvas.itemconfig(button_text, fill='#FFFFFF')  # White text
button_canvas.config(cursor='hand2')  # Hand cursor
```

### Loading State Example

```python
def on_login():
    """Handle login with loading state."""
    # Disable and show loading
    button_enabled = False
    button_canvas.itemconfig(button_rect, fill='#475569')
    button_canvas.itemconfig(button_text, text='SIGNING IN...')
    button_canvas.config(cursor='wait')
    
    # Start background task
    thread = threading.Thread(target=login_thread, daemon=True)
    thread.start()

def login_success():
    """Re-enable button after success."""
    button_enabled = True
    button_canvas.itemconfig(button_rect, fill='#3047ff')
    button_canvas.itemconfig(button_text, text='LOGIN')
    button_canvas.config(cursor='hand2')
```

---

## Fixed Components in This Project

### 1. Login Page (`pages/login_page.py`)

**LOGIN Button**
- Location: Line ~220
- Canvas size: 300×50
- Colors: Blue (#3047ff) normal, Grey (#475569) loading
- Features: Hover effect, loading state, click binding

**Code:**
```python
self.login_canvas = tk.Canvas(
    self.lgn_frame,
    width=300,
    height=50,
    bg='#040405',
    highlightthickness=0
)
self.login_canvas.place(x=550, y=460)

self.login_enabled = True
self.login_rect = self.login_canvas.create_rectangle(
    0, 0, 300, 50,
    fill='#3047ff',
    outline='',
    tags='button'
)

self.login_text = self.login_canvas.create_text(
    150, 25,
    text='LOGIN',
    font=("yu gothic ui", 13, "bold"),
    fill='white',
    tags='button'
)
```

### 2. Navigation Bar (`main.py`)

**All four navigation buttons fixed:**

#### Back Button (← Back)
- Canvas size: 90×34
- Colors: Blue (#3B82F6) enabled, Grey (#64748B) disabled
- Location: `_create_navigation_bar()` method, Line ~500

#### Forward Button (Forward →)
- Canvas size: 110×34
- Colors: Blue (#3B82F6) enabled, Grey (#64748B) disabled
- Location: `_create_navigation_bar()` method, Line ~508

#### Profile Button (👤 Profile)
- Canvas size: 110×34
- Colors: Dark grey (#2D3748), hover (#374151)
- Location: `_create_navigation_bar()` method, Line ~550

#### Notifications Button (🔔 Notifications)
- Canvas size: 140×34
- Colors: Dark grey (#2D3748), hover (#374151)
- Location: `_create_navigation_bar()` method, Line ~542

**State Update Method:**
```python
def _update_nav_buttons(self):
    """Update back/forward button states with proper styling."""
    if self.nav_history.can_go_back():
        self.back_enabled = True
        self.back_canvas.itemconfig(self.back_rect, fill='#3B82F6')
        self.back_canvas.itemconfig(self.back_text, fill='#FFFFFF')
        self.back_canvas.config(cursor='hand2')
    else:
        self.back_enabled = False
        self.back_canvas.itemconfig(self.back_rect, fill='#64748B')
        self.back_canvas.itemconfig(self.back_text, fill='#94A3B8')
        self.back_canvas.config(cursor='arrow')
    # ... similar for forward button
```

---

## Color Scheme Reference

### Login Page Colors
- **Primary Blue**: `#3047ff` (button normal)
- **Hover Blue**: `#1e3acc` (button hover)
- **Loading Grey**: `#475569` (disabled/loading)
- **Background Dark**: `#040405` (page background)
- **Text White**: `#FFFFFF` (button text)

### Navigation Bar Colors
- **Primary Blue**: `#3B82F6` (back/forward enabled)
- **Hover Blue**: `#2563EB` (back/forward hover)
- **Disabled Grey**: `#64748B` (back/forward disabled)
- **Disabled Text**: `#94A3B8` (disabled text color)
- **Nav Bar Background**: `#1E293B` (dark slate)
- **Button Dark**: `#2D3748` (profile/notifications normal)
- **Button Hover**: `#374151` (profile/notifications hover)
- **Text Light**: `#F1F5F9` (profile/notifications text)

---

## Key Points to Remember

### ✅ DO's
- ✅ Use `tk.Canvas` for buttons with custom colors on macOS
- ✅ Set canvas `highlightthickness=0` to remove border
- ✅ Match canvas `bg` to parent background for seamless integration
- ✅ Use `create_rectangle()` for button background
- ✅ Use `create_text()` for button label
- ✅ Tag both rectangle and text with same tag for unified event binding
- ✅ Track button enabled/disabled state manually
- ✅ Update colors with `itemconfig()` for state changes
- ✅ Test hover effects and loading states

### ❌ DON'Ts
- ❌ Don't use regular `tk.Button` with `bg` parameter on macOS
- ❌ Don't expect `activebackground` to work on macOS buttons
- ❌ Don't use `button.config(state='disabled')` - manually track state
- ❌ Don't forget to update cursor style for disabled state
- ❌ Don't use white text on light backgrounds (visibility!)
- ❌ Don't bind events to canvas instead of tags (use tags!)

---

## Testing Checklist

When implementing canvas-based buttons, test:

- [ ] Button displays with correct background color
- [ ] Text is clearly visible (good contrast)
- [ ] Click events trigger the correct action
- [ ] Hover effect changes color smoothly
- [ ] Disabled state shows greyed out appearance
- [ ] Disabled button doesn't respond to clicks
- [ ] Cursor changes between hand and arrow appropriately
- [ ] Loading state displays correctly
- [ ] State transitions work without flickering
- [ ] Button scales properly with different dimensions

---

## Troubleshooting

### Issue: Button still appears white/grey
**Solution:** Check that you're using `tk.Canvas`, not `tk.Button`

### Issue: Click events not working
**Solution:** Ensure you're binding to tags: `canvas.tag_bind('button', '<Button-1>', handler)`

### Issue: White border around button
**Solution:** Set `highlightthickness=0` on the canvas

### Issue: Hover not working
**Solution:** Check that `button_enabled` flag is set and hover handlers are bound

### Issue: Text not centered
**Solution:** Use `width/2` and `height/2` for text coordinates

### Issue: Button looks disconnected from background
**Solution:** Match canvas `bg` to parent frame's background color

---

## Platform Compatibility

| Platform | Regular tk.Button | Canvas Button |
|----------|-------------------|---------------|
| **macOS** | ❌ Colors ignored | ✅ Works perfectly |
| **Windows** | ✅ Works fine | ✅ Works perfectly |
| **Linux** | ✅ Works fine | ✅ Works perfectly |

**Recommendation:** Use canvas-based buttons for all platforms to ensure consistent appearance and behavior.

---

## Additional Resources

### Official Documentation
- [Tkinter Canvas Documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Canvas)
- [Canvas Item Configuration](https://docs.python.org/3/library/tkinter.html#canvas-objects)

### Related Issues
- This is a known limitation of Tkinter on macOS
- The issue exists since macOS Catalina (10.15) and continues in newer versions
- Apple's native button rendering overrides Tkinter's color settings

### Alternative Solutions (Not Recommended)
1. **ttk.Button with custom styles** - Complex to set up, still has limitations
2. **Custom Frame-based buttons** - Less efficient than canvas approach
3. **Third-party libraries (ttkbootstrap)** - Adds dependencies

---

## Version History

| Date | Change | Files Modified |
|------|--------|----------------|
| 2025-10-10 | Fixed Login button | `pages/login_page.py` |
| 2025-10-10 | Fixed Navigation bar buttons (Back, Forward, Profile, Notifications) | `main.py` |

---

## Future Considerations

If you need to add new buttons to the application:

1. **Copy the canvas button template** from this document
2. **Adjust dimensions** based on text length
3. **Match colors** to the design scheme
4. **Implement hover effects** for better UX
5. **Test on macOS** before committing
6. **Update this document** with new button locations

---

## Questions?

If you encounter the button color issue again:
1. Check if it's a `tk.Button` widget
2. Convert to canvas-based button using the template above
3. Test all states (normal, hover, disabled, loading)
4. Update this document with the new fix location

**Last Updated:** October 10, 2025
**Issue Status:** ✅ RESOLVED
