"""
Configuration module for Campus Event System
Provides unified configuration management
"""

from .settings import (
    settings,
    get_settings,
    reload_settings,
    get_config_value,
    get_api_base_url,
    get_cache_dir,
    get_log_dir,
    Settings,
)

__all__ = [
    'settings',
    'get_settings',
    'reload_settings',
    'get_config_value',
    'get_api_base_url',
    'get_cache_dir',
    'get_log_dir',
    'Settings',
]
