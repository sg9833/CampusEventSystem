#!/usr/bin/env python3
"""
Test script to verify Create Event API works correctly
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "http://localhost:8080/api"
ORGANIZER_EMAIL = "organizer1@campus.com"
ORGANIZER_PASSWORD = "test123"

def test_create_event():
    """Test the create event functionality"""
    
    print("=" * 60)
    print("CREATE EVENT API TEST")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1. Logging in as organizer...")
    login_url = f"{API_BASE_URL}/auth/login"
    login_data = {
        "email": ORGANIZER_EMAIL,
        "password": ORGANIZER_PASSWORD
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        response.raise_for_status()
        login_result = response.json()
        
        token = login_result.get('token')
        user_id = login_result.get('id') or login_result.get('userId')  # Try both
        
        if not token or not user_id:
            print("❌ Login failed: No token or user ID in response")
            print(f"Response: {login_result}")
            return False
        
        print(f"✅ Login successful!")
        print(f"   User ID: {user_id}")
        print(f"   Token: {token[:20]}...")
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    # Step 2: Create Event
    print("\n2. Creating a test event...")
    create_url = f"{API_BASE_URL}/events"
    
    # Prepare event data (matching backend DTO)
    # Use ISO 8601 format with 'T' separator for Java LocalDateTime
    future_date = (datetime.now() + timedelta(days=7))
    start_time = future_date.replace(hour=9, minute=0, second=0)
    end_time = future_date.replace(hour=17, minute=0, second=0)
    
    event_data = {
        "title": "Test Event - API Verification",
        "description": "This is a test event to verify the create event API works correctly after the fix.",
        "organizerId": user_id,  # Required!
        "startTime": start_time.strftime('%Y-%m-%dT%H:%M:%S'),  # ISO 8601 format with T
        "endTime": end_time.strftime('%Y-%m-%dT%H:%M:%S'),      # ISO 8601 format with T
        "venue": "Test Auditorium"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n   Sending payload:")
    print(f"   {json.dumps(event_data, indent=4)}")
    
    try:
        response = requests.post(create_url, json=event_data, headers=headers)
        
        print(f"\n   Response Status: {response.status_code}")
        print(f"   Response Body: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Event created successfully!")
            print(f"   Event ID: {result.get('id')}")
            print(f"   Message: {result.get('message')}")
            return True
        elif response.status_code == 403:
            print(f"\n❌ 403 Forbidden Error!")
            print(f"   This means the authorization failed.")
            print(f"   Response: {response.text}")
            return False
        elif response.status_code == 400:
            print(f"\n❌ 400 Bad Request!")
            print(f"   This means validation failed.")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"\n❌ Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Create event failed: {e}")
        return False

def check_backend():
    """Check if backend is running"""
    print("\n0. Checking if backend is running...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        print("✅ Backend is running!")
        return True
    except Exception as e:
        print(f"❌ Backend is not running: {e}")
        print("\nPlease start the backend first:")
        print("   ./run.sh")
        return False

if __name__ == "__main__":
    if check_backend():
        success = test_create_event()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ TEST PASSED - Create Event is working!")
        else:
            print("❌ TEST FAILED - Create Event is not working")
        print("=" * 60)
    else:
        print("\n❌ Cannot run test - Backend is not available")

