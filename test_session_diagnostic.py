#!/usr/bin/env python3
"""
Quick diagnostic to check what's in the session after login
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend_tkinter'))

from utils.session_manager import SessionManager
from utils.api_client import APIClient
import requests

API_BASE_URL = "http://localhost:8080/api"
ORGANIZER_EMAIL = "organizer1@campus.com"
ORGANIZER_PASSWORD = "test123"

print("=" * 60)
print("SESSION DIAGNOSTIC TEST")
print("=" * 60)

# Step 1: Login
print("\n1. Logging in...")
login_url = f"{API_BASE_URL}/auth/login"
login_data = {
    "email": ORGANIZER_EMAIL,
    "password": ORGANIZER_PASSWORD
}

try:
    response = requests.post(login_url, json=login_data)
    response.raise_for_status()
    login_result = response.json()
    
    print(f"✅ Login successful!")
    print(f"\nLogin Response:")
    print(f"  - id: {login_result.get('id')}")
    print(f"  - email: {login_result.get('email')}")
    print(f"  - role: {login_result.get('role')}")
    print(f"  - token: {login_result.get('token')[:30] if login_result.get('token') else 'None'}...")
    
    # Step 2: Store in session (like login page does)
    print("\n2. Storing in SessionManager...")
    session = SessionManager()
    session.store_user(
        user_id=login_result.get('id'),
        username=login_result.get('email'),
        role=login_result.get('role'),
        token=login_result.get('token'),
        token_expires_in=86400
    )
    print("✅ Session stored")
    
    # Step 3: Retrieve from session
    print("\n3. Retrieving from SessionManager...")
    user_data = session.get_user()
    
    if user_data:
        print(f"✅ Session retrieved!")
        print(f"\nSession Data:")
        print(f"  Keys: {list(user_data.keys())}")
        for key, value in user_data.items():
            print(f"  - {key}: {value}")
        
        # Check what key has the ID
        print(f"\n4. Checking ID keys:")
        print(f"  - user_data.get('id'): {user_data.get('id')}")
        print(f"  - user_data.get('user_id'): {user_data.get('user_id')}")
        
        user_id = user_data.get('id') or user_data.get('user_id')
        if user_id:
            print(f"\n✅ User ID found: {user_id}")
            print(f"\n5. This is what should be sent as organizerId in create event")
        else:
            print(f"\n❌ No user ID found!")
    else:
        print(f"❌ Session data is None!")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)

