"""
Usage Examples for SearchComponent

This file shows how to use the SearchComponent in different pages.
"""

import tkinter as tk
from components.search_component import SearchComponent


# Example 1: Events Page
def example_events_page():
    """Example usage for Events page"""
    
    def on_search(search_text, filters):
        """Callback when search or filters change"""
        print(f"Search text: {search_text}")
        print(f"Active filters: {filters}")
        
        # Use the data to filter events
        # filtered_events = filter_events(search_text, filters)
        # render_events(filtered_events)
    
    # Configure for events
    config = {
        'categories': ['Workshop', 'Seminar', 'Meeting', 'Conference', 'Social'],
        'statuses': ['Upcoming', 'Ongoing', 'Completed', 'Cancelled'],
        'sort_options': ['Date', 'Name', 'Popularity', 'Attendees'],
        'show_date_filter': True,
        'show_category_filter': True,
        'show_status_filter': True,
        'placeholder': 'Search events by name, organizer, or description...'
    }
    
    # Create search component
    # search = SearchComponent(parent_frame, on_search_callback=on_search, config=config)
    # search.pack(fill='x', pady=(0, 20))


# Example 2: Resources Page
def example_resources_page():
    """Example usage for Resources page"""
    
    def on_search(search_text, filters):
        """Callback when search or filters change"""
        print(f"Search: {search_text}")
        print(f"Filters: {filters}")
        
        # Filter resources
        # filtered_resources = filter_resources(search_text, filters)
        # render_resources(filtered_resources)
    
    # Configure for resources
    config = {
        'categories': ['Conference Room', 'Lecture Hall', 'Lab', 'Auditorium', 'Study Room'],
        'statuses': ['Available', 'Maintenance', 'Reserved'],
        'sort_options': ['Name', 'Capacity', 'Location', 'Availability'],
        'show_date_filter': True,  # For availability date range
        'show_category_filter': True,
        'show_status_filter': True,
        'placeholder': 'Search resources by name, location, or amenities...'
    }
    
    # Create search component
    # search = SearchComponent(parent_frame, on_search_callback=on_search, config=config)
    # search.pack(fill='x', pady=(0, 20))


# Example 3: Users Page (Admin)
def example_users_page():
    """Example usage for Admin Users page"""
    
    def on_search(search_text, filters):
        """Callback when search or filters change"""
        print(f"Search: {search_text}")
        print(f"Filters: {filters}")
        
        # Filter users
        # filtered_users = filter_users(search_text, filters)
        # populate_users_table(filtered_users)
    
    # Configure for users
    config = {
        'categories': ['Student', 'Organizer', 'Admin'],  # Using as roles
        'statuses': ['Active', 'Blocked', 'Pending'],
        'sort_options': ['Name', 'Email', 'Registration Date', 'Role'],
        'show_date_filter': True,  # For registration date range
        'show_category_filter': True,  # Shows as "Roles" in context
        'show_status_filter': True,
        'placeholder': 'Search users by name, email, or ID...'
    }
    
    # Create search component
    # search = SearchComponent(parent_frame, on_search_callback=on_search, config=config)
    # search.pack(fill='x', pady=(0, 20))


# Example 4: Bookings Page
def example_bookings_page():
    """Example usage for Bookings page"""
    
    def on_search(search_text, filters):
        """Callback when search or filters change"""
        print(f"Search: {search_text}")
        print(f"Filters: {filters}")
    
    # Configure for bookings
    config = {
        'categories': [],  # No categories needed
        'statuses': ['Pending', 'Approved', 'Rejected', 'Completed', 'Cancelled'],
        'sort_options': ['Date', 'Resource', 'User', 'Status'],
        'show_date_filter': True,
        'show_category_filter': False,  # Disable category filter
        'show_status_filter': True,
        'placeholder': 'Search bookings by resource, user, or purpose...'
    }
    
    # Create search component
    # search = SearchComponent(parent_frame, on_search_callback=on_search, config=config)
    # search.pack(fill='x', pady=(0, 20))


# Example 5: Programmatic Usage
def example_programmatic_usage():
    """Example of programmatic control"""
    
    def on_search(search_text, filters):
        print(f"Search: {search_text}, Filters: {filters}")
    
    # search = SearchComponent(parent_frame, on_search_callback=on_search, config=config)
    
    # Get current values
    # current_search = search.get_search_text()
    # current_filters = search.get_active_filters()
    
    # Clear search only
    # search.clear_search()
    
    # Reset everything
    # search.reset_all()


# Example 6: Complete Integration
class ExamplePage(tk.Frame):
    """Example page with SearchComponent integration"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Search component config
        config = {
            'categories': ['Category 1', 'Category 2', 'Category 3'],
            'statuses': ['Active', 'Inactive'],
            'sort_options': ['Relevance', 'Date', 'Name'],
            'placeholder': 'Search...'
        }
        
        # Create search component
        self.search = SearchComponent(
            self,
            on_search_callback=self.handle_search,
            config=config,
            colors={
                'primary': '#2C3E50',
                'secondary': '#3498DB',
                'success': '#27AE60',
                'warning': '#F39C12',
                'danger': '#E74C3C'
            }
        )
        self.search.pack(fill='x', padx=20, pady=20)
        
        # Results area
        self.results_frame = tk.Frame(self)
        self.results_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Initial load
        self.load_data()
    
    def handle_search(self, search_text, filters):
        """Handle search and filter changes"""
        # This is called automatically when:
        # - User types in search (after 500ms debounce)
        # - User clicks Search button
        # - User applies filters
        # - User removes filter tags
        
        print(f"Searching for: '{search_text}'")
        print(f"With filters: {filters}")
        
        # Apply to your data
        self.load_data(search=search_text, filters=filters)
    
    def load_data(self, search='', filters=None):
        """Load and display filtered data"""
        filters = filters or {}
        
        # Clear results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Example: Filter your data based on search and filters
        # data = get_data()
        
        # Apply search text
        # if search:
        #     data = [item for item in data if search.lower() in item['name'].lower()]
        
        # Apply date range filter
        # if 'date_range' in filters:
        #     start = filters['date_range']['start']
        #     end = filters['date_range']['end']
        #     data = [item for item in data if start <= item['date'] <= end]
        
        # Apply category filter
        # if 'categories' in filters:
        #     data = [item for item in data if item['category'] in filters['categories']]
        
        # Apply status filter
        # if 'status' in filters:
        #     data = [item for item in data if item['status'] == filters['status']]
        
        # Apply sorting
        # if 'sort' in filters:
        #     sort_by = filters['sort']
        #     data.sort(key=lambda x: x[sort_by.lower()])
        
        # Display results
        # self.display_results(data)
        
        tk.Label(self.results_frame, text=f"Results for: {search}", font=('Helvetica', 12)).pack()


if __name__ == '__main__':
    # Test the component
    root = tk.Tk()
    root.title('SearchComponent Example')
    root.geometry('800x600')
    
    page = ExamplePage(root)
    page.pack(fill='both', expand=True)
    
    root.mainloop()
