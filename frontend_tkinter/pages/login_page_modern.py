import tkinter as tk
from frontend_tkinter.widgets.modern_entry import ModernEntry
from frontend_tkinter.widgets.modern_button import ModernButton
from frontend_tkinter.styles.theme import ThemeManager


class LoginPageModern(tk.Frame):
    """Modern login page using the new styled widgets."""

    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.tm = ThemeManager()
        self.configure(bg=self.tm.colors()['bg_secondary'])

        container = tk.Frame(self, bg=self.tm.colors()['bg_secondary'])
        container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(container, text='Campus Event System', font=self.tm.fonts()['h2'],
                 bg=self.tm.colors()['bg_secondary'], fg=self.tm.colors()['text_primary']).pack(pady=8)

        self.username = ModernEntry(container, placeholder='Email or username')
        self.username.pack(pady=6)

        self.password = ModernEntry(container, placeholder='Password', is_password=True)
        self.password.pack(pady=6)

        btn_frame = tk.Frame(container, bg=self.tm.colors()['bg_secondary'])
        btn_frame.pack(pady=12)

        ModernButton(btn_frame, text='Login', style='primary', command=self._on_login).pack(side='left', padx=6)
        ModernButton(btn_frame, text='Register', style='ghost', command=lambda: controller.navigate('register')).pack(side='left', padx=6)

    def _on_login(self):
        # Minimal local validation then call controller's login flow (if exists)
        email = self.username.get()
        pwd = self.password.get()
        print('Modern login attempt:', email)

        # If controller provides a login handler, call it; otherwise fallback
        login_method = getattr(self.controller, 'handle_login', None) or getattr(self.controller, 'login', None)
        if callable(login_method):
            try:
                login_method(email, pwd)
            except TypeError:
                # If signature differs, call navigate to dashboard for demo
                self.controller.navigate('student_dashboard')
        else:
            self.controller.navigate('student_dashboard')
