#!/usr/bin/env python3
import requests
import json

# First, let's login to get the authentication token
login_url = 'http://localhost:8000/api/auth/login/'
login_data = {
    'email': 'test@gmail.com',  # Using existing user
    'password': 'password123'  # Replace with actual password
}

print("Attempting to login...")
login_response = requests.post(login_url, json=login_data)
if login_response.status_code == 200:
    token = login_response.json().get('access')
    print(f"Login successful. Token: {token[:20]}...")
else:
    print(f"Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

# Test data matching the frontend structure
test_data = {
    "company_email": "sergeiromanoff.job@gmail.com",
    "description": "Hello",
    "location": "test2",
    "priority": "medium",
    "title": "Test 1",
    "image_data": [
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    ]
}

# Make the POST request
url = 'http://localhost:8000/api/field/technical/'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

print("\nSending POST request to /api/field/technical/...")
print(f"Data: {json.dumps(test_data, indent=2)}")

response = requests.post(url, json=test_data, headers=headers)

print(f"\nResponse Status: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response Body: {response.text}")

# Test GET request
print("\n\nTesting GET request...")
get_response = requests.get(url, headers=headers)
print(f"GET Response Status: {get_response.status_code}")
if get_response.status_code == 200:
    data = get_response.json()
    print(f"Number of records: {len(data)}")
    if data:
        print(f"Latest record: {json.dumps(data[0], indent=2)}")