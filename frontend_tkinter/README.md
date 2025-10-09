# Campus Event System - Frontend (Tkinter)

A comprehensive desktop application for managing campus events, resources, and user interactions built with Python Tkinter.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Architecture](#architecture)
- [Pages & Components](#pages--components)
- [Reusable Components](#reusable-components)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [API Integration](#api-integration)

## 🎯 Overview

This is a full-featured campus event and resource management system with role-based access control, real-time notifications, analytics dashboards, and comprehensive administrative tools.

### Key Technologies

- **Python 3.8+** - Core language
- **Tkinter** - GUI framework
- **TTK** - Themed widget set
- **matplotlib** - Data visualization
- **Pillow (PIL)** - Image processing
- **tkcalendar** - Date picker widgets
- **requests** - API communication
- **threading** - Asynchronous operations

## ✨ Features

### For Students
- 🔍 **Browse Events** - Search and filter campus events with advanced options
- 📚 **Book Resources** - Reserve classrooms, labs, equipment, and facilities
- ✅ **Event Registration** - Register for events with real-time capacity checking
- 📅 **My Bookings** - View and manage resource bookings
- 🔔 **Notifications** - Real-time updates on bookings, events, and approvals
- 👤 **Profile Management** - Update profile, change password, manage settings

### For Organizers
- ➕ **Create Events** - Create and manage campus events
- 📊 **My Events** - Track event registrations and attendees
- 📝 **Event Updates** - Edit event details and send notifications
- 🎫 **Attendee Management** - View and manage registered participants

### For Admins
- ✅ **Event Approvals** - Review and approve/reject event requests
- 📋 **Booking Approvals** - Manage resource booking requests with conflict detection
- 👥 **User Management** - Comprehensive user administration (roles, blocking, deletion)
- 🏢 **Resource Management** - Add, edit, and manage campus resources
- 📈 **Analytics Dashboard** - Visualize system usage with interactive charts
- 📧 **Notifications Management** - System-wide notification controls

## 🚀 Installation

### Prerequisites

```bash
# Python 3.8 or higher
python3 --version

# pip package manager
pip3 --version
```

### Setup Steps

1. **Clone the repository**
   ```bash
   cd /path/to/CampusEventSystem/frontend_tkinter
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure API endpoint**
   Edit `config.py`:
   ```python
   API_BASE_URL = "http://localhost:8080/api"
   ```

4. **Run the application**
   ```bash
   python3 main.py
   ```

## 🏗️ Architecture

### Project Structure

```
frontend_tkinter/
├── main.py                      # Application entry point
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
│
├── assets/                      # Images, icons, resources
│
├── pages/                       # Application pages
│   ├── __init__.py
│   ├── login_page.py           # User authentication
│   ├── register_page.py        # User registration
│   ├── student_dashboard.py    # Student home page
│   ├── browse_events.py        # Event browsing with search
│   ├── browse_resources.py     # Resource browsing with filters
│   ├── book_resource.py        # Resource booking form
│   ├── create_event.py         # Event creation form
│   ├── my_events.py            # Organizer's events
│   ├── my_bookings.py          # User's bookings
│   ├── event_approvals.py      # Admin event approvals
│   ├── booking_approvals.py    # Admin booking approvals
│   ├── manage_users.py         # Admin user management
│   ├── manage_resources.py     # Admin resource management
│   ├── profile_page.py         # User profile management
│   ├── notifications_page.py   # Notification center
│   └── analytics_page.py       # Analytics dashboard
│
├── components/                  # Reusable UI components
│   ├── __init__.py
│   ├── search_component.py     # Advanced search widget
│   └── search_component_examples.py  # Usage examples
│
└── utils/                       # Utility modules
    ├── api_client.py           # API communication
    ├── session_manager.py      # Session management
    └── validators.py           # Form validation
```

### Design Patterns

- **MVC Pattern** - Separation of UI, logic, and data
- **Component-Based** - Reusable UI components
- **Observer Pattern** - Real-time updates via polling
- **Factory Pattern** - Dynamic page creation
- **Singleton** - Session and API client management

## 📄 Pages & Components

### Core Pages

#### 1. **Login Page** (`login_page.py`)
- User authentication with email/password
- Role-based redirection (Student/Organizer/Admin)
- "Remember Me" functionality
- Link to registration page

#### 2. **Browse Events Page** (`browse_events.py`) ⭐ **NEW: SearchComponent Integrated**
- Grid layout (3 columns) with event cards
- **SearchComponent integration** with:
  - Debounced search input
  - Advanced filters (date range, categories, status, sort)
  - Removable filter tags
- Event details modal with registration
- Pagination for large result sets
- Color-coded category badges
- Real-time capacity checking

#### 3. **Browse Resources Page** (`browse_resources.py`) ⭐ **NEW: SearchComponent Integrated**
- 2-column grid layout with resource cards
- **SearchComponent integration** with:
  - Resource type filtering
  - Availability date picker
  - Amenity-based search
  - Sort by capacity/location/name
- Sidebar filters (kept for advanced options):
  - Resource type radio buttons
  - Capacity sliders (min/max)
  - Amenity checkboxes
  - Time slot selection
- Resource details modal
- Booking functionality

#### 4. **Booking Approvals Page** (`booking_approvals.py`)
- Pending bookings queue with priority sorting
- **Conflict detection** - Highlights time/resource conflicts
- Calendar view with color-coded bookings
- Approval modal with:
  - User booking history
  - Alternative time slot suggestions
  - Reason for rejection input
- Bulk approve/reject operations
- Filter by resource type, date range, status
- Export booking reports

#### 5. **Profile Page** (`profile_page.py`)
- Two-tab interface:
  - **View Profile Tab**:
    - Profile photo upload with preview
    - Display user information
    - Edit profile modal
  - **Account Settings Tab**:
    - Password change with strength indicator
    - Email notification preferences
    - Privacy settings (profile visibility)
    - Account activity log
- Photo upload with base64 encoding
- Form validation for all inputs

#### 6. **Manage Users Page** (`manage_users.py`)
- Comprehensive user table (Treeview)
- Search and filter controls (can be upgraded to SearchComponent)
- User actions:
  - View detailed user profile
  - Edit user role (Student/Organizer/Admin)
  - Block/Unblock users
  - Reset password
  - Send email
  - Delete user (double confirmation)
- Context menu (right-click) for quick actions
- CSV export for user list
- Activity statistics per user

#### 7. **Analytics Page** (`analytics_page.py`)
- **Overview Cards** (4):
  - Total Events (with growth %)
  - Active Users (with growth %)
  - Total Bookings (with growth %)
  - Revenue (with growth %)
- **Interactive Charts** (5):
  - Events by Category (Pie Chart)
  - Monthly Event Registrations (Line Chart)
  - Resource Utilization (Bar Chart)
  - User Growth Over Time (Area Chart)
  - Popular Resources (Horizontal Bar)
- Date range selector for analytics
- Export reports (PDF/Excel options)
- Embedded matplotlib with TkAgg backend

#### 8. **Notifications Page** (`notifications_page.py`)
- Grouped notifications (Today/Yesterday/Earlier)
- 8 notification types with icons:
  - Booking Approved ✅
  - Booking Rejected ❌
  - Event Registration 🎟️
  - Event Reminder ⏰
  - Event Cancelled 🚫
  - Resource Available 📚
  - Profile Update 👤
  - System Announcement 📢
- Filter buttons (All/Unread/Read)
- Mark as read/delete actions
- Action links to related items
- **Real-time updates** (30-second polling)
- Timestamp formatting (relative times)

## 🧩 Reusable Components

### SearchComponent ⭐

A powerful, reusable search component with advanced filtering capabilities.

### CalendarView ⭐ **NEW**

A comprehensive, interactive calendar component with multiple view modes and event markers.

#### Features
- **Debounced Search** - 500ms delay to prevent excessive API calls
- **Advanced Filters Modal** - Date range, categories, status, sort options
- **Filter Tags** - Visual display of active filters with remove buttons
- **Search History** - Tracks last 10 searches
- **Highly Configurable** - Adapt for different use cases
- **Callback Pattern** - Clean integration with parent pages

#### Usage Example

```python
from components.search_component import SearchComponent

def handle_search(search_text, filters):
    """Called when user searches or changes filters"""
    print(f"Search: {search_text}")
    print(f"Filters: {filters}")
    # Apply to your data...

# Configure for your use case
config = {
    'categories': ['Category1', 'Category2', 'Category3'],
    'statuses': ['Active', 'Inactive', 'Pending'],
    'sort_options': ['Name', 'Date', 'Popularity'],
    'show_date_filter': True,
    'show_category_filter': True,
    'show_status_filter': True,
    'placeholder': 'Search...'
}

# Create component
search = SearchComponent(
    parent_frame,
    on_search_callback=handle_search,
    config=config,
    colors=app_colors  # Optional: custom color scheme
)
search.pack(fill='x', padx=20, pady=10)
```

#### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `categories` | list | `[]` | List of category options for filter |
| `statuses` | list | `[]` | List of status options for filter |
| `sort_options` | list | `['Relevance']` | Sorting options |
| `show_date_filter` | bool | `True` | Show date range picker |
| `show_category_filter` | bool | `True` | Show category checkboxes |
| `show_status_filter` | bool | `True` | Show status radio buttons |
| `placeholder` | str | `'Search...'` | Search input placeholder |

#### Integration Examples

See `components/search_component_examples.py` for:
- Events page configuration
- Resources page configuration
- Users page configuration
- Bookings page configuration
- Programmatic control examples
- Complete page integration example

#### Public Methods

```python
# Get current search text
search_text = search_component.get_search_text()

# Get active filters dict
filters = search_component.get_active_filters()

# Clear search input only
search_component.clear_search()

# Reset everything (search + filters)
search_component.reset_all()
```

#### Filter Object Structure

The `filters` dict passed to the callback contains:

```python
{
    'date_range': {
        'start': datetime.date,  # or None
        'end': datetime.date      # or None
    },
    'categories': ['Cat1', 'Cat2'],  # Selected categories
    'status': 'Active',              # Selected status or None
    'sort': 'Name'                   # Selected sort option
}
```

---

### CalendarView Component

#### Features
- **Multiple View Modes** - Month, Week, Day views
- **Event Markers** - Color-coded dots/bars on dates with events
- **Booking Markers** - Status-based colors for bookings
- **Interactive** - Click dates to see details
- **Tooltips** - Hover over dates to see quick preview
- **Navigation** - Previous/Next buttons, "Today" button
- **Mini Mode** - Compact mode for dashboards/sidebars
- **Highly Customizable** - Colors, view mode, controls visibility

#### Usage Example

```python
from components import CalendarView

def on_date_click(date, items):
    """Called when user clicks a date"""
    print(f"Date: {date}")
    print(f"Events/Bookings: {len(items)}")
    for item in items:
        print(f"  - {item.get('title') or item.get('resource')}")

# Sample data
events = [
    {
        'title': 'Data Science Workshop',
        'category': 'workshop',
        'start_time': '2025-10-15 14:00:00',
        'venue': 'Lab 101',
        'status': 'approved'
    }
]

bookings = [
    {
        'resource': 'Conference Room A',
        'start_time': '2025-10-15 09:00:00',
        'status': 'approved'
    }
]

# Create calendar
calendar = CalendarView(
    parent_frame,
    on_date_click_callback=on_date_click,
    events=events,
    bookings=bookings,
    view_mode='month',  # 'month', 'week', or 'day'
    show_controls=True,
    mini_mode=False
)
calendar.pack(fill='both', expand=True, padx=20, pady=20)
```

#### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `on_date_click_callback` | function | `None` | Callback function(date, items) |
| `events` | list | `[]` | List of event dicts |
| `bookings` | list | `[]` | List of booking dicts |
| `view_mode` | str | `'month'` | Initial view: 'month', 'week', or 'day' |
| `colors` | dict | Default colors | Custom color scheme |
| `show_controls` | bool | `True` | Show navigation controls |
| `mini_mode` | bool | `False` | Compact mode for sidebars |

#### View Modes

**Month View:**
- Grid layout with all dates
- Event markers (colored dots/bars)
- Hover tooltips showing event list
- Click date to see full details

**Week View:**
- 7-column layout (Sun-Sat)
- Hourly time slots (8 AM - 8 PM)
- Events displayed in time slots
- Click time slot to see items for that hour

**Day View:**
- Single day, 24-hour breakdown
- Detailed event/booking display
- Full event information in slots
- Scroll through hours

#### Event Colors (by category)

| Category | Color | Hex |
|----------|-------|-----|
| Academic | Blue | `#3498DB` |
| Sports | Green | `#27AE60` |
| Cultural | Purple | `#9B59B6` |
| Workshop | Orange | `#F39C12` |
| Seminar | Red | `#E74C3C` |
| Conference | Teal | `#1ABC9C` |
| Social | Pink | `#E91E63` |

#### Booking Colors (by status)

| Status | Color | Hex |
|--------|-------|-----|
| Approved | Green | `#27AE60` |
| Pending | Orange | `#F39C12` |
| Rejected | Red | `#E74C3C` |
| Cancelled | Gray | `#95A5A6` |
| Active | Blue | `#3498DB` |

#### Public Methods

```python
# Update calendar data
calendar.update_data(events=new_events, bookings=new_bookings)

# Navigate to specific date
calendar.set_date('2025-12-25')
calendar.set_date(datetime.now())

# Change view mode
calendar.set_view('week')  # 'month', 'week', or 'day'

# Get current displayed date
current = calendar.get_current_date()

# Get selected date (user clicked)
selected = calendar.get_selected_date()
```

#### Integration Examples

**Dashboard (Mini Calendar):**
```python
mini_calendar = CalendarView(
    sidebar_frame,
    events=upcoming_events,
    view_mode='month',
    show_controls=True,
    mini_mode=True  # Compact mode
)
mini_calendar.pack(fill='both', padx=10, pady=10)
```

**Events Page (Full Calendar):**
```python
full_calendar = CalendarView(
    main_frame,
    on_date_click_callback=show_event_details,
    events=all_events,
    view_mode='month',
    show_controls=True,
    mini_mode=False
)
full_calendar.pack(fill='both', expand=True, padx=20, pady=20)
```

**Bookings Page (Availability Calendar):**
```python
booking_calendar = CalendarView(
    booking_frame,
    on_date_click_callback=check_availability,
    events=[],
    bookings=all_bookings,
    view_mode='week',  # Week view for time slots
    show_controls=True
)
booking_calendar.pack(fill='both', expand=True)
```

#### Data Format

**Events:**
```python
{
    'id': 1,
    'title': 'Event Title',
    'category': 'workshop',  # academic, sports, cultural, etc.
    'start_time': '2025-10-15 14:00:00',  # ISO format
    'end_time': '2025-10-15 16:00:00',
    'venue': 'Location',
    'status': 'approved',
    'description': 'Event details...'
}
```

**Bookings:**
```python
{
    'id': 1,
    'resource': 'Conference Room A',
    'start_time': '2025-10-15 09:00:00',
    'end_time': '2025-10-15 11:00:00',
    'status': 'approved',  # approved, pending, rejected, cancelled
    'user_id': 123,
    'purpose': 'Team meeting'
}
```

### Custom Styled Widgets ⭐ **NEW**

A comprehensive library of custom-styled UI widgets with consistent theming, animations, and interactive states.

#### Available Widgets

1. **StyledButton** - Custom button with variants and states
2. **StyledEntry** - Enhanced text entry with icons and validation
3. **StyledCard** - Card component with shadow and hover effects
4. **ProgressBar** - Animated progress bar with percentage
5. **Toast** - Toast notification system with auto-dismiss

#### 1. StyledButton

Custom button widget with multiple variants, hover effects, loading states, and disabled states.

**Features:**
- 5 variants: primary, secondary, success, danger, ghost
- Smooth hover effects
- Loading state with animated spinner
- Disabled state with proper styling
- Customizable size and appearance

**Usage:**
```python
from components import StyledButton

# Primary button
save_btn = StyledButton(
    parent,
    text="Save Changes",
    variant="primary",
    command=save_handler,
    width=140,
    height=36
)
save_btn.pack(pady=10)

# Loading state
save_btn.set_loading(True)  # Shows spinner
# ... after operation completes ...
save_btn.set_loading(False)

# Disabled state
save_btn.set_disabled(True)

# Update text
save_btn.set_text("Saved!")
```

**Variants:**

| Variant | Color | Use Case |
|---------|-------|----------|
| `primary` | Blue | Main actions (Submit, Save, Continue) |
| `secondary` | Gray | Secondary actions (Cancel, Back) |
| `success` | Green | Positive actions (Approve, Confirm) |
| `danger` | Red | Destructive actions (Delete, Reject) |
| `ghost` | Transparent | Subtle actions (View More, Skip) |

**Methods:**
- `set_loading(bool)` - Enable/disable loading animation
- `set_disabled(bool)` - Enable/disable button
- `set_text(str)` - Update button text

#### 2. StyledEntry

Enhanced text entry widget with icons, placeholder text, validation states, and clear button.

**Features:**
- Left/right icon support (emojis or symbols)
- Placeholder text that disappears on focus
- Error state with red border and error message
- Success state with green border
- Optional clear button
- Password visibility toggle
- Focus states with border highlights

**Usage:**
```python
from components import StyledEntry

# Basic entry with placeholder
name_entry = StyledEntry(
    parent,
    placeholder="Enter your name",
    width=30
)
name_entry.pack(fill='x', pady=5)

# Entry with icon and clear button
email_entry = StyledEntry(
    parent,
    placeholder="Enter email",
    icon_left="📧",
    clear_button=True
)
email_entry.pack(fill='x', pady=5)

# Password entry with visibility toggle
password_entry = StyledEntry(
    parent,
    placeholder="Enter password",
    icon_right="👁️",
    show="•"  # Hide characters
)
password_entry.pack(fill='x', pady=5)

# Get value
email = email_entry.get()

# Set value
email_entry.set("user@example.com")

# Validation states
if not email:
    email_entry.set_error("Email is required")
elif "@" not in email:
    email_entry.set_error("Invalid email format")
else:
    email_entry.set_success()

# Clear error
email_entry.clear_state()

# Clear everything
email_entry.clear()

# Set focus
email_entry.focus()
```

**Methods:**
- `get()` - Get entry value (returns empty string if placeholder shown)
- `set(value)` - Set entry value
- `clear()` - Clear entry and show placeholder
- `set_error(message)` - Show error state with message
- `set_success()` - Show success state (green border)
- `clear_state()` - Remove error/success state
- `focus()` - Set focus to entry

#### 3. StyledCard

Card widget with elevated shadow effect, rounded corners, and optional hover states.

**Features:**
- Elevated shadow effect for depth
- Hover state with enhanced shadow
- Customizable padding
- Optional click handler
- Automatic event binding for all children

**Usage:**
```python
from components import StyledCard

# Basic card
card = StyledCard(
    parent,
    padding=20,
    hover=True
)
card.pack(pady=10, padx=20, fill='x')

# Add content to card (use card.content_frame as parent)
tk.Label(
    card.content_frame,
    text="Card Title",
    font=("Segoe UI", 14, "bold")
).pack(anchor='w')

tk.Label(
    card.content_frame,
    text="Card content goes here..."
).pack(anchor='w', pady=(5, 0))

# Clickable card
clickable_card = StyledCard(
    parent,
    padding=20,
    hover=True,
    click_handler=lambda: Toast.show(root, "Card clicked!", "info")
)
clickable_card.pack(pady=10)
```

**Parameters:**
- `padding` (int) - Internal padding in pixels (default: 15)
- `hover` (bool) - Enable hover effect (default: True)
- `click_handler` (function) - Optional click callback

**Note:** Always add child widgets to `card.content_frame`, not directly to `card`.

#### 4. ProgressBar

Animated progress bar with percentage display and customizable colors.

**Features:**
- Smooth animation to target percentage
- Percentage label overlay
- Customizable foreground/background colors
- Rounded corners
- Reset functionality

**Usage:**
```python
from components import ProgressBar, Theme

# Create progress bar
progress = ProgressBar(
    parent,
    width=400,
    height=24,
    bg_color=Theme.BG_LIGHT,
    fg_color=Theme.PRIMARY
)
progress.pack(pady=10)

# Set progress (animates smoothly)
progress.set_progress(75)

# Change color
progress.set_color(Theme.SUCCESS)

# Reset to 0
progress.reset()

# Example: File upload simulation
def simulate_upload():
    progress.reset()
    
    def update(current):
        if current <= 100:
            progress.set_progress(current)
            root.after(50, lambda: update(current + 5))
        else:
            Toast.show(root, "Upload complete!", "success")
    
    update(0)

upload_btn = StyledButton(
    parent,
    text="Start Upload",
    variant="primary",
    command=simulate_upload
)
upload_btn.pack(pady=5)
```

**Methods:**
- `set_progress(value)` - Set progress 0-100 with animation
- `set_color(color)` - Change foreground color
- `reset()` - Reset progress to 0

#### 5. Toast Notifications

Toast notification system with auto-dismiss, animations, and multiple types.

**Features:**
- 4 types: success, error, info, warning
- Auto-dismiss after configurable duration (default: 3 seconds)
- Slide-in animation from top
- Multiple toasts stack vertically
- Click to dismiss manually
- Always on top
- Fade-out animation

**Usage:**
```python
from components import Toast

# Success toast
Toast.show(
    root,
    "Changes saved successfully!",
    type="success"
)

# Error toast
Toast.show(
    root,
    "Failed to connect to server",
    type="error",
    duration=5000  # Show for 5 seconds
)

# Info toast
Toast.show(
    root,
    "New event added to your calendar",
    type="info"
)

# Warning toast
Toast.show(
    root,
    "Your session will expire in 5 minutes",
    type="warning"
)

# Multiple toasts (they stack)
Toast.show(root, "First notification", "info")
root.after(300, lambda: Toast.show(root, "Second notification", "success"))
root.after(600, lambda: Toast.show(root, "Third notification", "warning"))
```

**Types:**

| Type | Color | Icon | Use Case |
|------|-------|------|----------|
| `success` | Green | ✓ | Successful operations |
| `error` | Red | ✕ | Errors and failures |
| `info` | Blue | ℹ | Information messages |
| `warning` | Orange | ⚠ | Warnings and alerts |

**Parameters:**
- `parent` - Parent widget (usually root window)
- `message` - Message text to display
- `type` - Toast type: "success", "error", "info", or "warning"
- `duration` - Duration in milliseconds before auto-dismiss (default: 3000)

#### Theme Colors

All widgets use a centralized theme for consistent styling:

```python
from components import Theme

# Use theme colors in your application
frame = tk.Frame(parent, bg=Theme.BG_LIGHT)
label = tk.Label(parent, fg=Theme.TEXT_DARK)
button_bg = Theme.PRIMARY
```

**Available Colors:**
- Primary: `PRIMARY`, `PRIMARY_HOVER`, `PRIMARY_ACTIVE`
- Secondary: `SECONDARY`, `SECONDARY_HOVER`, `SECONDARY_ACTIVE`
- Success: `SUCCESS`, `SUCCESS_HOVER`, `SUCCESS_ACTIVE`
- Danger: `DANGER`, `DANGER_HOVER`, `DANGER_ACTIVE`
- Warning: `WARNING`, `WARNING_HOVER`, `WARNING_ACTIVE`
- Info: `INFO`, `INFO_HOVER`
- Text: `TEXT_DARK`, `TEXT_LIGHT`, `TEXT_MUTED`, `TEXT_PLACEHOLDER`
- Background: `BG_WHITE`, `BG_LIGHT`, `BG_DARK`, `BG_CARD`
- Border: `BORDER_LIGHT`, `BORDER_ERROR`, `BORDER_SUCCESS`, `BORDER_FOCUS`
- Shadow: `SHADOW`, `SHADOW_HOVER`

#### Utility Functions

**Loading Dialog:**
```python
from components import show_loading_dialog

# Show loading dialog (modal, blocks interaction)
dialog = show_loading_dialog(root, "Fetching data...")

# ... perform operation ...

# Close dialog
dialog.destroy()
```

#### Complete Form Example

See `components/custom_widgets_examples.py` for a complete form example that demonstrates all widgets working together:

```python
from components import (
    StyledButton, StyledEntry, StyledCard,
    ProgressBar, Toast, Theme
)

# Form card
form = StyledCard(parent, padding=30)
form.pack(padx=40, pady=20, fill='x')

# Title
tk.Label(
    form.content_frame,
    text="Create New Event",
    font=("Segoe UI", 18, "bold")
).pack(anchor='w', pady=(0, 20))

# Event name
tk.Label(form.content_frame, text="Event Name *").pack(anchor='w', pady=(10, 2))
name_entry = StyledEntry(form.content_frame, placeholder="Enter event name", icon_left="📝")
name_entry.pack(fill='x', pady=5)

# Category
tk.Label(form.content_frame, text="Category *").pack(anchor='w', pady=(10, 2))
category_entry = StyledEntry(form.content_frame, placeholder="e.g., Workshop", icon_left="🏷️")
category_entry.pack(fill='x', pady=5)

# Submit button
submit_btn = StyledButton(
    form.content_frame,
    text="Create Event",
    variant="success",
    command=submit_handler
)
submit_btn.pack(pady=(20, 0))

def submit_handler():
    # Validate
    if not name_entry.get():
        name_entry.set_error("Event name is required")
        Toast.show(root, "Please fill in all required fields", "error")
        return
    
    # Show loading
    submit_btn.set_loading(True)
    
    # Simulate API call
    def finish():
        submit_btn.set_loading(False)
        Toast.show(root, "Event created successfully!", "success")
        name_entry.clear()
        category_entry.clear()
    
    root.after(1500, finish)
```

#### Examples File

Run `components/custom_widgets_examples.py` to see an interactive demo showcasing:
- All button variants and states
- Text entries with different configurations
- Card layouts and interactions
- Progress bar animations
- Toast notifications
- Complete form with validation

## 🎨 Assets & Icons

### Image Loader System

The application includes a comprehensive image loading and caching system for managing icons, logos, and images.

#### ImageLoader Class

Centralized image management with automatic caching:

```python
from utils.image_loader import ImageLoader, load_icon, load_image, load_logo

# Get singleton instance
loader = ImageLoader.get_instance()

# Load logo
logo = loader.load_logo(size=(200, 100))

# Load icon
icon = loader.load_icon("dashboard", size=(24, 24))

# Load event image (with fallback to placeholder)
event_img = loader.load_event_image("event123.jpg", size=(300, 200))

# Load resource image
resource_img = loader.load_resource_image("lab101.jpg", size=(300, 200))

# Load user avatar
avatar = loader.load_user_avatar("user456.png", size=(100, 100))

# Convenience functions
logo = load_logo(size=(200, 100))
icon = load_icon("dashboard", size=(24, 24))
```

**Features:**
- Automatic image caching for performance
- Automatic resizing to specified dimensions
- Placeholder generation for missing images
- PNG, JPG, GIF format support
- Thread-safe caching

**Cache Management:**
```python
# Get cache size
cache_size = loader.get_cache_size()

# Clear entire cache
loader.clear_cache()

# Remove specific image
loader.remove_from_cache("logo.png", size=(200, 100))

# Preload icons for better performance
loader.preload_icons(['dashboard', 'events', 'resources'], size=(24, 24))
```

#### IconSet Class

Unicode emoji icons for fallback or quick prototyping:

```python
from utils.image_loader import IconSet

# Navigation icons
tk.Label(parent, text=f"{IconSet.DASHBOARD} Dashboard")
tk.Label(parent, text=f"{IconSet.EVENTS} Events")
tk.Label(parent, text=f"{IconSet.RESOURCES} Resources")
tk.Label(parent, text=f"{IconSet.BOOKINGS} Bookings")

# Action icons
tk.Label(parent, text=f"{IconSet.ADD} Add New")
tk.Label(parent, text=f"{IconSet.EDIT} Edit")
tk.Label(parent, text=f"{IconSet.DELETE} Delete")
tk.Label(parent, text=f"{IconSet.APPROVE} Approve")

# Dynamic icon selection
category = "academic"
icon = IconSet.get_category_icon(category)
tk.Label(parent, text=f"{icon} {category.capitalize()}")

status = "approved"
icon = IconSet.get_status_icon(status)
tk.Label(parent, text=f"{icon} {status.capitalize()}")
```

**Available Icon Categories:**
- **Navigation:** Dashboard, Events, Resources, Bookings, Profile, Settings, Notifications, Logout
- **Actions:** Search, Add, Edit, Delete, Save, Cancel, Approve, Reject, Refresh
- **Status:** Success, Error, Warning, Info, Pending, Active, Inactive
- **Content:** Email, Phone, Location, Calendar, Clock, User, Users, Building
- **Categories:** Academic, Sports, Cultural, Workshop, Seminar, Conference, Social
- **UI:** Menu, Close, Back, Forward, Up, Down, More, Expand, Collapse

### Assets Directory Structure

```
assets/
├── icons/                     # Application icons (48x48 PNG)
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
└── images/                    # General images and placeholders
    ├── logo.png                    # App logo (400x200)
    ├── event_placeholder.png       # Event default (600x400)
    ├── resource_placeholder.png    # Resource default (600x400)
    └── avatar_placeholder.png      # User avatar default (200x200)
```

### Icon Specifications

| Icon Type | Size | Format | Usage |
|-----------|------|--------|-------|
| Navigation Icons | 48x48 | PNG | Sidebar, menus, page headers |
| Action Icons | 48x48 | PNG | Buttons, toolbars |
| Logo | 400x200 | PNG | App header, splash screen |
| Event Images | 600x400 | PNG/JPG | Event cards, details |
| Resource Images | 600x400 | PNG/JPG | Resource cards, details |
| User Avatars | 200x200 | PNG/JPG | Profile, comments |

### Generating Assets

To create or regenerate all placeholder assets:

```bash
cd utils
python3 generate_assets.py
```

This creates:
- Application logo with gradient and icons
- 14 colored icon placeholders
- Event placeholder (blue with calendar)
- Resource placeholder (green with building)
- Avatar placeholder (purple with person)

### Usage Examples

**Loading Icon in Button:**
```python
icon = load_icon("add", size=(16, 16))
button = tk.Button(parent, image=icon, text=" Add Event", compound="left")
button.image = icon  # Keep reference!
```

**Event Card with Image:**
```python
# Load event image (falls back to placeholder if missing)
event_img = loader.load_event_image(
    event.get('image_filename'),
    size=(300, 200)
)

img_label = tk.Label(card, image=event_img)
img_label.image = event_img
img_label.pack()
```

**User Avatar:**
```python
avatar = loader.load_user_avatar(
    user.get('avatar_filename'),
    size=(64, 64)
)

avatar_label = tk.Label(profile_frame, image=avatar)
avatar_label.image = avatar
avatar_label.pack()
```

**Combining PNG and Unicode Icons:**
```python
# Try PNG first, fallback to Unicode
try:
    icon_img = load_icon("dashboard", size=(24, 24))
    label = tk.Label(parent, image=icon_img)
    label.image = icon_img
except:
    # Fallback to Unicode
    label = tk.Label(parent, text=IconSet.DASHBOARD)
```

### Best Practices

1. **Keep Image References:**
   ```python
   label = tk.Label(parent, image=icon)
   label.image = icon  # Prevents garbage collection!
   ```

2. **Load at Display Size:**
   ```python
   # Good - load at needed size
   icon = load_icon("dashboard", size=(24, 24))
   
   # Avoid - loading full size unnecessarily
   icon = load_icon("dashboard")  # Loads 48x48
   ```

3. **Preload Frequently Used Icons:**
   ```python
   loader.preload_icons(
       ['dashboard', 'events', 'resources', 'bookings'],
       size=(24, 24)
   )
   ```

4. **Use Placeholders:**
   ```python
   # ImageLoader automatically shows placeholder for None/missing files
   image = loader.load_event_image(None, size=(300, 200))
   ```

5. **Clear Cache When Needed:**
   ```python
   # After bulk image uploads
   loader.clear_cache()
   ```

### File Naming Conventions

- **Icons:** `lowercase_descriptive.png` (e.g., `dashboard.png`, `add_event.png`)
- **Event Images:** `event_descriptive.jpg` (e.g., `event_tech_workshop.jpg`)
- **Resource Images:** `resource_descriptive.jpg` (e.g., `resource_lab_101.jpg`)
- **User Avatars:** `user_id.png` (e.g., `user_12345.png`)

### Demo Application

Run the image loader demo to see all features:

```bash
cd utils
python3 image_loader_examples.py
```

Features:
- Logo display at multiple sizes
- Icon gallery (all 14 icons)
- Event/resource image placeholders
- Avatar placeholders
- Unicode icon set showcase
- Cache information and management

For detailed documentation, see: `assets/README.md`

## ⚙️ Configuration

### Color Scheme

The application uses a consistent color palette:

```python
colors = {
    'primary': '#2C3E50',      # Dark blue-gray
    'secondary': '#3498DB',    # Bright blue
    'success': '#27AE60',      # Green
    'warning': '#F39C12',      # Orange
    'danger': '#E74C3C',       # Red
    'background': '#ECF0F1'    # Light gray
}
```

### API Configuration

Edit `config.py`:

```python
# API Settings
API_BASE_URL = "http://localhost:8080/api"
REQUEST_TIMEOUT = 30  # seconds

# Session Settings
SESSION_TIMEOUT = 3600  # 1 hour

# Pagination
ITEMS_PER_PAGE = 20

# Notification Polling
NOTIFICATION_POLL_INTERVAL = 30000  # 30 seconds (in milliseconds)
```

## 🔌 API Integration

### API Client (`utils/api_client.py`)

The `APIClient` class handles all HTTP communication:

```python
from utils.api_client import APIClient

api = APIClient()

# GET request
events = api.get('events')

# POST request with data
response = api.post('events', {
    'title': 'New Event',
    'venue': 'Hall A',
    # ...
})

# PUT request
updated = api.put('events/123', {'title': 'Updated Title'})

# DELETE request
api.delete('events/123')
```

### Session Manager (`utils/session_manager.py`)

Manages user authentication state:

```python
from utils.session_manager import SessionManager

session = SessionManager()

# Store session after login
session.set_session(user_data, token)

# Get current user
user = session.get_user()

# Get user role
role = session.get_role()  # 'STUDENT', 'ORGANIZER', 'ADMIN'

# Check if logged in
if session.is_logged_in():
    # ...

# Logout
session.clear_session()
```

## 📝 Usage Examples

### Example 1: Integrating SearchComponent into a New Page

```python
import tkinter as tk
from components.search_component import SearchComponent

class MyPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure SearchComponent
        config = {
            'categories': ['Type1', 'Type2'],
            'statuses': ['Active', 'Inactive'],
            'sort_options': ['Name', 'Date'],
            'placeholder': 'Search items...'
        }
        
        # Create search component
        search = SearchComponent(
            self,
            on_search_callback=self.on_search,
            config=config
        )
        search.pack(fill='x', padx=20, pady=10)
        
        # Results area
        self.results = tk.Frame(self)
        self.results.pack(fill='both', expand=True)
    
    def on_search(self, search_text, filters):
        """Handle search updates"""
        # Clear results
        for widget in self.results.winfo_children():
            widget.destroy()
        
        # Filter your data
        filtered_data = self.filter_data(search_text, filters)
        
        # Display results
        self.display_results(filtered_data)
```

### Example 2: Adding Real-time Notifications

```python
def start_notification_polling(self):
    """Poll for new notifications every 30 seconds"""
    def poll():
        try:
            notifications = self.api.get('notifications')
            self.update_notification_badge(len(notifications))
        except Exception as e:
            print(f"Polling error: {e}")
        
        # Schedule next poll
        self.after(30000, poll)  # 30 seconds
    
    poll()  # Start polling
```

### Example 3: Creating a Modal Dialog

```python
def show_details_modal(self, item):
    """Show item details in a modal"""
    modal = tk.Toplevel(self)
    modal.title('Item Details')
    modal.geometry('500x400')
    modal.transient(self.winfo_toplevel())
    modal.grab_set()
    
    # Center modal
    modal.update_idletasks()
    x = (modal.winfo_screenwidth() // 2) - (500 // 2)
    y = (modal.winfo_screenheight() // 2) - (400 // 2)
    modal.geometry(f'500x400+{x}+{y}')
    
    # Add content
    tk.Label(modal, text=item['name'], font=('Helvetica', 16, 'bold')).pack(pady=20)
    # ... more content ...
    
    # Close button
    tk.Button(modal, text='Close', command=modal.destroy).pack(pady=10)
```

## 🛠️ Development

### Adding a New Page

1. **Create page file** in `pages/` directory:
   ```python
   # pages/my_new_page.py
   import tkinter as tk
   
   class MyNewPage(tk.Frame):
       def __init__(self, parent, controller):
           super().__init__(parent)
           self.controller = controller
           # Build UI...
   ```

2. **Register page** in `main.py`:
   ```python
   from pages.my_new_page import MyNewPage
   
   # In CampusEventApp.__init__:
   self.frames['MyNewPage'] = MyNewPage(self.container, self)
   ```

3. **Add navigation** (if needed):
   ```python
   # In sidebar or menu:
   tk.Button(sidebar, text='My Page', 
             command=lambda: controller.show_page('MyNewPage')).pack()
   ```

### Code Style Guidelines

- **PEP 8** - Follow Python style guide
- **Type hints** - Use where beneficial
- **Docstrings** - Document all classes and public methods
- **Error handling** - Always catch exceptions in API calls
- **Threading** - Use threads for long-running operations
- **Naming** - Use descriptive variable names
  - `_private_method()` - Internal methods
  - `public_method()` - Public API
  - `CONSTANTS` - All caps for constants

### Testing

Run manual tests for:
- ✅ Login/logout flows
- ✅ Page navigation
- ✅ Form validation
- ✅ API error handling
- ✅ Search and filtering
- ✅ Modal dialogs
- ✅ Responsive layouts

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'tkcalendar'`  
**Solution**: Install dependencies: `pip3 install -r requirements.txt`

**Issue**: API connection errors  
**Solution**: Check `config.py` API_BASE_URL and ensure backend is running

**Issue**: SearchComponent not found  
**Solution**: Ensure `components/__init__.py` exists with proper imports

**Issue**: Tkinter not found on macOS  
**Solution**: Install Python with tkinter: `brew install python-tk@3.9`

**Issue**: Images not loading  
**Solution**: Check `assets/` directory exists and paths are correct

## �️ Error Handler & Exception Management

Comprehensive error handling system for graceful error management, logging, and user-friendly error messages.

### ErrorHandler Class

Centralized singleton for handling all types of errors:
- **API/HTTP errors** (400, 401, 403, 404, 500, etc.)
- **Validation errors** (form field validation)
- **Network errors** (connection issues, timeouts)
- **Session management** (authentication, authorization)
- **Generic exceptions** (unexpected errors)

**Key Features:**
- ✅ Automatic error logging to `logs/error.log`
- ✅ User-friendly error messages
- ✅ Toast notification integration
- ✅ Widget highlighting for validation errors
- ✅ Session expiration handling
- ✅ Context-aware error messages
- ✅ Comprehensive error logging with traceback

### Quick Start

```python
from utils.error_handler import get_error_handler, setup_error_handling

# Setup error handler with callbacks
error_handler = setup_error_handling(
    toast_callback=show_toast_function,
    logout_callback=logout_function,
    login_redirect_callback=redirect_to_login_function
)

# Handle API error
try:
    response = api_client.get('/events')
except Exception as error:
    error_handler.handle_api_error(error, context="Loading events")

# Handle validation error
if not email:
    error_handler.handle_validation_error(
        field="Email",
        message="Email is required",
        widget=email_entry  # Optional: highlights widget
    )

# Handle network error
error_handler.handle_network_error()

# Log error
error_handler.log_error(error, context="Processing booking")
```

### Custom Exceptions

```python
from utils.error_handler import (
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    SessionExpiredError
)

# Validation error
if len(password) < 8:
    raise ValidationError("Password", "Must be at least 8 characters")

# Authentication error
if not session.is_logged_in():
    raise AuthenticationError("User must be logged in")

# Authorization error
if user_role != 'ADMIN':
    raise AuthorizationError(required_role='ADMIN', user_role=user_role)

# Session expired
if token_expired:
    raise SessionExpiredError("Session has expired")
```

### Decorators

**@require_login** - Check if user is logged in:

```python
from utils.error_handler import require_login

@require_login
def view_dashboard(self):
    """Only logged-in users can access"""
    # This only executes if user is logged in
    pass
```

**@require_role** - Check user role:

```python
from utils.error_handler import require_role

@require_role('ADMIN')
def delete_user(self, user_id):
    """Only ADMIN can delete users"""
    pass

@require_role('ADMIN', 'ORGANIZER')
def create_event(self, event_data):
    """ADMIN or ORGANIZER can create events"""
    pass
```

**@handle_errors** - Wrap function with error handling:

```python
from utils.error_handler import handle_errors

@handle_errors(context="Loading events", return_on_error=[])
def load_events(self):
    """Automatically handles any errors"""
    return api_client.get('/events')

@handle_errors(context="Saving event", return_on_error=False)
def save_event(self, event_data):
    """Returns False if error occurs"""
    api_client.post('/events', event_data)
    return True
```

### Error Types Handled

| Error Type | Handler | User Message |
|------------|---------|--------------|
| HTTP 400 | `handle_api_error()` | "Invalid request. Please check your input." |
| HTTP 401 | `handle_api_error()` | "Authentication failed. Please log in again." + Session expired |
| HTTP 403 | `handle_api_error()` | "Access denied. You don't have permission." |
| HTTP 404 | `handle_api_error()` | "The requested resource was not found." |
| HTTP 500 | `handle_api_error()` | "Server error occurred. Please try again later." |
| ConnectionError | `handle_network_error()` | "Cannot connect to server. Check your connection." |
| Timeout | `handle_api_error()` | "Request timed out. Please try again." |
| ValidationError | `handle_validation_error()` | Custom message + widget highlight |

### Methods

**Error Handling:**
- `handle_api_error(error, context)` - Handle HTTP/API errors
- `handle_validation_error(field, message, widget)` - Handle form validation with widget highlighting
- `handle_network_error()` - Handle connection errors
- `handle_session_expired()` - Handle expired sessions (logout + redirect)
- `handle_authorization_error(required_role, user_role)` - Handle permission errors
- `handle_exception(error, context, show_details)` - Generic exception handler

**Logging:**
- `log_error(error, context)` - Log error to file with traceback

**Callbacks:**
- `set_toast_callback(callback)` - Set toast notification callback
- `set_logout_callback(callback)` - Set logout callback
- `set_login_redirect_callback(callback)` - Set login redirect callback

**Utility:**
- `get_log_file_path()` - Get path to error.log
- `clear_log_file()` - Clear error log

### Integration Example

```python
# main.py

from utils.error_handler import setup_error_handling
from components.custom_widgets import Toast

class CampusEventApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        # Setup error handler FIRST
        self.setup_error_handler()
        self.setup_ui()
    
    def setup_error_handler(self):
        """Setup error handler with callbacks"""
        
        def show_toast(message, toast_type):
            Toast(self, message, toast_type).show()
        
        def logout():
            SessionManager().clear_session()
            self.clear_user_data()
        
        def redirect_to_login():
            self.show_page('login')
        
        self.error_handler = setup_error_handling(
            toast_callback=show_toast,
            logout_callback=logout,
            login_redirect_callback=redirect_to_login
        )
```

### Service Layer Example

```python
from utils.error_handler import handle_errors, require_role

class EventService:
    
    @handle_errors(context="Loading events", return_on_error=[])
    def get_events(self):
        """Automatically handles errors, returns [] on failure"""
        return api_client.get('/events')
    
    @require_role('ADMIN', 'ORGANIZER')
    @handle_errors(context="Creating event", return_on_error=None)
    def create_event(self, event_data):
        """Only ADMIN/ORGANIZER can create, handles errors automatically"""
        return api_client.post('/events', event_data)
```

### Best Practices

1. **Setup error handler early** - Before any UI or API calls
2. **Always provide context** - Makes debugging easier
3. **Use decorators for access control** - Cleaner than manual checks
4. **Highlight widgets on validation errors** - Better UX
5. **Log all errors** - Even if handled gracefully
6. **Use appropriate error types** - ValidationError, AuthenticationError, etc.
7. **Clear logs periodically** - Prevent file from growing too large

### Documentation

- **Full Documentation:** `utils/ERROR_HANDLER_README.md`
- **Examples:** `utils/error_handler_examples.py`
- **Error Log:** `logs/error.log`

---

## �📚 Additional Resources

- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [tkcalendar Documentation](https://tkcalendar.readthedocs.io/)

## 📄 License

[Your License Here]

## 👥 Contributors

[Your Contributors Here]

---

**Version**: 1.0.0  
**Last Updated**: October 2025  
**Python Version**: 3.8+

For questions or issues, please contact [your-email@example.com]
