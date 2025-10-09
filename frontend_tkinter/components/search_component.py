"""
Reusable Search Component with Advanced Filters
Can be used across Events, Resources, and Users pages
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkcalendar import DateEntry


class SearchComponent(tk.Frame):
    """Reusable search component with advanced filters."""

    def __init__(self, parent, on_search_callback, config=None, colors=None):
        """
        Initialize search component.
        
        Args:
            parent: Parent widget
            on_search_callback: Callback function(search_text, filters) called when search/filter changes
            config: Configuration dict with:
                - categories: List of category options (e.g., ['Workshop', 'Seminar'])
                - statuses: List of status options (e.g., ['Active', 'Pending'])
                - sort_options: List of sort options (e.g., ['Date', 'Name', 'Popularity'])
                - show_date_filter: bool (default True)
                - show_category_filter: bool (default True)
                - show_status_filter: bool (default True)
                - placeholder: str (default 'Search...')
            colors: Color scheme dict
        """
        super().__init__(parent, bg='white')
        
        self.on_search_callback = on_search_callback
        
        # Configuration
        self.config = config or {}
        self.categories = self.config.get('categories', [])
        self.statuses = self.config.get('statuses', [])
        self.sort_options = self.config.get('sort_options', ['Relevance', 'Date', 'Name'])
        self.placeholder = self.config.get('placeholder', 'Search...')
        
        # Feature flags
        self.show_date_filter = self.config.get('show_date_filter', True)
        self.show_category_filter = self.config.get('show_category_filter', True)
        self.show_status_filter = self.config.get('show_status_filter', True)
        
        # Colors
        self.colors = colors or {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'background': '#ECF0F1'
        }
        
        # State
        self.search_text = tk.StringVar()
        self.search_history = []
        self.active_filters = {}
        self.debounce_timer = None
        
        # Filter variables
        self.start_date = None
        self.end_date = None
        self.selected_categories = []
        self.selected_status = tk.StringVar(value='all')
        self.selected_sort = tk.StringVar(value=self.sort_options[0] if self.sort_options else 'Relevance')
        
        # Build UI
        self._build_ui()
        
        # Bind search
        self.search_text.trace('w', self._on_search_change)

    def _build_ui(self):
        """Build the search component UI"""
        # Main container
        self.configure(bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        
        # Search bar row
        search_row = tk.Frame(self, bg='white')
        search_row.pack(fill='x', padx=16, pady=12)
        
        # Search icon
        tk.Label(search_row, text='🔍', bg='white', font=('Helvetica', 14)).pack(side='left', padx=(0, 8))
        
        # Search input
        self.search_entry = tk.Entry(search_row, textvariable=self.search_text, font=('Helvetica', 11), relief='flat', bg='white', fg='#1F2937')
        self.search_entry.pack(side='left', fill='x', expand=True)
        
        # Placeholder behavior
        self._setup_placeholder()
        
        # Advanced filters button
        self.filters_btn = tk.Button(search_row, text='⚙️ Filters', command=self._show_filters_modal, bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6, cursor='hand2')
        self.filters_btn.pack(side='right', padx=(8, 0))
        
        # Search button
        search_btn = tk.Button(search_row, text='Search', command=self._execute_search, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=16, pady=6, cursor='hand2')
        search_btn.pack(side='right', padx=(8, 0))
        
        # Filter tags container (initially hidden)
        self.tags_frame = tk.Frame(self, bg='white')
        
        # Separator
        tk.Frame(self, bg='#E5E7EB', height=1).pack(fill='x')

    def _setup_placeholder(self):
        """Setup placeholder text behavior"""
        def on_focus_in(event):
            if self.search_entry.get() == self.placeholder:
                self.search_entry.delete(0, 'end')
                self.search_entry.config(fg='#1F2937')
        
        def on_focus_out(event):
            if not self.search_entry.get():
                self.search_entry.insert(0, self.placeholder)
                self.search_entry.config(fg='#9CA3AF')
        
        self.search_entry.insert(0, self.placeholder)
        self.search_entry.config(fg='#9CA3AF')
        self.search_entry.bind('<FocusIn>', on_focus_in)
        self.search_entry.bind('<FocusOut>', on_focus_out)

    def _on_search_change(self, *args):
        """Handle search text change with debouncing"""
        # Cancel previous timer
        if self.debounce_timer:
            self.after_cancel(self.debounce_timer)
        
        # Set new timer (500ms debounce)
        self.debounce_timer = self.after(500, self._execute_search)

    def _execute_search(self):
        """Execute search with current text and filters"""
        search_text = self.search_text.get()
        
        # Don't search if placeholder is showing
        if search_text == self.placeholder:
            search_text = ''
        
        # Add to history if not empty and not already in history
        if search_text and search_text not in self.search_history:
            self.search_history.insert(0, search_text)
            if len(self.search_history) > 10:
                self.search_history.pop()
        
        # Call callback with search text and filters
        if self.on_search_callback:
            self.on_search_callback(search_text, self.active_filters.copy())

    def _show_filters_modal(self):
        """Show advanced filters modal"""
        modal = tk.Toplevel(self)
        modal.title('Advanced Filters')
        modal.geometry('550x700')
        modal.configure(bg='white')
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 275
        y = (modal.winfo_screenheight() // 2) - 350
        modal.geometry(f'550x700+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=self.colors.get('secondary', '#3498DB'))
        header.pack(fill='x')
        tk.Label(header, text='⚙️ Advanced Filters', bg=self.colors.get('secondary', '#3498DB'), fg='white', font=('Helvetica', 16, 'bold')).pack(pady=20)
        
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
        
        # Date Range Filter
        if self.show_date_filter:
            self._add_section_header(form_frame, '📅 Date Range')
            
            date_frame = tk.Frame(form_frame, bg='white')
            date_frame.pack(fill='x', pady=(0, 20))
            
            # Start date
            left_col = tk.Frame(date_frame, bg='white')
            left_col.pack(side='left', fill='both', expand=True, padx=(0, 12))
            
            tk.Label(left_col, text='From:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w', pady=(0, 4))
            start_date_entry = DateEntry(left_col, width=15, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            start_date_entry.pack(fill='x', ipady=4)
            if self.start_date:
                start_date_entry.set_date(self.start_date)
            
            # End date
            right_col = tk.Frame(date_frame, bg='white')
            right_col.pack(side='left', fill='both', expand=True)
            
            tk.Label(right_col, text='To:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w', pady=(0, 4))
            end_date_entry = DateEntry(right_col, width=15, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            end_date_entry.pack(fill='x', ipady=4)
            if self.end_date:
                end_date_entry.set_date(self.end_date)
        
        # Category Filter
        category_vars = {}
        if self.show_category_filter and self.categories:
            self._add_section_header(form_frame, '📂 Categories')
            
            tk.Label(form_frame, text='Select one or more categories:', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 8))
            
            categories_frame = tk.Frame(form_frame, bg='white')
            categories_frame.pack(fill='x', pady=(0, 20))
            
            for category in self.categories:
                var = tk.BooleanVar(value=category in self.selected_categories)
                category_vars[category] = var
                
                cb = tk.Checkbutton(categories_frame, text=category, variable=var, bg='white', font=('Helvetica', 10), selectcolor='white')
                cb.pack(anchor='w', pady=2)
        
        # Status Filter
        if self.show_status_filter and self.statuses:
            self._add_section_header(form_frame, '📊 Status')
            
            status_frame = tk.Frame(form_frame, bg='white')
            status_frame.pack(fill='x', pady=(0, 20))
            
            status_var = tk.StringVar(value=self.selected_status.get())
            
            # Add "All" option
            tk.Radiobutton(status_frame, text='All', variable=status_var, value='all', bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=2)
            
            for status in self.statuses:
                tk.Radiobutton(status_frame, text=status, variable=status_var, value=status.lower(), bg='white', font=('Helvetica', 10), selectcolor='white').pack(anchor='w', pady=2)
        
        # Sort Options
        self._add_section_header(form_frame, '🔄 Sort By')
        
        tk.Label(form_frame, text='Choose how to sort results:', bg='white', fg='#6B7280', font=('Helvetica', 9)).pack(anchor='w', pady=(0, 8))
        
        sort_dropdown = ttk.Combobox(form_frame, textvariable=self.selected_sort, state='readonly', font=('Helvetica', 10))
        sort_dropdown['values'] = self.sort_options
        sort_dropdown.pack(fill='x', pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        tk.Button(btn_frame, text='Apply Filters', command=lambda: self._apply_filters(modal, start_date_entry if self.show_date_filter else None, end_date_entry if self.show_date_filter else None, category_vars, status_var if self.show_status_filter else None), bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=20, pady=10).pack(fill='x', pady=(0, 8))
        
        tk.Button(btn_frame, text='Clear Filters', command=lambda: self._clear_filters(modal, start_date_entry if self.show_date_filter else None, end_date_entry if self.show_date_filter else None, category_vars, status_var if self.show_status_filter else None), bg=self.colors.get('warning', '#F39C12'), fg='white', relief='flat', font=('Helvetica', 11, 'bold'), padx=20, pady=10).pack(fill='x', pady=(0, 8))
        
        tk.Button(btn_frame, text='Cancel', command=modal.destroy, bg='#E5E7EB', fg='#374151', relief='flat', font=('Helvetica', 11, 'bold'), padx=20, pady=10).pack(fill='x')

    def _add_section_header(self, parent, text):
        """Add section header"""
        tk.Label(parent, text=text, bg='white', fg='#1F2937', font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 8))
        tk.Frame(parent, bg='#E5E7EB', height=1).pack(fill='x', pady=(0, 12))

    def _apply_filters(self, modal, start_date_entry, end_date_entry, category_vars, status_var):
        """Apply selected filters"""
        # Save date range
        if self.show_date_filter and start_date_entry and end_date_entry:
            self.start_date = start_date_entry.get_date()
            self.end_date = end_date_entry.get_date()
        
        # Save categories
        if self.show_category_filter:
            self.selected_categories = [cat for cat, var in category_vars.items() if var.get()]
        
        # Save status
        if self.show_status_filter and status_var:
            self.selected_status.set(status_var.get())
        
        # Build active filters dict
        self.active_filters = {}
        
        if self.show_date_filter and self.start_date and self.end_date:
            self.active_filters['date_range'] = {
                'start': self.start_date.strftime('%Y-%m-%d'),
                'end': self.end_date.strftime('%Y-%m-%d')
            }
        
        if self.show_category_filter and self.selected_categories:
            self.active_filters['categories'] = self.selected_categories.copy()
        
        if self.show_status_filter and self.selected_status.get() != 'all':
            self.active_filters['status'] = self.selected_status.get()
        
        if self.selected_sort.get() and self.selected_sort.get() != 'Relevance':
            self.active_filters['sort'] = self.selected_sort.get()
        
        # Update filter tags display
        self._update_filter_tags()
        
        # Update filters button badge
        filter_count = len(self.active_filters)
        if filter_count > 0:
            self.filters_btn.config(text=f'⚙️ Filters ({filter_count})', bg=self.colors.get('secondary', '#3498DB'), fg='white')
        else:
            self.filters_btn.config(text='⚙️ Filters', bg='#F3F4F6', fg='#374151')
        
        # Close modal
        modal.destroy()
        
        # Execute search with new filters
        self._execute_search()

    def _clear_filters(self, modal, start_date_entry, end_date_entry, category_vars, status_var):
        """Clear all filters"""
        # Reset date range
        if self.show_date_filter and start_date_entry and end_date_entry:
            start_date_entry.set_date(datetime.now())
            end_date_entry.set_date(datetime.now())
            self.start_date = None
            self.end_date = None
        
        # Reset categories
        if self.show_category_filter:
            for var in category_vars.values():
                var.set(False)
            self.selected_categories = []
        
        # Reset status
        if self.show_status_filter and status_var:
            status_var.set('all')
            self.selected_status.set('all')
        
        # Reset sort
        self.selected_sort.set(self.sort_options[0] if self.sort_options else 'Relevance')
        
        # Clear active filters
        self.active_filters = {}
        
        # Update UI
        self._update_filter_tags()
        self.filters_btn.config(text='⚙️ Filters', bg='#F3F4F6', fg='#374151')
        
        # Execute search
        self._execute_search()

    def _update_filter_tags(self):
        """Update filter tags display"""
        # Clear existing tags
        for widget in self.tags_frame.winfo_children():
            widget.destroy()
        
        # Hide frame if no filters
        if not self.active_filters:
            self.tags_frame.pack_forget()
            return
        
        # Show frame
        self.tags_frame.pack(fill='x', padx=16, pady=(0, 12))
        
        # Add tags
        tags_container = tk.Frame(self.tags_frame, bg='white')
        tags_container.pack(fill='x')
        
        # Date range tag
        if 'date_range' in self.active_filters:
            date_range = self.active_filters['date_range']
            tag_text = f"📅 {date_range['start']} to {date_range['end']}"
            self._create_filter_tag(tags_container, tag_text, 'date_range')
        
        # Category tags
        if 'categories' in self.active_filters:
            for category in self.active_filters['categories']:
                self._create_filter_tag(tags_container, f"📂 {category}", f"category_{category}")
        
        # Status tag
        if 'status' in self.active_filters:
            status = self.active_filters['status']
            self._create_filter_tag(tags_container, f"📊 {status.title()}", 'status')
        
        # Sort tag
        if 'sort' in self.active_filters:
            sort = self.active_filters['sort']
            self._create_filter_tag(tags_container, f"🔄 Sort: {sort}", 'sort')

    def _create_filter_tag(self, parent, text, filter_key):
        """Create a removable filter tag (chip)"""
        tag = tk.Frame(parent, bg='#E0E7FF', highlightthickness=1, highlightbackground='#BFDBFE')
        tag.pack(side='left', padx=(0, 8), pady=2)
        
        tk.Label(tag, text=text, bg='#E0E7FF', fg='#1E40AF', font=('Helvetica', 9)).pack(side='left', padx=(8, 4), pady=4)
        
        # Remove button
        remove_btn = tk.Label(tag, text='×', bg='#E0E7FF', fg='#1E40AF', font=('Helvetica', 12, 'bold'), cursor='hand2')
        remove_btn.pack(side='left', padx=(0, 6), pady=4)
        remove_btn.bind('<Button-1>', lambda e: self._remove_filter_tag(filter_key))

    def _remove_filter_tag(self, filter_key):
        """Remove a specific filter"""
        if filter_key == 'date_range':
            self.start_date = None
            self.end_date = None
            if 'date_range' in self.active_filters:
                del self.active_filters['date_range']
        
        elif filter_key.startswith('category_'):
            category = filter_key.replace('category_', '')
            if category in self.selected_categories:
                self.selected_categories.remove(category)
            if 'categories' in self.active_filters:
                if category in self.active_filters['categories']:
                    self.active_filters['categories'].remove(category)
                if not self.active_filters['categories']:
                    del self.active_filters['categories']
        
        elif filter_key == 'status':
            self.selected_status.set('all')
            if 'status' in self.active_filters:
                del self.active_filters['status']
        
        elif filter_key == 'sort':
            self.selected_sort.set(self.sort_options[0] if self.sort_options else 'Relevance')
            if 'sort' in self.active_filters:
                del self.active_filters['sort']
        
        # Update UI
        self._update_filter_tags()
        
        # Update filters button
        filter_count = len(self.active_filters)
        if filter_count > 0:
            self.filters_btn.config(text=f'⚙️ Filters ({filter_count})')
        else:
            self.filters_btn.config(text='⚙️ Filters', bg='#F3F4F6', fg='#374151')
        
        # Execute search
        self._execute_search()

    def get_search_text(self):
        """Get current search text"""
        text = self.search_text.get()
        return '' if text == self.placeholder else text

    def get_active_filters(self):
        """Get current active filters"""
        return self.active_filters.copy()

    def clear_search(self):
        """Clear search text"""
        self.search_text.set('')
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, self.placeholder)
        self.search_entry.config(fg='#9CA3AF')

    def reset_all(self):
        """Reset search and all filters"""
        self.clear_search()
        self.start_date = None
        self.end_date = None
        self.selected_categories = []
        self.selected_status.set('all')
        self.selected_sort.set(self.sort_options[0] if self.sort_options else 'Relevance')
        self.active_filters = {}
        self._update_filter_tags()
        self.filters_btn.config(text='⚙️ Filters', bg='#F3F4F6', fg='#374151')
        self._execute_search()
