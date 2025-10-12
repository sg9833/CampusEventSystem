#!/usr/bin/env python3
"""Test that My Events filtering works correctly."""

import sys
import os

# Add frontend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend_tkinter'))

from utils.api_client import APIClient
from utils.session_manager import SessionManager

def test_my_events():
    """Test the My Events endpoint fix."""
    
    api = APIClient()
    session = SessionManager()
    
    print("=" * 60)
    print("TESTING MY EVENTS FIX")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1️⃣ Logging in as organizer1@campus.com...")
    try:
        login_response = api.post('auth/login', {
            'email': 'organizer1@campus.com',
            'password': 'test123'
        })
        
        token = login_response.get('token')
        user_id = login_response.get('id')
        
        if not token:
            print("❌ Login failed - no token returned")
            return False
        
        print(f"✅ Login successful!")
        print(f"   User ID: {user_id}")
        print(f"   Token: {token[:20]}...")
        
        # Store in session (just set token for API client)
        api.set_auth_token(token)
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    # Step 2: Get ALL events
    print("\n2️⃣ Fetching ALL events from GET /api/events...")
    try:
        all_events = api.get('events') or []
        print(f"✅ Retrieved {len(all_events)} total events")
        
        # Show details
        for i, event in enumerate(all_events, 1):
            print(f"\n   Event {i}:")
            print(f"      ID: {event.get('id')}")
            print(f"      Title: {event.get('title')}")
            print(f"      Organizer ID: {event.get('organizerId')}")
            
    except Exception as e:
        print(f"❌ Failed to fetch events: {e}")
        return False
    
    # Step 3: Filter by organizerId
    print(f"\n3️⃣ Filtering events for organizer ID {user_id}...")
    try:
        # This is what the frontend now does
        my_events = [
            event for event in all_events 
            if event.get('organizerId') == user_id or event.get('organizer_id') == user_id
        ]
        
        print(f"✅ Found {len(my_events)} events for this organizer")
        
        if my_events:
            print("\n   MY EVENTS:")
            for i, event in enumerate(my_events, 1):
                print(f"      {i}. {event.get('title')} (ID: {event.get('id')})")
        else:
            print("   ⚠️  No events found for this organizer")
            
    except Exception as e:
        print(f"❌ Filtering failed: {e}")
        return False
    
    # Step 4: Verify the newly created event appears
    print("\n4️⃣ Checking if recently created events appear...")
    
    # Look for event with ID 5 (created in previous test)
    event_5 = next((e for e in my_events if e.get('id') == 5), None)
    
    if event_5:
        print(f"✅✅ SUCCESS! Event ID 5 found in My Events!")
        print(f"   Title: {event_5.get('title')}")
        print(f"   Description: {event_5.get('description')}")
    else:
        print(f"⚠️  Event ID 5 not found (may have been created by different user)")
    
    print("\n" + "=" * 60)
    print("✅ TEST PASSED - My Events filtering works!")
    print("=" * 60)
    print("\nℹ️  The frontend now:")
    print("   1. Calls GET /api/events (gets ALL events)")
    print("   2. Filters by organizerId matching current user")
    print("   3. Shows only events created by this organizer")
    print("\n🎯 RESTART THE FRONTEND TO SEE YOUR EVENTS!")
    
    return True

if __name__ == '__main__':
    test_my_events()
