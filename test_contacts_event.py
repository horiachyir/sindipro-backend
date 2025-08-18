import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login/"
EVENT_URL = f"{BASE_URL}/api/contacts/event/"

# Test credentials (you should replace with actual test credentials)
TEST_USER = {
    "username": "testuser",
    "password": "testpass"
}

def get_auth_token():
    """Get authentication token"""
    response = requests.post(LOGIN_URL, data=TEST_USER)
    if response.status_code == 200:
        return response.json().get('access')
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

def test_create_event():
    """Test creating a contact event"""
    token = get_auth_token()
    if not token:
        print("Failed to get auth token, skipping test")
        return
    
    # Test data matching the frontend structure
    event_data = {
        "title": "dfdf",
        "event_type": "meetingEvent",
        "date_time": "2025-08-18T06:53:00Z",
        "condominium": "Edifício Central",
        "people_involved": ["dfe"],
        "comments": "dfdfd"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("Testing POST /api/contacts/event/")
    print(f"Data: {json.dumps(event_data, indent=2)}")
    
    response = requests.post(EVENT_URL, json=event_data, headers=headers)
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ Event created successfully!")
    else:
        print("❌ Failed to create event")

if __name__ == "__main__":
    test_create_event()