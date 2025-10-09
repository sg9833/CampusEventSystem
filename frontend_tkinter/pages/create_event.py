import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading

from utils.api_client import APIClient
from utils.session_manager import SessionManager


class CreateEventPage(tk.Frame):
    """Multi-step event creation wizard for organizers."""

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
        
        # Form state
        self.current_step = 1
        self.total_steps = 3
        
        # Form data
        self.form_data = {
            # Step 1
            'title': tk.StringVar(),
            'category': tk.StringVar(value='Technical'),
            'description': None,  # Text widget
            'event_type': tk.StringVar(value='Offline'),
            
            # Step 2
            'event_date': tk.StringVar(),
            'start_time': tk.StringVar(),
            'end_time': tk.StringVar(),
            'venue': tk.StringVar(),
            'meeting_link': tk.StringVar(),
            'expected_attendees': tk.StringVar(),
            'registration_deadline': tk.StringVar(),
            
            # Step 3
            'resources': {},  # Dictionary of checkboxes
            'additional_requirements': None  # Text widget
        }
        
        # Layout
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Progress
        self.grid_rowconfigure(2, weight=1)  # Content
        self.grid_rowconfigure(3, weight=0)  # Navigation
        self.grid_columnconfigure(0, weight=1)
        
        self._build_header()
        self._build_progress_bar()
        self._build_content_area()
        self._build_navigation()
        
        # Show first step
        self._show_step(1)

    def _build_header(self):
        """Build header section"""
        header = tk.Frame(self, bg='white', height=80, highlightthickness=1, highlightbackground='#E5E7EB')
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)
        
        container = tk.Frame(header, bg='white')
        container.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Title
        tk.Label(container, text='Create New Event', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(side='left')
        
        # Save draft button
        tk.Button(container, text='💾 Save as Draft', command=self._save_draft, bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 10), padx=16, pady=8).pack(side='right')

    def _build_progress_bar(self):
        """Build progress indicator"""
        self.progress_frame = tk.Frame(self, bg=self.colors.get('background', '#ECF0F1'))
        self.progress_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=(20, 0))
        
        # This will be populated when showing steps

    def _update_progress_bar(self):
        """Update the progress bar based on current step"""
        # Clear existing progress
        for widget in self.progress_frame.winfo_children():
            widget.destroy()
        
        steps = [
            ('1', 'Basic Details'),
            ('2', 'Schedule & Venue'),
            ('3', 'Resources & Review')
        ]
        
        container = tk.Frame(self.progress_frame, bg=self.colors.get('background', '#ECF0F1'))
        container.pack()
        
        for i, (num, label) in enumerate(steps, 1):
            # Step circle
            if i < self.current_step:
                # Completed step
                circle_bg = self.colors.get('success', '#27AE60')
                circle_text = '✓'
                label_color = self.colors.get('success', '#27AE60')
            elif i == self.current_step:
                # Current step
                circle_bg = self.colors.get('secondary', '#3498DB')
                circle_text = num
                label_color = self.colors.get('secondary', '#3498DB')
            else:
                # Upcoming step
                circle_bg = '#D1D5DB'
                circle_text = num
                label_color = '#9CA3AF'
            
            step_frame = tk.Frame(container, bg=self.colors.get('background', '#ECF0F1'))
            step_frame.pack(side='left')
            
            # Circle
            circle = tk.Label(step_frame, text=circle_text, bg=circle_bg, fg='white', font=('Helvetica', 14, 'bold'), width=3, height=1)
            circle.pack()
            
            # Label
            tk.Label(step_frame, text=label, bg=self.colors.get('background', '#ECF0F1'), fg=label_color, font=('Helvetica', 10, 'bold')).pack(pady=(4, 0))
            
            # Connector line (except for last step)
            if i < len(steps):
                line_color = self.colors.get('success', '#27AE60') if i < self.current_step else '#D1D5DB'
                line = tk.Frame(container, bg=line_color, width=100, height=3)
                line.pack(side='left', padx=8)

    def _build_content_area(self):
        """Build scrollable content area"""
        # Content container with scrollbar
        content_container = tk.Frame(self, bg=self.colors.get('background', '#ECF0F1'))
        content_container.grid(row=2, column=0, sticky='nsew', padx=30, pady=20)
        
        canvas = tk.Canvas(content_container, bg=self.colors.get('background', '#ECF0F1'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient='vertical', command=canvas.yview)
        
        self.content = tk.Frame(canvas, bg='white')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=self.content, anchor='nw', width=canvas.winfo_width())
        self.content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Update canvas width on resize
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag('all')[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

    def _build_navigation(self):
        """Build navigation buttons"""
        self.nav_frame = tk.Frame(self, bg='white', height=80, highlightthickness=1, highlightbackground='#E5E7EB')
        self.nav_frame.grid(row=3, column=0, sticky='ew')
        self.nav_frame.grid_propagate(False)
        
        container = tk.Frame(self.nav_frame, bg='white')
        container.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Previous button
        self.prev_btn = tk.Button(container, text='← Previous', command=self._prev_step, bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 11), padx=24, pady=10)
        self.prev_btn.pack(side='left')
        
        # Cancel button
        tk.Button(container, text='Cancel', command=self._cancel, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 11), padx=24, pady=10).pack(side='left', padx=(12, 0))
        
        # Next/Submit button
        self.next_btn = tk.Button(container, text='Next →', command=self._next_step, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=24, pady=10)
        self.next_btn.pack(side='right')

    def _show_step(self, step):
        """Show the specified step"""
        self.current_step = step
        self._update_progress_bar()
        self._clear_content()
        
        if step == 1:
            self._render_step1()
        elif step == 2:
            self._render_step2()
        elif step == 3:
            self._render_step3()
        
        # Update navigation buttons
        self.prev_btn.config(state='normal' if step > 1 else 'disabled')
        
        if step == self.total_steps:
            self.next_btn.config(text='Submit for Approval', bg=self.colors.get('success', '#27AE60'))
        else:
            self.next_btn.config(text='Next →', bg=self.colors.get('secondary', '#3498DB'))

    def _clear_content(self):
        """Clear content area"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def _render_step1(self):
        """Render Step 1: Basic Details"""
        container = tk.Frame(self.content, bg='white')
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        tk.Label(container, text='Step 1: Basic Details', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 16, 'bold')).pack(anchor='w', pady=(0, 20))
        
        # Event name
        self._create_label(container, 'Event Name *', 'Required')
        entry = tk.Entry(container, textvariable=self.form_data['title'], font=('Helvetica', 11), width=60)
        entry.pack(anchor='w', pady=(0, 16), ipady=6)
        
        # Category
        self._create_label(container, 'Category *', 'Select event category')
        categories = ['Technical', 'Cultural', 'Sports', 'Workshop', 'Seminar', 'Academic', 'Social', 'Competition', 'Other']
        category_dropdown = ttk.Combobox(container, textvariable=self.form_data['category'], values=categories, state='readonly', font=('Helvetica', 11), width=58)
        category_dropdown.pack(anchor='w', pady=(0, 16), ipady=6)
        
        # Event type
        self._create_label(container, 'Event Type *', 'Online or Offline event')
        type_frame = tk.Frame(container, bg='white')
        type_frame.pack(anchor='w', pady=(0, 16))
        
        tk.Radiobutton(type_frame, text='Offline (In-person)', variable=self.form_data['event_type'], value='Offline', bg='white', font=('Helvetica', 11), selectcolor='white').pack(side='left', padx=(0, 20))
        tk.Radiobutton(type_frame, text='Online (Virtual)', variable=self.form_data['event_type'], value='Online', bg='white', font=('Helvetica', 11), selectcolor='white').pack(side='left')
        
        # Description
        self._create_label(container, 'Description *', 'Provide detailed event description')
        desc_frame = tk.Frame(container, bg='white', highlightthickness=1, highlightbackground='#D1D5DB')
        desc_frame.pack(anchor='w', pady=(0, 16))
        
        desc_scroll = ttk.Scrollbar(desc_frame, orient='vertical')
        desc_text = tk.Text(desc_frame, height=8, width=58, font=('Helvetica', 11), yscrollcommand=desc_scroll.set, wrap='word')
        desc_scroll.config(command=desc_text.yview)
        desc_scroll.pack(side='right', fill='y')
        desc_text.pack(side='left', fill='both', expand=True)
        
        # Restore previous content if exists
        if self.form_data['description'] and hasattr(self.form_data['description'], 'get'):
            try:
                desc_text.insert('1.0', self.form_data['description'].get('1.0', 'end-1c'))
            except:
                pass
        
        self.form_data['description'] = desc_text

    def _render_step2(self):
        """Render Step 2: Schedule & Venue"""
        container = tk.Frame(self.content, bg='white')
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        tk.Label(container, text='Step 2: Schedule & Venue', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 16, 'bold')).pack(anchor='w', pady=(0, 20))
        
        # Two-column layout
        columns = tk.Frame(container, bg='white')
        columns.pack(fill='x', pady=(0, 16))
        columns.grid_columnconfigure(0, weight=1)
        columns.grid_columnconfigure(1, weight=1)
        
        # Left column
        left = tk.Frame(columns, bg='white')
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 16))
        
        # Event date
        self._create_label(left, 'Event Date *', 'Format: YYYY-MM-DD (must be future date)')
        date_entry = tk.Entry(left, textvariable=self.form_data['event_date'], font=('Helvetica', 11), width=25)
        date_entry.pack(anchor='w', pady=(0, 16), ipady=6)
        
        # Suggest today's date + 7 days as placeholder
        if not self.form_data['event_date'].get():
            suggested_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            date_entry.insert(0, suggested_date)
        
        # Start time
        self._create_label(left, 'Start Time *', 'Format: HH:MM (24-hour)')
        start_entry = tk.Entry(left, textvariable=self.form_data['start_time'], font=('Helvetica', 11), width=25)
        start_entry.pack(anchor='w', pady=(0, 16), ipady=6)
        if not self.form_data['start_time'].get():
            start_entry.insert(0, '09:00')
        
        # End time
        self._create_label(left, 'End Time *', 'Format: HH:MM (24-hour)')
        end_entry = tk.Entry(left, textvariable=self.form_data['end_time'], font=('Helvetica', 11), width=25)
        end_entry.pack(anchor='w', pady=(0, 16), ipady=6)
        if not self.form_data['end_time'].get():
            end_entry.insert(0, '17:00')
        
        # Right column
        right = tk.Frame(columns, bg='white')
        right.grid(row=0, column=1, sticky='nsew', padx=(16, 0))
        
        # Expected attendees
        self._create_label(right, 'Expected Attendees', 'Estimated number of participants')
        attendees_entry = tk.Entry(right, textvariable=self.form_data['expected_attendees'], font=('Helvetica', 11), width=25)
        attendees_entry.pack(anchor='w', pady=(0, 16), ipady=6)
        
        # Registration deadline
        self._create_label(right, 'Registration Deadline', 'Format: YYYY-MM-DD HH:MM')
        deadline_entry = tk.Entry(right, textvariable=self.form_data['registration_deadline'], font=('Helvetica', 11), width=25)
        deadline_entry.pack(anchor='w', pady=(0, 16), ipady=6)
        
        # Conditional fields based on event type
        event_type = self.form_data['event_type'].get()
        
        if event_type == 'Offline':
            # Venue
            self._create_label(container, 'Venue/Location *', 'Physical location for the event')
            venue_entry = tk.Entry(container, textvariable=self.form_data['venue'], font=('Helvetica', 11), width=60)
            venue_entry.pack(anchor='w', pady=(0, 16), ipady=6)
        else:
            # Meeting link
            self._create_label(container, 'Meeting Link *', 'Online meeting URL (Zoom, Teams, etc.)')
            link_entry = tk.Entry(container, textvariable=self.form_data['meeting_link'], font=('Helvetica', 11), width=60)
            link_entry.pack(anchor='w', pady=(0, 16), ipady=6)
        
        # Help text
        help_frame = tk.Frame(container, bg='#EFF6FF', highlightthickness=1, highlightbackground='#BFDBFE')
        help_frame.pack(fill='x', pady=(8, 0))
        tk.Label(help_frame, text='💡 Tip: Make sure event date is in the future and times are in 24-hour format', bg='#EFF6FF', fg='#1E40AF', font=('Helvetica', 10)).pack(padx=12, pady=10, anchor='w')

    def _render_step3(self):
        """Render Step 3: Resources & Review"""
        container = tk.Frame(self.content, bg='white')
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        tk.Label(container, text='Step 3: Resource Requirements & Review', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 16, 'bold')).pack(anchor='w', pady=(0, 20))
        
        # Resource requirements
        self._create_label(container, 'Resource Requirements', 'Select resources needed for your event')
        
        resources_frame = tk.Frame(container, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        resources_frame.pack(fill='x', pady=(0, 16))
        
        resources_grid = tk.Frame(resources_frame, bg='#F9FAFB')
        resources_grid.pack(padx=20, pady=16)
        
        # Resource options
        resource_options = [
            ('projector', '📽️ Projector'),
            ('audio_system', '🔊 Audio System'),
            ('microphone', '🎤 Microphone'),
            ('computers', '💻 Computers'),
            ('whiteboard', '📝 Whiteboard'),
            ('chairs', '🪑 Extra Chairs'),
            ('tables', '🪑 Tables'),
            ('camera', '📷 Camera/Recording Equipment'),
            ('screen', '🖥️ Display Screen'),
            ('wifi', '📡 WiFi/Internet'),
            ('room', '🚪 Specific Room/Lab'),
            ('other', '➕ Other Resources')
        ]
        
        # Create checkboxes in 3 columns
        for i, (key, label) in enumerate(resource_options):
            row = i // 3
            col = i % 3
            
            var = tk.BooleanVar()
            self.form_data['resources'][key] = var
            
            cb = tk.Checkbutton(resources_grid, text=label, variable=var, bg='#F9FAFB', font=('Helvetica', 10), selectcolor='white')
            cb.grid(row=row, column=col, sticky='w', padx=10, pady=6)
        
        # Additional requirements
        self._create_label(container, 'Additional Requirements', 'Specify any other requirements or special arrangements')
        
        req_frame = tk.Frame(container, bg='white', highlightthickness=1, highlightbackground='#D1D5DB')
        req_frame.pack(anchor='w', pady=(0, 20))
        
        req_scroll = ttk.Scrollbar(req_frame, orient='vertical')
        req_text = tk.Text(req_frame, height=6, width=75, font=('Helvetica', 11), yscrollcommand=req_scroll.set, wrap='word')
        req_scroll.config(command=req_text.yview)
        req_scroll.pack(side='right', fill='y')
        req_text.pack(side='left', fill='both', expand=True)
        
        # Restore previous content if exists
        if self.form_data['additional_requirements'] and hasattr(self.form_data['additional_requirements'], 'get'):
            try:
                req_text.insert('1.0', self.form_data['additional_requirements'].get('1.0', 'end-1c'))
            except:
                pass
        
        self.form_data['additional_requirements'] = req_text
        
        # Review section
        review_label = tk.Label(container, text='Review Your Event', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 14, 'bold'))
        review_label.pack(anchor='w', pady=(20, 12))
        
        review_frame = tk.Frame(container, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        review_frame.pack(fill='x', pady=(0, 16))
        
        review_content = tk.Frame(review_frame, bg='#F9FAFB')
        review_content.pack(padx=20, pady=16, fill='x')
        
        # Display summary
        self._add_review_item(review_content, 'Event Name:', self.form_data['title'].get() or 'Not specified')
        self._add_review_item(review_content, 'Category:', self.form_data['category'].get())
        self._add_review_item(review_content, 'Event Type:', self.form_data['event_type'].get())
        
        date = self.form_data['event_date'].get()
        start = self.form_data['start_time'].get()
        end = self.form_data['end_time'].get()
        self._add_review_item(review_content, 'Schedule:', f"{date} | {start} - {end}" if all([date, start, end]) else 'Not specified')
        
        if self.form_data['event_type'].get() == 'Offline':
            self._add_review_item(review_content, 'Venue:', self.form_data['venue'].get() or 'Not specified')
        else:
            self._add_review_item(review_content, 'Meeting Link:', self.form_data['meeting_link'].get() or 'Not specified')
        
        attendees = self.form_data['expected_attendees'].get()
        self._add_review_item(review_content, 'Expected Attendees:', attendees if attendees else 'Not specified')
        
        # Selected resources
        selected_resources = [label for key, label in resource_options if self.form_data['resources'].get(key) and self.form_data['resources'][key].get()]
        if selected_resources:
            self._add_review_item(review_content, 'Resources:', ', '.join([r.split(' ', 1)[1] for r in selected_resources]))
        
        # Warning message
        warning_frame = tk.Frame(container, bg='#FEF3C7', highlightthickness=1, highlightbackground='#FCD34D')
        warning_frame.pack(fill='x', pady=(8, 0))
        tk.Label(warning_frame, text='⚠️ Your event will be submitted for admin approval. You will be notified once it is reviewed.', bg='#FEF3C7', fg='#92400E', font=('Helvetica', 10, 'bold')).pack(padx=12, pady=12)

    def _create_label(self, parent, text, hint=''):
        """Create a form label with optional hint"""
        label_frame = tk.Frame(parent, bg='white')
        label_frame.pack(anchor='w', pady=(0, 4))
        
        tk.Label(label_frame, text=text, bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(side='left')
        
        if hint:
            tk.Label(label_frame, text=f'  ({hint})', bg='white', fg='#9CA3AF', font=('Helvetica', 9)).pack(side='left')

    def _add_review_item(self, parent, label, value):
        """Add a review item"""
        item_frame = tk.Frame(parent, bg='#F9FAFB')
        item_frame.pack(fill='x', pady=4)
        
        tk.Label(item_frame, text=label, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 10)).pack(side='left', anchor='w', padx=(0, 8))
        tk.Label(item_frame, text=value, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(side='left', anchor='w')

    def _prev_step(self):
        """Go to previous step"""
        if self.current_step > 1:
            self._show_step(self.current_step - 1)

    def _next_step(self):
        """Go to next step or submit"""
        if self.current_step < self.total_steps:
            # Validate current step
            if self._validate_step(self.current_step):
                self._show_step(self.current_step + 1)
        else:
            # Final step - submit
            self._submit_event()

    def _validate_step(self, step):
        """Validate current step"""
        if step == 1:
            # Validate basic details
            if not self.form_data['title'].get().strip():
                messagebox.showerror('Validation Error', 'Event name is required')
                return False
            
            if not self.form_data['description'] or not self.form_data['description'].get('1.0', 'end-1c').strip():
                messagebox.showerror('Validation Error', 'Event description is required')
                return False
            
            return True
            
        elif step == 2:
            # Validate schedule and venue
            date = self.form_data['event_date'].get().strip()
            start_time = self.form_data['start_time'].get().strip()
            end_time = self.form_data['end_time'].get().strip()
            
            if not date:
                messagebox.showerror('Validation Error', 'Event date is required')
                return False
            
            # Validate date format
            try:
                event_date = datetime.strptime(date, '%Y-%m-%d')
                if event_date.date() < datetime.now().date():
                    messagebox.showerror('Validation Error', 'Event date must be in the future')
                    return False
            except ValueError:
                messagebox.showerror('Validation Error', 'Invalid date format. Use YYYY-MM-DD')
                return False
            
            if not start_time or not end_time:
                messagebox.showerror('Validation Error', 'Start time and end time are required')
                return False
            
            # Validate time format
            try:
                datetime.strptime(start_time, '%H:%M')
                datetime.strptime(end_time, '%H:%M')
            except ValueError:
                messagebox.showerror('Validation Error', 'Invalid time format. Use HH:MM (24-hour)')
                return False
            
            # Check venue or meeting link based on type
            if self.form_data['event_type'].get() == 'Offline':
                if not self.form_data['venue'].get().strip():
                    messagebox.showerror('Validation Error', 'Venue is required for offline events')
                    return False
            else:
                if not self.form_data['meeting_link'].get().strip():
                    messagebox.showerror('Validation Error', 'Meeting link is required for online events')
                    return False
            
            return True
        
        return True

    def _save_draft(self):
        """Save event as draft"""
        if not messagebox.askyesno('Save Draft', 'Save this event as a draft? You can complete it later.'):
            return
        
        try:
            payload = self._build_payload()
            payload['status'] = 'DRAFT'
            
            response = self.api.post('events/draft', payload)
            messagebox.showinfo('Success', 'Event saved as draft successfully!')
            self._reset_form()
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save draft: {str(e)}')

    def _submit_event(self):
        """Submit event for approval"""
        # Final validation
        if not self._validate_step(1) or not self._validate_step(2):
            messagebox.showerror('Validation Error', 'Please complete all required fields')
            return
        
        # Confirm submission
        if not messagebox.askyesno('Confirm Submission', 
                                   'Submit this event for admin approval?\n\nYou will be notified once it is reviewed.'):
            return
        
        try:
            payload = self._build_payload()
            
            # Submit to API
            response = self.api.post('events', payload)
            
            messagebox.showinfo('Success', 
                              'Event submitted successfully!\n\n'
                              'Your event is now pending admin approval. '
                              'You will be notified once it is reviewed.')
            
            # Reset form
            self._reset_form()
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to submit event: {str(e)}')

    def _build_payload(self):
        """Build API payload from form data"""
        # Combine date and times
        date = self.form_data['event_date'].get().strip()
        start_time = self.form_data['start_time'].get().strip()
        end_time = self.form_data['end_time'].get().strip()
        
        start_datetime = f"{date} {start_time}:00"
        end_datetime = f"{date} {end_time}:00"
        
        payload = {
            'title': self.form_data['title'].get().strip(),
            'category': self.form_data['category'].get(),
            'description': self.form_data['description'].get('1.0', 'end-1c').strip(),
            'event_type': self.form_data['event_type'].get(),
            'start_time': start_datetime,
            'end_time': end_datetime,
        }
        
        # Add venue or meeting link
        if self.form_data['event_type'].get() == 'Offline':
            payload['venue'] = self.form_data['venue'].get().strip()
        else:
            payload['meeting_link'] = self.form_data['meeting_link'].get().strip()
            payload['venue'] = 'Online'  # Backend might require venue field
        
        # Optional fields
        if self.form_data['expected_attendees'].get().strip():
            try:
                payload['capacity'] = int(self.form_data['expected_attendees'].get().strip())
            except ValueError:
                pass
        
        if self.form_data['registration_deadline'].get().strip():
            payload['registration_deadline'] = self.form_data['registration_deadline'].get().strip()
        
        # Resources
        selected_resources = []
        for key, var in self.form_data['resources'].items():
            if var.get():
                selected_resources.append(key)
        
        if selected_resources:
            payload['resources'] = selected_resources
        
        # Additional requirements
        additional = self.form_data['additional_requirements'].get('1.0', 'end-1c').strip()
        if additional:
            payload['additional_requirements'] = additional
        
        return payload

    def _reset_form(self):
        """Reset form to initial state"""
        # Clear string variables
        self.form_data['title'].set('')
        self.form_data['category'].set('Technical')
        self.form_data['event_type'].set('Offline')
        self.form_data['event_date'].set('')
        self.form_data['start_time'].set('')
        self.form_data['end_time'].set('')
        self.form_data['venue'].set('')
        self.form_data['meeting_link'].set('')
        self.form_data['expected_attendees'].set('')
        self.form_data['registration_deadline'].set('')
        
        # Clear text widgets
        if self.form_data['description'] and hasattr(self.form_data['description'], 'delete'):
            self.form_data['description'].delete('1.0', 'end')
        
        if self.form_data['additional_requirements'] and hasattr(self.form_data['additional_requirements'], 'delete'):
            self.form_data['additional_requirements'].delete('1.0', 'end')
        
        # Clear resources
        self.form_data['resources'] = {}
        
        # Go back to step 1
        self._show_step(1)

    def _cancel(self):
        """Cancel event creation"""
        if messagebox.askyesno('Cancel', 'Are you sure you want to cancel? All unsaved changes will be lost.'):
            self._reset_form()
            # Navigate back to dashboard if controller has navigation
            if hasattr(self.controller, 'show_page'):
                self.controller.show_page('OrganizerDashboard')
