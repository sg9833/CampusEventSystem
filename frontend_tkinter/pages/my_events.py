import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
import csv
from tkinter import filedialog

from utils.api_client import APIClient
from utils.session_manager import SessionManager


class MyEventsPage(tk.Frame):
    """My Events page with tabbed interface for event management."""

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
        self.all_events = []
        self.pending_events = []
        self.approved_events = []
        self.past_events = []
        self.rejected_events = []
        
        # Layout
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Tabs
        self.grid_rowconfigure(2, weight=1)  # Content
        self.grid_columnconfigure(0, weight=1)
        
        self._build_header()
        self._build_tabs()
        self._build_content_area()
        
        # Load data
        self._load_events()

    def _build_header(self):
        """Build header section"""
        header = tk.Frame(self, bg='white', height=80, highlightthickness=1, highlightbackground='#E5E7EB')
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)
        
        container = tk.Frame(header, bg='white')
        container.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Title
        title_frame = tk.Frame(container, bg='white')
        title_frame.pack(side='left')
        tk.Label(title_frame, text='My Events', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Manage your created events', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(container, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text='🔄 Refresh', command=self._load_events, bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 10), padx=16, pady=8).pack(side='left', padx=(0, 8))
        tk.Button(btn_frame, text='➕ Create New Event', command=self._create_new_event, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=16, pady=8).pack(side='left')

    def _build_tabs(self):
        """Build tab navigation"""
        self.tab_frame = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        self.tab_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=(12, 0))
        
        self.current_tab = 'pending'
        
        tabs = [
            ('pending', 'Pending Approval', '#F59E0B'),
            ('approved', 'Approved Events', '#10B981'),
            ('past', 'Past Events', '#6B7280'),
            ('rejected', 'Rejected', '#EF4444')
        ]
        
        for tab_id, label, color in tabs:
            btn = tk.Button(self.tab_frame, text=label, command=lambda t=tab_id: self._switch_tab(t), bg='white', fg='#374151', relief='flat', font=('Helvetica', 11), padx=20, pady=12, cursor='hand2')
            btn.pack(side='left')
            
            # Store button reference
            if not hasattr(self, 'tab_buttons'):
                self.tab_buttons = {}
            self.tab_buttons[tab_id] = btn

    def _build_content_area(self):
        """Build scrollable content area"""
        content_container = tk.Frame(self, bg=self.colors.get('background', '#ECF0F1'))
        content_container.grid(row=2, column=0, sticky='nsew', padx=30, pady=(0, 20))
        
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
        
        # Loading indicator
        self.loading_frame = tk.Frame(self.content, bg=self.colors.get('background', '#ECF0F1'))

    def _load_events(self):
        """Load events from API"""
        # Show loading
        self._show_loading()
        
        def worker():
            try:
                # Load all organizer's events
                self.all_events = self.api.get('events/my') or []
                
                # Categorize events
                now = datetime.now()
                self.pending_events = []
                self.approved_events = []
                self.past_events = []
                self.rejected_events = []
                
                for event in self.all_events:
                    status = (event.get('status') or 'pending').lower()
                    end_time = self._parse_dt(event.get('end_time'))
                    
                    if status == 'pending':
                        self.pending_events.append(event)
                    elif status == 'rejected':
                        self.rejected_events.append(event)
                    elif end_time and end_time < now:
                        self.past_events.append(event)
                    else:
                        self.approved_events.append(event)
                
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load events: {str(e)}')
                self.after(0, show_error)
            
            # Render content
            self.after(0, lambda: self._switch_tab(self.current_tab))
        
        threading.Thread(target=worker, daemon=True).start()

    def _show_loading(self):
        """Show loading indicator"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        self.loading_frame = tk.Frame(self.content, bg=self.colors.get('background', '#ECF0F1'))
        self.loading_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(self.loading_frame, text='Loading events...', bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 12)).pack()
        
        spinner = ttk.Progressbar(self.loading_frame, mode='indeterminate', length=300)
        spinner.pack(pady=10)
        spinner.start(10)

    def _switch_tab(self, tab_id):
        """Switch to specified tab"""
        self.current_tab = tab_id
        
        # Update tab button styles
        for tid, btn in self.tab_buttons.items():
            if tid == tab_id:
                btn.config(bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 11, 'bold'))
            else:
                btn.config(bg='white', fg='#374151', font=('Helvetica', 11))
        
        # Render content based on tab
        self._render_tab_content(tab_id)

    def _render_tab_content(self, tab_id):
        """Render content for the selected tab"""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Get events for current tab
        if tab_id == 'pending':
            events = self.pending_events
            empty_msg = 'No pending events'
            empty_icon = '⏳'
        elif tab_id == 'approved':
            events = self.approved_events
            empty_msg = 'No approved events'
            empty_icon = '✓'
        elif tab_id == 'past':
            events = self.past_events
            empty_msg = 'No past events'
            empty_icon = '📅'
        else:  # rejected
            events = self.rejected_events
            empty_msg = 'No rejected events'
            empty_icon = '✗'
        
        # Show count
        count_frame = tk.Frame(self.content, bg=self.colors.get('background', '#ECF0F1'))
        count_frame.pack(fill='x', pady=(12, 8))
        tk.Label(count_frame, text=f'{len(events)} event{"s" if len(events) != 1 else ""}', bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 11)).pack(side='left')
        
        if not events:
            # Empty state
            empty_frame = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            empty_frame.pack(fill='both', expand=True, pady=20)
            
            tk.Label(empty_frame, text=empty_icon, bg='white', font=('Helvetica', 48)).pack(pady=(40, 10))
            tk.Label(empty_frame, text=empty_msg, bg='white', fg='#374151', font=('Helvetica', 14, 'bold')).pack()
            tk.Label(empty_frame, text='Create your first event to get started', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(pady=(4, 40))
        else:
            # Render event cards
            for event in events:
                card = self._create_event_card(event, tab_id)
                card.pack(fill='x', pady=(0, 12))

    def _create_event_card(self, event, tab_id):
        """Create an event card"""
        card = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=16)
        
        # Header row
        header = tk.Frame(content, bg='white')
        header.pack(fill='x', pady=(0, 8))
        
        # Title
        title_frame = tk.Frame(header, bg='white')
        title_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(title_frame, text=event.get('title', 'Untitled Event'), bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(side='left')
        
        # Status badge
        status = (event.get('status') or 'pending').lower()
        status_config = {
            'pending': ('⏳ Pending', '#FEF3C7', '#92400E'),
            'approved': ('✓ Approved', '#D1FAE5', '#065F46'),
            'rejected': ('✗ Rejected', '#FEE2E2', '#991B1B'),
            'draft': ('📝 Draft', '#E0E7FF', '#3730A3')
        }
        
        badge_text, badge_bg, badge_fg = status_config.get(status, ('Unknown', '#F3F4F6', '#6B7280'))
        status_badge = tk.Label(title_frame, text=badge_text, bg=badge_bg, fg=badge_fg, font=('Helvetica', 9, 'bold'), padx=10, pady=3)
        status_badge.pack(side='left', padx=(12, 0))
        
        # Actions menu button
        actions_btn = tk.Menubutton(header, text='⋮ Actions', bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6, cursor='hand2')
        actions_btn.pack(side='right')
        
        # Create actions menu
        actions_menu = tk.Menu(actions_btn, tearoff=0, font=('Helvetica', 10))
        actions_btn.config(menu=actions_menu)
        
        actions_menu.add_command(label='👁️ View Details', command=lambda e=event: self._view_event_details(e))
        
        # Check if can edit (pending/approved and not in past)
        can_edit = status in ['pending', 'approved'] and not self._is_past_event(event)
        if can_edit:
            actions_menu.add_command(label='✏️ Edit Event', command=lambda e=event: self._edit_event(e))
        
        actions_menu.add_command(label='👥 View Registrations', command=lambda e=event: self._view_registrations(e))
        actions_menu.add_command(label='📥 Download Attendee List', command=lambda e=event: self._download_attendees(e))
        
        if not self._is_past_event(event):
            actions_menu.add_command(label='📢 Send Announcement', command=lambda e=event: self._send_announcement(e))
        
        actions_menu.add_separator()
        actions_menu.add_command(label='🗑️ Cancel Event', command=lambda e=event: self._cancel_event(e))
        
        # Details row
        details = tk.Frame(content, bg='white')
        details.pack(fill='x', pady=(0, 8))
        
        # Category tag
        category = (event.get('category', 'General') or 'General').title()
        tk.Label(details, text=f'🏷️ {category}', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(side='left', padx=(0, 16))
        
        # Date
        start_time = event.get('start_time', 'TBA')
        tk.Label(details, text=f'📅 {start_time}', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(side='left', padx=(0, 16))
        
        # Venue
        venue = event.get('venue', 'TBA')
        tk.Label(details, text=f'📍 {venue}', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(side='left', padx=(0, 16))
        
        # Registration count
        reg_count = event.get('registered_count', 0)
        capacity = event.get('capacity', 'Unlimited')
        reg_text = f'👥 {reg_count} registered'
        if capacity != 'Unlimited':
            reg_text += f' / {capacity}'
        tk.Label(details, text=reg_text, bg='white', fg=self.colors.get('secondary', '#3498DB'), font=('Helvetica', 9, 'bold')).pack(side='left')
        
        # Description preview
        description = event.get('description', '')
        if description:
            desc_preview = description[:150] + ('...' if len(description) > 150 else '')
            tk.Label(content, text=desc_preview, bg='white', fg='#6B7280', font=('Helvetica', 9), wraplength=900, justify='left').pack(anchor='w')
        
        return card

    def _view_event_details(self, event):
        """View full event details"""
        event_id = event.get('id')
        if not event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return
        
        # Import and show event details modal
        try:
            from pages.event_details_modal import show_event_details
            show_event_details(self, event_id, self.controller, on_close_callback=self._load_events)
        except ImportError:
            # Fallback to simple message box
            details = f"Event: {event.get('title', 'Untitled')}\n"
            details += f"Category: {event.get('category', 'N/A')}\n"
            details += f"Start: {event.get('start_time', 'N/A')}\n"
            details += f"End: {event.get('end_time', 'N/A')}\n"
            details += f"Venue: {event.get('venue', 'N/A')}\n"
            details += f"Status: {event.get('status', 'N/A')}\n"
            details += f"Registered: {event.get('registered_count', 0)}"
            messagebox.showinfo('Event Details', details)

    def _edit_event(self, event):
        """Edit event details"""
        messagebox.showinfo('Edit Event', f"Edit functionality for '{event.get('title', 'Event')}' would open here.\n\nThis would navigate to an edit form with pre-filled data.")

    def _view_registrations(self, event):
        """View registrations modal"""
        event_id = event.get('id')
        if not event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return
        
        # Create modal
        modal = tk.Toplevel(self)
        modal.title(f"Registrations - {event.get('title', 'Event')}")
        modal.geometry('700x500')
        modal.configure(bg='white')
        modal.transient(self)
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (700 // 2)
        y = (modal.winfo_screenheight() // 2) - (500 // 2)
        modal.geometry(f'700x500+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        tk.Label(header, text=f"Registrations for: {event.get('title', 'Event')}", bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 14, 'bold')).pack(padx=20, pady=16)
        
        # Load registrations
        loading_label = tk.Label(modal, text='Loading registrations...', bg='white', fg='#6B7280', font=('Helvetica', 11))
        loading_label.pack(pady=50)
        
        def load_registrations():
            try:
                registrations = self.api.get(f'events/{event_id}/registrations') or []
                
                def render():
                    loading_label.destroy()
                    
                    # Toolbar
                    toolbar = tk.Frame(modal, bg='white')
                    toolbar.pack(fill='x', padx=20, pady=(12, 0))
                    
                    tk.Label(toolbar, text=f'{len(registrations)} registration{"s" if len(registrations) != 1 else ""}', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='left')
                    
                    tk.Button(toolbar, text='📥 Export CSV', command=lambda: self._export_registrations_csv(registrations, event), bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='right')
                    
                    # Table frame
                    table_frame = tk.Frame(modal, bg='white')
                    table_frame.pack(fill='both', expand=True, padx=20, pady=(12, 12))
                    
                    if not registrations:
                        tk.Label(table_frame, text='No registrations yet', bg='white', fg='#6B7280', font=('Helvetica', 11)).pack(pady=50)
                    else:
                        # Create table
                        columns = ('Name', 'Email', 'Registration Date')
                        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
                        
                        # Configure columns
                        tree.heading('Name', text='Name')
                        tree.heading('Email', text='Email')
                        tree.heading('Registration Date', text='Registration Date')
                        
                        tree.column('Name', width=200)
                        tree.column('Email', width=250)
                        tree.column('Registration Date', width=200)
                        
                        # Add scrollbar
                        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
                        tree.configure(yscrollcommand=scrollbar.set)
                        scrollbar.pack(side='right', fill='y')
                        tree.pack(side='left', fill='both', expand=True)
                        
                        # Populate data
                        for reg in registrations:
                            user = reg.get('user', {})
                            name = user.get('username', user.get('name', 'N/A'))
                            email = user.get('email', 'N/A')
                            reg_date = reg.get('registered_at', 'N/A')
                            
                            tree.insert('', 'end', values=(name, email, reg_date))
                    
                    # Close button
                    tk.Button(modal, text='Close', command=modal.destroy, bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 10), padx=24, pady=10).pack(pady=(0, 16))
                
                modal.after(0, render)
                
            except Exception as e:
                def show_error():
                    loading_label.config(text=f'Error: {str(e)}')
                modal.after(0, show_error)
        
        threading.Thread(target=load_registrations, daemon=True).start()

    def _download_attendees(self, event):
        """Download attendee list as CSV"""
        event_id = event.get('id')
        if not event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return
        
        try:
            registrations = self.api.get(f'events/{event_id}/registrations') or []
            
            if not registrations:
                messagebox.showinfo('No Data', 'No registrations to export')
                return
            
            self._export_registrations_csv(registrations, event)
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load registrations: {str(e)}')

    def _export_registrations_csv(self, registrations, event):
        """Export registrations to CSV file"""
        if not registrations:
            messagebox.showinfo('No Data', 'No registrations to export')
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            initialfile=f"attendees_{event.get('title', 'event').replace(' ', '_')}.csv"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header
                writer.writerow(['Name', 'Email', 'Registration Date', 'User ID'])
                
                # Data
                for reg in registrations:
                    user = reg.get('user', {})
                    name = user.get('username', user.get('name', 'N/A'))
                    email = user.get('email', 'N/A')
                    reg_date = reg.get('registered_at', 'N/A')
                    user_id = user.get('id', reg.get('user_id', 'N/A'))
                    
                    writer.writerow([name, email, reg_date, user_id])
            
            messagebox.showinfo('Success', f'Attendee list exported successfully to:\n{filename}')
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to export CSV: {str(e)}')

    def _send_announcement(self, event):
        """Send announcement to registered users"""
        event_id = event.get('id')
        if not event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return
        
        # Create announcement modal
        modal = tk.Toplevel(self)
        modal.title('Send Announcement')
        modal.geometry('600x450')
        modal.configure(bg='white')
        modal.transient(self)
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (600 // 2)
        y = (modal.winfo_screenheight() // 2) - (450 // 2)
        modal.geometry(f'600x450+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        tk.Label(header, text=f"Send Announcement", bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 14, 'bold')).pack(padx=20, pady=16)
        
        # Content
        content = tk.Frame(modal, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(content, text=f"Event: {event.get('title', 'Event')}", bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 16))
        
        # Subject
        tk.Label(content, text='Subject *', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        subject_var = tk.StringVar()
        subject_entry = tk.Entry(content, textvariable=subject_var, font=('Helvetica', 11), width=60)
        subject_entry.pack(anchor='w', pady=(0, 16), ipady=4)
        
        # Message
        tk.Label(content, text='Message *', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        
        msg_frame = tk.Frame(content, bg='white', highlightthickness=1, highlightbackground='#D1D5DB')
        msg_frame.pack(anchor='w', pady=(0, 16))
        
        msg_scroll = ttk.Scrollbar(msg_frame, orient='vertical')
        msg_text = tk.Text(msg_frame, height=10, width=58, font=('Helvetica', 11), yscrollcommand=msg_scroll.set, wrap='word')
        msg_scroll.config(command=msg_text.yview)
        msg_scroll.pack(side='right', fill='y')
        msg_text.pack(side='left', fill='both', expand=True)
        
        # Info
        info_frame = tk.Frame(content, bg='#EFF6FF', highlightthickness=1, highlightbackground='#BFDBFE')
        info_frame.pack(fill='x', pady=(0, 16))
        tk.Label(info_frame, text=f"This will be sent to {event.get('registered_count', 0)} registered user(s)", bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 9)).pack(padx=12, pady=8)
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        def send():
            subject = subject_var.get().strip()
            message = msg_text.get('1.0', 'end-1c').strip()
            
            if not subject or not message:
                messagebox.showerror('Validation Error', 'Subject and message are required')
                return
            
            if messagebox.askyesno('Confirm', f'Send this announcement to all registered users?'):
                try:
                    payload = {
                        'subject': subject,
                        'message': message
                    }
                    self.api.post(f'events/{event_id}/announce', payload)
                    messagebox.showinfo('Success', 'Announcement sent successfully!')
                    modal.destroy()
                except Exception as e:
                    messagebox.showerror('Error', f'Failed to send announcement: {str(e)}')
        
        tk.Button(btn_frame, text='Send Announcement', command=send, bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=10).pack(side='left', fill='x', expand=True, padx=(0, 8))
        tk.Button(btn_frame, text='Cancel', command=modal.destroy, bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 10), padx=20, pady=10).pack(side='right', fill='x', expand=True, padx=(8, 0))

    def _cancel_event(self, event):
        """Cancel/delete event"""
        event_id = event.get('id')
        if not event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return
        
        if not messagebox.askyesno('Confirm Cancellation', 
                                   f"Are you sure you want to cancel '{event.get('title', 'this event')}'?\n\n"
                                   f"This action cannot be undone and all registrations will be cancelled."):
            return
        
        try:
            self.api.delete(f'events/{event_id}')
            messagebox.showinfo('Success', 'Event cancelled successfully')
            self._load_events()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to cancel event: {str(e)}')

    def _create_new_event(self):
        """Navigate to create event page"""
        if hasattr(self.controller, 'show_page'):
            self.controller.show_page('CreateEventPage')
        else:
            messagebox.showinfo('Create Event', 'Navigate to event creation page')

    def _is_past_event(self, event):
        """Check if event is in the past"""
        end_time = self._parse_dt(event.get('end_time'))
        if end_time:
            return end_time < datetime.now()
        return False

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
