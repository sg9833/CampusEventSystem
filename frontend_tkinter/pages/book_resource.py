import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime, timedelta
from tkcalendar import DateEntry

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.canvas_button import create_primary_button, create_secondary_button, create_success_button


class BookResourcePage(tk.Frame):
    """Resource booking page with availability checking."""

    def __init__(self, parent, controller, resource_id=None):
        super().__init__(parent, bg=controller.colors.get('background', '#ECF0F1'))
        self.controller = controller
        self.api = APIClient()
        self.session = SessionManager()
        self.preselected_resource_id = resource_id
        
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
        self.resources = []
        self.selected_resource = None
        self.availability_data = {}
        self.selected_start_slot = None
        self.selected_end_slot = None
        
        # Form variables
        self.resource_var = tk.StringVar()
        self.purpose_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.attendees_var = tk.StringVar(value='')
        self.requirements_var = tk.StringVar()
        self.priority_var = tk.StringVar(value='normal')
        
        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_resources()

    def _build_ui(self):
        """Build the main UI"""
        # Scrollable container
        canvas = tk.Canvas(self, bg=self.colors.get('background', '#ECF0F1'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        
        self.content = tk.Frame(canvas, bg=self.colors.get('background', '#ECF0F1'))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        canvas.grid(row=0, column=0, sticky='nsew')
        
        canvas.create_window((0, 0), window=self.content, anchor='nw')
        self.content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Update canvas width on resize
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag('all')[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Header
        header = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        header.pack(fill='x', padx=30, pady=(20, 0))
        
        header_content = tk.Frame(header, bg='white')
        header_content.pack(padx=30, pady=20)
        
        tk.Label(header_content, text='📅 Book a Resource', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(header_content, text='Fill in the details below to request a resource booking', bg='white', fg='#1F2937', font=('Helvetica', 11)).pack(anchor='w', pady=(4, 0))
        
        # Booking form container
        form_container = tk.Frame(self.content, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        form_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        form_content = tk.Frame(form_container, bg='white')
        form_content.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Section 1: Resource Selection
        self._add_section_header(form_content, '1. Select Resource')
        
        resource_frame = tk.Frame(form_content, bg='white')
        resource_frame.pack(fill='x', pady=(0, 24))
        
        tk.Label(resource_frame, text='Resource *', bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 6))
        
        self.resource_dropdown = ttk.Combobox(resource_frame, textvariable=self.resource_var, state='readonly', font=('Helvetica', 11), width=50)
        self.resource_dropdown.pack(fill='x', pady=(0, 6))
        self.resource_dropdown.bind('<<ComboboxSelected>>', self._on_resource_selected)
        
        # Resource info display
        self.resource_info_frame = tk.Frame(resource_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        self.resource_info_frame.pack(fill='x', pady=(8, 0))
        self.resource_info_frame.pack_forget()  # Hide initially
        
        # Section 2: Purpose
        self._add_section_header(form_content, '2. Booking Purpose')
        
        purpose_frame = tk.Frame(form_content, bg='white')
        purpose_frame.pack(fill='x', pady=(0, 24))
        
        tk.Label(purpose_frame, text='Purpose of Booking *', bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 6))
        tk.Label(purpose_frame, text='Briefly describe why you need this resource', bg='white', fg='#1F2937', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 6))
        
        purpose_entry = tk.Entry(purpose_frame, textvariable=self.purpose_var, font=('Helvetica', 11))
        purpose_entry.pack(fill='x')
        
        # Section 3: Date and Time
        self._add_section_header(form_content, '3. Schedule Your Booking')
        
        datetime_frame = tk.Frame(form_content, bg='white')
        datetime_frame.pack(fill='x', pady=(0, 24))
        
        # Date selection
        tk.Label(datetime_frame, text='Booking Date *', bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 6))
        
        date_container = tk.Frame(datetime_frame, bg='white')
        date_container.pack(fill='x', pady=(0, 16))
        
        try:
            self.date_picker = DateEntry(date_container, width=20, background=self.colors.get('secondary', '#3498DB'), foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', mindate=datetime.now())
            self.date_picker.pack(side='left')
            self.date_picker.bind('<<DateEntrySelected>>', lambda e: self._load_availability())
        except:
            # Fallback
            date_entry = tk.Entry(date_container, textvariable=self.date_var, font=('Helvetica', 11), width=22)
            date_entry.pack(side='left')
            tk.Label(date_container, text='Format: YYYY-MM-DD', bg='white', fg='#1F2937', font=('Helvetica', 9)).pack(side='left', padx=(8, 0))
        
        check_btn = create_primary_button(date_container, text='Check Availability', command=self._load_availability)
        check_btn.pack(side='left', padx=(12, 0))
        
        # Time slots
        tk.Label(datetime_frame, text='Select Time Slot *', bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 6))
        tk.Label(datetime_frame, text='Click to select start time, then click again to select end time. Green = Available, Red = Booked, Gray = Unavailable', bg='white', fg='#1F2937', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 8))
        
        # Time slot grid container
        self.timeslot_container = tk.Frame(datetime_frame, bg='white')
        self.timeslot_container.pack(fill='x')
        
        # Selection display
        self.selection_frame = tk.Frame(datetime_frame, bg='#EFF6FF', highlightthickness=1, highlightbackground='#BFDBFE')
        self.selection_frame.pack(fill='x', pady=(12, 0))
        self.selection_frame.pack_forget()  # Hide initially
        
        selection_content = tk.Frame(self.selection_frame, bg='#EFF6FF')
        selection_content.pack(padx=16, pady=12)
        
        self.selection_label = tk.Label(selection_content, text='', bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 10, 'bold'))
        self.selection_label.pack()
        
        # Section 4: Additional Details
        self._add_section_header(form_content, '4. Additional Details')
        
        details_frame = tk.Frame(form_content, bg='white')
        details_frame.pack(fill='x', pady=(0, 24))
        
        # Expected attendees
        tk.Label(details_frame, text='Expected Attendees *', bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 6))
        attendees_entry = tk.Entry(details_frame, textvariable=self.attendees_var, font=('Helvetica', 11))
        attendees_entry.pack(fill='x', pady=(0, 16))
        
        # Additional requirements
        tk.Label(details_frame, text='Additional Requirements', bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 6))
        tk.Label(details_frame, text='Any special requirements or setup needs', bg='white', fg='#1F2937', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 6))
        
        requirements_text = tk.Text(details_frame, height=4, font=('Helvetica', 10), wrap='word')
        requirements_text.pack(fill='x', pady=(0, 16))
        requirements_text.bind('<KeyRelease>', lambda e: self.requirements_var.set(requirements_text.get('1.0', 'end-1c')))
        
        # Priority
        tk.Label(details_frame, text='Request Priority', bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 6))
        
        priority_frame = tk.Frame(details_frame, bg='white')
        priority_frame.pack(fill='x')
        
        tk.Radiobutton(priority_frame, text='⚪ Normal - Standard processing (2-3 days)', variable=self.priority_var, value='normal', bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=2)
        tk.Radiobutton(priority_frame, text='🔴 Urgent - Expedited processing (within 24 hours)', variable=self.priority_var, value='urgent', bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=2)
        
        # Warning box
        self.warning_frame = tk.Frame(form_content, bg='#FEF3C7', highlightthickness=1, highlightbackground='#F59E0B')
        self.warning_frame.pack(fill='x', pady=(0, 20))
        self.warning_frame.pack_forget()  # Hide initially
        
        # Action buttons
        btn_frame = tk.Frame(form_content, bg='white')
        btn_frame.pack(fill='x', pady=(12, 0))
        
        cancel_btn = create_secondary_button(btn_frame, text='Cancel', command=self._cancel, width=200)
        cancel_btn.pack(side='left', padx=5)
        
        submit_btn = create_primary_button(btn_frame, text='Submit Booking Request', command=self._submit_booking, width=300)
        submit_btn.pack(side='right', padx=5)

    def _add_section_header(self, parent, text):
        """Add a section header"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', pady=(0, 12))
        
        tk.Label(frame, text=text, bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 14, 'bold')).pack(side='left')
        
        separator = tk.Frame(parent, bg='#E5E7EB', height=1)
        separator.pack(fill='x', pady=(0, 16))

    def _load_resources(self):
        """Load available resources"""
        def worker():
            try:
                self.resources = self.api.get('resources') or []
                
                def update_ui():
                    if self.resources:
                        resource_names = [f"{r.get('name', 'Unknown')} ({r.get('code', r.get('id', 'N/A'))})" for r in self.resources]
                        self.resource_dropdown['values'] = resource_names
                        
                        # If resource was preselected
                        if self.preselected_resource_id:
                            for idx, r in enumerate(self.resources):
                                if str(r.get('id')) == str(self.preselected_resource_id):
                                    self.resource_dropdown.current(idx)
                                    self._on_resource_selected(None)
                                    break
                    else:
                        messagebox.showwarning('No Resources', 'No resources available for booking.')
                
                self.after(0, update_ui)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load resources: {str(e)}')
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _on_resource_selected(self, event):
        """Handle resource selection"""
        selected_idx = self.resource_dropdown.current()
        if selected_idx >= 0 and selected_idx < len(self.resources):
            self.selected_resource = self.resources[selected_idx]
            self._show_resource_info()
            self._load_availability()

    def _show_resource_info(self):
        """Display selected resource information"""
        if not self.selected_resource:
            return
        
        # Clear previous info
        for widget in self.resource_info_frame.winfo_children():
            widget.destroy()
        
        info_content = tk.Frame(self.resource_info_frame, bg='#F9FAFB')
        info_content.pack(padx=16, pady=12)
        
        # Resource details
        details_frame = tk.Frame(info_content, bg='#F9FAFB')
        details_frame.pack(fill='x')
        
        resource_type = self.selected_resource.get('type', 'N/A')
        capacity = self.selected_resource.get('capacity', 'N/A')
        location = self.selected_resource.get('location', self.selected_resource.get('building', 'N/A'))
        
        self._add_info_item(details_frame, '📋 Type:', resource_type)
        self._add_info_item(details_frame, '🎫 Capacity:', str(capacity))
        self._add_info_item(details_frame, '📍 Location:', location)
        
        # Amenities
        amenities = self.selected_resource.get('amenities', [])
        if amenities:
            tk.Label(info_content, text='Amenities:', bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 9)).pack(anchor='w', pady=(8, 4))
            amenities_text = ', '.join([str(a).title() for a in amenities])
            tk.Label(info_content, text=amenities_text, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 9)).pack(anchor='w')
        
        self.resource_info_frame.pack(fill='x', pady=(8, 0))

    def _add_info_item(self, parent, label, value):
        """Add info item"""
        frame = tk.Frame(parent, bg='#F9FAFB')
        frame.pack(side='left', padx=(0, 20))
        tk.Label(frame, text=label, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 9)).pack(side='left', padx=(0, 4))
        tk.Label(frame, text=value, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 9, 'bold')).pack(side='left')

    def _load_availability(self):
        """Load availability for selected date and resource"""
        if not self.selected_resource:
            messagebox.showwarning('No Resource', 'Please select a resource first.')
            return
        
        # Get selected date
        try:
            if hasattr(self, 'date_picker'):
                selected_date = self.date_picker.get_date().strftime('%Y-%m-%d')
            else:
                selected_date = self.date_var.get()
        except:
            selected_date = datetime.now().strftime('%Y-%m-%d')
        
        # Show loading
        for widget in self.timeslot_container.winfo_children():
            widget.destroy()
        
        loading_label = tk.Label(self.timeslot_container, text='Loading availability...', bg='white', fg='#1F2937', font=('Helvetica', 10))
        loading_label.pack(pady=20)
        
        def worker():
            try:
                resource_id = self.selected_resource.get('id')
                # Include date parameter in URL instead of params argument
                self.availability_data = self.api.get(f'resources/{resource_id}/availability?date={selected_date}') or {}
                
                self.after(0, self._render_timeslots)
            except Exception as e:
                error_msg = str(e)
                # Check if it's a 500/404 error indicating endpoint doesn't exist
                if '500' in error_msg or '404' in error_msg or 'No static resource' in error_msg:
                    # Gracefully handle missing endpoint - show all slots as available
                    print(f"[WARNING] Availability endpoint not implemented. Showing all time slots as available.")
                    self.availability_data = {'booked_slots': [], 'unavailable_slots': []}
                    self.after(0, self._render_timeslots)
                else:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to load availability: {error_msg}')
                        self._render_timeslots()  # Render with empty data
                    self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _render_timeslots(self):
        """Render time slot grid"""
        # Clear container
        for widget in self.timeslot_container.winfo_children():
            widget.destroy()
        
        # Reset selection
        self.selected_start_slot = None
        self.selected_end_slot = None
        self.selection_frame.pack_forget()
        
        # Create grid
        grid = tk.Frame(self.timeslot_container, bg='white')
        grid.pack(fill='x')
        
        # Time slots from 8 AM to 6 PM (10 hours = 10 slots)
        hours = list(range(8, 19))  # 8 AM to 6 PM (18:00)
        booked_slots = self.availability_data.get('booked_slots', [])
        unavailable_slots = self.availability_data.get('unavailable_slots', [])
        
        # Create buttons for each hour
        row = 0
        col = 0
        max_cols = 5
        
        for hour in hours:
            time_str = f"{hour:02d}:00"
            slot_status = 'available'
            
            # Check if slot is booked or unavailable
            if time_str in booked_slots or any(time_str in str(slot) for slot in booked_slots):
                slot_status = 'booked'
            elif time_str in unavailable_slots or any(time_str in str(slot) for slot in unavailable_slots):
                slot_status = 'unavailable'
            
            # Determine color
            if slot_status == 'available':
                bg_color = self.colors.get('success', '#27AE60')
                fg_color = 'white'
                hover_color = '#229954'
            elif slot_status == 'booked':
                bg_color = self.colors.get('danger', '#E74C3C')
                fg_color = 'white'
                hover_color = bg_color
            else:
                bg_color = '#9CA3AF'
                fg_color = 'white'
                hover_color = bg_color
            
            # Create slot button using CanvasButton for macOS compatibility
            from utils.canvas_button import CanvasButton
            
            btn = CanvasButton(
                grid,
                text=f"{hour % 12 or 12} {('AM' if hour < 12 else 'PM')}\n{time_str}",
                command=lambda h=hour: self._select_timeslot(h) if slot_status == 'available' else None,
                width=110,
                height=65,
                bg_color=bg_color,
                fg_color=fg_color,
                hover_color=hover_color,
                font=('Helvetica', 9, 'bold'),
                canvas_bg='white'
            )
            
            if slot_status != 'available':
                btn.config(state='disabled')
            
            btn.grid(row=row, column=col, padx=4, pady=4)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Legend
        legend_frame = tk.Frame(self.timeslot_container, bg='white')
        legend_frame.pack(fill='x', pady=(12, 0))
        
        tk.Label(legend_frame, text='Legend:', bg='white', fg='#1F2937', font=('Helvetica', 9, 'bold')).pack(side='left', padx=(0, 12))
        
        self._add_legend_item(legend_frame, self.colors.get('success', '#27AE60'), 'Available')
        self._add_legend_item(legend_frame, self.colors.get('danger', '#E74C3C'), 'Booked')
        self._add_legend_item(legend_frame, '#9CA3AF', 'Unavailable')

    def _add_legend_item(self, parent, color, text):
        """Add legend item"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(side='left', padx=(0, 12))
        
        color_box = tk.Frame(frame, bg=color, width=20, height=20)
        color_box.pack(side='left', padx=(0, 4))
        color_box.pack_propagate(False)
        
        tk.Label(frame, text=text, bg='white', fg='#1F2937', font=('Helvetica', 9)).pack(side='left')

    def _select_timeslot(self, hour):
        """Handle time slot selection"""
        if self.selected_start_slot is None:
            # Select start time
            self.selected_start_slot = hour
            self.selected_end_slot = None
            self._update_selection_display()
        elif self.selected_end_slot is None:
            # Select end time
            if hour <= self.selected_start_slot:
                messagebox.showwarning('Invalid Selection', 'End time must be after start time.')
                return
            
            self.selected_end_slot = hour
            self._update_selection_display()
            self._check_overlapping_bookings()
        else:
            # Reset and start new selection
            self.selected_start_slot = hour
            self.selected_end_slot = None
            self.warning_frame.pack_forget()
            self._update_selection_display()

    def _update_selection_display(self):
        """Update the selection display"""
        if self.selected_start_slot is not None:
            start_str = f"{self.selected_start_slot % 12 or 12} {'AM' if self.selected_start_slot < 12 else 'PM'}"
            
            if self.selected_end_slot is not None:
                end_str = f"{self.selected_end_slot % 12 or 12} {'AM' if self.selected_end_slot < 12 else 'PM'}"
                duration = self.selected_end_slot - self.selected_start_slot
                self.selection_label.config(text=f"✓ Selected: {start_str} - {end_str} ({duration} hour{'s' if duration > 1 else ''})")
                self.selection_frame.pack(fill='x', pady=(12, 0))
            else:
                self.selection_label.config(text=f"Start time selected: {start_str}. Now select end time.")
                self.selection_frame.pack(fill='x', pady=(12, 0))
        else:
            self.selection_frame.pack_forget()

    def _check_overlapping_bookings(self):
        """Check for overlapping bookings"""
        if not (self.selected_start_slot and self.selected_end_slot):
            return
        
        # Check if any booked slots fall within selected range
        booked_slots = self.availability_data.get('booked_slots', [])
        overlapping = []
        
        for slot in booked_slots:
            try:
                # Parse slot time
                if isinstance(slot, str):
                    slot_hour = int(slot.split(':')[0])
                    if self.selected_start_slot <= slot_hour < self.selected_end_slot:
                        overlapping.append(slot)
            except:
                continue
        
        if overlapping:
            # Show warning
            for widget in self.warning_frame.winfo_children():
                widget.destroy()
            
            warning_content = tk.Frame(self.warning_frame, bg='#FEF3C7')
            warning_content.pack(padx=16, pady=12)
            
            tk.Label(warning_content, text='⚠️ Warning', bg='#FEF3C7', fg='#92400E', font=('Helvetica', 11, 'bold')).pack(anchor='w')
            tk.Label(warning_content, text=f'Some slots in your selection overlap with existing bookings. Please review the availability grid.', bg='#FEF3C7', fg='#92400E', font=('Helvetica', 9), wraplength=600).pack(anchor='w', pady=(4, 0))
            
            self.warning_frame.pack(fill='x', pady=(0, 20))

    def _validate_form(self):
        """Validate booking form"""
        if not self.selected_resource:
            messagebox.showerror('Validation Error', 'Please select a resource.')
            return False
        
        if not self.purpose_var.get().strip():
            messagebox.showerror('Validation Error', 'Please enter the purpose of booking.')
            return False
        
        if self.selected_start_slot is None or self.selected_end_slot is None:
            messagebox.showerror('Validation Error', 'Please select start and end time.')
            return False
        
        if not self.attendees_var.get().strip():
            messagebox.showerror('Validation Error', 'Please enter expected number of attendees.')
            return False
        
        try:
            attendees = int(self.attendees_var.get().strip())
            if attendees <= 0:
                messagebox.showerror('Validation Error', 'Number of attendees must be positive.')
                return False
            
            # Check capacity
            capacity = self.selected_resource.get('capacity', 0)
            if capacity and attendees > capacity:
                result = messagebox.askyesno('Capacity Warning', 
                                            f'Number of attendees ({attendees}) exceeds resource capacity ({capacity}).\n\nDo you want to continue anyway?')
                if not result:
                    return False
        except ValueError:
            messagebox.showerror('Validation Error', 'Please enter a valid number for attendees.')
            return False
        
        return True

    def _submit_booking(self):
        """Submit booking request"""
        if not self._validate_form():
            return
        
        # Show confirmation dialog
        self._show_confirmation_dialog()

    def _show_confirmation_dialog(self):
        """Show booking confirmation dialog"""
        # Get booking details
        try:
            if hasattr(self, 'date_picker'):
                booking_date = self.date_picker.get_date().strftime('%Y-%m-%d')
            else:
                booking_date = self.date_var.get()
        except:
            booking_date = datetime.now().strftime('%Y-%m-%d')
        
        start_time = f"{self.selected_start_slot:02d}:00"
        end_time = f"{self.selected_end_slot:02d}:00"
        duration = self.selected_end_slot - self.selected_start_slot
        
        # Create modal
        modal = tk.Toplevel(self)
        modal.title('Confirm Booking')
        modal.geometry('600x650')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (300)
        y = (modal.winfo_screenheight() // 2) - (325)
        modal.geometry(f'600x650+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=self.colors.get('secondary', '#3498DB'))
        header_content.pack(padx=20, pady=20)
        
        tk.Label(header_content, text='📋', bg=self.colors.get('secondary', '#3498DB'), font=('Helvetica', 36)).pack()
        tk.Label(header_content, text='Review Booking Details', bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=(8, 0))
        tk.Label(header_content, text='Please review your booking before submitting', bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 10)).pack(pady=(4, 0))
        
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
        
        # Booking details
        self._add_detail_row(details_frame, '🏢 Resource:', self.selected_resource.get('name', 'N/A'))
        self._add_detail_row(details_frame, '📋 Purpose:', self.purpose_var.get())
        self._add_detail_row(details_frame, '📅 Date:', booking_date)
        self._add_detail_row(details_frame, '🕐 Time:', f"{start_time} - {end_time}")
        self._add_detail_row(details_frame, '⏱️ Duration:', f"{duration} hour{'s' if duration > 1 else ''}")
        self._add_detail_row(details_frame, '👥 Attendees:', self.attendees_var.get())
        
        requirements = self.requirements_var.get().strip()
        if requirements:
            self._add_detail_row(details_frame, '📝 Requirements:', requirements, multiline=True)
        
        priority_text = 'Normal Priority' if self.priority_var.get() == 'normal' else 'Urgent Priority'
        priority_icon = '⚪' if self.priority_var.get() == 'normal' else '🔴'
        self._add_detail_row(details_frame, f'{priority_icon} Priority:', priority_text)
        
        # Approval info
        tk.Frame(details_frame, bg='#E5E7EB', height=1).pack(fill='x', pady=16)
        
        approval_frame = tk.Frame(details_frame, bg='#F0F9FF', highlightthickness=1, highlightbackground='#BFDBFE')
        approval_frame.pack(fill='x', pady=(0, 16))
        
        approval_content = tk.Frame(approval_frame, bg='#F0F9FF')
        approval_content.pack(padx=16, pady=12)
        
        tk.Label(approval_content, text='ℹ️ Approval Information', bg='#F0F9FF', fg='#1E40AF', font=('Helvetica', 11, 'bold')).pack(anchor='w')
        
        if self.priority_var.get() == 'urgent':
            approval_text = 'Your booking request will be processed within 24 hours.'
        else:
            approval_text = 'Your booking request will be reviewed by an administrator within 2-3 business days.'
        
        tk.Label(approval_content, text=approval_text, bg='#F0F9FF', fg='#1E40AF', font=('Helvetica', 9), wraplength=520).pack(anchor='w', pady=(4, 0))
        tk.Label(approval_content, text='You will receive a notification once your request is approved or rejected.', bg='#F0F9FF', fg='#1E40AF', font=('Helvetica', 9), wraplength=520).pack(anchor='w', pady=(4, 0))
        
        # Action buttons
        btn_frame = tk.Frame(details_frame, bg='white')
        btn_frame.pack(fill='x', pady=(16, 0))
        
        cancel_btn = create_secondary_button(btn_frame, text='Cancel', command=modal.destroy)
        cancel_btn.pack(side='left', padx=5)
        
        confirm_btn = create_success_button(btn_frame, text='Confirm & Submit', command=lambda: self._confirm_booking(modal, booking_date, start_time, end_time))
        confirm_btn.pack(side='right', padx=5)

    def _add_detail_row(self, parent, label, value, multiline=False):
        """Add detail row to confirmation"""
        row = tk.Frame(parent, bg='white')
        row.pack(fill='x', pady=6)
        
        tk.Label(row, text=label, bg='white', fg='#1F2937', font=('Helvetica', 10), width=15, anchor='w').pack(side='left')
        
        if multiline:
            tk.Label(row, text=value, bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold'), wraplength=400, justify='left').pack(side='left', fill='x', expand=True)
        else:
            tk.Label(row, text=value, bg='white', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(side='left')

    def _confirm_booking(self, modal, booking_date, start_time, end_time):
        """Confirm and submit booking"""
        modal.destroy()
        
        # Get current user ID
        user = self.session.get_user()
        if not user or 'id' not in user:
            messagebox.showerror('Error', 'User session not found. Please login again.')
            return
        
        # Convert date + time to ISO-8601 datetime format (YYYY-MM-DDTHH:MM:SS)
        start_datetime_str = f"{booking_date}T{start_time}:00"
        end_datetime_str = f"{booking_date}T{end_time}:00"
        
        # Prepare booking data matching backend BookingRequest format
        booking_data = {
            'userId': user['id'],
            'resourceId': self.selected_resource.get('id'),
            'startTime': start_datetime_str,
            'endTime': end_datetime_str,
            'eventId': None  # Optional field for event-related bookings
        }
        
        # Show loading
        loading = tk.Toplevel(self)
        loading.title('Submitting...')
        loading.geometry('300x100')
        loading.configure(bg='white')
        loading.transient(self.winfo_toplevel())
        loading.grab_set()
        
        tk.Label(loading, text='Submitting your booking request...', bg='white', fg='#1F2937', font=('Helvetica', 11)).pack(pady=10)
        progress = ttk.Progressbar(loading, mode='indeterminate', length=250)
        progress.pack(pady=10)
        progress.start(10)
        
        # Center loading dialog
        loading.update_idletasks()
        x = (loading.winfo_screenwidth() // 2) - 150
        y = (loading.winfo_screenheight() // 2) - 50
        loading.geometry(f'300x100+{x}+{y}')
        
        def worker():
            try:
                response = self.api.post('bookings', booking_data)
                
                def show_success():
                    loading.destroy()
                    messagebox.showinfo('Success', 
                                      'Your booking request has been submitted successfully!\n\n'
                                      'You will receive a notification once it is reviewed by an administrator.')
                    self._reset_form()
                
                self.after(0, show_success)
            except Exception as e:
                def show_error():
                    loading.destroy()
                    messagebox.showerror('Error', f'Failed to submit booking: {str(e)}')
                
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _reset_form(self):
        """Reset the booking form"""
        self.resource_var.set('')
        self.purpose_var.set('')
        self.attendees_var.set('')
        self.requirements_var.set('')
        self.priority_var.set('normal')
        self.selected_resource = None
        self.selected_start_slot = None
        self.selected_end_slot = None
        self.availability_data = {}
        
        self.resource_info_frame.pack_forget()
        self.selection_frame.pack_forget()
        self.warning_frame.pack_forget()
        
        for widget in self.timeslot_container.winfo_children():
            widget.destroy()

    def _cancel(self):
        """Cancel booking"""
        result = messagebox.askyesno('Cancel Booking', 
                                     'Are you sure you want to cancel? All entered information will be lost.')
        if result:
            self._reset_form()
