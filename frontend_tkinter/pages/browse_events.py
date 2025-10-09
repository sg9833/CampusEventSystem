import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
import math

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.button_styles import ButtonStyles
from components.search_component import SearchComponent


class BrowseEventsPage(tk.Frame):
    """Browse Events page with search, filters, and grid layout."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors.get('background', '#ECF0F1'))
        self.controller = controller
        self.api = APIClient()
        self.session = SessionManager()

        # Data
        self.all_events = []
        self.filtered_events = []
        self.current_page = 1
        self.items_per_page = 9  # 3x3 grid
        
        # Current filters from SearchComponent
        self.active_filters = {}

        # Layout
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Search Component
        self.grid_rowconfigure(2, weight=1)  # Content
        self.grid_rowconfigure(3, weight=0)  # Pagination
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_search()
        self._build_content()
        self._build_pagination()

        # Load data
        self._load_events()

    def _build_header(self):
        """Build header with title"""
        colors = self.controller.colors
        header = tk.Frame(self, bg='white', height=70, highlightthickness=1, highlightbackground='#E5E7EB')
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)

        container = tk.Frame(header, bg='white')
        container.pack(fill='both', expand=True, padx=20, pady=10)

        # Title
        title_frame = tk.Frame(container, bg='white')
        title_frame.pack(side='left')
        tk.Label(title_frame, text='Browse Events', bg='white', fg=colors.get('primary', '#2C3E50'), font=('Helvetica', 18, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Discover and register for campus events', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')

    def _build_search(self):
        """Build SearchComponent for filtering events"""
        search_frame = tk.Frame(self, bg=self.controller.colors.get('background', '#ECF0F1'))
        search_frame.grid(row=1, column=0, sticky='ew', padx=20, pady=(12, 8))
        
        # Configure SearchComponent for events
        config = {
            'categories': ['Academic', 'Sports', 'Cultural', 'Workshop', 'Seminar', 'Conference', 'Social'],
            'statuses': ['Upcoming', 'Active', 'Past', 'Approved', 'Cancelled'],
            'sort_options': ['Date', 'Popularity', 'Name', 'Attendees'],
            'show_date_filter': True,
            'show_category_filter': True,
            'show_status_filter': True,
            'placeholder': 'Search events by name, organizer, or description...'
        }
        
        # Create search component
        self.search_component = SearchComponent(
            search_frame,
            on_search_callback=self._handle_search,
            config=config,
            colors=self.controller.colors
        )
        self.search_component.pack(fill='x')

    def _build_content(self):
        """Build scrollable content area for event cards"""
        # Content container (scrollable)
        content_container = tk.Frame(self, bg=self.controller.colors.get('background', '#ECF0F1'))
        content_container.grid(row=2, column=0, sticky='nsew', padx=20)

        canvas = tk.Canvas(content_container, bg=self.controller.colors.get('background', '#ECF0F1'), highlightthickness=0)
        vscroll = ttk.Scrollbar(content_container, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)
        vscroll.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        self.content = tk.Frame(canvas, bg=self.controller.colors.get('background', '#ECF0F1'))
        canvas.create_window((0, 0), window=self.content, anchor='nw')
        self.content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Spinner
        self.spinner = ttk.Progressbar(self.content, mode='indeterminate')

    def _build_pagination(self):
        """Build pagination controls"""
        self.pagination = tk.Frame(self, bg=self.controller.colors.get('background', '#ECF0F1'))
        self.pagination.grid(row=3, column=0, sticky='ew', padx=20, pady=(8, 16))

    def _load_events(self):
        """Load events from API"""
        self._show_spinner()

        def worker():
            try:
                self.all_events = self.api.get('events') or []
                self.filtered_events = self.all_events.copy()
            except Exception as e:
                self.all_events = []
                self.filtered_events = []
                
                def show_error():
                    messagebox.showerror('Error', f'Failed to load events: {str(e)}')
                self.after(0, show_error)

            def done():
                self._hide_spinner()
                self._apply_filters()

            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()

    def _handle_search(self, search_text, filters):
        """Handle search and filters from SearchComponent"""
        self.active_filters = filters
        
        # Filter events
        filtered = self.all_events.copy()

        # Search filter
        if search_text:
            search_query = search_text.lower().strip()
            filtered = [e for e in filtered if 
                       search_query in (e.get('title', '') or '').lower() or 
                       search_query in (e.get('description', '') or '').lower() or
                       search_query in (e.get('organizer_name', '') or '').lower()]

        # Date range filter
        if 'date_range' in filters:
            start_date = filters['date_range'].get('start')
            end_date = filters['date_range'].get('end')
            if start_date and end_date:
                filtered = [e for e in filtered if 
                           self._parse_dt(e.get('start_time')) and 
                           start_date <= self._parse_dt(e.get('start_time')).date() <= end_date]

        # Category filter
        if 'categories' in filters and filters['categories']:
            filtered = [e for e in filtered if 
                       (e.get('category', '') or '').lower() in [c.lower() for c in filters['categories']]]

        # Status filter
        if 'status' in filters and filters['status']:
            status = filters['status'].lower()
            now = datetime.now()
            if status == 'upcoming':
                filtered = [e for e in filtered if self._parse_dt(e.get('start_time')) and self._parse_dt(e.get('start_time')) > now]
            elif status == 'past':
                filtered = [e for e in filtered if self._parse_dt(e.get('end_time')) and self._parse_dt(e.get('end_time')) < now]
            elif status == 'active':
                filtered = [e for e in filtered if (e.get('status', '') or '').lower() in ('approved', 'active')]
            elif status == 'approved':
                filtered = [e for e in filtered if (e.get('status', '') or '').lower() == 'approved']
            elif status == 'cancelled':
                filtered = [e for e in filtered if (e.get('status', '') or '').lower() == 'cancelled']

        # Sort events
        sort_by = filters.get('sort', 'Date').lower()
        if sort_by == 'date':
            filtered.sort(key=lambda e: self._parse_dt(e.get('start_time')) or datetime.max)
        elif sort_by == 'popularity':
            filtered.sort(key=lambda e: e.get('registered_count', 0), reverse=True)
        elif sort_by == 'name':
            filtered.sort(key=lambda e: (e.get('title', '') or '').lower())
        elif sort_by == 'attendees':
            filtered.sort(key=lambda e: e.get('registered_count', 0), reverse=True)

        self.filtered_events = filtered
        self.current_page = 1
        self._render_events()

    def _render_events(self):
        """Render event cards in grid layout"""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()

        # Calculate pagination
        total_events = len(self.filtered_events)
        total_pages = math.ceil(total_events / self.items_per_page) if total_events > 0 else 1
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_events = self.filtered_events[start_idx:end_idx]

        # Show results count
        results_frame = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        results_frame.pack(fill='x', pady=(0, 12))
        tk.Label(results_frame, text=f'Showing {len(page_events)} of {total_events} events', bg=self.controller.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 10)).pack(side='left')

        if not page_events:
            # No events found
            no_events = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            no_events.pack(fill='both', expand=True, pady=20)
            tk.Label(no_events, text='🔍', bg='white', font=('Helvetica', 48)).pack(pady=(40, 10))
            tk.Label(no_events, text='No events found', bg='white', fg='#374151', font=('Helvetica', 16, 'bold')).pack()
            tk.Label(no_events, text='Try adjusting your filters or search query', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(pady=(4, 40))
        else:
            # Create grid container
            grid_frame = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
            grid_frame.pack(fill='both', expand=True)

            # Configure grid columns
            for i in range(3):
                grid_frame.grid_columnconfigure(i, weight=1, uniform='col')

            # Render event cards in 3-column grid
            for idx, event in enumerate(page_events):
                row = idx // 3
                col = idx % 3
                card = self._create_event_card(grid_frame, event)
                card.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')

        # Update pagination
        self._update_pagination(total_pages)

    def _create_event_card(self, parent, event):
        """Create an individual event card"""
        colors = self.controller.colors
        
        # Card container
        card = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB', cursor='hand2')
        card.bind('<Button-1>', lambda e: self._show_event_details(event))

        # Card header with category tag
        header = tk.Frame(card, bg='white')
        header.pack(fill='x', padx=12, pady=(12, 0))
        
        category = (event.get('category', 'General') or 'General').title()
        category_colors = {
            'Academic': '#3498DB',
            'Sports': '#27AE60',
            'Cultural': '#9B59B6',
            'Workshop': '#F39C12',
            'Seminar': '#E74C3C',
            'General': '#95A5A6'
        }
        cat_color = category_colors.get(category, '#95A5A6')
        
        tag = tk.Label(header, text=category, bg=cat_color, fg='white', font=('Helvetica', 8, 'bold'), padx=8, pady=2)
        tag.pack(side='left')
        
        # Status badge
        status = (event.get('status', 'pending') or 'pending').lower()
        if status == 'approved':
            status_badge = tk.Label(header, text='✓', bg='#D1FAE5', fg='#065F46', font=('Helvetica', 8, 'bold'), padx=6, pady=2)
            status_badge.pack(side='right')

        # Event title
        title = event.get('title', 'Untitled Event')
        title_label = tk.Label(card, text=title, bg='white', fg='#1F2937', font=('Helvetica', 13, 'bold'), wraplength=250, justify='left')
        title_label.pack(anchor='w', padx=12, pady=(8, 4))
        title_label.bind('<Button-1>', lambda e: self._show_event_details(event))

        # Date & time
        start_time = event.get('start_time', 'TBA')
        date_frame = tk.Frame(card, bg='white')
        date_frame.pack(anchor='w', padx=12, pady=2)
        tk.Label(date_frame, text='📅', bg='white', font=('Helvetica', 10)).pack(side='left', padx=(0, 4))
        tk.Label(date_frame, text=start_time, bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(side='left')
        date_frame.bind('<Button-1>', lambda e: self._show_event_details(event))

        # Venue
        venue = event.get('venue', 'TBA')
        venue_frame = tk.Frame(card, bg='white')
        venue_frame.pack(anchor='w', padx=12, pady=2)
        tk.Label(venue_frame, text='📍', bg='white', font=('Helvetica', 10)).pack(side='left', padx=(0, 4))
        tk.Label(venue_frame, text=venue, bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(side='left')
        venue_frame.bind('<Button-1>', lambda e: self._show_event_details(event))

        # Organizer
        organizer = event.get('organizer_name', f"Organizer #{event.get('organizer_id', 'N/A')}")
        org_frame = tk.Frame(card, bg='white')
        org_frame.pack(anchor='w', padx=12, pady=2)
        tk.Label(org_frame, text='👤', bg='white', font=('Helvetica', 10)).pack(side='left', padx=(0, 4))
        tk.Label(org_frame, text=organizer, bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(side='left')
        org_frame.bind('<Button-1>', lambda e: self._show_event_details(event))

        # Capacity
        capacity = event.get('capacity', 'N/A')
        registered = event.get('registered_count', 0)
        available = capacity - registered if isinstance(capacity, int) and isinstance(registered, int) else 'N/A'
        
        capacity_frame = tk.Frame(card, bg='white')
        capacity_frame.pack(anchor='w', padx=12, pady=2)
        tk.Label(capacity_frame, text='🎫', bg='white', font=('Helvetica', 10)).pack(side='left', padx=(0, 4))
        
        if available != 'N/A':
            capacity_text = f"{available} / {capacity} seats available"
            capacity_color = '#27AE60' if available > 0 else '#E74C3C'
        else:
            capacity_text = 'Unlimited seats'
            capacity_color = '#6B7280'
            
        tk.Label(capacity_frame, text=capacity_text, bg='white', fg=capacity_color, font=('Helvetica', 9, 'bold')).pack(side='left')
        capacity_frame.bind('<Button-1>', lambda e: self._show_event_details(event))

        # Separator
        separator = tk.Frame(card, bg='#E5E7EB', height=1)
        separator.pack(fill='x', padx=12, pady=(8, 0))

        # Action buttons
        btn_frame = tk.Frame(card, bg='white')
        btn_frame.pack(fill='x', padx=12, pady=12)

        tk.Button(btn_frame, text='View Details', command=lambda: self._show_event_details(event), bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', fill='x', expand=True, padx=(0, 4))
        
        # Register button (check if already registered or full)
        can_register = True
        register_text = 'Register'
        register_bg = colors.get('secondary', '#3498DB')
        
        if available != 'N/A' and available <= 0:
            can_register = False
            register_text = 'Full'
            register_bg = '#E74C3C'
        
        register_btn = tk.Button(btn_frame, text=register_text, command=lambda: self._register_event(event) if can_register else None, bg=register_bg, fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6, state='normal' if can_register else 'disabled')
        register_btn.pack(side='right', fill='x', expand=True, padx=(4, 0))

        return card

    def _update_pagination(self, total_pages):
        """Update pagination controls"""
        # Clear pagination
        for widget in self.pagination.winfo_children():
            widget.destroy()

        if total_pages <= 1:
            return

        colors = self.controller.colors
        
        # Pagination container
        pag_container = tk.Frame(self.pagination, bg=self.controller.colors.get('background', '#ECF0F1'))
        pag_container.pack()

        # Previous button
        prev_btn = tk.Button(pag_container, text='← Previous', command=self._prev_page, bg='white', fg='#374151', relief='flat', font=('Helvetica', 9), padx=12, pady=6, state='normal' if self.current_page > 1 else 'disabled', highlightthickness=1, highlightbackground='#E5E7EB')
        prev_btn.pack(side='left', padx=(0, 8))

        # Page numbers
        start_page = max(1, self.current_page - 2)
        end_page = min(total_pages, start_page + 4)
        start_page = max(1, end_page - 4)

        for page in range(start_page, end_page + 1):
            if page == self.current_page:
                btn = tk.Button(pag_container, text=str(page), bg=colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6, state='disabled')
            else:
                btn = tk.Button(pag_container, text=str(page), command=lambda p=page: self._goto_page(p), bg='white', fg='#374151', relief='flat', font=('Helvetica', 9), padx=12, pady=6, highlightthickness=1, highlightbackground='#E5E7EB')
            btn.pack(side='left', padx=2)

        # Next button
        next_btn = tk.Button(pag_container, text='Next →', command=self._next_page, bg='white', fg='#374151', relief='flat', font=('Helvetica', 9), padx=12, pady=6, state='normal' if self.current_page < total_pages else 'disabled', highlightthickness=1, highlightbackground='#E5E7EB')
        next_btn.pack(side='left', padx=(8, 0))

        # Page info
        page_info = tk.Label(self.pagination, text=f'Page {self.current_page} of {total_pages}', bg=self.controller.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 9))
        page_info.pack(pady=(4, 0))

    def _prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self._render_events()

    def _next_page(self):
        """Go to next page"""
        total_pages = math.ceil(len(self.filtered_events) / self.items_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self._render_events()

    def _goto_page(self, page):
        """Go to specific page"""
        self.current_page = page
        self._render_events()

    def _show_event_details(self, event):
        """Show event details in a modal dialog"""
        # Create modal window
        modal = tk.Toplevel(self)
        modal.title('Event Details')
        modal.geometry('500x600')
        modal.configure(bg='white')
        modal.transient(self)
        modal.grab_set()

        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (600 // 2)
        modal.geometry(f'500x600+{x}+{y}')

        # Scrollable content
        canvas = tk.Canvas(modal, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(modal, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg='white')

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        canvas.create_window((0, 0), window=content, anchor='nw')
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Content
        colors = self.controller.colors
        
        # Header
        header = tk.Frame(content, bg=colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        tk.Label(header, text=event.get('title', 'Untitled Event'), bg=colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 16, 'bold'), wraplength=450, justify='left').pack(padx=20, pady=20)

        # Details container
        details = tk.Frame(content, bg='white')
        details.pack(fill='both', expand=True, padx=20, pady=20)

        def detail_row(icon, label, value):
            row = tk.Frame(details, bg='white')
            row.pack(fill='x', pady=6)
            tk.Label(row, text=icon, bg='white', font=('Helvetica', 12)).pack(side='left', padx=(0, 8))
            info_frame = tk.Frame(row, bg='white')
            info_frame.pack(side='left', fill='x', expand=True)
            tk.Label(info_frame, text=label, bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w')
            tk.Label(info_frame, text=value, bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w')

        detail_row('📅', 'Start Time', event.get('start_time', 'TBA'))
        detail_row('🕐', 'End Time', event.get('end_time', 'TBA'))
        detail_row('📍', 'Venue', event.get('venue', 'TBA'))
        detail_row('👤', 'Organizer', event.get('organizer_name', f"User #{event.get('organizer_id', 'N/A')}"))
        detail_row('🏷️', 'Category', (event.get('category', 'General') or 'General').title())
        
        capacity = event.get('capacity', 'Unlimited')
        registered = event.get('registered_count', 0)
        detail_row('🎫', 'Capacity', f"{registered} / {capacity}" if capacity != 'Unlimited' else 'Unlimited')
        
        # Description
        tk.Label(details, text='Description', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(12, 4))
        desc_frame = tk.Frame(details, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        desc_frame.pack(fill='x', pady=(0, 12))
        desc_text = event.get('description', 'No description available')
        tk.Label(desc_frame, text=desc_text, bg='#F9FAFB', fg='#374151', font=('Helvetica', 10), wraplength=420, justify='left').pack(padx=12, pady=12)

        # Action buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(btn_frame, text='Close', command=modal.destroy, bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 10), padx=20, pady=8).pack(side='left', fill='x', expand=True, padx=(0, 4))
        tk.Button(btn_frame, text='Register for Event', command=lambda: [self._register_event(event), modal.destroy()], bg=colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=8).pack(side='right', fill='x', expand=True, padx=(4, 0))

    def _register_event(self, event):
        """Register for an event"""
        event_id = event.get('id')
        if not event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return

        try:
            response = self.api.post(f'events/{event_id}/register', {})
            messagebox.showinfo('Success', f"Successfully registered for '{event.get('title', 'Event')}'!")
            # Reload events to update counts
            self._load_events()
        except Exception as e:
            error_msg = str(e)
            if 'already registered' in error_msg.lower():
                messagebox.showwarning('Already Registered', 'You are already registered for this event')
            elif 'full' in error_msg.lower() or 'capacity' in error_msg.lower():
                messagebox.showerror('Event Full', 'This event has reached maximum capacity')
            else:
                messagebox.showerror('Error', f'Failed to register: {error_msg}')

    # Utilities
    def _show_spinner(self):
        try:
            self.spinner.pack(fill='x', padx=16, pady=(16, 0))
            self.spinner.start(10)
        except Exception:
            pass

    def _hide_spinner(self):
        try:
            self.spinner.stop()
            self.spinner.pack_forget()
        except Exception:
            pass

    @staticmethod
    def _parse_dt(text):
        if not text:
            return None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(text[:19], fmt)
            except Exception:
                continue
        return None
