"""
Unified Configuration Management System
Supports: config.ini, .env files, environment variables
Priority: ENV_VARS > .env > config.ini > defaults

Author: Campus Event System Team
Date: October 11, 2025
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import configparser
import logging

# Try to import dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False
    print("Warning: python-dotenv not installed. .env files will not be loaded.")


class Settings:
    """
    Unified application settings with validation
    
    Configuration priority (highest to lowest):
    1. Environment variables
    2. .env file
    3. config.ini file
    4. Default values
    
    Usage:
        from config.settings import settings
        
        api_url = settings.API_BASE_URL
        # or
        api_url = settings.get('API_BASE_URL')
    """
    
    _instance = None
    
    def __new__(cls, env: str = None):
        """Singleton pattern - only one Settings instance"""
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, env: str = None):
        """Initialize settings"""
        if self._initialized:
            return
            
        self.env = env or os.getenv('ENVIRONMENT', 'development')
        self._config: Dict[str, Any] = {}
        self._load_all_config()
        self._validate()
        self._initialized = True
    
    def _load_all_config(self):
        """Load configuration from all sources in priority order"""
        # 1. Load defaults first
        self._config.update(self._get_defaults())
        
        # 2. Load from config.ini
        self._config.update(self._load_from_ini())
        
        # 3. Load from .env file
        if HAS_DOTENV:
            self._config.update(self._load_from_env())
        
        # 4. Override with environment variables
        self._config.update(self._load_from_system_env())
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Default configuration values"""
        return {
            # API Configuration
            'API_BASE_URL': 'http://localhost:8080/api',
            'API_TIMEOUT': 30,
            'API_RETRY_ATTEMPTS': 3,
            'API_RETRY_DELAY': 1,
            'API_MAX_CONNECTIONS': 10,
            
            # Cache Configuration
            'CACHE_ENABLED': True,
            'CACHE_TTL': 300,  # 5 minutes
            'CACHE_MAX_SIZE': 100,
            'CACHE_DIR': 'cache',
            
            # Logging Configuration
            'LOG_LEVEL': 'INFO',
            'LOG_DIR': 'logs',
            'LOG_MAX_SIZE': 10485760,  # 10 MB
            'LOG_BACKUP_COUNT': 5,
            'LOG_FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            
            # Session Configuration
            'SESSION_TIMEOUT': 1800,  # 30 minutes
            'SESSION_WARNING_TIME': 300,  # 5 minutes before timeout
            'SESSION_PERSISTENT': False,
            'SESSION_FILE': 'cache/session.json',
            
            # UI Configuration
            'UI_THEME': 'light',
            'UI_WINDOW_WIDTH': 1200,
            'UI_WINDOW_HEIGHT': 700,
            'UI_FONT_FAMILY': 'Segoe UI',
            'UI_FONT_SIZE': 10,
            'UI_SHOW_TOOLTIPS': True,
            'UI_ANIMATION_ENABLED': True,
            
            # Performance Configuration
            'PERFORMANCE_LAZY_LOADING': True,
            'PERFORMANCE_MONITORING': True,
            'PERFORMANCE_PAGE_SIZE': 20,
            'PERFORMANCE_IMAGE_CACHE': True,
            
            # Security Configuration
            'SECURITY_CSRF_ENABLED': True,
            'SECURITY_RATE_LIMIT': 100,
            'SECURITY_RATE_WINDOW': 60,  # seconds
            'SECURITY_PASSWORD_MIN_LENGTH': 6,
            'SECURITY_SESSION_ENCRYPTION': False,
            
            # Notification Configuration
            'NOTIFICATION_POLL_INTERVAL': 30,  # seconds
            'NOTIFICATION_RETENTION_DAYS': 30,
            'NOTIFICATION_SOUND_ENABLED': True,
            
            # Feature Flags
            'FEATURE_OFFLINE_MODE': False,
            'FEATURE_DARK_MODE': True,
            'FEATURE_ANALYTICS': True,
            'FEATURE_NOTIFICATIONS': True,
            
            # Debug Configuration
            'DEBUG': False,
            'DEBUG_PRINT_API_CALLS': False,
            'DEBUG_SHOW_PERFORMANCE': False,
        }
    
    def _load_from_ini(self) -> Dict[str, Any]:
        """Load configuration from config.ini file"""
        result = {}
        config_file = self._find_config_file('config.ini')
        
        if not config_file:
            return result
        
        try:
            parser = configparser.ConfigParser()
            parser.read(config_file)
            
            # Map INI sections to config keys
            section_mapping = {
                'API': 'API_',
                'CACHE': 'CACHE_',
                'LOG': 'LOG_',
                'SESSION': 'SESSION_',
                'UI': 'UI_',
                'PERFORMANCE': 'PERFORMANCE_',
                'SECURITY': 'SECURITY_',
                'NOTIFICATION': 'NOTIFICATION_',
                'FEATURE': 'FEATURE_',
                'DEBUG': 'DEBUG_',
            }
            
            for section, prefix in section_mapping.items():
                if parser.has_section(section):
                    for key, value in parser[section].items():
                        config_key = f"{prefix}{key.upper()}"
                        result[config_key] = self._parse_value(value)
            
            # Also load [DEFAULT] section
            if parser.has_section('DEFAULT'):
                for key, value in parser['DEFAULT'].items():
                    result[key.upper()] = self._parse_value(value)
                    
        except Exception as e:
            print(f"Warning: Could not load config.ini: {e}")
        
        return result
    
    def _load_from_env(self) -> Dict[str, Any]:
        """Load configuration from .env file"""
        result = {}
        env_file = self._find_config_file('.env')
        
        if env_file and HAS_DOTENV:
            try:
                load_dotenv(env_file)
            except Exception as e:
                print(f"Warning: Could not load .env file: {e}")
        
        return result
    
    def _load_from_system_env(self) -> Dict[str, Any]:
        """Load configuration from system environment variables"""
        result = {}
        
        # Prefixes to look for
        prefixes = ['API_', 'CACHE_', 'LOG_', 'SESSION_', 'UI_', 
                   'PERFORMANCE_', 'SECURITY_', 'NOTIFICATION_', 
                   'FEATURE_', 'DEBUG_']
        
        for key, value in os.environ.items():
            # Check if key starts with any of our prefixes
            if any(key.startswith(prefix) for prefix in prefixes):
                result[key] = self._parse_value(value)
            # Also check for common config keys
            elif key in ['ENVIRONMENT', 'DEBUG', 'PORT']:
                result[key] = self._parse_value(value)
        
        return result
    
    def _find_config_file(self, filename: str) -> Optional[Path]:
        """Find configuration file in current or parent directories"""
        current_dir = Path(__file__).parent.parent  # Go up from config/ to frontend_tkinter/
        
        # Search in current directory and parent directories
        search_dirs = [
            current_dir,
            current_dir.parent,
            Path.cwd(),
        ]
        
        for directory in search_dirs:
            config_path = directory / filename
            if config_path.exists():
                return config_path
        
        return None
    
    def _parse_value(self, value: str) -> Any:
        """Parse string value to appropriate type"""
        if not isinstance(value, str):
            return value
            
        # Boolean values
        if value.lower() in ('true', 'yes', '1', 'on'):
            return True
        if value.lower() in ('false', 'no', '0', 'off'):
            return False
        
        # None/null values
        if value.lower() in ('none', 'null', ''):
            return None
        
        # Try integer
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def _validate(self):
        """Validate configuration values"""
        # Required fields
        required = ['API_BASE_URL']
        for key in required:
            if key not in self._config or self._config[key] is None:
                raise ValueError(f"Required configuration '{key}' is missing")
        
        # Validate API URL format
        api_url = self._config['API_BASE_URL']
        if not api_url.startswith(('http://', 'https://')):
            raise ValueError("API_BASE_URL must start with http:// or https://")
        
        # Validate numeric ranges
        if self._config.get('API_TIMEOUT', 0) <= 0:
            raise ValueError("API_TIMEOUT must be positive")
        
        if self._config.get('SESSION_TIMEOUT', 0) <= 0:
            raise ValueError("SESSION_TIMEOUT must be positive")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value (runtime only, not persistent)"""
        self._config[key] = value
    
    def __getattr__(self, key: str) -> Any:
        """Allow attribute-style access: settings.API_BASE_URL"""
        if key.startswith('_'):
            return object.__getattribute__(self, key)
        return self.get(key)
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access: settings['API_BASE_URL']"""
        return self.get(key)
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.env.lower() in ('development', 'dev')
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.env.lower() in ('production', 'prod')
    
    def is_testing(self) -> bool:
        """Check if running in testing environment"""
        return self.env.lower() in ('testing', 'test')
    
    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return self._config.copy()
    
    def print_config(self, show_secrets: bool = False):
        """Print current configuration (for debugging)"""
        print("\n" + "="*60)
        print(f"Configuration (Environment: {self.env})")
        print("="*60)
        
        secret_keys = ['PASSWORD', 'SECRET', 'KEY', 'TOKEN']
        
        for key, value in sorted(self._config.items()):
            # Hide sensitive values
            if not show_secrets and any(s in key.upper() for s in secret_keys):
                display_value = "***HIDDEN***"
            else:
                display_value = value
            
            print(f"{key:40} = {display_value}")
        
        print("="*60 + "\n")
    
    def reload(self):
        """Reload configuration from all sources"""
        self._config = {}
        self._load_all_config()
        self._validate()


# Global settings instance
settings = Settings()


# Convenience functions
def get_settings() -> Settings:
    """Get global settings instance"""
    return settings


def reload_settings():
    """Reload settings from configuration files"""
    global settings
    settings.reload()


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a configuration value"""
    return settings.get(key, default)


# Aliases for backward compatibility
def get_api_base_url() -> str:
    """Get API base URL"""
    return settings.API_BASE_URL


def get_cache_dir() -> str:
    """Get cache directory"""
    return settings.CACHE_DIR


def get_log_dir() -> str:
    """Get logs directory"""
    return settings.LOG_DIR


# Export main objects
__all__ = [
    'Settings',
    'settings',
    'get_settings',
    'reload_settings',
    'get_config_value',
    'get_api_base_url',
    'get_cache_dir',
    'get_log_dir',
]
