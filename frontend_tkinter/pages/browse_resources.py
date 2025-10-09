import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime, timedelta
from tkcalendar import DateEntry

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from components.search_component import SearchComponent


class BrowseResourcesPage(tk.Frame):
    """Browse and book resources with filtering options."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors.get('background', '#ECF0F1'))
        self.controller = controller
        self.api = APIClient()
        self.session = SessionManager()
        
        # Get colors
        self.colors = controller.colors if hasattr(controller, 'colors') else {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'background': '#ECF0F1'
        }
        
        # Data
        self.all_resources = []
        self.filtered_resources = []
        
        # Filter state
        self.filter_type = tk.StringVar(value='all')
        self.filter_date = tk.StringVar(value='')
        self.min_capacity = tk.IntVar(value=0)
        self.max_capacity = tk.IntVar(value=500)
        self.amenities = {}
        
        # Layout: sidebar + main content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Main content
        
        self._build_sidebar()
        self._build_main_area()
        
        # Load data
        self._load_resources()

    def _build_sidebar(self):
        """Build filter sidebar"""
        sidebar = tk.Frame(self, bg='white', width=280, highlightthickness=1, highlightbackground='#E5E7EB')
        sidebar.grid(row=0, column=0, sticky='nsw')
        sidebar.grid_propagate(False)
        
        # Scrollable sidebar content
        canvas = tk.Canvas(sidebar, bg='white', highlightthickness=0, width=280)
        scrollbar = ttk.Scrollbar(sidebar, orient='vertical', command=canvas.yview)
        
        content = tk.Frame(canvas, bg='white')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=content, anchor='nw', width=260)
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Sidebar header
        header = tk.Frame(content, bg='white')
        header.pack(fill='x', padx=16, pady=(16, 12))
        tk.Label(header, text='Filters', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 14, 'bold')).pack(anchor='w')
        
        # Clear filters button
        tk.Button(content, text='Clear All Filters', command=self._clear_filters, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 9), padx=12, pady=6).pack(fill='x', padx=16, pady=(0, 12))
        
        # Resource Type Filter
        self._add_filter_section(content, 'Resource Type')
        
        type_frame = tk.Frame(content, bg='white')
        type_frame.pack(fill='x', padx=16, pady=(0, 16))
        
        resource_types = [
            ('all', 'All Resources'),
            ('classroom', 'Classroom'),
            ('lab', 'Laboratory'),
            ('auditorium', 'Auditorium'),
            ('equipment', 'Equipment'),
            ('conference', 'Conference Room'),
            ('sports', 'Sports Facility')
        ]
        
        for value, label in resource_types:
            rb = tk.Radiobutton(type_frame, text=label, variable=self.filter_type, value=value, bg='white', font=('Helvetica', 10), selectcolor='white', command=self._apply_filters)
            rb.pack(anchor='w', pady=2)
        
        # Capacity Filter
        self._add_filter_section(content, 'Capacity Range')
        
        capacity_frame = tk.Frame(content, bg='white')
        capacity_frame.pack(fill='x', padx=16, pady=(0, 16))
        
        tk.Label(capacity_frame, text='Minimum Capacity:', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w')
        
        min_cap_frame = tk.Frame(capacity_frame, bg='white')
        min_cap_frame.pack(fill='x', pady=(2, 8))
        
        min_slider = tk.Scale(min_cap_frame, from_=0, to=500, orient='horizontal', variable=self.min_capacity, bg='white', highlightthickness=0, showvalue=0, command=lambda v: self._on_capacity_change())
        min_slider.pack(side='left', fill='x', expand=True)
        
        self.min_label = tk.Label(min_cap_frame, text='0', bg='white', fg=self.colors.get('secondary', '#3498DB'), font=('Helvetica', 9, 'bold'), width=4)
        self.min_label.pack(side='right')
        
        tk.Label(capacity_frame, text='Maximum Capacity:', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w')
        
        max_cap_frame = tk.Frame(capacity_frame, bg='white')
        max_cap_frame.pack(fill='x', pady=(2, 0))
        
        max_slider = tk.Scale(max_cap_frame, from_=0, to=500, orient='horizontal', variable=self.max_capacity, bg='white', highlightthickness=0, showvalue=0, command=lambda v: self._on_capacity_change())
        max_slider.pack(side='left', fill='x', expand=True)
        
        self.max_label = tk.Label(max_cap_frame, text='500', bg='white', fg=self.colors.get('secondary', '#3498DB'), font=('Helvetica', 9, 'bold'), width=4)
        self.max_label.pack(side='right')
        
        # Amenities Filter
        self._add_filter_section(content, 'Amenities')
        
        amenities_frame = tk.Frame(content, bg='white')
        amenities_frame.pack(fill='x', padx=16, pady=(0, 16))
        
        amenity_options = [
            ('projector', '📽️ Projector'),
            ('whiteboard', '📝 Whiteboard'),
            ('computers', '💻 Computers'),
            ('audio', '🔊 Audio System'),
            ('ac', '❄️ Air Conditioning'),
            ('wifi', '📡 WiFi'),
            ('podium', '🎤 Podium'),
            ('recording', '📹 Recording')
        ]
        
        for key, label in amenity_options:
            var = tk.BooleanVar()
            self.amenities[key] = var
            cb = tk.Checkbutton(amenities_frame, text=label, variable=var, bg='white', font=('Helvetica', 9), selectcolor='white', command=self._apply_filters)
            cb.pack(anchor='w', pady=2)
        
        # Availability Date Picker
        self._add_filter_section(content, 'Check Availability')
        
        date_frame = tk.Frame(content, bg='white')
        date_frame.pack(fill='x', padx=16, pady=(0, 16))
        
        tk.Label(date_frame, text='Select Date:', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 4))
        
        try:
            # Try to use DateEntry from tkcalendar
            self.date_picker = DateEntry(date_frame, width=20, background=self.colors.get('secondary', '#3498DB'), foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', mindate=datetime.now())
            self.date_picker.pack(anchor='w', pady=(0, 8))
            self.date_picker.bind('<<DateEntrySelected>>', lambda e: self._apply_filters())
        except:
            # Fallback to simple entry
            date_entry = tk.Entry(date_frame, textvariable=self.filter_date, font=('Helvetica', 10), width=22)
            date_entry.pack(anchor='w', pady=(0, 8))
            date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
            tk.Label(date_frame, text='Format: YYYY-MM-DD', bg='white', fg='#9CA3AF', font=('Helvetica', 8)).pack(anchor='w')
        
        # Time slot filter
        tk.Label(date_frame, text='Time Slot:', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(8, 4))
        
        self.time_slot = tk.StringVar(value='all')
        time_slots = [
            ('all', 'All Day'),
            ('morning', 'Morning (8AM-12PM)'),
            ('afternoon', 'Afternoon (12PM-5PM)'),
            ('evening', 'Evening (5PM-9PM)')
        ]
        
        for value, label in time_slots:
            rb = tk.Radiobutton(date_frame, text=label, variable=self.time_slot, value=value, bg='white', font=('Helvetica', 9), selectcolor='white', command=self._apply_filters)
            rb.pack(anchor='w', pady=1)
        
        # Apply button
        tk.Button(content, text='Apply Filters', command=self._apply_filters, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=16, pady=10).pack(fill='x', padx=16, pady=(8, 16))

    def _add_filter_section(self, parent, title):
        """Add a filter section header"""
        separator = tk.Frame(parent, bg='#E5E7EB', height=1)
        separator.pack(fill='x', padx=16, pady=(0, 8))
        
        tk.Label(parent, text=title, bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w', padx=16, pady=(0, 8))

    def _build_main_area(self):
        """Build main content area"""
        main = tk.Frame(self, bg=self.colors.get('background', '#ECF0F1'))
        main.grid(row=0, column=1, sticky='nsew')
        
        main.grid_rowconfigure(0, weight=0)  # Header
        main.grid_rowconfigure(1, weight=1)  # Content
        main.grid_columnconfigure(0, weight=1)
        
        # Header
        header = tk.Frame(main, bg='white', height=80, highlightthickness=1, highlightbackground='#E5E7EB')
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)
        
        header_content = tk.Frame(header, bg='white')
        header_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Title
        title_frame = tk.Frame(header_content, bg='white')
        title_frame.pack(fill='x')
        tk.Label(title_frame, text='Browse Resources', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Find and book campus resources', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        
        # SearchComponent below title
        search_frame = tk.Frame(header_content, bg='white')
        search_frame.pack(fill='x', pady=(10, 0))
        
        # Configure SearchComponent for resources
        config = {
            'categories': ['Classroom', 'Laboratory', 'Auditorium', 'Equipment', 'Conference Room', 'Sports Facility'],
            'statuses': ['Available', 'Maintenance', 'Reserved', 'Out of Service'],
            'sort_options': ['Name', 'Capacity', 'Location', 'Type'],
            'show_date_filter': True,
            'show_category_filter': True,
            'show_status_filter': True,
            'placeholder': 'Search resources by name, location, or amenities...'
        }
        
        # Create search component
        self.search_component = SearchComponent(
            search_frame,
            on_search_callback=self._handle_search,
            config=config,
            colors=self.colors
        )
        self.search_component.pack(fill='x')
        
        # Scrollable content
        content_container = tk.Frame(main, bg=self.colors.get('background', '#ECF0F1'))
        content_container.grid(row=1, column=0, sticky='nsew', padx=30, pady=20)
        
        canvas = tk.Canvas(content_container, bg=self.colors.get('background', '#ECF0F1'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient='vertical', command=canvas.yview)
        
        self.content = tk.Frame(canvas, bg=self.colors.get('background', '#ECF0F1'))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=self.content, anchor='nw', width=canvas.winfo_width())
        self.content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Update canvas width on resize
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag('all')[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

    def _load_resources(self):
        """Load resources from API"""
        self._show_loading()
        
        def worker():
            try:
                self.all_resources = self.api.get('resources') or []
                self.filtered_resources = self.all_resources.copy()
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load resources: {str(e)}')
                self.after(0, show_error)
                self.all_resources = []
                self.filtered_resources = []
            
            self.after(0, self._render_resources)
        
        threading.Thread(target=worker, daemon=True).start()

    def _show_loading(self):
        """Show loading indicator"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.content, bg=self.colors.get('background', '#ECF0F1'))
        loading_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(loading_frame, text='Loading resources...', bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 12)).pack()
        
        spinner = ttk.Progressbar(loading_frame, mode='indeterminate', length=300)
        spinner.pack(pady=10)
        spinner.start(10)

    def _handle_search(self, search_text, filters):
        """Handle search and filters from SearchComponent"""
        # Filter resources
        filtered = self.all_resources.copy()
        
        # Search filter
        if search_text:
            search_query = search_text.lower().strip()
            filtered = [r for r in filtered if 
                       search_query in (r.get('name', '') or '').lower() or
                       search_query in (r.get('code', '') or '').lower() or
                       search_query in (r.get('type', '') or '').lower() or
                       search_query in (r.get('location', '') or '').lower() or
                       search_query in str(r.get('amenities', [])).lower()]
        
        # Date range filter (check availability)
        if 'date_range' in filters:
            start_date = filters['date_range'].get('start')
            end_date = filters['date_range'].get('end')
            # Would check against bookings here in real implementation
            # For now, just pass through
            pass
        
        # Category filter (resource type)
        if 'categories' in filters and filters['categories']:
            filtered = [r for r in filtered if 
                       (r.get('type', '') or '').lower() in [c.lower() for c in filters['categories']]]
        
        # Status filter
        if 'status' in filters and filters['status']:
            status = filters['status'].lower()
            filtered = [r for r in filtered if 
                       (r.get('status', 'available') or 'available').lower() == status]
        
        # Sort resources
        sort_by = filters.get('sort', 'Name').lower()
        if sort_by == 'name':
            filtered.sort(key=lambda r: (r.get('name', '') or '').lower())
        elif sort_by == 'capacity':
            filtered.sort(key=lambda r: r.get('capacity', 0), reverse=True)
        elif sort_by == 'location':
            filtered.sort(key=lambda r: (r.get('location', '') or '').lower())
        elif sort_by == 'type':
            filtered.sort(key=lambda r: (r.get('type', '') or '').lower())
        
        self.filtered_resources = filtered
        self._render_resources()
    
    def _apply_filters(self):
        """Legacy method for sidebar filters - delegate to search component"""
        # This can be kept for sidebar compatibility or removed
        search_query = self.search_var.get().lower().strip() if hasattr(self, 'search_var') else ''
        resource_type = self.filter_type.get()
        min_cap = self.min_capacity.get()
        max_cap = self.max_capacity.get()
        
        # Get selected amenities
        selected_amenities = [key for key, var in self.amenities.items() if var.get()]
        
        # Filter resources
        filtered = self.all_resources.copy()
        
        # Search filter
        if search_query:
            filtered = [r for r in filtered if 
                       search_query in (r.get('name', '') or '').lower() or
                       search_query in (r.get('code', '') or '').lower() or
                       search_query in (r.get('type', '') or '').lower()]
        
        # Type filter
        if resource_type != 'all':
            filtered = [r for r in filtered if (r.get('type', '') or '').lower() == resource_type]
        
        # Capacity filter
        filtered = [r for r in filtered if 
                   min_cap <= (r.get('capacity', 0) or 0) <= max_cap]
        
        # Amenities filter
        if selected_amenities:
            filtered = [r for r in filtered if 
                       any(amenity in (r.get('amenities', []) or []) for amenity in selected_amenities)]
        
        self.filtered_resources = filtered
        self._render_resources()

    def _clear_filters(self):
        """Clear all filters"""
        self.filter_type.set('all')
        self.min_capacity.set(0)
        self.max_capacity.set(500)
        self.search_var.set('')
        self.time_slot.set('all')
        
        for var in self.amenities.values():
            var.set(False)
        
        if hasattr(self, 'date_picker'):
            self.date_picker.set_date(datetime.now())
        else:
            self.filter_date.set(datetime.now().strftime('%Y-%m-%d'))
        
        self._apply_filters()

    def _on_capacity_change(self):
        """Handle capacity slider change"""
        self.min_label.config(text=str(self.min_capacity.get()))
        self.max_label.config(text=str(self.max_capacity.get()))

    def _render_resources(self):
        """Render resource cards"""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Results count
        count_frame = tk.Frame(self.content, bg=self.colors.get('background', '#ECF0F1'))
        count_frame.pack(fill='x', pady=(0, 12))
        tk.Label(count_frame, text=f'{len(self.filtered_resources)} resource{"s" if len(self.filtered_resources) != 1 else ""} found', bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 11)).pack(side='left')
        
        if not self.filtered_resources:
            # Empty state
            empty_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            empty_frame.pack(fill='both', expand=True, pady=20)
            
            tk.Label(empty_frame, text='🔍', bg='white', font=('Helvetica', 48)).pack(pady=(40, 10))
            tk.Label(empty_frame, text='No resources found', bg='white', fg='#374151', font=('Helvetica', 14, 'bold')).pack()
            tk.Label(empty_frame, text='Try adjusting your filters', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(pady=(4, 40))
        else:
            # Create grid of resource cards (2 columns)
            grid_frame = tk.Frame(self.content, bg=self.colors.get('background', '#ECF0F1'))
            grid_frame.pack(fill='both', expand=True)
            
            for i in range(2):
                grid_frame.grid_columnconfigure(i, weight=1, uniform='col')
            
            for idx, resource in enumerate(self.filtered_resources):
                row = idx // 2
                col = idx % 2
                card = self._create_resource_card(resource)
                card.grid(row=row, column=col, padx=(0, 12) if col == 0 else (0, 0), pady=(0, 12), sticky='nsew')

    def _create_resource_card(self, resource):
        """Create a resource card"""
        card = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB', cursor='hand2')
        card.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=16)
        content.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        # Header with icon and type badge
        header = tk.Frame(content, bg='white')
        header.pack(fill='x', pady=(0, 12))
        header.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        # Icon based on type
        resource_type = (resource.get('type', 'equipment') or 'equipment').lower()
        type_icons = {
            'classroom': '🏫',
            'lab': '🔬',
            'auditorium': '🎭',
            'equipment': '⚙️',
            'conference': '💼',
            'sports': '⚽'
        }
        icon = type_icons.get(resource_type, '📦')
        
        icon_label = tk.Label(header, text=icon, bg='white', font=('Helvetica', 32))
        icon_label.pack(side='left', padx=(0, 12))
        icon_label.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        # Name and code
        info_frame = tk.Frame(header, bg='white')
        info_frame.pack(side='left', fill='x', expand=True)
        info_frame.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        name_label = tk.Label(info_frame, text=resource.get('name', 'Unnamed Resource'), bg='white', fg='#1F2937', font=('Helvetica', 13, 'bold'), wraplength=280, justify='left')
        name_label.pack(anchor='w')
        name_label.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        code = resource.get('code', resource.get('id', 'N/A'))
        code_label = tk.Label(info_frame, text=f"Code: {code}", bg='white', fg='#6B7280', font=('Helvetica', 9))
        code_label.pack(anchor='w', pady=(2, 0))
        code_label.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        # Type badge
        type_colors = {
            'classroom': '#3B82F6',
            'lab': '#8B5CF6',
            'auditorium': '#EC4899',
            'equipment': '#F59E0B',
            'conference': '#10B981',
            'sports': '#EF4444'
        }
        badge_color = type_colors.get(resource_type, '#6B7280')
        
        type_badge = tk.Label(header, text=resource_type.title(), bg=badge_color, fg='white', font=('Helvetica', 8, 'bold'), padx=8, pady=3)
        type_badge.pack(side='right')
        
        # Details section
        details = tk.Frame(content, bg='#F9FAFB')
        details.pack(fill='x', pady=(0, 12))
        details.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        details_content = tk.Frame(details, bg='#F9FAFB')
        details_content.pack(padx=12, pady=10)
        details_content.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        # Capacity
        capacity = resource.get('capacity', 'N/A')
        cap_frame = tk.Frame(details_content, bg='#F9FAFB')
        cap_frame.pack(side='left', padx=(0, 20))
        cap_frame.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        cap_label1 = tk.Label(cap_frame, text='Capacity', bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 8))
        cap_label1.pack()
        cap_label1.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        cap_label2 = tk.Label(cap_frame, text=f"🎫 {capacity}", bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 11, 'bold'))
        cap_label2.pack()
        cap_label2.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        # Location
        location = resource.get('location', resource.get('building', 'N/A'))
        loc_frame = tk.Frame(details_content, bg='#F9FAFB')
        loc_frame.pack(side='left')
        loc_frame.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        loc_label1 = tk.Label(loc_frame, text='Location', bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 8))
        loc_label1.pack()
        loc_label1.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        loc_label2 = tk.Label(loc_frame, text=f"📍 {location}", bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 11, 'bold'))
        loc_label2.pack()
        loc_label2.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        # Amenities
        amenities = resource.get('amenities', [])
        if amenities:
            amenities_label = tk.Label(content, text='Amenities:', bg='white', fg='#6B7280', font=('Helvetica', 9))
            amenities_label.pack(anchor='w', pady=(0, 4))
            amenities_label.bind('<Button-1>', lambda e: self._show_resource_details(resource))
            
            amenities_frame = tk.Frame(content, bg='white')
            amenities_frame.pack(fill='x', pady=(0, 12))
            amenities_frame.bind('<Button-1>', lambda e: self._show_resource_details(resource))
            
            amenity_icons = {
                'projector': '📽️',
                'whiteboard': '📝',
                'computers': '💻',
                'audio': '🔊',
                'ac': '❄️',
                'wifi': '📡',
                'podium': '🎤',
                'recording': '📹'
            }
            
            displayed = 0
            for amenity in amenities[:6]:  # Show first 6
                amenity_key = str(amenity).lower()
                icon = amenity_icons.get(amenity_key, '✓')
                label = f"{icon} {amenity_key.title()}"
                
                amenity_tag = tk.Label(amenities_frame, text=label, bg='#E0E7FF', fg='#3730A3', font=('Helvetica', 8), padx=6, pady=2)
                amenity_tag.pack(side='left', padx=(0, 4), pady=2)
                amenity_tag.bind('<Button-1>', lambda e: self._show_resource_details(resource))
                displayed += 1
            
            if len(amenities) > 6:
                more_tag = tk.Label(amenities_frame, text=f'+{len(amenities) - 6} more', bg='#F3F4F6', fg='#6B7280', font=('Helvetica', 8), padx=6, pady=2)
                more_tag.pack(side='left', padx=(0, 4), pady=2)
                more_tag.bind('<Button-1>', lambda e: self._show_resource_details(resource))
        
        # Action buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text='Check Availability', command=lambda: self._check_availability(resource), bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=8).pack(side='left', fill='x', expand=True, padx=(0, 6))
        
        tk.Button(btn_frame, text='Book Now', command=lambda: self._book_resource(resource), bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=8).pack(side='right', fill='x', expand=True, padx=(6, 0))
        
        return card

    def _show_resource_details(self, resource):
        """Show resource details modal"""
        resource_id = resource.get('id')
        if not resource_id:
            messagebox.showerror('Error', 'Invalid resource ID')
            return
        
        # Create modal
        modal = tk.Toplevel(self)
        modal.title(f"Resource Details - {resource.get('name', 'Resource')}")
        modal.geometry('700x600')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (700 // 2)
        y = (modal.winfo_screenheight() // 2) - (600 // 2)
        modal.geometry(f'700x600+{x}+{y}')
        
        # Header
        resource_type = (resource.get('type', 'equipment') or 'equipment').lower()
        type_icons = {
            'classroom': '🏫',
            'lab': '🔬',
            'auditorium': '🎭',
            'equipment': '⚙️',
            'conference': '💼',
            'sports': '⚽'
        }
        icon = type_icons.get(resource_type, '📦')
        
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=self.colors.get('secondary', '#3498DB'))
        header_content.pack(padx=20, pady=20)
        
        tk.Label(header_content, text=icon, bg=self.colors.get('secondary', '#3498DB'), font=('Helvetica', 36)).pack()
        tk.Label(header_content, text=resource.get('name', 'Unnamed Resource'), bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=(8, 0))
        tk.Label(header_content, text=f"Code: {resource.get('code', resource.get('id', 'N/A'))}", bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 10)).pack(pady=(4, 0))
        
        # Scrollable content
        canvas = tk.Canvas(modal, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(modal, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg='white')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=content, anchor='nw')
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Details
        details_frame = tk.Frame(content, bg='white')
        details_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Basic info
        tk.Label(details_frame, text='Basic Information', bg='white', fg='#1F2937', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 12))
        
        info_grid = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        info_grid.pack(fill='x', pady=(0, 20))
        
        info_content = tk.Frame(info_grid, bg='#F9FAFB')
        info_content.pack(padx=16, pady=12)
        
        self._add_detail_item(info_content, 'Type:', resource_type.title())
        self._add_detail_item(info_content, 'Capacity:', str(resource.get('capacity', 'N/A')))
        self._add_detail_item(info_content, 'Location:', resource.get('location', resource.get('building', 'N/A')))
        
        # Description
        description = resource.get('description', 'No description available')
        tk.Label(details_frame, text='Description', bg='white', fg='#1F2937', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 12))
        tk.Label(details_frame, text=description, bg='white', fg='#6B7280', font=('Helvetica', 10), wraplength=620, justify='left').pack(anchor='w', pady=(0, 20))
        
        # Amenities
        amenities = resource.get('amenities', [])
        if amenities:
            tk.Label(details_frame, text='Available Amenities', bg='white', fg='#1F2937', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 12))
            
            amenities_grid = tk.Frame(details_frame, bg='white')
            amenities_grid.pack(fill='x', pady=(0, 20))
            
            for amenity in amenities:
                amenity_row = tk.Frame(amenities_grid, bg='white')
                amenity_row.pack(fill='x', pady=2)
                tk.Label(amenity_row, text='✓', bg='white', fg=self.colors.get('success', '#27AE60'), font=('Helvetica', 12, 'bold')).pack(side='left', padx=(0, 8))
                tk.Label(amenity_row, text=str(amenity).title(), bg='white', fg='#374151', font=('Helvetica', 10)).pack(side='left')
        
        # Action buttons
        btn_frame = tk.Frame(details_frame, bg='white')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        tk.Button(btn_frame, text='Check Availability', command=lambda: [modal.destroy(), self._check_availability(resource)], bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=10).pack(side='left', fill='x', expand=True, padx=(0, 8))
        tk.Button(btn_frame, text='Book This Resource', command=lambda: [modal.destroy(), self._book_resource(resource)], bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=10).pack(side='right', fill='x', expand=True, padx=(8, 0))

    def _add_detail_item(self, parent, label, value):
        """Add a detail item to modal"""
        row = tk.Frame(parent, bg='#F9FAFB')
        row.pack(fill='x', pady=4)
        tk.Label(row, text=label, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 10), width=15, anchor='w').pack(side='left')
        tk.Label(row, text=str(value), bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(side='left')

    def _check_availability(self, resource):
        """Check resource availability"""
        messagebox.showinfo('Check Availability', 
                          f"Availability calendar for '{resource.get('name', 'Resource')}' would be shown here.\n\n"
                          f"This would display a real-time calendar showing booked and available time slots.")

    def _book_resource(self, resource):
        """Book a resource"""
        messagebox.showinfo('Book Resource', 
                          f"Booking form for '{resource.get('name', 'Resource')}' would open here.\n\n"
                          f"This would allow you to select date, time, and submit a booking request.")

    @staticmethod
    def _parse_dt(text):
        """Parse datetime string"""
        if not text:
            return None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(text[:19], fmt)
            except Exception:
                continue
        return None
