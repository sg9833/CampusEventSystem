"""
Configuration Management Module
Handles loading and managing application configuration from config.ini
and environment variables.
"""

import os
import configparser
import logging
from typing import Any, Dict, Optional


class Config:
    """
    Configuration manager for the application.
    
    Supports:
    - Loading from config.ini file
    - Environment variable overrides
    - Different environments (dev/staging/prod)
    - Type conversion
    """
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """Singleton pattern - only one config instance."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from config.ini file."""
        self._config = configparser.ConfigParser()
        
        # Get config file path
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config.ini'
        )
        
        if os.path.exists(config_path):
            self._config.read(config_path)
            print(f"[CONFIG] Loaded configuration from: {config_path}")
        else:
            print(f"[CONFIG] Warning: config.ini not found at {config_path}")
            # Create default config
            self._create_default_config()
    
    def _create_default_config(self):
        """Create default configuration if config.ini doesn't exist."""
        self._config['API'] = {
            'base_url': 'http://localhost:8080/api',
            'timeout': '30',
            'retry_attempts': '3',
            'retry_delay': '1'
        }
        self._config['LOGGING'] = {
            'level': 'INFO',
            'log_dir': 'logs'
        }
        self._config['UI'] = {
            'default_theme': 'light',
            'window_width': '1200',
            'window_height': '700'
        }
    
    def get(self, section: str, key: str, fallback: Any = None) -> str:
        """
        Get configuration value with environment variable override.
        
        Priority:
        1. Environment variable (SECTION_KEY format)
        2. config.ini value
        3. fallback value
        
        Args:
            section: Configuration section name
            key: Configuration key name
            fallback: Default value if not found
            
        Returns:
            Configuration value as string
        """
        # Check environment variable first
        env_key = f"{section.upper()}_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return env_value
        
        # Check config file
        try:
            return self._config.get(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """Get configuration value as integer."""
        value = self.get(section, key, str(fallback))
        try:
            return int(value)
        except (ValueError, TypeError):
            return fallback
    
    def get_float(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get configuration value as float."""
        value = self.get(section, key, str(fallback))
        try:
            return float(value)
        except (ValueError, TypeError):
            return fallback
    
    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get configuration value as boolean."""
        value = self.get(section, key, str(fallback))
        if isinstance(value, bool):
            return value
        return value.lower() in ('true', 'yes', '1', 'on', 'enabled')
    
    def get_section(self, section: str) -> Dict[str, str]:
        """Get all key-value pairs from a section."""
        try:
            return dict(self._config.items(section))
        except configparser.NoSectionError:
            return {}
    
    def get_environment(self) -> str:
        """
        Get current environment.
        
        Priority:
        1. ENVIRONMENT env variable
        2. config.ini ENVIRONMENT.environment
        3. 'development' default
        """
        env = os.environ.get('ENVIRONMENT')
        if env:
            return env.lower()
        
        return self.get('ENVIRONMENT', 'environment', 'development').lower()
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.get_environment() == 'development'
    
    def is_staging(self) -> bool:
        """Check if running in staging environment."""
        return self.get_environment() == 'staging'
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.get_environment() == 'production'
    
    def get_api_base_url(self) -> str:
        """
        Get API base URL with environment-specific override.
        
        Priority:
        1. API_BASE_URL env variable
        2. config.ini API.base_url
        3. Default based on environment
        """
        # Check environment variable
        env_url = os.environ.get('API_BASE_URL')
        if env_url:
            return env_url
        
        # Check config file
        config_url = self.get('API', 'base_url')
        if config_url:
            return config_url
        
        # Default based on environment
        env = self.get_environment()
        if env == 'production':
            return 'https://api.campusevents.edu/api'
        elif env == 'staging':
            return 'https://staging-api.campusevents.edu/api'
        else:  # development
            return 'http://localhost:8080/api'
    
    def get_log_level(self) -> str:
        """Get logging level with environment override."""
        # Check environment variable
        env_level = os.environ.get('LOG_LEVEL')
        if env_level:
            return env_level.upper()
        
        # Check config file
        return self.get('LOGGING', 'level', 'INFO').upper()
    
    def reload(self):
        """Reload configuration from file."""
        self._load_config()
        print("[CONFIG] Configuration reloaded")


# Global config instance
config = Config()


# Convenience functions
def get_config() -> Config:
    """Get global configuration instance."""
    return config


def get_api_base_url() -> str:
    """Get API base URL."""
    return config.get_api_base_url()


def get_environment() -> str:
    """Get current environment."""
    return config.get_environment()


def is_development() -> bool:
    """Check if development environment."""
    return config.is_development()


def is_production() -> bool:
    """Check if production environment."""
    return config.is_production()
