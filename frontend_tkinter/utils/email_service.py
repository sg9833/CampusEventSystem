"""
Email Notification Service for Campus Event System

This module provides email notification functionality including:
- Event registration confirmations
- Event reminders (1 day before)
- Booking confirmations (approved/rejected)
- Event approval/rejection notifications
- Weekly digest of upcoming events

Usage:
    from utils.email_service import EmailService
    
    email_service = EmailService()
    email_service.send_event_reminder(user_email, event_details)
"""

from utils.api_client import APIClient
from utils.session_manager import SessionManager
from datetime import datetime, timedelta
import threading
from typing import Dict, Any, List, Optional, Callable


class EmailService:
    """
    Email notification service for the Campus Event System.
    
    Sends email notifications via backend API endpoint: POST /api/notifications/email
    """
    
    def __init__(self):
        self.api = APIClient()
        self.session = SessionManager()
    
    def _send_email(
        self,
        to: str,
        subject: str,
        email_type: str,
        data: Dict[str, Any],
        on_success: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
        async_send: bool = True
    ):
        """
        Internal method to send email via backend API.
        
        Args:
            to: Recipient email address
            subject: Email subject
            email_type: Type of email (event_registration, event_reminder, etc.)
            data: Email data (event details, booking details, etc.)
            on_success: Optional callback for successful send
            on_error: Optional callback for error
            async_send: Whether to send asynchronously (default: True)
        """
        payload = {
            "to": to,
            "subject": subject,
            "type": email_type,
            "data": data
        }
        
        def send_request():
            try:
                response = self.api.post("notifications/email", payload)
                print(f"[EMAIL] Sent {email_type} to {to}")
                if on_success:
                    on_success(response)
                return response
            except Exception as e:
                print(f"[EMAIL ERROR] Failed to send {email_type} to {to}: {str(e)}")
                if on_error:
                    on_error(e)
                return None
        
        if async_send:
            # Send asynchronously in background thread
            thread = threading.Thread(target=send_request, daemon=True)
            thread.start()
        else:
            # Send synchronously
            return send_request()
    
    def send_event_registration_confirmation(
        self,
        user_email: str,
        event_details: Dict[str, Any],
        user_name: Optional[str] = None,
        on_success: Optional[Callable] = None,
        on_error: Optional[Callable] = None
    ):
        """
        Send event registration confirmation email.
        
        Args:
            user_email: Recipient email address
            event_details: Event details dictionary with keys:
                - title: Event title
                - date: Event date (YYYY-MM-DD or datetime string)
                - time: Event time (HH:MM or time string)
                - location: Event location
            user_name: User's name (optional, will use session if not provided)
            on_success: Optional callback for successful send
            on_error: Optional callback for error
        
        Example:
            email_service.send_event_registration_confirmation(
                user_email="student@example.com",
                event_details={
                    "title": "Python Workshop",
                    "date": "2025-10-15",
                    "time": "14:00",
                    "location": "Room 301"
                }
            )
        """
        if not user_name:
            user = self.session.get_user()
            user_name = user.get('name', 'Student') if user else 'Student'
        
        data = {
            "user_name": user_name,
            "event_title": event_details.get('title', event_details.get('name', 'Event')),
            "event_date": self._format_date(event_details.get('date', event_details.get('start_date', 'TBD'))),
            "event_time": self._format_time(event_details.get('time', event_details.get('start_time', 'TBD'))),
            "event_location": event_details.get('location', event_details.get('venue', 'TBD'))
        }
        
        subject = f"Registration Confirmed: {data['event_title']}"
        
        self._send_email(
            to=user_email,
            subject=subject,
            email_type="event_registration",
            data=data,
            on_success=on_success,
            on_error=on_error
        )
    
    def send_event_reminder(
        self,
        user_email: str,
        event_details: Dict[str, Any],
        user_name: Optional[str] = None,
        days_before: int = 1,
        on_success: Optional[Callable] = None,
        on_error: Optional[Callable] = None
    ):
        """
        Send event reminder email (typically 1 day before event).
        
        Args:
            user_email: Recipient email address
            event_details: Event details dictionary
            user_name: User's name (optional)
            days_before: Number of days before event (default: 1)
            on_success: Optional callback for successful send
            on_error: Optional callback for error
        
        Example:
            email_service.send_event_reminder(
                user_email="student@example.com",
                event_details={
                    "title": "Python Workshop",
                    "date": "2025-10-15",
                    "time": "14:00",
                    "location": "Room 301"
                },
                days_before=1
            )
        """
        if not user_name:
            user = self.session.get_user()
            user_name = user.get('name', 'Student') if user else 'Student'
        
        event_date = self._format_date(event_details.get('date', event_details.get('start_date', 'Tomorrow')))
        
        data = {
            "user_name": user_name,
            "event_title": event_details.get('title', event_details.get('name', 'Event')),
            "event_date": event_date,
            "event_time": self._format_time(event_details.get('time', event_details.get('start_time', 'TBD'))),
            "event_location": event_details.get('location', event_details.get('venue', 'TBD'))
        }
        
        subject = f"Reminder: {data['event_title']} - {event_date}"
        
        self._send_email(
            to=user_email,
            subject=subject,
            email_type="event_reminder",
            data=data,
            on_success=on_success,
            on_error=on_error
        )
    
    def send_booking_confirmation(
        self,
        user_email: str,
        booking_details: Dict[str, Any],
        status: str = "confirmed",
        user_name: Optional[str] = None,
        on_success: Optional[Callable] = None,
        on_error: Optional[Callable] = None
    ):
        """
        Send booking confirmation email.
        
        Args:
            user_email: Recipient email address
            booking_details: Booking details dictionary with keys:
                - resource_name: Name of the resource
                - date: Booking date
                - time: Booking time
                - start_time: Start time (if no 'time' key)
                - end_time: End time
            status: Booking status (confirmed, pending, cancelled)
            user_name: User's name (optional)
            on_success: Optional callback for successful send
            on_error: Optional callback for error
        
        Example:
            email_service.send_booking_confirmation(
                user_email="student@example.com",
                booking_details={
                    "resource_name": "Conference Room A",
                    "date": "2025-10-15",
                    "start_time": "14:00",
                    "end_time": "16:00"
                },
                status="confirmed"
            )
        """
        if not user_name:
            user = self.session.get_user()
            user_name = user.get('name', 'Student') if user else 'Student'
        
        # Format booking time
        booking_time = booking_details.get('time', '')
        if not booking_time:
            start = booking_details.get('start_time', '')
            end = booking_details.get('end_time', '')
            if start and end:
                booking_time = f"{self._format_time(start)} - {self._format_time(end)}"
            elif start:
                booking_time = self._format_time(start)
            else:
                booking_time = 'TBD'
        
        data = {
            "user_name": user_name,
            "resource_name": booking_details.get('resource_name', booking_details.get('name', 'Resource')),
            "booking_date": self._format_date(booking_details.get('date', booking_details.get('booking_date', 'TBD'))),
            "booking_time": booking_time,
            "status": status
        }
        
        subject = f"Booking {status.title()}: {data['resource_name']}"
        
        self._send_email(
            to=user_email,
            subject=subject,
            email_type="booking_confirmation",
            data=data,
            on_success=on_success,
            on_error=on_error
        )
    
    def send_approval_notification(
        self,
        user_email: str,
        item_type: str,
        item_name: str,
        status: str,
        reason: str = "",
        user_name: Optional[str] = None,
        on_success: Optional[Callable] = None,
        on_error: Optional[Callable] = None
    ):
        """
        Send approval/rejection notification email.
        
        Args:
            user_email: Recipient email address
            item_type: Type of item (event, booking, resource)
            item_name: Name of the item
            status: Status (approved, rejected, pending)
            reason: Reason for approval/rejection (optional)
            user_name: User's name (optional)
            on_success: Optional callback for successful send
            on_error: Optional callback for error
        
        Example:
            email_service.send_approval_notification(
                user_email="organizer@example.com",
                item_type="event",
                item_name="Python Workshop",
                status="approved",
                reason="Meets all requirements"
            )
        """
        if not user_name:
            user = self.session.get_user()
            user_name = user.get('name', 'Student') if user else 'Student'
        
        data = {
            "user_name": user_name,
            "item_type": item_type,
            "item_name": item_name,
            "status": status,
            "reason": reason
        }
        
        subject = f"{item_type.title()} {status.title()}: {item_name}"
        
        self._send_email(
            to=user_email,
            subject=subject,
            email_type="approval_notification",
            data=data,
            on_success=on_success,
            on_error=on_error
        )
    
    def send_weekly_digest(
        self,
        user_email: str,
        events: List[Dict[str, Any]],
        user_name: Optional[str] = None,
        on_success: Optional[Callable] = None,
        on_error: Optional[Callable] = None
    ):
        """
        Send weekly digest of upcoming events.
        
        Args:
            user_email: Recipient email address
            events: List of event dictionaries
            user_name: User's name (optional)
            on_success: Optional callback for successful send
            on_error: Optional callback for error
        
        Example:
            events = [
                {"title": "Python Workshop", "date": "2025-10-15", "location": "Room 301"},
                {"title": "Career Fair", "date": "2025-10-17", "location": "Main Hall"}
            ]
            email_service.send_weekly_digest(
                user_email="student@example.com",
                events=events
            )
        """
        if not user_name:
            user = self.session.get_user()
            user_name = user.get('name', 'Student') if user else 'Student'
        
        # Format events as strings
        event_strings = []
        for event in events:
            title = event.get('title', event.get('name', 'Event'))
            date = self._format_date(event.get('date', event.get('start_date', 'TBD')))
            location = event.get('location', event.get('venue', 'TBD'))
            event_strings.append(f"{title} - {date} at {location}")
        
        data = {
            "user_name": user_name,
            "events": event_strings
        }
        
        subject = "Weekly Event Digest - Campus Event System"
        
        self._send_email(
            to=user_email,
            subject=subject,
            email_type="weekly_digest",
            data=data,
            on_success=on_success,
            on_error=on_error
        )
    
    def send_bulk_notifications(
        self,
        recipients: List[str],
        subject: str,
        email_type: str,
        data: Dict[str, Any],
        on_success: Optional[Callable] = None,
        on_error: Optional[Callable] = None
    ):
        """
        Send bulk email notifications to multiple recipients.
        
        Args:
            recipients: List of email addresses
            subject: Email subject
            email_type: Type of email
            data: Email data
            on_success: Optional callback for successful send
            on_error: Optional callback for error
        
        Example:
            email_service.send_bulk_notifications(
                recipients=["user1@example.com", "user2@example.com"],
                subject="Event Cancelled",
                email_type="event_reminder",
                data={"event_title": "Python Workshop", ...}
            )
        """
        payload = {
            "recipients": recipients,
            "subject": subject,
            "type": email_type,
            "data": data
        }
        
        def send_request():
            try:
                response = self.api.post("notifications/email/bulk", payload)
                print(f"[EMAIL] Bulk sent {email_type} to {len(recipients)} recipients")
                if on_success:
                    on_success(response)
                return response
            except Exception as e:
                print(f"[EMAIL ERROR] Failed to send bulk emails: {str(e)}")
                if on_error:
                    on_error(e)
                return None
        
        # Send in background thread
        thread = threading.Thread(target=send_request, daemon=True)
        thread.start()
    
    def _format_date(self, date_str: str) -> str:
        """Format date string to readable format."""
        if not date_str or date_str == 'TBD':
            return 'TBD'
        
        try:
            # Try parsing different date formats
            for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
                try:
                    dt = datetime.strptime(date_str[:19] if 'T' in date_str or ' ' in date_str else date_str, fmt)
                    return dt.strftime("%B %d, %Y")  # e.g., "October 15, 2025"
                except ValueError:
                    continue
            
            # If parsing fails, return as-is
            return date_str
        except Exception:
            return date_str
    
    def _format_time(self, time_str: str) -> str:
        """Format time string to readable format."""
        if not time_str or time_str == 'TBD':
            return 'TBD'
        
        try:
            # Try parsing time
            if ':' in time_str:
                parts = time_str.split(':')
                hour = int(parts[0])
                minute = int(parts[1])
                
                # Convert to 12-hour format
                period = 'AM' if hour < 12 else 'PM'
                if hour == 0:
                    hour = 12
                elif hour > 12:
                    hour -= 12
                
                return f"{hour}:{minute:02d} {period}"
            
            return time_str
        except Exception:
            return time_str


# Singleton instance
_email_service_instance = None


def get_email_service() -> EmailService:
    """
    Get singleton instance of EmailService.
    
    Returns:
        EmailService instance
    
    Example:
        from utils.email_service import get_email_service
        
        email_service = get_email_service()
        email_service.send_event_reminder(...)
    """
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailService()
    return _email_service_instance
