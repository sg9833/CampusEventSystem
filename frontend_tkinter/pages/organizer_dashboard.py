import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.button_styles import ButtonStyles
from utils.canvas_button import create_primary_button, create_secondary_button, create_success_button, create_danger_button, create_warning_button


class OrganizerDashboard(tk.Frame):
    """Organizer Dashboard with sidebar navigation and dynamic content area."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors.get('background', '#ECF0F1'))
        self.controller = controller
        self.api = APIClient()
        self.session = SessionManager()

        # Data caches
        self.my_events = []
        self.event_registrations = {}
        self.resource_requests = []
        
        # Auto-refresh tracking
        self.auto_refresh_enabled = True
        self.auto_refresh_interval = 30000  # 30 seconds
        self.refresh_timer = None
        self.current_view = 'dashboard'

        # Layout: 1 row, 2 columns (sidebar, main)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_main()

        # Initial content
        self._load_all_data_then(self._render_dashboard)
        
        # Start auto-refresh
        self._start_auto_refresh()

    # Sidebar
    def _build_sidebar(self):
        colors = self.controller.colors
        sidebar = tk.Frame(self, width=200, bg=colors.get('primary', '#2C3E50'))
        sidebar.grid(row=0, column=0, sticky='nsw')
        sidebar.grid_propagate(False)

        u = self.session.get_user() or {}
        name = u.get('username') or u.get('email') or 'Organizer'
        role = (self.session.get_role() or 'ORGANIZER').title()

        # Profile section
        profile = tk.Frame(sidebar, bg=colors.get('primary', '#2C3E50'))
        profile.pack(fill='x', pady=(16, 8))
        tk.Label(profile, text='👔', bg=colors.get('primary', '#2C3E50'), fg='white', font=('Helvetica', 26)).pack()
        tk.Label(profile, text=name, bg=colors.get('primary', '#2C3E50'), fg='white', font=('Helvetica', 12, 'bold')).pack(pady=(6, 0))
        tk.Label(profile, text=role, bg=colors.get('primary', '#2C3E50'), fg='#D1D5DB', font=('Helvetica', 10)).pack()

        # Nav menu
        menu = tk.Frame(sidebar, bg=colors.get('primary', '#2C3E50'))
        menu.pack(fill='both', expand=True, pady=(12, 12))

        def add_btn(text, cmd, icon='•'):
            # Create canvas-based button for macOS compatibility
            btn_frame = tk.Frame(menu, bg=colors.get('primary', '#2C3E50'))
            btn_frame.pack(fill='x', pady=2)
            
            canvas = tk.Canvas(btn_frame, width=200, height=40, bg=colors.get('primary', '#2C3E50'), 
                             highlightthickness=0, cursor='hand2')
            canvas.pack(fill='x')
            
            # Button background (initially same as sidebar)
            rect = canvas.create_rectangle(0, 0, 200, 40, fill=colors.get('primary', '#2C3E50'), 
                                         outline='', tags='btn')
            # Button text
            text_label = f"{icon}  {text}"
            text_id = canvas.create_text(16, 20, text=text_label, fill='#FFFFFF', 
                                        font=('Helvetica', 11), anchor='w', tags='btn')
            
            # Hover effects
            def on_enter(e):
                canvas.itemconfig(rect, fill=colors.get('secondary', '#3498DB'))
            
            def on_leave(e):
                canvas.itemconfig(rect, fill=colors.get('primary', '#2C3E50'))
            
            def on_click(e):
                cmd()
            
            canvas.tag_bind('btn', '<Enter>', on_enter)
            canvas.tag_bind('btn', '<Leave>', on_leave)
            canvas.tag_bind('btn', '<Button-1>', on_click)

        add_btn('Dashboard', self._render_dashboard, icon='🏠')
        add_btn('Create Event', self._render_create_event, icon='➕')
        add_btn('My Events', self._render_my_events, icon='📋')
        add_btn('Event Registrations', self._render_event_registrations, icon='👥')
        add_btn('Book Resources', self._render_book_resources, icon='📚')
        add_btn('My Bookings', self._render_my_bookings, icon='📅')
        add_btn('Resource Requests', self._render_resource_requests, icon='📦')
        add_btn('Analytics', self._render_analytics, icon='📊')
        add_btn('Profile', self._render_profile, icon='⚙️')
        add_btn('Logout', self._logout, icon='🚪')

    # Main area
    def _build_main(self):
        colors = self.controller.colors
        main = tk.Frame(self, bg=self.controller.colors.get('background', '#ECF0F1'))
        main.grid(row=0, column=1, sticky='nsew')
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
        self.main = main

        # Top bar
        top = tk.Frame(main, bg='white', height=56, highlightthickness=1, highlightbackground='#E5E7EB')
        top.grid(row=0, column=0, sticky='ew')
        top.grid_propagate(False)

        user = self.session.get_user() or {}
        welcome = tk.Label(top, text=f"Welcome, {user.get('username') or 'Organizer'}", bg='white', fg=colors.get('primary', '#2C3E50'), font=('Helvetica', 13, 'bold'))
        welcome.pack(side='left', padx=16)

        # Search bar with explicit light mode colors
        search_frame = tk.Frame(top, bg='white')
        search_frame.pack(side='right', padx=16)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               bg='white', fg='#1F2937',  # White background, dark text
                               insertbackground='#1F2937',  # Cursor color
                               highlightthickness=1, highlightbackground='#D1D5DB',
                               highlightcolor='#3B82F6')  # Blue focus border
        search_entry.pack(side='left')
        search_btn = create_primary_button(search_frame, 'Search', self._on_search, width=80, height=30)
        search_btn.pack(side='left', padx=(6, 0))

        # Notifications icon
        notif_btn = create_secondary_button(top, '🔔', lambda: messagebox.showinfo('Notifications', 'No new notifications'), width=40, height=30)
        notif_btn.pack(side='right', padx=(0, 8))

        # Content container (scrollable)
        content_container = tk.Frame(main, bg=self.controller.colors.get('background', '#ECF0F1'))
        content_container.grid(row=1, column=0, sticky='nsew')

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

    # Data loading
    def _load_all_data_then(self, callback):
        self._show_spinner()

        def worker():
            errors = []
            try:
                # Get ALL events from backend
                all_events = self.api.get('events') or []
                
                # Filter to show only events created by this organizer
                user_data = self.session.get_user()
                user_id = user_data.get('id') or user_data.get('user_id') if user_data else None
                
                if user_id:
                    # Filter events where organizer_id matches current user's ID
                    # Backend returns 'organizerId' (camelCase) in Event model
                    self.my_events = [
                        event for event in all_events 
                        if event.get('organizerId') == user_id or event.get('organizer_id') == user_id
                    ]
                else:
                    self.my_events = []
            except Exception as e:
                errors.append(('my_events', str(e)))
                self.my_events = []
            
            # Load registrations for each event
            for event in self.my_events:
                event_id = event.get('id')
                if event_id:
                    try:
                        registrations = self.api.get(f'events/{event_id}/registrations') or []
                        self.event_registrations[event_id] = registrations
                    except Exception as e:
                        errors.append((f'registrations_{event_id}', str(e)))
                        self.event_registrations[event_id] = []
            
            try:
                # Resource requests endpoint may vary - placeholder
                self.resource_requests = self.api.get('resources/requests') or []
            except Exception as e:
                errors.append(('resource_requests', str(e)))
                self.resource_requests = []

            def done():
                self._hide_spinner()
                if errors:
                    # Show first error non-blocking
                    self._info_banner(f"Some data failed to load: {errors[0][0]}: {errors[0][1]}")
                callback()

            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()

    # Auto-refresh methods
    def _start_auto_refresh(self):
        """Start automatic refresh of data every 30 seconds"""
        if self.auto_refresh_enabled:
            self._schedule_refresh()
    
    def _schedule_refresh(self):
        """Schedule the next refresh"""
        if self.refresh_timer:
            self.after_cancel(self.refresh_timer)
        self.refresh_timer = self.after(self.auto_refresh_interval, self._auto_refresh)
    
    def _auto_refresh(self):
        """Auto-refresh data in background"""
        if not self.auto_refresh_enabled:
            return
        
        def worker():
            try:
                # Silently refresh my events
                all_events = self.api.get('events') or []
                user_data = self.session.get_user()
                user_id = user_data.get('id') or user_data.get('user_id') if user_data else None
                
                if user_id:
                    self.my_events = [
                        event for event in all_events 
                        if event.get('organizerId') == user_id or event.get('organizer_id') == user_id
                    ]
                    
                # Refresh view if needed (but NOT when user is creating an event)
                if self.current_view == 'dashboard':
                    self.after(0, self._render_dashboard)
                elif self.current_view == 'my_events':
                    self.after(0, self._render_my_events)
                # Do NOT auto-refresh when on create_event, event_registrations, book_resources, etc.
                # to avoid interrupting user input
                    
            except Exception:
                pass  # Fail silently for background refresh
            
            # Schedule next refresh
            self.after(0, self._schedule_refresh)
        
        threading.Thread(target=worker, daemon=True).start()
    
    def _manual_refresh(self):
        """Manual refresh triggered by user"""
        self._load_all_data_then(lambda: None)
        # Re-render current view
        if self.current_view == 'dashboard':
            self._render_dashboard()
        elif self.current_view == 'my_events':
            self._render_my_events()
    
    def _stop_auto_refresh(self):
        """Stop auto-refresh (call this when dashboard is destroyed)"""
        self.auto_refresh_enabled = False
        if self.refresh_timer:
            self.after_cancel(self.refresh_timer)
    
    def destroy(self):
        """Override destroy to stop auto-refresh"""
        self._stop_auto_refresh()
        super().destroy()

    # Views
    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _info_banner(self, text):
        colors = self.controller.colors
        bar = tk.Frame(self.content, bg='#FEF3C7', highlightthickness=1, highlightbackground='#FCD34D')
        bar.pack(fill='x', padx=16, pady=(12, 0))
        tk.Label(bar, text=text, bg='#FEF3C7', fg='#92400E').pack(side='left', padx=8, pady=6)

    def _render_dashboard(self):
        self.current_view = 'dashboard'
        self._clear_content()
        colors = self.controller.colors
        
        # Add refresh button at top
        top_bar = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        top_bar.pack(fill='x', padx=16, pady=(12, 0))
        tk.Label(top_bar, text='Organizer Dashboard', bg=self.controller.colors.get('background', '#ECF0F1'), 
                font=('Helvetica', 16, 'bold'), fg=colors.get('primary', '#2C3E50')).pack(side='left')
        
        refresh_btn = create_secondary_button(top_bar, '🔄 Refresh', self._manual_refresh, width=100)
        refresh_btn.pack(side='right')

        # Stats cards
        stats = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        stats.pack(fill='x', padx=16, pady=(16, 8))
        for i in range(3):
            stats.grid_columnconfigure(i, weight=1)

        def card(parent, title, value, color):
            f = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            tk.Label(f, text=title, bg='white', fg='#6B7280').pack(anchor='w', padx=12, pady=(10, 0))
            tk.Label(f, text=str(value), bg='white', fg=color, font=('Helvetica', 20, 'bold')).pack(anchor='w', padx=12, pady=(0, 12))
            return f

        total_events = len(self.my_events)
        pending_events = len([e for e in self.my_events if (e.get('status') or '').lower() == 'pending'])
        active_events = len([e for e in self.my_events if (e.get('status') or '').lower() in ('approved', 'active')])

        c1 = card(stats, 'Total Events Created', total_events, colors.get('secondary', '#3498DB'))
        c2 = card(stats, 'Pending Approvals', pending_events, colors.get('warning', '#F39C12'))
        c3 = card(stats, 'Active Events', active_events, colors.get('success', '#27AE60'))
        c1.grid(row=0, column=0, sticky='ew', padx=(0, 8))
        c2.grid(row=0, column=1, sticky='ew', padx=8)
        c3.grid(row=0, column=2, sticky='ew', padx=(8, 0))

        # Event status cards
        status_section = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        status_section.pack(fill='x', padx=16, pady=(8, 8))
        tk.Label(status_section, text='Events by Status', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold'), fg=colors.get('primary', '#2C3E50')).pack(anchor='w', pady=(4, 6))

        status_cards = tk.Frame(status_section, bg=self.controller.colors.get('background', '#ECF0F1'))
        status_cards.pack(fill='x')
        for i in range(3):
            status_cards.grid_columnconfigure(i, weight=1)

        approved = len([e for e in self.my_events if (e.get('status') or '').lower() == 'approved'])
        pending = len([e for e in self.my_events if (e.get('status') or '').lower() == 'pending'])
        rejected = len([e for e in self.my_events if (e.get('status') or '').lower() == 'rejected'])

        def status_card(parent, title, count, bg_color, text_color):
            f = tk.Frame(parent, bg=bg_color, highlightthickness=1, highlightbackground='#E5E7EB')
            tk.Label(f, text=title, bg=bg_color, fg=text_color, font=('Helvetica', 11)).pack(pady=(12, 4))
            tk.Label(f, text=str(count), bg=bg_color, fg=text_color, font=('Helvetica', 24, 'bold')).pack(pady=(0, 12))
            return f

        sc1 = status_card(status_cards, 'Approved', approved, '#D1FAE5', '#065F46')
        sc2 = status_card(status_cards, 'Pending', pending, '#FEF3C7', '#92400E')
        sc3 = status_card(status_cards, 'Rejected', rejected, '#FEE2E2', '#991B1B')
        sc1.grid(row=0, column=0, sticky='ew', padx=(0, 8))
        sc2.grid(row=0, column=1, sticky='ew', padx=8)
        sc3.grid(row=0, column=2, sticky='ew', padx=(8, 0))

        # Quick actions
        actions = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        actions.pack(fill='x', padx=16, pady=(8, 8))
        tk.Label(actions, text='Quick Actions', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold'), fg=colors.get('primary', '#2C3E50')).pack(anchor='w', pady=(4, 6))

        action_buttons = tk.Frame(actions, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        action_buttons.pack(fill='x', pady=(0, 0))
        
        btn_frame = tk.Frame(action_buttons, bg='white')
        btn_frame.pack(padx=12, pady=12)
        
        create_btn = create_primary_button(btn_frame, '➕ Create New Event', self._render_create_event, width=180, height=40)
        create_btn.pack(side='left', padx=(0, 8))
        reg_btn = create_success_button(btn_frame, '👥 Check Registrations', self._render_event_registrations, width=200, height=40)
        reg_btn.pack(side='left', padx=8)
        analytics_btn = create_warning_button(btn_frame, '📊 View Analytics', self._render_analytics, width=160, height=40)
        analytics_btn.pack(side='left', padx=(8, 0))

        # Calendar view of scheduled events
        calendar = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        calendar.pack(fill='both', expand=True, padx=16, pady=(8, 16))
        tk.Label(calendar, text='Scheduled Events', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold'), fg=colors.get('primary', '#2C3E50')).pack(anchor='w', pady=(4, 6))

        calendar_frame = tk.Frame(calendar, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        calendar_frame.pack(fill='both', expand=True)

        # Sort events by date
        events_sorted = sorted(self.my_events, key=lambda e: self._parse_dt(e.get('start_time')) or datetime.max)
        
        if not events_sorted:
            tk.Label(calendar_frame, text='No scheduled events', bg='white', fg='#6B7280').pack(padx=12, pady=12)
        else:
            # Header
            header = tk.Frame(calendar_frame, bg='#F9FAFB')
            header.pack(fill='x')
            for i, h in enumerate(['Event', 'Date & Time', 'Venue', 'Status', 'Registrations']):
                tk.Label(header, text=h, bg='#F9FAFB', fg='#374151', font=('Helvetica', 10, 'bold')).grid(row=0, column=i, sticky='w', padx=8, pady=8)
                header.grid_columnconfigure(i, weight=1 if i == 0 else 0)

            # Event rows
            for ev in events_sorted:
                row = tk.Frame(calendar_frame, bg='white')
                row.pack(fill='x', padx=4, pady=2)
                
                title = ev.get('title') or 'Untitled Event'
                start_time = ev.get('start_time') or 'N/A'
                venue = ev.get('venue') or 'N/A'
                status = (ev.get('status') or 'pending').title()
                event_id = ev.get('id')
                
                # Handle both dict and list response formats for registration count
                registrations_data = self.event_registrations.get(event_id, [])
                if isinstance(registrations_data, dict):
                    reg_count = registrations_data.get('count', 0)
                elif isinstance(registrations_data, list):
                    reg_count = len(registrations_data)
                else:
                    reg_count = 0
                
                # Status color
                status_colors = {
                    'Approved': '#27AE60',
                    'Pending': '#F39C12',
                    'Rejected': '#E74C3C'
                }
                status_color = status_colors.get(status, '#6B7280')
                
                tk.Label(row, text=title, bg='white', font=('Helvetica', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=8)
                tk.Label(row, text=start_time, bg='white', fg='#6B7280').grid(row=0, column=1, sticky='w', padx=8)
                tk.Label(row, text=venue, bg='white', fg='#6B7280').grid(row=0, column=2, sticky='w', padx=8)
                tk.Label(row, text=status, bg='white', fg=status_color, font=('Helvetica', 10, 'bold')).grid(row=0, column=3, sticky='w', padx=8)
                tk.Label(row, text=f'{reg_count} attendees', bg='white', fg='#6B7280').grid(row=0, column=4, sticky='w', padx=8)

    def _render_create_event(self):
        self.current_view = 'create_event'
        self._clear_content()
        colors = self.controller.colors
        
        tk.Label(self.content, text='Create New Event', bg=self.controller.colors.get('background', '#ECF0F1'), 
                fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        form_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        form_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        
        # Form container
        form = tk.Frame(form_frame, bg='white')
        form.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Event Title with explicit light mode colors
        tk.Label(form, text='Event Title *', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=(0, 4))
        title_entry = tk.Entry(form, width=50, bg='white', fg='#1F2937', insertbackground='#1F2937',
                              highlightthickness=1, highlightbackground='#D1D5DB', highlightcolor='#3B82F6')
        title_entry.grid(row=1, column=0, sticky='ew', pady=(0, 12))
        
        # Description with explicit light mode colors
        tk.Label(form, text='Description *', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=(0, 4))
        desc_text = tk.Text(form, width=50, height=5, bg='white', fg='#1F2937', insertbackground='#1F2937',
                           highlightthickness=1, highlightbackground='#D1D5DB', highlightcolor='#3B82F6')
        desc_text.grid(row=3, column=0, sticky='ew', pady=(0, 12))
        
        # Start Time with explicit light mode colors
        tk.Label(form, text='Start Time (YYYY-MM-DD HH:MM:SS) *', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).grid(row=4, column=0, sticky='w', pady=(0, 4))
        start_entry = tk.Entry(form, width=50, bg='white', fg='#1F2937', insertbackground='#1F2937',
                              highlightthickness=1, highlightbackground='#D1D5DB', highlightcolor='#3B82F6')
        start_entry.insert(0, '2025-10-20 09:00:00')  # Default placeholder
        start_entry.grid(row=5, column=0, sticky='ew', pady=(0, 12))
        
        # End Time with explicit light mode colors
        tk.Label(form, text='End Time (YYYY-MM-DD HH:MM:SS) *', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).grid(row=6, column=0, sticky='w', pady=(0, 4))
        end_entry = tk.Entry(form, width=50, bg='white', fg='#1F2937', insertbackground='#1F2937',
                            highlightthickness=1, highlightbackground='#D1D5DB', highlightcolor='#3B82F6')
        end_entry.insert(0, '2025-10-20 17:00:00')  # Default placeholder
        end_entry.grid(row=7, column=0, sticky='ew', pady=(0, 12))
        
        # Venue with explicit light mode colors
        tk.Label(form, text='Venue *', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).grid(row=8, column=0, sticky='w', pady=(0, 4))
        venue_entry = tk.Entry(form, width=50, bg='white', fg='#1F2937', insertbackground='#1F2937',
                              highlightthickness=1, highlightbackground='#D1D5DB', highlightcolor='#3B82F6')
        venue_entry.grid(row=9, column=0, sticky='ew', pady=(0, 12))
        
        # Capacity with explicit light mode colors
        tk.Label(form, text='Capacity', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).grid(row=10, column=0, sticky='w', pady=(0, 4))
        capacity_entry = tk.Entry(form, width=50, bg='white', fg='#1F2937', insertbackground='#1F2937',
                                 highlightthickness=1, highlightbackground='#D1D5DB', highlightcolor='#3B82F6')
        capacity_entry.grid(row=11, column=0, sticky='ew', pady=(0, 12))
        
        form.grid_columnconfigure(0, weight=1)
        
        # Submit button
        def submit_event():
            title = title_entry.get().strip()
            description = desc_text.get('1.0', 'end').strip()
            start_time = start_entry.get().strip()
            end_time = end_entry.get().strip()
            venue = venue_entry.get().strip()
            capacity = capacity_entry.get().strip()
            
            if not all([title, description, start_time, end_time, venue]):
                messagebox.showerror('Error', 'Please fill all required fields')
                return
            
            # Get current user's ID from session
            user_data = self.session.get_user()
            if not user_data:
                messagebox.showerror('Error', 'User session not found. Please log in again.')
                return
            
            # Get user ID - could be 'id' or 'user_id' depending on how session was set
            user_id = user_data.get('id') or user_data.get('user_id')
            if not user_id:
                messagebox.showerror('Error', 'User ID not found in session. Please log in again.')
                return
            
            # Convert datetime format: "YYYY-MM-DD HH:MM:SS" to "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
            # Replace space with 'T' for Java LocalDateTime
            start_time_iso = start_time.replace(' ', 'T')
            end_time_iso = end_time.replace(' ', 'T')
            
            # Build payload matching backend DTO (CreateEventRequest.java)
            payload = {
                'title': title,
                'description': description,
                'organizerId': user_id,  # REQUIRED by backend
                'startTime': start_time_iso,  # camelCase with ISO 8601 format
                'endTime': end_time_iso,      # camelCase with ISO 8601 format
                'venue': venue
            }
            
            # Note: capacity is NOT in CreateEventRequest.java DTO, so it won't be sent
            # If you need capacity, update the backend DTO first
            
            try:
                response = self.api.post('events', payload)
                messagebox.showinfo('Success', f"Event '{title}' created successfully!")
                self._load_all_data_then(self._render_my_events)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to create event: {str(e)}')
        
        btn_frame = tk.Frame(form, bg='white')
        btn_frame.grid(row=12, column=0, sticky='ew', pady=(12, 0))
        
        create_event_btn = create_primary_button(btn_frame, 'Create Event', submit_event, width=140, height=44)
        create_event_btn.pack(side='left')
        cancel_btn = create_secondary_button(btn_frame, 'Cancel', self._render_dashboard, width=100, height=44)
        cancel_btn.pack(side='left', padx=(8, 0))

    def _render_my_events(self):
        self.current_view = 'my_events'
        self._clear_content()
        
        # Header with event count and refresh button
        header_frame = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        header_frame.pack(fill='x', padx=16, pady=(16, 8))
        
        # Add refresh button
        refresh_btn = create_secondary_button(header_frame, '🔄 Refresh', self._manual_refresh, width=100)
        refresh_btn.pack(side='right')
        
        tk.Label(
            header_frame, 
            text='My Events', 
            bg=self.controller.colors.get('background', '#ECF0F1'),
            fg='#1F2937',  # Dark text for light mode visibility
            font=('Helvetica', 14, 'bold')
        ).pack(side='left')
        
        tk.Label(
            header_frame, 
            text=f'({len(self.my_events)} events)', 
            bg=self.controller.colors.get('background', '#ECF0F1'), 
            font=('Helvetica', 12),
            fg='#6B7280'
        ).pack(side='left', padx=(8, 0))
        
        if not self.my_events:
            no_events = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            no_events.pack(fill='both', expand=True, padx=16, pady=(0, 16))
            tk.Label(no_events, text='No events created yet', bg='white', fg='#6B7280').pack(padx=12, pady=40)
            first_event_btn = create_primary_button(no_events, 'Create Your First Event', self._render_create_event, width=200, height=40)
            first_event_btn.pack(pady=(0, 40))
        else:
            self._render_events_table(self.my_events, show_actions=True)

    def _render_event_registrations(self):
        self.current_view = 'event_registrations'
        self._clear_content()
        tk.Label(self.content, text='Event Registrations', bg=self.controller.colors.get('background', '#ECF0F1'), 
                fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        # Show registrations grouped by event
        for event in self.my_events:
            event_id = event.get('id')
            registrations_data = self.event_registrations.get(event_id, [])
            
            # Handle both dict and list response formats
            # Backend returns: {'count': X, 'registrations': [...]}
            if isinstance(registrations_data, dict):
                reg_count = registrations_data.get('count', 0)
                registrations = registrations_data.get('registrations', [])
            elif isinstance(registrations_data, list):
                registrations = registrations_data
                reg_count = len(registrations)
            else:
                registrations = []
                reg_count = 0
            
            event_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            event_frame.pack(fill='x', padx=16, pady=(0, 12))
            
            # Event header
            header = tk.Frame(event_frame, bg='#F9FAFB')
            header.pack(fill='x')
            tk.Label(header, text=event.get('title', 'Untitled'), bg='#F9FAFB', fg='#1F2937', 
                    font=('Helvetica', 12, 'bold')).pack(side='left', padx=12, pady=8)
            tk.Label(header, text=f'{reg_count} registrations', bg='#F9FAFB', fg='#1F2937').pack(side='right', padx=12, pady=8)
            
            # Registrations list
            if not registrations:
                tk.Label(event_frame, text='No registrations yet', bg='white', fg='#1F2937').pack(padx=12, pady=12)
            else:
                for reg in registrations:
                    reg_row = tk.Frame(event_frame, bg='white')
                    reg_row.pack(fill='x', padx=12, pady=4)
                    
                    user_info = reg.get('user', {})
                    user_name = user_info.get('username') or user_info.get('email') or f"User {reg.get('user_id', 'N/A')}"
                    reg_date = reg.get('registered_at') or 'N/A'
                    
                    tk.Label(reg_row, text='👤', bg='white', fg='#1F2937').pack(side='left', padx=(0, 8))
                    tk.Label(reg_row, text=user_name, bg='white', fg='#1F2937', 
                            font=('Helvetica', 10, 'bold')).pack(side='left')
                    tk.Label(reg_row, text=f'Registered: {reg_date}', bg='white', fg='#1F2937').pack(side='right')

    def _render_book_resources(self):
        """Navigate to browse resources page with booking functionality"""
        self.controller.navigate('browse_resources')

    def _render_my_bookings(self):
        """Navigate to my bookings page"""
        self.controller.navigate('my_bookings')

    def _render_resource_requests(self):
        self.current_view = 'resource_requests'
        self._clear_content()
        tk.Label(self.content, text='Resource Requests', bg=self.controller.colors.get('background', '#ECF0F1'), 
                fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        if not self.resource_requests:
            no_requests = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            no_requests.pack(fill='both', expand=True, padx=16, pady=(0, 16))
            tk.Label(no_requests, text='No resource requests', bg='white', fg='#1F2937').pack(padx=12, pady=40)
        else:
            table_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            table_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
            
            # Apply custom Treeview style for dark mode compatibility
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('Requests.Treeview',
                          background='white',
                          foreground='#1F2937',
                          fieldbackground='white',
                          borderwidth=0)
            style.configure('Requests.Treeview.Heading',
                          background='#F9FAFB',
                          foreground='#1F2937',
                          borderwidth=1,
                          relief='solid')
            style.map('Requests.Treeview',
                     background=[('selected', '#3B82F6')],
                     foreground=[('selected', 'white')])
            
            cols = ('id', 'resource', 'start_time', 'end_time', 'status')
            tv = ttk.Treeview(table_frame, columns=cols, show='headings', style='Requests.Treeview')
            for c in cols:
                tv.heading(c, text=c.replace('_', ' ').title())
                tv.column(c, width=140)
            for req in self.resource_requests:
                tv.insert('', 'end', values=(req.get('id'), req.get('resource_name'), req.get('start_time'), req.get('end_time'), req.get('status')))
            tv.pack(fill='both', expand=True, padx=4, pady=4)

    def _render_analytics(self):
        self.current_view = 'analytics'
        self._clear_content()
        colors = self.controller.colors
        
        tk.Label(self.content, text='Analytics', bg=self.controller.colors.get('background', '#ECF0F1'), 
                fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        analytics_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        analytics_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        
        # Calculate analytics
        total_events = len(self.my_events)
        
        # Calculate total registrations handling both dict and list formats
        total_registrations = 0
        for regs_data in self.event_registrations.values():
            if isinstance(regs_data, dict):
                total_registrations += regs_data.get('count', 0)
            elif isinstance(regs_data, list):
                total_registrations += len(regs_data)
        
        avg_registrations = total_registrations / total_events if total_events > 0 else 0
        
        stats_container = tk.Frame(analytics_frame, bg='white')
        stats_container.pack(padx=20, pady=20, fill='x')
        
        tk.Label(stats_container, text='Overview Statistics', bg='white', fg='#1F2937', 
                font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 16))
        
        # Stats rows
        def stat_row(label, value):
            row = tk.Frame(stats_container, bg='white')
            row.pack(fill='x', pady=6)
            tk.Label(row, text=label, bg='white', fg='#1F2937', font=('Helvetica', 11)).pack(side='left')
            tk.Label(row, text=str(value), bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(side='right')
        
        stat_row('Total Events Created:', total_events)
        stat_row('Total Registrations:', total_registrations)
        stat_row('Average Registrations per Event:', f'{avg_registrations:.1f}')
        stat_row('Most Popular Event:', self._get_most_popular_event())
        
        # Chart placeholder
        chart_frame = tk.Frame(analytics_frame, bg='#F9FAFB')
        chart_frame.pack(fill='both', expand=True, padx=20, pady=(12, 20))
        tk.Label(chart_frame, text='📊 Chart visualization would go here', bg='#F9FAFB', 
                fg='#1F2937', font=('Helvetica', 12)).pack(pady=40)

    def _render_profile(self):
        self.current_view = 'profile'
        self._clear_content()
        tk.Label(self.content, text='Profile Settings', bg=self.controller.colors.get('background', '#ECF0F1'), 
                fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        profile_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        profile_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        
        user = self.session.get_user() or {}
        
        info_container = tk.Frame(profile_frame, bg='white')
        info_container.pack(padx=20, pady=20)
        
        tk.Label(info_container, text='👔', bg='white', font=('Helvetica', 48)).pack(pady=(0, 16))
        tk.Label(info_container, text=user.get('username', 'N/A'), bg='white', fg='#1F2937', 
                font=('Helvetica', 16, 'bold')).pack()
        tk.Label(info_container, text=user.get('email', 'N/A'), bg='white', fg='#1F2937').pack(pady=(4, 0))
        tk.Label(info_container, text=f"Role: {(self.session.get_role() or 'ORGANIZER').title()}", 
                bg='white', fg='#1F2937').pack(pady=(4, 16))
        
        tk.Label(info_container, text='Profile editing coming soon', bg='white', fg='#1F2937').pack(pady=(8, 0))

    def _render_events_table(self, events, show_actions=False):
        """Render events table using simple Treeview"""
        
        # Simple container
        frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        
        # NO EVENTS
        if not events:
            tk.Label(frame, text='No events', bg='white', fg='#6B7280').pack(padx=12, pady=12)
            return
        
        # Configure Treeview style for light mode (override dark mode)
        style = ttk.Style()
        style.theme_use('clam')  # Use 'clam' theme for better customization
        
        # Configure colors to ensure light mode visibility
        style.configure('Events.Treeview',
                       background='white',
                       foreground='#1F2937',  # Dark gray text
                       fieldbackground='white',
                       rowheight=28)
        
        style.configure('Events.Treeview.Heading',
                       background='#F3F4F6',  # Light gray header
                       foreground='#1F2937',  # Dark gray text
                       font=('Helvetica', 10, 'bold'))
        
        # Hover effect
        style.map('Events.Treeview',
                 background=[('selected', '#3B82F6')],  # Blue when selected
                 foreground=[('selected', 'white')])
        
        # SIMPLE TREEVIEW
        cols = ('id', 'title', 'start', 'end', 'venue', 'status')
        tree = ttk.Treeview(frame, columns=cols, show='headings', height=15, style='Events.Treeview')
        
        tree.heading('id', text='ID')
        tree.heading('title', text='Title')
        tree.heading('start', text='Start')
        tree.heading('end', text='End')
        tree.heading('venue', text='Venue')
        tree.heading('status', text='Status')
        
        tree.column('id', width=50)
        tree.column('title', width=250)
        tree.column('start', width=150)
        tree.column('end', width=150)
        tree.column('venue', width=120)
        tree.column('status', width=100)
        
        # Insert data
        for e in events:
            tree.insert('', 'end', values=(
                e.get('id', ''),
                e.get('title', 'Untitled'),
                e.get('startTime', e.get('start_time', '')),
                e.get('endTime', e.get('end_time', '')),
                e.get('venue', ''),
                e.get('status', 'pending')
            ))
        
        # Scrollbar
        scroll = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=4, pady=4)
        scroll.pack(side='right', fill='y', pady=4)
        
        # Actions
        if show_actions:
            btn_frame = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
            btn_frame.pack(fill='x', padx=16, pady=8)
            
            def get_selected():
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning('No Selection', 'Select an event first')
                    return None
                vals = tree.item(sel[0], 'values')
                return int(vals[0]) if vals else None
            
            create_primary_button(btn_frame, '📋 View', lambda: self._show_event_details(get_selected()) if get_selected() else None, 100, 36).pack(side='left', padx=5)
            create_secondary_button(btn_frame, '✏️ Edit', lambda: self._edit_event(get_selected()) if get_selected() else None, 90, 36).pack(side='left', padx=5)
            create_danger_button(btn_frame, '🗑️ Delete', lambda: self._delete_event(get_selected()) if get_selected() else None, 100, 36).pack(side='left', padx=5)
    
    def _show_event_details(self, event_id):
        """Show detailed view of a specific event"""
        event = next((e for e in self.my_events if e.get('id') == event_id), None)
        if not event:
            messagebox.showerror('Error', 'Event not found')
            return
        
        # CRITICAL FIX: Always fetch FRESH registration data from API
        # Don't rely on cached data which may be stale
        try:
            registrations_response = self.api.get(f'events/{event_id}/registrations')
            # Backend returns: {'count': X, 'registrations': [...]}
            if isinstance(registrations_response, dict):
                reg_count = registrations_response.get('count', 0)
                reg_list = registrations_response.get('registrations', [])
            elif isinstance(registrations_response, list):
                reg_list = registrations_response
                reg_count = len(reg_list)
            else:
                reg_count = 0
                reg_list = []
            
            # Update cache with fresh data
            self.event_registrations[event_id] = registrations_response
        except Exception as e:
            # Fallback to cached data if API fails
            registrations = self.event_registrations.get(event_id, [])
            if isinstance(registrations, dict):
                reg_count = registrations.get('count', 0)
                reg_list = registrations.get('registrations', [])
            elif isinstance(registrations, list):
                reg_list = registrations
                reg_count = len(reg_list)
            else:
                reg_count = 0
                reg_list = []
        
        # Format datetime fields (backend sends camelCase: startTime, endTime)
        start_time = event.get('startTime', 'N/A')
        end_time = event.get('endTime', 'N/A')
        
        # Format dates if present
        if start_time != 'N/A':
            try:
                # Backend sends ISO format: 2025-11-20T09:00:00
                start_time = start_time.replace('T', ' ') if 'T' in start_time else start_time
            except:
                pass
        
        if end_time != 'N/A':
            try:
                end_time = end_time.replace('T', ' ') if 'T' in end_time else end_time
            except:
                pass
        
        details = f"Event: {event.get('title', 'Untitled')}\n"
        details += f"Description: {event.get('description', 'N/A')}\n"
        details += f"Start: {start_time}\n"
        details += f"End: {end_time}\n"
        details += f"Venue: {event.get('venue', 'N/A')}\n"
        details += f"Status: {event.get('status', 'N/A')}\n"
        details += f"Registrations: {reg_count}"
        
        messagebox.showinfo('Event Details', details)

    def _edit_event(self, event_id):
        """Edit an existing event"""
        event = next((e for e in self.my_events if e.get('id') == event_id), None)
        if not event:
            messagebox.showerror('Error', 'Event not found')
            return
        
        # Create edit modal
        edit_window = tk.Toplevel(self)
        edit_window.title(f"Edit Event: {event.get('title', 'Untitled')}")
        edit_window.geometry('600x700')
        edit_window.transient(self)
        edit_window.grab_set()
        
        # Main container
        main_frame = tk.Frame(edit_window, bg='white', padx=30, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        tk.Label(main_frame, text=f"Edit Event", 
                bg='white', fg='#1F2937', font=('Helvetica', 18, 'bold')).pack(anchor='w', pady=(0, 5))
        
        tk.Label(main_frame, text="After editing, event will be sent for admin re-approval", 
                bg='white', fg='#F59E0B', font=('Helvetica', 10)).pack(anchor='w', pady=(0, 20))
        
        # Title
        tk.Label(main_frame, text='Event Title *', bg='white', fg='#374151', 
                font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        title_entry = tk.Entry(main_frame, font=('Helvetica', 12), width=50)
        title_entry.insert(0, event.get('title', ''))
        title_entry.pack(fill='x', pady=(0, 15))
        
        # Description
        tk.Label(main_frame, text='Description *', bg='white', fg='#374151',
                font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        desc_text = tk.Text(main_frame, font=('Helvetica', 11), height=6, wrap='word')
        desc_text.insert('1.0', event.get('description', ''))
        desc_text.pack(fill='x', pady=(0, 15))
        
        # Venue
        tk.Label(main_frame, text='Venue *', bg='white', fg='#374151',
                font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        venue_entry = tk.Entry(main_frame, font=('Helvetica', 12), width=50)
        venue_entry.insert(0, event.get('venue', ''))
        venue_entry.pack(fill='x', pady=(0, 15))
        
        # Extract and parse existing dates
        start_time_str = event.get('startTime', '')
        end_time_str = event.get('endTime', '')
        
        # Parse existing datetime (format: 2025-11-20T09:00:00)
        from datetime import datetime
        try:
            if start_time_str and 'T' in start_time_str:
                start_dt = datetime.fromisoformat(start_time_str)
                start_date_val = start_dt.strftime('%Y-%m-%d')
                start_time_val = start_dt.strftime('%H:%M')
            else:
                start_date_val = ''
                start_time_val = '09:00'
        except:
            start_date_val = ''
            start_time_val = '09:00'
        
        try:
            if end_time_str and 'T' in end_time_str:
                end_dt = datetime.fromisoformat(end_time_str)
                end_date_val = end_dt.strftime('%Y-%m-%d')
                end_time_val = end_dt.strftime('%H:%M')
            else:
                end_date_val = ''
                end_time_val = '17:00'
        except:
            end_date_val = ''
            end_time_val = '17:00'
        
        # Start Date
        tk.Label(main_frame, text='Start Date *', bg='white', fg='#374151',
                font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        start_date_entry = tk.Entry(main_frame, font=('Helvetica', 12), width=50)
        start_date_entry.insert(0, start_date_val)
        start_date_entry.pack(fill='x', pady=(0, 5))
        tk.Label(main_frame, text='Format: YYYY-MM-DD', bg='white', fg='#6B7280',
                font=('Helvetica', 9)).pack(anchor='w', pady=(0, 15))
        
        # Start Time
        tk.Label(main_frame, text='Start Time *', bg='white', fg='#374151',
                font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        start_time_entry = tk.Entry(main_frame, font=('Helvetica', 12), width=50)
        start_time_entry.insert(0, start_time_val)
        start_time_entry.pack(fill='x', pady=(0, 5))
        tk.Label(main_frame, text='Format: HH:MM (24-hour)', bg='white', fg='#6B7280',
                font=('Helvetica', 9)).pack(anchor='w', pady=(0, 15))
        
        # End Date
        tk.Label(main_frame, text='End Date *', bg='white', fg='#374151',
                font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        end_date_entry = tk.Entry(main_frame, font=('Helvetica', 12), width=50)
        end_date_entry.insert(0, end_date_val)
        end_date_entry.pack(fill='x', pady=(0, 5))
        tk.Label(main_frame, text='Format: YYYY-MM-DD', bg='white', fg='#6B7280',
                font=('Helvetica', 9)).pack(anchor='w', pady=(0, 15))
        
        # End Time
        tk.Label(main_frame, text='End Time *', bg='white', fg='#374151',
                font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        end_time_entry = tk.Entry(main_frame, font=('Helvetica', 12), width=50)
        end_time_entry.insert(0, end_time_val)
        end_time_entry.pack(fill='x', pady=(0, 5))
        tk.Label(main_frame, text='Format: HH:MM (24-hour)', bg='white', fg='#6B7280',
                font=('Helvetica', 9)).pack(anchor='w', pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        def submit_edit():
            # Get values
            title = title_entry.get().strip()
            description = desc_text.get('1.0', 'end-1c').strip()
            venue = venue_entry.get().strip()
            start_date = start_date_entry.get().strip()
            start_time = start_time_entry.get().strip()
            end_date = end_date_entry.get().strip()
            end_time = end_time_entry.get().strip()
            
            # Validation
            if not title or len(title) < 3:
                messagebox.showerror('Validation Error', 'Title must be at least 3 characters')
                return
            
            if not description or len(description) < 10:
                messagebox.showerror('Validation Error', 'Description must be at least 10 characters')
                return
            
            if not venue:
                messagebox.showerror('Validation Error', 'Venue is required')
                return
            
            # Combine date and time
            try:
                start_datetime = f"{start_date}T{start_time}:00"
                end_datetime = f"{end_date}T{end_time}:00"
                
                # Validate datetime format
                datetime.fromisoformat(start_datetime)
                datetime.fromisoformat(end_datetime)
            except ValueError:
                messagebox.showerror('Validation Error', 'Invalid date/time format')
                return
            
            # Prepare payload
            user_data = self.session.get_user()
            organizer_id = user_data.get('id') or user_data.get('user_id') if user_data else None
            
            payload = {
                'title': title,
                'description': description,
                'organizerId': organizer_id,
                'startTime': start_datetime,
                'endTime': end_datetime,
                'venue': venue
            }
            
            try:
                # Call PUT endpoint to update event
                response = self.api.put(f'events/{event_id}', payload)
                messagebox.showinfo('Success', 
                    f"Event '{title}' updated successfully!\n\n"
                    f"Status: Pending (requires admin re-approval)")
                edit_window.destroy()
                # Reload data
                self._load_all_data_then(self._render_my_events)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to update event:\n\n{str(e)}')
        
        # Create canvas buttons for macOS compatibility
        cancel_btn = create_secondary_button(button_frame, 'Cancel', edit_window.destroy, width=100, height=40)
        cancel_btn.pack(side='left', padx=(0, 10))
        
        save_btn = create_primary_button(button_frame, 'Save Changes', submit_edit, width=140, height=40)
        save_btn.pack(side='left')

    def _delete_event(self, event_id):
        """Delete an event with confirmation"""
        event = next((e for e in self.my_events if e.get('id') == event_id), None)
        if not event:
            messagebox.showerror('Error', 'Event not found')
            return
        
        # Confirmation dialog
        confirm = messagebox.askyesno(
            'Confirm Delete',
            f"Are you sure you want to delete this event?\n\n"
            f"Event: {event.get('title', 'Untitled')}\n"
            f"Venue: {event.get('venue', 'N/A')}\n"
            f"Start: {event.get('startTime') or event.get('start_time', 'N/A')}\n\n"
            f"⚠️ This action cannot be undone!"
        )
        
        if not confirm:
            return
        
        try:
            # Call DELETE endpoint
            self.api.delete(f'events/{event_id}')
            messagebox.showinfo('Success', f"Event '{event.get('title')}' has been deleted successfully!")
            
            # Reload events
            self._load_all_data_then(self._render_my_events)
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check error type
            if '405' in error_msg or 'method not allowed' in error_msg or '404' in error_msg:
                # Backend doesn't have DELETE endpoint
                messagebox.showwarning(
                    'Feature Not Available',
                    '❌ Delete endpoint not implemented in backend yet!\n\n'
                    '📋 To enable delete functionality:\n\n'
                    '1. Add to EventController.java:\n'
                    '   @DeleteMapping("/{id}")\n'
                    '   public ResponseEntity<?> deleteEvent(@PathVariable int id) {\n'
                    '       eventDao.delete(id);\n'
                    '       return ResponseEntity.ok(\n'
                    '           Map.of("message", "Event deleted"));\n'
                    '   }\n\n'
                    '2. Add to EventDao.java:\n'
                    '   public void delete(int id) {\n'
                    '       jdbc.update("DELETE FROM events WHERE id = ?", id);\n'
                    '   }\n\n'
                    '3. Restart backend\n\n'
                    'See BACKEND_DELETE_IMPLEMENTATION.md for full code.'
                )
            elif '403' in error_msg or 'forbidden' in error_msg:
                messagebox.showerror(
                    'Permission Denied',
                    'You do not have permission to delete this event.\n\n'
                    'Only the event organizer or admin can delete events.'
                )
            else:
                messagebox.showerror('Error', f'Failed to delete event:\n\n{str(e)}')

    # Actions
    def _logout(self):
        try:
            self.session.clear_session()
        finally:
            self.controller.navigate('login', add_to_history=False)

    def _on_search(self):
        q = (self.search_var.get() or '').lower().strip()
        if not q:
            self._render_my_events()
            return
        filtered = [e for e in self.my_events if q in (e.get('title') or '').lower()]
        self._clear_content()
        tk.Label(self.content, text=f"Search results for '{q}'", bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        self._render_events_table(filtered, show_actions=True)

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

    def _get_most_popular_event(self):
        """Find the event with most registrations"""
        if not self.my_events:
            return 'N/A'
        
        max_regs = 0
        popular_event = 'N/A'
        
        for event in self.my_events:
            event_id = event.get('id')
            
            # Handle both dict and list response formats for registration count
            registrations_data = self.event_registrations.get(event_id, [])
            if isinstance(registrations_data, dict):
                reg_count = registrations_data.get('count', 0)
            elif isinstance(registrations_data, list):
                reg_count = len(registrations_data)
            else:
                reg_count = 0
            
            if reg_count > max_regs:
                max_regs = reg_count
                popular_event = event.get('title', 'Untitled')
        
        return f'{popular_event} ({max_regs} regs)' if max_regs > 0 else 'N/A'

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
