import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime
from PIL import Image, ImageTk
import io
import base64
import re

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.canvas_button import create_primary_button, create_secondary_button, create_success_button, create_warning_button, create_danger_button


class ProfilePage(tk.Frame):
    """User profile and account settings page."""

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
        self.profile_data = {}
        self.profile_photo = None
        self.photo_preview = None
        self.photo_data = None
        self.current_tab = tk.StringVar(value='profile')
        
        # Password strength
        self.password_strength = tk.StringVar(value='')
        
        # Notification preferences
        self.notif_bookings = tk.BooleanVar(value=True)
        self.notif_events = tk.BooleanVar(value=True)
        self.notif_approvals = tk.BooleanVar(value=True)
        self.notif_reminders = tk.BooleanVar(value=True)
        self.notif_newsletters = tk.BooleanVar(value=False)
        
        # Privacy settings
        self.privacy_show_email = tk.BooleanVar(value=False)
        self.privacy_show_phone = tk.BooleanVar(value=False)
        self.privacy_show_profile = tk.BooleanVar(value=True)
        
        # Layout - row 2 (content) should expand, not row 0 (header)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_profile()

    def _build_ui(self):
        """Build the main UI"""
        # Header
        header = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        header.grid(row=0, column=0, sticky='ew')
        
        header_content = tk.Frame(header, bg='white')
        header_content.pack(fill='x', padx=30, pady=(12, 8))
        
        # Title
        title_frame = tk.Frame(header_content, bg='white')
        title_frame.pack(side='left')
        tk.Label(title_frame, text='👤 My Profile', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Manage your profile and account settings', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w', pady=(2, 0))
        
        # Action buttons
        btn_frame = tk.Frame(header_content, bg='white')
        btn_frame.pack(side='right')
        
        refresh_btn = create_secondary_button(btn_frame, '🔄 Refresh', self._load_profile, width=100, height=28)
        refresh_btn.pack(side='left')
        
        # Tab navigation
        tabs_frame = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        tabs_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=(0, 0))
        
        tabs_content = tk.Frame(tabs_frame, bg='white')
        tabs_content.pack(fill='x', padx=20, pady=12)
        
        # Profile tab button (canvas-based for macOS)
        profile_tab_frame = tk.Frame(tabs_content, bg='white')
        profile_tab_frame.pack(side='left', padx=(0, 8))
        
        self.profile_tab_canvas = tk.Canvas(profile_tab_frame, width=160, height=38, bg='white', highlightthickness=0, cursor='hand2')
        self.profile_tab_canvas.pack()
        
        self.profile_tab_rect = self.profile_tab_canvas.create_rectangle(0, 0, 160, 38, fill=self.colors.get('secondary', '#3498DB'), outline='', tags='btn')
        self.profile_tab_text = self.profile_tab_canvas.create_text(80, 19, text='👤 View Profile', fill='#FFFFFF', font=('Helvetica', 10, 'bold'), tags='btn')
        
        self.profile_tab_canvas.tag_bind('btn', '<Button-1>', lambda e: self._switch_tab('profile'))
        self.profile_tab_canvas.tag_bind('btn', '<Enter>', lambda e: self.profile_tab_canvas.itemconfig(self.profile_tab_rect, fill=self._get_tab_hover_color('profile')))
        self.profile_tab_canvas.tag_bind('btn', '<Leave>', lambda e: self.profile_tab_canvas.itemconfig(self.profile_tab_rect, fill=self._get_tab_color('profile')))
        
        # Settings tab button (canvas-based for macOS)
        settings_tab_frame = tk.Frame(tabs_content, bg='white')
        settings_tab_frame.pack(side='left')
        
        self.settings_tab_canvas = tk.Canvas(settings_tab_frame, width=190, height=38, bg='white', highlightthickness=0, cursor='hand2')
        self.settings_tab_canvas.pack()
        
        self.settings_tab_rect = self.settings_tab_canvas.create_rectangle(0, 0, 190, 38, fill='#F3F4F6', outline='', tags='btn')
        self.settings_tab_text = self.settings_tab_canvas.create_text(95, 19, text='⚙️ Account Settings', fill='#374151', font=('Helvetica', 10, 'bold'), tags='btn')
        
        self.settings_tab_canvas.tag_bind('btn', '<Button-1>', lambda e: self._switch_tab('settings'))
        self.settings_tab_canvas.tag_bind('btn', '<Enter>', lambda e: self.settings_tab_canvas.itemconfig(self.settings_tab_rect, fill=self._get_tab_hover_color('settings')))
        self.settings_tab_canvas.tag_bind('btn', '<Leave>', lambda e: self.settings_tab_canvas.itemconfig(self.settings_tab_rect, fill=self._get_tab_color('settings')))
        
        # Content area
        self.content_area = tk.Frame(self, bg=self.colors.get('background', '#ECF0F1'))
        self.content_area.grid(row=2, column=0, sticky='nsew', padx=30, pady=(12, 12))

    def _load_profile(self):
        """Load user profile from API or use fallback data"""
        self._show_loading()
        
        def worker():
            try:
                # Try to get profile from API
                self.profile_data = self.api.get('users/profile') or {}
                
                # If empty, use session data as fallback
                if not self.profile_data:
                    user = self.session.get_user()
                    if user:
                        self.profile_data = {
                            'name': user.get('name', 'User Name'),
                            'email': user.get('email', 'user@example.com'),
                            'username': user.get('username', user.get('email', '').split('@')[0]),
                            'role': user.get('role', 'student'),
                            'phone': user.get('phone', 'N/A'),
                            'department': user.get('department', 'N/A'),
                            'student_id': user.get('student_id', 'N/A'),
                            'year': user.get('year', 'N/A'),
                            'status': 'active',
                            'joined_date': user.get('created_at', '2024-01-01'),
                            'events_attended': 0,
                            'bookings_made': 0,
                            'photo_url': ''
                        }
                
                # Set notification preferences from profile
                prefs = self.profile_data.get('notification_preferences', {})
                self.notif_bookings.set(prefs.get('bookings', True))
                self.notif_events.set(prefs.get('events', True))
                self.notif_approvals.set(prefs.get('approvals', True))
                self.notif_reminders.set(prefs.get('reminders', True))
                self.notif_newsletters.set(prefs.get('newsletters', False))
                
                # Set privacy settings from profile
                privacy = self.profile_data.get('privacy_settings', {})
                self.privacy_show_email.set(privacy.get('show_email', False))
                self.privacy_show_phone.set(privacy.get('show_phone', False))
                self.privacy_show_profile.set(privacy.get('show_profile', True))
                
                self.after(0, self._render_content)
            except Exception as error:
                # Use session data as fallback
                def show_with_fallback():
                    user = self.session.get_user()
                    if user:
                        self.profile_data = {
                            'name': user.get('name', 'User Name'),
                            'email': user.get('email', 'user@example.com'),
                            'username': user.get('username', user.get('email', '').split('@')[0]),
                            'role': user.get('role', 'student'),
                            'phone': user.get('phone', 'N/A'),
                            'department': user.get('department', 'N/A'),
                            'student_id': user.get('student_id', 'N/A'),
                            'year': user.get('year', 'N/A'),
                            'status': 'active',
                            'joined_date': user.get('created_at', '2024-01-01'),
                            'events_attended': 0,
                            'bookings_made': 0,
                            'photo_url': ''
                        }
                    else:
                        self.profile_data = {
                            'name': 'User Name',
                            'email': 'user@example.com',
                            'username': 'user',
                            'role': 'student',
                            'phone': 'N/A',
                            'department': 'N/A',
                            'student_id': 'N/A',
                            'year': 'N/A',
                            'status': 'active',
                            'joined_date': '2024-01-01',
                            'events_attended': 0,
                            'bookings_made': 0,
                            'photo_url': ''
                        }
                    self._render_content()
                
                self.after(0, show_with_fallback)
        
        threading.Thread(target=worker, daemon=True).start()

    def _show_loading(self):
        """Show loading indicator"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.content_area, bg=self.colors.get('background', '#ECF0F1'))
        loading_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(loading_frame, text='Loading profile...', bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 12)).pack()
        
        spinner = ttk.Progressbar(loading_frame, mode='indeterminate', length=300)
        spinner.pack(pady=10)
        spinner.start(10)

    def _get_tab_color(self, tab):
        """Get current tab color based on selection"""
        is_active = (self.current_tab.get() == tab)
        return self.colors.get('secondary', '#3498DB') if is_active else '#F3F4F6'
    
    def _get_tab_hover_color(self, tab):
        """Get tab hover color"""
        is_active = (self.current_tab.get() == tab)
        return '#2980B9' if is_active else '#E5E7EB'
    
    def _switch_tab(self, tab):
        """Switch between tabs"""
        self.current_tab.set(tab)
        
        if tab == 'profile':
            self.profile_tab_canvas.itemconfig(self.profile_tab_rect, fill=self.colors.get('secondary', '#3498DB'))
            self.profile_tab_canvas.itemconfig(self.profile_tab_text, fill='#FFFFFF')
            self.settings_tab_canvas.itemconfig(self.settings_tab_rect, fill='#F3F4F6')
            self.settings_tab_canvas.itemconfig(self.settings_tab_text, fill='#374151')
        else:
            self.profile_tab_canvas.itemconfig(self.profile_tab_rect, fill='#F3F4F6')
            self.profile_tab_canvas.itemconfig(self.profile_tab_text, fill='#374151')
            self.settings_tab_canvas.itemconfig(self.settings_tab_rect, fill=self.colors.get('secondary', '#3498DB'))
            self.settings_tab_canvas.itemconfig(self.settings_tab_text, fill='#FFFFFF')
        
        self._render_content()

    def _render_content(self):
        """Render content based on current tab"""
        if self.current_tab.get() == 'profile':
            self._render_profile_view()
        else:
            self._render_settings_view()

    def _render_profile_view(self):
        """Render profile view tab"""
        # Clear content
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Scrollable container
        canvas = tk.Canvas(self.content_area, bg=self.colors.get('background', '#ECF0F1'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient='vertical', command=canvas.yview)
        
        content = tk.Frame(canvas, bg=self.colors.get('background', '#ECF0F1'))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=content, anchor='nw')
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Update canvas width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag('all')[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Profile header card
        header_card = tk.Frame(content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        header_card.pack(fill='x', pady=(0, 16))
        
        header_content = tk.Frame(header_card, bg='white')
        header_content.pack(fill='x', padx=30, pady=30)
        
        # Profile photo section
        photo_frame = tk.Frame(header_content, bg='white')
        photo_frame.pack(side='left', padx=(0, 30))
        
        # Profile photo
        photo_container = tk.Frame(photo_frame, bg='#E5E7EB', width=150, height=150, highlightthickness=2, highlightbackground=self.colors.get('secondary', '#3498DB'))
        photo_container.pack()
        photo_container.pack_propagate(False)
        
        # Load or show placeholder
        photo_url = self.profile_data.get('photo_url', '')
        if photo_url:
            try:
                # For demo, show placeholder
                tk.Label(photo_container, text='📷', bg='#E5E7EB', font=('Helvetica', 48)).pack(expand=True)
            except:
                tk.Label(photo_container, text='👤', bg='#E5E7EB', font=('Helvetica', 48)).pack(expand=True)
        else:
            tk.Label(photo_container, text='👤', bg='#E5E7EB', font=('Helvetica', 48)).pack(expand=True)
        
        # Upload button
        change_photo_btn = create_primary_button(photo_frame, '📷 Change Photo', self._upload_photo, width=140, height=32)
        change_photo_btn.pack(pady=(12, 0))
        
        # Profile info
        info_frame = tk.Frame(header_content, bg='white')
        info_frame.pack(side='left', fill='both', expand=True)
        
        # Name and role
        name = self.profile_data.get('name', 'User Name')
        role = self.profile_data.get('role', 'User')
        
        tk.Label(info_frame, text=name, bg='white', fg='#1F2937', font=('Helvetica', 24, 'bold')).pack(anchor='w')
        
        role_badge = tk.Frame(info_frame, bg='#EFF6FF', highlightthickness=1, highlightbackground='#BFDBFE')
        role_badge.pack(anchor='w', pady=(8, 16))
        tk.Label(role_badge, text=role.upper(), bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 9, 'bold'), padx=12, pady=4).pack()
        
        # Quick stats
        stats_frame = tk.Frame(info_frame, bg='white')
        stats_frame.pack(anchor='w', fill='x')
        
        self._add_stat_item(stats_frame, '📅', 'Events Attended', str(self.profile_data.get('events_attended', 0)))
        self._add_stat_item(stats_frame, '📋', 'Bookings Made', str(self.profile_data.get('bookings_made', 0)))
        self._add_stat_item(stats_frame, '📆', 'Member Since', self._format_date(self.profile_data.get('joined_date', '')))
        
        # Personal details card
        personal_card = tk.Frame(content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        personal_card.pack(fill='x', pady=(0, 16))
        
        personal_content = tk.Frame(personal_card, bg='white')
        personal_content.pack(fill='x', padx=30, pady=20)
        
        self._add_section_header(personal_content, '📋 Personal Information')
        
        details_grid = tk.Frame(personal_content, bg='white')
        details_grid.pack(fill='x', pady=(12, 0))
        
        # Left column
        left_col = tk.Frame(details_grid, bg='white')
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        self._add_detail_row(left_col, 'Full Name:', self.profile_data.get('name', 'N/A'))
        self._add_detail_row(left_col, 'Email:', self.profile_data.get('email', 'N/A'))
        self._add_detail_row(left_col, 'Phone:', self.profile_data.get('phone', 'N/A'))
        
        # Right column
        right_col = tk.Frame(details_grid, bg='white')
        right_col.pack(side='left', fill='both', expand=True)
        
        self._add_detail_row(right_col, 'Department:', self.profile_data.get('department', 'N/A'))
        self._add_detail_row(right_col, 'Student ID:', self.profile_data.get('student_id', 'N/A'))
        self._add_detail_row(right_col, 'Year:', self.profile_data.get('year', 'N/A'))
        
        # Account details card
        account_card = tk.Frame(content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        account_card.pack(fill='x', pady=(0, 16))
        
        account_content = tk.Frame(account_card, bg='white')
        account_content.pack(fill='x', padx=30, pady=20)
        
        self._add_section_header(account_content, '🔐 Account Details')
        
        account_grid = tk.Frame(account_content, bg='white')
        account_grid.pack(fill='x', pady=(12, 0))
        
        # Account info
        left_col2 = tk.Frame(account_grid, bg='white')
        left_col2.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        self._add_detail_row(left_col2, 'Username:', self.profile_data.get('username', 'N/A'))
        self._add_detail_row(left_col2, 'Role:', self.profile_data.get('role', 'N/A'))
        
        right_col2 = tk.Frame(account_grid, bg='white')
        right_col2.pack(side='left', fill='both', expand=True)
        
        self._add_detail_row(right_col2, 'Account Status:', self.profile_data.get('status', 'Active'))
        self._add_detail_row(right_col2, 'Joined Date:', self._format_date(self.profile_data.get('joined_date', '')))
        
        # Edit button
        edit_profile_btn = create_primary_button(content, '✏️ Edit Profile', self._edit_profile, width=600, height=48)
        edit_profile_btn.pack(fill='x', pady=(0, 16))

    def _render_settings_view(self):
        """Render account settings tab"""
        # Clear content
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Scrollable container
        canvas = tk.Canvas(self.content_area, bg=self.colors.get('background', '#ECF0F1'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient='vertical', command=canvas.yview)
        
        content = tk.Frame(canvas, bg=self.colors.get('background', '#ECF0F1'))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=content, anchor='nw')
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Update canvas width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag('all')[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Change password card
        password_card = tk.Frame(content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        password_card.pack(fill='x', pady=(0, 16))
        
        password_content = tk.Frame(password_card, bg='white')
        password_content.pack(fill='x', padx=30, pady=20)
        
        self._add_section_header(password_content, '🔒 Change Password')
        
        form_frame = tk.Frame(password_content, bg='white')
        form_frame.pack(fill='x', pady=(12, 0))
        
        # Current password
        tk.Label(form_frame, text='Current Password:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self.current_password_entry = tk.Entry(form_frame, show='•', font=('Helvetica', 11), relief='solid', borderwidth=1)
        self.current_password_entry.pack(fill='x', ipady=6, pady=(0, 12))
        
        # New password
        tk.Label(form_frame, text='New Password:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self.new_password_entry = tk.Entry(form_frame, show='•', font=('Helvetica', 11), relief='solid', borderwidth=1)
        self.new_password_entry.pack(fill='x', ipady=6, pady=(0, 8))
        self.new_password_entry.bind('<KeyRelease>', self._check_password_strength)
        
        # Password strength indicator
        self.strength_frame = tk.Frame(form_frame, bg='white')
        self.strength_frame.pack(fill='x', pady=(0, 12))
        
        self.strength_bar = tk.Frame(self.strength_frame, bg='#E5E7EB', height=4)
        self.strength_bar.pack(fill='x', pady=(0, 4))
        
        self.strength_label = tk.Label(self.strength_frame, text='', bg='white', fg='#6B7280', font=('Helvetica', 8))
        self.strength_label.pack(anchor='w')
        
        # Confirm password
        tk.Label(form_frame, text='Confirm New Password:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self.confirm_password_entry = tk.Entry(form_frame, show='•', font=('Helvetica', 11), relief='solid', borderwidth=1)
        self.confirm_password_entry.pack(fill='x', ipady=6, pady=(0, 12))
        
        # Change password button
        change_password_btn = create_primary_button(form_frame, '🔒 Change Password', self._change_password, width=600, height=44)
        change_password_btn.pack(fill='x')
        
        # Notification preferences card
        notif_card = tk.Frame(content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        notif_card.pack(fill='x', pady=(0, 16))
        
        notif_content = tk.Frame(notif_card, bg='white')
        notif_content.pack(fill='x', padx=30, pady=20)
        
        self._add_section_header(notif_content, '🔔 Email Notification Preferences')
        
        tk.Label(notif_content, text='Choose which email notifications you want to receive:', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 12))
        
        notif_options = tk.Frame(notif_content, bg='white')
        notif_options.pack(fill='x')
        
        tk.Checkbutton(notif_options, text='📋 Booking confirmations and updates', variable=self.notif_bookings, bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=4)
        tk.Checkbutton(notif_options, text='📅 Event invitations and reminders', variable=self.notif_events, bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=4)
        tk.Checkbutton(notif_options, text='✅ Approval status notifications', variable=self.notif_approvals, bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=4)
        tk.Checkbutton(notif_options, text='⏰ Upcoming event reminders (24h before)', variable=self.notif_reminders, bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=4)
        tk.Checkbutton(notif_options, text='📰 Campus newsletters and announcements', variable=self.notif_newsletters, bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=4)
        
        # Privacy settings card
        privacy_card = tk.Frame(content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        privacy_card.pack(fill='x', pady=(0, 16))
        
        privacy_content = tk.Frame(privacy_card, bg='white')
        privacy_content.pack(fill='x', padx=30, pady=20)
        
        self._add_section_header(privacy_content, '🔐 Privacy Settings')
        
        tk.Label(privacy_content, text='Control who can see your information:', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 12))
        
        privacy_options = tk.Frame(privacy_content, bg='white')
        privacy_options.pack(fill='x')
        
        tk.Checkbutton(privacy_options, text='📧 Show email address in public profile', variable=self.privacy_show_email, bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=4)
        tk.Checkbutton(privacy_options, text='📱 Show phone number in public profile', variable=self.privacy_show_phone, bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=4)
        tk.Checkbutton(privacy_options, text='👤 Show profile in user directory', variable=self.privacy_show_profile, bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=4)
        
        # Save settings button
        save_settings_btn = create_success_button(content, '💾 Save Settings', self._save_settings, width=600, height=48)
        save_settings_btn.pack(fill='x', pady=(0, 16))
        
        # Danger zone
        danger_card = tk.Frame(content, bg='#FEF2F2', highlightthickness=2, highlightbackground='#E74C3C')
        danger_card.pack(fill='x', pady=(0, 16))
        
        danger_content = tk.Frame(danger_card, bg='#FEF2F2')
        danger_content.pack(fill='x', padx=30, pady=20)
        
        tk.Label(danger_content, text='⚠️ Danger Zone', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 8))
        tk.Label(danger_content, text='Once you delete your account, there is no going back. Please be certain.', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 12))
        
        delete_account_btn = create_danger_button(danger_content, '🗑️ Delete Account', self._delete_account, width=180, height=44)
        delete_account_btn.pack(anchor='w')

    def _add_stat_item(self, parent, icon, label, value):
        """Add statistics item"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(side='left', padx=(0, 40))
        
        tk.Label(frame, text=icon, bg='white', font=('Helvetica', 20)).pack(side='left', padx=(0, 8))
        
        text_frame = tk.Frame(frame, bg='white')
        text_frame.pack(side='left')
        
        tk.Label(text_frame, text=value, bg='white', fg='#1F2937', font=('Helvetica', 16, 'bold')).pack(anchor='w')
        tk.Label(text_frame, text=label, bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w')

    def _add_section_header(self, parent, text):
        """Add section header"""
        tk.Label(parent, text=text, bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 8))
        tk.Frame(parent, bg='#E5E7EB', height=1).pack(fill='x', pady=(0, 0))

    def _add_detail_row(self, parent, label, value):
        """Add detail row"""
        row = tk.Frame(parent, bg='white')
        row.pack(fill='x', pady=8)
        
        tk.Label(row, text=label, bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        tk.Label(row, text=str(value), bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(2, 0))

    def _upload_photo(self):
        """Upload profile photo"""
        file_path = filedialog.askopenfilename(
            title='Select Profile Photo',
            filetypes=[('Image Files', '*.png *.jpg *.jpeg *.gif *.bmp')]
        )
        
        if not file_path:
            return
        
        try:
            # Open and resize image
            img = Image.open(file_path)
            
            # Check file size (max 5MB)
            import os
            file_size = os.path.getsize(file_path)
            if file_size > 5 * 1024 * 1024:
                messagebox.showerror('Error', 'Image file too large. Maximum size is 5MB.')
                return
            
            # Resize for preview
            img.thumbnail((150, 150), Image.Resampling.LANCZOS)
            
            # Show preview modal
            self._show_photo_preview(img, file_path)
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load image: {str(e)}')

    def _show_photo_preview(self, img, file_path):
        """Show photo preview modal"""
        modal = tk.Toplevel(self)
        modal.title('Preview Profile Photo')
        modal.geometry('400x500')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 200
        y = (modal.winfo_screenheight() // 2) - 250
        modal.geometry(f'400x500+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        tk.Label(header, text='📷 Preview Profile Photo', bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 14, 'bold')).pack(pady=20)
        
        # Preview
        content = tk.Frame(modal, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(content, text='Preview:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w', pady=(0, 8))
        
        # Photo preview
        photo_frame = tk.Frame(content, bg='#E5E7EB', width=200, height=200, highlightthickness=2, highlightbackground=self.colors.get('secondary', '#3498DB'))
        photo_frame.pack(pady=10)
        photo_frame.pack_propagate(False)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(photo_frame, image=photo, bg='#E5E7EB')
        label.image = photo  # Keep reference
        label.pack(expand=True)
        
        tk.Label(content, text='This photo will be visible on your profile.', bg='white', fg='#6B7280', font=('Helvetica', 9), wraplength=340).pack(pady=(12, 20))
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        upload_photo_btn = create_success_button(btn_frame, '✅ Upload Photo', lambda: [modal.destroy(), self._confirm_upload_photo(file_path)], width=340, height=44)
        upload_photo_btn.pack(fill='x', pady=(0, 8))
        
        cancel_btn = create_secondary_button(btn_frame, 'Cancel', modal.destroy, width=340, height=44)
        cancel_btn.pack(fill='x')

    def _confirm_upload_photo(self, file_path):
        """Confirm and upload photo"""
        def worker():
            try:
                # Read file and encode to base64
                with open(file_path, 'rb') as f:
                    photo_data = base64.b64encode(f.read()).decode('utf-8')
                
                # Upload to API
                data = {'photo': photo_data}
                self.api.post('users/profile/photo', data)
                
                def show_success():
                    messagebox.showinfo('Success', 'Profile photo updated successfully!')
                    self._load_profile()
                
                self.after(0, show_success)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to upload photo: {str(e)}')
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _check_password_strength(self, event=None):
        """Check password strength"""
        password = self.new_password_entry.get()
        
        if not password:
            self.strength_bar.config(bg='#E5E7EB')
            self.strength_label.config(text='')
            return
        
        # Calculate strength
        strength = 0
        feedback = []
        
        if len(password) >= 8:
            strength += 1
        else:
            feedback.append('at least 8 characters')
        
        if re.search(r'[a-z]', password):
            strength += 1
        else:
            feedback.append('lowercase letter')
        
        if re.search(r'[A-Z]', password):
            strength += 1
        else:
            feedback.append('uppercase letter')
        
        if re.search(r'\d', password):
            strength += 1
        else:
            feedback.append('number')
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            strength += 1
        else:
            feedback.append('special character')
        
        # Update UI
        if strength <= 2:
            color = '#E74C3C'
            text = '❌ Weak password'
            if feedback:
                text += f' - Add: {", ".join(feedback[:2])}'
        elif strength == 3:
            color = '#F39C12'
            text = '⚠️ Fair password'
            if feedback:
                text += f' - Add: {", ".join(feedback[:1])}'
        elif strength == 4:
            color = '#3498DB'
            text = '✓ Good password'
        else:
            color = '#27AE60'
            text = '✅ Strong password'
        
        self.strength_bar.config(bg=color)
        self.strength_label.config(text=text, fg=color)

    def _change_password(self):
        """Change password"""
        current = self.current_password_entry.get().strip()
        new = self.new_password_entry.get().strip()
        confirm = self.confirm_password_entry.get().strip()
        
        # Validate
        if not current:
            messagebox.showerror('Validation Error', 'Please enter your current password.')
            return
        
        if not new:
            messagebox.showerror('Validation Error', 'Please enter a new password.')
            return
        
        if len(new) < 8:
            messagebox.showerror('Validation Error', 'New password must be at least 8 characters long.')
            return
        
        if new != confirm:
            messagebox.showerror('Validation Error', 'New passwords do not match.')
            return
        
        if current == new:
            messagebox.showerror('Validation Error', 'New password must be different from current password.')
            return
        
        def worker():
            try:
                data = {
                    'current_password': current,
                    'new_password': new
                }
                self.api.put('users/change-password', data)
                
                def show_success():
                    messagebox.showinfo('Success',
                                      '✅ Password changed successfully!\n\n'
                                      'Please use your new password on your next login.')
                    # Clear fields
                    self.current_password_entry.delete(0, 'end')
                    self.new_password_entry.delete(0, 'end')
                    self.confirm_password_entry.delete(0, 'end')
                    self.strength_bar.config(bg='#E5E7EB')
                    self.strength_label.config(text='')
                
                self.after(0, show_success)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to change password: {str(e)}')
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _save_settings(self):
        """Save notification and privacy settings"""
        def worker():
            try:
                data = {
                    'notification_preferences': {
                        'bookings': self.notif_bookings.get(),
                        'events': self.notif_events.get(),
                        'approvals': self.notif_approvals.get(),
                        'reminders': self.notif_reminders.get(),
                        'newsletters': self.notif_newsletters.get()
                    },
                    'privacy_settings': {
                        'show_email': self.privacy_show_email.get(),
                        'show_phone': self.privacy_show_phone.get(),
                        'show_profile': self.privacy_show_profile.get()
                    }
                }
                
                self.api.put('users/profile', data)
                
                def show_success():
                    messagebox.showinfo('Success',
                                      '✅ Settings saved successfully!\n\n'
                                      'Your preferences have been updated.')
                
                self.after(0, show_success)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to save settings: {str(e)}')
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _edit_profile(self):
        """Open edit profile modal"""
        modal = tk.Toplevel(self)
        modal.title('Edit Profile')
        modal.geometry('600x700')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 300
        y = (modal.winfo_screenheight() // 2) - 350
        modal.geometry(f'600x700+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        tk.Label(header, text='✏️ Edit Profile', bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Scrollable content
        canvas = tk.Canvas(modal, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(modal, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg='white')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=content, anchor='nw')
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        form_frame = tk.Frame(content, bg='white')
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Form fields
        fields = {}
        
        # Name
        tk.Label(form_frame, text='Full Name:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        fields['name'] = tk.Entry(form_frame, font=('Helvetica', 11), relief='solid', borderwidth=1)
        fields['name'].insert(0, self.profile_data.get('name', ''))
        fields['name'].pack(fill='x', ipady=6, pady=(0, 12))
        
        # Email
        tk.Label(form_frame, text='Email:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        fields['email'] = tk.Entry(form_frame, font=('Helvetica', 11), relief='solid', borderwidth=1)
        fields['email'].insert(0, self.profile_data.get('email', ''))
        fields['email'].pack(fill='x', ipady=6, pady=(0, 12))
        
        # Phone
        tk.Label(form_frame, text='Phone:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        fields['phone'] = tk.Entry(form_frame, font=('Helvetica', 11), relief='solid', borderwidth=1)
        fields['phone'].insert(0, self.profile_data.get('phone', ''))
        fields['phone'].pack(fill='x', ipady=6, pady=(0, 12))
        
        # Department
        tk.Label(form_frame, text='Department:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        fields['department'] = tk.Entry(form_frame, font=('Helvetica', 11), relief='solid', borderwidth=1)
        fields['department'].insert(0, self.profile_data.get('department', ''))
        fields['department'].pack(fill='x', ipady=6, pady=(0, 12))
        
        # Student ID
        tk.Label(form_frame, text='Student ID:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        fields['student_id'] = tk.Entry(form_frame, font=('Helvetica', 11), relief='solid', borderwidth=1)
        fields['student_id'].insert(0, self.profile_data.get('student_id', ''))
        fields['student_id'].pack(fill='x', ipady=6, pady=(0, 12))
        
        # Year
        tk.Label(form_frame, text='Year:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        fields['year'] = tk.Entry(form_frame, font=('Helvetica', 11), relief='solid', borderwidth=1)
        fields['year'].insert(0, self.profile_data.get('year', ''))
        fields['year'].pack(fill='x', ipady=6, pady=(0, 12))
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        save_changes_btn = create_success_button(btn_frame, '💾 Save Changes', lambda: self._save_profile_changes(modal, fields), width=540, height=48)
        save_changes_btn.pack(fill='x', pady=(0, 8))
        
        cancel_modal_btn = create_secondary_button(btn_frame, 'Cancel', modal.destroy, width=540, height=48)
        cancel_modal_btn.pack(fill='x')

    def _save_profile_changes(self, modal, fields):
        """Save profile changes"""
        # Get values
        data = {}
        for key, entry in fields.items():
            value = entry.get().strip()
            data[key] = value
        
        # Validate
        if not data.get('name'):
            messagebox.showerror('Validation Error', 'Name is required.')
            return
        
        if not data.get('email'):
            messagebox.showerror('Validation Error', 'Email is required.')
            return
        
        # Validate email format
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
            messagebox.showerror('Validation Error', 'Invalid email format.')
            return
        
        def worker():
            try:
                self.api.put('users/profile', data)
                
                def show_success():
                    messagebox.showinfo('Success', '✅ Profile updated successfully!')
                    modal.destroy()
                    self._load_profile()
                
                self.after(0, show_success)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to update profile: {str(e)}')
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _delete_account(self):
        """Delete user account"""
        result = messagebox.askyesno('Delete Account',
                                     '⚠️ WARNING: This action cannot be undone!\n\n'
                                     'Are you sure you want to delete your account?\n\n'
                                     'This will:\n'
                                     '• Delete all your data\n'
                                     '• Cancel all your bookings\n'
                                     '• Remove you from all events\n'
                                     '• Permanently delete your profile',
                                     icon='warning')
        
        if not result:
            return
        
        # Second confirmation
        result2 = messagebox.askyesno('Final Confirmation',
                                      '⚠️ FINAL WARNING\n\n'
                                      'This is your last chance to cancel.\n\n'
                                      'Delete your account permanently?',
                                      icon='warning')
        
        if result2:
            messagebox.showinfo('Account Deletion',
                              'Account deletion feature is not yet implemented.\n\n'
                              'Please contact an administrator to delete your account.')

    def _format_date(self, date_str):
        """Format date for display"""
        if not date_str:
            return 'N/A'
        try:
            date_obj = datetime.strptime(date_str[:10] if len(date_str) >= 10 else date_str, '%Y-%m-%d')
            return date_obj.strftime('%B %d, %Y')
        except:
            return date_str or 'N/A'
