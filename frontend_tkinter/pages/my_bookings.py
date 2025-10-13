import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime, timedelta
from calendar import monthrange

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.canvas_button import create_primary_button, create_secondary_button, create_success_button, create_danger_button


class MyBookingsPage(tk.Frame):
    """User's bookings page with tabbed interface and calendar view."""

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
        self.all_bookings = []
        self.filtered_bookings = []
        self.current_status = 'pending'
        self.view_mode = 'list'  # 'list' or 'calendar'
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        
        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_bookings()

    def _build_ui(self):
        """Build the main UI"""
        # Header
        header = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        header.grid(row=0, column=0, sticky='ew')
        
        header_content = tk.Frame(header, bg='white')
        header_content.pack(fill='x', padx=30, pady=15)
        
        # Title
        title_frame = tk.Frame(header_content, bg='white')
        title_frame.pack(side='left')
        tk.Label(title_frame, text='📚 My Bookings', bg='white', fg='#1F2937', font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='View and manage your resource bookings', bg='white', fg='#1F2937', font=('Helvetica', 10)).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(header_content, bg='white')
        btn_frame.pack(side='right')
        
        create_secondary_button(btn_frame, text='🔄 Refresh', command=self._load_bookings).pack(side='left', padx=(0, 8))
        
        # View toggle
        self.view_toggle_btn = create_primary_button(btn_frame, text='📅 Calendar View', command=self._toggle_view)
        self.view_toggle_btn.pack(side='left', padx=(0, 8))
        
        create_success_button(btn_frame, text='➕ New Booking', command=self._new_booking).pack(side='left')
        
        # Content container
        content_container = tk.Frame(self, bg=self.colors.get('background', '#ECF0F1'))
        content_container.grid(row=1, column=0, sticky='nsew')
        content_container.grid_rowconfigure(0, weight=1)
        content_container.grid_columnconfigure(0, weight=1)
        
        # Tab navigation
        tab_nav = tk.Frame(content_container, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        tab_nav.grid(row=0, column=0, sticky='ew', padx=30, pady=(20, 0))
        
        tabs = [
            ('pending', 'Pending Approval', '#F59E0B'),
            ('approved', 'Approved', '#3B82F6'),
            ('completed', 'Completed', '#10B981'),
            ('rejected', 'Rejected', '#EF4444')
        ]
        
        self.tab_buttons = {}
        for status, label, color in tabs:
            btn = tk.Button(tab_nav, text=label, command=lambda s=status: self._switch_tab(s), bg='white', fg='#1F2937', relief='flat', font=('Helvetica', 11), padx=20, pady=12, cursor='hand2')
            btn.pack(side='left')
            self.tab_buttons[status] = btn
        
        # Content area (will contain either list or calendar view)
        self.content_area = tk.Frame(content_container, bg=self.colors.get('background', '#ECF0F1'))
        self.content_area.grid(row=1, column=0, sticky='nsew', padx=30, pady=(0, 20))
        
        # Set initial active tab
        self._update_active_tab()

    def _build_list_view(self):
        """Build list view with booking cards"""
        # Clear content area
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
        
        # Update canvas width on resize
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag('all')[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Render bookings
        self._render_booking_cards(content)

    def _build_calendar_view(self):
        """Build calendar view"""
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Calendar header
        header = tk.Frame(self.content_area, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        header.pack(fill='x', pady=(10, 10))
        
        header_content = tk.Frame(header, bg='white')
        header_content.pack(padx=20, pady=12)
        
        # Month navigation
        create_secondary_button(header_content, text='◀', command=self._prev_month).pack(side='left', padx=(0, 12))
        
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month_label = tk.Label(header_content, text=f"{month_names[self.current_month - 1]} {self.current_year}", bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold'))
        month_label.pack(side='left', padx=12)
        
        create_secondary_button(header_content, text='▶', command=self._next_month).pack(side='left', padx=(12, 0))
        
        # Today button
        create_primary_button(header_content, text='Today', command=self._goto_today).pack(side='right', padx=(20, 0))
        
        # Calendar grid
        cal_frame = tk.Frame(self.content_area, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        cal_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Scrollable calendar content
        canvas = tk.Canvas(cal_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(cal_frame, orient='vertical', command=canvas.yview)
        
        cal_content = tk.Frame(canvas, bg='white')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=cal_content, anchor='nw')
        cal_content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        self._render_calendar(cal_content)

    def _render_calendar(self, parent):
        """Render calendar grid"""
        # Day headers
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        header_row = tk.Frame(parent, bg='#F9FAFB')
        header_row.pack(fill='x', padx=20, pady=(20, 0))
        
        for day_name in day_names:
            tk.Label(header_row, text=day_name, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 10, 'bold'), width=15, height=2).pack(side='left', padx=1)
        
        # Get calendar data
        first_day = datetime(self.current_year, self.current_month, 1)
        last_day_num = monthrange(self.current_year, self.current_month)[1]
        start_weekday = first_day.weekday()  # Monday = 0
        
        # Create calendar grid
        grid_frame = tk.Frame(parent, bg='white')
        grid_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        current_date = datetime.now().date()
        day_num = 1
        week_num = 0
        
        # Group bookings by date
        bookings_by_date = {}
        for booking in self.all_bookings:
            booking_date = self._parse_date(booking.get('date', ''))
            if booking_date and booking_date.year == self.current_year and booking_date.month == self.current_month:
                date_key = booking_date.day
                if date_key not in bookings_by_date:
                    bookings_by_date[date_key] = []
                bookings_by_date[date_key].append(booking)
        
        # Build weeks
        while day_num <= last_day_num:
            week_row = tk.Frame(grid_frame, bg='white')
            week_row.pack(fill='x', pady=1)
            
            for weekday in range(7):
                if week_num == 0 and weekday < start_weekday:
                    # Empty cell before month starts
                    tk.Frame(week_row, bg='#F9FAFB', width=15, height=100).pack(side='left', padx=1)
                elif day_num > last_day_num:
                    # Empty cell after month ends
                    tk.Frame(week_row, bg='#F9FAFB', width=15, height=100).pack(side='left', padx=1)
                else:
                    # Day cell
                    cell_date = datetime(self.current_year, self.current_month, day_num).date()
                    is_today = cell_date == current_date
                    
                    cell = tk.Frame(week_row, bg='#FFFFFF' if not is_today else '#E0E7FF', highlightthickness=1, highlightbackground='#DBEAFE' if is_today else '#E5E7EB', width=15, height=100)
                    cell.pack(side='left', padx=1, fill='both', expand=True)
                    cell.pack_propagate(False)
                    
                    # Day number
                    day_header = tk.Frame(cell, bg='#FFFFFF' if not is_today else '#E0E7FF')
                    day_header.pack(fill='x', padx=4, pady=(4, 2))
                    
                    tk.Label(day_header, text=str(day_num), bg='#FFFFFF' if not is_today else '#E0E7FF', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='ne')
                    
                    # Bookings for this day
                    if day_num in bookings_by_date:
                        bookings_container = tk.Frame(cell, bg='#FFFFFF' if not is_today else '#E0E7FF')
                        bookings_container.pack(fill='both', expand=True, padx=2, pady=(0, 2))
                        
                        for booking in bookings_by_date[day_num][:3]:  # Show max 3
                            status = booking.get('status', 'pending').lower()
                            status_colors = {
                                'pending': '#F59E0B',
                                'approved': '#3B82F6',
                                'completed': '#10B981',
                                'rejected': '#EF4444'
                            }
                            color = status_colors.get(status, '#6B7280')
                            
                            booking_tag = tk.Frame(bookings_container, bg=color, height=4, cursor='hand2')
                            booking_tag.pack(fill='x', pady=1)
                            booking_tag.bind('<Button-1>', lambda e, b=booking: self._show_booking_details(b))
                            
                            # Tooltip on hover
                            resource_name = booking.get('resource_name', 'Booking')
                            booking_tag.bind('<Enter>', lambda e, text=resource_name: self._show_tooltip(e, text))
                            booking_tag.bind('<Leave>', lambda e: self._hide_tooltip())
                        
                        if len(bookings_by_date[day_num]) > 3:
                            more_label = tk.Label(bookings_container, text=f'+{len(bookings_by_date[day_num]) - 3}', bg='#FFFFFF' if not is_today else '#E0E7FF', fg='#1F2937', font=('Helvetica', 7))
                            more_label.pack(anchor='center', pady=1)
                    
                    day_num += 1
            
            week_num += 1

    def _render_booking_cards(self, parent):
        """Render booking cards in list view"""
        if not self.filtered_bookings:
            # Empty state
            empty_frame = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            empty_frame.pack(fill='both', expand=True, pady=20)
            
            tk.Label(empty_frame, text='📋', bg='white', font=('Helvetica', 48)).pack(pady=(40, 10))
            tk.Label(empty_frame, text=f'No {self.current_status} bookings', bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold')).pack()
            tk.Label(empty_frame, text='Your bookings will appear here', bg='white', fg='#1F2937', font=('Helvetica', 10)).pack(pady=(4, 40))
        else:
            # Booking cards
            for booking in self.filtered_bookings:
                card = self._create_booking_card(booking)
                card.pack(fill='x', pady=(0, 12))

    def _create_booking_card(self, booking):
        """Create a booking card"""
        card = tk.Frame(self.content_area, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=16)
        
        # Header row
        header_row = tk.Frame(content, bg='white')
        header_row.pack(fill='x', pady=(0, 12))
        
        # Resource info
        resource_frame = tk.Frame(header_row, bg='white')
        resource_frame.pack(side='left', fill='x', expand=True)
        
        resource_name = booking.get('resource_name', 'Unknown Resource')
        resource_type = booking.get('resource_type', 'Resource')
        
        tk.Label(resource_frame, text=resource_name, bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w')
        tk.Label(resource_frame, text=f"Type: {resource_type}", bg='white', fg='#1F2937', font=('Helvetica', 9)).pack(anchor='w', pady=(2, 0))
        
        # Status badge
        status = booking.get('status', 'pending').lower()
        status_config = {
            'pending': ('Pending Approval', '#F59E0B', '#FFFBEB'),
            'approved': ('Approved', '#3B82F6', '#EFF6FF'),
            'completed': ('Completed', '#10B981', '#F0FDF4'),
            'rejected': ('Rejected', '#EF4444', '#FEF2F2')
        }
        
        status_text, status_color, status_bg = status_config.get(status, ('Unknown', '#6B7280', '#F3F4F6'))
        
        status_badge = tk.Frame(header_row, bg=status_bg, highlightthickness=1, highlightbackground=status_color)
        status_badge.pack(side='right')
        
        tk.Label(status_badge, text=status_text, bg=status_bg, fg=status_color, font=('Helvetica', 9, 'bold'), padx=12, pady=4).pack()
        
        # Booking details
        details_frame = tk.Frame(content, bg='#F9FAFB')
        details_frame.pack(fill='x', pady=(0, 12))
        
        details_content = tk.Frame(details_frame, bg='#F9FAFB')
        details_content.pack(padx=16, pady=12)
        
        # Date and time
        booking_date = self._format_date(booking.get('date', ''))
        start_time = booking.get('start_time', 'N/A')
        end_time = booking.get('end_time', 'N/A')
        
        self._add_detail_item(details_content, '📅 Date:', booking_date)
        self._add_detail_item(details_content, '🕐 Time:', f"{start_time} - {end_time}")
        self._add_detail_item(details_content, '👥 Attendees:', str(booking.get('attendees', 'N/A')))
        
        # Purpose
        purpose = booking.get('purpose', 'No purpose provided')
        tk.Label(content, text='Purpose:', bg='white', fg='#1F2937', font=('Helvetica', 9, 'bold')).pack(anchor='w', pady=(0, 4))
        tk.Label(content, text=purpose, bg='white', fg='#1F2937', font=('Helvetica', 10), wraplength=700, justify='left').pack(anchor='w', pady=(0, 12))
        
        # Priority indicator
        priority = booking.get('priority', 'normal')
        if priority == 'urgent':
            priority_frame = tk.Frame(content, bg='#FEF3C7', highlightthickness=1, highlightbackground='#F59E0B')
            priority_frame.pack(fill='x', pady=(0, 12))
            tk.Label(priority_frame, text='🔴 Urgent Priority', bg='#FEF3C7', fg='#1F2937', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(anchor='w')
        
        # Actions
        actions_frame = tk.Frame(content, bg='white')
        actions_frame.pack(fill='x')
        
        create_secondary_button(actions_frame, text='View Details', command=lambda: self._show_booking_details(booking)).pack(side='left', padx=(0, 8))
        
        # Conditional actions based on status
        if status in ['pending', 'approved']:
            # Check if booking date hasn't passed
            booking_date_obj = self._parse_date(booking.get('date', ''))
            if booking_date_obj and booking_date_obj >= datetime.now().date():
                create_danger_button(actions_frame, text='Cancel Booking', command=lambda: self._cancel_booking(booking)).pack(side='left', padx=(0, 8))
        
        if status == 'approved':
            create_success_button(actions_frame, text='📥 Download Confirmation', command=lambda: self._download_confirmation(booking)).pack(side='left', padx=(0, 8))
        
        if status == 'rejected':
            create_primary_button(actions_frame, text='🔄 Rebook', command=lambda: self._rebook(booking)).pack(side='left', padx=(0, 8))
        
        return card

    def _add_detail_item(self, parent, label, value):
        """Add detail item"""
        frame = tk.Frame(parent, bg='#F9FAFB')
        frame.pack(side='left', padx=(0, 20))
        tk.Label(frame, text=label, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 9)).pack(side='left', padx=(0, 4))
        tk.Label(frame, text=value, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 9, 'bold')).pack(side='left')

    def _load_bookings(self):
        """Load bookings from API"""
        self._show_loading()
        
        def worker():
            try:
                # Load all bookings
                self.all_bookings = self.api.get('bookings/my') or []
                
                self.after(0, self._filter_and_render)
            except Exception as e:
                error_msg = str(e)
                def show_error():
                    messagebox.showerror('Error', f'Failed to load bookings: {error_msg}')
                    self.all_bookings = []
                    self._filter_and_render()
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _show_loading(self):
        """Show loading indicator"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.content_area, bg=self.colors.get('background', '#ECF0F1'))
        loading_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(loading_frame, text='Loading bookings...', bg=self.colors.get('background', '#ECF0F1'), fg='#1F2937', font=('Helvetica', 12)).pack()
        
        spinner = ttk.Progressbar(loading_frame, mode='indeterminate', length=300)
        spinner.pack(pady=10)
        spinner.start(10)

    def _filter_and_render(self):
        """Filter bookings by current status and render"""
        # Filter by status
        self.filtered_bookings = [b for b in self.all_bookings if b.get('status', '').lower() == self.current_status]
        
        # Sort by date (newest first)
        self.filtered_bookings.sort(key=lambda x: self._parse_date(x.get('date', '')) or datetime.min.date(), reverse=True)
        
        # Render based on view mode
        if self.view_mode == 'list':
            self._build_list_view()
        else:
            self._build_calendar_view()

    def _switch_tab(self, status):
        """Switch to a different tab"""
        self.current_status = status
        self._update_active_tab()
        self._filter_and_render()

    def _update_active_tab(self):
        """Update active tab styling"""
        for status, btn in self.tab_buttons.items():
            if status == self.current_status:
                btn.config(bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 11, 'bold'))
            else:
                btn.config(bg='white', fg='#1F2937', font=('Helvetica', 11))

    def _toggle_view(self):
        """Toggle between list and calendar view"""
        if self.view_mode == 'list':
            self.view_mode = 'calendar'
            self.view_toggle_btn.config(text='📋 List View')
        else:
            self.view_mode = 'list'
            self.view_toggle_btn.config(text='📅 Calendar View')
        
        self._filter_and_render()

    def _prev_month(self):
        """Navigate to previous month"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._build_calendar_view()

    def _next_month(self):
        """Navigate to next month"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._build_calendar_view()

    def _goto_today(self):
        """Go to current month"""
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self._build_calendar_view()

    def _show_booking_details(self, booking):
        """Show booking details in modal"""
        modal = tk.Toplevel(self)
        modal.title('Booking Details')
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
        status = booking.get('status', 'pending').lower()
        status_colors = {
            'pending': '#F59E0B',
            'approved': '#3B82F6',
            'completed': '#10B981',
            'rejected': '#EF4444'
        }
        header_color = status_colors.get(status, '#6B7280')
        
        header = tk.Frame(modal, bg=header_color)
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=header_color)
        header_content.pack(padx=20, pady=20)
        
        tk.Label(header_content, text='📋', bg=header_color, font=('Helvetica', 36)).pack()
        tk.Label(header_content, text='Booking Details', bg=header_color, fg='white', font=('Helvetica', 16, 'bold')).pack(pady=(8, 0))
        
        # Scrollable content
        canvas = tk.Canvas(modal, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(modal, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg='white')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=content, anchor='nw')
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        details_frame = tk.Frame(content, bg='white')
        details_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Details
        self._add_modal_detail(details_frame, '🏢 Resource:', booking.get('resource_name', 'N/A'))
        self._add_modal_detail(details_frame, '📋 Type:', booking.get('resource_type', 'N/A'))
        self._add_modal_detail(details_frame, '📅 Date:', self._format_date(booking.get('date', '')))
        self._add_modal_detail(details_frame, '🕐 Start Time:', booking.get('start_time', 'N/A'))
        self._add_modal_detail(details_frame, '🕐 End Time:', booking.get('end_time', 'N/A'))
        self._add_modal_detail(details_frame, '👥 Attendees:', str(booking.get('attendees', 'N/A')))
        self._add_modal_detail(details_frame, '⚪ Priority:', booking.get('priority', 'normal').title())
        
        # Status
        status_text = status.title()
        tk.Frame(details_frame, bg='#E5E7EB', height=1).pack(fill='x', pady=16)
        self._add_modal_detail(details_frame, '📊 Status:', status_text)
        
        # Purpose
        tk.Frame(details_frame, bg='#E5E7EB', height=1).pack(fill='x', pady=16)
        tk.Label(details_frame, text='Purpose:', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        tk.Label(details_frame, text=booking.get('purpose', 'No purpose provided'), bg='white', fg='#1F2937', font=('Helvetica', 10), wraplength=520, justify='left').pack(anchor='w', pady=(0, 16))
        
        # Additional requirements
        requirements = booking.get('additional_requirements', '').strip()
        if requirements:
            tk.Label(details_frame, text='Additional Requirements:', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 8))
            tk.Label(details_frame, text=requirements, bg='white', fg='#1F2937', font=('Helvetica', 10), wraplength=520, justify='left').pack(anchor='w', pady=(0, 16))
        
        # Rejection reason (if rejected)
        if status == 'rejected':
            rejection_reason = booking.get('rejection_reason', 'No reason provided')
            tk.Frame(details_frame, bg='#E5E7EB', height=1).pack(fill='x', pady=16)
            
            rejection_frame = tk.Frame(details_frame, bg='#FEF2F2', highlightthickness=1, highlightbackground='#EF4444')
            rejection_frame.pack(fill='x', pady=(0, 16))
            
            rejection_content = tk.Frame(rejection_frame, bg='#FEF2F2')
            rejection_content.pack(padx=16, pady=12)
            
            tk.Label(rejection_content, text='Rejection Reason:', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 10, 'bold')).pack(anchor='w')
            tk.Label(rejection_content, text=rejection_reason, bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9), wraplength=520, justify='left').pack(anchor='w', pady=(4, 0))
        
        # Close button
        create_secondary_button(details_frame, text='Close', command=modal.destroy).pack(fill='x', pady=(16, 0))

    def _add_modal_detail(self, parent, label, value):
        """Add detail row to modal"""
        row = tk.Frame(parent, bg='white')
        row.pack(fill='x', pady=6)
        tk.Label(row, text=label, bg='white', fg='#1F2937', font=('Helvetica', 10), width=18, anchor='w').pack(side='left')
        tk.Label(row, text=str(value), bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(side='left')

    def _cancel_booking(self, booking):
        """Cancel a booking"""
        result = messagebox.askyesno('Cancel Booking', 
                                     f"Are you sure you want to cancel the booking for '{booking.get('resource_name', 'this resource')}'?\n\nThis action cannot be undone.")
        
        if result:
            def worker():
                try:
                    booking_id = booking.get('id')
                    self.api.delete(f'bookings/{booking_id}')
                    
                    def show_success():
                        messagebox.showinfo('Success', 'Booking cancelled successfully.')
                        self._load_bookings()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to cancel booking: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _download_confirmation(self, booking):
        """Download booking confirmation"""
        messagebox.showinfo('Download Confirmation', 
                          f"Booking confirmation for '{booking.get('resource_name', 'Resource')}' would be downloaded as a PDF.\n\n"
                          f"Date: {self._format_date(booking.get('date', ''))}\n"
                          f"Time: {booking.get('start_time', '')} - {booking.get('end_time', '')}")

    def _rebook(self, booking):
        """Rebook a rejected booking"""
        messagebox.showinfo('Rebook', 
                          f"You will be redirected to the booking page with pre-filled details from this rejected booking.\n\n"
                          f"Resource: {booking.get('resource_name', 'N/A')}")

    def _new_booking(self):
        """Create new booking"""
        messagebox.showinfo('New Booking', 'You will be redirected to the book resource page.')

    def _show_tooltip(self, event, text):
        """Show tooltip on hover"""
        # Simple tooltip implementation
        self.tooltip = tk.Toplevel()
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        label = tk.Label(self.tooltip, text=text, bg='#1F2937', fg='white', font=('Helvetica', 9), padx=8, pady=4)
        label.pack()

    def _hide_tooltip(self):
        """Hide tooltip"""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def _format_date(self, date_str):
        """Format date for display"""
        date_obj = self._parse_date(date_str)
        if date_obj:
            return date_obj.strftime('%B %d, %Y')
        return date_str or 'N/A'

    def _parse_date(self, date_str):
        """Parse date string"""
        if not date_str:
            return None
        try:
            for fmt in ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
                try:
                    return datetime.strptime(date_str[:10], '%Y-%m-%d').date()
                except:
                    continue
        except:
            pass
        return None
