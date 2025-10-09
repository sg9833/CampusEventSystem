"""
Email Notification Testing and Scheduled Jobs

This script demonstrates:
1. Testing email notification system
2. Scheduled event reminders (1 day before)
3. Weekly digest emails
4. Bulk notifications

Usage:
    python test_email_notifications.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.email_service import get_email_service
from utils.api_client import APIClient
from datetime import datetime, timedelta
import time


def test_event_registration_email():
    """Test event registration confirmation email"""
    print("\n" + "="*60)
    print("TEST 1: Event Registration Confirmation Email")
    print("="*60)
    
    email_service = get_email_service()
    
    email_service.send_event_registration_confirmation(
        user_email="test@example.com",
        event_details={
            "title": "Python Programming Workshop",
            "date": "2025-10-15",
            "time": "14:00",
            "location": "Computer Lab, Room 301"
        },
        user_name="John Doe"
    )
    
    print("✅ Event registration email sent!")
    print("Check backend console for email content")
    time.sleep(2)


def test_event_reminder_email():
    """Test event reminder email"""
    print("\n" + "="*60)
    print("TEST 2: Event Reminder Email (1 Day Before)")
    print("="*60)
    
    email_service = get_email_service()
    
    # Event happening tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    
    email_service.send_event_reminder(
        user_email="test@example.com",
        event_details={
            "title": "Python Programming Workshop",
            "date": tomorrow.strftime("%Y-%m-%d"),
            "time": "14:00",
            "location": "Computer Lab, Room 301"
        },
        user_name="John Doe",
        days_before=1
    )
    
    print("✅ Event reminder email sent!")
    print("Check backend console for email content")
    time.sleep(2)


def test_booking_confirmation_email():
    """Test booking confirmation email"""
    print("\n" + "="*60)
    print("TEST 3: Booking Confirmation Email")
    print("="*60)
    
    email_service = get_email_service()
    
    # Approved booking
    email_service.send_booking_confirmation(
        user_email="test@example.com",
        booking_details={
            "resource_name": "Conference Room A",
            "date": "2025-10-20",
            "start_time": "14:00",
            "end_time": "16:00"
        },
        status="approved",
        user_name="Jane Smith"
    )
    
    print("✅ Booking confirmation email sent!")
    print("Check backend console for email content")
    time.sleep(2)


def test_approval_notification_email():
    """Test approval/rejection notification email"""
    print("\n" + "="*60)
    print("TEST 4: Approval Notification Email")
    print("="*60)
    
    email_service = get_email_service()
    
    # Event approved
    email_service.send_approval_notification(
        user_email="organizer@example.com",
        item_type="event",
        item_name="Python Programming Workshop",
        status="approved",
        reason="Your event meets all requirements and has been approved for publication.",
        user_name="Dr. Smith"
    )
    
    print("✅ Approval notification email sent!")
    time.sleep(1)
    
    # Event rejected
    email_service.send_approval_notification(
        user_email="organizer@example.com",
        item_type="event",
        item_name="Test Event",
        status="rejected",
        reason="Insufficient details provided. Please include event description and target audience.",
        user_name="Dr. Smith"
    )
    
    print("✅ Rejection notification email sent!")
    print("Check backend console for email content")
    time.sleep(2)


def test_weekly_digest_email():
    """Test weekly digest email"""
    print("\n" + "="*60)
    print("TEST 5: Weekly Digest Email")
    print("="*60)
    
    email_service = get_email_service()
    
    # Sample upcoming events
    events = [
        {
            "title": "Python Programming Workshop",
            "date": "2025-10-15",
            "location": "Computer Lab, Room 301"
        },
        {
            "title": "Career Fair 2025",
            "date": "2025-10-17",
            "location": "Main Hall, Building A"
        },
        {
            "title": "Hackathon Kickoff",
            "date": "2025-10-19",
            "location": "Innovation Center"
        }
    ]
    
    email_service.send_weekly_digest(
        user_email="test@example.com",
        events=events,
        user_name="John Doe"
    )
    
    print("✅ Weekly digest email sent!")
    print("Check backend console for email content")
    time.sleep(2)


def test_bulk_notifications():
    """Test bulk email notifications"""
    print("\n" + "="*60)
    print("TEST 6: Bulk Email Notifications")
    print("="*60)
    
    email_service = get_email_service()
    
    recipients = [
        "student1@example.com",
        "student2@example.com",
        "student3@example.com"
    ]
    
    email_service.send_bulk_notifications(
        recipients=recipients,
        subject="Event Cancelled: Python Workshop",
        email_type="event_reminder",
        data={
            "user_name": "Student",
            "event_title": "Python Programming Workshop",
            "event_date": "October 15, 2025",
            "event_time": "2:00 PM",
            "event_location": "Computer Lab, Room 301"
        }
    )
    
    print(f"✅ Bulk email sent to {len(recipients)} recipients!")
    print("Check backend console for email content")
    time.sleep(2)


def send_scheduled_event_reminders():
    """
    Scheduled job to send event reminders (1 day before)
    
    This should be run daily (e.g., via cron job or scheduler)
    """
    print("\n" + "="*60)
    print("SCHEDULED JOB: Event Reminders (1 Day Before)")
    print("="*60)
    
    api = APIClient()
    email_service = get_email_service()
    
    try:
        # Get tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")
        
        print(f"Checking for events on {tomorrow_str}...")
        
        # Get all events happening tomorrow
        events = api.get("events")
        
        if not events:
            print("No events found in system")
            return
        
        # Filter events happening tomorrow
        tomorrow_events = []
        for event in events:
            event_date = event.get('date', event.get('start_date', ''))
            if event_date and event_date[:10] == tomorrow_str:
                tomorrow_events.append(event)
        
        print(f"Found {len(tomorrow_events)} event(s) happening tomorrow")
        
        # For each event, get registered users and send reminders
        for event in tomorrow_events:
            event_id = event.get('id')
            event_title = event.get('title', event.get('name', 'Event'))
            
            print(f"\nProcessing event: {event_title}")
            
            try:
                # Get registered users for this event
                # Note: This endpoint needs to be implemented in backend
                registered_users = api.get(f"events/{event_id}/registered-users")
                
                if registered_users:
                    print(f"  Sending reminders to {len(registered_users)} user(s)...")
                    
                    for user in registered_users:
                        user_email = user.get('email')
                        user_name = user.get('name', 'Student')
                        
                        if user_email:
                            email_service.send_event_reminder(
                                user_email=user_email,
                                event_details=event,
                                user_name=user_name,
                                days_before=1
                            )
                            print(f"    ✅ Reminder sent to {user_email}")
                    
                    print(f"  Completed: {len(registered_users)} reminder(s) sent")
                else:
                    print(f"  No registered users for this event")
                    
            except Exception as e:
                print(f"  ❌ Error processing event {event_title}: {e}")
        
        print(f"\n✅ Event reminder job completed!")
        print(f"   Total events processed: {len(tomorrow_events)}")
        
    except Exception as e:
        print(f"❌ Error in scheduled reminder job: {e}")


def send_weekly_digest():
    """
    Scheduled job to send weekly digest (every Monday)
    
    This should be run weekly (e.g., via cron job)
    """
    print("\n" + "="*60)
    print("SCHEDULED JOB: Weekly Event Digest")
    print("="*60)
    
    api = APIClient()
    email_service = get_email_service()
    
    try:
        # Get date range (next 7 days)
        today = datetime.now()
        next_week = today + timedelta(days=7)
        
        print(f"Generating digest for: {today.strftime('%Y-%m-%d')} to {next_week.strftime('%Y-%m-%d')}")
        
        # Get all upcoming events
        events = api.get("events")
        
        if not events:
            print("No events found in system")
            return
        
        # Filter events in next 7 days
        upcoming_events = []
        for event in events:
            event_date_str = event.get('date', event.get('start_date', ''))
            if event_date_str:
                try:
                    event_date = datetime.strptime(event_date_str[:10], "%Y-%m-%d")
                    if today <= event_date <= next_week:
                        upcoming_events.append(event)
                except ValueError:
                    continue
        
        print(f"Found {len(upcoming_events)} upcoming event(s)")
        
        if not upcoming_events:
            print("No upcoming events to include in digest")
            return
        
        # Get all active users
        # Note: This endpoint needs to be implemented in backend
        try:
            users = api.get("users/active")
            
            if not users:
                print("No active users found")
                return
            
            print(f"Sending digest to {len(users)} user(s)...")
            
            for user in users:
                user_email = user.get('email')
                user_name = user.get('name', 'Student')
                
                if user_email:
                    email_service.send_weekly_digest(
                        user_email=user_email,
                        events=upcoming_events,
                        user_name=user_name
                    )
                    print(f"  ✅ Digest sent to {user_email}")
            
            print(f"\n✅ Weekly digest job completed!")
            print(f"   Recipients: {len(users)}")
            print(f"   Events included: {len(upcoming_events)}")
            
        except Exception as e:
            print(f"❌ Could not get active users: {e}")
            print("   Skipping weekly digest")
        
    except Exception as e:
        print(f"❌ Error in weekly digest job: {e}")


def main():
    """Run all email notification tests"""
    print("\n" + "="*60)
    print("EMAIL NOTIFICATION SYSTEM - TEST SUITE")
    print("="*60)
    print("\nThis script will test all email notification features.")
    print("Make sure your backend is running on port 8080.")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    # Run all tests
    try:
        test_event_registration_email()
        test_event_reminder_email()
        test_booking_confirmation_email()
        test_approval_notification_email()
        test_weekly_digest_email()
        test_bulk_notifications()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60)
        print("\nCheck your backend console to see the email content.")
        print("In production, these would be sent via email service (SendGrid, AWS SES, etc.)")
        
        print("\n" + "="*60)
        print("SCHEDULED JOB EXAMPLES")
        print("="*60)
        print("\nWould you like to test scheduled jobs? (y/n)")
        response = input().lower()
        
        if response == 'y':
            print("\nRunning scheduled job examples...")
            send_scheduled_event_reminders()
            send_weekly_digest()
        
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")


if __name__ == "__main__":
    main()
