"""
Reusable UI Components Package

This package contains reusable components that can be used across multiple pages.

Available Components:
--------------------
- SearchComponent: Advanced search widget with filters, debouncing, and callbacks
- CalendarView: Interactive calendar with month/week/day views and event markers
- StyledButton: Custom button with variants (primary, secondary, success, danger, ghost)
- StyledEntry: Enhanced text entry with icons, validation, and states
- StyledCard: Card widget with shadow effects and hover states
- ProgressBar: Animated progress bar with percentage display
- Toast: Toast notification system with success/error/info/warning types
- Theme: Centralized color palette for consistent styling

Usage:
------
from components import (
    SearchComponent, CalendarView,
    StyledButton, StyledEntry, StyledCard, ProgressBar, Toast, Theme
)

SearchComponent Example:
-----------------------
config = {
    'categories': ['Type1', 'Type2'],
    'statuses': ['Active', 'Inactive'],
    'sort_options': ['Name', 'Date'],
    'placeholder': 'Search...'
}

search = SearchComponent(
    parent_frame,
    on_search_callback=handle_search,
    config=config
)
search.pack(fill='x')

CalendarView Example:
--------------------
def on_date_click(date, items):
    print(f"Clicked: {date}, Items: {len(items)}")

calendar = CalendarView(
    parent_frame,
    on_date_click_callback=on_date_click,
    events=events_list,
    bookings=bookings_list,
    view_mode='month',
    show_controls=True
)
calendar.pack(fill='both', expand=True)

StyledButton Example:
--------------------
button = StyledButton(
    parent,
    text="Save Changes",
    variant="primary",
    command=save_handler
)
button.pack(pady=10)

# Loading state
button.set_loading(True)

StyledEntry Example:
-------------------
entry = StyledEntry(
    parent,
    placeholder="Enter email",
    icon_left="📧",
    clear_button=True
)
entry.pack(fill='x', pady=5)

# Error state
entry.set_error("Invalid email format")

# Get value
email = entry.get()

StyledCard Example:
------------------
card = StyledCard(parent, padding=20, hover=True)
card.pack(pady=10, padx=20)

# Add content to card
tk.Label(card.content_frame, text="Card Title").pack()

ProgressBar Example:
-------------------
progress = ProgressBar(parent, width=300, fg_color=Theme.SUCCESS)
progress.pack(pady=10)
progress.set_progress(75)

Toast Example:
-------------
Toast.show(root, "Operation successful!", type="success")
Toast.show(root, "An error occurred", type="error", duration=5000)

For detailed examples, see:
- components/search_component_examples.py
- components/calendar_view_examples.py
- components/custom_widgets_examples.py

For full documentation, see: README.md
"""

from .search_component import SearchComponent
from .calendar_view import CalendarView
from .custom_widgets import (
    StyledButton,
    StyledEntry,
    StyledCard,
    ProgressBar,
    Toast,
    Theme,
    show_loading_dialog
)

__all__ = [
    'SearchComponent',
    'CalendarView',
    'StyledButton',
    'StyledEntry',
    'StyledCard',
    'ProgressBar',
    'Toast',
    'Theme',
    'show_loading_dialog'
]

__version__ = '1.4.0'
__author__ = 'Campus Event System Team'
