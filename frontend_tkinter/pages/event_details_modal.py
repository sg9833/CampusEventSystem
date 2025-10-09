import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.email_service import get_email_service


class EventDetailsModal(tk.Toplevel):
    """Full-featured event details modal with registration functionality."""

    def __init__(self, parent, event_id, controller=None, on_close_callback=None):
        super().__init__(parent)
        
        self.event_id = event_id
        self.controller = controller
        self.api = APIClient()
        self.session = SessionManager()
        self.on_close_callback = on_close_callback
        
        # Event data
        self.event = None
        self.is_registered = False
        
        # Get colors from controller or use defaults
        if controller and hasattr(controller, 'colors'):
            self.colors = controller.colors
        else:
            self.colors = {
                'primary': '#2C3E50',
                'secondary': '#3498DB',
                'success': '#27AE60',
                'warning': '#F39C12',
                'danger': '#E74C3C',
                'background': '#ECF0F1'
            }
        
        # Configure window
        self.title('Event Details')
        self.configure(bg='white')
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Set size and position (large modal)
        width = 800
        height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Prevent resize
        self.resizable(False, False)
        
        # Build UI
        self._build_ui()
        
        # Load event data
        self._load_event_details()
        
        # Handle close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        """Build the modal UI structure"""
        # Main container with scrollbar
        main_container = tk.Frame(self, bg='white')
        main_container.pack(fill='both', expand=True)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        
        self.content_frame = tk.Frame(canvas, bg='white')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=self.content_frame, anchor='nw', width=780)
        self.content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Loading spinner
        self.spinner_frame = tk.Frame(self.content_frame, bg='white')
        self.spinner_frame.pack(fill='both', expand=True, pady=100)
        tk.Label(self.spinner_frame, text='Loading event details...', bg='white', fg='#6B7280', font=('Helvetica', 12)).pack()
        self.spinner = ttk.Progressbar(self.spinner_frame, mode='indeterminate', length=300)
        self.spinner.pack(pady=10)
        self.spinner.start(10)

    def _load_event_details(self):
        """Load event details from API"""
        def worker():
            try:
                # Load event details
                self.event = self.api.get(f'events/{self.event_id}')
                
                # Check if user is registered
                try:
                    registered_events = self.api.get('events/registered') or []
                    self.is_registered = any(e.get('id') == self.event_id for e in registered_events)
                except Exception:
                    self.is_registered = False
                
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load event details: {str(e)}')
                    self._on_close()
                self.after(0, show_error)
                return
            
            # Render the content
            self.after(0, self._render_content)
        
        threading.Thread(target=worker, daemon=True).start()

    def _render_content(self):
        """Render the event details content"""
        # Stop and hide spinner
        self.spinner.stop()
        self.spinner_frame.destroy()
        
        if not self.event:
            tk.Label(self.content_frame, text='Event not found', bg='white', fg='#E74C3C', font=('Helvetica', 14)).pack(pady=50)
            return
        
        # Close button (top right)
        close_btn = tk.Button(self.content_frame, text='✕', command=self._on_close, bg='white', fg='#6B7280', relief='flat', font=('Helvetica', 18, 'bold'), width=3, cursor='hand2')
        close_btn.place(x=740, y=10)
        
        # Banner section (colored header)
        banner = tk.Frame(self.content_frame, bg=self.colors.get('secondary', '#3498DB'), height=180)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        
        # Banner content
        banner_content = tk.Frame(banner, bg=self.colors.get('secondary', '#3498DB'))
        banner_content.place(relx=0.5, rely=0.5, anchor='center')
        
        # Category tag
        category = (self.event.get('category', 'General') or 'General').title()
        category_tag = tk.Label(banner_content, text=category, bg='white', fg=self.colors.get('secondary', '#3498DB'), font=('Helvetica', 10, 'bold'), padx=12, pady=4)
        category_tag.pack(pady=(0, 8))
        
        # Event title
        title = self.event.get('title', 'Untitled Event')
        title_label = tk.Label(banner_content, text=title, bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 24, 'bold'), wraplength=700, justify='center')
        title_label.pack(pady=(0, 8))
        
        # Status badge
        status = (self.event.get('status', 'pending') or 'pending').lower()
        if status == 'approved':
            status_label = tk.Label(banner_content, text='✓ Approved Event', bg='#D1FAE5', fg='#065F46', font=('Helvetica', 9, 'bold'), padx=10, pady=3)
            status_label.pack()
        elif status == 'pending':
            status_label = tk.Label(banner_content, text='⏳ Pending Approval', bg='#FEF3C7', fg='#92400E', font=('Helvetica', 9, 'bold'), padx=10, pady=3)
            status_label.pack()
        
        # Main content area
        main_content = tk.Frame(self.content_frame, bg='white')
        main_content.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Quick info cards (3 columns)
        info_cards = tk.Frame(main_content, bg='white')
        info_cards.pack(fill='x', pady=(0, 20))
        
        for i in range(3):
            info_cards.grid_columnconfigure(i, weight=1, uniform='col')
        
        # Date & Time card
        date_card = self._create_info_card(info_cards, '📅', 'Date & Time', 
                                            self.event.get('start_time', 'TBA'),
                                            self.colors.get('secondary', '#3498DB'))
        date_card.grid(row=0, column=0, padx=(0, 8), sticky='ew')
        
        # Venue card
        venue_card = self._create_info_card(info_cards, '📍', 'Venue', 
                                             self.event.get('venue', 'TBA'),
                                             self.colors.get('success', '#27AE60'))
        venue_card.grid(row=0, column=1, padx=8, sticky='ew')
        
        # Duration card
        duration = self._calculate_duration()
        duration_card = self._create_info_card(info_cards, '⏱️', 'Duration', 
                                                duration,
                                                self.colors.get('warning', '#F39C12'))
        duration_card.grid(row=0, column=2, padx=(8, 0), sticky='ew')
        
        # Organizer section
        organizer_frame = tk.Frame(main_content, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        organizer_frame.pack(fill='x', pady=(0, 20))
        
        org_content = tk.Frame(organizer_frame, bg='#F9FAFB')
        org_content.pack(padx=16, pady=12)
        
        tk.Label(org_content, text='👤', bg='#F9FAFB', font=('Helvetica', 16)).pack(side='left', padx=(0, 10))
        org_info = tk.Frame(org_content, bg='#F9FAFB')
        org_info.pack(side='left')
        tk.Label(org_info, text='Organized by', bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w')
        organizer_name = self.event.get('organizer_name', f"User #{self.event.get('organizer_id', 'N/A')}")
        tk.Label(org_info, text=organizer_name, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 12, 'bold')).pack(anchor='w')
        
        # Description section
        desc_frame = tk.Frame(main_content, bg='white')
        desc_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(desc_frame, text='About this event', bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w', pady=(0, 8))
        
        description = self.event.get('description', 'No description available')
        desc_text = tk.Label(desc_frame, text=description, bg='white', fg='#374151', font=('Helvetica', 11), wraplength=720, justify='left')
        desc_text.pack(anchor='w')
        
        # Details grid (2 columns)
        details_frame = tk.Frame(main_content, bg='white')
        details_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(details_frame, text='Event Details', bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w', pady=(0, 12))
        
        details_grid = tk.Frame(details_frame, bg='white')
        details_grid.pack(fill='x')
        details_grid.grid_columnconfigure(0, weight=1)
        details_grid.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # Start time
        self._add_detail_row(details_grid, row, 0, '🕐 Start Time', self.event.get('start_time', 'TBA'))
        
        # End time
        self._add_detail_row(details_grid, row, 1, '🕐 End Time', self.event.get('end_time', 'TBA'))
        row += 1
        
        # Category
        self._add_detail_row(details_grid, row, 0, '🏷️ Category', category)
        
        # Registration deadline
        deadline = self.event.get('registration_deadline', 'Not specified')
        self._add_detail_row(details_grid, row, 1, '⏰ Registration Deadline', deadline)
        row += 1
        
        # Capacity
        capacity = self.event.get('capacity', 'Unlimited')
        registered_count = self.event.get('registered_count', 0)
        capacity_text = f"{registered_count} / {capacity}" if capacity != 'Unlimited' else f"{registered_count} registered"
        self._add_detail_row(details_grid, row, 0, '🎫 Capacity', capacity_text)
        
        # Status
        self._add_detail_row(details_grid, row, 1, '📊 Status', status.title())
        row += 1
        
        # Registration count section
        reg_frame = tk.Frame(main_content, bg='#EFF6FF', highlightthickness=1, highlightbackground='#DBEAFE')
        reg_frame.pack(fill='x', pady=(0, 20))
        
        reg_content = tk.Frame(reg_frame, bg='#EFF6FF')
        reg_content.pack(padx=16, pady=12)
        
        tk.Label(reg_content, text='👥', bg='#EFF6FF', font=('Helvetica', 20)).pack(side='left', padx=(0, 12))
        reg_info = tk.Frame(reg_content, bg='#EFF6FF')
        reg_info.pack(side='left', fill='x', expand=True)
        tk.Label(reg_info, text='Current Registrations', bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 11, 'bold')).pack(anchor='w')
        
        available = capacity - registered_count if isinstance(capacity, int) and isinstance(registered_count, int) else 'Unlimited'
        if available != 'Unlimited':
            reg_text = f"{registered_count} people registered • {available} seats available"
            reg_color = '#059669' if available > 0 else '#DC2626'
        else:
            reg_text = f"{registered_count} people registered • Unlimited capacity"
            reg_color = '#1E40AF'
        
        tk.Label(reg_info, text=reg_text, bg='#EFF6FF', fg=reg_color, font=('Helvetica', 10)).pack(anchor='w', pady=(2, 0))
        
        # Resource requirements (if any)
        resources = self.event.get('resources', [])
        if resources:
            res_frame = tk.Frame(main_content, bg='white')
            res_frame.pack(fill='x', pady=(0, 20))
            
            tk.Label(res_frame, text='Resource Requirements', bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w', pady=(0, 8))
            
            res_list = tk.Frame(res_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
            res_list.pack(fill='x')
            
            if isinstance(resources, list):
                for resource in resources:
                    res_row = tk.Frame(res_list, bg='#F9FAFB')
                    res_row.pack(fill='x', padx=12, pady=6)
                    tk.Label(res_row, text='📦', bg='#F9FAFB', font=('Helvetica', 12)).pack(side='left', padx=(0, 8))
                    
                    if isinstance(resource, dict):
                        res_name = resource.get('name', 'Resource')
                        res_details = resource.get('quantity', '')
                    else:
                        res_name = str(resource)
                        res_details = ''
                    
                    tk.Label(res_row, text=res_name, bg='#F9FAFB', fg='#374151', font=('Helvetica', 10, 'bold')).pack(side='left')
                    if res_details:
                        tk.Label(res_row, text=f"(Qty: {res_details})", bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 9)).pack(side='left', padx=(4, 0))
            else:
                tk.Label(res_list, text='No specific resources listed', bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 10)).pack(padx=12, pady=12)
        
        # Tags/Categories
        tags = self.event.get('tags', [])
        if tags or category:
            tags_frame = tk.Frame(main_content, bg='white')
            tags_frame.pack(fill='x', pady=(0, 20))
            
            tk.Label(tags_frame, text='Tags', bg='white', fg='#1F2937', font=('Helvetica', 14, 'bold')).pack(anchor='w', pady=(0, 8))
            
            tags_container = tk.Frame(tags_frame, bg='white')
            tags_container.pack(anchor='w')
            
            # Add category as first tag
            tag_colors = ['#3498DB', '#27AE60', '#9B59B6', '#F39C12', '#E74C3C', '#1ABC9C', '#34495E']
            
            tag_btn = tk.Label(tags_container, text=category, bg=tag_colors[0], fg='white', font=('Helvetica', 9, 'bold'), padx=10, pady=4)
            tag_btn.pack(side='left', padx=(0, 6))
            
            # Add other tags if they exist
            if isinstance(tags, list):
                for i, tag in enumerate(tags[:6]):  # Limit to 6 additional tags
                    color = tag_colors[(i + 1) % len(tag_colors)]
                    tag_btn = tk.Label(tags_container, text=str(tag), bg=color, fg='white', font=('Helvetica', 9, 'bold'), padx=10, pady=4)
                    tag_btn.pack(side='left', padx=(0, 6))
        
        # Separator
        separator = tk.Frame(main_content, bg='#E5E7EB', height=1)
        separator.pack(fill='x', pady=20)
        
        # Action buttons
        self._render_action_buttons(main_content)

    def _create_info_card(self, parent, icon, label, value, color):
        """Create an info card widget"""
        card = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        
        # Icon with colored background
        icon_frame = tk.Frame(card, bg=color, width=60, height=60)
        icon_frame.pack(pady=(12, 8))
        icon_frame.pack_propagate(False)
        tk.Label(icon_frame, text=icon, bg=color, font=('Helvetica', 24)).place(relx=0.5, rely=0.5, anchor='center')
        
        # Label
        tk.Label(card, text=label, bg='white', fg='#6B7280', font=('Helvetica', 9)).pack()
        
        # Value
        tk.Label(card, text=value, bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold'), wraplength=200).pack(pady=(2, 12))
        
        return card

    def _add_detail_row(self, parent, row, col, label, value):
        """Add a detail row to the grid"""
        detail_frame = tk.Frame(parent, bg='white')
        detail_frame.grid(row=row, column=col, sticky='w', padx=(0, 16), pady=6)
        
        tk.Label(detail_frame, text=label, bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w')
        tk.Label(detail_frame, text=str(value), bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(2, 0))

    def _render_action_buttons(self, parent):
        """Render action buttons based on registration status"""
        btn_frame = tk.Frame(parent, bg='white')
        btn_frame.pack(fill='x', pady=(0, 20))
        
        if self.is_registered:
            # User is already registered
            status_msg = tk.Frame(btn_frame, bg='#D1FAE5', highlightthickness=1, highlightbackground='#6EE7B7')
            status_msg.pack(fill='x', pady=(0, 12))
            
            msg_content = tk.Frame(status_msg, bg='#D1FAE5')
            msg_content.pack(padx=16, pady=12)
            tk.Label(msg_content, text='✓', bg='#D1FAE5', fg='#065F46', font=('Helvetica', 16, 'bold')).pack(side='left', padx=(0, 8))
            tk.Label(msg_content, text='You are registered for this event!', bg='#D1FAE5', fg='#065F46', font=('Helvetica', 12, 'bold')).pack(side='left')
            
            # Cancel registration button
            tk.Button(btn_frame, text='Cancel Registration', command=self._cancel_registration, bg='#E74C3C', fg='white', relief='flat', font=('Helvetica', 12, 'bold'), padx=40, pady=12, cursor='hand2').pack(fill='x')
        else:
            # Check if event is full
            capacity = self.event.get('capacity', 'Unlimited')
            registered_count = self.event.get('registered_count', 0)
            is_full = False
            
            if capacity != 'Unlimited' and isinstance(capacity, int) and isinstance(registered_count, int):
                is_full = registered_count >= capacity
            
            if is_full:
                # Event is full
                full_msg = tk.Frame(btn_frame, bg='#FEE2E2', highlightthickness=1, highlightbackground='#FCA5A5')
                full_msg.pack(fill='x', pady=(0, 12))
                
                msg_content = tk.Frame(full_msg, bg='#FEE2E2')
                msg_content.pack(padx=16, pady=12)
                tk.Label(msg_content, text='⚠️', bg='#FEE2E2', fg='#991B1B', font=('Helvetica', 16, 'bold')).pack(side='left', padx=(0, 8))
                tk.Label(msg_content, text='This event has reached maximum capacity', bg='#FEE2E2', fg='#991B1B', font=('Helvetica', 12, 'bold')).pack(side='left')
                
                tk.Button(btn_frame, text='Event Full - Cannot Register', bg='#9CA3AF', fg='white', relief='flat', font=('Helvetica', 12, 'bold'), padx=40, pady=12, state='disabled').pack(fill='x')
            else:
                # Can register
                tk.Button(btn_frame, text='🎫 Register Now', command=self._register_event, bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 12, 'bold'), padx=40, pady=12, cursor='hand2').pack(fill='x')
        
        # Close button
        tk.Button(btn_frame, text='Close', command=self._on_close, bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 11), padx=40, pady=10, cursor='hand2').pack(fill='x', pady=(8, 0))

    def _calculate_duration(self):
        """Calculate event duration"""
        start = self._parse_dt(self.event.get('start_time'))
        end = self._parse_dt(self.event.get('end_time'))
        
        if start and end:
            duration = end - start
            hours = duration.total_seconds() / 3600
            
            if hours < 1:
                minutes = int(duration.total_seconds() / 60)
                return f"{minutes} minutes"
            elif hours < 24:
                return f"{hours:.1f} hours"
            else:
                days = int(hours / 24)
                return f"{days} day{'s' if days > 1 else ''}"
        
        return "Duration not specified"

    def _register_event(self):
        """Register for the event"""
        if not self.event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return
        
        # Confirm registration
        if not messagebox.askyesno('Confirm Registration', 
                                   f"Do you want to register for '{self.event.get('title', 'this event')}'?"):
            return
        
        try:
            response = self.api.post(f'events/{self.event_id}/register', {})
            messagebox.showinfo('Success', 'Successfully registered for the event!')
            
            # Send registration confirmation email
            try:
                user = self.session.get_user()
                if user and user.get('email'):
                    email_service = get_email_service()
                    email_service.send_event_registration_confirmation(
                        user_email=user['email'],
                        event_details=self.event,
                        user_name=user.get('name', 'Student')
                    )
                    print("[EMAIL] Registration confirmation sent")
            except Exception as email_error:
                print(f"[EMAIL ERROR] Failed to send confirmation: {email_error}")
            
            # Update registration status and reload
            self.is_registered = True
            self._load_event_details()
            
        except Exception as e:
            error_msg = str(e)
            if 'already registered' in error_msg.lower():
                messagebox.showwarning('Already Registered', 'You are already registered for this event')
                self.is_registered = True
                self._load_event_details()
            elif 'full' in error_msg.lower() or 'capacity' in error_msg.lower():
                messagebox.showerror('Event Full', 'This event has reached maximum capacity')
            else:
                messagebox.showerror('Error', f'Failed to register: {error_msg}')

    def _cancel_registration(self):
        """Cancel event registration"""
        if not self.event_id:
            messagebox.showerror('Error', 'Invalid event ID')
            return
        
        # Confirm cancellation
        if not messagebox.askyesno('Confirm Cancellation', 
                                   f"Are you sure you want to cancel your registration for '{self.event.get('title', 'this event')}'?"):
            return
        
        try:
            response = self.api.delete(f'events/{self.event_id}/register')
            messagebox.showinfo('Success', 'Registration cancelled successfully')
            
            # Update registration status and reload
            self.is_registered = False
            self._load_event_details()
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to cancel registration: {str(e)}')

    def _on_close(self):
        """Handle modal close"""
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

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


# Convenience function to open modal
def show_event_details(parent, event_id, controller=None, on_close_callback=None):
    """
    Convenience function to show event details modal.
    
    Args:
        parent: Parent widget
        event_id: Event ID to display
        controller: Main controller (for colors)
        on_close_callback: Optional callback when modal closes
    """
    modal = EventDetailsModal(parent, event_id, controller, on_close_callback)
    return modal
