import tkinter as tk


class LoginPage(tk.Frame):
    """A minimal login page used as the initial page."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors['background'])
        self.controller = controller
        label = tk.Label(self, text="Login", font=("Helvetica", 24), bg=controller.colors['background'])
        label.pack(pady=20)


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Campus Event & Resource Coordination")

        # Window size and center
        width = 1200
        height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Color scheme
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'danger': '#E74C3C',
            'background': '#ECF0F1'
        }
        self.configure(bg=self.colors['background'])

        # Container for pages
        container = tk.Frame(self, bg=self.colors['background'])
        container.pack(fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.container = container
        self.pages = {}

        # Register initial pages
        self.register_page('LoginPage', LoginPage)

        # Show initial page
        self.show_page('LoginPage')

    def register_page(self, name, page_class):
        """Create and store a page frame but don't show it yet."""
        frame = page_class(self.container, self)
        frame.grid(row=0, column=0, sticky='nsew')
        self.pages[name] = frame

    def show_page(self, page_name: str):
        """Raise the requested page to the front of the container."""
        page = self.pages.get(page_name)
        if page is None:
            # If page not registered, we could raise or log. For now, do nothing.
            return
        page.tkraise()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()