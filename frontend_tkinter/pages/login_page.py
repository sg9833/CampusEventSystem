import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Literal

try:
	from PIL import Image, ImageTk
except Exception:
	Image = None
	ImageTk = None

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.validators import validate_required_field, sanitize_input
from utils.button_styles import ButtonStyles


class LoginPage(tk.Frame):
	"""Login Page with a centered card UI and async login flow."""

	def __init__(self, parent, controller):
		super().__init__(parent, bg=controller.colors.get('background', '#F5F6F7'))
		self.controller = controller
		self.api = APIClient()
		self.session = SessionManager()

		# State
		self._password_visible = False

		# Center container
		self._build_layout()
		self._load_remembered_user()

	def _build_layout(self):
		# Center the card using an outer container
		outer = tk.Frame(self, bg=self.controller.colors.get('background', '#F5F6F7'))
		outer.pack(expand=True, fill='both')

		# Card container
		card = tk.Frame(
			outer,
			width=400,
			height=500,
			bg='white',
			highlightthickness=1,
			highlightbackground='#E0E0E0',
		)
		card.place(relx=0.5, rely=0.5, anchor='center')

		# Allow internal layout
		for i in range(0, 12):
			card.grid_rowconfigure(i, weight=0)
		card.grid_columnconfigure(0, weight=1)

		# Logo / Title
		logo_frame = tk.Frame(card, bg='white')
		logo_frame.grid(row=0, column=0, sticky='ew', pady=(24, 8))
		self._add_logo_or_title(logo_frame)

		subtitle = tk.Label(
			card,
			text="Sign in to continue",
			bg='white',
			fg='#6B7280',
			font=("Helvetica", 11)
		)
		subtitle.grid(row=1, column=0, pady=(0, 16))

		# Error message area
		self.error_var = tk.StringVar(value="")
		self.error_label = tk.Label(
			card,
			textvariable=self.error_var,
			fg=self.controller.colors.get('danger', '#E74C3C'),
			bg='white',
			font=("Helvetica", 10)
		)
		self.error_label.grid(row=2, column=0, sticky='ew', padx=24)

		# Username/email field with icon
		user_container = tk.Frame(card, bg='white')
		user_container.grid(row=3, column=0, sticky='ew', padx=24, pady=(8, 8))
		user_container.grid_columnconfigure(1, weight=1)

		user_icon = tk.Label(user_container, text='👤', bg='white', font=("Helvetica", 12))
		user_icon.grid(row=0, column=0, padx=(0, 8))

		self.username_var = tk.StringVar()
		self.username_entry = tk.Entry(
			user_container,
			textvariable=self.username_var,
			font=("Helvetica", 12),
			relief='solid',
			bd=1
		)
		self.username_entry.grid(row=0, column=1, sticky='ew')
		self.username_entry.insert(0, "Email or Username")
		self.username_entry.bind("<FocusIn>", self._clear_placeholder)
		self.username_entry.bind("<FocusOut>", self._restore_placeholder)

		# Password field with icon + show/hide toggle
		pwd_container = tk.Frame(card, bg='white')
		pwd_container.grid(row=4, column=0, sticky='ew', padx=24, pady=(8, 8))
		pwd_container.grid_columnconfigure(1, weight=1)

		lock_icon = tk.Label(pwd_container, text='🔒', bg='white', font=("Helvetica", 12))
		lock_icon.grid(row=0, column=0, padx=(0, 8))

		self.password_var = tk.StringVar()
		self.password_entry = tk.Entry(
			pwd_container,
			textvariable=self.password_var,
			font=("Helvetica", 12),
			show='•',
			relief='solid',
			bd=1
		)
		self.password_entry.grid(row=0, column=1, sticky='ew')
		# Add placeholder text for password field
		self.password_entry.insert(0, "Password")
		self.password_entry.bind("<FocusIn>", self._clear_password_placeholder)
		self.password_entry.bind("<FocusOut>", self._restore_password_placeholder)

		self.toggle_btn = tk.Button(
			pwd_container,
			text='👁',
			font=("Helvetica", 14),
			relief='flat',
			bg='white',
			fg='#2C3E50',
			activebackground='#ECF0F1',
			activeforeground='#2C3E50',
			cursor='hand2',
			borderwidth=0,
			command=self._toggle_password
		)
		self.toggle_btn.grid(row=0, column=2, padx=(8, 0))

		# Remember me + Forgot password
		opts_container = tk.Frame(card, bg='white')
		opts_container.grid(row=5, column=0, sticky='ew', padx=24, pady=(4, 4))
		opts_container.grid_columnconfigure(0, weight=1)
		opts_container.grid_columnconfigure(1, weight=0)

		self.remember_var = tk.BooleanVar(value=False)
		remember_cb = tk.Checkbutton(
			opts_container,
			text="Remember Me",
			variable=self.remember_var,
			bg='white',
			activebackground='white'
		)
		remember_cb.grid(row=0, column=0, sticky='w')

		forgot_btn = ButtonStyles.create_link_button(
			opts_container,
			text="Forgot Password?",
			command=self._forgot_password
		)
		forgot_btn.grid(row=0, column=1, sticky='e')

		# Login button using Canvas for reliable color rendering on macOS
		login_btn_container = tk.Frame(card, bg='white')
		login_btn_container.grid(row=6, column=0, sticky='ew', padx=24, pady=(8, 8))
		
		# Create canvas-based button for guaranteed color
		canvas_btn = tk.Canvas(
			login_btn_container,
			width=400,
			height=45,
			bg='white',
			highlightthickness=0,
			cursor='hand2'
		)
		canvas_btn.pack(fill='x', expand=True)
		
		# Draw the button background
		self.login_btn_rect = canvas_btn.create_rectangle(
			0, 0, 400, 45,
			fill='#007AFF',  # Bright iOS blue
			outline='',
			tags='button_bg'
		)
		
		# Draw the button text
		self.login_btn_text = canvas_btn.create_text(
			200, 22,
			text='Login',
			fill='#FFFFFF',  # White text
			font=('Helvetica', 14, 'bold'),
			tags='button_text'
		)
		
		# Bind click event
		canvas_btn.tag_bind('button_bg', '<Button-1>', lambda e: self._on_login_clicked())
		canvas_btn.tag_bind('button_text', '<Button-1>', lambda e: self._on_login_clicked())
		canvas_btn.bind('<Button-1>', lambda e: self._on_login_clicked())
		
		# Hover effects
		def on_enter(e):
			canvas_btn.itemconfig(self.login_btn_rect, fill='#0051D5')  # Darker on hover
		def on_leave(e):
			canvas_btn.itemconfig(self.login_btn_rect, fill='#007AFF')  # Back to normal
		
		canvas_btn.bind('<Enter>', on_enter)
		canvas_btn.bind('<Leave>', on_leave)
		
		self.login_btn = canvas_btn

		# Loading spinner
		spinner_container = tk.Frame(card, bg='white')
		spinner_container.grid(row=7, column=0, sticky='ew', padx=24)
		self.spinner = ttk.Progressbar(spinner_container, mode='indeterminate')
		self.spinner.pack(fill='x')
		self._hide_spinner()

		# Divider
		divider = tk.Frame(card, bg='#F1F5F9', height=2)
		divider.grid(row=8, column=0, sticky='ew', padx=24, pady=(16, 8))

		# Register link
		reg_container = tk.Frame(card, bg='white')
		reg_container.grid(row=9, column=0, pady=(0, 8))

		reg_label = tk.Label(reg_container, text="Don't have an account?", bg='white', font=("Helvetica", 10))
		reg_label.pack(side='left')
		reg_link = ButtonStyles.create_link_button(
			reg_container,
			text="Register",
			command=lambda: self.controller.navigate('register')
		)
		reg_link.pack(side='left', padx=(6, 0))

	def _add_logo_or_title(self, parent):
		# Try to load a logo from assets/logo.png
		logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
		logo_path = os.path.abspath(logo_path)
		if Image and ImageTk and os.path.exists(logo_path):
			try:
				img = Image.open(logo_path)
				img = img.resize((64, 64))
				self._logo_img = ImageTk.PhotoImage(img)
				label = tk.Label(parent, image=self._logo_img, bg='white')
				label.pack(pady=(8, 8))
			except Exception:
				pass
		title = tk.Label(
			parent,
			text="CampusCoord",
			bg='white',
			fg=self.controller.colors.get('primary', '#2C3E50'),
			font=("Helvetica", 20, 'bold')
		)
		title.pack()

	# Placeholder helpers
	def _clear_placeholder(self, event=None):
		if self.username_entry.get().strip() == "Email or Username":
			self.username_entry.delete(0, tk.END)

	def _restore_placeholder(self, event=None):
		if not self.username_entry.get().strip():
			self.username_entry.insert(0, "Email or Username")

	def _clear_password_placeholder(self, event=None):
		"""Clear password placeholder on focus"""
		current_text = self.password_entry.get()
		if current_text == "Password":
			self.password_entry.delete(0, tk.END)
			self.password_entry.config(show='•')  # Enable password masking

	def _restore_password_placeholder(self, event=None):
		"""Restore password placeholder if empty"""
		if not self.password_entry.get():
			self.password_entry.config(show='')  # Disable masking to show placeholder
			self.password_entry.insert(0, "Password")

	def _toggle_password(self):
		"""Toggle password visibility"""
		# Don't toggle if placeholder is shown
		if self.password_entry.get() == "Password":
			return
		
		self._password_visible = not self._password_visible
		if self._password_visible:
			self.password_entry.config(show='')
			self.toggle_btn.config(text='🙈')  # Hide eye
		else:
			self.password_entry.config(show='•')
			self.toggle_btn.config(text='👁')  # Show eye

	def _forgot_password(self):
		messagebox.showinfo("Forgot Password", "Password reset is not implemented yet.")

	def _show_spinner(self):
		self.spinner.grid()
		self.spinner.start(10)
		self._set_inputs_state('disabled')

	def _hide_spinner(self):
		try:
			self.spinner.stop()
		except Exception:
			pass
		self.spinner.grid_remove()
		self._set_inputs_state('normal')

	def _set_inputs_state(self, state: Literal['normal', 'disabled']):
		try:
			self.username_entry.config(state=state)
			self.password_entry.config(state=state)
			self.toggle_btn.config(state=state)
			# Canvas button - change opacity/color for disabled state
			if state == 'disabled':
				self.login_btn.itemconfig(self.login_btn_rect, fill='#CCCCCC')
			else:
				self.login_btn.itemconfig(self.login_btn_rect, fill='#007AFF')
		except Exception:
			pass

	def _on_login_clicked(self):
		# Reset error
		self.error_var.set("")

		raw_username = self.username_var.get().strip()
		if raw_username == "Email or Username":
			raw_username = ""
		raw_password = self.password_var.get()
		if raw_password == "Password":
			raw_password = ""

		# Sanitize basic input
		username = sanitize_input(raw_username)
		password = raw_password  # don't sanitize passwords; send as-is

		# Validate required fields
		ok_user, err_user = validate_required_field(username)
		ok_pwd, err_pwd = validate_required_field(password)
		if not ok_user or not ok_pwd:
			self.error_var.set(err_user or err_pwd or "Both fields are required")
			return

		remember = self.remember_var.get()
		self._show_spinner()

		# Run network call on background thread
		t = threading.Thread(target=self._login_thread, args=(username, password, remember), daemon=True)
		t.start()

	def _login_thread(self, username: str, password: str, remember: bool):
		try:
			# Backend expects 'email' key even if UI says username/email
			payload = {"email": username, "password": password}
			data = self.api.post("auth/login", payload)
			# Success path
			user_id = data.get('id')
			email = data.get('email') or username
			role = data.get('role') or 'USER'

			# Store session; backend doesn't return token currently
			self.session.store_user(user_id=user_id, username=email, role=role, token="")

			# Optionally remember username locally
			if remember:
				self._remember_username(email)
			else:
				self._forget_username()

			# Navigate to dashboard (based on role if pages exist)
			def after_success():
				self._hide_spinner()
				# Use the controller's _go_to_dashboard method which handles role-based navigation
				self.controller._go_to_dashboard()

			self.after(0, after_success)

		except Exception as e:
			# Capture error message before inner function
			error_msg = str(e)
			
			def after_error():
				self._hide_spinner()
				msg = error_msg
				# Make common errors friendlier
				if "401" in msg or "Invalid credentials" in msg:
					msg = "Invalid email/username or password"
				elif "Failed to connect" in msg:
					msg = "Cannot reach server. Is the backend running?"
				elif "timed out" in msg:
					msg = "Request timed out. Please try again."
				self.error_var.set(msg)

			self.after(0, after_error)

	# Remember me: simple local file storage
	def _remember_file_path(self) -> str:
		root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
		return os.path.join(root, '.remember_me.txt')

	def _remember_username(self, username: str):
		try:
			with open(self._remember_file_path(), 'w', encoding='utf-8') as f:
				f.write(username)
		except Exception:
			pass

	def _forget_username(self):
		try:
			path = self._remember_file_path()
			if os.path.exists(path):
				os.remove(path)
		except Exception:
			pass

	def _load_remembered_user(self):
		try:
			path = self._remember_file_path()
			if os.path.exists(path):
				with open(path, 'r', encoding='utf-8') as f:
					saved = f.read().strip()
					if saved:
						self.username_entry.delete(0, tk.END)
						self.username_entry.insert(0, saved)
						self.remember_var.set(True)
		except Exception:
			pass

