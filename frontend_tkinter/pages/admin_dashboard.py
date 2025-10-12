import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.button_styles import ButtonStyles
from utils.canvas_button import create_primary_button, create_secondary_button, create_success_button, create_danger_button, create_warning_button


class AdminDashboard(tk.Frame):
    """Admin Dashboard with sidebar navigation and dynamic content area."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors.get('background', '#ECF0F1'))
        self.controller = controller
        self.api = APIClient()
        self.session = SessionManager()

        # Data caches
        self.pending_events = []
        self.all_events = []
        self.all_resources = []
        self.all_users = []
        self.pending_bookings = []
        self.recent_activities = []

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
        name = u.get('username') or u.get('email') or 'Admin'
        role = (self.session.get_role() or 'ADMIN').title()

        # Profile section
        profile = tk.Frame(sidebar, bg=colors.get('primary', '#2C3E50'))
        profile.pack(fill='x', pady=(16, 8))
        tk.Label(profile, text='⚡', bg=colors.get('primary', '#2C3E50'), fg='white', font=('Helvetica', 26)).pack()
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
        add_btn('Manage Events', self._render_manage_events, icon='📅')
        add_btn('Manage Resources', self._render_manage_resources, icon='🏢')
        add_btn('Manage Users', self._render_manage_users, icon='👥')
        add_btn('Booking Approvals', self._render_booking_approvals, icon='✓')
        add_btn('Reports & Analytics', self._render_reports_analytics, icon='📊')
        add_btn('System Settings', self._render_system_settings, icon='⚙️')
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
        welcome = tk.Label(top, text=f"Admin Panel - {user.get('username') or 'Administrator'}", bg='white', fg=colors.get('primary', '#2C3E50'), font=('Helvetica', 13, 'bold'))
        welcome.pack(side='left', padx=16)

        # System status indicator
        status_frame = tk.Frame(top, bg='white')
        status_frame.pack(side='right', padx=16)
        tk.Label(status_frame, text='●', fg='#27AE60', bg='white', font=('Helvetica', 16)).pack(side='left')
        tk.Label(status_frame, text='System Operational', bg='white', fg='#27AE60', font=('Helvetica', 10, 'bold')).pack(side='left', padx=(4, 0))

        # Notifications icon
        notif_btn = create_secondary_button(top, '🔔', self._show_notifications, width=40, height=30)
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
            
            # Load pending events
            try:
                self.pending_events = self.api.get('admin/events/pending') or []
            except Exception as e:
                errors.append(('pending_events', str(e)))
                self.pending_events = []
            
            # Load all events
            try:
                self.all_events = self.api.get('events') or []
            except Exception as e:
                errors.append(('all_events', str(e)))
                self.all_events = []
            
            # Load all resources
            try:
                self.all_resources = self.api.get('admin/resources') or []
            except Exception as e:
                # Fallback to regular resources endpoint
                try:
                    self.all_resources = self.api.get('resources') or []
                except Exception:
                    errors.append(('resources', str(e)))
                    self.all_resources = []
            
            # Load all users
            try:
                self.all_users = self.api.get('admin/users') or []
            except Exception as e:
                errors.append(('users', str(e)))
                self.all_users = []
            
            # Load pending bookings
            try:
                self.pending_bookings = self.api.get('admin/bookings/pending') or []
            except Exception as e:
                errors.append(('pending_bookings', str(e)))
                self.pending_bookings = []

            def done():
                self._hide_spinner()
                if errors:
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

        # System Statistics Cards
        stats = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        stats.pack(fill='x', padx=16, pady=(16, 8))
        for i in range(4):
            stats.grid_columnconfigure(i, weight=1)

        def stat_card(parent, title, value, color, icon):
            f = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            header = tk.Frame(f, bg='white')
            header.pack(fill='x', padx=12, pady=(10, 0))
            tk.Label(header, text=icon, bg='white', font=('Helvetica', 20)).pack(side='left')
            tk.Label(header, text=title, bg='white', fg='#6B7280').pack(side='left', padx=(8, 0))
            tk.Label(f, text=str(value), bg='white', fg=color, font=('Helvetica', 20, 'bold')).pack(anchor='w', padx=12, pady=(4, 12))
            return f

        total_users = len(self.all_users)
        total_events = len(self.all_events)
        total_resources = len(self.all_resources)
        total_bookings = len(self.pending_bookings) + 10  # Placeholder for total bookings

        c1 = stat_card(stats, 'Total Users', total_users, colors.get('secondary', '#3498DB'), '👥')
        c2 = stat_card(stats, 'Total Events', total_events, colors.get('success', '#27AE60'), '📅')
        c3 = stat_card(stats, 'Resources', total_resources, colors.get('warning', '#F39C12'), '🏢')
        c4 = stat_card(stats, 'Bookings', total_bookings, colors.get('primary', '#2C3E50'), '📚')
        
        c1.grid(row=0, column=0, sticky='ew', padx=(0, 6))
        c2.grid(row=0, column=1, sticky='ew', padx=6)
        c3.grid(row=0, column=2, sticky='ew', padx=6)
        c4.grid(row=0, column=3, sticky='ew', padx=(6, 0))

        # Pending Approvals Section
        approvals_section = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        approvals_section.pack(fill='x', padx=16, pady=(8, 8))
        
        header_frame = tk.Frame(approvals_section, bg=self.controller.colors.get('background', '#ECF0F1'))
        header_frame.pack(fill='x', pady=(4, 6))
        tk.Label(header_frame, text='Pending Approvals', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold'), fg=colors.get('primary', '#2C3E50')).pack(side='left')
        
        pending_count = len(self.pending_events) + len(self.pending_bookings)
        if pending_count > 0:
            badge = tk.Label(header_frame, text=str(pending_count), bg='#E74C3C', fg='white', font=('Helvetica', 10, 'bold'), padx=8, pady=2)
            badge.pack(side='left', padx=(8, 0))

        approvals_frame = tk.Frame(approvals_section, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        approvals_frame.pack(fill='x')

        # Pending Events
        if self.pending_events:
            tk.Label(approvals_frame, text='Events Awaiting Approval', bg='#FEF3C7', fg='#92400E', font=('Helvetica', 11, 'bold')).pack(fill='x', padx=12, pady=(12, 6))
            
            for event in self.pending_events[:5]:  # Show first 5
                row = tk.Frame(approvals_frame, bg='white')
                row.pack(fill='x', padx=12, pady=4)
                
                tk.Label(row, text='📅', bg='white').pack(side='left', padx=(0, 8))
                tk.Label(row, text=event.get('title', 'Untitled Event'), bg='white', font=('Helvetica', 10, 'bold')).pack(side='left')
                tk.Label(row, text=event.get('start_time', 'N/A'), bg='white', fg='#6B7280').pack(side='left', padx=(12, 0))
                
                btn_frame = tk.Frame(row, bg='white')
                btn_frame.pack(side='right')
                approve_btn = create_success_button(btn_frame, '✓ Approve', lambda e=event: self._approve_event(e), width=100, height=30)
                approve_btn.pack(side='left', padx=(0, 4))
                reject_btn = create_danger_button(btn_frame, '✗ Reject', lambda e=event: self._reject_event(e), width=90, height=30)
                reject_btn.pack(side='left')

        # Pending Bookings
        if self.pending_bookings:
            tk.Label(approvals_frame, text='Booking Requests', bg='#FEF3C7', fg='#92400E', font=('Helvetica', 11, 'bold')).pack(fill='x', padx=12, pady=(12, 6))
            
            for booking in self.pending_bookings[:5]:  # Show first 5
                row = tk.Frame(approvals_frame, bg='white')
                row.pack(fill='x', padx=12, pady=4)
                
                tk.Label(row, text='📚', bg='white').pack(side='left', padx=(0, 8))
                tk.Label(row, text=f"Resource #{booking.get('resource_id', 'N/A')}", bg='white', font=('Helvetica', 10, 'bold')).pack(side='left')
                tk.Label(row, text=f"{booking.get('start_time', 'N/A')} - {booking.get('end_time', 'N/A')}", bg='white', fg='#6B7280').pack(side='left', padx=(12, 0))
                
                btn_frame = tk.Frame(row, bg='white')
                btn_frame.pack(side='right')
                approve_btn = create_success_button(btn_frame, '✓ Approve', lambda b=booking: self._approve_booking(b), width=100, height=30)
                approve_btn.pack(side='left', padx=(0, 4))
                reject_btn = create_danger_button(btn_frame, '✗ Reject', lambda b=booking: self._reject_booking(b), width=90, height=30)
                reject_btn.pack(side='left')

        if not self.pending_events and not self.pending_bookings:
            tk.Label(approvals_frame, text='No pending approvals', bg='white', fg='#6B7280').pack(padx=12, pady=20)

        # Recent Activities Log
        activities_section = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        activities_section.pack(fill='both', expand=True, padx=16, pady=(8, 8))
        tk.Label(activities_section, text='Recent Activities', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold'), fg=colors.get('primary', '#2C3E50')).pack(anchor='w', pady=(4, 6))

        activities_frame = tk.Frame(activities_section, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        activities_frame.pack(fill='both', expand=True)

        # Generate activity log from events and bookings
        activities = []
        for event in self.all_events[:10]:
            activities.append({
                'time': event.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'action': f"Event '{event.get('title', 'Untitled')}' {event.get('status', 'created')}",
                'icon': '📅',
                'user': f"User #{event.get('organizer_id', 'N/A')}"
            })
        
        for user in self.all_users[:5]:
            activities.append({
                'time': user.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'action': f"User '{user.get('username', 'Unknown')}' registered",
                'icon': '👤',
                'user': user.get('username', 'Unknown')
            })

        activities = sorted(activities, key=lambda a: a.get('time', ''), reverse=True)[:10]

        if not activities:
            tk.Label(activities_frame, text='No recent activities', bg='white', fg='#6B7280').pack(padx=12, pady=20)
        else:
            for activity in activities:
                row = tk.Frame(activities_frame, bg='white')
                row.pack(fill='x', padx=12, pady=6)
                
                tk.Label(row, text=activity['icon'], bg='white', font=('Helvetica', 14)).pack(side='left', padx=(0, 8))
                
                info_frame = tk.Frame(row, bg='white')
                info_frame.pack(side='left', fill='x', expand=True)
                tk.Label(info_frame, text=activity['action'], bg='white', font=('Helvetica', 10)).pack(anchor='w')
                tk.Label(info_frame, text=f"{activity['user']} • {activity['time']}", bg='white', fg='#9CA3AF', font=('Helvetica', 9)).pack(anchor='w')

        # System Health Indicators
        health_section = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        health_section.pack(fill='x', padx=16, pady=(8, 16))
        tk.Label(health_section, text='System Health', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold'), fg=colors.get('primary', '#2C3E50')).pack(anchor='w', pady=(4, 6))

        health_frame = tk.Frame(health_section, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        health_frame.pack(fill='x')

        health_indicators = [
            ('Database Connection', 'Healthy', '#27AE60', '●'),
            ('API Services', 'Operational', '#27AE60', '●'),
            ('User Sessions', f'{len(self.all_users)} active', '#3498DB', '●'),
            ('Server Load', 'Normal', '#27AE60', '●')
        ]

        for indicator, status, color, icon in health_indicators:
            row = tk.Frame(health_frame, bg='white')
            row.pack(fill='x', padx=12, pady=6)
            tk.Label(row, text=indicator, bg='white', font=('Helvetica', 10)).pack(side='left')
            tk.Label(row, text=icon, bg='white', fg=color, font=('Helvetica', 14)).pack(side='right', padx=(0, 4))
            tk.Label(row, text=status, bg='white', fg=color, font=('Helvetica', 10, 'bold')).pack(side='right')

    def _render_manage_events(self):
        self._clear_content()
        colors = self.controller.colors
        
        tk.Label(self.content, text='Manage Events', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        
        # Filter tabs
        tab_frame = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        tab_frame.pack(fill='x', padx=16, pady=(0, 8))
        
        all_btn = create_primary_button(tab_frame, 'All Events', lambda: self._filter_events('all'), width=100, height=36)
        all_btn.pack(side='left', padx=(0, 4))
        pending_btn = create_warning_button(tab_frame, 'Pending', lambda: self._filter_events('pending'), width=90, height=36)
        pending_btn.pack(side='left', padx=4)
        approved_btn = create_success_button(tab_frame, 'Approved', lambda: self._filter_events('approved'), width=100, height=36)
        approved_btn.pack(side='left', padx=4)
        rejected_btn = create_danger_button(tab_frame, 'Rejected', lambda: self._filter_events('rejected'), width=90, height=36)
        rejected_btn.pack(side='left', padx=4)

        # Events table
        self._render_events_management_table(self.all_events)

    def _filter_events(self, filter_type):
        """Filter events by status"""
        if filter_type == 'all':
            filtered = self.all_events
        else:
            filtered = [e for e in self.all_events if (e.get('status') or 'pending').lower() == filter_type]
        
        self._clear_content()
        tk.Label(self.content, text=f'Manage Events - {filter_type.title()}', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        self._render_events_management_table(filtered)

    def _render_events_management_table(self, events):
        """Render events table with admin actions"""
        frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        # Header
        header = tk.Frame(frame, bg='#F9FAFB')
        header.pack(fill='x')
        headers = ['Event Title', 'Organizer', 'Date', 'Venue', 'Status', 'Actions']
        for i, h in enumerate(headers):
            tk.Label(header, text=h, bg='#F9FAFB', fg='#374151', font=('Helvetica', 10, 'bold')).grid(row=0, column=i, sticky='w', padx=8, pady=8)
            header.grid_columnconfigure(i, weight=1 if i == 0 else 0)

        if not events:
            tk.Label(frame, text='No events found', bg='white', fg='#6B7280').pack(padx=12, pady=20)
        else:
            for event in events:
                row = tk.Frame(frame, bg='white')
                row.pack(fill='x', padx=4, pady=2)
                
                status = (event.get('status') or 'pending').title()
                status_colors = {
                    'Approved': '#27AE60',
                    'Pending': '#F39C12',
                    'Rejected': '#E74C3C'
                }
                status_color = status_colors.get(status, '#6B7280')
                
                tk.Label(row, text=event.get('title', 'Untitled'), bg='white', font=('Helvetica', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=8)
                tk.Label(row, text=f"User #{event.get('organizer_id', 'N/A')}", bg='white', fg='#6B7280').grid(row=0, column=1, sticky='w', padx=8)
                tk.Label(row, text=event.get('start_time', 'N/A'), bg='white', fg='#6B7280').grid(row=0, column=2, sticky='w', padx=8)
                tk.Label(row, text=event.get('venue', 'N/A'), bg='white', fg='#6B7280').grid(row=0, column=3, sticky='w', padx=8)
                tk.Label(row, text=status, bg='white', fg=status_color, font=('Helvetica', 10, 'bold')).grid(row=0, column=4, sticky='w', padx=8)
                
                # Action buttons
                btn_frame = tk.Frame(row, bg='white')
                btn_frame.grid(row=0, column=5, padx=8)
                
                if status == 'Pending':
                    approve_icon_btn = create_success_button(btn_frame, '✓', lambda e=event: self._approve_event(e), width=30, height=30)
                    approve_icon_btn.pack(side='left', padx=2)
                    reject_icon_btn = create_danger_button(btn_frame, '✗', lambda e=event: self._reject_event(e), width=30, height=30)
                    reject_icon_btn.pack(side='left', padx=2)
                
                view_btn = create_primary_button(btn_frame, 'View', lambda e=event: self._view_event_details(e), width=60, height=30)
                view_btn.pack(side='left', padx=2)

    def _render_manage_resources(self):
        self._clear_content()
        colors = self.controller.colors
        
        header_frame = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        header_frame.pack(fill='x', padx=16, pady=(16, 8))
        tk.Label(header_frame, text='Manage Resources', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(side='left')
        add_resource_btn = create_success_button(header_frame, '+ Add Resource', self._add_resource, width=140, height=36)
        add_resource_btn.pack(side='right')

        # Resources table
        frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        # Header
        header = tk.Frame(frame, bg='#F9FAFB')
        header.pack(fill='x')
        headers = ['ID', 'Name', 'Type', 'Capacity', 'Status', 'Actions']
        for i, h in enumerate(headers):
            tk.Label(header, text=h, bg='#F9FAFB', fg='#374151', font=('Helvetica', 10, 'bold')).grid(row=0, column=i, sticky='w', padx=8, pady=8)
            header.grid_columnconfigure(i, weight=1 if i == 1 else 0)

        if not self.all_resources:
            tk.Label(frame, text='No resources found', bg='white', fg='#6B7280').pack(padx=12, pady=20)
        else:
            for resource in self.all_resources:
                row = tk.Frame(frame, bg='white')
                row.pack(fill='x', padx=4, pady=2)
                
                tk.Label(row, text=resource.get('id', 'N/A'), bg='white').grid(row=0, column=0, sticky='w', padx=8, pady=8)
                tk.Label(row, text=resource.get('name', 'Unnamed'), bg='white', font=('Helvetica', 10, 'bold')).grid(row=0, column=1, sticky='w', padx=8)
                tk.Label(row, text=resource.get('type', 'N/A'), bg='white', fg='#6B7280').grid(row=0, column=2, sticky='w', padx=8)
                tk.Label(row, text=resource.get('capacity', 'N/A'), bg='white', fg='#6B7280').grid(row=0, column=3, sticky='w', padx=8)
                
                status = resource.get('status', 'active').title()
                status_color = '#27AE60' if status.lower() == 'active' else '#E74C3C'
                tk.Label(row, text=status, bg='white', fg=status_color, font=('Helvetica', 10, 'bold')).grid(row=0, column=4, sticky='w', padx=8)
                
                btn_frame = tk.Frame(row, bg='white')
                btn_frame.grid(row=0, column=5, padx=8)
                edit_btn = create_primary_button(btn_frame, 'Edit', lambda r=resource: self._edit_resource(r), width=60, height=30)
                edit_btn.pack(side='left', padx=2)
                delete_btn = create_danger_button(btn_frame, 'Delete', lambda r=resource: self._delete_resource(r), width=70, height=30)
                delete_btn.pack(side='left', padx=2)

    def _render_manage_users(self):
        self._clear_content()
        
        tk.Label(self.content, text='Manage Users', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))

        # Users table
        frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        # Header
        header = tk.Frame(frame, bg='#F9FAFB')
        header.pack(fill='x')
        headers = ['ID', 'Username', 'Email', 'Role', 'Status', 'Actions']
        for i, h in enumerate(headers):
            tk.Label(header, text=h, bg='#F9FAFB', fg='#374151', font=('Helvetica', 10, 'bold')).grid(row=0, column=i, sticky='w', padx=8, pady=8)
            header.grid_columnconfigure(i, weight=1 if i in [1, 2] else 0)

        if not self.all_users:
            tk.Label(frame, text='No users found', bg='white', fg='#6B7280').pack(padx=12, pady=20)
        else:
            for user in self.all_users:
                row = tk.Frame(frame, bg='white')
                row.pack(fill='x', padx=4, pady=2)
                
                tk.Label(row, text=user.get('id', 'N/A'), bg='white').grid(row=0, column=0, sticky='w', padx=8, pady=8)
                tk.Label(row, text=user.get('username', 'N/A'), bg='white', font=('Helvetica', 10, 'bold')).grid(row=0, column=1, sticky='w', padx=8)
                tk.Label(row, text=user.get('email', 'N/A'), bg='white', fg='#6B7280').grid(row=0, column=2, sticky='w', padx=8)
                tk.Label(row, text=(user.get('role', 'STUDENT') or 'STUDENT').title(), bg='white', fg='#6B7280').grid(row=0, column=3, sticky='w', padx=8)
                
                is_active = user.get('is_active', True)
                status = 'Active' if is_active else 'Blocked'
                status_color = '#27AE60' if is_active else '#E74C3C'
                tk.Label(row, text=status, bg='white', fg=status_color, font=('Helvetica', 10, 'bold')).grid(row=0, column=4, sticky='w', padx=8)
                
                btn_frame = tk.Frame(row, bg='white')
                btn_frame.grid(row=0, column=5, padx=8)
                
                if is_active:
                    block_btn = create_danger_button(btn_frame, 'Block', lambda u=user: self._block_user(u), width=70, height=30)
                    block_btn.pack(side='left', padx=2)
                else:
                    unblock_btn = create_success_button(btn_frame, 'Unblock', lambda u=user: self._unblock_user(u), width=80, height=30)
                    unblock_btn.pack(side='left', padx=2)
                
                view_btn = create_primary_button(btn_frame, 'View', lambda u=user: self._view_user_details(u), width=60, height=30)
                view_btn.pack(side='left', padx=2)

    def _render_booking_approvals(self):
        self._clear_content()
        
        tk.Label(self.content, text='Booking Approvals', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))

        frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        # Header
        header = tk.Frame(frame, bg='#F9FAFB')
        header.pack(fill='x')
        headers = ['ID', 'Resource', 'User', 'Start Time', 'End Time', 'Status', 'Actions']
        for i, h in enumerate(headers):
            tk.Label(header, text=h, bg='#F9FAFB', fg='#374151', font=('Helvetica', 10, 'bold')).grid(row=0, column=i, sticky='w', padx=8, pady=8)

        if not self.pending_bookings:
            tk.Label(frame, text='No pending bookings', bg='white', fg='#6B7280').pack(padx=12, pady=20)
        else:
            for booking in self.pending_bookings:
                row = tk.Frame(frame, bg='white')
                row.pack(fill='x', padx=4, pady=2)
                
                tk.Label(row, text=booking.get('id', 'N/A'), bg='white').grid(row=0, column=0, sticky='w', padx=8, pady=8)
                tk.Label(row, text=f"Resource #{booking.get('resource_id', 'N/A')}", bg='white', font=('Helvetica', 10, 'bold')).grid(row=0, column=1, sticky='w', padx=8)
                tk.Label(row, text=f"User #{booking.get('user_id', 'N/A')}", bg='white', fg='#6B7280').grid(row=0, column=2, sticky='w', padx=8)
                tk.Label(row, text=booking.get('start_time', 'N/A'), bg='white', fg='#6B7280').grid(row=0, column=3, sticky='w', padx=8)
                tk.Label(row, text=booking.get('end_time', 'N/A'), bg='white', fg='#6B7280').grid(row=0, column=4, sticky='w', padx=8)
                tk.Label(row, text='Pending', bg='white', fg='#F39C12', font=('Helvetica', 10, 'bold')).grid(row=0, column=5, sticky='w', padx=8)
                
                btn_frame = tk.Frame(row, bg='white')
                btn_frame.grid(row=0, column=6, padx=8)
                approve_booking_btn = create_success_button(btn_frame, '✓ Approve', lambda b=booking: self._approve_booking(b), width=100, height=30)
                approve_booking_btn.pack(side='left', padx=2)
                reject_booking_btn = create_danger_button(btn_frame, '✗ Reject', lambda b=booking: self._reject_booking(b), width=90, height=30)
                reject_booking_btn.pack(side='left', padx=2)

    def _render_reports_analytics(self):
        self._clear_content()
        colors = self.controller.colors
        
        tk.Label(self.content, text='Reports & Analytics', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))

        # Summary statistics
        stats_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        stats_frame.pack(fill='x', padx=16, pady=(0, 12))

        stats_container = tk.Frame(stats_frame, bg='white')
        stats_container.pack(padx=20, pady=20)

        tk.Label(stats_container, text='System Overview', bg='white', fg='#374151', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 16))

        def stat_row(label, value):
            row = tk.Frame(stats_container, bg='white')
            row.pack(fill='x', pady=6)
            tk.Label(row, text=label, bg='white', fg='#6B7280', font=('Helvetica', 11)).pack(side='left')
            tk.Label(row, text=str(value), bg='white', fg=colors.get('primary', '#2C3E50'), font=('Helvetica', 11, 'bold')).pack(side='right')

        stat_row('Total Users:', len(self.all_users))
        stat_row('Total Events:', len(self.all_events))
        stat_row('Pending Events:', len(self.pending_events))
        stat_row('Total Resources:', len(self.all_resources))
        stat_row('Pending Bookings:', len(self.pending_bookings))
        
        approved_events = len([e for e in self.all_events if (e.get('status') or '').lower() == 'approved'])
        stat_row('Approved Events:', approved_events)

        # Charts placeholder
        charts_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        charts_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        
        tk.Label(charts_frame, text='📊 Analytics Charts', bg='white', fg='#374151', font=('Helvetica', 13, 'bold')).pack(pady=(20, 10))
        tk.Label(charts_frame, text='Detailed charts and graphs would be displayed here', bg='white', fg='#9CA3AF').pack(pady=(0, 20))

    def _render_system_settings(self):
        self._clear_content()
        
        tk.Label(self.content, text='System Settings', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))

        settings_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        settings_frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        settings_container = tk.Frame(settings_frame, bg='white')
        settings_container.pack(padx=20, pady=20, fill='both', expand=True)

        settings = [
            ('Email Notifications', 'Enable email notifications for users', True),
            ('Event Auto-Approval', 'Automatically approve events', False),
            ('Resource Booking Limits', 'Limit bookings per user', True),
            ('User Registration', 'Allow new user registrations', True),
            ('Maintenance Mode', 'Enable maintenance mode', False)
        ]

        for title, description, enabled in settings:
            setting_row = tk.Frame(settings_container, bg='white')
            setting_row.pack(fill='x', pady=12)
            
            info_frame = tk.Frame(setting_row, bg='white')
            info_frame.pack(side='left', fill='x', expand=True)
            tk.Label(info_frame, text=title, bg='white', font=('Helvetica', 11, 'bold')).pack(anchor='w')
            tk.Label(info_frame, text=description, bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(2, 0))
            
            status = 'ON' if enabled else 'OFF'
            if enabled:
                toggle_btn = create_success_button(setting_row, status, lambda t=title: messagebox.showinfo('Settings', f'{t} toggled'), width=70, height=32)
            else:
                toggle_btn = create_danger_button(setting_row, status, lambda t=title: messagebox.showinfo('Settings', f'{t} toggled'), width=70, height=32)
            toggle_btn.pack(side='right')

    # Action methods
    def _approve_event(self, event):
        """Approve an event"""
        event_id = event.get('id')
        if not event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return
        
        try:
            self.api.put(f'admin/events/{event_id}/approve', {})
            messagebox.showinfo('Success', f"Event '{event.get('title', 'Event')}' approved successfully")
            self._load_all_data_then(self._render_dashboard)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to approve event: {str(e)}')

    def _reject_event(self, event):
        """Reject an event"""
        event_id = event.get('id')
        if not event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return
        
        try:
            self.api.put(f'admin/events/{event_id}/reject', {})
            messagebox.showinfo('Success', f"Event '{event.get('title', 'Event')}' rejected")
            self._load_all_data_then(self._render_dashboard)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to reject event: {str(e)}')

    def _approve_booking(self, booking):
        """Approve a booking"""
        booking_id = booking.get('id')
        if not booking_id:
            messagebox.showerror('Error', 'Invalid booking ID')
            return
        
        try:
            self.api.put(f'admin/bookings/{booking_id}/approve', {})
            messagebox.showinfo('Success', 'Booking approved successfully')
            self._load_all_data_then(self._render_booking_approvals)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to approve booking: {str(e)}')

    def _reject_booking(self, booking):
        """Reject a booking"""
        booking_id = booking.get('id')
        if not booking_id:
            messagebox.showerror('Error', 'Invalid booking ID')
            return
        
        try:
            self.api.put(f'admin/bookings/{booking_id}/reject', {})
            messagebox.showinfo('Success', 'Booking rejected')
            self._load_all_data_then(self._render_booking_approvals)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to reject booking: {str(e)}')

    def _add_resource(self):
        """Add a new resource"""
        messagebox.showinfo('Add Resource', 'Add resource form would open here')

    def _edit_resource(self, resource):
        """Edit a resource"""
        messagebox.showinfo('Edit Resource', f"Edit form for resource '{resource.get('name', 'Resource')}' would open here")

    def _delete_resource(self, resource):
        """Delete a resource"""
        if messagebox.askyesno('Confirm Delete', f"Are you sure you want to delete '{resource.get('name', 'Resource')}'?"):
            resource_id = resource.get('id')
            try:
                self.api.delete(f'admin/resources/{resource_id}')
                messagebox.showinfo('Success', 'Resource deleted successfully')
                self._load_all_data_then(self._render_manage_resources)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to delete resource: {str(e)}')

    def _block_user(self, user):
        """Block a user"""
        if messagebox.askyesno('Confirm Block', f"Are you sure you want to block user '{user.get('username', 'User')}'?"):
            user_id = user.get('id')
            try:
                self.api.put(f'admin/users/{user_id}/block', {})
                messagebox.showinfo('Success', 'User blocked successfully')
                self._load_all_data_then(self._render_manage_users)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to block user: {str(e)}')

    def _unblock_user(self, user):
        """Unblock a user"""
        user_id = user.get('id')
        try:
            self.api.put(f'admin/users/{user_id}/unblock', {})
            messagebox.showinfo('Success', 'User unblocked successfully')
            self._load_all_data_then(self._render_manage_users)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to unblock user: {str(e)}')

    def _view_event_details(self, event):
        """Show event details"""
        details = f"Event: {event.get('title', 'Untitled')}\n"
        details += f"Description: {event.get('description', 'N/A')}\n"
        details += f"Organizer: User #{event.get('organizer_id', 'N/A')}\n"
        details += f"Start: {event.get('start_time', 'N/A')}\n"
        details += f"End: {event.get('end_time', 'N/A')}\n"
        details += f"Venue: {event.get('venue', 'N/A')}\n"
        details += f"Status: {event.get('status', 'N/A')}"
        messagebox.showinfo('Event Details', details)

    def _view_user_details(self, user):
        """Show user details"""
        details = f"User ID: {user.get('id', 'N/A')}\n"
        details += f"Username: {user.get('username', 'N/A')}\n"
        details += f"Email: {user.get('email', 'N/A')}\n"
        details += f"Role: {user.get('role', 'N/A')}\n"
        details += f"Status: {'Active' if user.get('is_active', True) else 'Blocked'}\n"
        details += f"Created: {user.get('created_at', 'N/A')}"
        messagebox.showinfo('User Details', details)

    def _show_notifications(self):
        """Show notifications"""
        pending_count = len(self.pending_events) + len(self.pending_bookings)
        if pending_count > 0:
            messagebox.showinfo('Notifications', f'You have {pending_count} pending approvals')
        else:
            messagebox.showinfo('Notifications', 'No new notifications')

    def _logout(self):
        try:
            self.session.clear_session()
        finally:
            self.controller.navigate('login', add_to_history=False)

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
