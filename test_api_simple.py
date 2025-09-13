import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from field_mgmt.models import FieldMgmtTechnical

User = get_user_model()

print("Testing API endpoints for unique code generation")
print("=" * 60)

# Create a test user
try:
    user = User.objects.get(email='test@gmail.com')
    print("Using existing test user")
except User.DoesNotExist:
    user = User.objects.create_user(
        email='test@gmail.com',
        password='password123',
        first_name='Test',
        last_name='User'
    )
    print("Created new test user")

# Create a client and login
client = Client()

# Test POST request
print("\n1. Testing POST /api/field/technical/")
post_data = {
    'company_email': 'api_test@example.com',
    'title': 'API Test Request',
    'description': 'Testing API code generation',
    'location': 'Test Location',
    'priority': 'medium'
}

# Authenticate
client.force_login(user)

response = client.post(
    '/api/field/technical/',
    data=json.dumps(post_data),
    content_type='application/json'
)

print(f"Status: {response.status_code}")
if response.status_code == 201:
    response_data = response.json()
    print(f"✓ Request created successfully!")
    print(f"  Generated code: {response_data.get('code')}")
    print(f"  ID: {response_data.get('id')}")
    print(f"  Title: {response_data.get('title')}")
    created_id = response_data.get('id')
    created_code = response_data.get('code')
else:
    print(f"✗ POST request failed")
    print(f"Response: {response.content.decode()}")
    exit(1)

# Test GET request
print("\n2. Testing GET /api/field/technical/")
response = client.get('/api/field/technical/')
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✓ Retrieved {len(data)} records")

    # Find our created record
    our_record = None
    for record in data:
        if record.get('id') == created_id:
            our_record = record
            break

    if our_record:
        print(f"✓ Found our created record:")
        print(f"  - ID: {our_record.get('id')}")
        print(f"  - Code: {our_record.get('code')}")
        print(f"  - Title: {our_record.get('title')}")
        print(f"  - Company Email: {our_record.get('company_email')}")

        if our_record.get('code') == created_code:
            print(f"✓ Code consistency check passed!")
        else:
            print(f"✗ Code mismatch!")
    else:
        print(f"✗ Could not find our created record")
else:
    print(f"✗ GET request failed: {response.status_code}")
    print(f"Response: {response.content.decode()}")

# Clean up
print("\n3. Cleaning up test data...")
try:
    record = FieldMgmtTechnical.objects.get(id=created_id)
    record.delete()
    print("✓ Test record deleted")
except:
    print("! Could not delete test record")

print("\n" + "=" * 60)
print("API test completed!")