"""
CalendarView Component

A comprehensive calendar widget with month/week/day views, event markers,
tooltips, and interactive navigation.

Features:
- Month/Week/Day view toggle
- Event/booking markers on dates
- Color-coded by type/status
- Click date to see details
- Hover tooltips
- Month navigation
- "Today" button
- Highly configurable

Usage:
------
from components.calendar_view import CalendarView

def on_date_click(date, events):
    print(f"Clicked: {date}")
    print(f"Events: {events}")

calendar = CalendarView(
    parent_frame,
    on_date_click_callback=on_date_click,
    events=events_list,
    bookings=bookings_list,
    colors=color_scheme
)
calendar.pack(fill='both', expand=True)
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import calendar
from typing import List, Dict, Callable, Optional, Any


class CalendarView(tk.Frame):
    """
    Comprehensive calendar component with multiple views and event markers.
    
    Supports month, week, and day views with interactive event/booking display.
    """
    
    def __init__(
        self,
        parent,
        on_date_click_callback: Optional[Callable] = None,
        events: Optional[List[Dict[str, Any]]] = None,
        bookings: Optional[List[Dict[str, Any]]] = None,
        view_mode: str = 'month',  # 'month', 'week', 'day'
        colors: Optional[Dict[str, str]] = None,
        show_controls: bool = True,
        mini_mode: bool = False,
        **kwargs
    ):
        """
        Initialize CalendarView.
        
        Args:
            parent: Parent widget
            on_date_click_callback: Callback function(date, items) when date is clicked
            events: List of event dicts with 'start_time', 'title', 'type', etc.
            bookings: List of booking dicts with 'start_time', 'resource', 'status', etc.
            view_mode: Initial view mode ('month', 'week', 'day')
            colors: Color scheme dict
            show_controls: Show navigation controls
            mini_mode: Compact mode for dashboards
        """
        super().__init__(parent, **kwargs)
        
        # Data
        self.events = events or []
        self.bookings = bookings or []
        self.on_date_click_callback = on_date_click_callback
        
        # State
        self.view_mode = view_mode
        self.current_date = datetime.now()
        self.selected_date = None
        self.mini_mode = mini_mode
        self.show_controls = show_controls
        
        # Colors
        self.colors = colors or {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'background': '#ECF0F1'
        }
        
        # Event type colors
        self.event_colors = {
            'academic': '#3498DB',
            'sports': '#27AE60',
            'cultural': '#9B59B6',
            'workshop': '#F39C12',
            'seminar': '#E74C3C',
            'conference': '#1ABC9C',
            'social': '#E91E63',
            'default': '#95A5A6'
        }
        
        # Booking status colors
        self.booking_colors = {
            'approved': '#27AE60',
            'pending': '#F39C12',
            'rejected': '#E74C3C',
            'cancelled': '#95A5A6',
            'active': '#3498DB',
            'default': '#95A5A6'
        }
        
        # Tooltip
        self.tooltip = None
        self.tooltip_timer = None
        
        # Build UI
        self.configure(bg='white')
        self._build_ui()
        self._render_calendar()
    
    def _build_ui(self):
        """Build the calendar UI"""
        # Main container
        self.grid_rowconfigure(0, weight=0 if self.show_controls else 0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Controls (header)
        if self.show_controls:
            self._build_controls()
        
        # Calendar display area (scrollable for week/day views)
        calendar_container = tk.Frame(self, bg='white')
        calendar_container.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        
        canvas = tk.Canvas(calendar_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(calendar_container, orient='vertical', command=canvas.yview)
        
        self.calendar_frame = tk.Frame(canvas, bg='white')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=self.calendar_frame, anchor='nw')
        self.calendar_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Update canvas width on resize
        def on_canvas_configure(event):
            canvas_width = event.width
            canvas.itemconfig(canvas.find_withtag('all')[0] if canvas.find_withtag('all') else 1, width=canvas_width)
        canvas.bind('<Configure>', on_canvas_configure)
    
    def _build_controls(self):
        """Build calendar controls (navigation, view toggle, etc.)"""
        controls = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        controls.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 0))
        
        controls_content = tk.Frame(controls, bg='white')
        controls_content.pack(fill='x', padx=15, pady=10)
        
        # Navigation controls (left)
        nav_frame = tk.Frame(controls_content, bg='white')
        nav_frame.pack(side='left')
        
        # Previous button
        tk.Button(
            nav_frame,
            text='◀',
            command=self._prev_period,
            bg='#F3F4F6',
            fg='#374151',
            relief='flat',
            font=('Helvetica', 12, 'bold'),
            padx=12,
            pady=4,
            cursor='hand2'
        ).pack(side='left', padx=(0, 8))
        
        # Current period label
        self.period_label = tk.Label(
            nav_frame,
            text=self._get_period_label(),
            bg='white',
            fg=self.colors.get('primary', '#2C3E50'),
            font=('Helvetica', 14, 'bold')
        )
        self.period_label.pack(side='left', padx=8)
        
        # Next button
        tk.Button(
            nav_frame,
            text='▶',
            command=self._next_period,
            bg='#F3F4F6',
            fg='#374151',
            relief='flat',
            font=('Helvetica', 12, 'bold'),
            padx=12,
            pady=4,
            cursor='hand2'
        ).pack(side='left', padx=(8, 0))
        
        # View toggle and actions (right)
        actions_frame = tk.Frame(controls_content, bg='white')
        actions_frame.pack(side='right')
        
        if not self.mini_mode:
            # View toggle buttons
            view_frame = tk.Frame(actions_frame, bg='white')
            view_frame.pack(side='left', padx=(0, 12))
            
            for view in ['month', 'week', 'day']:
                btn_bg = self.colors.get('secondary', '#3498DB') if view == self.view_mode else '#F3F4F6'
                btn_fg = 'white' if view == self.view_mode else '#374151'
                
                btn = tk.Button(
                    view_frame,
                    text=view.capitalize(),
                    command=lambda v=view: self._change_view(v),
                    bg=btn_bg,
                    fg=btn_fg,
                    relief='flat',
                    font=('Helvetica', 9, 'bold'),
                    padx=12,
                    pady=4,
                    cursor='hand2'
                )
                btn.pack(side='left', padx=2)
        
        # Today button
        tk.Button(
            actions_frame,
            text='📅 Today',
            command=self._go_to_today,
            bg=self.colors.get('success', '#27AE60'),
            fg='white',
            relief='flat',
            font=('Helvetica', 9, 'bold'),
            padx=12,
            pady=6,
            cursor='hand2'
        ).pack(side='left')
    
    def _render_calendar(self):
        """Render the calendar based on current view mode"""
        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        if self.view_mode == 'month':
            self._render_month_view()
        elif self.view_mode == 'week':
            self._render_week_view()
        elif self.view_mode == 'day':
            self._render_day_view()
        
        # Update period label if controls are shown
        if self.show_controls:
            self.period_label.config(text=self._get_period_label())
    
    def _render_month_view(self):
        """Render month view with grid of dates"""
        year = self.current_date.year
        month = self.current_date.month
        
        # Get calendar data
        cal = calendar.monthcalendar(year, month)
        
        # Configure grid
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1, uniform='col')
        
        # Day headers (Sun-Sat)
        day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] if not self.mini_mode else ['S', 'M', 'T', 'W', 'T', 'F', 'S']
        
        for col, day_name in enumerate(day_names):
            header = tk.Label(
                self.calendar_frame,
                text=day_name,
                bg='#F9FAFB',
                fg='#6B7280',
                font=('Helvetica', 10 if not self.mini_mode else 8, 'bold'),
                pady=8 if not self.mini_mode else 4
            )
            header.grid(row=0, column=col, sticky='ew')
        
        # Date cells
        today = datetime.now().date()
        
        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                if day == 0:
                    # Empty cell for days outside current month
                    cell = tk.Frame(self.calendar_frame, bg='white', highlightthickness=1, highlightbackground='#F3F4F6')
                    cell.grid(row=week_idx + 1, column=day_idx, sticky='nsew', padx=1, pady=1)
                else:
                    # Create date cell
                    date = datetime(year, month, day).date()
                    is_today = date == today
                    is_selected = self.selected_date and date == self.selected_date
                    
                    cell = self._create_date_cell(date, is_today, is_selected)
                    cell.grid(row=week_idx + 1, column=day_idx, sticky='nsew', padx=1, pady=1)
    
    def _create_date_cell(self, date, is_today=False, is_selected=False):
        """Create a date cell with event markers"""
        # Cell frame
        if is_selected:
            bg_color = '#E3F2FD'
            border_color = self.colors.get('secondary', '#3498DB')
        elif is_today:
            bg_color = '#FFF9E6'
            border_color = self.colors.get('warning', '#F39C12')
        else:
            bg_color = 'white'
            border_color = '#E5E7EB'
        
        cell = tk.Frame(
            self.calendar_frame,
            bg=bg_color,
            highlightthickness=2 if (is_today or is_selected) else 1,
            highlightbackground=border_color,
            cursor='hand2'
        )
        
        # Get events and bookings for this date
        date_events = self._get_items_for_date(date, 'events')
        date_bookings = self._get_items_for_date(date, 'bookings')
        all_items = date_events + date_bookings
        
        # Date label
        date_label = tk.Label(
            cell,
            text=str(date.day),
            bg=bg_color,
            fg=self.colors.get('primary', '#2C3E50') if not is_today else self.colors.get('warning', '#F39C12'),
            font=('Helvetica', 12 if not self.mini_mode else 10, 'bold' if is_today else 'normal'),
            anchor='nw'
        )
        date_label.pack(anchor='nw', padx=8 if not self.mini_mode else 4, pady=6 if not self.mini_mode else 3)
        
        # Event/booking markers
        if all_items and not self.mini_mode:
            markers_frame = tk.Frame(cell, bg=bg_color)
            markers_frame.pack(fill='x', padx=4, pady=(0, 4))
            
            # Show up to 3 markers
            for item in all_items[:3]:
                marker_color = self._get_item_color(item)
                marker = tk.Frame(
                    markers_frame,
                    bg=marker_color,
                    height=4,
                    width=0
                )
                marker.pack(side='left', fill='x', expand=True, padx=1)
            
            # Count indicator if more than 3
            if len(all_items) > 3:
                count_label = tk.Label(
                    cell,
                    text=f'+{len(all_items) - 3} more',
                    bg=bg_color,
                    fg='#6B7280',
                    font=('Helvetica', 7)
                )
                count_label.pack(anchor='w', padx=4, pady=(0, 4))
        elif all_items and self.mini_mode:
            # Just show a dot in mini mode
            dot = tk.Label(
                cell,
                text='●',
                bg=bg_color,
                fg=self.colors.get('secondary', '#3498DB'),
                font=('Helvetica', 8)
            )
            dot.pack(anchor='center')
        
        # Bind click event
        cell.bind('<Button-1>', lambda e: self._on_date_click(date, all_items))
        date_label.bind('<Button-1>', lambda e: self._on_date_click(date, all_items))
        
        # Bind hover events for tooltip
        if all_items and not self.mini_mode:
            cell.bind('<Enter>', lambda e: self._show_tooltip(e, date, all_items))
            cell.bind('<Leave>', lambda e: self._hide_tooltip())
        
        return cell
    
    def _render_week_view(self):
        """Render week view with time slots"""
        # Get start of week (Sunday)
        start_of_week = self.current_date - timedelta(days=self.current_date.weekday() + 1)
        if start_of_week.weekday() != 6:  # If not Sunday
            start_of_week = start_of_week - timedelta(days=start_of_week.weekday() + 1)
        
        # Configure grid
        for i in range(8):  # Time column + 7 days
            self.calendar_frame.grid_columnconfigure(i, weight=1 if i > 0 else 0, uniform='col' if i > 0 else None)
        
        # Header row with dates
        tk.Label(
            self.calendar_frame,
            text='Time',
            bg='#F9FAFB',
            fg='#6B7280',
            font=('Helvetica', 9, 'bold'),
            width=8
        ).grid(row=0, column=0, sticky='ew', padx=1, pady=1)
        
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            is_today = date.date() == datetime.now().date()
            
            header_bg = '#FFF9E6' if is_today else '#F9FAFB'
            header_text = f"{date.strftime('%a')}\n{date.strftime('%d')}"
            
            header = tk.Label(
                self.calendar_frame,
                text=header_text,
                bg=header_bg,
                fg=self.colors.get('warning', '#F39C12') if is_today else '#6B7280',
                font=('Helvetica', 10, 'bold' if is_today else 'normal'),
                pady=8
            )
            header.grid(row=0, column=i + 1, sticky='ew', padx=1, pady=1)
        
        # Time slots (8 AM to 8 PM in 1-hour intervals)
        for hour in range(8, 21):
            time_label = tk.Label(
                self.calendar_frame,
                text=f"{hour:02d}:00",
                bg='white',
                fg='#9CA3AF',
                font=('Helvetica', 9),
                anchor='ne'
            )
            time_label.grid(row=hour - 7, column=0, sticky='ne', padx=4, pady=0)
            
            # Day cells for this hour
            for day in range(7):
                date = start_of_week + timedelta(days=day)
                cell = tk.Frame(
                    self.calendar_frame,
                    bg='white',
                    highlightthickness=1,
                    highlightbackground='#E5E7EB',
                    cursor='hand2'
                )
                cell.grid(row=hour - 7, column=day + 1, sticky='nsew', padx=1, pady=1)
                
                # Get events/bookings for this date and hour
                items = self._get_items_for_datetime(date.date(), hour)
                
                if items:
                    # Show events in this time slot
                    for item in items[:2]:  # Show max 2 per slot
                        color = self._get_item_color(item)
                        title = item.get('title') or item.get('resource') or 'Item'
                        
                        event_label = tk.Label(
                            cell,
                            text=title[:15] + '...' if len(title) > 15 else title,
                            bg=color,
                            fg='white',
                            font=('Helvetica', 8),
                            anchor='w',
                            padx=4,
                            pady=2
                        )
                        event_label.pack(fill='x', pady=1)
                    
                    if len(items) > 2:
                        more_label = tk.Label(
                            cell,
                            text=f'+{len(items) - 2}',
                            bg='#F3F4F6',
                            fg='#6B7280',
                            font=('Helvetica', 7)
                        )
                        more_label.pack()
                
                # Bind click
                cell.bind('<Button-1>', lambda e, d=date.date(), h=hour: self._on_time_slot_click(d, h))
    
    def _render_day_view(self):
        """Render detailed day view with hourly breakdown"""
        date = self.current_date.date()
        
        # Configure grid
        self.calendar_frame.grid_columnconfigure(0, weight=0)
        self.calendar_frame.grid_columnconfigure(1, weight=1)
        
        # Header with date
        header = tk.Label(
            self.calendar_frame,
            text=date.strftime('%A, %B %d, %Y'),
            bg='#F9FAFB',
            fg=self.colors.get('primary', '#2C3E50'),
            font=('Helvetica', 14, 'bold'),
            pady=12
        )
        header.grid(row=0, column=0, columnspan=2, sticky='ew')
        
        # Time slots (24 hours)
        for hour in range(24):
            # Time label
            time_label = tk.Label(
                self.calendar_frame,
                text=f"{hour:02d}:00",
                bg='white',
                fg='#9CA3AF',
                font=('Helvetica', 10),
                anchor='ne',
                width=8
            )
            time_label.grid(row=hour + 1, column=0, sticky='ne', padx=8, pady=2)
            
            # Hour cell
            cell = tk.Frame(
                self.calendar_frame,
                bg='white',
                highlightthickness=1,
                highlightbackground='#E5E7EB',
                height=60,
                cursor='hand2'
            )
            cell.grid(row=hour + 1, column=1, sticky='ew', padx=2, pady=1)
            cell.grid_propagate(False)
            
            # Get events/bookings for this hour
            items = self._get_items_for_datetime(date, hour)
            
            if items:
                for item in items:
                    color = self._get_item_color(item)
                    title = item.get('title') or item.get('resource') or 'Item'
                    
                    event_frame = tk.Frame(cell, bg=color)
                    event_frame.pack(fill='both', expand=True, padx=4, pady=2)
                    
                    tk.Label(
                        event_frame,
                        text=title,
                        bg=color,
                        fg='white',
                        font=('Helvetica', 10, 'bold'),
                        anchor='w'
                    ).pack(fill='x', padx=8, pady=4)
                    
                    # Show details
                    if 'venue' in item:
                        tk.Label(
                            event_frame,
                            text=f"📍 {item['venue']}",
                            bg=color,
                            fg='white',
                            font=('Helvetica', 8),
                            anchor='w'
                        ).pack(fill='x', padx=8, pady=(0, 4))
            
            # Bind click
            cell.bind('<Button-1>', lambda e, h=hour: self._on_time_slot_click(date, h))
    
    def _get_items_for_date(self, date, item_type='all'):
        """Get events/bookings for a specific date"""
        items = []
        
        if item_type in ('all', 'events'):
            for event in self.events:
                event_date = self._parse_date(event.get('start_time'))
                if event_date and event_date.date() == date:
                    items.append({'type': 'event', **event})
        
        if item_type in ('all', 'bookings'):
            for booking in self.bookings:
                booking_date = self._parse_date(booking.get('start_time'))
                if booking_date and booking_date.date() == date:
                    items.append({'type': 'booking', **booking})
        
        return items
    
    def _get_items_for_datetime(self, date, hour):
        """Get events/bookings for a specific date and hour"""
        items = []
        
        for event in self.events:
            event_time = self._parse_date(event.get('start_time'))
            if event_time and event_time.date() == date and event_time.hour == hour:
                items.append({'type': 'event', **event})
        
        for booking in self.bookings:
            booking_time = self._parse_date(booking.get('start_time'))
            if booking_time and booking_time.date() == date and booking_time.hour == hour:
                items.append({'type': 'booking', **booking})
        
        return items
    
    def _get_item_color(self, item):
        """Get color for an event or booking"""
        if item.get('type') == 'event':
            category = (item.get('category') or 'default').lower()
            return self.event_colors.get(category, self.event_colors['default'])
        elif item.get('type') == 'booking':
            status = (item.get('status') or 'default').lower()
            return self.booking_colors.get(status, self.booking_colors['default'])
        return '#95A5A6'
    
    def _on_date_click(self, date, items):
        """Handle date cell click"""
        self.selected_date = date
        
        if self.on_date_click_callback:
            self.on_date_click_callback(date, items)
        
        # Re-render to show selection
        self._render_calendar()
    
    def _on_time_slot_click(self, date, hour):
        """Handle time slot click in week/day view"""
        items = self._get_items_for_datetime(date, hour)
        
        if self.on_date_click_callback:
            datetime_obj = datetime.combine(date, datetime.min.time().replace(hour=hour))
            self.on_date_click_callback(datetime_obj, items)
    
    def _show_tooltip(self, event, date, items):
        """Show tooltip with event details on hover"""
        # Cancel any existing timer
        if self.tooltip_timer:
            self.after_cancel(self.tooltip_timer)
        
        # Set timer for tooltip (500ms delay)
        self.tooltip_timer = self.after(500, lambda: self._display_tooltip(event, date, items))
    
    def _display_tooltip(self, event, date, items):
        """Display the tooltip"""
        self._hide_tooltip()
        
        # Create tooltip window
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        # Tooltip content
        tooltip_frame = tk.Frame(
            self.tooltip,
            bg='#1F2937',
            highlightthickness=1,
            highlightbackground='#374151'
        )
        tooltip_frame.pack()
        
        # Date header
        tk.Label(
            tooltip_frame,
            text=date.strftime('%A, %B %d, %Y'),
            bg='#1F2937',
            fg='white',
            font=('Helvetica', 10, 'bold')
        ).pack(anchor='w', padx=10, pady=(8, 4))
        
        # Separator
        tk.Frame(tooltip_frame, bg='#4B5563', height=1).pack(fill='x', padx=10, pady=4)
        
        # Items list
        for item in items[:5]:  # Show max 5
            item_type = item.get('type', 'item')
            title = item.get('title') or item.get('resource') or 'Item'
            color = self._get_item_color(item)
            
            item_frame = tk.Frame(tooltip_frame, bg='#1F2937')
            item_frame.pack(fill='x', padx=10, pady=2)
            
            # Color indicator
            tk.Frame(item_frame, bg=color, width=4, height=16).pack(side='left', padx=(0, 6))
            
            # Title
            tk.Label(
                item_frame,
                text=title,
                bg='#1F2937',
                fg='white',
                font=('Helvetica', 9),
                anchor='w'
            ).pack(side='left', fill='x', expand=True)
        
        if len(items) > 5:
            tk.Label(
                tooltip_frame,
                text=f'+ {len(items) - 5} more...',
                bg='#1F2937',
                fg='#9CA3AF',
                font=('Helvetica', 8, 'italic')
            ).pack(anchor='w', padx=10, pady=(2, 8))
        else:
            tk.Label(tooltip_frame, text='', bg='#1F2937').pack(pady=4)
    
    def _hide_tooltip(self):
        """Hide tooltip"""
        if self.tooltip_timer:
            self.after_cancel(self.tooltip_timer)
            self.tooltip_timer = None
        
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
    
    def _prev_period(self):
        """Navigate to previous period"""
        if self.view_mode == 'month':
            # Previous month
            if self.current_date.month == 1:
                self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
            else:
                self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        elif self.view_mode == 'week':
            # Previous week
            self.current_date = self.current_date - timedelta(days=7)
        elif self.view_mode == 'day':
            # Previous day
            self.current_date = self.current_date - timedelta(days=1)
        
        self._render_calendar()
    
    def _next_period(self):
        """Navigate to next period"""
        if self.view_mode == 'month':
            # Next month
            if self.current_date.month == 12:
                self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
            else:
                self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        elif self.view_mode == 'week':
            # Next week
            self.current_date = self.current_date + timedelta(days=7)
        elif self.view_mode == 'day':
            # Next day
            self.current_date = self.current_date + timedelta(days=1)
        
        self._render_calendar()
    
    def _go_to_today(self):
        """Navigate to today"""
        self.current_date = datetime.now()
        self.selected_date = None
        self._render_calendar()
    
    def _change_view(self, view_mode):
        """Change calendar view mode"""
        if view_mode in ('month', 'week', 'day'):
            self.view_mode = view_mode
            self._render_calendar()
            
            # Update view toggle buttons
            if self.show_controls:
                self._build_controls()
                self._render_calendar()
    
    def _get_period_label(self):
        """Get label for current period"""
        if self.view_mode == 'month':
            return self.current_date.strftime('%B %Y')
        elif self.view_mode == 'week':
            start_of_week = self.current_date - timedelta(days=self.current_date.weekday() + 1)
            end_of_week = start_of_week + timedelta(days=6)
            return f"{start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d, %Y')}"
        elif self.view_mode == 'day':
            return self.current_date.strftime('%A, %B %d, %Y')
        return ''
    
    @staticmethod
    def _parse_date(date_str):
        """Parse date string to datetime object"""
        if not date_str:
            return None
        
        if isinstance(date_str, datetime):
            return date_str
        
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ"):
            try:
                return datetime.strptime(str(date_str)[:26], fmt)
            except Exception:
                continue
        return None
    
    # Public API Methods
    
    def update_data(self, events=None, bookings=None):
        """Update calendar data and re-render"""
        if events is not None:
            self.events = events
        if bookings is not None:
            self.bookings = bookings
        self._render_calendar()
    
    def set_date(self, date):
        """Set current date and re-render"""
        if isinstance(date, str):
            date = self._parse_date(date)
        if isinstance(date, datetime):
            self.current_date = date
        self._render_calendar()
    
    def set_view(self, view_mode):
        """Set view mode"""
        self._change_view(view_mode)
    
    def get_current_date(self):
        """Get current displayed date"""
        return self.current_date
    
    def get_selected_date(self):
        """Get selected date"""
        return self.selected_date
