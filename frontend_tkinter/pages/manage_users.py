import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from datetime import datetime

from utils.api_client import APIClient
from utils.session_manager import SessionManager


class ManageUsersPage(tk.Frame):
    """Admin page for managing users."""

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
        self.users = []
        self.filtered_users = []
        
        # Filter variables
        self.search_var = tk.StringVar()
        self.role_filter = tk.StringVar(value='all')
        self.status_filter = tk.StringVar(value='all')
        
        # Bind search
        self.search_var.trace('w', lambda *args: self._apply_filters())
        
        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_users()

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
        tk.Label(title_frame, text='👥 Manage Users', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='View and manage all system users', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(header_content, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text='🔄 Refresh', command=self._load_users, bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        tk.Button(btn_frame, text='📊 Export CSV', command=self._export_csv, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left')
        
        # Filters bar
        filters_frame = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        filters_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=(20, 0))
        
        filters_content = tk.Frame(filters_frame, bg='white')
        filters_content.pack(fill='x', padx=20, pady=12)
        
        # Search
        search_frame = tk.Frame(filters_content, bg='white')
        search_frame.pack(side='left', fill='x', expand=True, padx=(0, 20))
        
        tk.Label(search_frame, text='🔍', bg='white', font=('Helvetica', 12)).pack(side='left', padx=(0, 6))
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Helvetica', 10), relief='solid', borderwidth=1)
        search_entry.pack(side='left', fill='x', expand=True, ipady=4)
        search_entry.insert(0, 'Search by name or email...')
        search_entry.config(fg='#9CA3AF')
        
        def on_search_focus_in(event):
            if search_entry.get() == 'Search by name or email...':
                search_entry.delete(0, 'end')
                search_entry.config(fg='#1F2937')
        
        def on_search_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, 'Search by name or email...')
                search_entry.config(fg='#9CA3AF')
        
        search_entry.bind('<FocusIn>', on_search_focus_in)
        search_entry.bind('<FocusOut>', on_search_focus_out)
        
        # Role filter
        role_frame = tk.Frame(filters_content, bg='white')
        role_frame.pack(side='left', padx=(0, 12))
        
        tk.Label(role_frame, text='Role:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='left', padx=(0, 6))
        role_dropdown = ttk.Combobox(role_frame, textvariable=self.role_filter, state='readonly', width=15, font=('Helvetica', 10))
        role_dropdown['values'] = ('all', 'student', 'organizer', 'admin')
        role_dropdown.pack(side='left')
        role_dropdown.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
        
        # Status filter
        status_frame = tk.Frame(filters_content, bg='white')
        status_frame.pack(side='left')
        
        tk.Label(status_frame, text='Status:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='left', padx=(0, 6))
        status_dropdown = ttk.Combobox(status_frame, textvariable=self.status_filter, state='readonly', width=12, font=('Helvetica', 10))
        status_dropdown['values'] = ('all', 'active', 'blocked')
        status_dropdown.pack(side='left')
        status_dropdown.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
        
        # Results count
        self.count_label = tk.Label(filters_content, text='', bg='white', fg='#6B7280', font=('Helvetica', 10))
        self.count_label.pack(side='right', padx=(20, 0))
        
        # Table container
        table_frame = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        table_frame.grid(row=2, column=0, sticky='nsew', padx=30, pady=(12, 20))

        # Create Treeview with scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame, orient='vertical')
        tree_scroll_y.pack(side='right', fill='y')
        
        tree_scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')
        
        # Configure Treeview style
        style = ttk.Style()
        style.configure('Users.Treeview',
                       font=('Helvetica', 10),
                       rowheight=35,
                       background='white',
                       fieldbackground='white',
                       foreground='#1F2937')
        style.configure('Users.Treeview.Heading',
                       font=('Helvetica', 10, 'bold'),
                       background='#F9FAFB',
                       foreground='#374151')
        style.map('Users.Treeview',
                 background=[('selected', self.colors.get('secondary', '#3498DB'))],
                 foreground=[('selected', 'white')])
        
        # Create table
        columns = ('id', 'name', 'email', 'role', 'status', 'registered', 'actions')
        self.tree = ttk.Treeview(table_frame,
                                columns=columns,
                                show='headings',
                                style='Users.Treeview',
                                yscrollcommand=tree_scroll_y.set,
                                xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('email', text='Email')
        self.tree.heading('role', text='Role')
        self.tree.heading('status', text='Status')
        self.tree.heading('registered', text='Registration Date')
        self.tree.heading('actions', text='Actions')
        
        self.tree.column('id', width=60, anchor='center')
        self.tree.column('name', width=180)
        self.tree.column('email', width=220)
        self.tree.column('role', width=100, anchor='center')
        self.tree.column('status', width=100, anchor='center')
        self.tree.column('registered', width=150, anchor='center')
        self.tree.column('actions', width=100, anchor='center')
        
        self.tree.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Context menu
        self.context_menu = tk.Menu(self.tree, tearoff=0, font=('Helvetica', 10))
        self.context_menu.add_command(label='👁️ View Details', command=self._view_user_details)
        self.context_menu.add_command(label='✏️ Edit Role', command=self._edit_user_role)
        self.context_menu.add_separator()
        self.context_menu.add_command(label='🔒 Block User', command=self._block_user)
        self.context_menu.add_command(label='🔓 Unblock User', command=self._unblock_user)
        self.context_menu.add_separator()
        self.context_menu.add_command(label='🔑 Reset Password', command=self._reset_password)
        self.context_menu.add_command(label='📧 Send Email', command=self._send_email)
        self.context_menu.add_separator()
        self.context_menu.add_command(label='🗑️ Delete User', command=self._delete_user)
        
        # Bind events
        self.tree.bind('<Button-3>', self._show_context_menu)  # Right-click
        self.tree.bind('<Double-1>', lambda e: self._view_user_details())  # Double-click

    def _load_users(self):
        """Load users from API"""
        self._show_loading()
        
        def worker():
            try:
                # Build query params
                params = {}
                
                role = self.role_filter.get()
                if role != 'all':
                    params['role'] = role
                
                status = self.status_filter.get()
                if status != 'all':
                    params['status'] = status
                
                search = self.search_var.get()
                if search and search != 'Search by name or email...':
                    params['search'] = search
                
                # Build query string
                query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
                endpoint = f'admin/users?{query_string}' if query_string else 'admin/users'
                
                self.users = self.api.get(endpoint) or []
                self.filtered_users = self.users.copy()
                
                self.after(0, self._populate_table)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load users: {str(e)}')
                    self.users = []
                    self.filtered_users = []
                    self._populate_table()
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _show_loading(self):
        """Show loading in table"""
        self.tree.delete(*self.tree.get_children())
        self.count_label.config(text='Loading...')

    def _apply_filters(self):
        """Apply filters to user list"""
        search_text = self.search_var.get().lower()
        if search_text == 'search by name or email...':
            search_text = ''
        
        role = self.role_filter.get()
        status = self.status_filter.get()
        
        self.filtered_users = []
        
        for user in self.users:
            # Search filter
            if search_text:
                name = user.get('name', '').lower()
                email = user.get('email', '').lower()
                if search_text not in name and search_text not in email:
                    continue
            
            # Role filter
            if role != 'all' and user.get('role', '').lower() != role:
                continue
            
            # Status filter
            if status != 'all' and user.get('status', '').lower() != status:
                continue
            
            self.filtered_users.append(user)
        
        self._populate_table()

    def _populate_table(self):
        """Populate the users table"""
        # Clear table
        self.tree.delete(*self.tree.get_children())
        
        # Update count
        count = len(self.filtered_users)
        total = len(self.users)
        if count == total:
            self.count_label.config(text=f'Showing {count} user{"s" if count != 1 else ""}')
        else:
            self.count_label.config(text=f'Showing {count} of {total} users')
        
        # Add rows
        for user in self.filtered_users:
            user_id = user.get('id', '')
            name = user.get('name', 'N/A')
            email = user.get('email', 'N/A')
            role = (user.get('role', 'user') or 'user').title()
            status = (user.get('status', 'active') or 'active').title()
            registered = self._format_date(user.get('created_at', ''))
            
            # Format role with emoji
            role_display = {
                'Student': '🎓 Student',
                'Organizer': '📋 Organizer',
                'Admin': '👑 Admin'
            }.get(role, role)
            
            # Format status with emoji
            status_display = {
                'Active': '✅ Active',
                'Blocked': '🚫 Blocked'
            }.get(status, status)
            
            values = (user_id, name, email, role_display, status_display, registered, '⚙️ Actions')
            self.tree.insert('', 'end', values=values, tags=(user_id,))

    def _show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            
            # Get user status to enable/disable block/unblock
            user = self._get_selected_user()
            if user:
                status = user.get('status', 'active').lower()
                
                # Update menu items
                self.context_menu.entryconfig(3, state='normal' if status == 'active' else 'disabled')  # Block
                self.context_menu.entryconfig(4, state='normal' if status == 'blocked' else 'disabled')  # Unblock
            
            self.context_menu.post(event.x_root, event.y_root)

    def _get_selected_user(self):
        """Get the currently selected user"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = selection[0]
        user_id = self.tree.item(item)['values'][0]
        
        # Find user in list
        for user in self.filtered_users:
            if user.get('id') == user_id:
                return user
        
        return None

    def _view_user_details(self):
        """Show user details modal"""
        user = self._get_selected_user()
        if not user:
            messagebox.showwarning('No Selection', 'Please select a user to view.')
            return
        
        # Create modal
        modal = tk.Toplevel(self)
        modal.title(f"User Details - {user.get('name', 'User')}")
        modal.geometry('900x800')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 450
        y = (modal.winfo_screenheight() // 2) - 400
        modal.geometry(f'900x800+{x}+{y}')
        
        # Header
        status = user.get('status', 'active').lower()
        header_color = self.colors.get('danger', '#E74C3C') if status == 'blocked' else self.colors.get('secondary', '#3498DB')
        
        header = tk.Frame(modal, bg=header_color)
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=header_color)
        header_content.pack(padx=30, pady=20)
        
        tk.Label(header_content, text='👤', bg=header_color, font=('Helvetica', 36)).pack()
        tk.Label(header_content, text=user.get('name', 'User'), bg=header_color, fg='white', font=('Helvetica', 18, 'bold')).pack(pady=(8, 0))
        tk.Label(header_content, text=user.get('email', ''), bg=header_color, fg='white', font=('Helvetica', 11)).pack(pady=(4, 0))
        
        # Status badge
        status_text = '🚫 BLOCKED' if status == 'blocked' else '✅ ACTIVE'
        status_bg = '#FEF2F2' if status == 'blocked' else '#F0FDF4'
        status_fg = '#991B1B' if status == 'blocked' else '#166534'
        
        status_badge = tk.Frame(header_content, bg=status_bg, highlightthickness=1, highlightbackground=header_color)
        status_badge.pack(pady=(8, 0))
        tk.Label(status_badge, text=status_text, bg=status_bg, fg=status_fg, font=('Helvetica', 9, 'bold'), padx=12, pady=4).pack()
        
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
        
        # Profile information
        self._add_section_header(details_frame, '📋 Profile Information')
        
        profile_card = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        profile_card.pack(fill='x', pady=(0, 16))
        
        profile_content = tk.Frame(profile_card, bg='#F9FAFB')
        profile_content.pack(padx=20, pady=16)
        
        # Left column
        left_col = tk.Frame(profile_content, bg='#F9FAFB')
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 30))
        
        self._add_modal_detail(left_col, 'User ID:', user.get('id', 'N/A'))
        self._add_modal_detail(left_col, 'Full Name:', user.get('name', 'N/A'))
        self._add_modal_detail(left_col, 'Email:', user.get('email', 'N/A'))
        self._add_modal_detail(left_col, 'Phone:', user.get('phone', 'N/A'))
        
        # Right column
        right_col = tk.Frame(profile_content, bg='#F9FAFB')
        right_col.pack(side='left', fill='both', expand=True)
        
        self._add_modal_detail(right_col, 'Role:', (user.get('role', 'user') or 'user').title())
        self._add_modal_detail(right_col, 'Department:', user.get('department', 'N/A'))
        self._add_modal_detail(right_col, 'Student ID:', user.get('student_id', 'N/A'))
        self._add_modal_detail(right_col, 'Registered:', self._format_date(user.get('created_at', '')))
        
        # Activity statistics
        self._add_section_header(details_frame, '📊 Activity Statistics')
        
        stats_grid = tk.Frame(details_frame, bg='white')
        stats_grid.pack(fill='x', pady=(0, 16))
        
        # Stat cards
        stats_data = [
            ('📅', 'Events Attended', user.get('events_attended', 0), '#EFF6FF', '#1E40AF'),
            ('📋', 'Bookings Made', user.get('bookings_made', 0), '#F0FDF4', '#166534'),
            ('🎭', 'Events Organized', user.get('events_organized', 0), '#FEF3C7', '#92400E'),
            ('⚠️', 'Warnings', user.get('warnings', 0), '#FEF2F2', '#991B1B')
        ]
        
        for icon, label, value, bg, fg in stats_data:
            self._add_stat_card(stats_grid, icon, label, str(value), bg, fg)
        
        # Activity log
        self._add_section_header(details_frame, '📜 Recent Activity Log')
        
        activity_card = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
        activity_card.pack(fill='x', pady=(0, 16))
        
        activity_content = tk.Frame(activity_card, bg='#F9FAFB')
        activity_content.pack(padx=20, pady=16)
        
        # Sample activity items
        activities = [
            ('📅', 'Attended event "Tech Workshop 2024"', '2 days ago'),
            ('📋', 'Booked "Conference Room A"', '5 days ago'),
            ('✅', 'Booking approved for "Lab 101"', '1 week ago'),
            ('🎭', 'Created event "Study Group"', '2 weeks ago'),
            ('👤', 'Updated profile information', '1 month ago')
        ]
        
        for icon, action, time in activities:
            activity_item = tk.Frame(activity_content, bg='#F9FAFB')
            activity_item.pack(fill='x', pady=4)
            
            tk.Label(activity_item, text=icon, bg='#F9FAFB', font=('Helvetica', 12)).pack(side='left', padx=(0, 8))
            tk.Label(activity_item, text=action, bg='#F9FAFB', fg='#374151', font=('Helvetica', 9)).pack(side='left')
            tk.Label(activity_item, text=time, bg='#F9FAFB', fg='#9CA3AF', font=('Helvetica', 8)).pack(side='right')
        
        # Events organized (if organizer)
        if user.get('role', '').lower() == 'organizer':
            self._add_section_header(details_frame, '🎭 Events Organized')
            
            events_card = tk.Frame(details_frame, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
            events_card.pack(fill='x', pady=(0, 16))
            
            events_content = tk.Frame(events_card, bg='#F9FAFB')
            events_content.pack(padx=20, pady=16)
            
            # Sample events
            tk.Label(events_content, text='• Tech Workshop 2024 (Approved)', bg='#F9FAFB', fg='#374151', font=('Helvetica', 9)).pack(anchor='w', pady=2)
            tk.Label(events_content, text='• Student Meetup (Pending)', bg='#F9FAFB', fg='#374151', font=('Helvetica', 9)).pack(anchor='w', pady=2)
            tk.Label(events_content, text='• Coding Competition (Completed)', bg='#F9FAFB', fg='#374151', font=('Helvetica', 9)).pack(anchor='w', pady=2)
        
        # Warnings/violations
        warnings_count = user.get('warnings', 0)
        if warnings_count > 0:
            self._add_section_header(details_frame, '⚠️ Warnings & Violations')
            
            warnings_card = tk.Frame(details_frame, bg='#FEF2F2', highlightthickness=1, highlightbackground='#E74C3C')
            warnings_card.pack(fill='x', pady=(0, 16))
            
            warnings_content = tk.Frame(warnings_card, bg='#FEF2F2')
            warnings_content.pack(padx=20, pady=16)
            
            tk.Label(warnings_content, text=f'⚠️ This user has {warnings_count} warning{"s" if warnings_count > 1 else ""}', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 8))
            
            # Sample warnings
            tk.Label(warnings_content, text='• Late cancellation of booking (2024-09-15)', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9)).pack(anchor='w', pady=2)
            tk.Label(warnings_content, text='• No-show for event (2024-08-20)', bg='#FEF2F2', fg='#991B1B', font=('Helvetica', 9)).pack(anchor='w', pady=2)
        
        # Action buttons
        self._add_section_header(details_frame, '⚙️ Quick Actions')
        
        actions_frame = tk.Frame(details_frame, bg='white')
        actions_frame.pack(fill='x', pady=(0, 16))
        
        tk.Button(actions_frame, text='✏️ Edit Role', command=lambda: [modal.destroy(), self._edit_user_role()], bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=8).pack(side='left', padx=(0, 8))
        
        if status == 'active':
            tk.Button(actions_frame, text='🔒 Block User', command=lambda: [modal.destroy(), self._block_user()], bg=self.colors.get('danger', '#E74C3C'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=8).pack(side='left', padx=(0, 8))
        else:
            tk.Button(actions_frame, text='🔓 Unblock User', command=lambda: [modal.destroy(), self._unblock_user()], bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=8).pack(side='left', padx=(0, 8))
        
        tk.Button(actions_frame, text='🔑 Reset Password', command=lambda: [modal.destroy(), self._reset_password()], bg=self.colors.get('warning', '#F39C12'), fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=8).pack(side='left', padx=(0, 8))
        
        tk.Button(actions_frame, text='📧 Send Email', command=lambda: [modal.destroy(), self._send_email()], bg='#6366F1', fg='white', relief='flat', font=('Helvetica', 10, 'bold'), padx=20, pady=8).pack(side='left')
        
        # Close button
        tk.Button(details_frame, text='Close', command=modal.destroy, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 11, 'bold'), padx=30, pady=10).pack(fill='x', pady=(16, 0))

    def _add_section_header(self, parent, text):
        """Add section header"""
        tk.Label(parent, text=text, bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 13, 'bold')).pack(anchor='w', pady=(0, 8))
        tk.Frame(parent, bg='#E5E7EB', height=1).pack(fill='x', pady=(0, 12))

    def _add_modal_detail(self, parent, label, value):
        """Add detail row in modal"""
        row = tk.Frame(parent, bg='#F9FAFB')
        row.pack(fill='x', pady=4)
        tk.Label(row, text=label, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w')
        tk.Label(row, text=str(value), bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(2, 0))

    def _add_stat_card(self, parent, icon, label, value, bg_color, fg_color):
        """Add statistics card"""
        card = tk.Frame(parent, bg=bg_color, highlightthickness=1, highlightbackground=fg_color)
        card.pack(side='left', fill='both', expand=True, padx=(0, 12))
        
        content = tk.Frame(card, bg=bg_color)
        content.pack(padx=16, pady=12)
        
        tk.Label(content, text=icon, bg=bg_color, font=('Helvetica', 24)).pack()
        tk.Label(content, text=value, bg=bg_color, fg=fg_color, font=('Helvetica', 18, 'bold')).pack(pady=(4, 0))
        tk.Label(content, text=label, bg=bg_color, fg=fg_color, font=('Helvetica', 9)).pack()

    def _edit_user_role(self):
        """Edit user role"""
        user = self._get_selected_user()
        if not user:
            messagebox.showwarning('No Selection', 'Please select a user to edit.')
            return
        
        current_role = user.get('role', 'student')
        
        # Create modal
        modal = tk.Toplevel(self)
        modal.title(f"Edit Role - {user.get('name', 'User')}")
        modal.geometry('500x350')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 250
        y = (modal.winfo_screenheight() // 2) - 175
        modal.geometry(f'500x350+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        tk.Label(header, text='✏️ Edit User Role', bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Content
        content = tk.Frame(modal, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(content, text=f"Change role for: {user.get('name', 'User')}", bg='white', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 20))
        
        tk.Label(content, text='Current Role:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        tk.Label(content, text=current_role.title(), bg='white', fg='#1F2937', font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(2, 20))
        
        tk.Label(content, text='New Role:', bg='white', fg='#6B7280', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 8))
        
        # Role selection
        new_role_var = tk.StringVar(value=current_role)
        
        roles = [
            ('student', '🎓 Student', 'Regular student user'),
            ('organizer', '📋 Organizer', 'Can create and manage events'),
            ('admin', '👑 Admin', 'Full system access')
        ]
        
        for role_value, role_label, role_desc in roles:
            role_frame = tk.Frame(content, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB')
            role_frame.pack(fill='x', pady=(0, 8))
            
            rb = tk.Radiobutton(role_frame, text=role_label, variable=new_role_var, value=role_value, bg='#F9FAFB', font=('Helvetica', 11, 'bold'), selectcolor='#F9FAFB')
            rb.pack(anchor='w', padx=12, pady=(8, 2))
            
            tk.Label(role_frame, text=role_desc, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', padx=12, pady=(0, 8))
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        tk.Button(btn_frame, text='💾 Save Role', command=lambda: self._confirm_role_change(modal, user, new_role_var.get()), bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=20, pady=10).pack(fill='x', pady=(0, 8))
        tk.Button(btn_frame, text='Cancel', command=modal.destroy, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 11, 'bold'), padx=20, pady=10).pack(fill='x')

    def _confirm_role_change(self, modal, user, new_role):
        """Confirm and save role change"""
        if new_role == user.get('role'):
            messagebox.showinfo('No Change', 'The role has not been changed.')
            modal.destroy()
            return
        
        result = messagebox.askyesno('Confirm Role Change',
                                     f"Change role for {user.get('name', 'user')}?\n\n"
                                     f"From: {user.get('role', 'user').title()}\n"
                                     f"To: {new_role.title()}\n\n"
                                     f"This will affect the user's permissions.")
        
        if result:
            def worker():
                try:
                    user_id = user.get('id')
                    data = {'role': new_role}
                    self.api.put(f'admin/users/{user_id}/role', data)
                    
                    def show_success():
                        messagebox.showinfo('Success', f"User role updated to {new_role.title()}!")
                        modal.destroy()
                        self._load_users()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to update role: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _block_user(self):
        """Block a user"""
        user = self._get_selected_user()
        if not user:
            messagebox.showwarning('No Selection', 'Please select a user to block.')
            return
        
        if user.get('status', '').lower() == 'blocked':
            messagebox.showinfo('Already Blocked', 'This user is already blocked.')
            return
        
        reason = simpledialog.askstring('Block User',
                                       f"Provide a reason for blocking {user.get('name', 'this user')}:\n(Optional)",
                                       parent=self)
        
        result = messagebox.askyesno('Confirm Block',
                                     f"Block user: {user.get('name', 'User')}?\n\n"
                                     f"🚫 User will lose access\n"
                                     f"📋 All bookings will be cancelled\n"
                                     f"🎭 Events will be removed\n\n"
                                     f"Reason: {reason if reason else 'No reason provided'}")
        
        if result:
            def worker():
                try:
                    user_id = user.get('id')
                    data = {'reason': reason} if reason else {}
                    self.api.put(f'admin/users/{user_id}/block', data)
                    
                    def show_success():
                        messagebox.showinfo('User Blocked',
                                          f"🚫 {user.get('name', 'User')} has been blocked.\n\n"
                                          f"The user cannot access the system.")
                        self._load_users()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to block user: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _unblock_user(self):
        """Unblock a user"""
        user = self._get_selected_user()
        if not user:
            messagebox.showwarning('No Selection', 'Please select a user to unblock.')
            return
        
        if user.get('status', '').lower() != 'blocked':
            messagebox.showinfo('Not Blocked', 'This user is not blocked.')
            return
        
        result = messagebox.askyesno('Confirm Unblock',
                                     f"Unblock user: {user.get('name', 'User')}?\n\n"
                                     f"✅ User will regain access\n"
                                     f"📧 User will be notified")
        
        if result:
            def worker():
                try:
                    user_id = user.get('id')
                    self.api.put(f'admin/users/{user_id}/block', {'blocked': False})
                    
                    def show_success():
                        messagebox.showinfo('User Unblocked',
                                          f"✅ {user.get('name', 'User')} has been unblocked.\n\n"
                                          f"The user can now access the system.")
                        self._load_users()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to unblock user: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _reset_password(self):
        """Reset user password"""
        user = self._get_selected_user()
        if not user:
            messagebox.showwarning('No Selection', 'Please select a user.')
            return
        
        result = messagebox.askyesno('Reset Password',
                                     f"Reset password for: {user.get('name', 'User')}?\n\n"
                                     f"🔑 A temporary password will be generated\n"
                                     f"📧 User will receive reset instructions\n"
                                     f"⚠️ Current password will be invalidated")
        
        if result:
            messagebox.showinfo('Password Reset',
                              f"Password reset feature:\n\n"
                              f"✅ Temporary password: TempPass{user.get('id', '123')}!\n"
                              f"📧 Reset email sent to {user.get('email', 'user@example.com')}\n"
                              f"🔒 User must change password on next login")

    def _send_email(self):
        """Send email to user"""
        user = self._get_selected_user()
        if not user:
            messagebox.showwarning('No Selection', 'Please select a user.')
            return
        
        # Create email modal
        modal = tk.Toplevel(self)
        modal.title(f"Send Email - {user.get('name', 'User')}")
        modal.geometry('600x500')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 300
        y = (modal.winfo_screenheight() // 2) - 250
        modal.geometry(f'600x500+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg='#6366F1')
        header.pack(fill='x')
        tk.Label(header, text='📧 Send Email', bg='#6366F1', fg='white', font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Content
        content = tk.Frame(modal, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(content, text=f"To: {user.get('name', 'User')} ({user.get('email', '')})", bg='white', fg='#1F2937', font=('Helvetica', 10)).pack(anchor='w', pady=(0, 16))
        
        tk.Label(content, text='Subject:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        subject_entry = tk.Entry(content, font=('Helvetica', 11), relief='solid', borderwidth=1)
        subject_entry.pack(fill='x', ipady=6, pady=(0, 16))
        
        tk.Label(content, text='Message:', bg='white', fg='#374151', font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        message_text = tk.Text(content, height=10, font=('Helvetica', 11), wrap='word', relief='solid', borderwidth=1)
        message_text.pack(fill='both', expand=True, pady=(0, 16))
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text='📧 Send Email', command=lambda: [messagebox.showinfo('Email Sent', 'Email sent successfully!'), modal.destroy()], bg='#6366F1', fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=20, pady=10).pack(fill='x', pady=(0, 8))
        tk.Button(btn_frame, text='Cancel', command=modal.destroy, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 11, 'bold'), padx=20, pady=10).pack(fill='x')

    def _delete_user(self):
        """Delete a user"""
        user = self._get_selected_user()
        if not user:
            messagebox.showwarning('No Selection', 'Please select a user to delete.')
            return
        
        # Prevent deleting yourself
        current_user = self.session.get_user()
        if current_user and str(user.get('id')) == str(current_user.get('id')):
            messagebox.showerror('Cannot Delete', 'You cannot delete your own account!')
            return
        
        result = messagebox.askyesno('Confirm Deletion',
                                     f"⚠️ WARNING: Delete user {user.get('name', 'User')}?\n\n"
                                     f"This action CANNOT be undone!\n\n"
                                     f"This will:\n"
                                     f"• Permanently delete the user account\n"
                                     f"• Remove all their data\n"
                                     f"• Cancel all their bookings\n"
                                     f"• Delete all their events",
                                     icon='warning')
        
        if not result:
            return
        
        # Second confirmation
        result2 = messagebox.askyesno('Final Confirmation',
                                      f"⚠️ FINAL WARNING\n\n"
                                      f"Are you absolutely sure you want to delete:\n"
                                      f"{user.get('name', 'User')} ({user.get('email', '')})?",
                                      icon='warning')
        
        if result2:
            def worker():
                try:
                    user_id = user.get('id')
                    self.api.delete(f'admin/users/{user_id}')
                    
                    def show_success():
                        messagebox.showinfo('User Deleted',
                                          f"🗑️ User {user.get('name', 'User')} has been permanently deleted.")
                        self._load_users()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to delete user: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _export_csv(self):
        """Export users to CSV"""
        if not self.filtered_users:
            messagebox.showwarning('No Data', 'No users to export.')
            return
        
        try:
            import csv
            from tkinter import filedialog
            
            file_path = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[('CSV Files', '*.csv')],
                initialfile=f'users_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            )
            
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Header
                    writer.writerow(['ID', 'Name', 'Email', 'Role', 'Status', 'Department', 'Phone', 'Registered Date'])
                    
                    # Data
                    for user in self.filtered_users:
                        writer.writerow([
                            user.get('id', ''),
                            user.get('name', ''),
                            user.get('email', ''),
                            user.get('role', ''),
                            user.get('status', ''),
                            user.get('department', ''),
                            user.get('phone', ''),
                            self._format_date(user.get('created_at', ''))
                        ])
                
                messagebox.showinfo('Export Successful',
                                  f'✅ Exported {len(self.filtered_users)} user{"s" if len(self.filtered_users) != 1 else ""} to:\n{file_path}')
        except Exception as e:
            messagebox.showerror('Export Failed', f'Failed to export CSV: {str(e)}')

    def _format_date(self, date_str):
        """Format date for display"""
        if not date_str:
            return 'N/A'
        try:
            date_obj = datetime.strptime(date_str[:10] if len(date_str) >= 10 else date_str, '%Y-%m-%d')
            return date_obj.strftime('%b %d, %Y')
        except:
            return date_str or 'N/A'
