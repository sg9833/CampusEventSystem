import os
import sys

# Allow importing frontend_tkinter package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'frontend_tkinter'))

from main import CampusEventApp
from config import USE_MODERN_LOGIN

print('USE_MODERN_LOGIN flag is', USE_MODERN_LOGIN)

# Inspect the page class mapping by initializing app partially
app = CampusEventApp()
app._initialize_pages()
login_cls = app.page_classes.get('login')
print('Configured login page class:', login_cls)

# Don't start the mainloop
app.destroy()
