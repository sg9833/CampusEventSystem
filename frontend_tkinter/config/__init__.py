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
    'API_BASE_URL',
]

# Expose API_BASE_URL for backward compatibility
API_BASE_URL = get_api_base_url()
