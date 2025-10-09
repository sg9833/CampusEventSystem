import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime, timedelta

from utils.api_client import APIClient
from utils.session_manager import SessionManager


class NotificationsPage(tk.Frame):
    """User notifications page with real-time updates."""

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
        self.notifications = []
        self.filtered_notifications = []
        
        # Filter
        self.filter_var = tk.StringVar(value='all')
        
        # Auto-refresh
        self.auto_refresh_enabled = True
        self.refresh_interval = 30000  # 30 seconds
        
        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_notifications()
        self._start_auto_refresh()

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
        tk.Label(title_frame, text='🔔 Notifications', bg='white', fg=self.colors.get('primary', '#2C3E50'), font=('Helvetica', 20, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Stay updated with your activity', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(header_content, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text='🔄 Refresh', command=self._load_notifications, bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left', padx=(0, 8))
        tk.Button(btn_frame, text='✓ Mark All Read', command=self._mark_all_read, bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6).pack(side='left')
        
        # Filter bar
        filter_frame = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
        filter_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=(20, 0))
        
        filter_content = tk.Frame(filter_frame, bg='white')
        filter_content.pack(fill='x', padx=20, pady=12)
        
        # Notification count
        self.count_label = tk.Label(filter_content, text='Loading...', bg='white', fg='#6B7280', font=('Helvetica', 11, 'bold'))
        self.count_label.pack(side='left')
        
        # Filter buttons
        filter_buttons = tk.Frame(filter_content, bg='white')
        filter_buttons.pack(side='right')
        
        tk.Label(filter_buttons, text='Show:', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(side='left', padx=(0, 8))
        
        self.all_btn = tk.Button(filter_buttons, text='All', command=lambda: self._apply_filter('all'), bg=self.colors.get('secondary', '#3498DB'), fg='white', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6)
        self.all_btn.pack(side='left', padx=(0, 6))
        
        self.unread_btn = tk.Button(filter_buttons, text='Unread', command=lambda: self._apply_filter('unread'), bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6)
        self.unread_btn.pack(side='left', padx=(0, 6))
        
        self.read_btn = tk.Button(filter_buttons, text='Read', command=lambda: self._apply_filter('read'), bg='#F3F4F6', fg='#374151', relief='flat', font=('Helvetica', 9, 'bold'), padx=12, pady=6)
        self.read_btn.pack(side='left')
        
        # Scrollable content area
        canvas = tk.Canvas(self, bg=self.colors.get('background', '#ECF0F1'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        
        self.content_area = tk.Frame(canvas, bg=self.colors.get('background', '#ECF0F1'))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='ns')
        canvas.grid(row=2, column=0, sticky='nsew', padx=30, pady=(12, 20))
        
        canvas.create_window((0, 0), window=self.content_area, anchor='nw')
        self.content_area.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Update canvas width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag('all')[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

    def _load_notifications(self):
        """Load notifications from API"""
        self._show_loading()
        
        def worker():
            try:
                self.notifications = self.api.get('notifications') or []
                self.after(0, self._apply_filter_and_render)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to load notifications: {str(e)}')
                    # Use sample data for demo
                    self.notifications = self._get_sample_notifications()
                    self._apply_filter_and_render()
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _show_loading(self):
        """Show loading indicator"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.content_area, bg=self.colors.get('background', '#ECF0F1'))
        loading_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(loading_frame, text='Loading notifications...', bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 12)).pack()
        
        spinner = ttk.Progressbar(loading_frame, mode='indeterminate', length=300)
        spinner.pack(pady=10)
        spinner.start(10)

    def _apply_filter(self, filter_type):
        """Apply notification filter"""
        self.filter_var.set(filter_type)
        
        # Update button styles
        self.all_btn.config(bg='#F3F4F6' if filter_type != 'all' else self.colors.get('secondary', '#3498DB'),
                           fg='#374151' if filter_type != 'all' else 'white')
        self.unread_btn.config(bg='#F3F4F6' if filter_type != 'unread' else self.colors.get('secondary', '#3498DB'),
                              fg='#374151' if filter_type != 'unread' else 'white')
        self.read_btn.config(bg='#F3F4F6' if filter_type != 'read' else self.colors.get('secondary', '#3498DB'),
                            fg='#374151' if filter_type != 'read' else 'white')
        
        self._apply_filter_and_render()

    def _apply_filter_and_render(self):
        """Filter notifications and render"""
        filter_type = self.filter_var.get()
        
        if filter_type == 'all':
            self.filtered_notifications = self.notifications.copy()
        elif filter_type == 'unread':
            self.filtered_notifications = [n for n in self.notifications if not n.get('read', False)]
        elif filter_type == 'read':
            self.filtered_notifications = [n for n in self.notifications if n.get('read', False)]
        
        self._render_notifications()

    def _render_notifications(self):
        """Render notifications grouped by date"""
        # Clear content
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Update count
        total = len(self.notifications)
        unread = len([n for n in self.notifications if not n.get('read', False)])
        
        if unread > 0:
            self.count_label.config(text=f'🔔 {unread} unread of {total} notification{"s" if total != 1 else ""}')
        else:
            self.count_label.config(text=f'✅ All caught up! ({total} notification{"s" if total != 1 else ""})')
        
        if not self.filtered_notifications:
            # Empty state
            empty_frame = tk.Frame(self.content_area, bg='white', highlightthickness=1, highlightbackground='#E5E7EB')
            empty_frame.pack(fill='both', expand=True, pady=20)
            
            icon = '✅' if self.filter_var.get() == 'unread' else '📭'
            text = 'No unread notifications!' if self.filter_var.get() == 'unread' else 'No notifications found'
            
            tk.Label(empty_frame, text=icon, bg='white', font=('Helvetica', 48)).pack(pady=(40, 10))
            tk.Label(empty_frame, text=text, bg='white', fg='#374151', font=('Helvetica', 14, 'bold')).pack()
            tk.Label(empty_frame, text='You\'re all caught up!', bg='white', fg='#6B7280', font=('Helvetica', 10)).pack(pady=(4, 40))
            
            return
        
        # Group notifications by date
        grouped = self._group_notifications_by_date()
        
        # Render groups
        for group_name, notifications in grouped.items():
            if not notifications:
                continue
            
            # Group header
            group_header = tk.Frame(self.content_area, bg=self.colors.get('background', '#ECF0F1'))
            group_header.pack(fill='x', pady=(0, 8))
            
            tk.Label(group_header, text=group_name, bg=self.colors.get('background', '#ECF0F1'), fg='#6B7280', font=('Helvetica', 11, 'bold')).pack(anchor='w')
            
            # Notifications in group
            for notification in notifications:
                self._create_notification_card(notification)

    def _group_notifications_by_date(self):
        """Group notifications by date (Today, Yesterday, Earlier)"""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        groups = {
            'Today': [],
            'Yesterday': [],
            'Earlier': []
        }
        
        for notification in self.filtered_notifications:
            notif_date = self._parse_date(notification.get('created_at', ''))
            
            if notif_date:
                if notif_date == today:
                    groups['Today'].append(notification)
                elif notif_date == yesterday:
                    groups['Yesterday'].append(notification)
                else:
                    groups['Earlier'].append(notification)
            else:
                groups['Earlier'].append(notification)
        
        return groups

    def _create_notification_card(self, notification):
        """Create a notification card"""
        is_read = notification.get('read', False)
        notif_type = notification.get('type', 'general')
        
        # Card background
        bg_color = 'white' if is_read else '#EFF6FF'
        border_color = '#E5E7EB' if is_read else '#BFDBFE'
        
        card = tk.Frame(self.content_area, bg=bg_color, highlightthickness=1, highlightbackground=border_color)
        card.pack(fill='x', pady=(0, 8))
        
        content = tk.Frame(card, bg=bg_color)
        content.pack(fill='x', padx=16, pady=12)
        
        # Left section (icon + content)
        left_section = tk.Frame(content, bg=bg_color)
        left_section.pack(side='left', fill='both', expand=True)
        
        # Icon and main content
        main_row = tk.Frame(left_section, bg=bg_color)
        main_row.pack(fill='x')
        
        # Icon
        icon_frame = tk.Frame(main_row, bg=bg_color)
        icon_frame.pack(side='left', padx=(0, 12))
        
        icon, icon_bg = self._get_notification_icon(notif_type)
        icon_container = tk.Frame(icon_frame, bg=icon_bg, width=40, height=40)
        icon_container.pack()
        icon_container.pack_propagate(False)
        tk.Label(icon_container, text=icon, bg=icon_bg, font=('Helvetica', 18)).pack(expand=True)
        
        # Content
        text_frame = tk.Frame(main_row, bg=bg_color)
        text_frame.pack(side='left', fill='both', expand=True)
        
        # Title
        title_text = notification.get('title', 'Notification')
        if not is_read:
            title_text = '● ' + title_text
        
        title_label = tk.Label(text_frame, text=title_text, bg=bg_color, fg='#1F2937', font=('Helvetica', 11, 'bold'), anchor='w', justify='left')
        title_label.pack(anchor='w', fill='x')
        
        # Message
        message = notification.get('message', '')
        if message:
            message_label = tk.Label(text_frame, text=message, bg=bg_color, fg='#6B7280', font=('Helvetica', 10), anchor='w', justify='left', wraplength=600)
            message_label.pack(anchor='w', pady=(4, 0), fill='x')
        
        # Timestamp
        timestamp = self._format_timestamp(notification.get('created_at', ''))
        tk.Label(text_frame, text=timestamp, bg=bg_color, fg='#9CA3AF', font=('Helvetica', 8)).pack(anchor='w', pady=(4, 0))
        
        # Related action link
        action_data = notification.get('action_data', {})
        if action_data:
            action_text = action_data.get('text', 'View Details')
            action_link = tk.Label(text_frame, text=f'→ {action_text}', bg=bg_color, fg=self.colors.get('secondary', '#3498DB'), font=('Helvetica', 9, 'underline'), cursor='hand2')
            action_link.pack(anchor='w', pady=(6, 0))
            action_link.bind('<Button-1>', lambda e: self._handle_action(notification))
        
        # Right section (action buttons)
        right_section = tk.Frame(content, bg=bg_color)
        right_section.pack(side='right', padx=(12, 0))
        
        # Mark as read button
        if not is_read:
            read_btn = tk.Button(right_section, text='✓', command=lambda: self._mark_as_read(notification), bg='#E0E7FF', fg=self.colors.get('secondary', '#3498DB'), relief='flat', font=('Helvetica', 10, 'bold'), width=3, height=1)
            read_btn.pack(pady=(0, 4))
            
            # Tooltip
            self._create_tooltip(read_btn, 'Mark as read')
        
        # Delete button
        delete_btn = tk.Button(right_section, text='🗑️', command=lambda: self._delete_notification(notification), bg='#FEF2F2', fg=self.colors.get('danger', '#E74C3C'), relief='flat', font=('Helvetica', 10), width=3, height=1)
        delete_btn.pack()
        
        # Tooltip
        self._create_tooltip(delete_btn, 'Delete')

    def _get_notification_icon(self, notif_type):
        """Get icon and background color based on notification type"""
        icons = {
            'event_registration': ('🎉', '#DBEAFE'),
            'event_approval': ('✅', '#D1FAE5'),
            'event_rejection': ('❌', '#FEE2E2'),
            'booking_approval': ('📋', '#D1FAE5'),
            'booking_rejection': ('🚫', '#FEE2E2'),
            'event_reminder': ('⏰', '#FEF3C7'),
            'event_cancellation': ('⚠️', '#FEE2E2'),
            'resource_change': ('🔄', '#E0E7FF'),
            'general': ('📢', '#F3F4F6')
        }
        
        return icons.get(notif_type, icons['general'])

    def _create_tooltip(self, widget, text):
        """Create a simple tooltip"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, bg='#1F2937', fg='white', font=('Helvetica', 8), padx=8, pady=4)
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    def _mark_as_read(self, notification):
        """Mark a notification as read"""
        notif_id = notification.get('id')
        
        def worker():
            try:
                self.api.put(f'notifications/{notif_id}/read', {})
                
                # Update local data
                for n in self.notifications:
                    if n.get('id') == notif_id:
                        n['read'] = True
                        break
                
                self.after(0, self._apply_filter_and_render)
            except Exception as e:
                def show_error():
                    messagebox.showerror('Error', f'Failed to mark as read: {str(e)}')
                self.after(0, show_error)
        
        threading.Thread(target=worker, daemon=True).start()

    def _delete_notification(self, notification):
        """Delete a notification"""
        notif_id = notification.get('id')
        
        result = messagebox.askyesno('Delete Notification',
                                     'Delete this notification?\n\nThis action cannot be undone.')
        
        if result:
            def worker():
                try:
                    self.api.delete(f'notifications/{notif_id}')
                    
                    # Update local data
                    self.notifications = [n for n in self.notifications if n.get('id') != notif_id]
                    
                    self.after(0, self._apply_filter_and_render)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to delete notification: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _mark_all_read(self):
        """Mark all notifications as read"""
        unread_count = len([n for n in self.notifications if not n.get('read', False)])
        
        if unread_count == 0:
            messagebox.showinfo('All Read', 'All notifications are already marked as read!')
            return
        
        result = messagebox.askyesno('Mark All Read',
                                     f'Mark all {unread_count} unread notification{"s" if unread_count > 1 else ""} as read?')
        
        if result:
            def worker():
                try:
                    self.api.put('notifications/mark-all-read', {})
                    
                    # Update local data
                    for n in self.notifications:
                        n['read'] = True
                    
                    def show_success():
                        messagebox.showinfo('Success', f'✅ Marked {unread_count} notification{"s" if unread_count > 1 else ""} as read!')
                        self._apply_filter_and_render()
                    
                    self.after(0, show_success)
                except Exception as e:
                    def show_error():
                        messagebox.showerror('Error', f'Failed to mark all as read: {str(e)}')
                    self.after(0, show_error)
            
            threading.Thread(target=worker, daemon=True).start()

    def _handle_action(self, notification):
        """Handle notification action click"""
        action_data = notification.get('action_data', {})
        action_type = action_data.get('type', '')
        action_id = action_data.get('id', '')
        
        # Show appropriate page or action based on type
        if action_type == 'event':
            messagebox.showinfo('Action', f'Navigate to Event Details (ID: {action_id})')
        elif action_type == 'booking':
            messagebox.showinfo('Action', f'Navigate to Booking Details (ID: {action_id})')
        elif action_type == 'resource':
            messagebox.showinfo('Action', f'Navigate to Resource Details (ID: {action_id})')
        else:
            messagebox.showinfo('Action', 'Action link clicked!')

    def _start_auto_refresh(self):
        """Start automatic refresh timer"""
        if self.auto_refresh_enabled:
            self._load_notifications()
            self.after(self.refresh_interval, self._start_auto_refresh)

    def _parse_date(self, date_str):
        """Parse date string to date object"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str[:10] if len(date_str) >= 10 else date_str, '%Y-%m-%d').date()
        except:
            return None

    def _format_timestamp(self, timestamp_str):
        """Format timestamp for display"""
        if not timestamp_str:
            return 'Just now'
        
        try:
            timestamp = datetime.strptime(timestamp_str[:19] if len(timestamp_str) >= 19 else timestamp_str, '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            diff = now - timestamp
            
            if diff.seconds < 60:
                return 'Just now'
            elif diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
            elif diff.seconds < 86400:
                hours = diff.seconds // 3600
                return f'{hours} hour{"s" if hours > 1 else ""} ago'
            elif diff.days == 1:
                return 'Yesterday at ' + timestamp.strftime('%I:%M %p')
            elif diff.days < 7:
                return f'{diff.days} days ago'
            else:
                return timestamp.strftime('%b %d, %Y at %I:%M %p')
        except:
            return timestamp_str

    def _get_sample_notifications(self):
        """Get sample notifications for demo"""
        now = datetime.now()
        
        return [
            {
                'id': 1,
                'type': 'event_approval',
                'title': 'Event Approved',
                'message': 'Your event "Tech Workshop 2024" has been approved by admin.',
                'created_at': now.strftime('%Y-%m-%d %H:%M:%S'),
                'read': False,
                'action_data': {'type': 'event', 'id': 123, 'text': 'View Event'}
            },
            {
                'id': 2,
                'type': 'booking_approval',
                'title': 'Booking Confirmed',
                'message': 'Your booking for Conference Room A on Oct 15 has been confirmed.',
                'created_at': (now - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
                'read': False,
                'action_data': {'type': 'booking', 'id': 456, 'text': 'View Booking'}
            },
            {
                'id': 3,
                'type': 'event_reminder',
                'title': 'Event Reminder',
                'message': 'Reminder: "Student Meetup" starts tomorrow at 10:00 AM.',
                'created_at': (now - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'),
                'read': False,
                'action_data': {'type': 'event', 'id': 789, 'text': 'View Details'}
            },
            {
                'id': 4,
                'type': 'event_registration',
                'title': 'Registration Successful',
                'message': 'You have successfully registered for "Coding Competition".',
                'created_at': (now - timedelta(days=1, hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
                'read': True,
                'action_data': {'type': 'event', 'id': 234, 'text': 'View Event'}
            },
            {
                'id': 5,
                'type': 'resource_change',
                'title': 'Resource Availability Updated',
                'message': 'Lab 101 is now available for booking on your requested dates.',
                'created_at': (now - timedelta(days=1, hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                'read': True,
                'action_data': {'type': 'resource', 'id': 567, 'text': 'Book Now'}
            },
            {
                'id': 6,
                'type': 'event_cancellation',
                'title': 'Event Cancelled',
                'message': 'Unfortunately, "Workshop Series" has been cancelled by the organizer.',
                'created_at': (now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
                'read': True,
                'action_data': {}
            },
            {
                'id': 7,
                'type': 'booking_rejection',
                'title': 'Booking Rejected',
                'message': 'Your booking request for Auditorium has been rejected. Reason: Time conflict.',
                'created_at': (now - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'),
                'read': True,
                'action_data': {'type': 'booking', 'id': 890, 'text': 'View Details'}
            },
            {
                'id': 8,
                'type': 'general',
                'title': 'System Update',
                'message': 'The system will undergo maintenance on Oct 20 from 2:00 AM to 4:00 AM.',
                'created_at': (now - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
                'read': True,
                'action_data': {}
            }
        ]

    def destroy(self):
        """Clean up when page is destroyed"""
        self.auto_refresh_enabled = False
        super().destroy()
