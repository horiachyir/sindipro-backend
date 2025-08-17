#!/usr/bin/env python3
import os
import sys
import django

# Add project to path
sys.path.insert(0, '/home/administrator/Documents/SINDIPRO-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from field_mgmt.views import technical_requests
import json

User = get_user_model()

# Create request factory
factory = RequestFactory()

# Get a user or create one
try:
    user = User.objects.get(email='test@gmail.com')
except User.DoesNotExist:
    print("Creating test user...")
    user = User.objects.create_user(
        email='test@gmail.com',
        password='password123',
        first_name='Test',
        last_name='User',
        username='testuser'
    )

# Test data
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

# Create a POST request
request = factory.post('/api/field/technical/', 
                      data=json.dumps(test_data),
                      content_type='application/json')
request.user = user

print("Testing POST /api/field/technical/...")
response = technical_requests(request)
print(f"Response status: {response.status_code}")
print(f"Response data: {response.data}")

# Create a GET request
request = factory.get('/api/field/technical/')
request.user = user

print("\nTesting GET /api/field/technical/...")
response = technical_requests(request)
print(f"Response status: {response.status_code}")
print(f"Number of records: {len(response.data)}")
if response.data:
    print(f"Latest record: {response.data[0]}")