import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.button_styles import ButtonStyles


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

        # Layout: 1 row, 2 columns (sidebar, main)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_main()

        # Initial content
        self._load_all_data_then(self._render_dashboard)

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
            btn = tk.Button(
                menu,
                text=f"{icon}  {text}",
                font=('Helvetica', 11),
                bg=colors.get('primary', '#2C3E50'),
                fg='white',
                activebackground=colors.get('secondary', '#3498DB'),
                activeforeground='white',
                relief='flat',
                anchor='w',
                command=cmd,
                padx=16,
                pady=8,
            )
            btn.pack(fill='x')

        add_btn('Dashboard', self._render_dashboard, icon='🏠')
        add_btn('Create Event', self._render_create_event, icon='➕')
        add_btn('My Events', self._render_my_events, icon='📋')
        add_btn('Event Registrations', self._render_event_registrations, icon='👥')
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

        # Search bar
        search_frame = tk.Frame(top, bg='white')
        search_frame.pack(side='right', padx=16)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left')
        tk.Button(search_frame, text='Search', command=self._on_search, bg=colors.get('secondary', '#3498DB'), fg='white', relief='flat').pack(side='left', padx=(6, 0))

        # Notifications icon
        tk.Button(top, text='🔔', relief='flat', bg='white', command=lambda: messagebox.showinfo('Notifications', 'No new notifications')).pack(side='right', padx=(0, 8))

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
                self.my_events = self.api.get('events/my') or []
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
        self._clear_content()
        colors = self.controller.colors

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
        
        tk.Button(btn_frame, text='➕ Create New Event', command=self._render_create_event, bg=colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=16, pady=8).pack(side='left', padx=(0, 8))
        tk.Button(btn_frame, text='👥 Check Registrations', command=self._render_event_registrations, bg=colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=16, pady=8).pack(side='left', padx=8)
        tk.Button(btn_frame, text='📊 View Analytics', command=self._render_analytics, bg=colors.get('warning', '#F39C12'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=16, pady=8).pack(side='left', padx=(8, 0))

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
                reg_count = len(self.event_registrations.get(event_id, []))
                
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
        self._clear_content()
        colors = self.controller.colors
        
        tk.Label(self.content, text='Create New Event', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        form_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        form_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        
        # Form container
        form = tk.Frame(form_frame, bg='white')
        form.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Event Title
        tk.Label(form, text='Event Title *', bg='white', fg='#374151', font=('Helvetica', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=(0, 4))
        title_entry = tk.Entry(form, width=50)
        title_entry.grid(row=1, column=0, sticky='ew', pady=(0, 12))
        
        # Description
        tk.Label(form, text='Description *', bg='white', fg='#374151', font=('Helvetica', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=(0, 4))
        desc_text = tk.Text(form, width=50, height=5)
        desc_text.grid(row=3, column=0, sticky='ew', pady=(0, 12))
        
        # Start Time
        tk.Label(form, text='Start Time (YYYY-MM-DD HH:MM:SS) *', bg='white', fg='#374151', font=('Helvetica', 11, 'bold')).grid(row=4, column=0, sticky='w', pady=(0, 4))
        start_entry = tk.Entry(form, width=50)
        start_entry.grid(row=5, column=0, sticky='ew', pady=(0, 12))
        
        # End Time
        tk.Label(form, text='End Time (YYYY-MM-DD HH:MM:SS) *', bg='white', fg='#374151', font=('Helvetica', 11, 'bold')).grid(row=6, column=0, sticky='w', pady=(0, 4))
        end_entry = tk.Entry(form, width=50)
        end_entry.grid(row=7, column=0, sticky='ew', pady=(0, 12))
        
        # Venue
        tk.Label(form, text='Venue *', bg='white', fg='#374151', font=('Helvetica', 11, 'bold')).grid(row=8, column=0, sticky='w', pady=(0, 4))
        venue_entry = tk.Entry(form, width=50)
        venue_entry.grid(row=9, column=0, sticky='ew', pady=(0, 12))
        
        # Capacity
        tk.Label(form, text='Capacity', bg='white', fg='#374151', font=('Helvetica', 11, 'bold')).grid(row=10, column=0, sticky='w', pady=(0, 4))
        capacity_entry = tk.Entry(form, width=50)
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
            
            payload = {
                'title': title,
                'description': description,
                'start_time': start_time,
                'end_time': end_time,
                'venue': venue
            }
            
            if capacity:
                try:
                    payload['capacity'] = int(capacity)
                except ValueError:
                    messagebox.showerror('Error', 'Capacity must be a number')
                    return
            
            try:
                response = self.api.post('events', payload)
                messagebox.showinfo('Success', f"Event '{title}' created successfully!")
                self._load_all_data_then(self._render_my_events)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to create event: {str(e)}')
        
        btn_frame = tk.Frame(form, bg='white')
        btn_frame.grid(row=12, column=0, sticky='ew', pady=(12, 0))
        
        tk.Button(btn_frame, text='Create Event', command=submit_event, bg=colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=20, pady=10).pack(side='left')
        tk.Button(btn_frame, text='Cancel', command=self._render_dashboard, bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 11), padx=20, pady=10).pack(side='left', padx=(8, 0))

    def _render_my_events(self):
        self._clear_content()
        tk.Label(self.content, text='My Events', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        if not self.my_events:
            no_events = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            no_events.pack(fill='both', expand=True, padx=16, pady=(0, 16))
            tk.Label(no_events, text='No events created yet', bg='white', fg='#6B7280').pack(padx=12, pady=40)
            tk.Button(no_events, text='Create Your First Event', command=self._render_create_event, bg=self.controller.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=16, pady=8).pack(pady=(0, 40))
        else:
            self._render_events_table(self.my_events, show_actions=True)

    def _render_event_registrations(self):
        self._clear_content()
        tk.Label(self.content, text='Event Registrations', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        # Show registrations grouped by event
        for event in self.my_events:
            event_id = event.get('id')
            registrations = self.event_registrations.get(event_id, [])
            
            event_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            event_frame.pack(fill='x', padx=16, pady=(0, 12))
            
            # Event header
            header = tk.Frame(event_frame, bg='#F9FAFB')
            header.pack(fill='x')
            tk.Label(header, text=event.get('title', 'Untitled'), bg='#F9FAFB', fg='#374151', font=('Helvetica', 12, 'bold')).pack(side='left', padx=12, pady=8)
            tk.Label(header, text=f'{len(registrations)} registrations', bg='#F9FAFB', fg='#6B7280').pack(side='right', padx=12, pady=8)
            
            # Registrations list
            if not registrations:
                tk.Label(event_frame, text='No registrations yet', bg='white', fg='#6B7280').pack(padx=12, pady=12)
            else:
                for reg in registrations:
                    reg_row = tk.Frame(event_frame, bg='white')
                    reg_row.pack(fill='x', padx=12, pady=4)
                    
                    user_info = reg.get('user', {})
                    user_name = user_info.get('username') or user_info.get('email') or f"User {reg.get('user_id', 'N/A')}"
                    reg_date = reg.get('registered_at') or 'N/A'
                    
                    tk.Label(reg_row, text='👤', bg='white').pack(side='left', padx=(0, 8))
                    tk.Label(reg_row, text=user_name, bg='white', font=('Helvetica', 10, 'bold')).pack(side='left')
                    tk.Label(reg_row, text=f'Registered: {reg_date}', bg='white', fg='#6B7280').pack(side='right')

    def _render_resource_requests(self):
        self._clear_content()
        tk.Label(self.content, text='Resource Requests', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        if not self.resource_requests:
            no_requests = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            no_requests.pack(fill='both', expand=True, padx=16, pady=(0, 16))
            tk.Label(no_requests, text='No resource requests', bg='white', fg='#6B7280').pack(padx=12, pady=40)
        else:
            table_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            table_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
            
            cols = ('id', 'resource', 'start_time', 'end_time', 'status')
            tv = ttk.Treeview(table_frame, columns=cols, show='headings')
            for c in cols:
                tv.heading(c, text=c.replace('_', ' ').title())
                tv.column(c, width=140)
            for req in self.resource_requests:
                tv.insert('', 'end', values=(req.get('id'), req.get('resource_name'), req.get('start_time'), req.get('end_time'), req.get('status')))
            tv.pack(fill='both', expand=True, padx=4, pady=4)

    def _render_analytics(self):
        self._clear_content()
        colors = self.controller.colors
        
        tk.Label(self.content, text='Analytics', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        analytics_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        analytics_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        
        # Calculate analytics
        total_events = len(self.my_events)
        total_registrations = sum(len(regs) for regs in self.event_registrations.values())
        avg_registrations = total_registrations / total_events if total_events > 0 else 0
        
        stats_container = tk.Frame(analytics_frame, bg='white')
        stats_container.pack(padx=20, pady=20, fill='x')
        
        tk.Label(stats_container, text='Overview Statistics', bg='white', fg='#374151', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 16))
        
        # Stats rows
        def stat_row(label, value):
            row = tk.Frame(stats_container, bg='white')
            row.pack(fill='x', pady=6)
            tk.Label(row, text=label, bg='white', fg='#6B7280', font=('Helvetica', 11)).pack(side='left')
            tk.Label(row, text=str(value), bg='white', fg=colors.get('primary', '#2C3E50'), font=('Helvetica', 11, 'bold')).pack(side='right')
        
        stat_row('Total Events Created:', total_events)
        stat_row('Total Registrations:', total_registrations)
        stat_row('Average Registrations per Event:', f'{avg_registrations:.1f}')
        stat_row('Most Popular Event:', self._get_most_popular_event())
        
        # Chart placeholder
        chart_frame = tk.Frame(analytics_frame, bg='#F9FAFB')
        chart_frame.pack(fill='both', expand=True, padx=20, pady=(12, 20))
        tk.Label(chart_frame, text='📊 Chart visualization would go here', bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 12)).pack(pady=40)

    def _render_profile(self):
        self._clear_content()
        tk.Label(self.content, text='Profile Settings', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        profile_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        profile_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        
        user = self.session.get_user() or {}
        
        info_container = tk.Frame(profile_frame, bg='white')
        info_container.pack(padx=20, pady=20)
        
        tk.Label(info_container, text='👔', bg='white', font=('Helvetica', 48)).pack(pady=(0, 16))
        tk.Label(info_container, text=user.get('username', 'N/A'), bg='white', font=('Helvetica', 16, 'bold')).pack()
        tk.Label(info_container, text=user.get('email', 'N/A'), bg='white', fg='#6B7280').pack(pady=(4, 0))
        tk.Label(info_container, text=f"Role: {(self.session.get_role() or 'ORGANIZER').title()}", bg='white', fg='#6B7280').pack(pady=(4, 16))
        
        tk.Label(info_container, text='Profile editing coming soon', bg='white', fg='#9CA3AF').pack(pady=(8, 0))

    def _render_events_table(self, events, show_actions=False):
        cols = ['title', 'start_time', 'venue', 'status']
        if show_actions:
            cols.append('actions')
            
        frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        # Header row
        header = tk.Frame(frame, bg='#F9FAFB')
        header.pack(fill='x')
        headers = ['Title', 'Start Time', 'Venue', 'Status']
        if show_actions:
            headers.append('Actions')
        for i, h in enumerate(headers):
            tk.Label(header, text=h, bg='#F9FAFB', fg='#374151', font=('Helvetica', 10, 'bold')).grid(row=0, column=i, sticky='w', padx=8, pady=8)
            header.grid_columnconfigure(i, weight=1 if i == 0 else 0)

        # Rows
        if not events:
            tk.Label(frame, text='No events', bg='white', fg='#6B7280').pack(padx=12, pady=12)
        else:
            for e in events:
                row = tk.Frame(frame, bg='white')
                row.pack(fill='x', padx=4, pady=2)
                
                status = (e.get('status') or 'pending').title()
                status_colors = {
                    'Approved': '#27AE60',
                    'Pending': '#F39C12',
                    'Rejected': '#E74C3C'
                }
                status_color = status_colors.get(status, '#6B7280')
                
                tk.Label(row, text=e.get('title') or 'Untitled', bg='white').grid(row=0, column=0, sticky='w', padx=8, pady=8)
                tk.Label(row, text=e.get('start_time') or '', bg='white', fg='#6B7280').grid(row=0, column=1, sticky='w', padx=8)
                tk.Label(row, text=e.get('venue') or '', bg='white', fg='#6B7280').grid(row=0, column=2, sticky='w', padx=8)
                tk.Label(row, text=status, bg='white', fg=status_color, font=('Helvetica', 10, 'bold')).grid(row=0, column=3, sticky='w', padx=8)
                
                if show_actions:
                    event_id = e.get('id')
                    reg_count = len(self.event_registrations.get(event_id, []))
                    tk.Button(row, text=f'View ({reg_count})', command=lambda eid=event_id: self._show_event_details(eid), bg=self.controller.colors.get('secondary', '#3498DB'), fg='white', relief='flat').grid(row=0, column=4, padx=8)

    def _show_event_details(self, event_id):
        """Show detailed view of a specific event"""
        event = next((e for e in self.my_events if e.get('id') == event_id), None)
        if not event:
            messagebox.showerror('Error', 'Event not found')
            return
        
        registrations = self.event_registrations.get(event_id, [])
        
        details = f"Event: {event.get('title', 'Untitled')}\n"
        details += f"Description: {event.get('description', 'N/A')}\n"
        details += f"Start: {event.get('start_time', 'N/A')}\n"
        details += f"End: {event.get('end_time', 'N/A')}\n"
        details += f"Venue: {event.get('venue', 'N/A')}\n"
        details += f"Status: {event.get('status', 'N/A')}\n"
        details += f"Registrations: {len(registrations)}"
        
        messagebox.showinfo('Event Details', details)

    # Actions
    def _logout(self):
        try:
            self.session.clear_session()
        finally:
            self.controller.show_page('LoginPage')

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
            reg_count = len(self.event_registrations.get(event_id, []))
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
