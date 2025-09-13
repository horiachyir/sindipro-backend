#!/usr/bin/env python3
import requests
import json

# Test the unique code generation for technical field requests
# We'll test both POST (creating with code generation) and GET (retrieving with code)

# First, let's login to get the authentication token
login_url = 'http://localhost:8000/api/auth/login/'
login_data = {
    'email': 'test@gmail.com',
    'password': 'password123'
}

print("Testing unique code generation for /api/field/technical/")
print("=" * 60)

print("\n1. Attempting to login...")
login_response = requests.post(login_url, json=login_data)
if login_response.status_code == 200:
    token = login_response.json().get('access')
    print(f"   ✓ Login successful. Token: {token[:20]}...")
else:
    print(f"   ✗ Login failed: {login_response.status_code}")
    print(f"   Error: {login_response.text}")
    exit(1)

# Test data
test_data = {
    "company_email": "test.code@example.com",
    "description": "Testing unique code generation",
    "location": "Test Location",
    "priority": "medium",
    "title": "Code Generation Test"
}

# Test POST request - should generate a unique code
url = 'http://localhost:8000/api/field/technical/'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

print("\n2. Testing POST request (should generate unique code)...")
response = requests.post(url, json=test_data, headers=headers)

print(f"   Status: {response.status_code}")
if response.status_code == 201:
    response_data = response.json()
    print(f"   ✓ Request created successfully!")
    print(f"   Generated code: {response_data.get('code')}")
    print(f"   ID: {response_data.get('id')}")
    print(f"   Title: {response_data.get('title')}")
    created_id = response_data.get('id')
    created_code = response_data.get('code')
else:
    print(f"   ✗ POST request failed")
    print(f"   Error: {response.text}")
    exit(1)

# Test GET request - should include the code in response
print("\n3. Testing GET request (should include codes)...")
get_response = requests.get(url, headers=headers)
print(f"   Status: {get_response.status_code}")

if get_response.status_code == 200:
    data = get_response.json()
    print(f"   ✓ Retrieved {len(data)} records")

    # Find our created record
    our_record = None
    for record in data:
        if record.get('id') == created_id:
            our_record = record
            break

    if our_record:
        print(f"   ✓ Found our created record:")
        print(f"     - ID: {our_record.get('id')}")
        print(f"     - Code: {our_record.get('code')}")
        print(f"     - Title: {our_record.get('title')}")
        print(f"     - Company Email: {our_record.get('company_email')}")

        # Verify the code matches what we got from POST
        if our_record.get('code') == created_code:
            print(f"   ✓ Code consistency check passed!")
        else:
            print(f"   ✗ Code mismatch: POST returned '{created_code}', GET returned '{our_record.get('code')}'")
    else:
        print(f"   ✗ Could not find our created record in GET response")
else:
    print(f"   ✗ GET request failed: {get_response.status_code}")
    print(f"   Error: {get_response.text}")

# Test creating multiple records to verify unique codes
print("\n4. Testing unique code generation (creating multiple records)...")
codes_generated = []

for i in range(3):
    test_data_multi = {
        "company_email": f"test.code{i}@example.com",
        "description": f"Testing unique code generation #{i+1}",
        "location": "Test Location",
        "priority": "low",
        "title": f"Code Generation Test #{i+1}"
    }

    response = requests.post(url, json=test_data_multi, headers=headers)
    if response.status_code == 201:
        response_data = response.json()
        code = response_data.get('code')
        codes_generated.append(code)
        print(f"   ✓ Record {i+1}: Generated code '{code}'")
    else:
        print(f"   ✗ Failed to create record {i+1}: {response.status_code}")

# Check if all codes are unique
if len(codes_generated) == len(set(codes_generated)):
    print(f"   ✓ All {len(codes_generated)} generated codes are unique!")
else:
    print(f"   ✗ Duplicate codes detected: {codes_generated}")

print("\n" + "=" * 60)
print("Test completed!")