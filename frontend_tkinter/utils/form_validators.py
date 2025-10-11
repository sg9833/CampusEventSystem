"""
Form validation utilities for the Campus Event System.

This module provides reusable validation functions for common form fields
and patterns. All functions return (is_valid: bool, error_message: str).

Usage:
    from utils.form_validators import validate_required, validate_email
    
    is_valid, error = validate_required(field_value, "Email")
    if not is_valid:
        show_error(error)
"""

import re
from typing import Tuple, Optional, Any
from datetime import datetime


# ============================================================================
#  BASIC VALIDATORS
# ============================================================================

def validate_required(value: Any, field_name: str = "Field") -> Tuple[bool, str]:
    """
    Validate that a field is not empty.
    
    Args:
        value: The value to validate (string, StringVar, or any type)
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Examples:
        >>> validate_required("test", "Email")
        (True, "")
        
        >>> validate_required("", "Email")
        (False, "Email is required")
        
        >>> validate_required("   ", "Name")
        (False, "Name is required")
    """
    # Handle StringVar
    if hasattr(value, 'get'):
        value = value.get()
    
    # Convert to string and strip whitespace
    str_value = str(value).strip() if value is not None else ""
    
    if not str_value:
        return False, f"{field_name} is required"
    
    return True, ""


def validate_length(value: Any, min_length: Optional[int] = None, 
                   max_length: Optional[int] = None, 
                   field_name: str = "Field") -> Tuple[bool, str]:
    """
    Validate string length constraints.
    
    Args:
        value: The value to validate
        min_length: Minimum allowed length (optional)
        max_length: Maximum allowed length (optional)
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Examples:
        >>> validate_length("test", min_length=5, field_name="Title")
        (False, "Title must be at least 5 characters")
        
        >>> validate_length("test", max_length=3, field_name="Code")
        (False, "Code must be at most 3 characters")
    """
    # Handle StringVar
    if hasattr(value, 'get'):
        value = value.get()
    
    str_value = str(value).strip() if value is not None else ""
    length = len(str_value)
    
    if min_length is not None and length < min_length:
        return False, f"{field_name} must be at least {min_length} characters"
    
    if max_length is not None and length > max_length:
        return False, f"{field_name} must be at most {max_length} characters"
    
    return True, ""


def validate_email(email: Any) -> Tuple[bool, str]:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Examples:
        >>> validate_email("user@example.com")
        (True, "")
        
        >>> validate_email("invalid")
        (False, "Invalid email format")
    """
    # Handle StringVar
    if hasattr(email, 'get'):
        email = email.get()
    
    email_str = str(email).strip() if email is not None else ""
    
    if not email_str:
        return False, "Email is required"
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email_str):
        return False, "Invalid email format"
    
    return True, ""


def validate_integer(value: Any, field_name: str = "Field", 
                     min_value: Optional[int] = None,
                     max_value: Optional[int] = None) -> Tuple[bool, str]:
    """
    Validate integer value and range.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        min_value: Minimum allowed value (optional)
        max_value: Maximum allowed value (optional)
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Examples:
        >>> validate_integer("50", "Capacity", min_value=1)
        (True, "")
        
        >>> validate_integer("abc", "Capacity")
        (False, "Capacity must be a valid number")
        
        >>> validate_integer("-5", "Capacity", min_value=0)
        (False, "Capacity must be at least 0")
    """
    # Handle StringVar
    if hasattr(value, 'get'):
        value = value.get()
    
    str_value = str(value).strip() if value is not None else ""
    
    if not str_value:
        return False, f"{field_name} is required"
    
    try:
        int_value = int(str_value)
    except ValueError:
        return False, f"{field_name} must be a valid number"
    
    if min_value is not None and int_value < min_value:
        return False, f"{field_name} must be at least {min_value}"
    
    if max_value is not None and int_value > max_value:
        return False, f"{field_name} must be at most {max_value}"
    
    return True, ""


def validate_date(date_value: Any, field_name: str = "Date",
                 date_format: str = "%Y-%m-%d") -> Tuple[bool, str]:
    """
    Validate date format.
    
    Args:
        date_value: Date string to validate
        field_name: Name of the field for error messages
        date_format: Expected date format (default: YYYY-MM-DD)
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Examples:
        >>> validate_date("2025-01-15")
        (True, "")
        
        >>> validate_date("invalid")
        (False, "Date must be in format YYYY-MM-DD")
    """
    # Handle StringVar
    if hasattr(date_value, 'get'):
        date_value = date_value.get()
    
    str_value = str(date_value).strip() if date_value is not None else ""
    
    if not str_value:
        return False, f"{field_name} is required"
    
    try:
        datetime.strptime(str_value, date_format)
        return True, ""
    except ValueError:
        format_display = date_format.replace('%Y', 'YYYY').replace('%m', 'MM').replace('%d', 'DD')
        return False, f"{field_name} must be in format {format_display}"


def validate_time(time_value: Any, field_name: str = "Time",
                 time_format: str = "%H:%M") -> Tuple[bool, str]:
    """
    Validate time format.
    
    Args:
        time_value: Time string to validate
        field_name: Name of the field for error messages
        time_format: Expected time format (default: HH:MM)
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Examples:
        >>> validate_time("14:30")
        (True, "")
        
        >>> validate_time("25:00")
        (False, "Time must be in format HH:MM")
    """
    # Handle StringVar
    if hasattr(time_value, 'get'):
        time_value = time_value.get()
    
    str_value = str(time_value).strip() if time_value is not None else ""
    
    if not str_value:
        return False, f"{field_name} is required"
    
    try:
        datetime.strptime(str_value, time_format)
        return True, ""
    except ValueError:
        format_display = time_format.replace('%H', 'HH').replace('%M', 'MM')
        return False, f"{field_name} must be in format {format_display}"


# ============================================================================
#  COMPOSITE VALIDATORS
# ============================================================================

def validate_time_range(start_time: Any, end_time: Any) -> Tuple[bool, str]:
    """
    Validate that end time is after start time.
    
    Args:
        start_time: Start time string
        end_time: End time string
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Examples:
        >>> validate_time_range("09:00", "17:00")
        (True, "")
        
        >>> validate_time_range("17:00", "09:00")
        (False, "End time must be after start time")
    """
    # Handle StringVar
    if hasattr(start_time, 'get'):
        start_time = start_time.get()
    if hasattr(end_time, 'get'):
        end_time = end_time.get()
    
    start_str = str(start_time).strip() if start_time is not None else ""
    end_str = str(end_time).strip() if end_time is not None else ""
    
    if not start_str or not end_str:
        return False, "Both start and end time are required"
    
    try:
        start_dt = datetime.strptime(start_str, "%H:%M")
        end_dt = datetime.strptime(end_str, "%H:%M")
        
        if end_dt <= start_dt:
            return False, "End time must be after start time"
        
        return True, ""
    except ValueError:
        return False, "Invalid time format"


def validate_date_range(start_date: Any, end_date: Any) -> Tuple[bool, str]:
    """
    Validate that end date is after start date.
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Handle StringVar
    if hasattr(start_date, 'get'):
        start_date = start_date.get()
    if hasattr(end_date, 'get'):
        end_date = end_date.get()
    
    start_str = str(start_date).strip() if start_date is not None else ""
    end_str = str(end_date).strip() if end_date is not None else ""
    
    if not start_str or not end_str:
        return False, "Both start and end date are required"
    
    try:
        start_dt = datetime.strptime(start_str, "%Y-%m-%d")
        end_dt = datetime.strptime(end_str, "%Y-%m-%d")
        
        if end_dt < start_dt:
            return False, "End date must be after start date"
        
        return True, ""
    except ValueError:
        return False, "Invalid date format"


def validate_future_date(date_value: Any, field_name: str = "Date") -> Tuple[bool, str]:
    """
    Validate that date is in the future.
    
    Args:
        date_value: Date string to validate (YYYY-MM-DD)
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Handle StringVar
    if hasattr(date_value, 'get'):
        date_value = date_value.get()
    
    str_value = str(date_value).strip() if date_value is not None else ""
    
    if not str_value:
        return False, f"{field_name} is required"
    
    try:
        date_dt = datetime.strptime(str_value, "%Y-%m-%d").date()
        today = datetime.now().date()
        
        if date_dt < today:
            return False, f"{field_name} must be in the future"
        
        return True, ""
    except ValueError:
        return False, f"{field_name} must be in format YYYY-MM-DD"


# ============================================================================
#  BATCH VALIDATION
# ============================================================================

def validate_all(validations: list) -> Tuple[bool, list]:
    """
    Run multiple validations and return all errors.
    
    Args:
        validations: List of tuples (validator_func, args_tuple, kwargs_dict)
    
    Returns:
        Tuple of (all_valid, list_of_errors)
    
    Example:
        >>> validations = [
        ...     (validate_required, (title_var, "Title"), {}),
        ...     (validate_email, (email_var,), {}),
        ...     (validate_integer, (capacity_var, "Capacity"), {"min_value": 1})
        ... ]
        >>> is_valid, errors = validate_all(validations)
    """
    errors = []
    
    for validator, args, kwargs in validations:
        is_valid, error_msg = validator(*args, **kwargs)
        if not is_valid:
            errors.append(error_msg)
    
    return len(errors) == 0, errors


# ============================================================================
#  EXPORTS
# ============================================================================

__all__ = [
    'validate_required',
    'validate_length',
    'validate_email',
    'validate_integer',
    'validate_date',
    'validate_time',
    'validate_time_range',
    'validate_date_range',
    'validate_future_date',
    'validate_all',
]
