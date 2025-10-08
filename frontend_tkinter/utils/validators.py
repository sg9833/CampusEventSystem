import re
from datetime import datetime, date
from typing import Tuple, Optional


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate email format. Returns (is_valid, error_message)."""
    if not email or not email.strip():
        return False, "Email is required"
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if re.match(pattern, email):
        return True, None
    return False, "Invalid email format"


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """Validate a 10-digit phone number. Accepts digits, spaces, dashes, parentheses.
    Returns (is_valid, error_message)."""
    if not phone or not phone.strip():
        return False, "Phone number is required"
    # Remove common separators
    cleaned = re.sub(r'[\s\-()+.]', '', phone)
    if not cleaned.isdigit():
        return False, "Phone must contain only digits"
    if len(cleaned) != 10:
        return False, "Phone must be 10 digits"
    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """Validate password: minimum 8 chars, at least 1 uppercase, at least 1 number.
    Returns (is_valid, error_message)."""
    if not password:
        return False, "Password is required"
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, None


def validate_date(date_str: str) -> Tuple[bool, Optional[str]]:
    """Validate date format (YYYY-MM-DD) and ensure it's in the future.
    Returns (is_valid, error_message)."""
    if not date_str or not date_str.strip():
        return False, "Date is required"
    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format"
    today = date.today()
    if parsed <= today:
        return False, "Date must be in the future"
    return True, None


def validate_time(time_str: str) -> Tuple[bool, Optional[str]]:
    """Validate time format HH:MM (24-hour). Returns (is_valid, error_message)."""
    if not time_str or not time_str.strip():
        return False, "Time is required"
    pattern = r'^(?:[01]\d|2[0-3]):[0-5]\d$'
    if re.match(pattern, time_str):
        return True, None
    return False, "Time must be in HH:MM 24-hour format"


def sanitize_input(text: str) -> str:
    """Sanitize input string by removing characters commonly used in SQL injection.
    This is a best-effort client-side sanitizer — always use parameterized queries on the server.
    Returns the sanitized string."""
    if text is None:
        return ""
    # Remove common SQL meta-characters (quotes, semicolons, comment markers)
    cleaned = text
    # Remove SQL single/double quotes
    cleaned = cleaned.replace("'", " ").replace('"', ' ')
    # Remove semicolons
    cleaned = cleaned.replace(";", " ")
    # Remove SQL comment markers
    cleaned = re.sub(r"--+", " ", cleaned)
    # Remove parentheses which are not normally needed for simple input
    cleaned = cleaned.replace('(', ' ').replace(')', ' ')
    # Remove any remaining characters except a conservative safe set
    sanitized = re.sub(r"[^A-Za-z0-9 @._\-:(),/\\]", "", cleaned)
    # Collapse multiple spaces
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized


def validate_required_field(value: str) -> Tuple[bool, Optional[str]]:
    """Validate that a field is not empty. Returns (is_valid, error_message)."""
    if value and value.strip():
        return True, None
    return False, "This field is required"


def validate_positive_integer(value) -> Tuple[bool, Optional[str]]:
    """Validate that value is a positive integer. Returns (is_valid, error_message)."""
    try:
        num = int(value)
        if num > 0:
            return True, None
        return False, "Value must be a positive integer"
    except (ValueError, TypeError):
        return False, "Value must be a positive integer"