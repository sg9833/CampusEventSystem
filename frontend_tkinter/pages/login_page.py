"""
Login Page - Fixed Version with No White Boxes
All buttons are properly styled, no image dependencies for buttons
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.validators import validate_required_field, sanitize_input


class LoginPage(tk.Frame):
    """Modern login page with proper button styling."""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.api = APIClient()
        self.session = SessionManager()
        self.password_visible = False
        
        # Get the images folder path
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.images_path = os.path.join(self.base_path, 'images')
        
        self._build_ui()
        self._bind_events()
    
    def _build_ui(self):
        """Build the login page UI with properly styled buttons."""
        self.pack(fill='both', expand=True)
        
        # Background image (optional - works without it)
        try:
            bg_image_path = os.path.join(self.images_path, 'background1.png')
            if os.path.exists(bg_image_path):
                self.bg_frame = Image.open(bg_image_path)
                photo = ImageTk.PhotoImage(self.bg_frame)
                self.bg_panel = tk.Label(self, image=photo)
                self.bg_panel.image = photo
                self.bg_panel.pack(fill='both', expand=True)
            else:
                self.configure(bg='#040405')
        except Exception as e:
            print(f"Background image not loaded: {e}")
            self.configure(bg='#040405')
        
        # Login Frame - Main container
        self.lgn_frame = tk.Frame(self, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=200, y=70)
        
        # Welcome heading
        self.heading = tk.Label(
            self.lgn_frame,
            text="WELCOME",
            font=('yu gothic ui', 25, "bold"),
            bg="#040405",
            fg='white',
            bd=5,
            relief=tk.FLAT
        )
        self.heading.place(x=80, y=30, width=300, height=30)
        
        # Left side decorative image (optional)
        try:
            vector_path = os.path.join(self.images_path, 'vector.png')
            if os.path.exists(vector_path):
                self.side_image = Image.open(vector_path)
                photo = ImageTk.PhotoImage(self.side_image)
                self.side_image_label = tk.Label(self.lgn_frame, image=photo, bg='#040405')
                self.side_image_label.image = photo
                self.side_image_label.place(x=5, y=100)
        except Exception as e:
            print(f"Vector image not loaded: {e}")
        
        # Sign in illustration (optional)
        try:
            signin_path = os.path.join(self.images_path, 'hyy.png')
            if os.path.exists(signin_path):
                self.sign_in_image = Image.open(signin_path)
                photo = ImageTk.PhotoImage(self.sign_in_image)
                self.sign_in_image_label = tk.Label(self.lgn_frame, image=photo, bg='#040405')
                self.sign_in_image_label.image = photo
                self.sign_in_image_label.place(x=620, y=130)
        except Exception as e:
            print(f"Sign in image not loaded: {e}")
        
        # Sign in label
        self.sign_in_label = tk.Label(
            self.lgn_frame,
            text="Sign In",
            bg="#040405",
            fg="white",
            font=("yu gothic ui", 17, "bold")
        )
        self.sign_in_label.place(x=650, y=240)
        
        # === USERNAME SECTION ===
        self.username_label = tk.Label(
            self.lgn_frame,
            text="Username",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.username_label.place(x=550, y=300)
        
        # Username entry field
        self.username_entry = tk.Entry(
            self.lgn_frame,
            highlightthickness=0,
            relief=tk.FLAT,
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui ", 12, "bold"),
            insertbackground='#6b6a69'
        )
        self.username_entry.place(x=580, y=335, width=270)
        
        # Username underline
        self.username_line = tk.Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.username_line.place(x=550, y=359)
        
        # Username icon (optional)
        try:
            username_icon_path = os.path.join(self.images_path, 'username_icon.png')
            if os.path.exists(username_icon_path):
                self.username_icon = Image.open(username_icon_path)
                photo = ImageTk.PhotoImage(self.username_icon)
                self.username_icon_label = tk.Label(self.lgn_frame, image=photo, bg='#040405')
                self.username_icon_label.image = photo
                self.username_icon_label.place(x=550, y=332)
        except Exception as e:
            print(f"Username icon not loaded: {e}")
        
        # === PASSWORD SECTION ===
        self.password_label = tk.Label(
            self.lgn_frame,
            text="Password",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.password_label.place(x=550, y=380)
        
        # Password entry field
        self.password_entry = tk.Entry(
            self.lgn_frame,
            highlightthickness=0,
            relief=tk.FLAT,
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 12, "bold"),
            show="*",
            insertbackground='#6b6a69'
        )
        self.password_entry.place(x=580, y=416, width=244)
        
        # Password underline
        self.password_line = tk.Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.password_line.place(x=550, y=440)
        
        # Password icon (optional)
        try:
            password_icon_path = os.path.join(self.images_path, 'password_icon.png')
            if os.path.exists(password_icon_path):
                self.password_icon = Image.open(password_icon_path)
                photo = ImageTk.PhotoImage(self.password_icon)
                self.password_icon_label = tk.Label(self.lgn_frame, image=photo, bg='#040405')
                self.password_icon_label.image = photo
                self.password_icon_label.place(x=550, y=414)
        except Exception as e:
            print(f"Password icon not loaded: {e}")
        
        # === PASSWORD TOGGLE BUTTON (CANVAS-BASED FOR MACOS COMPATIBILITY) ===
        self.password_visible = False  # Track password visibility
        self.toggle_canvas = tk.Canvas(
            self.lgn_frame,
            width=30,
            height=30,
            bg='#040405',
            highlightthickness=0
        )
        self.toggle_canvas.place(x=830, y=414)
        
        # Create toggle button (eye icon)
        self.toggle_text = self.toggle_canvas.create_text(
            15, 15,
            text='👁',  # Eye symbol
            font=('Arial', 14),
            fill='#6b6a69',
            tags='toggle'
        )
        
        # Bind events
        self.toggle_canvas.tag_bind('toggle', '<Button-1>', lambda e: self._toggle_password())
        self.toggle_canvas.tag_bind('toggle', '<Enter>', self._toggle_hover_enter)
        self.toggle_canvas.tag_bind('toggle', '<Leave>', self._toggle_hover_leave)
        self.toggle_canvas.config(cursor='hand2')
        
        # === LOGIN BUTTON (CANVAS-BASED FOR MACOS COMPATIBILITY) ===
        # Create canvas for custom button rendering
        self.login_enabled = True  # Track button state
        self.login_canvas = tk.Canvas(
            self.lgn_frame,
            width=300,
            height=50,
            bg='#040405',
            highlightthickness=0
        )
        self.login_canvas.place(x=550, y=460)
        
        # Draw the button rectangle
        self.login_rect = self.login_canvas.create_rectangle(
            0, 0, 300, 50,
            fill='#3047ff',
            outline='',
            tags='button'
        )
        
        # Add button text
        self.login_text = self.login_canvas.create_text(
            150, 25,
            text='LOGIN',
            font=("yu gothic ui", 13, "bold"),
            fill='white',
            tags='button'
        )
        
        # Bind click events
        self.login_canvas.tag_bind('button', '<Button-1>', lambda e: self._on_login())
        self.login_canvas.tag_bind('button', '<Enter>', self._login_hover_enter)
        self.login_canvas.tag_bind('button', '<Leave>', self._login_hover_leave)
        self.login_canvas.config(cursor='hand2')
        
        # === FORGOT PASSWORD BUTTON ===
        self.forgot_button = tk.Button(
            self.lgn_frame,
            text="Forgot Password?",
            font=("yu gothic ui", 11, "bold"),
            fg="#3047ff",
            bg="#040405",
            activebackground="#040405",
            activeforeground="#60A5FA",
            relief=tk.FLAT,
            borderwidth=0,
            cursor='hand2',
            command=self._forgot_password
        )
        self.forgot_button.place(x=640, y=515)
        
        # Hover effect
        self.forgot_button.bind('<Enter>', lambda e: self.forgot_button.config(fg='#60A5FA'))
        self.forgot_button.bind('<Leave>', lambda e: self.forgot_button.config(fg='#3047ff'))
        
        # === SIGN UP SECTION ===
        self.sign_label = tk.Label(
            self.lgn_frame,
            text="Don't have an account?",
            font=("yu gothic ui", 11, "bold"),
            relief=tk.FLAT,
            borderwidth=0,
            bg="#040405",
            fg='#4f4e4d'
        )
        self.sign_label.place(x=550, y=560)
        
        # Sign up button (text-based, no image)
        self.signup_button = tk.Button(
            self.lgn_frame,
            text="Sign Up",
            font=("yu gothic ui", 11, "bold"),
            bg='#040405',
            fg='#3047ff',
            activebackground='#040405',
            activeforeground='#60A5FA',
            relief=tk.FLAT,
            borderwidth=0,
            cursor='hand2',
            command=self._go_to_register
        )
        self.signup_button.place(x=720, y=558)
        
        # Hover effect
        self.signup_button.bind('<Enter>', lambda e: self.signup_button.config(fg='#60A5FA'))
        self.signup_button.bind('<Leave>', lambda e: self.signup_button.config(fg='#3047ff'))
    
    def _bind_events(self):
        """Bind keyboard events."""
        self.username_entry.bind("<Return>", lambda e: self._on_login())
        self.password_entry.bind("<Return>", lambda e: self._on_login())
    
    def _login_hover_enter(self, event):
        """Handle mouse hover over login button."""
        if hasattr(self, 'login_enabled') and self.login_enabled:
            self.login_canvas.itemconfig(self.login_rect, fill='#1e3acc')
    
    def _login_hover_leave(self, event):
        """Handle mouse leaving login button."""
        if hasattr(self, 'login_enabled') and self.login_enabled:
            self.login_canvas.itemconfig(self.login_rect, fill='#3047ff')
        elif hasattr(self, 'login_enabled') and not self.login_enabled:
            self.login_canvas.itemconfig(self.login_rect, fill='#475569')
    
    def _toggle_hover_enter(self, event):
        """Handle mouse hover over toggle button."""
        self.toggle_canvas.itemconfig(self.toggle_text, fill='#bdb9b1')
    
    def _toggle_hover_leave(self, event):
        """Handle mouse leaving toggle button."""
        if self.password_visible:
            self.toggle_canvas.itemconfig(self.toggle_text, fill='#3047ff')
        else:
            self.toggle_canvas.itemconfig(self.toggle_text, fill='#6b6a69')
    
    def _toggle_password(self):
        """Toggle password visibility."""
        self.password_visible = not self.password_visible
        
        if self.password_visible:
            # Show password
            self.password_entry.config(show='')
            self.toggle_canvas.itemconfig(self.toggle_text, text='○', fill='#3047ff')
        else:
            # Hide password
            self.password_entry.config(show='*')
            self.toggle_canvas.itemconfig(self.toggle_text, text='👁', fill='#6b6a69')
    
    def _forgot_password(self):
        """Handle forgot password."""
        messagebox.showinfo(
            "Forgot Password",
            "Password reset functionality will be available soon.\n\n"
            "Please contact your administrator for assistance."
        )
    
    def _go_to_register(self):
        """Navigate to registration page."""
        try:
            self.controller.navigate('register')
        except Exception as e:
            print(f"Navigation error: {e}")
            messagebox.showerror("Error", "Could not navigate to registration page")
    
    def _on_login(self):
        """Handle login button click."""
        # Get credentials
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validate inputs
        if not username:
            messagebox.showerror("Error", "Please enter your username")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter your password")
            self.password_entry.focus()
            return
        
        # Sanitize username
        username = sanitize_input(username)
        
        # Disable button and show loading state
        self.login_enabled = False
        self.login_canvas.itemconfig(self.login_rect, fill='#475569')
        self.login_canvas.itemconfig(self.login_text, text='SIGNING IN...')
        self.login_canvas.config(cursor='wait')
        
        # Start login thread
        thread = threading.Thread(
            target=self._login_thread,
            args=(username, password),
            daemon=True
        )
        thread.start()
    
    def _login_thread(self, username: str, password: str):
        """Perform login in background thread."""
        try:
            # Call API
            payload = {"email": username, "password": password}
            print(f"[DEBUG] Attempting login with email: {username}")
            print(f"[DEBUG] API endpoint: auth/login")
            print(f"[DEBUG] Payload: {payload}")
            data = self.api.post("auth/login", payload)
            print(f"[DEBUG] Login response: {data}")
            
            # Extract user data including JWT token
            user_id = data.get('id')
            email = data.get('email') or username
            role = data.get('role') or 'USER'
            token = data.get('token', '')  # Extract JWT token
            
            # Store session with JWT token
            # Token expires in 24 hours (86400 seconds)
            self.session.store_user(
                user_id=user_id,
                username=email,
                role=role,
                token=token,
                token_expires_in=86400  # 24 hours
            )
            
            # Set JWT token in API client for future requests
            self.api.set_auth_token(token)
            print(f"[DEBUG] JWT token stored and set in API client")
            
            # Success callback
            def after_success():
                self.login_enabled = True
                self.login_canvas.itemconfig(self.login_rect, fill='#3047ff')
                self.login_canvas.itemconfig(self.login_text, text='LOGIN')
                self.login_canvas.config(cursor='hand2')
                self.controller._go_to_dashboard()
            
            self.after(0, after_success)
            
        except Exception as e:
            error_msg = str(e)
            
            # Error callback
            def after_error():
                self.login_enabled = True
                self.login_canvas.itemconfig(self.login_rect, fill='#3047ff')
                self.login_canvas.itemconfig(self.login_text, text='LOGIN')
                self.login_canvas.config(cursor='hand2')
                
                # Format error message
                if "401" in error_msg or "Invalid credentials" in error_msg:
                    msg = "Invalid username or password.\nPlease try again."
                elif "Failed to connect" in error_msg:
                    msg = "Cannot connect to server.\nPlease check if the backend is running."
                elif "timed out" in error_msg:
                    msg = "Request timed out.\nPlease check your connection and try again."
                else:
                    msg = f"Login failed:\n{error_msg}"
                
                messagebox.showerror("Login Failed", msg)
            
            self.after(0, after_error)