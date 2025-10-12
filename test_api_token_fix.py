#!/usr/bin/env python3
"""
Test that APIClient can get token from SessionManager
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend_tkinter'))

from utils.session_manager import SessionManager
from utils.api_client import APIClient

print("=" * 60)
print("API CLIENT TOKEN TEST")
print("=" * 60)

# Step 1: Store token in session
print("\n1. Storing token in SessionManager...")
session = SessionManager()
session.store_user(
    user_id=2,
    username="organizer1@campus.com",
    role="organizer",
    token="test_jwt_token_12345",
    token_expires_in=86400
)
print("✅ Token stored in session")

# Step 2: Create a NEW APIClient (like pages do)
print("\n2. Creating NEW APIClient instance...")
api = APIClient()
print("   - api.auth_token:", api.auth_token)  # Should be None initially
print("✅ New APIClient created")

# Step 3: Check if headers include token from session
print("\n3. Getting headers (should auto-fetch from SessionManager)...")
headers = api._get_headers()
print(f"   Headers: {headers}")

if 'Authorization' in headers:
    print(f"✅ Authorization header found!")
    print(f"   Value: {headers['Authorization']}")
    if "test_jwt_token_12345" in headers['Authorization']:
        print("✅✅ CORRECT TOKEN FROM SESSION!")
    else:
        print("❌ Wrong token")
else:
    print("❌ No Authorization header!")

print("\n" + "=" * 60)
print("If you see '✅✅ CORRECT TOKEN FROM SESSION!', the fix works!")
print("=" * 60)

