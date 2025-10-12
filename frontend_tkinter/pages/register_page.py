import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Tuple

from utils.api_client import APIClient
from utils.button_styles import ButtonStyles
from utils.validators import (
    validate_email,
    validate_phone,
    validate_password,
    validate_required_field,
    sanitize_input,
)


class RegisterPage(tk.Frame):
    """Scrollable Registration Page with real-time validation."""

    ROLES = ["STUDENT", "ORGANIZER"]

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors.get('background', '#ECF0F1'))
        self.controller = controller
        self.api = APIClient()

        # Form variables
        self.fullname_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_var = tk.StringVar()
        self.role_var = tk.StringVar(value=self.ROLES[0])
        self.dept_var = tk.StringVar()
        self.terms_var = tk.BooleanVar(value=False)

        # Validation state labels
        self._labels = {}

        # Build UI
        self._build_scrollable_form()

    # UI construction
    def _build_scrollable_form(self):
        container = tk.Frame(self, bg=self.controller.colors.get('background', '#ECF0F1'))
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=self.controller.colors.get('background', '#ECF0F1'), highlightthickness=0)
        vscroll = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)

        vscroll.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        form = tk.Frame(canvas, bg='white')
        self.form = form

        canvas.create_window((0, 0), window=form, anchor='nw')

        form.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        self._bind_mousewheel(canvas)

        # Configure grid columns - give both columns proper weight
        form.grid_columnconfigure(0, weight=0, minsize=200)  # Label column with minimum width
        form.grid_columnconfigure(1, weight=1)  # Entry column expands

        # Header
        header = tk.Label(form, text="Create your account", bg='white', fg=self.controller.colors.get('primary', '#2C3E50'), font=("Helvetica", 20, 'bold'))
        header.grid(row=0, column=0, columnspan=2, sticky='w', padx=24, pady=(24, 12))

        # Fields
        row = 1
        row = self._add_text_field("Full Name", self.fullname_var, row)
        row = self._add_text_field("Email", self.email_var, row, on_change=self._validate_email)
        row = self._add_text_field("Phone Number", self.phone_var, row, on_change=self._validate_phone)
        row = self._add_text_field("Username", self.username_var, row, on_change=self._validate_username_uniqueness)
        row = self._add_password_field("Password", self.password_var, row)
        row = self._add_confirm_password_field("Confirm Password", self.confirm_var, row)

        # Role dropdown
        tk.Label(form, text="Role", bg='white', fg='#2C3E50', font=("Helvetica", 11)).grid(row=row, column=0, sticky='nw', padx=(24, 12), pady=(8, 2))
        role_cb = ttk.Combobox(form, textvariable=self.role_var, values=self.ROLES, state='readonly')
        role_cb.grid(row=row, column=1, sticky='ew', padx=(12, 24), pady=(8, 2))
        row += 1
        self._labels['role'] = self._add_hint_label(row)
        row += 1

        # Department
        row = self._add_text_field("Department/College Name", self.dept_var, row)

        # Terms
        terms = tk.Checkbutton(form, text="I agree to the Terms & Conditions", variable=self.terms_var, bg='white', activebackground='white', command=self._validate_terms)
        terms.grid(row=row, column=0, columnspan=2, sticky='w', padx=24, pady=(8, 2))
        self._labels['terms'] = self._add_hint_label(row + 1)
        row += 2

        # Register button (Canvas-based for macOS compatibility)
        self.register_enabled = True  # Track button state
        button_container = tk.Frame(form, bg='white')
        button_container.grid(row=row, column=0, columnspan=2, sticky='ew', padx=24, pady=(8, 16))
        
        self.register_canvas = tk.Canvas(
            button_container,
            width=400,
            height=50,
            bg='white',
            highlightthickness=0
        )
        self.register_canvas.pack(fill='x', expand=True)
        
        # Draw the button rectangle
        self.register_rect = self.register_canvas.create_rectangle(
            0, 0, 400, 50,
            fill='#28a745',
            outline='',
            tags='button'
        )
        
        # Add button text
        self.register_text = self.register_canvas.create_text(
            200, 25,
            text='REGISTER',
            font=("Helvetica", 12, "bold"),
            fill='white',
            tags='button'
        )
        
        # Bind events for button interaction
        self.register_canvas.tag_bind('button', '<Button-1>', lambda e: self._on_register_clicked() if self.register_enabled else None)
        self.register_canvas.tag_bind('button', '<Enter>', self._register_hover_enter)
        self.register_canvas.tag_bind('button', '<Leave>', self._register_hover_leave)
        self.register_canvas.config(cursor='hand2')
        
        row += 1

        # Loading bar
        self.spinner = ttk.Progressbar(form, mode='indeterminate')
        self.spinner.grid(row=row, column=0, columnspan=2, sticky='ew', padx=24)
        self._hide_spinner()
        row += 1

        # Login link (Canvas-based for macOS compatibility)
        link_frame = tk.Frame(form, bg='white')
        link_frame.grid(row=row, column=0, columnspan=2, pady=(8, 24))
        tk.Label(link_frame, text="Already have an account?", bg='white', font=("Helvetica", 10)).pack(side='left')
        
        # Create canvas for login link
        login_canvas = tk.Canvas(
            link_frame,
            width=50,
            height=20,
            bg='white',
            highlightthickness=0
        )
        login_canvas.pack(side='left', padx=(6, 0))
        
        # Add login link text
        login_text = login_canvas.create_text(
            25, 10,
            text='Login',
            font=("Helvetica", 10, "underline"),
            fill='#3047ff',
            tags='login_link'
        )
        
        # Bind events
        login_canvas.tag_bind('login_link', '<Button-1>', lambda e: self.controller.navigate('login'))
        login_canvas.tag_bind('login_link', '<Enter>', lambda e: login_canvas.itemconfig(login_text, fill='#60A5FA'))
        login_canvas.tag_bind('login_link', '<Leave>', lambda e: login_canvas.itemconfig(login_text, fill='#3047ff'))
        login_canvas.config(cursor='hand2')

    def _bind_mousewheel(self, canvas: tk.Canvas):
        def _on_mousewheel(event):
            canvas.yview_scroll(-1 if event.delta > 0 else 1, 'units')
        canvas.bind_all('<MouseWheel>', _on_mousewheel)

    def _register_hover_enter(self, event):
        """Change button color on hover."""
        if self.register_enabled:
            self.register_canvas.itemconfig(self.register_rect, fill='#218838')

    def _register_hover_leave(self, event):
        """Restore button color when not hovering."""
        if self.register_enabled:
            self.register_canvas.itemconfig(self.register_rect, fill='#28a745')
        else:
            self.register_canvas.itemconfig(self.register_rect, fill='#94D3A2')

    def _add_hint_label(self, row: int) -> tk.Label:
        lbl = tk.Label(self.form, text="", bg='white', fg=self.controller.colors.get('danger', '#E74C3C'), font=("Helvetica", 9))
        lbl.grid(row=row, column=0, columnspan=2, sticky='w', padx=24, pady=(0, 0))
        return lbl

    def _add_text_field(self, label: str, var: tk.StringVar, row: int, on_change=None) -> int:
        tk.Label(self.form, text=label, bg='white', fg='#2C3E50', font=("Helvetica", 11)).grid(row=row, column=0, sticky='nw', padx=(24, 12), pady=(8, 2))
        entry = tk.Entry(self.form, textvariable=var, font=("Helvetica", 12))
        entry.grid(row=row, column=1, sticky='ew', padx=(12, 24), pady=(8, 2))
        row += 1
        hint = self._add_hint_label(row)
        key = label.lower().split()[0]
        self._labels[key] = hint
        if on_change:
            entry.bind('<KeyRelease>', lambda e: on_change())
            entry.bind('<FocusOut>', lambda e: on_change())
        else:
            entry.bind('<KeyRelease>', lambda e, v=var, k=key: self._validate_required(v.get(), k))
            entry.bind('<FocusOut>', lambda e, v=var, k=key: self._validate_required(v.get(), k))
        return row + 1

    def _add_password_field(self, label: str, var: tk.StringVar, row: int) -> int:
        tk.Label(self.form, text=label, bg='white', fg='#2C3E50', font=("Helvetica", 11)).grid(row=row, column=0, sticky='nw', padx=(24, 12), pady=(8, 2))
        entry = tk.Entry(self.form, textvariable=var, show='•', font=("Helvetica", 12))
        entry.grid(row=row, column=1, sticky='ew', padx=(12, 24), pady=(8, 2))
        row += 1
        # Compact strength meter - place in column 1 only, no full-width divider
        meter_frame = tk.Frame(self.form, bg='white')
        meter_frame.grid(row=row, column=1, sticky='ew', padx=(12, 24), pady=(2, 0))
        self.pwd_meter = ttk.Progressbar(meter_frame, maximum=100, length=150)
        self.pwd_meter.pack(side='left')
        self.pwd_label = tk.Label(meter_frame, text="", bg='white', font=("Helvetica", 9))
        self.pwd_label.pack(side='left', padx=(8, 0))
        row += 1
        hint = self._add_hint_label(row)
        self._labels['password'] = hint
        entry.bind('<KeyRelease>', lambda e: (self._validate_password(), self._update_strength()))
        entry.bind('<FocusOut>', lambda e: (self._validate_password(), self._update_strength()))
        return row + 1

    def _add_confirm_password_field(self, label: str, var: tk.StringVar, row: int) -> int:
        tk.Label(self.form, text=label, bg='white', fg='#2C3E50', font=("Helvetica", 11)).grid(row=row, column=0, sticky='nw', padx=(24, 12), pady=(8, 2))
        entry = tk.Entry(self.form, textvariable=var, show='•', font=("Helvetica", 12))
        entry.grid(row=row, column=1, sticky='ew', padx=(12, 24), pady=(8, 2))
        row += 1
        hint = self._add_hint_label(row)
        self._labels['confirm'] = hint
        entry.bind('<KeyRelease>', lambda e: self._validate_confirm())
        entry.bind('<FocusOut>', lambda e: self._validate_confirm())
        return row + 1

    # Validation helpers
    def _validate_required(self, value: str, key: str) -> bool:
        ok, err = validate_required_field(sanitize_input(value))
        self._labels.get(key, tk.Label()).config(text='' if ok else err)
        return ok

    def _validate_email(self) -> bool:
        ok, err = validate_email(self.email_var.get().strip())
        self._labels.get('email', tk.Label()).config(text='' if ok else err)
        return ok

    def _validate_phone(self) -> bool:
        ok, err = validate_phone(self.phone_var.get().strip())
        self._labels.get('phone', tk.Label()).config(text='' if ok else err)
        return ok

    def _validate_password(self) -> bool:
        ok, err = validate_password(self.password_var.get())
        self._labels.get('password', tk.Label()).config(text='' if ok else err)
        return ok

    def _validate_confirm(self) -> bool:
        match = self.password_var.get() == self.confirm_var.get()
        self._labels.get('confirm', tk.Label()).config(text='' if match else 'Passwords do not match')
        return match

    def _validate_terms(self) -> bool:
        ok = self.terms_var.get()
        self._labels.get('terms', tk.Label()).config(text='' if ok else 'You must accept Terms & Conditions')
        return ok

    def _update_strength(self):
        pwd = self.password_var.get()
        score = 0
        if len(pwd) >= 8:
            score += 30
        if any(c.islower() for c in pwd):
            score += 20
        if any(c.isupper() for c in pwd):
            score += 20
        if any(c.isdigit() for c in pwd):
            score += 20
        if any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for c in pwd):
            score += 10
        score = min(score, 100)
        self.pwd_meter['value'] = score
        if score < 40:
            text, color = 'Weak', '#DC2626'
        elif score < 70:
            text, color = 'Medium', '#D97706'
        else:
            text, color = 'Strong', '#16A34A'
        self.pwd_label.config(text=text, fg=color)

    def _validate_username_uniqueness(self):
        # Basic client validation
        uname = sanitize_input(self.username_var.get().strip())
        if not uname:
            self._labels.get('username', tk.Label()).config(text='Username is required')
            return False
        if len(uname) < 3:
            self._labels.get('username', tk.Label()).config(text='Username must be at least 3 characters')
            return False

        # Attempt server-side uniqueness check if available
        def check():
            try:
                # Expecting GET /auth/check-username?username=...
                res = self.api.get(f"auth/check-username?username={uname}")
                # If server returns {'available': true/false}
                available = bool(res.get('available', True)) if isinstance(res, dict) else True
                msg = '' if available else 'Username already taken'
            except Exception:
                # If endpoint missing, do not block registration
                msg = ''
            self._labels.get('username', tk.Label()).config(text=msg)

        threading.Thread(target=check, daemon=True).start()
        return True

    # Submission
    def _on_register_clicked(self):
        all_ok = True
        all_ok &= self._validate_required(self.fullname_var.get(), 'full')
        all_ok &= self._validate_email()
        all_ok &= self._validate_phone()
        all_ok &= self._validate_username_uniqueness()
        all_ok &= self._validate_password()
        all_ok &= self._validate_confirm()
        all_ok &= self._validate_terms()
        if not all_ok:
            messagebox.showerror("Fix errors", "Please correct the highlighted fields.")
            return

        payload = {
            'name': self.fullname_var.get().strip(),
            'email': self.email_var.get().strip(),
            'password': self.password_var.get(),
            'role': self.role_var.get().lower(),  # Convert to lowercase for backend
            'username': self.username_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'department': self.dept_var.get().strip(),
        }

        self._show_spinner()

        def worker():
            try:
                # Backend endpoint expected: POST /auth/register
                # Now returns JWT token directly
                register_res = self.api.post('auth/register', payload)
                
                # Extract user data and JWT token from registration response
                user_id = register_res.get('id')
                email = register_res.get('email')
                role = register_res.get('role')
                token = register_res.get('token', '')  # Extract JWT token
                
                # Store session with JWT token (24 hours expiration)
                from utils.session_manager import SessionManager
                session = SessionManager()
                session.store_user(
                    user_id=user_id,
                    username=email,
                    role=role,
                    token=token,
                    token_expires_in=86400  # 24 hours
                )
                
                # Set JWT token in API client for future requests
                self.api.set_auth_token(token)
                print(f"[DEBUG] JWT token stored after registration")
                
                # Navigate to dashboard
                self.after(0, lambda: (self._hide_spinner(), self.controller._go_to_dashboard()))
                messagebox.showinfo("Welcome", "Registration successful. You are now logged in.")
                
            except Exception as e:
                error_msg = str(e)
                def on_err():
                    self._hide_spinner()
                    messagebox.showerror("Registration failed", error_msg)
                self.after(0, on_err)

        threading.Thread(target=worker, daemon=True).start()

    def _show_spinner(self):
        self.spinner.grid()
        self.spinner.start(10)
        self.register_enabled = False
        self.register_canvas.itemconfig(self.register_rect, fill='#94D3A2')  # Lighter green when disabled
        self.register_canvas.config(cursor='arrow')

    def _hide_spinner(self):
        try:
            self.spinner.stop()
        except Exception:
            pass
        self.spinner.grid_remove()
        self.register_enabled = True
        self.register_canvas.itemconfig(self.register_rect, fill='#28a745')  # Restore normal green
        self.register_canvas.config(cursor='hand2')
