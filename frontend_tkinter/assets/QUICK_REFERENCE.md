# Assets & Icons - Quick Reference

## Import

```python
from utils.image_loader import (
    ImageLoader,
    IconSet,
    get_image_loader,
    load_image,
    load_icon,
    load_logo
)
```

## Quick Usage

### Load Logo
```python
# Using convenience function
logo = load_logo(size=(200, 100))

# Or using ImageLoader
loader = get_image_loader()
logo = loader.load_logo(size=(200, 100))

# Display
label = tk.Label(parent, image=logo)
label.image = logo  # IMPORTANT: Keep reference!
label.pack()
```

### Load Icon
```python
# Convenience function
icon = load_icon("dashboard", size=(24, 24))

# Display in button
button = tk.Button(
    parent,
    image=icon,
    text=" Dashboard",
    compound="left"
)
button.image = icon
button.pack()
```

### Load Event Image
```python
loader = get_image_loader()

# With fallback to placeholder
event_img = loader.load_event_image(
    event.get('image_filename'),  # Can be None
    size=(300, 200)
)

img_label = tk.Label(card, image=event_img)
img_label.image = event_img
img_label.pack()
```

### Load Resource Image
```python
resource_img = loader.load_resource_image(
    resource.get('image_filename'),
    size=(300, 200)
)
```

### Load User Avatar
```python
avatar = loader.load_user_avatar(
    user.get('avatar_filename'),
    size=(64, 64)
)
```

### Unicode Icons (IconSet)
```python
# Direct usage
label = tk.Label(parent, text=f"{IconSet.DASHBOARD} Dashboard")

# Dynamic selection
category_icon = IconSet.get_category_icon("academic")  # Returns 📚
status_icon = IconSet.get_status_icon("approved")      # Returns ✅
```

## Available Icons

### PNG Icons (48x48)
All located in `assets/icons/`:

**Navigation:**
- dashboard.png, events.png, resources.png, bookings.png
- profile.png, settings.png, notifications.png, logout.png

**Actions:**
- search.png, add.png, edit.png, delete.png
- approve.png, reject.png

### Unicode Icons (IconSet)

**Navigation:**
```python
IconSet.DASHBOARD      # 🏠
IconSet.EVENTS         # 📅
IconSet.RESOURCES      # 🏢
IconSet.BOOKINGS       # 📋
IconSet.PROFILE        # 👤
IconSet.SETTINGS       # ⚙️
IconSet.NOTIFICATIONS  # 🔔
IconSet.LOGOUT         # 🚪
```

**Actions:**
```python
IconSet.SEARCH    # 🔍
IconSet.ADD       # ➕
IconSet.EDIT      # ✏️
IconSet.DELETE    # 🗑️
IconSet.SAVE      # 💾
IconSet.CANCEL    # ❌
IconSet.APPROVE   # ✅
IconSet.REJECT    # ❌
IconSet.REFRESH   # 🔄
```

**Status:**
```python
IconSet.SUCCESS   # ✓
IconSet.ERROR     # ✕
IconSet.WARNING   # ⚠
IconSet.INFO      # ℹ
IconSet.PENDING   # ⏳
IconSet.ACTIVE    # 🟢
IconSet.INACTIVE  # 🔴
```

**Content:**
```python
IconSet.EMAIL      # 📧
IconSet.PHONE      # 📞
IconSet.LOCATION   # 📍
IconSet.CALENDAR   # 📅
IconSet.CLOCK      # 🕐
IconSet.USER       # 👤
IconSet.USERS      # 👥
IconSet.BUILDING   # 🏢
```

**Categories:**
```python
IconSet.ACADEMIC     # 📚
IconSet.SPORTS       # ⚽
IconSet.CULTURAL     # 🎭
IconSet.WORKSHOP     # 🔧
IconSet.SEMINAR      # 💼
IconSet.CONFERENCE   # 🎤
IconSet.SOCIAL       # 🎉
```

## Cache Management

```python
loader = get_image_loader()

# Get cache size
size = loader.get_cache_size()

# Clear entire cache
loader.clear_cache()

# Remove specific image
loader.remove_from_cache("logo.png", size=(200, 100))

# Preload icons
loader.preload_icons(
    ['dashboard', 'events', 'resources'],
    size=(24, 24)
)
```

## Common Patterns

### Navigation Button with Icon
```python
icon = load_icon("dashboard", size=(20, 20))

button = tk.Button(
    sidebar,
    image=icon,
    text=" Dashboard",
    compound="left",
    anchor="w",
    command=show_dashboard
)
button.image = icon
button.pack(fill='x', pady=2)
```

### Event Card with Image
```python
# Card container
card = StyledCard(parent, padding=15)
card.pack(pady=10, fill='x')

# Event image
event_img = loader.load_event_image(
    event.get('image'),
    size=(280, 187)
)

img_label = tk.Label(card.content_frame, image=event_img)
img_label.image = event_img
img_label.pack()

# Event title
title_label = tk.Label(
    card.content_frame,
    text=event['title'],
    font=("Segoe UI", 12, "bold")
)
title_label.pack(anchor='w', pady=(10, 5))
```

### User Profile with Avatar
```python
# Profile frame
profile_frame = tk.Frame(parent)
profile_frame.pack(pady=10)

# Avatar
avatar = loader.load_user_avatar(
    user.get('avatar'),
    size=(80, 80)
)

avatar_label = tk.Label(profile_frame, image=avatar)
avatar_label.image = avatar
avatar_label.pack(side='left', padx=10)

# User info
info_frame = tk.Frame(profile_frame)
info_frame.pack(side='left', fill='both', expand=True)

tk.Label(
    info_frame,
    text=user['name'],
    font=("Segoe UI", 14, "bold")
).pack(anchor='w')

tk.Label(
    info_frame,
    text=f"{IconSet.EMAIL} {user['email']}"
).pack(anchor='w')
```

### Status Indicator with Icon
```python
status = event['status']  # 'approved', 'pending', 'rejected'
icon = IconSet.get_status_icon(status)

status_label = tk.Label(
    parent,
    text=f"{icon} {status.capitalize()}"
)
```

### Category Badge with Icon
```python
category = event['category']  # 'academic', 'sports', etc.
icon = IconSet.get_category_icon(category)

category_label = tk.Label(
    parent,
    text=f"{icon} {category.capitalize()}",
    bg="#E0E0E0",
    padx=10,
    pady=5
)
```

## Best Practices

### ✅ Do

```python
# Keep image reference
label = tk.Label(parent, image=icon)
label.image = icon  # Prevents garbage collection

# Load at display size
icon = load_icon("dashboard", size=(24, 24))

# Preload frequently used icons
loader.preload_icons(['dashboard', 'events', 'resources'], size=(24, 24))

# Use placeholders
image = loader.load_event_image(None, size=(300, 200))  # Shows placeholder

# Clear cache after bulk operations
loader.clear_cache()
```

### ❌ Don't

```python
# Don't forget reference
label = tk.Label(parent, image=load_icon("dashboard"))  # ❌ Lost reference

# Don't load at wrong size
icon = load_icon("dashboard")  # Loads full 48x48
# Then scale in tkinter - inefficient

# Don't load same image multiple times
for item in items:
    icon = load_icon("dashboard", size=(24, 24))  # ❌ Load once outside loop
```

## File Locations

```
frontend_tkinter/
├── assets/
│   ├── icons/                 # 14 PNG icons (48x48)
│   │   ├── dashboard.png
│   │   ├── events.png
│   │   └── ...
│   ├── images/                # Logos and placeholders
│   │   ├── logo.png
│   │   ├── event_placeholder.png
│   │   ├── resource_placeholder.png
│   │   └── avatar_placeholder.png
│   └── README.md              # Assets documentation
│
└── utils/
    ├── image_loader.py        # ImageLoader & IconSet
    ├── generate_assets.py     # Asset generator script
    └── image_loader_examples.py  # Demo application
```

## Generate Assets

```bash
cd utils
python3 generate_assets.py
```

Creates:
- Logo (400x200)
- 14 icon files (48x48)
- 3 placeholder images (event, resource, avatar)

## Run Demo

```bash
cd utils
python3 image_loader_examples.py
```

Shows:
- Logo at multiple sizes
- All icons (PNG)
- All Unicode icons
- Placeholders
- Cache management

## Troubleshooting

### Images Not Showing

1. Check file exists: `ls assets/icons/dashboard.png`
2. Keep image reference: `label.image = icon`
3. Regenerate: `python3 utils/generate_assets.py`

### Out of Memory

1. Clear cache: `loader.clear_cache()`
2. Load smaller sizes
3. Don't preload all images

### Wrong Size

Load at display size:
```python
# Good
icon = load_icon("dashboard", size=(24, 24))

# Bad
icon = load_icon("dashboard")  # Full size (48x48)
```

## Resources

- **Full Documentation**: `assets/README.md`
- **Examples**: `utils/image_loader_examples.py`
- **API Reference**: Docstrings in `utils/image_loader.py`
- **Main README**: Section "Assets & Icons"

---

**Version:** 1.5.0  
**Last Updated:** October 9, 2025
