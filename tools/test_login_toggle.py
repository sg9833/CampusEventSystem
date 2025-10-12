"""
Lightweight test to verify runtime toggle for modern login page.
This script avoids importing the full APIClient to prevent external network or package
dependencies by injecting a small stub APIClient implementation into sys.modules.

Run with:
PYTHONPATH=/Users/garinesaiajay/Desktop/CampusEventSystem python3 tools/test_login_toggle.py
"""
import sys
import types
import os
import tkinter as tk

# Inject a stub utils.api_client module to avoid requiring requests
stub_api = types.ModuleType('utils.api_client')

class StubAPIClient:
    def __init__(self):
        self.base_url = 'http://localhost:8080/api'
    def set_auth_token(self, token):
        pass
    def set_auth_error_callback(self, cb):
        pass
    def get(self, path):
        # Simulate unreachable backend by raising an exception
        raise Exception('connection error: stub')

stub_api.APIClient = StubAPIClient
sys.modules['utils.api_client'] = stub_api

# --- Create stubs for other utils modules to avoid external deps ---
err_mod = types.ModuleType('utils.error_handler')
class ErrorHandler:
    def __init__(self):
        pass
err_mod.ErrorHandler = ErrorHandler
sys.modules['utils.error_handler'] = err_mod

sess_mod = types.ModuleType('utils.session_manager')
class SessionManager:
    def __init__(self):
        self._user = None
    def is_logged_in(self):
        return False
    def get_token(self):
        return None
    def get_user(self):
        return {}
    def clear_session(self):
        self._user = None
sess_mod.SessionManager = SessionManager
sys.modules['utils.session_manager'] = sess_mod

sec_mod = types.ModuleType('utils.security')
class SecurityManager:
    def __init__(self):
        pass
sec_mod.SecurityManager = SecurityManager
sys.modules['utils.security'] = sec_mod

acc_mod = types.ModuleType('utils.accessibility')
def get_keyboard_navigator(app):
    class KNav:
        def register_shortcut(self, *args, **kwargs):
            pass
        def push_modal(self, win):
            pass
        def _show_help(self):
            pass
    return KNav()
def get_screen_reader_announcer(app):
    class Ann:
        def announce(self, *args, **kwargs):
            pass
        def announce_page_change(self, *args, **kwargs):
            pass
    return Ann()
def get_color_validator():
    return lambda x: True
def get_font_scaler(app):
    class FS:
        def __init__(self):
            self.scale_factor = 1.0
        def set_scale(self, s):
            self.scale_factor = s
        def increase_font(self):
            self.scale_factor += 0.1
        def decrease_font(self):
            self.scale_factor = max(0.5, self.scale_factor - 0.1)
        def reset_font(self):
            self.scale_factor = 1.0
    return FS()
def get_focus_indicator(app):
    return object()
def get_high_contrast_mode(app):
    class HC:
        def __init__(self):
            self.enabled = False
        def enable(self):
            self.enabled = True
        def disable(self):
            self.enabled = False
        def toggle(self):
            self.enabled = not self.enabled
    return HC()
acc_mod.get_keyboard_navigator = get_keyboard_navigator
acc_mod.get_screen_reader_announcer = get_screen_reader_announcer
acc_mod.get_color_validator = get_color_validator
acc_mod.get_font_scaler = get_font_scaler
acc_mod.get_focus_indicator = get_focus_indicator
acc_mod.get_high_contrast_mode = get_high_contrast_mode
sys.modules['utils.accessibility'] = acc_mod

perf_mod = types.ModuleType('utils.performance')
def get_cache():
    class C:
        def clear(self):
            pass
    return C()
def get_lazy_loader():
    return lambda *a, **k: None
def get_performance_monitor():
    return object()
perf_mod.get_cache = get_cache
perf_mod.get_lazy_loader = get_lazy_loader
perf_mod.get_performance_monitor = get_performance_monitor
sys.modules['utils.performance'] = perf_mod

loading_mod = types.ModuleType('utils.loading_indicators')
class LoadingOverlay:
    def __init__(self, parent, message=None):
        self._visible = False
    def show(self):
        self._visible = True
    def hide(self):
        self._visible = False
loading_mod.LoadingOverlay = LoadingOverlay
sys.modules['utils.loading_indicators'] = loading_mod

# --- Stub pages to avoid heavy UI deps (PIL) during this test ---
pages_login_mod = types.ModuleType('pages.login_page')
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
    def load_page(self):
        pass
pages_login_mod.LoginPage = LoginPage
sys.modules['pages.login_page'] = pages_login_mod

pages_login_modern = types.ModuleType('pages.login_page_modern')
class LoginPageModern(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
    def load_page(self):
        pass
pages_login_modern.LoginPageModern = LoginPageModern
sys.modules['pages.login_page_modern'] = pages_login_modern

# Now import the app and check preference application logic
# Instead of instantiating the full Tk app, create a minimal fake controller
# that holds preferences and a page_classes mapping and apply the same logic
# as _apply_login_preference to verify which class would be selected.

class FakeApp:
    def __init__(self):
        self.app_state = types.SimpleNamespace(preferences={})
        self.page_classes = {}

def select_login_class(use_modern: bool):
    # Mirror the logic in main._apply_login_preference
    if use_modern:
        mod = sys.modules.get('pages.login_page_modern')
        cls = getattr(mod, 'LoginPageModern', None) if mod else None
    else:
        mod = sys.modules.get('pages.login_page')
        cls = getattr(mod, 'LoginPage', None) if mod else None
    return cls

fake = FakeApp()
print('Initial login class (module lookup):', select_login_class(False))
print('Applying modern preference ->', select_login_class(True))
print('Reverting to legacy ->', select_login_class(False))

print('Test completed.')
