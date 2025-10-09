"""
CalendarView Usage Examples

This file demonstrates how to use the CalendarView component in different scenarios.
"""

import tkinter as tk
from datetime import datetime, timedelta
from components.calendar_view import CalendarView


# Example 1: Full Calendar for Events Page
def example_events_calendar():
    """Full calendar view for events page"""
    
    def on_date_click(date, items):
        """Callback when date is clicked"""
        print(f"Date clicked: {date}")
        print(f"Items on this date: {len(items)}")
        for item in items:
            print(f"  - {item.get('title') or item.get('resource')}")
    
    # Sample events data
    events = [
        {
            'id': 1,
            'title': 'Data Science Workshop',
            'category': 'workshop',
            'start_time': '2025-10-15 14:00:00',
            'venue': 'Lab 101',
            'status': 'approved'
        },
        {
            'id': 2,
            'title': 'Basketball Tournament',
            'category': 'sports',
            'start_time': '2025-10-15 16:00:00',
            'venue': 'Sports Complex',
            'status': 'approved'
        },
        {
            'id': 3,
            'title': 'Cultural Fest',
            'category': 'cultural',
            'start_time': '2025-10-20 10:00:00',
            'venue': 'Auditorium',
            'status': 'approved'
        }
    ]
    
    # Create calendar
    # calendar = CalendarView(
    #     parent_frame,
    #     on_date_click_callback=on_date_click,
    #     events=events,
    #     bookings=[],
    #     view_mode='month',
    #     show_controls=True,
    #     mini_mode=False
    # )
    # calendar.pack(fill='both', expand=True, padx=20, pady=20)


# Example 2: Mini Calendar for Dashboard
def example_dashboard_mini_calendar():
    """Compact calendar for dashboard sidebar"""
    
    def on_date_click(date, items):
        """Show quick info for clicked date"""
        print(f"Quick view for {date}")
    
    events = [
        {'title': 'Meeting', 'start_time': '2025-10-15 10:00:00', 'category': 'academic'},
        {'title': 'Workshop', 'start_time': '2025-10-16 14:00:00', 'category': 'workshop'}
    ]
    
    # Create mini calendar
    # calendar = CalendarView(
    #     sidebar_frame,
    #     on_date_click_callback=on_date_click,
    #     events=events,
    #     view_mode='month',
    #     show_controls=True,
    #     mini_mode=True  # Compact mode
    # )
    # calendar.pack(fill='both', padx=10, pady=10)


# Example 3: Booking Availability Calendar
def example_bookings_calendar():
    """Calendar showing resource bookings"""
    
    def on_date_click(date, items):
        """Show booking details"""
        print(f"Bookings on {date}:")
        for item in items:
            if item.get('type') == 'booking':
                print(f"  - {item.get('resource')}: {item.get('status')}")
    
    # Sample bookings data
    bookings = [
        {
            'id': 1,
            'resource': 'Conference Room A',
            'start_time': '2025-10-15 09:00:00',
            'end_time': '2025-10-15 11:00:00',
            'status': 'approved'
        },
        {
            'id': 2,
            'resource': 'Lab 201',
            'start_time': '2025-10-15 14:00:00',
            'end_time': '2025-10-15 16:00:00',
            'status': 'pending'
        },
        {
            'id': 3,
            'resource': 'Auditorium',
            'start_time': '2025-10-16 10:00:00',
            'end_time': '2025-10-16 12:00:00',
            'status': 'approved'
        }
    ]
    
    # Create calendar
    # calendar = CalendarView(
    #     parent_frame,
    #     on_date_click_callback=on_date_click,
    #     events=[],
    #     bookings=bookings,
    #     view_mode='week',  # Week view for detailed booking slots
    #     show_controls=True
    # )
    # calendar.pack(fill='both', expand=True)


# Example 4: Week View with Schedule
def example_week_schedule():
    """Week view showing detailed schedule"""
    
    def on_time_slot_click(datetime_obj, items):
        """Handle time slot click"""
        print(f"Time slot: {datetime_obj}")
        print(f"Items: {len(items)}")
    
    events = [
        {'title': 'Morning Lecture', 'start_time': '2025-10-15 09:00:00', 'category': 'academic', 'venue': 'Hall A'},
        {'title': 'Lab Session', 'start_time': '2025-10-15 14:00:00', 'category': 'academic', 'venue': 'Lab 101'},
        {'title': 'Study Group', 'start_time': '2025-10-16 10:00:00', 'category': 'academic', 'venue': 'Library'},
        {'title': 'Sports Practice', 'start_time': '2025-10-17 16:00:00', 'category': 'sports', 'venue': 'Gym'}
    ]
    
    # calendar = CalendarView(
    #     parent_frame,
    #     on_date_click_callback=on_time_slot_click,
    #     events=events,
    #     view_mode='week',
    #     show_controls=True
    # )
    # calendar.pack(fill='both', expand=True)


# Example 5: Day View for Detailed Schedule
def example_day_view():
    """Detailed day view with hourly breakdown"""
    
    def on_time_slot_click(datetime_obj, items):
        """Handle time slot click"""
        if items:
            print(f"Hour {datetime_obj.hour}:00 - {len(items)} item(s)")
        else:
            print(f"Hour {datetime_obj.hour}:00 - Available")
    
    events = [
        {'title': 'Team Meeting', 'start_time': '2025-10-15 09:00:00', 'category': 'academic', 'venue': 'Room 301'},
        {'title': 'Project Work', 'start_time': '2025-10-15 10:00:00', 'category': 'academic', 'venue': 'Lab'},
        {'title': 'Lunch Break', 'start_time': '2025-10-15 12:00:00', 'category': 'social', 'venue': 'Cafeteria'},
        {'title': 'Coding Workshop', 'start_time': '2025-10-15 14:00:00', 'category': 'workshop', 'venue': 'Lab 202'},
        {'title': 'Study Session', 'start_time': '2025-10-15 16:00:00', 'category': 'academic', 'venue': 'Library'}
    ]
    
    # calendar = CalendarView(
    #     parent_frame,
    #     on_date_click_callback=on_time_slot_click,
    #     events=events,
    #     view_mode='day',
    #     show_controls=True
    # )
    # calendar.pack(fill='both', expand=True)


# Example 6: Combined Events and Bookings
def example_combined_calendar():
    """Calendar showing both events and bookings"""
    
    def on_date_click(date, items):
        """Show all items for date"""
        events = [i for i in items if i.get('type') == 'event']
        bookings = [i for i in items if i.get('type') == 'booking']
        
        print(f"Date: {date}")
        print(f"  Events: {len(events)}")
        print(f"  Bookings: {len(bookings)}")
    
    events = [
        {'title': 'Conference', 'start_time': '2025-10-15 10:00:00', 'category': 'conference'},
        {'title': 'Workshop', 'start_time': '2025-10-16 14:00:00', 'category': 'workshop'}
    ]
    
    bookings = [
        {'resource': 'Room A', 'start_time': '2025-10-15 09:00:00', 'status': 'approved'},
        {'resource': 'Lab 1', 'start_time': '2025-10-15 14:00:00', 'status': 'pending'}
    ]
    
    # calendar = CalendarView(
    #     parent_frame,
    #     on_date_click_callback=on_date_click,
    #     events=events,
    #     bookings=bookings,
    #     view_mode='month'
    # )
    # calendar.pack(fill='both', expand=True)


# Example 7: Dynamic Data Update
def example_dynamic_update():
    """Update calendar data dynamically"""
    
    def on_date_click(date, items):
        print(f"Clicked: {date}")
    
    # Create calendar with initial data
    # calendar = CalendarView(
    #     parent_frame,
    #     on_date_click_callback=on_date_click,
    #     events=[],
    #     view_mode='month'
    # )
    # calendar.pack(fill='both', expand=True)
    
    # Later, update with new data
    # new_events = fetch_events_from_api()
    # calendar.update_data(events=new_events)
    
    # Or update bookings
    # new_bookings = fetch_bookings_from_api()
    # calendar.update_data(bookings=new_bookings)


# Example 8: Programmatic Navigation
def example_programmatic_navigation():
    """Control calendar programmatically"""
    
    # calendar = CalendarView(parent_frame, view_mode='month')
    
    # Navigate to specific date
    # calendar.set_date('2025-12-25')
    
    # Change view mode
    # calendar.set_view('week')
    
    # Get current date
    # current = calendar.get_current_date()
    
    # Get selected date
    # selected = calendar.get_selected_date()


# Example 9: Custom Colors
def example_custom_colors():
    """Calendar with custom color scheme"""
    
    custom_colors = {
        'primary': '#1A237E',      # Deep blue
        'secondary': '#0277BD',    # Light blue
        'success': '#00695C',      # Teal
        'warning': '#F57C00',      # Orange
        'danger': '#C62828',       # Red
        'background': '#FAFAFA'    # Light gray
    }
    
    # calendar = CalendarView(
    #     parent_frame,
    #     events=[],
    #     colors=custom_colors
    # )
    # calendar.pack(fill='both', expand=True)


# Example 10: Complete Integration Example
class CalendarPage(tk.Frame):
    """Complete page with CalendarView integration"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='white')
        
        # Sample data
        self.events = self._generate_sample_events()
        self.bookings = self._generate_sample_bookings()
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build page UI"""
        # Header
        header = tk.Frame(self, bg='white', height=60)
        header.pack(fill='x', padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text='📅 Event Calendar',
            bg='white',
            font=('Helvetica', 18, 'bold')
        ).pack(side='left')
        
        # Calendar
        self.calendar = CalendarView(
            self,
            on_date_click_callback=self._on_date_click,
            events=self.events,
            bookings=self.bookings,
            view_mode='month',
            show_controls=True,
            mini_mode=False
        )
        self.calendar.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Details panel (shows selected date info)
        self.details_frame = tk.Frame(self, bg='#F9FAFB', height=150)
        self.details_frame.pack(fill='x', padx=20, pady=(0, 20))
        self.details_frame.pack_propagate(False)
        
        self.details_label = tk.Label(
            self.details_frame,
            text='Click on a date to see details',
            bg='#F9FAFB',
            fg='#6B7280',
            font=('Helvetica', 12)
        )
        self.details_label.pack(expand=True)
    
    def _on_date_click(self, date, items):
        """Handle date click"""
        # Clear details
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        # Show date info
        info_frame = tk.Frame(self.details_frame, bg='#F9FAFB')
        info_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Date header
        if isinstance(date, datetime):
            date_str = date.strftime('%A, %B %d, %Y at %I:%M %p')
        else:
            date_str = date.strftime('%A, %B %d, %Y')
        
        tk.Label(
            info_frame,
            text=date_str,
            bg='#F9FAFB',
            fg='#1F2937',
            font=('Helvetica', 14, 'bold')
        ).pack(anchor='w', pady=(0, 8))
        
        # Items list
        if items:
            for item in items[:5]:  # Show first 5
                item_type = item.get('type', 'item')
                title = item.get('title') or item.get('resource') or 'Item'
                
                item_frame = tk.Frame(info_frame, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
                item_frame.pack(fill='x', pady=2)
                
                tk.Label(
                    item_frame,
                    text=f"{'📅' if item_type == 'event' else '📚'} {title}",
                    bg='white',
                    fg='#374151',
                    font=('Helvetica', 10),
                    anchor='w'
                ).pack(side='left', padx=8, pady=6)
        else:
            tk.Label(
                info_frame,
                text='No events or bookings on this date',
                bg='#F9FAFB',
                fg='#9CA3AF',
                font=('Helvetica', 10, 'italic')
            ).pack(anchor='w')
    
    def _generate_sample_events(self):
        """Generate sample events"""
        today = datetime.now()
        events = []
        
        for i in range(10):
            date = today + timedelta(days=i * 2)
            events.append({
                'id': i + 1,
                'title': f'Event {i + 1}',
                'category': ['academic', 'sports', 'cultural', 'workshop'][i % 4],
                'start_time': date.strftime('%Y-%m-%d 10:00:00'),
                'venue': f'Venue {i + 1}',
                'status': 'approved'
            })
        
        return events
    
    def _generate_sample_bookings(self):
        """Generate sample bookings"""
        today = datetime.now()
        bookings = []
        
        for i in range(5):
            date = today + timedelta(days=i * 3)
            bookings.append({
                'id': i + 1,
                'resource': f'Resource {i + 1}',
                'start_time': date.strftime('%Y-%m-%d 14:00:00'),
                'end_time': (date + timedelta(hours=2)).strftime('%Y-%m-%d 16:00:00'),
                'status': ['approved', 'pending', 'approved'][i % 3]
            })
        
        return bookings


# Example 11: No Controls Mode
def example_no_controls():
    """Calendar without navigation controls (embedded view)"""
    
    # Simple calendar without header controls
    # calendar = CalendarView(
    #     parent_frame,
    #     events=events,
    #     show_controls=False,  # Hide controls
    #     mini_mode=True
    # )
    # calendar.pack(fill='both', expand=True)


if __name__ == '__main__':
    # Test the component
    root = tk.Tk()
    root.title('CalendarView Examples')
    root.geometry('900x700')
    
    page = CalendarPage(root, None)
    page.pack(fill='both', expand=True)
    
    root.mainloop()
