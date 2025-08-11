import requests
import json

# Test data matching the frontend structure
test_data = {
    "active": True,
    "buildingTypes": ["residential"],
    "conditions": "Test",
    "daysBeforeExpiry": 30,
    "description": "Hello!",
    "frequency": "annual",
    "name": "Test Obligation",
    "requiresQuote": True
}

# First, we need to get a JWT token
# Using test credentials (you should replace with actual credentials)
auth_url = "http://localhost:8000/api/auth/login/"
auth_data = {
    "email": "mason@gmail.com",  # Using existing superuser
    "password": "password123"       # You may need to update this password
}

print("Testing Legal Template API Endpoint\n")
print("1. Attempting to authenticate...")
try:
    auth_response = requests.post(auth_url, json=auth_data)
    if auth_response.status_code == 200:
        tokens = auth_response.json()
        access_token = tokens.get('accessToken')
        print("✓ Authentication successful")
        
        # Test the legal template endpoint
        template_url = "http://localhost:8000/api/legal/template/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        print("\n2. Testing POST /api/legal/template/")
        print(f"Request data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(template_url, json=test_data, headers=headers)
        
        print(f"\nResponse status: {response.status_code}")
        print(f"Response body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("\n✓ Legal template created successfully!")
        else:
            print("\n✗ Failed to create legal template")
    else:
        print(f"✗ Authentication failed: {auth_response.status_code}")
        print(f"Response: {auth_response.text}")
        print("\nNote: Please update the test script with valid credentials")
        
except requests.exceptions.ConnectionError:
    print("✗ Could not connect to the server. Make sure Django is running on http://localhost:8000")
except Exception as e:
    print(f"✗ Error: {str(e)}")