"""
Unit tests for form validation utilities.

Tests all validation functions in utils/form_validators.py.
"""

import pytest
import tkinter as tk
from datetime import datetime, timedelta

from utils.form_validators import (
    validate_required,
    validate_length,
    validate_email,
    validate_integer,
    validate_date,
    validate_time,
    validate_time_range,
    validate_date_range,
    validate_future_date,
    validate_all,
)


# ============================================================================
#  TEST validate_required
# ============================================================================

class TestValidateRequired:
    """Test validate_required function"""
    
    def test_valid_string(self):
        """Test with valid non-empty string"""
        is_valid, error = validate_required("test", "Email")
        assert is_valid is True
        assert error == ""
    
    def test_empty_string(self):
        """Test with empty string"""
        is_valid, error = validate_required("", "Email")
        assert is_valid is False
        assert "Email is required" in error
    
    def test_whitespace_only(self):
        """Test with whitespace-only string"""
        is_valid, error = validate_required("   ", "Name")
        assert is_valid is False
        assert "Name is required" in error
    
    def test_none_value(self):
        """Test with None value"""
        is_valid, error = validate_required(None, "Field")
        assert is_valid is False
        assert "Field is required" in error
    
    def test_with_stringvar(self, root):
        """Test with tkinter StringVar"""
        var = tk.StringVar(value="test")
        is_valid, error = validate_required(var, "Title")
        assert is_valid is True
        assert error == ""
    
    def test_with_empty_stringvar(self, root):
        """Test with empty tkinter StringVar"""
        var = tk.StringVar(value="")
        is_valid, error = validate_required(var, "Title")
        assert is_valid is False
        assert "Title is required" in error


# ============================================================================
#  TEST validate_length
# ============================================================================

class TestValidateLength:
    """Test validate_length function"""
    
    def test_valid_length(self):
        """Test with valid length"""
        is_valid, error = validate_length("test", min_length=3, max_length=10, field_name="Title")
        assert is_valid is True
        assert error == ""
    
    def test_too_short(self):
        """Test with string too short"""
        is_valid, error = validate_length("ab", min_length=3, field_name="Title")
        assert is_valid is False
        assert "at least 3 characters" in error
    
    def test_too_long(self):
        """Test with string too long"""
        is_valid, error = validate_length("toolongstring", max_length=5, field_name="Code")
        assert is_valid is False
        assert "at most 5 characters" in error
    
    def test_min_length_only(self):
        """Test with only minimum length"""
        is_valid, error = validate_length("test", min_length=2, field_name="Name")
        assert is_valid is True
        assert error == ""
    
    def test_max_length_only(self):
        """Test with only maximum length"""
        is_valid, error = validate_length("test", max_length=10, field_name="Name")
        assert is_valid is True
        assert error == ""
    
    def test_exact_min_length(self):
        """Test with exact minimum length"""
        is_valid, error = validate_length("abc", min_length=3, field_name="Code")
        assert is_valid is True
        assert error == ""


# ============================================================================
#  TEST validate_email
# ============================================================================

class TestValidateEmail:
    """Test validate_email function"""
    
    def test_valid_email(self):
        """Test with valid email"""
        is_valid, error = validate_email("user@example.com")
        assert is_valid is True
        assert error == ""
    
    def test_valid_email_with_dots(self):
        """Test with valid email containing dots"""
        is_valid, error = validate_email("john.doe@example.co.uk")
        assert is_valid is True
        assert error == ""
    
    def test_invalid_no_at(self):
        """Test with email missing @ symbol"""
        is_valid, error = validate_email("userexample.com")
        assert is_valid is False
        assert "Invalid email format" in error
    
    def test_invalid_no_domain(self):
        """Test with email missing domain"""
        is_valid, error = validate_email("user@")
        assert is_valid is False
        assert "Invalid email format" in error
    
    def test_invalid_no_tld(self):
        """Test with email missing TLD"""
        is_valid, error = validate_email("user@example")
        assert is_valid is False
        assert "Invalid email format" in error
    
    def test_empty_email(self):
        """Test with empty email"""
        is_valid, error = validate_email("")
        assert is_valid is False
        assert "Email is required" in error
    
    def test_with_stringvar(self, root):
        """Test with tkinter StringVar"""
        var = tk.StringVar(value="test@example.com")
        is_valid, error = validate_email(var)
        assert is_valid is True
        assert error == ""


# ============================================================================
#  TEST validate_integer
# ============================================================================

class TestValidateInteger:
    """Test validate_integer function"""
    
    def test_valid_integer(self):
        """Test with valid integer"""
        is_valid, error = validate_integer("50", "Capacity")
        assert is_valid is True
        assert error == ""
    
    def test_invalid_non_numeric(self):
        """Test with non-numeric string"""
        is_valid, error = validate_integer("abc", "Capacity")
        assert is_valid is False
        assert "must be a valid number" in error
    
    def test_below_min(self):
        """Test with value below minimum"""
        is_valid, error = validate_integer("-5", "Capacity", min_value=0)
        assert is_valid is False
        assert "at least 0" in error
    
    def test_above_max(self):
        """Test with value above maximum"""
        is_valid, error = validate_integer("100", "Capacity", max_value=50)
        assert is_valid is False
        assert "at most 50" in error
    
    def test_within_range(self):
        """Test with value within range"""
        is_valid, error = validate_integer("25", "Capacity", min_value=1, max_value=100)
        assert is_valid is True
        assert error == ""
    
    def test_empty_string(self):
        """Test with empty string"""
        is_valid, error = validate_integer("", "Capacity")
        assert is_valid is False
        assert "is required" in error
    
    def test_float_string(self):
        """Test with float string"""
        is_valid, error = validate_integer("25.5", "Capacity")
        assert is_valid is False
        assert "must be a valid number" in error


# ============================================================================
#  TEST validate_date
# ============================================================================

class TestValidateDate:
    """Test validate_date function"""
    
    def test_valid_date(self):
        """Test with valid date"""
        is_valid, error = validate_date("2025-01-15", "Event Date")
        assert is_valid is True
        assert error == ""
    
    def test_invalid_format(self):
        """Test with invalid date format"""
        is_valid, error = validate_date("01/15/2025", "Event Date")
        assert is_valid is False
        assert "must be in format" in error
    
    def test_invalid_date(self):
        """Test with invalid date (e.g., Feb 30)"""
        is_valid, error = validate_date("2025-02-30", "Event Date")
        assert is_valid is False
        assert "must be in format" in error
    
    def test_empty_date(self):
        """Test with empty date"""
        is_valid, error = validate_date("", "Event Date")
        assert is_valid is False
        assert "is required" in error
    
    def test_custom_format(self):
        """Test with custom date format"""
        is_valid, error = validate_date("15/01/2025", "Event Date", date_format="%d/%m/%Y")
        assert is_valid is True
        assert error == ""


# ============================================================================
#  TEST validate_time
# ============================================================================

class TestValidateTime:
    """Test validate_time function"""
    
    def test_valid_time(self):
        """Test with valid time"""
        is_valid, error = validate_time("14:30", "Start Time")
        assert is_valid is True
        assert error == ""
    
    def test_invalid_format(self):
        """Test with invalid time format"""
        is_valid, error = validate_time("2:30 PM", "Start Time")
        assert is_valid is False
        assert "must be in format" in error
    
    def test_invalid_hour(self):
        """Test with invalid hour"""
        is_valid, error = validate_time("25:00", "Start Time")
        assert is_valid is False
        assert "must be in format" in error
    
    def test_invalid_minute(self):
        """Test with invalid minute"""
        is_valid, error = validate_time("14:70", "Start Time")
        assert is_valid is False
        assert "must be in format" in error
    
    def test_empty_time(self):
        """Test with empty time"""
        is_valid, error = validate_time("", "Start Time")
        assert is_valid is False
        assert "is required" in error


# ============================================================================
#  TEST validate_time_range
# ============================================================================

class TestValidateTimeRange:
    """Test validate_time_range function"""
    
    def test_valid_range(self):
        """Test with valid time range"""
        is_valid, error = validate_time_range("09:00", "17:00")
        assert is_valid is True
        assert error == ""
    
    def test_end_before_start(self):
        """Test with end time before start time"""
        is_valid, error = validate_time_range("17:00", "09:00")
        assert is_valid is False
        assert "End time must be after start time" in error
    
    def test_equal_times(self):
        """Test with equal times"""
        is_valid, error = validate_time_range("14:00", "14:00")
        assert is_valid is False
        assert "End time must be after start time" in error
    
    def test_missing_start_time(self):
        """Test with missing start time"""
        is_valid, error = validate_time_range("", "17:00")
        assert is_valid is False
        assert "required" in error
    
    def test_missing_end_time(self):
        """Test with missing end time"""
        is_valid, error = validate_time_range("09:00", "")
        assert is_valid is False
        assert "required" in error
    
    def test_with_stringvar(self, root):
        """Test with tkinter StringVar"""
        start_var = tk.StringVar(value="09:00")
        end_var = tk.StringVar(value="17:00")
        is_valid, error = validate_time_range(start_var, end_var)
        assert is_valid is True
        assert error == ""


# ============================================================================
#  TEST validate_date_range
# ============================================================================

class TestValidateDateRange:
    """Test validate_date_range function"""
    
    def test_valid_range(self):
        """Test with valid date range"""
        is_valid, error = validate_date_range("2025-01-15", "2025-01-20")
        assert is_valid is True
        assert error == ""
    
    def test_end_before_start(self):
        """Test with end date before start date"""
        is_valid, error = validate_date_range("2025-01-20", "2025-01-15")
        assert is_valid is False
        assert "End date must be after start date" in error
    
    def test_equal_dates(self):
        """Test with equal dates (should be valid for same-day events)"""
        is_valid, error = validate_date_range("2025-01-15", "2025-01-15")
        assert is_valid is True
        assert error == ""
    
    def test_missing_dates(self):
        """Test with missing dates"""
        is_valid, error = validate_date_range("", "2025-01-20")
        assert is_valid is False
        assert "required" in error


# ============================================================================
#  TEST validate_future_date
# ============================================================================

class TestValidateFutureDate:
    """Test validate_future_date function"""
    
    def test_future_date(self):
        """Test with future date"""
        future = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        is_valid, error = validate_future_date(future, "Event Date")
        assert is_valid is True
        assert error == ""
    
    def test_past_date(self):
        """Test with past date"""
        past = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        is_valid, error = validate_future_date(past, "Event Date")
        assert is_valid is False
        assert "must be in the future" in error
    
    def test_today(self):
        """Test with today's date (should be valid)"""
        today = datetime.now().strftime("%Y-%m-%d")
        is_valid, error = validate_future_date(today, "Event Date")
        assert is_valid is True
        assert error == ""
    
    def test_invalid_format(self):
        """Test with invalid date format"""
        is_valid, error = validate_future_date("2025/01/15", "Event Date")
        assert is_valid is False
        assert "must be in format" in error


# ============================================================================
#  TEST validate_all
# ============================================================================

class TestValidateAll:
    """Test validate_all function"""
    
    def test_all_valid(self):
        """Test with all validations passing"""
        validations = [
            (validate_required, ("test", "Title"), {}),
            (validate_email, ("user@example.com",), {}),
            (validate_integer, ("50", "Capacity"), {"min_value": 1}),
        ]
        is_valid, errors = validate_all(validations)
        assert is_valid is True
        assert errors == []
    
    def test_some_invalid(self):
        """Test with some validations failing"""
        validations = [
            (validate_required, ("", "Title"), {}),
            (validate_email, ("invalid",), {}),
            (validate_integer, ("50", "Capacity"), {"min_value": 1}),
        ]
        is_valid, errors = validate_all(validations)
        assert is_valid is False
        assert len(errors) == 2
        assert any("Title is required" in e for e in errors)
        assert any("Invalid email format" in e for e in errors)
    
    def test_all_invalid(self):
        """Test with all validations failing"""
        validations = [
            (validate_required, ("", "Title"), {}),
            (validate_email, ("invalid",), {}),
            (validate_integer, ("abc", "Capacity"), {}),
        ]
        is_valid, errors = validate_all(validations)
        assert is_valid is False
        assert len(errors) == 3


# ============================================================================
#  INTEGRATION TESTS
# ============================================================================

class TestValidatorIntegration:
    """Integration tests for validator combinations"""
    
    def test_form_validation_flow(self, root):
        """Test complete form validation flow"""
        # Create form data
        title_var = tk.StringVar(value="Tech Conference")
        email_var = tk.StringVar(value="organizer@example.com")
        capacity_var = tk.StringVar(value="100")
        date_var = tk.StringVar(value="2025-12-15")
        
        # Validate all fields
        validations = [
            (validate_required, (title_var, "Title"), {}),
            (validate_length, (title_var, "Title"), {"min_length": 3, "max_length": 100}),
            (validate_email, (email_var,), {}),
            (validate_integer, (capacity_var, "Capacity"), {"min_value": 1, "max_value": 1000}),
            (validate_date, (date_var, "Event Date"), {}),
        ]
        
        is_valid, errors = validate_all(validations)
        assert is_valid is True
        assert errors == []
    
    def test_form_with_errors(self, root):
        """Test form validation with errors"""
        # Create form data with errors
        title_var = tk.StringVar(value="")
        email_var = tk.StringVar(value="invalid")
        capacity_var = tk.StringVar(value="-5")
        
        # Validate all fields
        validations = [
            (validate_required, (title_var, "Title"), {}),
            (validate_email, (email_var,), {}),
            (validate_integer, (capacity_var, "Capacity"), {"min_value": 1}),
        ]
        
        is_valid, errors = validate_all(validations)
        assert is_valid is False
        assert len(errors) == 3
