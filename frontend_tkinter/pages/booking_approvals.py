import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from datetime import datetime, timedelta
from calendar import monthrange

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.email_service import get_email_service


class BookingApprovalsPage(tk.Frame):
    """Admin page for approving/rejecting pending booking requests."""

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
        self.pending_bookings = []
        self.selected_bookings = []
        self.view_mode = 'list'  # 'list' or 'calendar'
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.sort_by = tk.StringVar(value='date')
        
        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_pending_bookings()

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
        tk.Label(title_frame, text='📋 Booking Approvals', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Review and approve pending booking requests', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(header_content, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text='🔄 Refresh', command=self._load_pending_bookings, bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        
        self.view_toggle_btn = tk.Button(btn_frame, text='📅 Calendar View', command=self._toggle_view, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6)
        self.view_toggle_btn.pack(side='left', padx=(0, 8))
        
        tk.Button(btn_frame, text='✅ Bulk Approve', command=self._bulk_approve, bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        tk.Button(btn_frame, text='❌ Bulk Reject', command=self._bulk_reject, bg=self.colors.get('danger', '#E74C3C'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left')
        
        # Controls bar
        controls_frame = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        controls_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=(20, 0))
        
        controls_content = tk.Frame(controls_frame, bg='white')
        controls_content.pack(fill='x', padx=20, pady=12)
        
        # Queue info
        self.queue_label = tk.Label(controls_content, text='Loading...', bg='white', fg='#6B7280', font=('Helvetica', 11))
        self.queue_label.pack(side='left')
        
        # Sort and filters (for list view)
        self.list_controls = tk.Frame(controls_content, bg='white')
        self.list_controls.pack(side='right')
        
        tk.Label(self.list_controls, text='Sort by:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='right', padx=(0, 6))
        sort_dropdown = ttk.Combobox(self.list_controls, textvariable=self.sort_by, state='readonly', width=20, font=('Helvetica', 10))
        sort_dropdown['values'] = ('date', 'priority', 'resource', 'user')
        sort_dropdown.pack(side='right', padx=(0, 20))
        sort_dropdown.bind('<<ComboboxSelected>>', lambda e: self._sort_bookings())
        
        self.select_all_var = tk.BooleanVar()
        tk.Checkbutton(self.list_controls, text='Select All', variable=self.select_all_var, command=self._toggle_select_all, bg='white', font=('Helvetica', 10), selectcolor='white').pack(side='right', padx=(0, 20))
        
        # Content area
        self.content_area = tk.Frame(self, bg=self.colors.get('background', '#ECF0F1'))
        self.content_area.grid(row=2, column=0, sticky='nsew', padx=30, pady=(12, 20))

    def _load_pending_bookings(self):
        """Load pending bookings from API"""
        self._show_loading()
        
        def worker():
            try:
                self.pending_bookings = self.api.get('admin/bookings/pending') or []
                self.selected_bookings = []
                self.after(0, self._render_content)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load pending bookings: {str(e)}')
                    self.pending_bookings = []
                    self._render_content()
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _show_loading(self):
        """Show loading indicator"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.content_area, bg=self.colors.get('background', '#ECF0F1'))
        loading_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(loading_frame, text='Loading pending bookings...', bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 12)).pack()
        
        spinner = ttk.Progressbar(loading_frame, mode='indeterminate', length=300)
        spinner.pack(pady=10)
        spinner.start(10)

    def _sort_bookings(self):
        """Sort bookings based on selected criteria"""
        sort_by = self.sort_by.get()
        
        if sort_by == 'date':
            self.pending_bookings.sort(key=lambda b: self._parse_date(b.get('date', '')) or datetime.min.date())
        elif sort_by == 'priority':
            self.pending_bookings.sort(key=lambda b: (not (b.get('priority', 'normal') == 'urgent'), self._parse_date(b.get('date', '')) or datetime.min.date()))
        elif sort_by == 'resource':
            self.pending_bookings.sort(key=lambda b: b.get('resource_name', ''))
        elif sort_by == 'user':
            self.pending_bookings.sort(key=lambda b: b.get('user_name', ''))
        
        self._render_content()

    def _toggle_view(self):
        """Toggle between list and calendar view"""
        if self.view_mode == 'list':
            self.view_mode = 'calendar'
            self.view_toggle_btn.config(text='📋 List View')
            self.list_controls.pack_forget()
        else:
            self.view_mode = 'list'
            self.view_toggle_btn.config(text='📅 Calendar View')
            self.list_controls.pack(side='right')
        
        self._render_content()

    def _render_content(self):
        """Render content based on view mode"""
        if self.view_mode == 'list':
            self._render_list_view()
        else:
            self._render_calendar_view()

    def _render_list_view(self):
        """Render list view with booking cards"""
        # Clear content
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Update queue label
        count = len(self.pending_bookings)
        conflicts_count = sum(1 for b in self.pending_bookings if b.get('has_conflict', False))
        
        label_text = f'📋 {count} pending booking{"s" if count != 1 else ""}'
        if conflicts_count > 0:
            label_text += f' ⚠️ {conflicts_count} with conflict{"s" if conflicts_count != 1 else ""}'
        
        self.queue_label.config(text=label_text)
        
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
        
        if not self.pending_bookings:
            # Empty state
            empty_frame = tk.Frame(content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            empty_frame.pack(fill='both', expand=True, pady=20)
            
            tk.Label(empty_frame, text='✅', bg='white', font=('Helvetica', 48)).pack(pady=(40, 10))
            tk.Label(empty_frame, text='All caught up!', bg='white', fg='#374151', font=('Helvetica', 14, 'bold')).pack()
            tk.Label(empty_frame, text='No pending bookings to review', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(pady=(4, 40))
        else:
            # Booking cards
            for booking in self.pending_bookings:
                card = self._create_booking_card(booking)
                card.pack(fill='x', pady=(0, 12))

    def _create_booking_card(self, booking):
        """Create a booking approval card"""
        card = tk.Frame(self.content_area, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        
        # Track selection
        selected_var = tk.BooleanVar(value=booking.get('id') in self.selected_bookings)
        
        def on_checkbox_change():
            booking_id = booking.get('id')
            if selected_var.get():
                if booking_id not in self.selected_bookings:
                    self.selected_bookings.append(booking_id)
            else:
                if booking_id in self.selected_bookings:
                    self.selected_bookings.remove(booking_id)
        
        # Content
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=16)
        
        # Header row
        header_row = tk.Frame(content, bg='white')
        header_row.pack(fill='x', pady=(0, 12))
        
        # Checkbox
        checkbox = tk.Checkbutton(header_row, variable=selected_var, command=on_checkbox_change, bg='white', selectcolor='white')
        checkbox.pack(side='left', padx=(0, 12))
        
        # User and resource info
        info_frame = tk.Frame(header_row, bg='white')
        info_frame.pack(side='left', fill='x', expand=True)
        
        # Resource name
        resource_name = booking.get('resource_name', 'Unknown Resource')
        tk.Label(info_frame, text=resource_name, bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w')
        
        # User info
        user_name = booking.get('user_name', 'Unknown User')
        user_role = booking.get('user_role', 'User')
        tk.Label(info_frame, text=f"Requested by: {user_name} ({user_role})", bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(2, 0))
        
        # Badges
        badges_frame = tk.Frame(header_row, bg='white')
        badges_frame.pack(side='right')
        
        # Priority badge
        if booking.get('priority', 'normal') == 'urgent':
            priority_badge = tk.Frame(badges_frame, bg='#FEF3C7', highlightthickness=1, highlightbackground='#F59E0B')
            priority_badge.pack(side='left', padx=(0, 6))
            tk.Label(priority_badge, text='🔴 URGENT', bg='#FEF3C7', fg='#92400E', font=('Helvetica', 8, 'bold'), padx=6, pady=2).pack()
        
        # Conflict badge
        if booking.get('has_conflict', False):
            conflict_badge = tk.Frame(badges_frame, bg='#FEF2F2', highlightthickness=1, highlightbackground='#E74C3C')
            conflict_badge.pack(side='left')
            tk.Label(conflict_badge, text='⚠️ CONFLICT', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 8, 'bold'), padx=6, pady=2).pack()
        
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
        self._add_detail_item(details_content, '📝 Submitted:', self._format_date(booking.get('created_at', '')))
        
        # Purpose
        purpose = booking.get('purpose', 'No purpose provided')
        if len(purpose) > 150:
            purpose = purpose[:150] + '...'
        
        tk.Label(content, text='Purpose:', bg='white', fg='#6B7280', font=('Helvetica', 9, 'bold')).pack(anchor='w', pady=(0, 4))
        tk.Label(content, text=purpose, bg='white', fg='#374151', font=('Helvetica', 9), wraplength=900, justify='left').pack(anchor='w', pady=(0, 12))
        
        # Conflict warning
        if booking.get('has_conflict', False):
            conflict_frame = tk.Frame(content, bg='#FEF2F2', highlightthickness=1, highlightbackground='#E74C3C')
            conflict_frame.pack(fill='x', pady=(0, 12))
            
            conflict_content = tk.Frame(conflict_frame, bg='#FEF2F2')
            conflict_content.pack(padx=12, pady=8)
            
            tk.Label(conflict_content, text='⚠️ Time Conflict Detected', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9, 'bold')).pack(anchor='w')
            tk.Label(conflict_content, text='This time slot overlaps with an existing booking for this resource', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 8)).pack(anchor='w', pady=(2, 0))
        
        # Action buttons
        actions_frame = tk.Frame(content, bg='white')
        actions_frame.pack(fill='x')
        
        tk.Button(actions_frame, text='View Full Details', command=lambda: self._show_approval_modal(booking), bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        
        tk.Button(actions_frame, text='✅ Approve', command=lambda: self._approve_booking(booking), bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=16, pady=6).pack(side='left', padx=(0, 8))
        
        tk.Button(actions_frame, text='❌ Reject', command=lambda: self._reject_booking(booking), bg=self.colors.get('danger', '#E74C3C'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=16, pady=6).pack(side='left', padx=(0, 8))
        
        if booking.get('has_conflict', False):
            tk.Button(actions_frame, text='🔄 Suggest Alternative', command=lambda: self._suggest_alternative(booking), bg=self.colors.get('warning', '#F39C12'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left')
        
        return card

    def _add_detail_item(self, parent, label, value):
        """Add detail item"""
        frame = tk.Frame(parent, bg='#F9FAFB')
        frame.pack(side='left', padx=(0, 24))
        tk.Label(frame, text=label, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 9)).pack(side='left', padx=(0, 4))
        tk.Label(frame, text=value, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 9, 'bold')).pack(side='left')

    def _render_calendar_view(self):
        """Render calendar view with bookings"""
        # Clear content
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Update queue label
        count = len(self.pending_bookings)
        self.queue_label.config(text=f'📅 Calendar View - {count} pending booking{"s" if count != 1 else ""}')
        
        # Calendar header
        header = tk.Frame(self.content_area, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        header.pack(fill='x', pady=(10, 10))
        
        header_content = tk.Frame(header, bg='white')
        header_content.pack(padx=20, pady=12)
        
        # Month navigation
        tk.Button(header_content, text='◀', command=self._prev_month, bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 12, 'bold'), padx=12, pady=4).pack(side='left', padx=(0, 12))
        
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month_label = tk.Label(header_content, text=f"{month_names[self.current_month - 1]} {self.current_year}", bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold'))
        month_label.pack(side='left', padx=12)
        
        tk.Button(header_content, text='▶', command=self._next_month, bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 12, 'bold'), padx=12, pady=4).pack(side='left', padx=(12, 0))
        
        # Today button
        tk.Button(header_content, text='Today', command=self._goto_today, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=16, pady=4).pack(side='right', padx=(20, 0))
        
        # Legend
        legend_frame = tk.Frame(header_content, bg='white')
        legend_frame.pack(side='right', padx=(20, 20))
        
        self._add_legend_item(legend_frame, '#F59E0B', 'Pending')
        self._add_legend_item(legend_frame, '#E74C3C', 'Conflict')
        
        # Calendar grid
        cal_frame = tk.Frame(self.content_area, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        cal_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Scrollable calendar
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
            tk.Label(header_row, text=day_name, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 10, 'bold'), width=15, height=2).pack(side='left', padx=1)
        
        # Get calendar data
        first_day = datetime(self.current_year, self.current_month, 1)
        last_day_num = monthrange(self.current_year, self.current_month)[1]
        start_weekday = first_day.weekday()
        
        # Create calendar grid
        grid_frame = tk.Frame(parent, bg='white')
        grid_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        current_date = datetime.now().date()
        day_num = 1
        week_num = 0
        
        # Group bookings by date
        bookings_by_date = {}
        for booking in self.pending_bookings:
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
                    tk.Frame(week_row, bg='#F9FAFB', width=15, height=120).pack(side='left', padx=1)
                elif day_num > last_day_num:
                    tk.Frame(week_row, bg='#F9FAFB', width=15, height=120).pack(side='left', padx=1)
                else:
                    cell_date = datetime(self.current_year, self.current_month, day_num).date()
                    is_today = cell_date == current_date
                    
                    cell = tk.Frame(week_row, bg='#FFFFFF' if not is_today else '#E0E7FF', highlightthickness=1, highlightbackground='#DBEAFE' if is_today else '#E5E7EB', width=15, height=120)
                    cell.pack(side='left', padx=1, fill='both', expand=True)
                    cell.pack_propagate(False)
                    
                    # Day number
                    day_header = tk.Frame(cell, bg='#FFFFFF' if not is_today else '#E0E7FF')
                    day_header.pack(fill='x', padx=4, pady=(4, 2))
                    
                    tk.Label(day_header, text=str(day_num), bg='#FFFFFF' if not is_today else '#E0E7FF', fg=self.colors.get('secondary', '#3498DB') if is_today else '#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='ne')
                    
                    # Bookings for this day
                    if day_num in bookings_by_date:
                        bookings_container = tk.Frame(cell, bg='#FFFFFF' if not is_today else '#E0E7FF')
                        bookings_container.pack(fill='both', expand=True, padx=2, pady=(0, 2))
                        
                        for booking in bookings_by_date[day_num][:4]:  # Show max 4
                            has_conflict = booking.get('has_conflict', False)
                            color = '#E74C3C' if has_conflict else '#F59E0B'
                            
                            booking_item = tk.Frame(bookings_container, bg=color, cursor='hand2')
                            booking_item.pack(fill='x', pady=1)
                            
                            # Booking info
                            resource_name = booking.get('resource_name', 'Booking')[:20]
                            time_str = f"{booking.get('start_time', '')}".split(':')[0] if booking.get('start_time') else ''
                            
                            tk.Label(booking_item, text=f"{time_str}h {resource_name}", bg=color, fg='white', font=('Helvetica', 7), anchor='w', padx=4, pady=2).pack(fill='x')
                            
                            booking_item.bind('<Button-1>', lambda e, b=booking: self._show_approval_modal(b))
                        
                        if len(bookings_by_date[day_num]) > 4:
                            more_label = tk.Label(bookings_container, text=f'+{len(bookings_by_date[day_num]) - 4}', bg='#FFFFFF' if not is_today else '#E0E7FF', fg='#6B7280', font=('Helvetica', 7, 'bold'))
                            more_label.pack(anchor='center', pady=1)
                    
                    day_num += 1
            
            week_num += 1

    def _add_legend_item(self, parent, color, text):
        """Add legend item"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(side='left', padx=(0, 12))
        
        color_box = tk.Frame(frame, bg=color, width=16, height=16)
        color_box.pack(side='left', padx=(0, 4))
        color_box.pack_propagate(False)
        
        tk.Label(frame, text=text, bg='white', fg='#374151', font=('Helvetica', 9)).pack(side='left')

    def _prev_month(self):
        """Navigate to previous month"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._render_calendar_view()

    def _next_month(self):
        """Navigate to next month"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._render_calendar_view()

    def _goto_today(self):
        """Go to current month"""
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self._render_calendar_view()

    def _show_approval_modal(self, booking):
        """Show detailed approval modal"""
        modal = tk.Toplevel(self)
        modal.title(f"Approve Booking - {booking.get('resource_name', 'Resource')}")
        modal.geometry('800x900')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 400
        y = (modal.winfo_screenheight() // 2) - 450
        modal.geometry(f'800x900+{x}+{y}')
        
        # Header
        has_conflict = booking.get('has_conflict', False)
        header_color = self.colors.get('danger', '#E74C3C') if has_conflict else self.colors.get('secondary', '#3498DB')
        
        header = tk.Frame(modal, bg=header_color)
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=header_color)
        header_content.pack(padx=20, pady=20)
        
        icon = '⚠️' if has_conflict else '📋'
        tk.Label(header_content, text=icon, bg=header_color, font=('Helvetica', 36)).pack()
        tk.Label(header_content, text='Booking Approval Review', bg=header_color, fg='white', font=('Helvetica', 16, 'bold')).pack(pady=(8, 0))
        
        if has_conflict:
            tk.Label(header_content, text='⚠️ Time Conflict Detected', bg=header_color, fg='white', font=('Helvetica', 11, 'bold')).pack(pady=(4, 0))
        
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
        
        # Booking information
        self._add_section_header(details_frame, 'Booking Information')
        
        booking_info = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        booking_info.pack(fill='x', pady=(0, 16))
        
        info_content = tk.Frame(booking_info, bg='#F9FAFB')
        info_content.pack(padx=16, pady=12)
        
        self._add_modal_detail(info_content, 'Resource:', booking.get('resource_name', 'N/A'))
        self._add_modal_detail(info_content, 'Resource Type:', booking.get('resource_type', 'N/A'))
        self._add_modal_detail(info_content, 'Date:', self._format_date(booking.get('date', '')))
        self._add_modal_detail(info_content, 'Start Time:', booking.get('start_time', 'N/A'))
        self._add_modal_detail(info_content, 'End Time:', booking.get('end_time', 'N/A'))
        self._add_modal_detail(info_content, 'Expected Attendees:', str(booking.get('attendees', 'N/A')))
        self._add_modal_detail(info_content, 'Priority:', (booking.get('priority', 'normal') or 'normal').title())
        
        # Purpose
        tk.Label(details_frame, text='Purpose:', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        tk.Label(details_frame, text=booking.get('purpose', 'No purpose'), bg='white', fg='#6B7280', font=('Helvetica', 10), wraplength=720, justify='left').pack(anchor='w', pady=(0, 16))
        
        # Requirements
        requirements = booking.get('additional_requirements', '').strip()
        if requirements:
            tk.Label(details_frame, text='Additional Requirements:', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 8))
            tk.Label(details_frame, text=requirements, bg='white', fg='#6B7280', font=('Helvetica', 10), wraplength=720, justify='left').pack(anchor='w', pady=(0, 16))
        
        # User information
        self._add_section_header(details_frame, 'User Information')
        
        user_info = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        user_info.pack(fill='x', pady=(0, 16))
        
        user_content = tk.Frame(user_info, bg='#F9FAFB')
        user_content.pack(padx=16, pady=12)
        
        self._add_modal_detail(user_content, 'Name:', booking.get('user_name', 'N/A'))
        self._add_modal_detail(user_content, 'Email:', booking.get('user_email', 'N/A'))
        self._add_modal_detail(user_content, 'Role:', booking.get('user_role', 'N/A'))
        
        # User booking history
        tk.Label(details_frame, text="User's Booking History:", bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w', pady=(0, 8))
        
        history_frame = tk.Frame(details_frame, bg='#EFF6FF', highlightthickness=1, highlightbackground='#BFDBFE')
        history_frame.pack(fill='x', pady=(0, 16))
        
        history_content = tk.Frame(history_frame, bg='#EFF6FF')
        history_content.pack(padx=16, pady=12)
        
        tk.Label(history_content, text='📊 Total Bookings: 8 (7 approved, 1 cancelled)', bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 9)).pack(anchor='w')
        tk.Label(history_content, text='✅ Compliance Rate: 87%', bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 9)).pack(anchor='w', pady=(2, 0))
        tk.Label(history_content, text='⭐ User Rating: Good Standing', bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 9)).pack(anchor='w', pady=(2, 0))
        
        # Conflict check
        self._add_section_header(details_frame, 'Conflict Analysis')
        
        if has_conflict:
            conflict_frame = tk.Frame(details_frame, bg='#FEF2F2', highlightthickness=1, highlightbackground='#E74C3C')
            conflict_frame.pack(fill='x', pady=(0, 16))
            
            conflict_content = tk.Frame(conflict_frame, bg='#FEF2F2')
            conflict_content.pack(padx=16, pady=12)
            
            tk.Label(conflict_content, text='⚠️ Time Conflict Detected', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 11, 'bold')).pack(anchor='w')
            tk.Label(conflict_content, text='This booking overlaps with an existing confirmed booking:', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9)).pack(anchor='w', pady=(4, 8))
            tk.Label(conflict_content, text='• Existing booking: 10:00 AM - 12:00 PM', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9)).pack(anchor='w')
            tk.Label(conflict_content, text='• Requested slot: 11:00 AM - 1:00 PM', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9)).pack(anchor='w')
            tk.Label(conflict_content, text='• Overlap: 1 hour', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 8))
            
            tk.Button(conflict_content, text='🔄 Suggest Alternative Time Slots', command=lambda: self._suggest_alternative(booking), bg='#F59E0B', fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(anchor='w')
        else:
            no_conflict_frame = tk.Frame(details_frame, bg='#F0FDF4', highlightthickness=1, highlightbackground='#27AE60')
            no_conflict_frame.pack(fill='x', pady=(0, 16))
            
            no_conflict_content = tk.Frame(no_conflict_frame, bg='#F0FDF4')
            no_conflict_content.pack(padx=16, pady=12)
            
            tk.Label(no_conflict_content, text='✅ No Conflicts Detected', bg='#F0FDF4', fg='#166534', font=('Helvetica', 10, 'bold')).pack(anchor='w')
            tk.Label(no_conflict_content, text='Resource is available for the requested time slot', bg='#F0FDF4', fg='#166534', font=('Helvetica', 9)).pack(anchor='w', pady=(4, 0))
        
        # Comments
        self._add_section_header(details_frame, 'Admin Comments')
        
        tk.Label(details_frame, text='Add comments or notes (optional):', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 6))
        
        comments_text = tk.Text(details_frame, height=4, font=('Helvetica', 10), wrap='word')
        comments_text.pack(fill='x', pady=(0, 16))
        
        # Decision buttons
        self._add_section_header(details_frame, 'Make Decision')
        
        decision_frame = tk.Frame(details_frame, bg='white')
        decision_frame.pack(fill='x', pady=(0, 16))
        
        tk.Button(decision_frame, text='✅ Approve Booking', command=lambda: [modal.destroy(), self._approve_booking(booking, comments_text.get('1.0', 'end-1c'))], bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=30, pady=12, width=20).pack(side='left', padx=(0, 8))
        
        tk.Button(decision_frame, text='❌ Reject Booking', command=lambda: [modal.destroy(), self._reject_booking(booking, comments_text.get('1.0', 'end-1c'))], bg=self.colors.get('danger', '#E74C3C'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=30, pady=12, width=20).pack(side='left')
        
        # Close button
        tk.Button(details_frame, text='Close Without Decision', command=modal.destroy, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 11, 'bold'), padx=30, pady=12).pack(fill='x', pady=(16, 0))

    def _add_section_header(self, parent, text):
        """Add section header"""
        tk.Label(parent, text=text, bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 8))
        tk.Frame(parent, bg='#E5E7EB', height=1).pack(fill='x', pady=(0, 12))

    def _add_modal_detail(self, parent, label, value):
        """Add modal detail row"""
        row = tk.Frame(parent, bg='#F9FAFB')
        row.pack(fill='x', pady=4)
        tk.Label(row, text=label, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 10), width=20, anchor='w').pack(side='left')
        tk.Label(row, text=str(value), bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(side='left')

    def _approve_booking(self, booking, comments=''):
        """Approve a booking"""
        resource_name = booking.get('resource_name', 'this resource')
        
        result = messagebox.askyesno('Approve Booking',
                                     f"Approve booking for '{resource_name}'?\n\n"
                                     f"✅ Booking will be confirmed\n"
                                     f"📧 User will receive confirmation\n"
                                     f"📅 Resource will be reserved")
        
        if result:
            def worker():
                try:
                    booking_id = booking.get('id')
                    data = {'comments': comments} if comments else {}
                    self.api.put(f'admin/bookings/{booking_id}/approve', data)
                    
                    # Send booking confirmation email
                    try:
                        user_email = booking.get('user_email')
                        user_name = booking.get('user_name', 'Student')
                        if user_email:
                            email_service = get_email_service()
                            email_service.send_booking_confirmation(
                                user_email=user_email,
                                booking_details=booking,
                                status="approved",
                                user_name=user_name
                            )
                            print("[EMAIL] Booking approval notification sent")
                    except Exception as email_error:
                        print(f"[EMAIL ERROR] Failed to send booking confirmation: {email_error}")
                    
                    def show_success():
                        messagebox.showinfo('Success',
                                          f"Booking approved successfully!\n\n"
                                          f"✅ Resource confirmed\n"
                                          f"📧 Notification sent to user")
                        self._load_pending_bookings()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to approve booking: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _reject_booking(self, booking, comments=''):
        """Reject a booking"""
        resource_name = booking.get('resource_name', 'this resource')
        
        # Get rejection reason
        reason = simpledialog.askstring('Reject Booking',
                                       f"Provide a reason for rejecting this booking:\n(Required)",
                                       parent=self)
        
        if not reason:
            return
        
        result = messagebox.askyesno('Confirm Rejection',
                                     f"Reject booking for '{resource_name}'?\n\n"
                                     f"❌ Booking will be rejected\n"
                                     f"📧 User will be notified\n\n"
                                     f"Reason: {reason}")
        
        if result:
            def worker():
                try:
                    booking_id = booking.get('id')
                    data = {'reason': reason, 'comments': comments}
                    self.api.put(f'admin/bookings/{booking_id}/reject', data)
                    
                    # Send booking rejection email
                    try:
                        user_email = booking.get('user_email')
                        user_name = booking.get('user_name', 'Student')
                        if user_email:
                            email_service = get_email_service()
                            email_service.send_approval_notification(
                                user_email=user_email,
                                item_type="booking",
                                item_name=resource_name,
                                status="rejected",
                                reason=reason,
                                user_name=user_name
                            )
                            print("[EMAIL] Booking rejection notification sent")
                    except Exception as email_error:
                        print(f"[EMAIL ERROR] Failed to send rejection notification: {email_error}")
                    
                    def show_success():
                        messagebox.showinfo('Booking Rejected',
                                          f"Booking rejected.\n\n"
                                          f"❌ User has been notified\n"
                                          f"📧 Rejection reason sent")
                        self._load_pending_bookings()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to reject booking: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _suggest_alternative(self, booking):
        """Suggest alternative time slots"""
        messagebox.showinfo('Suggest Alternative',
                          f"Alternative time slots for {booking.get('resource_name', 'resource')}:\n\n"
                          f"Available slots on {self._format_date(booking.get('date', ''))}:\n"
                          f"• 8:00 AM - 10:00 AM\n"
                          f"• 2:00 PM - 4:00 PM\n"
                          f"• 4:00 PM - 6:00 PM\n\n"
                          f"Feature: Send these suggestions to the user via email.")

    def _toggle_select_all(self):
        """Toggle selection of all bookings"""
        if self.select_all_var.get():
            self.selected_bookings = [b.get('id') for b in self.pending_bookings]
        else:
            self.selected_bookings = []
        
        self._render_content()

    def _bulk_approve(self):
        """Approve multiple bookings"""
        if not self.selected_bookings:
            messagebox.showwarning('No Selection', 'Please select bookings to approve.')
            return
        
        count = len(self.selected_bookings)
        result = messagebox.askyesno('Bulk Approve',
                                     f"Approve {count} selected booking{'s' if count > 1 else ''}?\n\n"
                                     f"✅ All bookings will be confirmed\n"
                                     f"📧 Users will receive confirmations")
        
        if result:
            def worker():
                try:
                    success_count = 0
                    for booking_id in self.selected_bookings:
                        try:
                            self.api.put(f'admin/bookings/{booking_id}/approve', {})
                            success_count += 1
                        except:
                            pass
                    
                    def show_success():
                        messagebox.showinfo('Bulk Approval Complete',
                                          f"✅ {success_count} of {count} bookings approved!")
                        self._load_pending_bookings()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Bulk approval failed: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _bulk_reject(self):
        """Reject multiple bookings"""
        if not self.selected_bookings:
            messagebox.showwarning('No Selection', 'Please select bookings to reject.')
            return
        
        count = len(self.selected_bookings)
        reason = simpledialog.askstring('Bulk Reject',
                                       f'Provide a reason for rejecting {count} booking{"s" if count > 1 else ""}:',
                                       parent=self)
        
        if not reason:
            return
        
        result = messagebox.askyesno('Confirm Bulk Reject',
                                     f"Reject {count} selected booking{'s' if count > 1 else ''}?\n\n"
                                     f"❌ All bookings will be rejected\n"
                                     f"📧 Users will be notified\n\n"
                                     f"Reason: {reason}")
        
        if result:
            def worker():
                try:
                    success_count = 0
                    for booking_id in self.selected_bookings:
                        try:
                            self.api.put(f'admin/bookings/{booking_id}/reject', {'reason': reason})
                            success_count += 1
                        except:
                            pass
                    
                    def show_success():
                        messagebox.showinfo('Bulk Rejection Complete',
                                          f"❌ {success_count} of {count} bookings rejected.")
                        self._load_pending_bookings()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Bulk rejection failed: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

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
                    return datetime.strptime(date_str[:10] if len(date_str) >= 10 else date_str, '%Y-%m-%d').date()
                except:
                    continue
        except:
            pass
        return None
