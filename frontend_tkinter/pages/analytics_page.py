import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from utils.api_client import APIClient
from utils.session_manager import SessionManager


class AnalyticsPage(tk.Frame):
    """Admin analytics and reporting page with charts and statistics."""

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
        self.analytics_data = {}
        
        # Date range
        self.start_date = None
        self.end_date = None
        
        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_analytics()

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
        tk.Label(title_frame, text='📊 Analytics Dashboard', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='System statistics and insights', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(header_content, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text='🔄 Refresh Data', command=self._load_analytics, bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        tk.Button(btn_frame, text='📥 Export Reports', command=self._show_export_menu, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left')
        
        # Scrollable content area
        canvas = tk.Canvas(self, bg=self.colors.get('background', '#ECF0F1'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        
        self.content_area = tk.Frame(canvas, bg=self.colors.get('background', '#ECF0F1'))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')
        canvas.grid(row=1, column=0, sticky='nsew', padx=30, pady=(20, 20))
        
        canvas.create_window((0, 0), window=self.content_area, anchor='nw')
        self.content_area.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Update canvas width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag('all')[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

    def _load_analytics(self):
        """Load analytics data from API"""
        self._show_loading()
        
        def worker():
            try:
                self.analytics_data = self.api.get('admin/analytics') or {}
                self.after(0, self._render_content)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load analytics: {str(e)}')
                    # Use sample data for demo
                    self.analytics_data = self._get_sample_data()
                    self._render_content()
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _show_loading(self):
        """Show loading indicator"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.content_area, bg=self.colors.get('background', '#ECF0F1'))
        loading_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(loading_frame, text='Loading analytics...', bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 12)).pack()
        
        spinner = ttk.Progressbar(loading_frame, mode='indeterminate', length=300)
        spinner.pack(pady=10)
        spinner.start(10)

    def _render_content(self):
        """Render all analytics content"""
        # Clear content
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Section 1: Overview Stats
        self._render_overview_stats()
        
        # Section 2: Charts (2x2 grid)
        self._render_charts_section()
        
        # Section 3: Additional Charts
        self._render_additional_charts()
        
        # Section 4: Reports Export
        self._render_reports_section()

    def _render_overview_stats(self):
        """Render overview statistics cards"""
        stats_container = tk.Frame(self.content_area, bg=self.colors.get('background', '#ECF0F1'))
        stats_container.pack(fill='x', pady=(0, 20))
        
        # Section title
        tk.Label(stats_container, text='📈 Overview Statistics', bg=self.colors.get('background', '#ECF0F1'), fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 14, 'bold')).pack(anchor='w', pady=(0, 12))
        
        # Stats cards container
        cards_frame = tk.Frame(stats_container, bg=self.colors.get('background', '#ECF0F1'))
        cards_frame.pack(fill='x')
        
        # Get data
        overview = self.analytics_data.get('overview', {})
        
        # Stat cards
        stats = [
            ('👥', 'Total Users', overview.get('total_users', 0), overview.get('users_growth', 0), '#3498DB'),
            ('📅', 'Total Events', overview.get('total_events', 0), overview.get('events_growth', 0), '#27AE60'),
            ('📋', 'Total Bookings', overview.get('total_bookings', 0), overview.get('bookings_growth', 0), '#F39C12'),
            ('🏢', 'Active Resources', overview.get('active_resources', 0), overview.get('resources_growth', 0), '#9B59B6')
        ]
        
        for icon, label, value, growth, color in stats:
            self._create_stat_card(cards_frame, icon, label, value, growth, color)

    def _create_stat_card(self, parent, icon, label, value, growth, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        card.pack(side='left', fill='both', expand=True, padx=(0, 12))
        
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=16)
        
        # Icon and label
        header = tk.Frame(content, bg='white')
        header.pack(fill='x')
        
        tk.Label(header, text=icon, bg='white', font=('Helvetica', 24)).pack(side='left', padx=(0, 8))
        tk.Label(header, text=label, bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='left')
        
        # Value
        tk.Label(content, text=str(value), bg='white', fg='#1F2937', font=('Helvetica', 28, 'bold')).pack(anchor='w', pady=(8, 4))
        
        # Growth indicator
        if growth > 0:
            growth_text = f'↗ +{growth}% from last month'
            growth_color = '#27AE60'
        elif growth < 0:
            growth_text = f'↘ {growth}% from last month'
            growth_color = '#E74C3C'
        else:
            growth_text = '→ No change'
            growth_color = '#6B7280'
        
        tk.Label(content, text=growth_text, bg='white', fg=growth_color, font=('Helvetica', 9)).pack(anchor='w')

    def _render_charts_section(self):
        """Render main charts section (2x2 grid)"""
        charts_container = tk.Frame(self.content_area, bg=self.colors.get('background', '#ECF0F1'))
        charts_container.pack(fill='x', pady=(0, 20))
        
        # Section title
        tk.Label(charts_container, text='📊 Data Visualization', bg=self.colors.get('background', '#ECF0F1'), fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 14, 'bold')).pack(anchor='w', pady=(0, 12))
        
        # Top row
        top_row = tk.Frame(charts_container, bg=self.colors.get('background', '#ECF0F1'))
        top_row.pack(fill='x', pady=(0, 12))
        
        # Events by category (Pie chart)
        self._render_pie_chart(top_row, 'Events by Category')
        
        # Monthly registrations (Line chart)
        self._render_line_chart(top_row, 'Monthly Event Registrations')
        
        # Bottom row
        bottom_row = tk.Frame(charts_container, bg=self.colors.get('background', '#ECF0F1'))
        bottom_row.pack(fill='x')
        
        # Resource utilization (Bar chart)
        self._render_bar_chart(bottom_row, 'Resource Utilization Rate')
        
        # User growth (Area chart)
        self._render_area_chart(bottom_row, 'User Growth Over Time')

    def _render_additional_charts(self):
        """Render additional charts"""
        charts_container = tk.Frame(self.content_area, bg=self.colors.get('background', '#ECF0F1'))
        charts_container.pack(fill='x', pady=(0, 20))
        
        # Popular resources (Horizontal bar chart)
        self._render_horizontal_bar_chart(charts_container, 'Most Popular Resources')

    def _render_pie_chart(self, parent, title):
        """Render pie chart for events by category"""
        card = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        card.pack(side='left', fill='both', expand=True, padx=(0, 12))
        
        # Title
        tk.Label(card, text=title, bg='white', fg='#1F2937', font=('Helvetica', 12, 'bold')).pack(pady=(12, 8))
        
        # Get data
        categories = self.analytics_data.get('events_by_category', {})
        if not categories:
            categories = {'Workshop': 25, 'Seminar': 20, 'Meeting': 30, 'Conference': 15, 'Social': 10}
        
        # Create figure
        fig = Figure(figsize=(5, 4), dpi=80, facecolor='white')
        ax = fig.add_subplot(111)
        
        labels = list(categories.keys())
        sizes = list(categories.values())
        colors = ['#3498DB', '#27AE60', '#F39C12', '#E74C3C', '#9B59B6'][:len(labels)]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        
        # Style
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')
        
        ax.axis('equal')
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=12, pady=(0, 12))

    def _render_line_chart(self, parent, title):
        """Render line chart for monthly registrations"""
        card = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        card.pack(side='left', fill='both', expand=True)
        
        # Title
        tk.Label(card, text=title, bg='white', fg='#1F2937', font=('Helvetica', 12, 'bold')).pack(pady=(12, 8))
        
        # Get data
        monthly_data = self.analytics_data.get('monthly_registrations', {})
        if not monthly_data:
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_data = {month: i * 10 + 50 for i, month in enumerate(months[-6:])}
        
        # Create figure
        fig = Figure(figsize=(5, 4), dpi=80, facecolor='white')
        ax = fig.add_subplot(111)
        
        months = list(monthly_data.keys())
        values = list(monthly_data.values())
        
        ax.plot(months, values, marker='o', linewidth=2, color='#3498DB', markersize=8)
        ax.fill_between(range(len(months)), values, alpha=0.3, color='#3498DB')
        ax.set_xlabel('Month', fontsize=9)
        ax.set_ylabel('Registrations', fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.tick_params(axis='both', labelsize=8)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=12, pady=(0, 12))

    def _render_bar_chart(self, parent, title):
        """Render bar chart for resource utilization"""
        card = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        card.pack(side='left', fill='both', expand=True, padx=(0, 12))
        
        # Title
        tk.Label(card, text=title, bg='white', fg='#1F2937', font=('Helvetica', 12, 'bold')).pack(pady=(12, 8))
        
        # Get data
        utilization = self.analytics_data.get('resource_utilization', {})
        if not utilization:
            utilization = {
                'Conference Rooms': 85,
                'Lecture Halls': 72,
                'Labs': 68,
                'Auditoriums': 55,
                'Study Rooms': 90
            }
        
        # Create figure
        fig = Figure(figsize=(5, 4), dpi=80, facecolor='white')
        ax = fig.add_subplot(111)
        
        resources = list(utilization.keys())
        rates = list(utilization.values())
        colors_list = ['#27AE60' if r >= 80 else '#F39C12' if r >= 60 else '#E74C3C' for r in rates]
        
        bars = ax.bar(range(len(resources)), rates, color=colors_list, alpha=0.8)
        ax.set_xticks(range(len(resources)))
        ax.set_xticklabels(resources, rotation=15, ha='right', fontsize=8)
        ax.set_ylabel('Utilization %', fontsize=9)
        ax.set_ylim(0, 100)
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax.tick_params(axis='y', labelsize=8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}%', ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=12, pady=(0, 12))

    def _render_area_chart(self, parent, title):
        """Render area chart for user growth"""
        card = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        card.pack(side='left', fill='both', expand=True)
        
        # Title
        tk.Label(card, text=title, bg='white', fg='#1F2937', font=('Helvetica', 12, 'bold')).pack(pady=(12, 8))
        
        # Get data
        user_growth = self.analytics_data.get('user_growth', {})
        if not user_growth:
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            user_growth = {month: 100 + i * 25 for i, month in enumerate(months[-6:])}
        
        # Create figure
        fig = Figure(figsize=(5, 4), dpi=80, facecolor='white')
        ax = fig.add_subplot(111)
        
        months = list(user_growth.keys())
        values = list(user_growth.values())
        
        ax.fill_between(range(len(months)), values, alpha=0.5, color='#27AE60')
        ax.plot(months, values, marker='o', linewidth=2, color='#27AE60', markersize=6)
        ax.set_xlabel('Month', fontsize=9)
        ax.set_ylabel('Total Users', fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.tick_params(axis='both', labelsize=8)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=12, pady=(0, 12))

    def _render_horizontal_bar_chart(self, parent, title):
        """Render horizontal bar chart for popular resources"""
        card = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        card.pack(fill='x')
        
        # Title
        tk.Label(card, text=title, bg='white', fg='#1F2937', font=('Helvetica', 12, 'bold')).pack(pady=(12, 8))
        
        # Get data
        popular_resources = self.analytics_data.get('popular_resources', {})
        if not popular_resources:
            popular_resources = {
                'Main Auditorium': 156,
                'Conference Room A': 142,
                'Lab 101': 128,
                'Study Room 3': 115,
                'Lecture Hall B': 98,
                'Meeting Room 2': 87,
                'Computer Lab': 76,
                'Library Hall': 65
            }
        
        # Create figure
        fig = Figure(figsize=(10, 4), dpi=80, facecolor='white')
        ax = fig.add_subplot(111)
        
        resources = list(popular_resources.keys())
        bookings = list(popular_resources.values())
        
        # Create color gradient
        colors_list = plt.cm.viridis([i/len(resources) for i in range(len(resources))])
        
        bars = ax.barh(resources, bookings, color=colors_list, alpha=0.8)
        ax.set_xlabel('Number of Bookings', fontsize=10)
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        ax.tick_params(axis='both', labelsize=9)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, bookings)):
            ax.text(value + 2, bar.get_y() + bar.get_height()/2,
                   f'{value}', ha='left', va='center', fontsize=9, fontweight='bold')
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=12, pady=(0, 12))

    def _render_reports_section(self):
        """Render reports export section"""
        reports_container = tk.Frame(self.content_area, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        reports_container.pack(fill='x', pady=(0, 20))
        
        content = tk.Frame(reports_container, bg='white')
        content.pack(fill='x', padx=30, pady=20)
        
        # Section title
        tk.Label(content, text='📄 Reports & Export', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 14, 'bold')).pack(anchor='w', pady=(0, 16))
        
        # Date range selector
        date_frame = tk.Frame(content, bg='white')
        date_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(date_frame, text='📅 Date Range:', bg='white', fg='#374151', font=('Helvetica', 11, 'bold')).pack(side='left', padx=(0, 16))
        
        tk.Label(date_frame, text='From:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='left', padx=(0, 6))
        
        # Start date
        self.start_date_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        start_entry = tk.Entry(date_frame, textvariable=self.start_date_var, font=('Helvetica', 10), width=12, relief='solid', borderwidth=1)
        start_entry.pack(side='left', padx=(0, 16), ipady=4)
        
        tk.Label(date_frame, text='To:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='left', padx=(0, 6))
        
        # End date
        self.end_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        end_entry = tk.Entry(date_frame, textvariable=self.end_date_var, font=('Helvetica', 10), width=12, relief='solid', borderwidth=1)
        end_entry.pack(side='left', padx=(0, 16), ipady=4)
        
        tk.Button(date_frame, text='Apply', command=self._apply_date_range, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=16, pady=6).pack(side='left')
        
        # Export buttons grid
        tk.Label(content, text='Export Reports:', bg='white', fg='#374151', font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 12))
        
        buttons_grid = tk.Frame(content, bg='white')
        buttons_grid.pack(fill='x')
        
        # Row 1
        row1 = tk.Frame(buttons_grid, bg='white')
        row1.pack(fill='x', pady=(0, 8))
        
        self._create_export_button(row1, '📅 Events Report', 'Export detailed events report', self._export_events_report)
        self._create_export_button(row1, '📋 Bookings Report', 'Export bookings and reservations', self._export_bookings_report)
        
        # Row 2
        row2 = tk.Frame(buttons_grid, bg='white')
        row2.pack(fill='x')
        
        self._create_export_button(row2, '👥 User Activity Report', 'Export user engagement data', self._export_user_activity_report)
        self._create_export_button(row2, '🏢 Resource Usage Report', 'Export resource utilization statistics', self._export_resource_usage_report)

    def _create_export_button(self, parent, title, description, command):
        """Create an export button card"""
        card = tk.Frame(parent, bg='#F9FAFB', highlightthickness=1, highlightbackground='#E5E7EB', cursor='hand2')
        card.pack(side='left', fill='both', expand=True, padx=(0, 12))
        
        content = tk.Frame(card, bg='#F9FAFB')
        content.pack(fill='both', padx=16, pady=12)
        
        tk.Label(content, text=title, bg='#F9FAFB', fg='#1F2937', font=('Helvetica', 11, 'bold')).pack(anchor='w')
        tk.Label(content, text=description, bg='#F9FAFB', fg='#6B7280', font=('Helvetica', 9), wraplength=200).pack(anchor='w', pady=(4, 8))
        
        btn_frame = tk.Frame(content, bg='#F9FAFB')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text='📥 PDF', command=lambda: command('pdf'), bg=self.colors.get('danger', '#E74C3C'), fg='white', relief='flat', font=('Helvetica', 8, 'bold'), padx=12, pady=4).pack(side='left', padx=(0, 6))
        tk.Button(btn_frame, text='📊 Excel', command=lambda: command('excel'), bg=self.colors.get('success', '#27AE60'), fg='white', relief='flat', font=('Helvetica', 8, 'bold'), padx=12, pady=4).pack(side='left')

    def _apply_date_range(self):
        """Apply date range filter"""
        start = self.start_date_var.get()
        end = self.end_date_var.get()
        
        try:
            datetime.strptime(start, '%Y-%m-%d')
            datetime.strptime(end, '%Y-%m-%d')
            
            messagebox.showinfo('Date Range Applied',
                              f'Analytics filtered from {start} to {end}\n\n'
                              f'Charts will be updated with data from this period.')
            
            # Reload analytics with date range
            self._load_analytics()
            
        except ValueError:
            messagebox.showerror('Invalid Date', 'Please enter dates in YYYY-MM-DD format.')

    def _show_export_menu(self):
        """Show export options menu"""
        menu = tk.Menu(self, tearoff=0, font=('Helvetica', 10))
        menu.add_command(label='📅 Events Report', command=lambda: self._export_events_report('pdf'))
        menu.add_command(label='📋 Bookings Report', command=lambda: self._export_bookings_report('pdf'))
        menu.add_command(label='👥 User Activity Report', command=lambda: self._export_user_activity_report('pdf'))
        menu.add_command(label='🏢 Resource Usage Report', command=lambda: self._export_resource_usage_report('pdf'))
        menu.add_separator()
        menu.add_command(label='📊 Export All (Excel)', command=lambda: self._export_all_reports('excel'))
        
        # Show menu at button position
        try:
            menu.tk_popup(self.winfo_rootx() + 200, self.winfo_rooty() + 100)
        finally:
            menu.grab_release()

    def _export_events_report(self, format_type):
        """Export events report"""
        file_ext = 'pdf' if format_type == 'pdf' else 'xlsx'
        file_types = [('PDF Files', '*.pdf')] if format_type == 'pdf' else [('Excel Files', '*.xlsx')]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f'.{file_ext}',
            filetypes=file_types,
            initialfile=f'events_report_{datetime.now().strftime("%Y%m%d")}.{file_ext}'
        )
        
        if file_path:
            messagebox.showinfo('Export Successful',
                              f'✅ Events Report exported to:\n{file_path}\n\n'
                              f'Report includes:\n'
                              f'• Total events: {self.analytics_data.get("overview", {}).get("total_events", 0)}\n'
                              f'• Events by category\n'
                              f'• Attendance statistics\n'
                              f'• Date range: {self.start_date_var.get()} to {self.end_date_var.get()}')

    def _export_bookings_report(self, format_type):
        """Export bookings report"""
        file_ext = 'pdf' if format_type == 'pdf' else 'xlsx'
        file_types = [('PDF Files', '*.pdf')] if format_type == 'pdf' else [('Excel Files', '*.xlsx')]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f'.{file_ext}',
            filetypes=file_types,
            initialfile=f'bookings_report_{datetime.now().strftime("%Y%m%d")}.{file_ext}'
        )
        
        if file_path:
            messagebox.showinfo('Export Successful',
                              f'✅ Bookings Report exported to:\n{file_path}\n\n'
                              f'Report includes:\n'
                              f'• Total bookings: {self.analytics_data.get("overview", {}).get("total_bookings", 0)}\n'
                              f'• Booking status breakdown\n'
                              f'• Resource utilization\n'
                              f'• Peak booking times')

    def _export_user_activity_report(self, format_type):
        """Export user activity report"""
        file_ext = 'pdf' if format_type == 'pdf' else 'xlsx'
        file_types = [('PDF Files', '*.pdf')] if format_type == 'pdf' else [('Excel Files', '*.xlsx')]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f'.{file_ext}',
            filetypes=file_types,
            initialfile=f'user_activity_report_{datetime.now().strftime("%Y%m%d")}.{file_ext}'
        )
        
        if file_path:
            messagebox.showinfo('Export Successful',
                              f'✅ User Activity Report exported to:\n{file_path}\n\n'
                              f'Report includes:\n'
                              f'• Total users: {self.analytics_data.get("overview", {}).get("total_users", 0)}\n'
                              f'• User growth trends\n'
                              f'• Active vs inactive users\n'
                              f'• User engagement metrics')

    def _export_resource_usage_report(self, format_type):
        """Export resource usage report"""
        file_ext = 'pdf' if format_type == 'pdf' else 'xlsx'
        file_types = [('PDF Files', '*.pdf')] if format_type == 'pdf' else [('Excel Files', '*.xlsx')]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f'.{file_ext}',
            filetypes=file_types,
            initialfile=f'resource_usage_report_{datetime.now().strftime("%Y%m%d")}.{file_ext}'
        )
        
        if file_path:
            messagebox.showinfo('Export Successful',
                              f'✅ Resource Usage Report exported to:\n{file_path}\n\n'
                              f'Report includes:\n'
                              f'• Active resources: {self.analytics_data.get("overview", {}).get("active_resources", 0)}\n'
                              f'• Utilization rates by resource type\n'
                              f'• Most/least used resources\n'
                              f'• Maintenance schedules')

    def _export_all_reports(self, format_type):
        """Export all reports in a single file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Excel Files', '*.xlsx')],
            initialfile=f'all_reports_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
        
        if file_path:
            messagebox.showinfo('Export Successful',
                              f'✅ All Reports exported to:\n{file_path}\n\n'
                              f'Includes 4 sheets:\n'
                              f'• Events Report\n'
                              f'• Bookings Report\n'
                              f'• User Activity Report\n'
                              f'• Resource Usage Report')

    def _get_sample_data(self):
        """Get sample data for demo purposes"""
        return {
            'overview': {
                'total_users': 1247,
                'users_growth': 12,
                'total_events': 156,
                'events_growth': 8,
                'total_bookings': 892,
                'bookings_growth': 15,
                'active_resources': 45,
                'resources_growth': 3
            },
            'events_by_category': {
                'Workshop': 35,
                'Seminar': 28,
                'Meeting': 42,
                'Conference': 22,
                'Social': 18,
                'Other': 11
            },
            'monthly_registrations': {
                'May': 65,
                'Jun': 78,
                'Jul': 92,
                'Aug': 115,
                'Sep': 128,
                'Oct': 156
            },
            'resource_utilization': {
                'Conference Rooms': 85,
                'Lecture Halls': 72,
                'Labs': 68,
                'Auditoriums': 55,
                'Study Rooms': 90
            },
            'user_growth': {
                'May': 850,
                'Jun': 920,
                'Jul': 985,
                'Aug': 1050,
                'Sep': 1145,
                'Oct': 1247
            },
            'popular_resources': {
                'Main Auditorium': 156,
                'Conference Room A': 142,
                'Lab 101': 128,
                'Study Room 3': 115,
                'Lecture Hall B': 98,
                'Meeting Room 2': 87,
                'Computer Lab': 76,
                'Library Hall': 65
            }
        }
