# Assets Directory

This directory contains all visual assets for the Campus Event System application.

## Directory Structure

```
assets/
├── icons/              # Application icons (PNG format)
│   ├── dashboard.png
│   ├── events.png
│   ├── resources.png
│   ├── bookings.png
│   ├── profile.png
│   ├── settings.png
│   ├── notifications.png
│   ├── search.png
│   ├── add.png
│   ├── edit.png
│   ├── delete.png
│   ├── approve.png
│   ├── reject.png
│   └── logout.png
│
└── images/             # General images and placeholders
    ├── logo.png                    # Application logo (400x200)
    ├── event_placeholder.png       # Event default image (600x400)
    ├── resource_placeholder.png    # Resource default image (600x400)
    └── avatar_placeholder.png      # User avatar default (200x200)
```

## Icon Set

### Navigation Icons (48x48 PNG)
- **dashboard.png** - Home/Dashboard icon
- **events.png** - Events calendar icon
- **resources.png** - Resources/facilities icon
- **bookings.png** - Bookings/reservations icon
- **profile.png** - User profile icon
- **settings.png** - Settings/preferences icon
- **notifications.png** - Notifications/alerts icon
- **logout.png** - Logout/sign out icon

### Action Icons (48x48 PNG)
- **search.png** - Search icon
- **add.png** - Add/create new icon
- **edit.png** - Edit/modify icon
- **delete.png** - Delete/remove icon
- **approve.png** - Approve/accept icon
- **reject.png** - Reject/decline icon

## Usage

### Using ImageLoader

```python
from utils.image_loader import ImageLoader, load_icon, load_image

# Get loader instance
loader = ImageLoader.get_instance()

# Load icon
icon = loader.load_icon("dashboard", size=(24, 24))

# Or use convenience function
icon = load_icon("dashboard", size=(24, 24))

# Display in label
label = tk.Label(parent, image=icon)
label.image = icon  # Keep reference!
label.pack()
```

### Using Unicode Icons (Fallback)

```python
from utils.image_loader import IconSet

# Use emoji icons when PNG not available
dashboard_label = tk.Label(
    parent,
    text=f"{IconSet.DASHBOARD} Dashboard"
)
```

## Image Specifications

### Logo
- **Format:** PNG
- **Size:** 400x200 pixels
- **Usage:** Application header, splash screen, about dialog
- **Background:** Transparent or gradient blue

### Icons
- **Format:** PNG with transparency
- **Size:** 48x48 pixels (will be resized as needed)
- **Style:** Flat design with solid colors
- **Colors:** Match theme colors (see Theme class)

### Event Images
- **Format:** PNG or JPG
- **Recommended Size:** 600x400 pixels
- **Aspect Ratio:** 3:2
- **Fallback:** `event_placeholder.png` (blue background with calendar icon)

### Resource Images
- **Format:** PNG or JPG
- **Recommended Size:** 600x400 pixels
- **Aspect Ratio:** 3:2
- **Fallback:** `resource_placeholder.png` (green background with building icon)

### User Avatars
- **Format:** PNG or JPG
- **Recommended Size:** 200x200 pixels
- **Aspect Ratio:** 1:1 (square)
- **Fallback:** `avatar_placeholder.png` (purple background with person icon)

## Adding New Assets

### Adding New Icons

1. Create icon as 48x48 PNG with transparency
2. Save to `assets/icons/` with descriptive name
3. Use ImageLoader to load:
   ```python
   icon = load_icon("your_icon_name", size=(24, 24))
   ```

### Adding Event/Resource Images

1. Prepare image in recommended size (600x400)
2. Save to `assets/images/` with unique filename
3. Reference in database or data structure
4. Load with ImageLoader:
   ```python
   image = loader.load_event_image("event123.png", size=(300, 200))
   ```

### Adding User Avatars

1. Prepare square image (200x200 recommended)
2. Save to `assets/images/` with user ID or unique name
3. Load with ImageLoader:
   ```python
   avatar = loader.load_user_avatar("user123.png", size=(100, 100))
   ```

## Generating Assets

To regenerate all placeholder assets (logo, icons, placeholders):

```bash
cd utils
python3 generate_assets.py
```

This will create:
- Application logo
- 14 icon placeholders
- Event placeholder
- Resource placeholder
- Avatar placeholder

## Icon Color Scheme

Icons follow the application theme colors:

| Icon Type | Color | Hex |
|-----------|-------|-----|
| Dashboard | Blue | #3498DB |
| Events | Red | #E74C3C |
| Resources | Green | #27AE60 |
| Bookings | Orange | #F39C12 |
| Profile | Purple | #9B59B6 |
| Settings | Gray | #95A5A6 |
| Notifications | Pink | #E91E63 |
| Search | Light Green | #2ECC71 |
| Add | Teal | #16A085 |
| Edit | Blue | #2980B9 |
| Delete | Dark Red | #C0392B |
| Approve | Green | #27AE60 |
| Reject | Red | #E74C3C |
| Logout | Gray | #7F8C8D |

## Image Caching

The ImageLoader automatically caches all loaded images to improve performance:

- **First Load:** Image is loaded from disk and cached
- **Subsequent Loads:** Image is retrieved from cache (instant)
- **Cache Key:** Combination of filename and size
- **Memory Management:** Call `loader.clear_cache()` if needed

## Best Practices

1. **Keep References:** Always keep a reference to PhotoImage objects
   ```python
   label = tk.Label(parent, image=icon)
   label.image = icon  # This prevents garbage collection
   ```

2. **Use Appropriate Sizes:** Load images at the size you need
   ```python
   # Good - load at display size
   icon = load_icon("dashboard", size=(24, 24))
   
   # Avoid - loading full size then scaling in tkinter
   icon = load_icon("dashboard")  # Full 48x48
   label = tk.Label(parent, image=icon, width=24, height=24)
   ```

3. **Preload for Performance:** Preload frequently used icons
   ```python
   loader.preload_icons(
       ['dashboard', 'events', 'resources', 'bookings'],
       size=(24, 24)
   )
   ```

4. **Use Placeholders:** Always provide fallback for missing images
   ```python
   # ImageLoader automatically generates placeholders for missing files
   image = loader.load_event_image(
       event.get('image'),  # May be None
       size=(300, 200)      # Will show placeholder if None
   )
   ```

5. **Clear Cache When Needed:** Clear cache after bulk operations
   ```python
   # After uploading many new images
   loader.clear_cache()
   ```

## File Naming Conventions

- **Icons:** lowercase, descriptive, no spaces: `dashboard.png`, `add_event.png`
- **Event Images:** prefix with `event_`: `event_tech_workshop.jpg`
- **Resource Images:** prefix with `resource_`: `resource_lab_101.jpg`
- **User Avatars:** prefix with `user_`: `user_12345.png`
- **General Images:** descriptive names: `logo.png`, `banner.jpg`

## Troubleshooting

### Images Not Loading

1. Check file exists in correct directory
2. Verify file extension matches (case-sensitive on some systems)
3. Check image format is supported (PNG, JPG, GIF)
4. Ensure PIL/Pillow is installed: `pip3 install Pillow`

### Placeholder Appears Instead of Icon

1. Icon file may be missing - check `assets/icons/` directory
2. File name may not match - check spelling
3. Regenerate assets: `python3 utils/generate_assets.py`

### Out of Memory Errors

1. Clear image cache: `loader.clear_cache()`
2. Reduce image sizes before loading
3. Load images on-demand rather than preloading all

## License

All placeholder images and icons are generated programmatically and are free to use.
Replace with custom graphics as needed for your deployment.

---

**Last Updated:** October 9, 2025  
**Version:** 1.0.0
