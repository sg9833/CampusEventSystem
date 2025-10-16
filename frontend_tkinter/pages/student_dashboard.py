import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.button_styles import ButtonStyles
from utils.canvas_button import create_primary_button, create_secondary_button, create_success_button, create_danger_button


class StudentDashboard(tk.Frame):
    """Student Dashboard with sidebar navigation and dynamic content area."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors.get('background', '#ECF0F1'))
        self.controller = controller
        self.api = APIClient()
        self.session = SessionManager()

        # Data caches
        self.events = []
        self.my_bookings = []
        self.registered_events = []

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
        name = u.get('username') or u.get('email') or 'Student'
        role = (self.session.get_role() or 'STUDENT').title()

        # Profile section
        profile = tk.Frame(sidebar, bg=colors.get('primary', '#2C3E50'))
        profile.pack(fill='x', pady=(16, 8))
        tk.Label(profile, text='🎓', bg=colors.get('primary', '#2C3E50'), fg='white', font=('Helvetica', 26)).pack()
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
                canvas.itemconfig(rect, fill='#3498DB')
            
            def on_leave(e):
                canvas.itemconfig(rect, fill=colors.get('primary', '#2C3E50'))
            
            def on_click(e):
                cmd()
            
            canvas.tag_bind('btn', '<Enter>', on_enter)
            canvas.tag_bind('btn', '<Leave>', on_leave)
            canvas.tag_bind('btn', '<Button-1>', on_click)

        add_btn('Dashboard', self._render_dashboard, icon='🏠')
        add_btn('Browse Events', self._render_browse_events, icon='🗂️')
        add_btn('My Registrations', self._render_my_registrations, icon='✅')
        # Note: Resource booking and My Bookings removed - organizers only
        add_btn('Profile Settings', self._render_profile_settings, icon='⚙️')
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
        welcome = tk.Label(top, text=f"Welcome, {user.get('username') or 'Student'}", bg='white', fg=colors.get('primary', '#2C3E50'), font=('Helvetica', 13, 'bold'))
        welcome.pack(side='left', padx=16)

        # Search bar
        search_frame = tk.Frame(top, bg='white')
        search_frame.pack(side='right', padx=16)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
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
                self.events = self.api.get('events') or []
            except Exception as e:
                errors.append(('events', str(e)))
                self.events = []
            # Note: Bookings removed - students cannot book resources
            # try:
            #     self.my_bookings = self.api.get('bookings/my') or []
            # except Exception as e:
            #     errors.append(('bookings', str(e)))
            #     self.my_bookings = []
            self.my_bookings = []  # Students don't have bookings
            try:
                self.registered_events = self.api.get('events/registered') or []
            except Exception as e:
                errors.append(('registered', str(e)))
                self.registered_events = []

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

        total_events = len(self.events)
        registered = len(self.registered_events)
        active_bookings = len([b for b in self.my_bookings if (b.get('status') or '').lower() in ('active', 'approved', 'pending')])

        c1 = card(stats, 'Total Events', total_events, colors.get('secondary', '#3498DB'))
        c2 = card(stats, 'Registered Events', registered, colors.get('success', '#27AE60'))
        c3 = card(stats, 'Active Bookings', active_bookings, colors.get('primary', '#2C3E50'))
        c1.grid(row=0, column=0, sticky='ew', padx=(0, 8))
        c2.grid(row=0, column=1, sticky='ew', padx=8)
        c3.grid(row=0, column=2, sticky='ew', padx=(8, 0))

        # Upcoming events (next 5)
        upc = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        upc.pack(fill='x', padx=16, pady=(8, 8))
        tk.Label(upc, text='Upcoming Events', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold'), fg=colors.get('primary', '#2C3E50')).pack(anchor='w', pady=(4, 6))

        list_frame = tk.Frame(upc, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        list_frame.pack(fill='x')

        events_sorted = sorted(self.events, key=lambda e: self._parse_dt(e.get('start_time')) or datetime.max)[:5]
        if not events_sorted:
            tk.Label(list_frame, text='No upcoming events', bg='white', fg='#6B7280').pack(padx=12, pady=12)
        for ev in events_sorted:
            row = tk.Frame(list_frame, bg='white')
            row.pack(fill='x', padx=8, pady=4)
            title = ev.get('title') or 'Untitled Event'
            when = ev.get('start_time') or ''
            tk.Label(row, text=f"📅 {title}", bg='white', font=('Helvetica', 12, 'bold')).pack(side='left', padx=(4, 8))
            tk.Label(row, text=when, bg='white', fg='#6B7280').pack(side='left')
            reg_btn = create_success_button(row, 'Register', lambda e=ev: self._register_event(e), width=90, height=30)
            reg_btn.pack(side='right')

        # Recent activities
        recent = tk.Frame(self.content, bg=self.controller.colors.get('background', '#ECF0F1'))
        recent.pack(fill='both', expand=True, padx=16, pady=(8, 16))
        tk.Label(recent, text='Recent Activities', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold'), fg=colors.get('primary', '#2C3E50')).pack(anchor='w', pady=(4, 6))

        timeline = tk.Frame(recent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        timeline.pack(fill='both', expand=True)

        items = []
        for ev in self.registered_events[:5]:
            items.append((ev.get('registered_at') or '', f"Registered for {ev.get('title')}", '✅'))
        for b in self.my_bookings[:5]:
            items.append((b.get('created_at') or '', f"Booking {b.get('status', '').title()} for resource {b.get('resource_id')}", '📚'))
        if not items:
            tk.Label(timeline, text='No recent activity', bg='white', fg='#6B7280').pack(padx=12, pady=12)
        else:
            for ts, text, icon in items:
                row = tk.Frame(timeline, bg='white')
                row.pack(fill='x', padx=12, pady=6)
                tk.Label(row, text=icon, bg='white').pack(side='left', padx=(0, 8))
                tk.Label(row, text=text, bg='white').pack(side='left')
                tk.Label(row, text=ts, bg='white', fg='#9CA3AF').pack(side='right')

    def _render_browse_events(self):
        self._clear_content()
        tk.Label(self.content, text='Browse Events', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        self._render_events_table(self.events)

    def _render_my_registrations(self):
        self._clear_content()
        tk.Label(self.content, text='My Registrations', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        self._render_events_table(self.registered_events)

    # My Bookings removed - students cannot book resources
    # def _render_my_bookings(self):
    #     self._clear_content()
    #     tk.Label(self.content, text='My Bookings', bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
    #     cols = ('id', 'resource_id', 'start_time', 'end_time', 'status')
    #     tv = ttk.Treeview(self.content, columns=cols, show='headings')
    #     for c in cols:
    #         tv.heading(c, text=c.replace('_', ' ').title())
    #         tv.column(c, width=140)
    #     for b in self.my_bookings:
    #         tv.insert('', 'end', values=(b.get('id'), b.get('resource_id'), b.get('start_time'), b.get('end_time'), b.get('status')))
    #     tv.pack(fill='both', expand=True, padx=16, pady=(0, 16))

    # Resource booking removed - organizers only
    # def _render_book_resources(self):
    #     """Navigate to browse resources page with booking functionality"""
    #     self.controller.navigate('browse_resources')

    def _render_profile_settings(self):
        """Navigate to profile page"""
        self.controller.navigate('profile')

    def _render_events_table(self, events):
        cols = ('title', 'start_time', 'venue', 'actions')
        frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        frame.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        # Header row
        header = tk.Frame(frame, bg='#F9FAFB')
        header.pack(fill='x')
        for i, h in enumerate(['Title', 'Start Time', 'Venue', '']):
            tk.Label(header, text=h, bg='#F9FAFB', fg='#374151', font=('Helvetica', 10, 'bold')).grid(row=0, column=i, sticky='w', padx=8, pady=8)
            header.grid_columnconfigure(i, weight=1 if i == 0 else 0)

        # Rows
        if not events:
            tk.Label(frame, text='No items', bg='white', fg='#6B7280').pack(padx=12, pady=12)
        else:
            for e in events:
                row = tk.Frame(frame, bg='white')
                row.pack(fill='x', padx=4, pady=2)
                tk.Label(row, text=e.get('title') or 'Untitled', bg='white').grid(row=0, column=0, sticky='w', padx=8, pady=8)
                tk.Label(row, text=e.get('start_time') or '', bg='white', fg='#6B7280').grid(row=0, column=1, sticky='w', padx=8)
                tk.Label(row, text=e.get('venue') or '', bg='white', fg='#6B7280').grid(row=0, column=2, sticky='w', padx=8)
                reg_btn = create_success_button(row, 'Register', lambda ev=e: self._register_event(ev), width=90, height=30)
                reg_btn.grid(row=0, column=3, padx=8)

    # Actions
    def _register_event(self, event):
        """Register for an event"""
        event_id = event.get('id')
        event_title = event.get('title', 'Event')
        
        if not event_id:
            messagebox.showerror('Error', 'Invalid event')
            return
        
        # Check if already registered
        if any(e.get('id') == event_id for e in self.registered_events):
            messagebox.showinfo('Already Registered', f"You are already registered for '{event_title}'")
            return
        
        # Confirm registration
        if not messagebox.askyesno('Confirm Registration', f"Do you want to register for '{event_title}'?"):
            return
        
        try:
            # Call registration endpoint
            response = self.api.post(f'events/{event_id}/register', {})
            messagebox.showinfo('Success', f"Successfully registered for '{event_title}'!")
            
            # Reload data to refresh the view
            self._load_all_data_then(self._render_dashboard)
        except Exception as e:
            error_msg = str(e)
            if 'already registered' in error_msg.lower():
                messagebox.showinfo('Already Registered', f"You are already registered for '{event_title}'")
            elif 'not approved' in error_msg.lower() or 'non-approved' in error_msg.lower():
                messagebox.showerror('Error', 'This event is not yet approved by admin')
            else:
                messagebox.showerror('Error', f'Failed to register: {error_msg}')

    def _logout(self):
        try:
            self.session.clear_session()
        finally:
            self.controller.navigate('login', add_to_history=False)

    def _on_search(self):
        q = (self.search_var.get() or '').lower().strip()
        if not q:
            self._render_browse_events()
            return
        filtered = [e for e in self.events if q in (e.get('title') or '').lower()]
        self._clear_content()
        tk.Label(self.content, text=f"Search results for '{q}'", bg=self.controller.colors.get('background', '#ECF0F1'), font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=16, pady=(16, 8))
        self._render_events_table(filtered)

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
