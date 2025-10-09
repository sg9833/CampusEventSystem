"""
Logging Configuration Module
Configures application-wide logging with multiple handlers and formatters.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional
import traceback


class LoggerSetup:
    """
    Centralized logging setup for the application.
    
    Features:
    - Multiple log files (app, error, api, audit)
    - Rotating file handlers
    - Console output with colors
    - Configurable log levels
    - Automatic log directory creation
    """
    
    _initialized = False
    _loggers = {}
    
    @classmethod
    def initialize(cls, log_dir: str = 'logs', log_level: str = 'INFO'):
        """
        Initialize logging configuration.
        
        Args:
            log_dir: Directory for log files
            log_level: Default logging level
        """
        if cls._initialized:
            return
        
        # Create logs directory
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"[LOGGING] Created log directory: {log_dir}")
        
        # Convert log level string to logging constant
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        ))
        root_logger.addHandler(console_handler)
        
        # Application log file (all logs)
        app_log_file = os.path.join(log_dir, 'app.log')
        app_handler = RotatingFileHandler(
            app_log_file,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        app_handler.setLevel(logging.DEBUG)
        app_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(app_handler)
        
        # Error log file (errors and critical only)
        error_log_file = os.path.join(log_dir, 'error.log')
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)
        
        cls._initialized = True
        print(f"[LOGGING] Logging initialized - Level: {log_level}")
        print(f"[LOGGING] App log: {app_log_file}")
        print(f"[LOGGING] Error log: {error_log_file}")
    
    @classmethod
    def get_logger(cls, name: str, log_file: Optional[str] = None) -> logging.Logger:
        """
        Get or create a logger with optional dedicated log file.
        
        Args:
            name: Logger name
            log_file: Optional dedicated log file path
            
        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(name)
        
        # Add dedicated file handler if specified
        if log_file:
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10 MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        cls._loggers[name] = logger
        return logger


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        """Format log record with colors."""
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        # Format message
        result = super().format(record)
        
        # Reset levelname for next use
        record.levelname = levelname
        
        return result


class APILogger:
    """
    Specialized logger for API calls.
    
    Logs:
    - Request method, URL, headers, body
    - Response status, headers, body
    - Timing information
    - Errors and exceptions
    """
    
    def __init__(self, log_dir: str = 'logs'):
        """Initialize API logger."""
        log_file = os.path.join(log_dir, 'api.log')
        self.logger = LoggerSetup.get_logger('api', log_file)
    
    def log_request(self, method: str, url: str, headers: dict = None, 
                   body: any = None, **kwargs):
        """Log API request."""
        self.logger.info(f"API Request: {method} {url}")
        if headers:
            self.logger.debug(f"Headers: {headers}")
        if body:
            self.logger.debug(f"Body: {body}")
        if kwargs:
            self.logger.debug(f"Params: {kwargs}")
    
    def log_response(self, method: str, url: str, status_code: int, 
                    response_time: float, response_body: any = None):
        """Log API response."""
        self.logger.info(
            f"API Response: {method} {url} - "
            f"Status: {status_code} - Time: {response_time:.2f}s"
        )
        if response_body:
            self.logger.debug(f"Response Body: {response_body}")
    
    def log_error(self, method: str, url: str, error: Exception):
        """Log API error."""
        self.logger.error(
            f"API Error: {method} {url} - {type(error).__name__}: {str(error)}"
        )
        self.logger.debug(traceback.format_exc())


class AuditLogger:
    """
    Specialized logger for user actions (audit trail).
    
    Logs:
    - User authentication (login/logout)
    - Data modifications (create/update/delete)
    - Permission changes
    - Security events
    """
    
    def __init__(self, log_dir: str = 'logs'):
        """Initialize audit logger."""
        log_file = os.path.join(log_dir, 'audit.log')
        self.logger = LoggerSetup.get_logger('audit', log_file)
    
    def log_login(self, username: str, success: bool, ip: str = None):
        """Log user login attempt."""
        status = "SUCCESS" if success else "FAILED"
        ip_info = f" from {ip}" if ip else ""
        self.logger.info(f"LOGIN {status}: {username}{ip_info}")
    
    def log_logout(self, username: str):
        """Log user logout."""
        self.logger.info(f"LOGOUT: {username}")
    
    def log_action(self, username: str, action: str, resource: str, 
                   resource_id: any = None, details: str = None):
        """
        Log user action.
        
        Args:
            username: Username performing action
            action: Action type (CREATE, UPDATE, DELETE, VIEW)
            resource: Resource type (Event, Booking, User, etc.)
            resource_id: Resource identifier
            details: Additional details
        """
        msg = f"{action} {resource}"
        if resource_id:
            msg += f" (ID: {resource_id})"
        msg += f" by {username}"
        if details:
            msg += f" - {details}"
        
        self.logger.info(msg)
    
    def log_permission_change(self, admin: str, user: str, old_role: str, 
                             new_role: str):
        """Log permission change."""
        self.logger.warning(
            f"PERMISSION CHANGE: {admin} changed {user} role "
            f"from {old_role} to {new_role}"
        )
    
    def log_security_event(self, event_type: str, username: str = None, 
                          details: str = None):
        """Log security-related event."""
        msg = f"SECURITY EVENT: {event_type}"
        if username:
            msg += f" - User: {username}"
        if details:
            msg += f" - {details}"
        
        self.logger.warning(msg)


# Global logger instances
_app_logger = None
_api_logger = None
_audit_logger = None


def get_logger(name: str = 'app') -> logging.Logger:
    """
    Get application logger.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    global _app_logger
    if _app_logger is None:
        _app_logger = LoggerSetup.get_logger(name)
    return _app_logger


def get_api_logger() -> APILogger:
    """Get API logger instance."""
    global _api_logger
    if _api_logger is None:
        _api_logger = APILogger()
    return _api_logger


def get_audit_logger() -> AuditLogger:
    """Get audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def initialize_logging(log_dir: str = 'logs', log_level: str = 'INFO'):
    """
    Initialize application logging.
    
    Args:
        log_dir: Directory for log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    LoggerSetup.initialize(log_dir, log_level)
    
    # Create log directory structure
    os.makedirs(log_dir, exist_ok=True)
    
    # Test logging
    logger = get_logger()
    logger.info("=" * 60)
    logger.info("Campus Event System - Logging Initialized")
    logger.info(f"Log Level: {log_level}")
    logger.info(f"Log Directory: {log_dir}")
    logger.info("=" * 60)
