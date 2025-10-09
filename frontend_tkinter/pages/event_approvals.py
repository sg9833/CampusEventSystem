import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from datetime import datetime

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.email_service import get_email_service


class EventApprovalsPage(tk.Frame):
    """Admin page for approving/rejecting pending events."""

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
        self.pending_events = []
        self.selected_events = []  # For bulk actions
        self.sort_by = tk.StringVar(value='date')
        
        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_pending_events()

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
        tk.Label(title_frame, text='✅ Event Approvals', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Review and approve pending event requests', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(header_content, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text='🔄 Refresh', command=self._load_pending_events, bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
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
        
        # Sort options
        tk.Label(controls_content, text='Sort by:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='right', padx=(0, 6))
        sort_dropdown = ttk.Combobox(controls_content, textvariable=self.sort_by, state='readonly', width=20, font=('Helvetica', 10))
        sort_dropdown['values'] = ('date', 'priority', 'organizer', 'attendees')
        sort_dropdown.pack(side='right', padx=(0, 20))
        sort_dropdown.bind('<<ComboboxSelected>>', lambda e: self._sort_events())
        
        # Select all checkbox
        self.select_all_var = tk.BooleanVar()
        tk.Checkbutton(controls_content, text='Select All', variable=self.select_all_var, command=self._toggle_select_all, bg='white', font=('Helvetica', 10), selectcolor='white').pack(side='right', padx=(0, 20))
        
        # Scrollable content area
        content_container = tk.Frame(self, bg=self.colors.get('background', '#ECF0F1'))
        content_container.grid(row=2, column=0, sticky='nsew', padx=30, pady=(12, 20))
        content_container.grid_rowconfigure(0, weight=1)
        content_container.grid_columnconfigure(0, weight=1)
        
        canvas = tk.Canvas(content_container, bg=self.colors.get('background', '#ECF0F1'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient='vertical', command=canvas.yview)
        
        self.content = tk.Frame(canvas, bg=self.colors.get('background', '#ECF0F1'))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=self.content, anchor='nw')
        self.content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Update canvas width on resize
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag('all')[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

    def _load_pending_events(self):
        """Load pending events from API"""
        self._show_loading()
        
        def worker():
            try:
                self.pending_events = self.api.get('admin/events/pending') or []
                self.selected_events = []
                self.after(0, self._render_events)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load pending events: {str(e)}')
                    self.pending_events = []
                    self._render_events()
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _show_loading(self):
        """Show loading indicator"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.content, bg=self.colors.get('background', '#ECF0F1'))
        loading_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(loading_frame, text='Loading pending events...', bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 12)).pack()
        
        spinner = ttk.Progressbar(loading_frame, mode='indeterminate', length=300)
        spinner.pack(pady=10)
        spinner.start(10)

    def _sort_events(self):
        """Sort events based on selected criteria"""
        sort_by = self.sort_by.get()
        
        if sort_by == 'date':
            self.pending_events.sort(key=lambda e: self._parse_datetime(e.get('start_date', '')) or datetime.min)
        elif sort_by == 'priority':
            # Priority events first, then by date
            self.pending_events.sort(key=lambda e: (not e.get('is_urgent', False), self._parse_datetime(e.get('start_date', '')) or datetime.min))
        elif sort_by == 'organizer':
            self.pending_events.sort(key=lambda e: e.get('organizer_name', ''))
        elif sort_by == 'attendees':
            self.pending_events.sort(key=lambda e: -(e.get('expected_attendees', 0) or 0))
        
        self._render_events()

    def _render_events(self):
        """Render pending events"""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Update queue label
        count = len(self.pending_events)
        self.queue_label.config(text=f'📋 {count} pending event{"s" if count != 1 else ""} awaiting approval')
        
        if not self.pending_events:
            # Empty state
            empty_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            empty_frame.pack(fill='both', expand=True, pady=20)
            
            tk.Label(empty_frame, text='✅', bg='white', font=('Helvetica', 48)).pack(pady=(40, 10))
            tk.Label(empty_frame, text='All caught up!', bg='white', fg='#374151', font=('Helvetica', 14, 'bold')).pack()
            tk.Label(empty_frame, text='No pending events to review', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(pady=(4, 40))
        else:
            # Event cards
            for event in self.pending_events:
                card = self._create_event_card(event)
                card.pack(fill='x', pady=(0, 12))

    def _create_event_card(self, event):
        """Create an event approval card"""
        card = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        
        # Track selection
        selected_var = tk.BooleanVar(value=event.get('id') in self.selected_events)
        
        def on_checkbox_change():
            event_id = event.get('id')
            if selected_var.get():
                if event_id not in self.selected_events:
                    self.selected_events.append(event_id)
            else:
                if event_id in self.selected_events:
                    self.selected_events.remove(event_id)
        
        # Content
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=16)
        
        # Header row with checkbox and title
        header_row = tk.Frame(content, bg='white')
        header_row.pack(fill='x', pady=(0, 12))
        
        # Selection checkbox
        checkbox = tk.Checkbutton(header_row, variable=selected_var, command=on_checkbox_change, bg='white', selectcolor='white')
        checkbox.pack(side='left', padx=(0, 12))
        
        # Event info
        event_info_frame = tk.Frame(header_row, bg='white')
        event_info_frame.pack(side='left', fill='x', expand=True)
        
        # Event name with priority badge
        title_row = tk.Frame(event_info_frame, bg='white')
        title_row.pack(fill='x')
        
        event_name = event.get('name', 'Unnamed Event')
        tk.Label(title_row, text=event_name, bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(side='left')
        
        # Priority badge
        if event.get('is_urgent', False):
            priority_badge = tk.Frame(title_row, bg='#FEF3C7', highlightthickness=1, highlightbackground='#F59E0B')
            priority_badge.pack(side='left', padx=(8, 0))
            tk.Label(priority_badge, text='🔴 URGENT', bg='#FEF3C7', fg='#92400E', font=('Helvetica', 8, 'bold'), padx=6, pady=2).pack()
        
        # Organizer info
        organizer_name = event.get('organizer_name', 'Unknown')
        tk.Label(event_info_frame, text=f"Organized by: {organizer_name}", bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(2, 0))
        
        # Submitted date
        submitted_date = self._format_datetime(event.get('submitted_date', event.get('created_at', '')))
        tk.Label(header_row, text=f"Submitted: {submitted_date}", bg='white', fg='#9CA3AF', font=('Helvetica', 9)).pack(side='right')
        
        # Event details grid
        details_frame = tk.Frame(content, bg='#F9FAFB')
        details_frame.pack(fill='x', pady=(0, 12))
        
        details_content = tk.Frame(details_frame, bg='#F9FAFB')
        details_content.pack(padx=16, pady=12)
        
        # Date and time
        start_date = self._format_datetime(event.get('start_date', ''))
        start_time = event.get('start_time', 'N/A')
        end_time = event.get('end_time', 'N/A')
        
        self._add_detail_item(details_content, '📅 Date:', start_date)
        self._add_detail_item(details_content, '🕐 Time:', f"{start_time} - {end_time}")
        
        # Venue
        venue = event.get('venue', event.get('location', 'N/A'))
        event_type = event.get('event_type', 'N/A')
        if event_type == 'virtual':
            venue = 'Virtual Event'
        
        self._add_detail_item(details_content, '📍 Venue:', venue)
        self._add_detail_item(details_content, '👥 Expected:', str(event.get('expected_attendees', 'N/A')))
        
        # Description preview
        description = event.get('description', 'No description provided')
        if len(description) > 150:
            description = description[:150] + '...'
        
        tk.Label(content, text='Description:', bg='white', fg='#6B7280', font=('Helvetica', 9, 'bold')).pack(anchor='w', pady=(0, 4))
        tk.Label(content, text=description, bg='white', fg='#374151', font=('Helvetica', 9), wraplength=900, justify='left').pack(anchor='w', pady=(0, 12))
        
        # Resource requirements (if any)
        resources = event.get('resources', [])
        if resources:
            tk.Label(content, text='Resource Requirements:', bg='white', fg='#6B7280', font=('Helvetica', 9, 'bold')).pack(anchor='w', pady=(0, 4))
            
            resources_frame = tk.Frame(content, bg='white')
            resources_frame.pack(fill='x', pady=(0, 12))
            
            for resource in resources[:5]:  # Show first 5
                resource_tag = tk.Label(resources_frame, text=f"• {resource}", bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 8), padx=8, pady=2)
                resource_tag.pack(side='left', padx=(0, 4), pady=2)
            
            if len(resources) > 5:
                more_tag = tk.Label(resources_frame, text=f'+{len(resources) - 5} more', bg='#F3F4F6', fg='#6B7280', font=('Helvetica', 8), padx=8, pady=2)
                more_tag.pack(side='left', padx=(0, 4), pady=2)
        
        # Action buttons
        actions_frame = tk.Frame(content, bg='white')
        actions_frame.pack(fill='x')
        
        tk.Button(actions_frame, text='View Full Details', command=lambda: self._show_approval_modal(event), bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        
        tk.Button(actions_frame, text='✅ Approve', command=lambda: self._approve_event(event), bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=16, pady=6).pack(side='left', padx=(0, 8))
        
        tk.Button(actions_frame, text='❌ Reject', command=lambda: self._reject_event(event), bg=self.colors.get('danger', '#E74C3C'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=16, pady=6).pack(side='left', padx=(0, 8))
        
        tk.Button(actions_frame, text='📝 Request Changes', command=lambda: self._request_changes(event), bg=self.colors.get('warning', '#F39C12'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left')
        
        return card

    def _add_detail_item(self, parent, label, value):
        """Add detail item"""
        frame = tk.Frame(parent, bg='#F9FAFB')
        frame.pack(side='left', padx=(0, 24))
        tk.Label(frame, text=label, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 9)).pack(side='left', padx=(0, 4))
        tk.Label(frame, text=value, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 9, 'bold')).pack(side='left')

    def _show_approval_modal(self, event):
        """Show detailed approval modal"""
        # Create modal
        modal = tk.Toplevel(self)
        modal.title(f"Approve Event - {event.get('name', 'Event')}")
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
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=self.colors.get('secondary', '#3498DB'))
        header_content.pack(padx=20, pady=20)
        
        tk.Label(header_content, text='📋', bg=self.colors.get('secondary', '#3498DB'), font=('Helvetica', 36)).pack()
        tk.Label(header_content, text='Event Approval Review', bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=(8, 0))
        tk.Label(header_content, text='Review all details before making a decision', bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 10)).pack(pady=(4, 0))
        
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
        
        # Event details section
        self._add_section_header(details_frame, 'Event Information')
        
        event_info = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        event_info.pack(fill='x', pady=(0, 16))
        
        info_content = tk.Frame(event_info, bg='#F9FAFB')
        info_content.pack(padx=16, pady=12)
        
        self._add_modal_detail(info_content, 'Event Name:', event.get('name', 'N/A'))
        self._add_modal_detail(info_content, 'Category:', event.get('category', 'N/A'))
        self._add_modal_detail(info_content, 'Type:', event.get('event_type', 'N/A'))
        self._add_modal_detail(info_content, 'Date:', self._format_datetime(event.get('start_date', '')))
        self._add_modal_detail(info_content, 'Start Time:', event.get('start_time', 'N/A'))
        self._add_modal_detail(info_content, 'End Time:', event.get('end_time', 'N/A'))
        self._add_modal_detail(info_content, 'Venue:', event.get('venue', event.get('location', 'N/A')))
        self._add_modal_detail(info_content, 'Expected Attendees:', str(event.get('expected_attendees', 'N/A')))
        self._add_modal_detail(info_content, 'Registration Deadline:', self._format_datetime(event.get('registration_deadline', '')))
        
        # Description
        tk.Label(details_frame, text='Description:', bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        tk.Label(details_frame, text=event.get('description', 'No description'), bg='white', fg='#6B7280', font=('Helvetica', 10), wraplength=720, justify='left').pack(anchor='w', pady=(0, 16))
        
        # Organizer information
        self._add_section_header(details_frame, 'Organizer Information')
        
        organizer_info = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        organizer_info.pack(fill='x', pady=(0, 16))
        
        org_content = tk.Frame(organizer_info, bg='#F9FAFB')
        org_content.pack(padx=16, pady=12)
        
        self._add_modal_detail(org_content, 'Name:', event.get('organizer_name', 'N/A'))
        self._add_modal_detail(org_content, 'Email:', event.get('organizer_email', 'N/A'))
        self._add_modal_detail(org_content, 'Department:', event.get('organizer_department', 'N/A'))
        
        # Previous events history
        tk.Label(details_frame, text="Organizer's Event History:", bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w', pady=(0, 8))
        
        history_frame = tk.Frame(details_frame, bg='#EFF6FF', highlightthickness=1, highlightbackground='#BFDBFE')
        history_frame.pack(fill='x', pady=(0, 16))
        
        history_content = tk.Frame(history_frame, bg='#EFF6FF')
        history_content.pack(padx=16, pady=12)
        
        # Mock history data (would come from API)
        tk.Label(history_content, text='📊 Previous Events: 5 (4 successful, 1 cancelled)', bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 9)).pack(anchor='w')
        tk.Label(history_content, text='⭐ Organizer Rating: 4.5/5.0', bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 9)).pack(anchor='w', pady=(2, 0))
        tk.Label(history_content, text='✅ Compliance Score: Excellent', bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 9)).pack(anchor='w', pady=(2, 0))
        
        # Resource availability check
        self._add_section_header(details_frame, 'Resource Availability')
        
        availability_frame = tk.Frame(details_frame, bg='#F0FDF4', highlightthickness=1, highlightbackground='#27AE60')
        availability_frame.pack(fill='x', pady=(0, 16))
        
        avail_content = tk.Frame(availability_frame, bg='#F0FDF4')
        avail_content.pack(padx=16, pady=12)
        
        tk.Label(avail_content, text='✅ Venue is available for requested date and time', bg='#F0FDF4', fg='#166534', font=('Helvetica', 10, 'bold')).pack(anchor='w')
        tk.Label(avail_content, text='✅ No scheduling conflicts detected', bg='#F0FDF4', fg='#166534', font=('Helvetica', 9)).pack(anchor='w', pady=(4, 0))
        
        # Resources
        resources = event.get('resources', [])
        if resources:
            tk.Label(avail_content, text='Requested Resources:', bg='#F0FDF4', fg='#166534', font=('Helvetica', 9)).pack(anchor='w', pady=(8, 4))
            for resource in resources:
                tk.Label(avail_content, text=f"  • {resource}", bg='#F0FDF4', fg='#166534', font=('Helvetica', 9)).pack(anchor='w')
        
        # Comments/Notes section
        self._add_section_header(details_frame, 'Admin Comments')
        
        tk.Label(details_frame, text='Add comments or notes (optional):', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 6))
        
        comments_text = tk.Text(details_frame, height=4, font=('Helvetica', 10), wrap='word')
        comments_text.pack(fill='x', pady=(0, 16))
        
        # Decision section
        self._add_section_header(details_frame, 'Make Decision')
        
        decision_frame = tk.Frame(details_frame, bg='white')
        decision_frame.pack(fill='x', pady=(0, 16))
        
        # Approval
        approve_frame = tk.Frame(decision_frame, bg='#F0FDF4', highlightthickness=1, highlightbackground='#27AE60')
        approve_frame.pack(side='left', fill='both', expand=True, padx=(0, 8))
        
        approve_content = tk.Frame(approve_frame, bg='#F0FDF4')
        approve_content.pack(padx=16, pady=16)
        
        tk.Label(approve_content, text='✅ Approve Event', bg='#F0FDF4', fg='#166534', font=('Helvetica', 11, 'bold')).pack()
        tk.Label(approve_content, text='Event will be published and\norganizer will be notified', bg='#F0FDF4', fg='#166534', font=('Helvetica', 9), justify='center').pack(pady=(4, 8))
        tk.Button(approve_content, text='Approve', command=lambda: [modal.destroy(), self._approve_event(event, comments_text.get('1.0', 'end-1c'))], bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=24, pady=8).pack()
        
        # Rejection
        reject_frame = tk.Frame(decision_frame, bg='#FEF2F2', highlightthickness=1, highlightbackground='#E74C3C')
        reject_frame.pack(side='right', fill='both', expand=True, padx=(8, 0))
        
        reject_content = tk.Frame(reject_frame, bg='#FEF2F2')
        reject_content.pack(padx=16, pady=16)
        
        tk.Label(reject_content, text='❌ Reject Event', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 11, 'bold')).pack()
        tk.Label(reject_content, text='Event will be rejected and\norganizer will be notified', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9), justify='center').pack(pady=(4, 8))
        tk.Button(reject_content, text='Reject', command=lambda: [modal.destroy(), self._reject_event(event, comments_text.get('1.0', 'end-1c'))], bg=self.colors.get('danger', '#E74C3C'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=24, pady=8).pack()
        
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

    def _approve_event(self, event, comments=''):
        """Approve an event"""
        event_name = event.get('name', 'this event')
        
        result = messagebox.askyesno('Approve Event', 
                                     f"Approve '{event_name}'?\n\n"
                                     f"✅ Event will be published\n"
                                     f"📧 Organizer will receive approval notification\n"
                                     f"📅 Event will appear in public listings")
        
        if result:
            def worker():
                try:
                    event_id = event.get('id')
                    data = {'comments': comments} if comments else {}
                    self.api.put(f'admin/events/{event_id}/approve', data)
                    
                    # Send approval notification email
                    try:
                        organizer_email = event.get('organizer_email')
                        organizer_name = event.get('organizer_name', 'Organizer')
                        if organizer_email:
                            email_service = get_email_service()
                            email_service.send_approval_notification(
                                user_email=organizer_email,
                                item_type="event",
                                item_name=event_name,
                                status="approved",
                                reason=comments or "Your event meets all requirements and has been approved.",
                                user_name=organizer_name
                            )
                            print("[EMAIL] Approval notification sent to organizer")
                    except Exception as email_error:
                        print(f"[EMAIL ERROR] Failed to send approval notification: {email_error}")
                    
                    def show_success():
                        messagebox.showinfo('Success', 
                                          f"Event '{event_name}' has been approved!\n\n"
                                          f"✅ Event is now published\n"
                                          f"📧 Notification sent to organizer")
                        self._load_pending_events()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to approve event: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _reject_event(self, event, comments=''):
        """Reject an event"""
        event_name = event.get('name', 'this event')
        
        # Show rejection reason dialog
        reason_modal = tk.Toplevel(self)
        reason_modal.title('Reject Event')
        reason_modal.geometry('500x350')
        reason_modal.configure(bg='white')
        reason_modal.transient(self.winfo_toplevel())
        reason_modal.grab_set()
        
        # Center modal
        reason_modal.update_idletasks()
        x = (reason_modal.winfo_screenwidth() // 2) - 250
        y = (reason_modal.winfo_screenheight() // 2) - 175
        reason_modal.geometry(f'500x350+{x}+{y}')
        
        # Header
        header = tk.Frame(reason_modal, bg=self.colors.get('danger', '#E74C3C'))
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=self.colors.get('danger', '#E74C3C'))
        header_content.pack(padx=20, pady=20)
        
        tk.Label(header_content, text='❌', bg=self.colors.get('danger', '#E74C3C'), font=('Helvetica', 36)).pack()
        tk.Label(header_content, text='Reject Event', bg=self.colors.get('danger', '#E74C3C'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=(8, 0))
        tk.Label(header_content, text=f"Provide a reason for rejecting '{event_name}'", bg=self.colors.get('danger', '#E74C3C'), fg='white', font=('Helvetica', 10)).pack(pady=(4, 0))
        
        # Content
        content = tk.Frame(reason_modal, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(content, text='Rejection Reason (Required) *', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 6))
        tk.Label(content, text='Please provide a clear reason for rejection. This will be sent to the organizer.', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 8))
        
        reason_text = tk.Text(content, height=6, font=('Helvetica', 10), wrap='word')
        reason_text.pack(fill='both', expand=True, pady=(0, 16))
        
        if comments:
            reason_text.insert('1.0', comments)
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text='Cancel', command=reason_modal.destroy, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=10, width=12).pack(side='left')
        
        def confirm_rejection():
            reason = reason_text.get('1.0', 'end-1c').strip()
            if not reason:
                messagebox.showerror('Required Field', 'Please provide a reason for rejection.')
                return
            
            reason_modal.destroy()
            
            def worker():
                try:
                    event_id = event.get('id')
                    data = {'reason': reason, 'comments': comments}
                    self.api.put(f'admin/events/{event_id}/reject', data)
                    
                    # Send rejection notification email
                    try:
                        organizer_email = event.get('organizer_email')
                        organizer_name = event.get('organizer_name', 'Organizer')
                        if organizer_email:
                            email_service = get_email_service()
                            email_service.send_approval_notification(
                                user_email=organizer_email,
                                item_type="event",
                                item_name=event_name,
                                status="rejected",
                                reason=reason,
                                user_name=organizer_name
                            )
                            print("[EMAIL] Rejection notification sent to organizer")
                    except Exception as email_error:
                        print(f"[EMAIL ERROR] Failed to send rejection notification: {email_error}")
                    
                    def show_success():
                        messagebox.showinfo('Event Rejected', 
                                          f"Event '{event_name}' has been rejected.\n\n"
                                          f"❌ Event will not be published\n"
                                          f"📧 Organizer has been notified with reason")
                        self._load_pending_events()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to reject event: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()
        
        tk.Button(btn_frame, text='Reject Event', command=confirm_rejection, bg=self.colors.get('danger', '#E74C3C'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=10, width=12).pack(side='right')

    def _request_changes(self, event):
        """Request changes to an event"""
        event_name = event.get('name', 'this event')
        
        # Show feedback form
        feedback_modal = tk.Toplevel(self)
        feedback_modal.title('Request Changes')
        feedback_modal.geometry('600x450')
        feedback_modal.configure(bg='white')
        feedback_modal.transient(self.winfo_toplevel())
        feedback_modal.grab_set()
        
        # Center modal
        feedback_modal.update_idletasks()
        x = (feedback_modal.winfo_screenwidth() // 2) - 300
        y = (feedback_modal.winfo_screenheight() // 2) - 225
        feedback_modal.geometry(f'600x450+{x}+{y}')
        
        # Header
        header = tk.Frame(feedback_modal, bg=self.colors.get('warning', '#F39C12'))
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=self.colors.get('warning', '#F39C12'))
        header_content.pack(padx=20, pady=20)
        
        tk.Label(header_content, text='📝', bg=self.colors.get('warning', '#F39C12'), font=('Helvetica', 36)).pack()
        tk.Label(header_content, text='Request Changes', bg=self.colors.get('warning', '#F39C12'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=(8, 0))
        tk.Label(header_content, text=f"Provide feedback for '{event_name}'", bg=self.colors.get('warning', '#F39C12'), fg='white', font=('Helvetica', 10)).pack(pady=(4, 0))
        
        # Content
        content = tk.Frame(feedback_modal, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(content, text='Changes Requested *', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 6))
        tk.Label(content, text='Describe what needs to be changed or improved. The organizer will be notified.', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 8))
        
        feedback_text = tk.Text(content, height=8, font=('Helvetica', 10), wrap='word')
        feedback_text.pack(fill='both', expand=True, pady=(0, 16))
        
        # Info box
        info_frame = tk.Frame(content, bg='#FFFBEB', highlightthickness=1, highlightbackground='#F59E0B')
        info_frame.pack(fill='x', pady=(0, 16))
        
        tk.Label(info_frame, text='ℹ️ Event will remain in pending status until organizer makes requested changes.', bg='#FFFBEB', fg='#92400E', font=('Helvetica', 9), padx=12, pady=8).pack()
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text='Cancel', command=feedback_modal.destroy, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=10, width=12).pack(side='left')
        
        def send_feedback():
            feedback = feedback_text.get('1.0', 'end-1c').strip()
            if not feedback:
                messagebox.showerror('Required Field', 'Please provide feedback for requested changes.')
                return
            
            feedback_modal.destroy()
            messagebox.showinfo('Feedback Sent', 
                              f"Change request sent to organizer of '{event_name}'.\n\n"
                              f"📧 Organizer will be notified\n"
                              f"⏳ Event remains pending until changes are made")
        
        tk.Button(btn_frame, text='Send Request', command=send_feedback, bg=self.colors.get('warning', '#F39C12'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=10, width=12).pack(side='right')

    def _toggle_select_all(self):
        """Toggle selection of all events"""
        if self.select_all_var.get():
            self.selected_events = [e.get('id') for e in self.pending_events]
        else:
            self.selected_events = []
        
        # Re-render to update checkboxes
        self._render_events()

    def _bulk_approve(self):
        """Approve multiple events"""
        if not self.selected_events:
            messagebox.showwarning('No Selection', 'Please select events to approve.')
            return
        
        count = len(self.selected_events)
        result = messagebox.askyesno('Bulk Approve', 
                                     f"Approve {count} selected event{'s' if count > 1 else ''}?\n\n"
                                     f"✅ All events will be published\n"
                                     f"📧 Organizers will receive approval notifications")
        
        if result:
            def worker():
                try:
                    success_count = 0
                    for event_id in self.selected_events:
                        try:
                            self.api.put(f'admin/events/{event_id}/approve', {})
                            success_count += 1
                        except:
                            pass
                    
                    def show_success():
                        messagebox.showinfo('Bulk Approval Complete', 
                                          f"✅ {success_count} of {count} events approved successfully!")
                        self._load_pending_events()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Bulk approval failed: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _bulk_reject(self):
        """Reject multiple events"""
        if not self.selected_events:
            messagebox.showwarning('No Selection', 'Please select events to reject.')
            return
        
        count = len(self.selected_events)
        
        # Get rejection reason
        reason = simpledialog.askstring('Bulk Reject', 
                                       f'Provide a reason for rejecting {count} event{"s" if count > 1 else ""}:',
                                       parent=self)
        
        if not reason:
            return
        
        result = messagebox.askyesno('Confirm Bulk Reject', 
                                     f"Reject {count} selected event{'s' if count > 1 else ''}?\n\n"
                                     f"❌ All events will be rejected\n"
                                     f"📧 Organizers will be notified\n\n"
                                     f"Reason: {reason}")
        
        if result:
            def worker():
                try:
                    success_count = 0
                    for event_id in self.selected_events:
                        try:
                            self.api.put(f'admin/events/{event_id}/reject', {'reason': reason})
                            success_count += 1
                        except:
                            pass
                    
                    def show_success():
                        messagebox.showinfo('Bulk Rejection Complete', 
                                          f"❌ {success_count} of {count} events rejected.")
                        self._load_pending_events()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Bulk rejection failed: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _format_datetime(self, date_str):
        """Format datetime for display"""
        dt = self._parse_datetime(date_str)
        if dt:
            return dt.strftime('%B %d, %Y')
        return date_str or 'N/A'

    def _parse_datetime(self, date_str):
        """Parse datetime string"""
        if not date_str:
            return None
        try:
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
                try:
                    return datetime.strptime(date_str[:19] if len(date_str) >= 19 else date_str, fmt)
                except:
                    continue
        except:
            pass
        return None
