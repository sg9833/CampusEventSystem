# Changelog

All notable changes to the Campus Event System Frontend will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2025-10-09

### Added - Error Handler & Exception Management System

#### ErrorHandler Class (`utils/error_handler.py`)
- **Comprehensive Error Handling System**
  - **Features**:
    * Singleton pattern for global access
    * Automatic error logging to `logs/error.log`
    * User-friendly error messages
    * Toast notification integration
    * Widget highlighting for validation errors
    * Session expiration handling
    * Context-aware error messages
    * Comprehensive logging with traceback
  
  - **Error Handling Methods**:
    * `handle_api_error(error, context)` - Parse HTTP errors, show user-friendly messages
      - Maps status codes (400, 401, 403, 404, 500, etc.) to readable messages
      - Automatically triggers session expiration on 401
      - Handles connection errors, timeouts, invalid responses
    
    * `handle_validation_error(field, message, widget)` - Highlight field, show error
      - Highlights widget with red background
      - Sets focus to invalid field
      - Auto-restores original style after 3 seconds
      - Shows toast notification with error message
    
    * `handle_network_error()` - "Check internet connection" message
      - Shows detailed checklist (connection, server, firewall)
      - Toast notification + detailed messagebox
    
    * `handle_session_expired()` - Logout user, redirect to login
      - Calls logout callback to clear session
      - Calls login redirect callback to navigate
      - Shows user-friendly expiration message
    
    * `handle_authorization_error(required_role, user_role)` - Handle permission errors
      - Shows required vs current role
      - User-friendly access denied message
    
    * `log_error(error, context)` - Write to error.log file
      - Includes error type, message, context
      - Full traceback for debugging
      - Timestamp for each error
      - Formatted with separators
  
  - **Callback Registration**:
    * `set_toast_callback(callback)` - Function to show toast notifications
    * `set_logout_callback(callback)` - Function to logout user
    * `set_login_redirect_callback(callback)` - Function to redirect to login
  
  - **Utility Methods**:
    * `get_log_file_path()` - Get path to error.log
    * `clear_log_file()` - Clear error log file

#### Custom Exception Types
- **ValidationError** - Form validation failures
  ```python
  raise ValidationError(field="email", message="Invalid format")
  ```
  - Attributes: `field`, `message`
  - Automatically handled by ErrorHandler

- **AuthenticationError** - User not logged in
  ```python
  raise AuthenticationError("User must be logged in")
  ```
  - Triggers session expired handling

- **AuthorizationError** - Insufficient permissions
  ```python
  raise AuthorizationError(required_role='ADMIN', user_role='STUDENT')
  ```
  - Attributes: `required_role`, `user_role`
  - Shows access denied message

- **SessionExpiredError** - Session has expired
  ```python
  raise SessionExpiredError("Token expired")
  ```
  - Triggers logout and redirect

#### Decorators

- **@require_login** - Check if user logged in
  ```python
  @require_login
  def view_dashboard(self):
      # Only executes if user is logged in
      pass
  ```
  - Checks `SessionManager().is_logged_in()`
  - Calls `handle_session_expired()` if not logged in
  - Raises `AuthenticationError`

- **@require_role(*roles)** - Check user role
  ```python
  @require_role('ADMIN')
  def delete_user(self, user_id):
      # Only ADMIN can execute
      pass
  
  @require_role('ADMIN', 'ORGANIZER')
  def create_event(self):
      # ADMIN or ORGANIZER can execute
      pass
  ```
  - Checks if user is logged in first
  - Verifies user role matches allowed roles
  - Calls `handle_authorization_error()` if role doesn't match
  - Raises `AuthorizationError`

- **@handle_errors** - Wrap function with error handling
  ```python
  @handle_errors(context="Loading events", return_on_error=[])
  def load_events(self):
      # Any error automatically handled
      return api_client.get('/events')
  
  @handle_errors(
      context="Saving event",
      show_toast=True,
      show_details=False,
      return_on_error=False
  )
  def save_event(self, event_data):
      api_client.post('/events', event_data)
      return True
  ```
  - Parameters:
    * `context` - Description for logging
    * `show_toast` - Show notification (default: True)
    * `show_details` - Show technical details (default: False)
    * `return_on_error` - Value to return on error (default: None)
  - Catches all exceptions
  - Routes to appropriate handler
  - Returns default value on error

#### Convenience Functions

- **get_error_handler()** - Get singleton instance
  ```python
  handler = get_error_handler()
  ```

- **setup_error_handling(callbacks)** - Setup with callbacks
  ```python
  error_handler = setup_error_handling(
      toast_callback=show_toast,
      logout_callback=logout,
      login_redirect_callback=redirect_to_login
  )
  ```

#### Error Type Handling

| Exception Type | Handler Method | User Message |
|----------------|----------------|--------------|
| `requests.HTTPError` | `handle_api_error()` | Status-specific messages |
| `requests.ConnectionError` | `handle_network_error()` | "Check internet connection" |
| `requests.Timeout` | `handle_api_error()` | "Request timed out" |
| `ValueError` | `handle_api_error()` | "Invalid response from server" |
| `ValidationError` | `handle_validation_error()` | Custom message |
| `AuthenticationError` | `handle_session_expired()` | "Session expired" |
| `AuthorizationError` | `handle_authorization_error()` | "Access denied" |
| `SessionExpiredError` | `handle_session_expired()` | "Please log in again" |

#### HTTP Status Code Messages

| Status | Message |
|--------|---------|
| 400 | "Invalid request. Please check your input and try again." |
| 401 | "Authentication failed. Please log in again." + Session expiration |
| 403 | "Access denied. You don't have permission to perform this action." |
| 404 | "The requested resource was not found." |
| 409 | "A conflict occurred. The resource may already exist." |
| 422 | "Validation failed. Please check your input." |
| 500 | "Server error occurred. Please try again later." |
| 502 | "Bad gateway. The server is temporarily unavailable." |
| 503 | "Service unavailable. Please try again later." |
| 504 | "Gateway timeout. The request took too long." |

#### Documentation & Examples

- **Full Documentation**: `utils/ERROR_HANDLER_README.md` (comprehensive guide)
  - Overview and features
  - Installation instructions
  - Quick start guide
  - Detailed API documentation
  - Custom exceptions guide
  - Decorator usage
  - Error type handling
  - Integration guide
  - Best practices
  - Troubleshooting

- **Examples Application**: `utils/error_handler_examples.py` (interactive demo)
  - Example 1: Basic error handling
  - Example 2: Using decorators
  - Example 3: Custom error types
  - Example 4: API error scenarios
  - Example 5: GUI integration with 4 tabs
    * API errors simulation
    * Validation demo
    * Authentication demo
    * Decorators demo

#### Integration Benefits

1. **Consistent Error Handling** - Same approach across all modules
2. **Better UX** - User-friendly messages instead of technical errors
3. **Easier Debugging** - Comprehensive logs with context
4. **Automatic Session Management** - Handles expired sessions gracefully
5. **Access Control** - Simple decorators for authentication/authorization
6. **Reduced Boilerplate** - Less try-except blocks needed
7. **Widget Highlighting** - Visual feedback for validation errors
8. **Production Ready** - Proper error logging and monitoring

---

## [1.5.0] - 2025-10-09

### Added - Assets & Image Management System

#### Image Loader Utility (`utils/image_loader.py`)
- **ImageLoader Class** - Centralized image loading and caching system
  - **Features**:
    * Singleton pattern for global access
    * Automatic image caching for performance optimization
    * Automatic resizing to specified dimensions
    * Placeholder generation for missing images
    * Support for PNG, JPG, GIF formats
    * Thread-safe caching mechanism
  
  - **Loading Methods**:
    * `load_image(filename, size, folder)` - Load any image with caching
    * `load_icon(icon_name, size)` - Load application icons
    * `load_logo(size)` - Load application logo
    * `load_event_image(filename, size)` - Load event images with fallback
    * `load_resource_image(filename, size)` - Load resource images with fallback
    * `load_user_avatar(filename, size)` - Load user avatars with fallback
  
  - **Cache Management**:
    * `get_cache_size()` - Get number of cached images
    * `clear_cache()` - Clear all cached images
    * `remove_from_cache(filename, size)` - Remove specific image
    * `preload_icons(icon_names, size)` - Preload icons for performance
  
  - **Placeholder Generation**:
    * Automatically generates colored placeholders for missing images
    * Event placeholder: Blue background with calendar icon
    * Resource placeholder: Green background with building icon
    * Avatar placeholder: Purple background with person icon
    * Icon placeholders: Colored circles with first letter

- **IconSet Class** - Unicode emoji icon set for fallback
  - **Categories**:
    * Navigation: Dashboard 🏠, Events 📅, Resources 🏢, Bookings 📋, etc.
    * Actions: Search 🔍, Add ➕, Edit ✏️, Delete 🗑️, Approve ✅, Reject ❌
    * Status: Success ✓, Error ✕, Warning ⚠, Info ℹ, Pending ⏳
    * Content: Email 📧, Phone 📞, Location 📍, Calendar 📅, Clock 🕐
    * Categories: Academic 📚, Sports ⚽, Cultural 🎭, Workshop 🔧
    * UI: Menu ☰, Close ✕, Back ◀, Forward ▶, More ⋯
  
  - **Helper Methods**:
    * `get_category_icon(category)` - Get icon for event category
    * `get_status_icon(status)` - Get icon for status
  
  - **Usage**: Instant icon display without image files
    ```python
    label = tk.Label(parent, text=f"{IconSet.DASHBOARD} Dashboard")
    ```

- **Convenience Functions**:
  * `get_image_loader()` - Get singleton ImageLoader instance
  * `load_image(filename, size)` - Quick image loading
  * `load_icon(icon_name, size)` - Quick icon loading
  * `load_logo(size)` - Quick logo loading

#### Assets Directory Structure
- **assets/icons/** - Application icons (48x48 PNG)
  * 14 generated icon files:
    - Navigation: dashboard, events, resources, bookings, profile, settings, notifications, logout
    - Actions: search, add, edit, delete, approve, reject
  * Colored placeholder icons with themed colors
  * First letter overlays for identification

- **assets/images/** - General images and placeholders
  * **logo.png** (400x200) - Application logo with gradient
    - Blue gradient background
    - Building and calendar icons
    - "Campus Event Management System" text
  * **event_placeholder.png** (600x400) - Default event image
    - Blue background with "EVENT" text
    - Calendar icon representation
  * **resource_placeholder.png** (600x400) - Default resource image
    - Green background with "RESOURCE" text
    - Building icon with windows
  * **avatar_placeholder.png** (200x200) - Default user avatar
    - Purple background
    - Simple person icon

#### Asset Generator (`utils/generate_assets.py`)
- **Script to create all placeholder assets**
  - `create_logo(output_path, size)` - Generate app logo
    * Gradient blue background (3 shades)
    * Building icon (campus representation)
    * Calendar icon (events representation)
    * Title and subtitle text
  
  - `create_icon_placeholders(icons_path)` - Generate 14 icon files
    * Colored circles with theme colors
    * First letter of icon name in center
    * 48x48 PNG with transparency
  
  - `create_placeholder_images(images_path)` - Generate placeholders
    * Event placeholder with calendar design
    * Resource placeholder with building design
    * Avatar placeholder with person design
  
  - **Run**: `python3 utils/generate_assets.py`
  - Creates all assets automatically with proper colors and designs

#### Documentation
- **assets/README.md** - Complete assets documentation
  * Directory structure overview
  * Icon set specifications
  * Usage examples for all image types
  * Image specifications and formats
  * File naming conventions
  * Best practices
  * Troubleshooting guide

- **utils/image_loader_examples.py** - Interactive demo application
  * Tab 1: Logo display at multiple sizes
  * Tab 2: Icon gallery (all 14 PNG icons)
  * Tab 3: Event image loading and placeholders
  * Tab 4: Resource image loading and placeholders
  * Tab 5: User avatar loading and placeholders
  * Tab 6: Unicode IconSet showcase with all categories
  * Tab 7: Cache information and management
  * Runnable Tkinter application for testing

- **README.md** - Updated with Assets & Icons section
  * ImageLoader class documentation
  * IconSet class documentation
  * Asset directory structure
  * Icon specifications table
  * Usage examples
  * Best practices
  * Integration examples

#### Icon Color Scheme
All icons follow application theme colors:
- Dashboard: Blue (#3498DB)
- Events: Red (#E74C3C)
- Resources: Green (#27AE60)
- Bookings: Orange (#F39C12)
- Profile: Purple (#9B59B6)
- Settings: Gray (#95A5A6)
- Notifications: Pink (#E91E63)
- Search: Light Green (#2ECC71)
- Add: Teal (#16A085)
- Edit: Blue (#2980B9)
- Delete: Dark Red (#C0392B)
- Approve: Green (#27AE60)
- Reject: Red (#E74C3C)
- Logout: Gray (#7F8C8D)

#### Integration Benefits
- **Performance**: Image caching eliminates redundant file I/O
- **Memory Efficiency**: Smart cache management with size tracking
- **Fallback Support**: Automatic placeholders for missing images
- **Consistent Styling**: Themed colors across all icons
- **Easy Usage**: Simple API with convenience functions
- **Flexible**: PNG files + Unicode emoji fallback
- **Scalable**: Automatic resizing to any dimension

### Changed
- Updated `README.md` with comprehensive Assets & Icons section
- Enhanced documentation with image loading examples

## [1.4.0] - 2025-10-09

### Added - Custom Styled Widgets Library

#### New Styled Widget Components
- **StyledButton** (`components/custom_widgets.py`)
  - **Variants**:
    * Primary - Blue button for main actions
    * Secondary - Gray button for secondary actions
    * Success - Green button for positive actions
    * Danger - Red button for destructive actions
    * Ghost - Transparent button with border outline
  - **States**:
    * Normal - Default interactive state
    * Hover - Smooth color transition on mouse over
    * Loading - Animated spinner with disabled interaction
    * Disabled - Grayed out non-interactive state
  - **Methods**:
    * `set_loading(bool)` - Show/hide loading spinner
    * `set_disabled(bool)` - Enable/disable button
    * `set_text(str)` - Update button text dynamically
  - **Features**:
    * Rounded corners
    * Smooth hover animations
    * Configurable width and height
    * Custom command callbacks

- **StyledEntry** (`components/custom_widgets.py`)
  - **Features**:
    * Left/right icon support (emojis or symbols)
    * Placeholder text (auto-show/hide)
    * Error state with red border and message
    * Success state with green border
    * Optional clear button (appears when typing)
    * Password visibility toggle
    * Focus border highlighting
  - **Methods**:
    * `get()` - Get entry value
    * `set(value)` - Set entry value
    * `clear()` - Clear entry and show placeholder
    * `set_error(message)` - Show error with message below
    * `set_success()` - Show success state
    * `clear_state()` - Remove error/success state
    * `focus()` - Set focus to entry
  - **Use Cases**:
    * Text input with validation
    * Email/password fields
    * Search bars with icons
    * Form fields with real-time validation

- **StyledCard** (`components/custom_widgets.py`)
  - **Features**:
    * Elevated shadow effect for depth
    * Hover state with enhanced shadow
    * Rounded corners (simulated)
    * Customizable internal padding
    * Optional click handler
    * Auto-binding events to all children
  - **Styling**:
    * Default: Subtle shadow (2px)
    * Hover: Enhanced shadow (3px)
    * Smooth shadow transitions
  - **Usage**:
    * Event/resource cards
    * User profile displays
    * Statistics panels
    * Content containers
  - **Parameters**:
    * `padding` - Internal padding (default: 15px)
    * `hover` - Enable hover effect (default: True)
    * `click_handler` - Optional click callback

- **ProgressBar** (`components/custom_widgets.py`)
  - **Features**:
    * Animated progress transitions
    * Percentage label overlay
    * Customizable colors
    * Rounded progress bar
    * Smooth 30ms frame animations
  - **Methods**:
    * `set_progress(value)` - Set progress 0-100 with animation
    * `set_color(color)` - Change foreground color
    * `reset()` - Reset to 0%
  - **Use Cases**:
    * File upload progress
    * Task completion tracking
    * Loading indicators
    * Form completion percentage

- **Toast Notification System** (`components/custom_widgets.py`)
  - **Types**:
    * Success (green, ✓ icon)
    * Error (red, ✕ icon)
    * Info (blue, ℹ icon)
    * Warning (orange, ⚠ icon)
  - **Features**:
    * Auto-dismiss after 3 seconds (configurable)
    * Slide-in animation from top
    * Fade-out animation on dismiss
    * Multiple toasts stack vertically
    * Click X button to dismiss manually
    * Always on top
    * Transparent background (95% opacity)
  - **Usage**:
    ```python
    Toast.show(root, "Success!", type="success", duration=3000)
    ```

- **Theme Class** (`components/custom_widgets.py`)
  - Centralized color palette for consistent styling
  - **Color Categories**:
    * Primary colors (blue shades)
    * Secondary colors (gray shades)
    * Success colors (green shades)
    * Danger colors (red shades)
    * Warning colors (orange shades)
    * Info colors (blue shades)
    * Text colors (dark, light, muted, placeholder)
    * Background colors (white, light, dark, card)
    * Border colors (light, error, success, focus)
    * Shadow colors (default, hover)
  - All colors have normal, hover, and active states
  - Easy to customize for different themes

#### Utility Functions
- **show_loading_dialog()** - Modal loading dialog with spinner
  - Blocks user interaction
  - Centered on parent window
  - Animated spinner
  - Custom message support

#### Documentation
- **custom_widgets_examples.py** - Comprehensive interactive demo:
  * Tab 1: Button variants and states
  * Tab 2: Text entries with icons and validation
  * Tab 3: Card layouts and interactions
  * Tab 4: Progress bar animations
  * Tab 5: Toast notifications
  * Tab 6: Complete form example with all widgets
  * Each tab includes multiple practical examples
  * Runnable demo application

- **README.md** - Updated with Custom Styled Widgets section:
  * Overview of all 5 widget types
  * Detailed usage examples for each widget
  * Configuration tables
  * Methods documentation
  * Complete form integration example
  * Theme colors reference
  * Utility functions documentation

- **components/__init__.py** - Updated to export all widgets:
  * Added imports for all custom widgets
  * Updated __all__ list
  * Enhanced package documentation
  * Version bumped to 1.4.0

#### Integration Potential
- **All Pages** - Consistent button styling across application
- **Forms** - Enhanced text entries with validation
- **Dashboard** - Cards for statistics and information display
- **File Uploads** - Progress bars for upload tracking
- **Notifications** - System-wide toast notifications
- **Login/Register** - Styled forms with validation feedback
- **Profile Pages** - Card-based layouts
- **Admin Pages** - Consistent styling and feedback

#### Technical Details
- Pure Tkinter implementation (no external widget libraries)
- Canvas-based rendering for custom shapes and animations
- Event binding propagation for card interactivity
- Smooth animations using `after()` scheduling
- Rounded corners using polygon smoothing
- Debounced hover detection
- Toplevel windows for toasts (always on top)
- Math-based spinner rotation calculations
- Fade animations for toasts (platform-dependent alpha support)

### Changed
- Updated `components/__init__.py` to version 1.4.0
- Added custom widgets to `__all__` exports
- Enhanced component package with comprehensive widget library

## [1.3.0] - 2025-10-09

### Added - CalendarView Component

#### New Reusable Component
- **CalendarView** (`components/calendar_view.py`)
  - Interactive calendar widget with multiple view modes
  - **View Modes**:
    * Month View - Grid layout with all dates, event markers
    * Week View - 7-day schedule with hourly time slots (8 AM - 8 PM)
    * Day View - 24-hour detailed breakdown with full event info
  - **Event Markers**:
    * Color-coded dots/bars on dates
    * Event type colors (Academic, Sports, Cultural, Workshop, etc.)
    * Booking status colors (Approved, Pending, Rejected, Cancelled)
    * Up to 3 markers shown, with "+X more" indicator
  - **Interactive Features**:
    * Click date to trigger callback with date and items
    * Hover tooltips showing event/booking preview
    * Previous/Next navigation buttons
    * "Today" button to jump to current date
    * View toggle buttons (Month/Week/Day)
  - **Mini Mode**:
    * Compact mode for dashboard sidebars
    * Shows simple dots for events
    * Reduced padding and font sizes
  - **Customization**:
    * Custom color schemes
    * Show/hide navigation controls
    * Configurable callbacks
  - **Public API**:
    * `update_data(events, bookings)` - Update calendar data
    * `set_date(date)` - Navigate to specific date
    * `set_view(mode)` - Change view mode
    * `get_current_date()` - Get displayed date
    * `get_selected_date()` - Get user-selected date

#### Documentation
- **calendar_view_examples.py** - 11 comprehensive usage examples:
  * Full calendar for events page
  * Mini calendar for dashboard
  * Booking availability calendar
  * Week schedule view
  * Detailed day view
  * Combined events and bookings
  * Dynamic data updates
  * Programmatic navigation
  * Custom color schemes
  * Complete page integration
  * No-controls embedded mode
- **README.md** - Updated with CalendarView section:
  * Features overview
  * Usage examples
  * Configuration options table
  * View modes documentation
  * Color scheme tables
  * Public methods documentation
  * Integration examples (Dashboard, Events, Bookings)
  * Data format specifications
- **components/__init__.py** - Updated to export CalendarView

#### Integration Potential
- **Dashboard** - Mini calendar showing upcoming events
- **Events Page** - Full calendar for browsing events by date
- **Bookings Page** - Week/Day view for checking availability
- **Profile Page** - Personal schedule view
- **Admin Pages** - Overview of all system activities

#### Technical Details
- Built with Python stdlib `calendar` module
- Uses tkinter Canvas for scrollable content
- Tooltip system with 500ms hover delay
- Efficient date parsing with multiple format support
- Grid-based responsive layout
- Event/booking data structure:
  ```python
  # Events
  {
    'title': str,
    'category': str,  # academic, sports, cultural, workshop, etc.
    'start_time': str,  # ISO datetime format
    'venue': str,
    'status': str
  }
  
  # Bookings
  {
    'resource': str,
    'start_time': str,
    'end_time': str,
    'status': str  # approved, pending, rejected, cancelled
  }
  ```

### Changed
- Updated `components/__init__.py` to version 1.3.0
- Added CalendarView to `__all__` exports
- Enhanced component package documentation

## [1.2.0] - 2025-10-09

### Added - SearchComponent & Integration

#### New Reusable Component
- **SearchComponent** (`components/search_component.py`)
  - Advanced search widget with debouncing (500ms)
  - Configurable filter options (categories, statuses, sort)
  - Advanced filters modal with:
    * Date range picker (DateEntry)
    * Category checkboxes (multi-select)
    * Status radio buttons (single-select)
    * Sort dropdown
  - Visual filter tags with remove buttons
  - Search history tracking (last 10 searches)
  - Callback pattern for clean integration
  - Highly customizable via config dict
  - Badge showing active filter count
  - Methods: `get_search_text()`, `get_active_filters()`, `clear_search()`, `reset_all()`

#### Documentation
- **README.md** - Comprehensive documentation:
  * Project overview and features
  * Installation instructions
  * Architecture and design patterns
  * Detailed page descriptions
  * SearchComponent usage guide
  * Configuration examples
  * API integration guide
  * Development guidelines
  * Troubleshooting section
- **search_component_examples.py** - Usage examples:
  * Events page configuration
  * Resources page configuration
  * Users page configuration
  * Bookings page configuration
  * Programmatic control examples
  * Complete integration example with runnable demo

#### Page Integrations
- **browse_events.py** - Integrated SearchComponent
  * Replaced manual search/filter UI with SearchComponent
  * Configured for event-specific filters:
    - Categories: Academic, Sports, Cultural, Workshop, Seminar, Conference, Social
    - Statuses: Upcoming, Active, Past, Approved, Cancelled
    - Sort: Date, Popularity, Name, Attendees
  * Date range filtering for event start times
  * Enhanced search includes organizer names
  * Cleaner header with just title (search moved below)

- **browse_resources.py** - Integrated SearchComponent
  * Added SearchComponent alongside existing sidebar filters
  * Configured for resource-specific filters:
    - Categories: Classroom, Laboratory, Auditorium, Equipment, Conference Room, Sports Facility
    - Statuses: Available, Maintenance, Reserved, Out of Service
    - Sort: Name, Capacity, Location, Type
  * Search includes location and amenities
  * Date range for availability checking
  * Hybrid approach: SearchComponent + sidebar for advanced options

### Changed
- Updated `browse_events.py` imports to include SearchComponent
- Updated `browse_resources.py` imports to include SearchComponent
- Removed redundant filter state variables from browse_events (now handled by SearchComponent)
- Modified header layouts to accommodate SearchComponent placement

### Technical Details
- Filter object structure:
  ```python
  {
      'date_range': {'start': date, 'end': date},
      'categories': ['Cat1', 'Cat2'],  # Multi-select
      'status': 'Active',               # Single-select
      'sort': 'Name'
  }
  ```
- Debouncing prevents API spam during typing
- Thread-safe callback mechanism
- Proper widget cleanup and memory management

## [1.1.0] - 2025-10-08

### Added - Admin & User Features

#### New Pages
- **booking_approvals.py** - Admin booking approval system
  * Pending bookings queue with priority sorting
  * Conflict detection with visual warnings
  * Calendar view with color-coded bookings
  * Approval modal with user booking history
  * Alternative time slot suggestions
  * Bulk approve/reject operations
  * Filter by resource type, date range, status
  * Export booking reports

- **profile_page.py** - User profile management
  * Two-tab interface (View Profile / Account Settings)
  * Profile photo upload with preview and base64 encoding
  * Edit profile modal with validation
  * Password change with strength indicator
  * Email notification preferences
  * Privacy settings (profile visibility)
  * Account activity log

- **manage_users.py** - Admin user management
  * Comprehensive user table (Treeview with 7 columns)
  * Search and filter controls (role, status)
  * User actions:
    - View detailed user profile with activity stats
    - Edit user role (Student/Organizer/Admin)
    - Block/Unblock users
    - Reset password
    - Send email modal
    - Delete user with double confirmation
  * Context menu (right-click) for quick actions
  * CSV export functionality
  * User activity statistics

- **analytics_page.py** - Admin analytics dashboard
  * Overview cards (4): Total Events, Active Users, Total Bookings, Revenue
  * Growth indicators with percentage changes
  * Interactive charts (5):
    - Events by Category (Pie Chart)
    - Monthly Event Registrations (Line Chart)
    - Resource Utilization (Bar Chart)
    - User Growth Over Time (Area Chart)
    - Popular Resources (Horizontal Bar)
  * Date range selector for analytics
  * Export report cards (PDF/Excel options)
  * Embedded matplotlib with TkAgg backend
  * Sample data for demonstration

- **notifications_page.py** - Notification center
  * Grouped notifications (Today/Yesterday/Earlier)
  * 8 notification types with icons:
    - Booking Approved ✅
    - Booking Rejected ❌
    - Event Registration 🎟️
    - Event Reminder ⏰
    - Event Cancelled 🚫
    - Resource Available 📚
    - Profile Update 👤
    - System Announcement 📢
  * Filter buttons (All/Unread/Read)
  * Mark as read/delete actions
  * Action links to related items (events, bookings, etc.)
  * Real-time updates with 30-second polling
  * Timestamp formatting with relative times
  * Empty state handling
  * Badge counts on filter buttons

#### Dependencies
- Added **matplotlib** 3.9.4 for data visualization
- Added **Pillow (PIL)** 11.3.0 for image processing
- Added **tkcalendar** 1.6.1 for date pickers
- Updated `requirements.txt` with new packages

### Enhanced
- **Color scheme** - Consistent across all pages:
  * Primary: #2C3E50 (Dark blue-gray)
  * Secondary: #3498DB (Bright blue)
  * Success: #27AE60 (Green)
  * Warning: #F39C12 (Orange)
  * Danger: #E74C3C (Red)
  * Background: #ECF0F1 (Light gray)

### Technical Improvements
- Threaded API calls for non-blocking operations
- Modal dialogs with proper centering
- Form validation across all pages
- Loading states with progress bars
- Confirmation dialogs for destructive actions
- Error handling with user-friendly messages
- Real-time polling mechanisms
- Debouncing for input fields

## [1.0.0] - 2025-10-01

### Initial Release

#### Core Pages
- **login_page.py** - User authentication
- **register_page.py** - User registration
- **student_dashboard.py** - Student home page
- **browse_events.py** - Event browsing (basic version)
- **browse_resources.py** - Resource browsing (basic version)
- **book_resource.py** - Resource booking form
- **create_event.py** - Event creation form
- **my_events.py** - Organizer's events
- **my_bookings.py** - User's bookings
- **event_approvals.py** - Admin event approvals
- **manage_resources.py** - Admin resource management

#### Core Utilities
- **api_client.py** - REST API communication
- **session_manager.py** - Session and authentication management
- **validators.py** - Form validation utilities
- **config.py** - Application configuration

#### Features
- Role-based access control (Student/Organizer/Admin)
- Event creation and management
- Resource booking system
- Admin approval workflows
- Responsive layouts
- Error handling
- Session management

---

## Legend

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes

---

## Upcoming Features (v1.3.0)

### Planned
- [ ] SearchComponent integration into `manage_users.py`
- [ ] Dark mode theme support
- [ ] Keyboard shortcuts (Ctrl+F for search, etc.)
- [ ] Advanced export options (PDF reports with charts)
- [ ] Offline mode with local caching
- [ ] Multi-language support (i18n)
- [ ] Accessibility improvements (screen reader support)
- [ ] Unit tests for components
- [ ] Integration tests for pages

### Under Consideration
- [ ] WebSocket support for real-time notifications (replace polling)
- [ ] Drag-and-drop resource scheduling
- [ ] Interactive calendar widget for bookings
- [ ] Advanced analytics with custom date ranges
- [ ] Email template editor for notifications
- [ ] Backup and restore functionality
- [ ] Audit log viewer
- [ ] Performance monitoring dashboard

---

**Maintainers**: [Your Name]  
**Repository**: https://github.com/yourusername/CampusEventSystem  
**Documentation**: See README.md for full documentation
