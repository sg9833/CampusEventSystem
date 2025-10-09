"""
Accessible Example Page - Campus Event Management System
Version: 1.9.0

This page demonstrates all accessibility features:
- Keyboard navigation
- Screen reader support
- Focus indicators
- High contrast mode
- Font scaling
- Accessible forms
- Color contrast validation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.accessibility import (
    get_keyboard_navigator,
    get_screen_reader_announcer,
    get_color_validator,
    get_font_scaler,
    get_focus_indicator,
    get_high_contrast_mode,
    AccessibleForm
)


class AccessibleDemoPage(tk.Frame):
    """
    Demo page showcasing all accessibility features.
    
    Features demonstrated:
    1. Keyboard navigation with visible focus
    2. Screen reader announcements
    3. Color contrast validation
    4. Font scaling
    5. High contrast mode
    6. Accessible form
    """
    
    def __init__(self, parent, navigate=None):
        """
        Initialize demo page.
        
        Args:
            parent: Parent widget
            navigate: Navigation callback
        """
        super().__init__(parent, bg="white")
        
        self.navigate = navigate
        self.loaded = False
        
        # Initialize accessibility features
        self.root = parent.winfo_toplevel()
        self.keyboard_nav = get_keyboard_navigator(self.root)
        self.announcer = get_screen_reader_announcer(self.root)
        self.color_validator = get_color_validator()
        self.font_scaler = get_font_scaler(self.root)
        self.focus_indicator = get_focus_indicator(self.root)
        self.high_contrast = get_high_contrast_mode(self.root)
    
    def load_page(self):
        """Lazy load page content."""
        if not self.loaded:
            print("[ACCESSIBILITY DEMO] Loading page...")
            self._create_ui()
            self.announcer.announce_page_change("Accessibility Demo")
            self.loaded = True
    
    def _create_ui(self):
        """Create demo UI."""
        # Main container with scrollbar
        main_canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Header
        self._create_header(scrollable_frame)
        
        # Section 1: Keyboard Navigation Demo
        self._create_keyboard_section(scrollable_frame)
        
        # Section 2: Screen Reader Demo
        self._create_screen_reader_section(scrollable_frame)
        
        # Section 3: Color Contrast Demo
        self._create_color_contrast_section(scrollable_frame)
        
        # Section 4: Font Scaling Demo
        self._create_font_scaling_section(scrollable_frame)
        
        # Section 5: High Contrast Mode Demo
        self._create_high_contrast_section(scrollable_frame)
        
        # Section 6: Accessible Form Demo
        self._create_accessible_form_section(scrollable_frame)
        
        # Bind mouse wheel for scrolling
        main_canvas.bind_all("<MouseWheel>", lambda e: main_canvas.yview_scroll(-1 * (e.delta // 120), "units"))
    
    def _create_header(self, parent):
        """Create page header."""
        header = tk.Frame(parent, bg="#3498db", height=100)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(
            header,
            text="♿ Accessibility Features Demo",
            font=("Arial", 24, "bold"),
            bg="#3498db",
            fg="white",
            pady=20
        )
        title.pack()
        self.font_scaler.register_widget(title)
        
        subtitle = tk.Label(
            header,
            text="Keyboard-only navigation | Screen reader support | WCAG AA compliant",
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            pady=10
        )
        subtitle.pack()
        self.font_scaler.register_widget(subtitle)
        
        # Register header for high contrast
        self.high_contrast.register_widget(header, "default")
        self.high_contrast.register_widget(title, "default")
        self.high_contrast.register_widget(subtitle, "default")
    
    def _create_section_title(self, parent, text, icon=""):
        """Create section title."""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill=tk.X, padx=40, pady=(20, 10))
        
        title = tk.Label(
            frame,
            text=f"{icon} {text}",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#2c3e50",
            anchor='w'
        )
        title.pack(fill=tk.X)
        self.font_scaler.register_widget(title)
        self.high_contrast.register_widget(frame, "default")
        self.high_contrast.register_widget(title, "default")
        
        # Separator
        separator = tk.Frame(parent, bg="#bdc3c7", height=2)
        separator.pack(fill=tk.X, padx=40, pady=10)
    
    def _create_keyboard_section(self, parent):
        """Create keyboard navigation demo section."""
        self._create_section_title(parent, "Keyboard Navigation", "⌨️")
        
        container = tk.Frame(parent, bg="white")
        container.pack(fill=tk.X, padx=60, pady=10)
        self.high_contrast.register_widget(container, "default")
        
        # Description
        desc = tk.Label(
            container,
            text="Try navigating with Tab, Shift+Tab, Enter, and Escape keys:",
            font=("Arial", 12),
            bg="white",
            fg="#34495e",
            anchor='w',
            wraplength=700,
            justify=tk.LEFT
        )
        desc.pack(fill=tk.X, pady=10)
        self.font_scaler.register_widget(desc)
        self.high_contrast.register_widget(desc, "default")
        
        # Demo widgets
        widgets_frame = tk.Frame(container, bg="white")
        widgets_frame.pack(fill=tk.X, pady=20)
        self.high_contrast.register_widget(widgets_frame, "default")
        
        # Text entries
        for i in range(3):
            entry_frame = tk.Frame(widgets_frame, bg="white")
            entry_frame.pack(fill=tk.X, pady=5)
            self.high_contrast.register_widget(entry_frame, "default")
            
            label = tk.Label(
                entry_frame,
                text=f"Field {i+1}:",
                font=("Arial", 11),
                bg="white",
                fg="#2c3e50",
                width=10,
                anchor='w'
            )
            label.pack(side=tk.LEFT, padx=5)
            self.font_scaler.register_widget(label)
            self.high_contrast.register_widget(label, "default")
            
            entry = tk.Entry(
                entry_frame,
                font=("Arial", 11),
                relief=tk.SOLID,
                borderwidth=1
            )
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self.focus_indicator.add_focus_ring(entry)
            self.font_scaler.register_widget(entry)
            self.high_contrast.register_widget(entry, "entry")
        
        # Buttons
        button_frame = tk.Frame(widgets_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=10)
        self.high_contrast.register_widget(button_frame, "default")
        
        submit_btn = tk.Button(
            button_frame,
            text="Submit (Enter)",
            command=lambda: self._on_demo_submit("Keyboard"),
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        submit_btn.pack(side=tk.LEFT, padx=5)
        self.focus_indicator.add_focus_ring(submit_btn)
        self.font_scaler.register_widget(submit_btn)
        self.high_contrast.register_widget(submit_btn, "button")
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel (Escape)",
            command=lambda: self.announcer.announce("Cancelled"),
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        self.focus_indicator.add_focus_ring(cancel_btn)
        self.font_scaler.register_widget(cancel_btn)
        self.high_contrast.register_widget(cancel_btn, "button")
        
        help_btn = tk.Button(
            button_frame,
            text="Shortcuts (F1)",
            command=self.keyboard_nav._show_help,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 11),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        help_btn.pack(side=tk.LEFT, padx=5)
        self.focus_indicator.add_focus_ring(help_btn)
        self.font_scaler.register_widget(help_btn)
        self.high_contrast.register_widget(help_btn, "button")
        
        # Set tab order
        all_widgets = []
        for child in widgets_frame.winfo_children():
            if isinstance(child, tk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, (tk.Entry, tk.Button)):
                        all_widgets.append(widget)
        
        self.keyboard_nav.set_tab_order(all_widgets)
        self.keyboard_nav.bind_enter(widgets_frame, lambda: self._on_demo_submit("Keyboard"))
        self.keyboard_nav.bind_escape(widgets_frame, lambda: self.announcer.announce("Cancelled"))
    
    def _create_screen_reader_section(self, parent):
        """Create screen reader demo section."""
        self._create_section_title(parent, "Screen Reader Support", "🔊")
        
        container = tk.Frame(parent, bg="white")
        container.pack(fill=tk.X, padx=60, pady=10)
        self.high_contrast.register_widget(container, "default")
        
        desc = tk.Label(
            container,
            text="Click buttons to hear screen reader announcements (check console):",
            font=("Arial", 12),
            bg="white",
            fg="#34495e",
            anchor='w',
            wraplength=700,
            justify=tk.LEFT
        )
        desc.pack(fill=tk.X, pady=10)
        self.font_scaler.register_widget(desc)
        self.high_contrast.register_widget(desc, "default")
        
        button_frame = tk.Frame(container, bg="white")
        button_frame.pack(fill=tk.X, pady=10)
        self.high_contrast.register_widget(button_frame, "default")
        
        announcements = [
            ("Polite Announcement", "polite", "This is a polite announcement", "#3498db"),
            ("Assertive Alert", "assertive", "Important: This interrupts!", "#e74c3c"),
            ("Success Message", "success", "Operation completed successfully", "#2ecc71"),
            ("Error Message", "error", "An error occurred", "#e74c3c"),
            ("Loading State", "loading", "Loading data...", "#f39c12")
        ]
        
        for text, ann_type, message, color in announcements:
            btn = tk.Button(
                button_frame,
                text=text,
                command=lambda m=message, t=ann_type: self._make_announcement(m, t),
                bg=color,
                fg="white",
                font=("Arial", 10),
                padx=15,
                pady=8,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.focus_indicator.add_focus_ring(btn, color=color)
            self.font_scaler.register_widget(btn)
            self.high_contrast.register_widget(btn, "button")
        
        # Recent announcements log
        log_frame = tk.Frame(container, bg="#ecf0f1", relief=tk.SOLID, borderwidth=1)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.high_contrast.register_widget(log_frame, "default")
        
        log_title = tk.Label(
            log_frame,
            text="Recent Announcements:",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
            anchor='w'
        )
        log_title.pack(fill=tk.X, padx=10, pady=5)
        self.font_scaler.register_widget(log_title)
        self.high_contrast.register_widget(log_title, "default")
        
        self.announcement_log = tk.Text(
            log_frame,
            height=5,
            font=("Courier", 10),
            bg="white",
            fg="#2c3e50",
            relief=tk.FLAT,
            state='disabled'
        )
        self.announcement_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.font_scaler.register_widget(self.announcement_log)
        self.high_contrast.register_widget(self.announcement_log, "entry")
    
    def _make_announcement(self, message, ann_type):
        """Make screen reader announcement."""
        if ann_type == "polite":
            self.announcer.announce(message, priority="polite")
        elif ann_type == "assertive":
            self.announcer.announce(message, priority="assertive")
        elif ann_type == "success":
            self.announcer.announce_success(message)
        elif ann_type == "error":
            self.announcer.announce_error(message)
        elif ann_type == "loading":
            self.announcer.announce_loading(message)
        
        # Update log
        self._update_announcement_log()
    
    def _update_announcement_log(self):
        """Update announcement log display."""
        recent = self.announcer.get_recent_announcements(5)
        
        self.announcement_log.config(state='normal')
        self.announcement_log.delete('1.0', tk.END)
        
        for announcement in reversed(recent):
            time = announcement['timestamp']
            priority = announcement['priority'].upper()
            message = announcement['message']
            self.announcement_log.insert(tk.END, f"[{time}] [{priority}] {message}\n")
        
        self.announcement_log.config(state='disabled')
    
    def _create_color_contrast_section(self, parent):
        """Create color contrast demo section."""
        self._create_section_title(parent, "Color Contrast Validation", "🎨")
        
        container = tk.Frame(parent, bg="white")
        container.pack(fill=tk.X, padx=60, pady=10)
        self.high_contrast.register_widget(container, "default")
        
        desc = tk.Label(
            container,
            text="Color combinations validated for WCAG AA compliance (4.5:1 ratio):",
            font=("Arial", 12),
            bg="white",
            fg="#34495e",
            anchor='w',
            wraplength=700,
            justify=tk.LEFT
        )
        desc.pack(fill=tk.X, pady=10)
        self.font_scaler.register_widget(desc)
        self.high_contrast.register_widget(desc, "default")
        
        # Color samples
        samples_frame = tk.Frame(container, bg="white")
        samples_frame.pack(fill=tk.X, pady=10)
        self.high_contrast.register_widget(samples_frame, "default")
        
        color_pairs = [
            ("Black on White", "#000000", "#FFFFFF"),
            ("Blue on White", "#3498db", "#FFFFFF"),
            ("White on Blue", "#FFFFFF", "#3498db"),
            ("Dark Gray on White", "#2c3e50", "#FFFFFF"),
            ("White on Red", "#FFFFFF", "#e74c3c"),
        ]
        
        for name, fg, bg in color_pairs:
            ratio = self.color_validator.calculate_ratio(fg, bg)
            passes = self.color_validator.check_contrast(fg, bg)
            
            sample_frame = tk.Frame(samples_frame, bg="white")
            sample_frame.pack(fill=tk.X, pady=5)
            
            # Color swatch
            swatch = tk.Label(
                sample_frame,
                text="Sample Text",
                font=("Arial", 12, "bold"),
                bg=bg,
                fg=fg,
                width=15,
                relief=tk.SOLID,
                borderwidth=1,
                padx=10,
                pady=5
            )
            swatch.pack(side=tk.LEFT, padx=5)
            self.font_scaler.register_widget(swatch)
            
            # Info
            status = "✓ PASS" if passes else "✗ FAIL"
            status_color = "#2ecc71" if passes else "#e74c3c"
            
            info = tk.Label(
                sample_frame,
                text=f"{name}: {ratio:.2f}:1 {status}",
                font=("Arial", 11),
                bg="white",
                fg=status_color,
                anchor='w'
            )
            info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            self.font_scaler.register_widget(info)
            self.high_contrast.register_widget(info, "default")
    
    def _create_font_scaling_section(self, parent):
        """Create font scaling demo section."""
        self._create_section_title(parent, "Font Size Scaling", "🔤")
        
        container = tk.Frame(parent, bg="white")
        container.pack(fill=tk.X, padx=60, pady=10)
        self.high_contrast.register_widget(container, "default")
        
        desc = tk.Label(
            container,
            text="Adjust font size for better readability (80% - 200%):",
            font=("Arial", 12),
            bg="white",
            fg="#34495e",
            anchor='w',
            wraplength=700,
            justify=tk.LEFT
        )
        desc.pack(fill=tk.X, pady=10)
        self.font_scaler.register_widget(desc)
        self.high_contrast.register_widget(desc, "default")
        
        # Controls
        controls_frame = tk.Frame(container, bg="white")
        controls_frame.pack(fill=tk.X, pady=10)
        self.high_contrast.register_widget(controls_frame, "default")
        
        # Decrease button
        decrease_btn = tk.Button(
            controls_frame,
            text="− Decrease (Ctrl+-)",
            command=self._decrease_font,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        decrease_btn.pack(side=tk.LEFT, padx=5)
        self.focus_indicator.add_focus_ring(decrease_btn)
        self.high_contrast.register_widget(decrease_btn, "button")
        
        # Scale label
        self.scale_label = tk.Label(
            controls_frame,
            text=f"100%",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2c3e50",
            width=10
        )
        self.scale_label.pack(side=tk.LEFT, padx=20)
        self.font_scaler.register_widget(self.scale_label)
        self.high_contrast.register_widget(self.scale_label, "default")
        
        # Increase button
        increase_btn = tk.Button(
            controls_frame,
            text="+ Increase (Ctrl++)",
            command=self._increase_font,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        increase_btn.pack(side=tk.LEFT, padx=5)
        self.focus_indicator.add_focus_ring(increase_btn)
        self.high_contrast.register_widget(increase_btn, "button")
        
        # Reset button
        reset_btn = tk.Button(
            controls_frame,
            text="Reset (Ctrl+0)",
            command=self._reset_font,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        self.focus_indicator.add_focus_ring(reset_btn)
        self.high_contrast.register_widget(reset_btn, "button")
        
        # Sample text at different sizes
        sample_frame = tk.Frame(container, bg="white")
        sample_frame.pack(fill=tk.X, pady=10)
        self.high_contrast.register_widget(sample_frame, "default")
        
        for style in ['title', 'heading', 'body', 'small']:
            sample = tk.Label(
                sample_frame,
                text=f"This is {style} text - adjusts with font scaling",
                font=self.font_scaler.get_font(style),
                bg="white",
                fg="#2c3e50",
                anchor='w'
            )
            sample.pack(fill=tk.X, pady=2)
            self.font_scaler.register_widget(sample)
            self.high_contrast.register_widget(sample, "default")
    
    def _increase_font(self):
        """Increase font size."""
        self.font_scaler.increase_font()
        self._update_scale_label()
        self.announcer.announce(f"Font size increased to {int(self.font_scaler.scale_factor * 100)}%")
    
    def _decrease_font(self):
        """Decrease font size."""
        self.font_scaler.decrease_font()
        self._update_scale_label()
        self.announcer.announce(f"Font size decreased to {int(self.font_scaler.scale_factor * 100)}%")
    
    def _reset_font(self):
        """Reset font size."""
        self.font_scaler.reset_font()
        self._update_scale_label()
        self.announcer.announce("Font size reset to 100%")
    
    def _update_scale_label(self):
        """Update scale percentage label."""
        percentage = int(self.font_scaler.scale_factor * 100)
        self.scale_label.config(text=f"{percentage}%")
    
    def _create_high_contrast_section(self, parent):
        """Create high contrast mode demo section."""
        self._create_section_title(parent, "High Contrast Mode", "🌓")
        
        container = tk.Frame(parent, bg="white")
        container.pack(fill=tk.X, padx=60, pady=10)
        self.high_contrast.register_widget(container, "default")
        
        desc = tk.Label(
            container,
            text="Toggle high contrast mode for better visibility (WCAG AAA compliant):",
            font=("Arial", 12),
            bg="white",
            fg="#34495e",
            anchor='w',
            wraplength=700,
            justify=tk.LEFT
        )
        desc.pack(fill=tk.X, pady=10)
        self.font_scaler.register_widget(desc)
        self.high_contrast.register_widget(desc, "default")
        
        # Toggle button
        self.hc_button = tk.Button(
            container,
            text="🌓 Toggle High Contrast (Ctrl+H)",
            command=self._toggle_high_contrast,
            bg="#34495e",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=15,
            cursor="hand2"
        )
        self.hc_button.pack(pady=10)
        self.focus_indicator.add_focus_ring(self.hc_button)
        self.font_scaler.register_widget(self.hc_button)
        self.high_contrast.register_widget(self.hc_button, "button")
        
        # Status
        self.hc_status = tk.Label(
            container,
            text="High Contrast Mode: OFF",
            font=("Arial", 11),
            bg="white",
            fg="#7f8c8d"
        )
        self.hc_status.pack(pady=5)
        self.font_scaler.register_widget(self.hc_status)
        self.high_contrast.register_widget(self.hc_status, "default")
    
    def _toggle_high_contrast(self):
        """Toggle high contrast mode."""
        self.high_contrast.toggle()
        
        if self.high_contrast.enabled:
            self.hc_status.config(text="High Contrast Mode: ON")
            self.announcer.announce("High contrast mode enabled")
        else:
            self.hc_status.config(text="High Contrast Mode: OFF")
            self.announcer.announce("High contrast mode disabled")
    
    def _create_accessible_form_section(self, parent):
        """Create accessible form demo section."""
        self._create_section_title(parent, "Accessible Form", "📝")
        
        container = tk.Frame(parent, bg="white")
        container.pack(fill=tk.X, padx=60, pady=10)
        self.high_contrast.register_widget(container, "default")
        
        desc = tk.Label(
            container,
            text="Complete accessible form with keyboard navigation and validation:",
            font=("Arial", 12),
            bg="white",
            fg="#34495e",
            anchor='w',
            wraplength=700,
            justify=tk.LEFT
        )
        desc.pack(fill=tk.X, pady=10)
        self.font_scaler.register_widget(desc)
        self.high_contrast.register_widget(desc, "default")
        
        # Create accessible form
        form = AccessibleForm(
            parent=container,
            title="Event Registration Form",
            navigator=self.keyboard_nav,
            announcer=self.announcer,
            focus_indicator=self.focus_indicator
        )
        form.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add fields
        form.add_field(
            label="Full Name",
            name="name",
            required=True,
            placeholder="Enter your full name"
        )
        
        form.add_field(
            label="Email Address",
            name="email",
            required=True,
            placeholder="your.email@example.com"
        )
        
        form.add_field(
            label="Event Category",
            name="category",
            widget_type="combobox",
            options=["Academic", "Sports", "Cultural", "Technical", "Other"]
        )
        
        form.add_field(
            label="Additional Comments",
            name="comments",
            widget_type="text"
        )
        
        # Add buttons
        form.add_buttons(
            submit_text="Register",
            cancel_text="Clear Form",
            show_cancel=True
        )
        
        # Set callbacks
        form.on_submit(self._on_form_submit)
        form.on_cancel(form.clear)
        
        # Register form for high contrast
        self.high_contrast.register_widget(form, "default")
    
    def _on_form_submit(self, data):
        """Handle form submission."""
        print(f"[FORM] Submitted data: {data}")
        
        # Show success message
        messagebox.showinfo(
            "Success",
            f"Form submitted successfully!\n\nData:\n{data}"
        )
        
        self.announcer.announce_success("Form submitted successfully")
    
    def _on_demo_submit(self, section):
        """Handle demo button submit."""
        self.announcer.announce_success(f"{section} demo submitted")
        messagebox.showinfo("Demo", f"{section} section submitted!")


def main():
    """Run standalone demo."""
    root = tk.Tk()
    root.title("Accessibility Demo - Campus Event Management")
    root.geometry("900x800")
    root.configure(bg="white")
    
    # Create demo page
    demo = AccessibleDemoPage(root)
    demo.pack(fill=tk.BOTH, expand=True)
    demo.load_page()
    
    # Create menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # Accessibility menu
    access_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Accessibility", menu=access_menu)
    
    access_menu.add_command(
        label="Increase Font Size (Ctrl++)",
        command=demo.font_scaler.increase_font
    )
    access_menu.add_command(
        label="Decrease Font Size (Ctrl+-)",
        command=demo.font_scaler.decrease_font
    )
    access_menu.add_command(
        label="Reset Font Size (Ctrl+0)",
        command=demo.font_scaler.reset_font
    )
    access_menu.add_separator()
    access_menu.add_command(
        label="Toggle High Contrast (Ctrl+H)",
        command=demo.high_contrast.toggle
    )
    access_menu.add_separator()
    access_menu.add_command(
        label="Keyboard Shortcuts (F1)",
        command=demo.keyboard_nav._show_help
    )
    
    # Register shortcuts
    demo.keyboard_nav.register_shortcut(
        '<Control-plus>',
        demo.font_scaler.increase_font,
        "Increase font size"
    )
    demo.keyboard_nav.register_shortcut(
        '<Control-minus>',
        demo.font_scaler.decrease_font,
        "Decrease font size"
    )
    demo.keyboard_nav.register_shortcut(
        '<Control-0>',
        demo.font_scaler.reset_font,
        "Reset font size"
    )
    demo.keyboard_nav.register_shortcut(
        '<Control-h>',
        demo.high_contrast.toggle,
        "Toggle high contrast mode"
    )
    
    print("\n" + "="*60)
    print("♿ ACCESSIBILITY DEMO")
    print("="*60)
    print("\nKeyboard Shortcuts:")
    print("  F1           - Show keyboard shortcuts help")
    print("  Tab          - Next field")
    print("  Shift+Tab    - Previous field")
    print("  Enter        - Submit form")
    print("  Escape       - Cancel/Close")
    print("  Ctrl++       - Increase font size")
    print("  Ctrl+-       - Decrease font size")
    print("  Ctrl+0       - Reset font size")
    print("  Ctrl+H       - Toggle high contrast mode")
    print("\nFeatures Demonstrated:")
    print("  ✓ Keyboard navigation")
    print("  ✓ Screen reader support")
    print("  ✓ Color contrast validation")
    print("  ✓ Font scaling")
    print("  ✓ High contrast mode")
    print("  ✓ Accessible forms")
    print("  ✓ Focus indicators")
    print("\nTest with:")
    print("  • Keyboard-only navigation (no mouse)")
    print("  • Screen reader (NVDA/JAWS/VoiceOver)")
    print("  • Large fonts (200%)")
    print("  • High contrast mode")
    print("="*60 + "\n")
    
    root.mainloop()


if __name__ == "__main__":
    main()
