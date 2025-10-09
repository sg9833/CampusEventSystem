import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime

from utils.api_client import APIClient
from utils.session_manager import SessionManager


class ManageResourcesPage(tk.Frame):
    """Admin page for managing resources."""

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
        self.all_resources = []
        self.filtered_resources = []
        self.search_var = tk.StringVar()
        self.filter_type = tk.StringVar(value='all')
        self.filter_status = tk.StringVar(value='all')
        
        # Bind search
        self.search_var.trace('w', lambda *args: self._apply_filters())
        
        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_resources()

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
        tk.Label(title_frame, text='🏢 Manage Resources', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Add, edit, and manage campus resources', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(header_content, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text='🔄 Refresh', command=self._load_resources, bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        tk.Button(btn_frame, text='➕ Add New Resource', command=self._show_add_resource_form, bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=16, pady=8).pack(side='left')
        
        # Filters and search
        filters_frame = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        filters_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=(20, 0))
        
        filters_content = tk.Frame(filters_frame, bg='white')
        filters_content.pack(fill='x', padx=20, pady=12)
        
        # Search
        tk.Label(filters_content, text='🔍', bg='white', font=('Helvetica', 14)).pack(side='left', padx=(0, 4))
        search_entry = tk.Entry(filters_content, textvariable=self.search_var, font=('Helvetica', 11), width=30)
        search_entry.pack(side='left', padx=(0, 20))
        
        # Type filter
        tk.Label(filters_content, text='Type:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='left', padx=(0, 6))
        type_dropdown = ttk.Combobox(filters_content, textvariable=self.filter_type, state='readonly', width=15, font=('Helvetica', 10))
        type_dropdown['values'] = ('all', 'classroom', 'lab', 'auditorium', 'equipment', 'conference', 'sports')
        type_dropdown.pack(side='left', padx=(0, 20))
        type_dropdown.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
        
        # Status filter
        tk.Label(filters_content, text='Status:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='left', padx=(0, 6))
        status_dropdown = ttk.Combobox(filters_content, textvariable=self.filter_status, state='readonly', width=15, font=('Helvetica', 10))
        status_dropdown['values'] = ('all', 'active', 'maintenance')
        status_dropdown.pack(side='left', padx=(0, 20))
        status_dropdown.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
        
        # Clear filters
        tk.Button(filters_content, text='Clear Filters', command=self._clear_filters, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 9), padx=12, pady=6).pack(side='left')
        
        # Table container
        table_container = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        table_container.grid(row=2, column=0, sticky='nsew', padx=30, pady=(12, 20))
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Create Treeview with scrollbar
        tree_frame = tk.Frame(table_container, bg='white')
        tree_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient='vertical')
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        # Treeview
        columns = ('ID', 'Name', 'Type', 'Capacity', 'Location', 'Amenities', 'Status')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=15)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Resource Name')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Capacity', text='Capacity')
        self.tree.heading('Location', text='Location')
        self.tree.heading('Amenities', text='Amenities')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('ID', width=60, anchor='center')
        self.tree.column('Name', width=200, anchor='w')
        self.tree.column('Type', width=120, anchor='center')
        self.tree.column('Capacity', width=80, anchor='center')
        self.tree.column('Location', width=150, anchor='w')
        self.tree.column('Amenities', width=250, anchor='w')
        self.tree.column('Status', width=100, anchor='center')
        
        # Pack scrollbars and tree
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.tree.pack(side='left', fill='both', expand=True)
        
        # Context menu on right-click
        self.tree.bind('<Button-2>', self._show_context_menu)  # Right-click on Mac
        self.tree.bind('<Button-3>', self._show_context_menu)  # Right-click on Windows/Linux
        self.tree.bind('<Double-Button-1>', lambda e: self._edit_resource())  # Double-click to edit
        
        # Action buttons below table
        action_frame = tk.Frame(table_container, bg='white')
        action_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        
        tk.Button(action_frame, text='View Details', command=self._view_resource_details, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        tk.Button(action_frame, text='Edit Resource', command=self._edit_resource, bg=self.colors.get('warning', '#F39C12'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        tk.Button(action_frame, text='View Bookings', command=self._view_bookings, bg='#6B7280', fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        tk.Button(action_frame, text='Toggle Maintenance', command=self._toggle_maintenance, bg=self.colors.get('warning', '#F39C12'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        tk.Button(action_frame, text='Delete Resource', command=self._delete_resource, bg=self.colors.get('danger', '#E74C3C'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left')

    def _load_resources(self):
        """Load resources from API"""
        def worker():
            try:
                self.all_resources = self.api.get('resources') or []
                self.after(0, self._apply_filters)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load resources: {str(e)}')
                    self.all_resources = []
                    self._apply_filters()
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _apply_filters(self):
        """Apply search and filters to resource list"""
        search_query = self.search_var.get().lower().strip()
        resource_type = self.filter_type.get()
        status = self.filter_status.get()
        
        # Filter resources
        filtered = self.all_resources.copy()
        
        # Search filter
        if search_query:
            filtered = [r for r in filtered if 
                       search_query in (r.get('name', '') or '').lower() or
                       search_query in (r.get('code', '') or '').lower() or
                       search_query in (r.get('type', '') or '').lower() or
                       search_query in (r.get('location', '') or '').lower()]
        
        # Type filter
        if resource_type != 'all':
            filtered = [r for r in filtered if (r.get('type', '') or '').lower() == resource_type]
        
        # Status filter
        if status != 'all':
            filtered = [r for r in filtered if (r.get('status', 'active') or 'active').lower() == status]
        
        self.filtered_resources = filtered
        self._render_table()

    def _render_table(self):
        """Render resources in table"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered resources
        for resource in self.filtered_resources:
            resource_id = resource.get('id', 'N/A')
            name = resource.get('name', 'Unknown')
            resource_type = (resource.get('type', 'N/A') or 'N/A').title()
            capacity = resource.get('capacity', 'N/A')
            location = resource.get('location', resource.get('building', 'N/A'))
            amenities = ', '.join([str(a) for a in (resource.get('amenities', []) or [])][:3])
            if len(resource.get('amenities', [])) > 3:
                amenities += f" (+{len(resource.get('amenities', [])) - 3})"
            status = (resource.get('status', 'active') or 'active').title()
            
            # Add tag based on status for styling
            tags = ('active',) if status.lower() == 'active' else ('maintenance',)
            
            self.tree.insert('', 'end', values=(resource_id, name, resource_type, capacity, location, amenities, status), tags=tags)
        
        # Configure tag colors
        self.tree.tag_configure('active', background='#F0FDF4')
        self.tree.tag_configure('maintenance', background='#FEF3C7')

    def _clear_filters(self):
        """Clear all filters"""
        self.search_var.set('')
        self.filter_type.set('all')
        self.filter_status.set('all')
        self._apply_filters()

    def _get_selected_resource(self):
        """Get selected resource from table"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning('No Selection', 'Please select a resource from the table.')
            return None
        
        # Get resource ID from first column
        item = self.tree.item(selection[0])
        resource_id = item['values'][0]
        
        # Find resource in filtered list
        for resource in self.filtered_resources:
            if str(resource.get('id')) == str(resource_id):
                return resource
        
        return None

    def _show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select row under mouse
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            
            # Create context menu
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label='View Details', command=self._view_resource_details)
            menu.add_command(label='Edit Resource', command=self._edit_resource)
            menu.add_command(label='View Bookings', command=self._view_bookings)
            menu.add_separator()
            menu.add_command(label='Toggle Maintenance', command=self._toggle_maintenance)
            menu.add_separator()
            menu.add_command(label='Delete Resource', command=self._delete_resource)
            
            menu.post(event.x_root, event.y_root)

    def _show_add_resource_form(self):
        """Show form to add new resource"""
        self._show_resource_form(mode='add')

    def _edit_resource(self):
        """Edit selected resource"""
        resource = self._get_selected_resource()
        if resource:
            self._show_resource_form(mode='edit', resource=resource)

    def _show_resource_form(self, mode='add', resource=None):
        """Show add/edit resource form modal"""
        # Create modal
        modal = tk.Toplevel(self)
        modal.title('Add New Resource' if mode == 'add' else 'Edit Resource')
        modal.geometry('700x800')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 350
        y = (modal.winfo_screenheight() // 2) - 400
        modal.geometry(f'700x800+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB') if mode == 'add' else self.colors.get('warning', '#F39C12'))
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=header.cget('bg'))
        header_content.pack(padx=20, pady=20)
        
        icon = '➕' if mode == 'add' else '✏️'
        tk.Label(header_content, text=icon, bg=header.cget('bg'), font=('Helvetica', 36)).pack()
        tk.Label(header_content, text='Add New Resource' if mode == 'add' else 'Edit Resource', bg=header.cget('bg'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=(8, 0))
        
        # Scrollable form
        canvas = tk.Canvas(modal, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(modal, orient='vertical', command=canvas.yview)
        form_frame = tk.Frame(canvas, bg='white')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=form_frame, anchor='nw')
        form_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Form fields
        content = tk.Frame(form_frame, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Form variables
        form_data = {
            'name': tk.StringVar(value=resource.get('name', '') if resource else ''),
            'type': tk.StringVar(value=resource.get('type', 'classroom') if resource else 'classroom'),
            'code': tk.StringVar(value=resource.get('code', '') if resource else ''),
            'capacity': tk.StringVar(value=str(resource.get('capacity', '')) if resource else ''),
            'location': tk.StringVar(value=resource.get('location', '') if resource else ''),
            'building': tk.StringVar(value=resource.get('building', '') if resource else ''),
            'floor': tk.StringVar(value=resource.get('floor', '') if resource else ''),
            'description': tk.StringVar(value=resource.get('description', '') if resource else ''),
            'status': tk.StringVar(value=resource.get('status', 'active') if resource else 'active'),
            'photo_path': tk.StringVar(value='')
        }
        
        # Amenities checkboxes
        amenity_vars = {}
        available_amenities = ['projector', 'whiteboard', 'computers', 'audio', 'ac', 'wifi', 'podium', 'recording']
        existing_amenities = resource.get('amenities', []) if resource else []
        
        for amenity in available_amenities:
            var = tk.BooleanVar(value=amenity in existing_amenities)
            amenity_vars[amenity] = var
        
        # Resource Name
        self._add_form_field(content, 'Resource Name *', form_data['name'], field_type='entry')
        
        # Type
        self._add_form_field(content, 'Resource Type *', form_data['type'], field_type='dropdown', 
                           options=['classroom', 'lab', 'auditorium', 'equipment', 'conference', 'sports'])
        
        # Code
        self._add_form_field(content, 'Resource Code', form_data['code'], field_type='entry', 
                           help_text='Unique identifier (e.g., CR-101, LAB-A1)')
        
        # Capacity
        self._add_form_field(content, 'Capacity *', form_data['capacity'], field_type='entry', 
                           help_text='Maximum number of people')
        
        # Location details section
        tk.Label(content, text='Location Details', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(16, 8))
        tk.Frame(content, bg='#E5E7EB', height=1).pack(fill='x', pady=(0, 12))
        
        self._add_form_field(content, 'Building', form_data['building'], field_type='entry')
        self._add_form_field(content, 'Floor', form_data['floor'], field_type='entry')
        self._add_form_field(content, 'Room/Location', form_data['location'], field_type='entry')
        
        # Description
        tk.Label(content, text='Description', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(12, 6))
        desc_text = tk.Text(content, height=4, font=('Helvetica', 10), wrap='word')
        desc_text.pack(fill='x', pady=(0, 12))
        if resource:
            desc_text.insert('1.0', resource.get('description', ''))
        desc_text.bind('<KeyRelease>', lambda e: form_data['description'].set(desc_text.get('1.0', 'end-1c')))
        
        # Amenities section
        tk.Label(content, text='Available Amenities', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(16, 8))
        tk.Frame(content, bg='#E5E7EB', height=1).pack(fill='x', pady=(0, 12))
        
        amenities_frame = tk.Frame(content, bg='white')
        amenities_frame.pack(fill='x', pady=(0, 12))
        
        amenity_labels = {
            'projector': '📽️ Projector',
            'whiteboard': '📝 Whiteboard',
            'computers': '💻 Computers',
            'audio': '🔊 Audio System',
            'ac': '❄️ Air Conditioning',
            'wifi': '📡 WiFi',
            'podium': '🎤 Podium',
            'recording': '📹 Recording Equipment'
        }
        
        for amenity, var in amenity_vars.items():
            label = amenity_labels.get(amenity, amenity.title())
            cb = tk.Checkbutton(amenities_frame, text=label, variable=var, bg='white', font=('Helvetica', 10), selectcolor='white')
            cb.pack(anchor='w', pady=2)
        
        # Photo upload
        tk.Label(content, text='Resource Photo', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(16, 8))
        tk.Frame(content, bg='#E5E7EB', height=1).pack(fill='x', pady=(0, 12))
        
        photo_frame = tk.Frame(content, bg='white')
        photo_frame.pack(fill='x', pady=(0, 12))
        
        tk.Button(photo_frame, text='📤 Upload Photo', command=lambda: self._upload_photo(form_data['photo_path']), bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left')
        photo_label = tk.Label(photo_frame, textvariable=form_data['photo_path'], bg='white', fg='#6B7280', font=('Helvetica', 9))
        photo_label.pack(side='left', padx=(8, 0))
        
        # Maintenance schedule (placeholder)
        tk.Label(content, text='Maintenance Schedule', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(16, 8))
        tk.Frame(content, bg='#E5E7EB', height=1).pack(fill='x', pady=(0, 12))
        
        maintenance_frame = tk.Frame(content, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        maintenance_frame.pack(fill='x', pady=(0, 12))
        
        tk.Label(maintenance_frame, text='Regular maintenance can be scheduled after resource creation', bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 9), padx=12, pady=8).pack(anchor='w')
        
        # Status toggle
        tk.Label(content, text='Resource Status', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(16, 8))
        tk.Frame(content, bg='#E5E7EB', height=1).pack(fill='x', pady=(0, 12))
        
        status_frame = tk.Frame(content, bg='white')
        status_frame.pack(fill='x', pady=(0, 12))
        
        tk.Radiobutton(status_frame, text='✅ Active - Available for booking', variable=form_data['status'], value='active', bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=2)
        tk.Radiobutton(status_frame, text='🔧 Maintenance - Not available for booking', variable=form_data['status'], value='maintenance', bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=2)
        
        # Action buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        tk.Button(btn_frame, text='Cancel', command=modal.destroy, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 11, 'bold'), padx=30, pady=12, width=12).pack(side='left')
        tk.Button(btn_frame, text='Save Resource', command=lambda: self._save_resource(modal, form_data, amenity_vars, mode, resource), bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=30, pady=12, width=15).pack(side='right')

    def _add_form_field(self, parent, label, variable, field_type='entry', options=None, help_text=None):
        """Add a form field"""
        tk.Label(parent, text=label, bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(12, 6))
        
        if help_text:
            tk.Label(parent, text=help_text, bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 4))
        
        if field_type == 'entry':
            entry = tk.Entry(parent, textvariable=variable, font=('Helvetica', 11))
            entry.pack(fill='x')
        elif field_type == 'dropdown':
            dropdown = ttk.Combobox(parent, textvariable=variable, state='readonly', font=('Helvetica', 11))
            dropdown['values'] = options or []
            dropdown.pack(fill='x')

    def _upload_photo(self, photo_var):
        """Handle photo upload"""
        filename = filedialog.askopenfilename(
            title='Select Resource Photo',
            filetypes=[('Image files', '*.jpg *.jpeg *.png *.gif'), ('All files', '*.*')]
        )
        if filename:
            photo_var.set(filename)

    def _save_resource(self, modal, form_data, amenity_vars, mode, resource):
        """Save resource (add or update)"""
        # Validate required fields
        if not form_data['name'].get().strip():
            messagebox.showerror('Validation Error', 'Resource name is required.')
            return
        
        if not form_data['capacity'].get().strip():
            messagebox.showerror('Validation Error', 'Capacity is required.')
            return
        
        try:
            capacity = int(form_data['capacity'].get().strip())
            if capacity <= 0:
                messagebox.showerror('Validation Error', 'Capacity must be a positive number.')
                return
        except ValueError:
            messagebox.showerror('Validation Error', 'Capacity must be a valid number.')
            return
        
        # Prepare data
        selected_amenities = [amenity for amenity, var in amenity_vars.items() if var.get()]
        
        resource_data = {
            'name': form_data['name'].get().strip(),
            'type': form_data['type'].get(),
            'code': form_data['code'].get().strip(),
            'capacity': capacity,
            'location': form_data['location'].get().strip(),
            'building': form_data['building'].get().strip(),
            'floor': form_data['floor'].get().strip(),
            'description': form_data['description'].get().strip(),
            'amenities': selected_amenities,
            'status': form_data['status'].get(),
            'photo': form_data['photo_path'].get()
        }
        
        modal.destroy()
        
        # Show loading
        loading = tk.Toplevel(self)
        loading.title('Saving...')
        loading.geometry('300x100')
        loading.configure(bg='white')
        loading.transient(self.winfo_toplevel())
        loading.grab_set()
        
        tk.Label(loading, text='Saving resource...', bg='white', fg='#374151', font=('Helvetica', 11)).pack(pady=10)
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
                if mode == 'add':
                    self.api.post('resources', resource_data)
                    message = 'Resource created successfully!'
                else:
                    resource_id = resource.get('id')
                    self.api.put(f'resources/{resource_id}', resource_data)
                    message = 'Resource updated successfully!'
                
                def show_success():
                    loading.destroy()
                    messagebox.showinfo('Success', message)
                    self._load_resources()
                
                self.after(0, show_success)
            except Exception as e:
                def show_error():
                    loading.destroy()
                    messagebox.showerror('Error', f'Failed to save resource: {str(e)}')
                
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _view_resource_details(self):
        """View detailed resource information"""
        resource = self._get_selected_resource()
        if not resource:
            return
        
        # Create modal
        modal = tk.Toplevel(self)
        modal.title(f"Resource Details - {resource.get('name', 'Resource')}")
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
        resource_type = (resource.get('type', 'equipment') or 'equipment').lower()
        type_icons = {
            'classroom': '🏫',
            'lab': '🔬',
            'auditorium': '🎭',
            'equipment': '⚙️',
            'conference': '💼',
            'sports': '⚽'
        }
        icon = type_icons.get(resource_type, '📦')
        
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=self.colors.get('secondary', '#3498DB'))
        header_content.pack(padx=20, pady=20)
        
        tk.Label(header_content, text=icon, bg=self.colors.get('secondary', '#3498DB'), font=('Helvetica', 36)).pack()
        tk.Label(header_content, text=resource.get('name', 'Unnamed Resource'), bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=(8, 0))
        tk.Label(header_content, text=f"Code: {resource.get('code', resource.get('id', 'N/A'))}", bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 10)).pack(pady=(4, 0))
        
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
        
        # Basic info
        tk.Label(details_frame, text='Basic Information', bg='white', fg='#1F2937', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 12))
        
        info_grid = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        info_grid.pack(fill='x', pady=(0, 20))
        
        info_content = tk.Frame(info_grid, bg='#F9FAFB')
        info_content.pack(padx=16, pady=12)
        
        self._add_detail_row(info_content, 'Type:', resource_type.title())
        self._add_detail_row(info_content, 'Capacity:', str(resource.get('capacity', 'N/A')))
        self._add_detail_row(info_content, 'Status:', (resource.get('status', 'active') or 'active').title())
        
        # Location
        tk.Label(details_frame, text='Location', bg='white', fg='#1F2937', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 12))
        
        location_grid = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        location_grid.pack(fill='x', pady=(0, 20))
        
        location_content = tk.Frame(location_grid, bg='#F9FAFB')
        location_content.pack(padx=16, pady=12)
        
        self._add_detail_row(location_content, 'Building:', resource.get('building', 'N/A'))
        self._add_detail_row(location_content, 'Floor:', resource.get('floor', 'N/A'))
        self._add_detail_row(location_content, 'Room:', resource.get('location', 'N/A'))
        
        # Description
        description = resource.get('description', 'No description available')
        tk.Label(details_frame, text='Description', bg='white', fg='#1F2937', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 12))
        tk.Label(details_frame, text=description, bg='white', fg='#6B7280', font=('Helvetica', 10), wraplength=520, justify='left').pack(anchor='w', pady=(0, 20))
        
        # Amenities
        amenities = resource.get('amenities', [])
        if amenities:
            tk.Label(details_frame, text='Available Amenities', bg='white', fg='#1F2937', font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 12))
            
            amenities_grid = tk.Frame(details_frame, bg='white')
            amenities_grid.pack(fill='x', pady=(0, 20))
            
            for amenity in amenities:
                amenity_row = tk.Frame(amenities_grid, bg='white')
                amenity_row.pack(fill='x', pady=2)
                tk.Label(amenity_row, text='✓', bg='white', fg=self.colors.get('success', '#27AE60'), font=('Helvetica', 12, 'bold')).pack(side='left', padx=(0, 8))
                tk.Label(amenity_row, text=str(amenity).title(), bg='white', fg='#374151', font=('Helvetica', 10)).pack(side='left')
        
        # Close button
        tk.Button(details_frame, text='Close', command=modal.destroy, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 11, 'bold'), padx=30, pady=12).pack(fill='x', pady=(16, 0))

    def _add_detail_row(self, parent, label, value):
        """Add detail row"""
        row = tk.Frame(parent, bg='#F9FAFB')
        row.pack(fill='x', pady=4)
        tk.Label(row, text=label, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 10), width=15, anchor='w').pack(side='left')
        tk.Label(row, text=str(value), bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(side='left')

    def _view_bookings(self):
        """View booking history for selected resource"""
        resource = self._get_selected_resource()
        if not resource:
            return
        
        messagebox.showinfo('View Bookings', 
                          f"Booking history for '{resource.get('name', 'Resource')}' would be displayed here.\n\n"
                          f"This would show:\n"
                          f"- Past bookings\n"
                          f"- Upcoming bookings\n"
                          f"- Pending requests\n"
                          f"- Utilization statistics")

    def _toggle_maintenance(self):
        """Toggle maintenance status for selected resource"""
        resource = self._get_selected_resource()
        if not resource:
            return
        
        current_status = resource.get('status', 'active').lower()
        new_status = 'maintenance' if current_status == 'active' else 'active'
        
        status_text = 'maintenance mode' if new_status == 'maintenance' else 'active status'
        
        result = messagebox.askyesno('Toggle Maintenance', 
                                     f"Change '{resource.get('name', 'Resource')}' to {status_text}?\n\n"
                                     f"{'This will prevent new bookings.' if new_status == 'maintenance' else 'This will allow new bookings.'}")
        
        if result:
            def worker():
                try:
                    resource_id = resource.get('id')
                    self.api.put(f'resources/{resource_id}', {'status': new_status})
                    
                    def show_success():
                        messagebox.showinfo('Success', f'Resource status updated to {status_text}.')
                        self._load_resources()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to update status: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _delete_resource(self):
        """Delete selected resource"""
        resource = self._get_selected_resource()
        if not resource:
            return
        
        result = messagebox.askyesno('Delete Resource', 
                                     f"Are you sure you want to delete '{resource.get('name', 'this resource')}'?\n\n"
                                     f"⚠️ This action cannot be undone!\n"
                                     f"All associated data will be permanently removed.",
                                     icon='warning')
        
        if result:
            # Double confirmation
            confirm = messagebox.askyesno('Final Confirmation', 
                                         'This is your final warning!\n\n'
                                         'Are you absolutely sure you want to delete this resource?',
                                         icon='warning')
            
            if confirm:
                def worker():
                    try:
                        resource_id = resource.get('id')
                        self.api.delete(f'resources/{resource_id}')
                        
                        def show_success():
                            messagebox.showinfo('Success', 'Resource deleted successfully.')
                            self._load_resources()
                        
                        self.after(0, show_success)
                    except Exception as e:
                        def show_error():
                            messagebox.showerror('Error', f'Failed to delete resource: {str(e)}')
                        self.after(0, show_error)
                
                threading.Thread(target=worker, daemon=True).start()
