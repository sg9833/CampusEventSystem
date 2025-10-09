"""
Test Data Setup Script
Campus Event & Resource Coordination System v2.0.0

This script helps prepare test data for manual testing.
Run this before executing test cases to ensure required test accounts and data exist.

Usage:
    python test_data_setup.py

Requirements:
    - Backend server running on http://localhost:8080
    - Database initialized with schema.sql
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "http://localhost:8080/api"
TEST_ACCOUNTS = [
    {
        "fullName": "John Student",
        "email": "student@test.com",
        "password": "Student123!",
        "role": "STUDENT"
    },
    {
        "fullName": "Jane Organizer",
        "email": "organizer@test.com",
        "password": "Organizer123!",
        "role": "ORGANIZER"
    },
    {
        "fullName": "Admin User",
        "email": "admin@test.com",
        "password": "Admin123!",
        "role": "ADMIN"
    }
]

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def register_account(account):
    """Register a test account"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json=account,
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ Created account: {account['email']}")
            return True
        elif response.status_code == 400:
            print(f"⚠️  Account already exists: {account['email']}")
            return True
        else:
            print(f"❌ Failed to create account: {account['email']} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating account {account['email']}: {str(e)}")
        return False

def login(email, password):
    """Login and get token"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('token')
        return None
    except requests.exceptions.RequestException:
        return None

def create_sample_resources(admin_token):
    """Create sample resources for testing"""
    resources = [
        {
            "name": "Main Auditorium",
            "type": "AUDITORIUM",
            "capacity": 500,
            "description": "Large auditorium for conferences and seminars",
            "location": "Building A, Floor 1",
            "facilities": ["Projector", "Sound System", "Air Conditioning", "Stage"]
        },
        {
            "name": "Computer Lab 1",
            "type": "LAB",
            "capacity": 40,
            "description": "Computer lab with 40 workstations",
            "location": "Building B, Floor 2",
            "facilities": ["Computers", "Projector", "Whiteboard", "Air Conditioning"]
        },
        {
            "name": "Classroom 201",
            "type": "CLASSROOM",
            "capacity": 60,
            "description": "Standard classroom for lectures",
            "location": "Building C, Floor 2",
            "facilities": ["Projector", "Whiteboard", "Air Conditioning"]
        },
        {
            "name": "Sports Field",
            "type": "SPORTS",
            "capacity": 200,
            "description": "Outdoor sports field for events",
            "location": "Campus Ground",
            "facilities": ["Seating", "Lighting", "Changing Rooms"]
        },
        {
            "name": "Meeting Room A",
            "type": "MEETING_ROOM",
            "capacity": 20,
            "description": "Small meeting room for workshops",
            "location": "Building D, Floor 1",
            "facilities": ["Projector", "Whiteboard", "Video Conference"]
        }
    ]
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    created = 0
    
    for resource in resources:
        try:
            response = requests.post(
                f"{API_BASE_URL}/resources",
                json=resource,
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                print(f"✅ Created resource: {resource['name']}")
                created += 1
            elif response.status_code == 400:
                print(f"⚠️  Resource already exists: {resource['name']}")
            else:
                print(f"❌ Failed to create resource: {resource['name']}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating resource {resource['name']}: {str(e)}")
    
    return created

def create_sample_events(organizer_token):
    """Create sample events for testing"""
    now = datetime.now()
    
    events = [
        {
            "title": "Tech Conference 2024",
            "description": "Annual technology conference featuring industry leaders",
            "category": "CONFERENCE",
            "startDateTime": (now + timedelta(days=30)).isoformat(),
            "endDateTime": (now + timedelta(days=30, hours=8)).isoformat(),
            "location": "Main Auditorium",
            "capacity": 500,
            "registrationDeadline": (now + timedelta(days=25)).isoformat(),
            "isPublic": True
        },
        {
            "title": "Python Workshop",
            "description": "Hands-on Python programming workshop for beginners",
            "category": "WORKSHOP",
            "startDateTime": (now + timedelta(days=15)).isoformat(),
            "endDateTime": (now + timedelta(days=15, hours=4)).isoformat(),
            "location": "Computer Lab 1",
            "capacity": 40,
            "registrationDeadline": (now + timedelta(days=10)).isoformat(),
            "isPublic": True
        },
        {
            "title": "Sports Day 2024",
            "description": "Annual sports day with various competitions",
            "category": "SPORTS",
            "startDateTime": (now + timedelta(days=45)).isoformat(),
            "endDateTime": (now + timedelta(days=45, hours=10)).isoformat(),
            "location": "Sports Field",
            "capacity": 200,
            "registrationDeadline": (now + timedelta(days=40)).isoformat(),
            "isPublic": True
        },
        {
            "title": "Guest Lecture: AI in Education",
            "description": "Guest lecture by Dr. Smith on AI applications in education",
            "category": "SEMINAR",
            "startDateTime": (now + timedelta(days=7)).isoformat(),
            "endDateTime": (now + timedelta(days=7, hours=2)).isoformat(),
            "location": "Classroom 201",
            "capacity": 60,
            "registrationDeadline": (now + timedelta(days=5)).isoformat(),
            "isPublic": True
        },
        {
            "title": "Student Club Meeting",
            "description": "Monthly meeting of the Computer Science Club",
            "category": "CLUB",
            "startDateTime": (now + timedelta(days=3)).isoformat(),
            "endDateTime": (now + timedelta(days=3, hours=2)).isoformat(),
            "location": "Meeting Room A",
            "capacity": 20,
            "registrationDeadline": (now + timedelta(days=2)).isoformat(),
            "isPublic": False
        }
    ]
    
    headers = {"Authorization": f"Bearer {organizer_token}"}
    created = 0
    
    for event in events:
        try:
            response = requests.post(
                f"{API_BASE_URL}/events",
                json=event,
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                print(f"✅ Created event: {event['title']}")
                created += 1
            elif response.status_code == 400:
                print(f"⚠️  Event creation failed: {event['title']} - {response.text}")
            else:
                print(f"❌ Failed to create event: {event['title']}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating event {event['title']}: {str(e)}")
    
    return created

def main():
    """Main setup function"""
    print("=" * 60)
    print("🧪 Test Data Setup Script")
    print("Campus Event & Resource Coordination System v2.0.0")
    print("=" * 60)
    print()
    
    # Step 1: Check backend
    print("Step 1: Checking backend server...")
    if not check_backend():
        print("❌ Backend server is not running!")
        print("Please start the backend server first:")
        print("  cd backend_java/backend")
        print("  mvn spring-boot:run")
        return False
    print("✅ Backend server is running")
    print()
    
    # Step 2: Create test accounts
    print("Step 2: Creating test accounts...")
    success_count = 0
    for account in TEST_ACCOUNTS:
        if register_account(account):
            success_count += 1
    print(f"Created/Verified {success_count}/{len(TEST_ACCOUNTS)} test accounts")
    print()
    
    # Step 3: Login as admin
    print("Step 3: Logging in as admin...")
    admin_token = login("admin@test.com", "Admin123!")
    if not admin_token:
        print("❌ Failed to login as admin")
        print("Please check if admin account was created successfully")
        return False
    print("✅ Admin login successful")
    print()
    
    # Step 4: Create resources
    print("Step 4: Creating sample resources...")
    resources_created = create_sample_resources(admin_token)
    print(f"Created {resources_created} resources")
    print()
    
    # Step 5: Login as organizer
    print("Step 5: Logging in as organizer...")
    organizer_token = login("organizer@test.com", "Organizer123!")
    if not organizer_token:
        print("❌ Failed to login as organizer")
        return False
    print("✅ Organizer login successful")
    print()
    
    # Step 6: Create events
    print("Step 6: Creating sample events...")
    events_created = create_sample_events(organizer_token)
    print(f"Created {events_created} events")
    print()
    
    # Summary
    print("=" * 60)
    print("✅ Test Data Setup Complete!")
    print("=" * 60)
    print()
    print("Test Accounts Created:")
    print("  👨‍🎓 Student:   student@test.com / Student123!")
    print("  👨‍💼 Organizer: organizer@test.com / Organizer123!")
    print("  👨‍💻 Admin:     admin@test.com / Admin123!")
    print()
    print(f"Sample Data Created:")
    print(f"  📍 Resources: {resources_created}")
    print(f"  🎉 Events: {events_created}")
    print()
    print("You can now proceed with testing!")
    print("See TEST_EXECUTION_GUIDE.md for testing instructions.")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n⚠️  Setup completed with warnings. Review messages above.")
            exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        exit(1)
