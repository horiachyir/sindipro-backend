#!/usr/bin/env python3
import os
import sys
import django
import json

# Add project to path
sys.path.insert(0, '/home/administrator/Documents/SINDIPRO-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from field_mgmt.views import technical_requests
import base64

User = get_user_model()

# Create request factory
factory = RequestFactory()

# Get or create a test user
try:
    user = User.objects.get(email='test@gmail.com')
except User.DoesNotExist:
    user = User.objects.create_user(
        email='test@gmail.com',
        password='password123',
        first_name='Test',
        last_name='User',
        username='testuser'
    )

# Larger test image to verify complete transmission
test_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8/5+hnoEIwDiqkL4KAcT9GO0U4BxoAAAAAElFTkSuQmCC"

print("=== Testing API Endpoint with Complete Image Data ===\n")

# Test POST with urgent priority
print("1. Testing POST with 'urgent' priority...")
post_data = {
    "company_email": "api.test@example.com",
    "description": "API endpoint test with complete image data",
    "location": "Testing Lab",
    "priority": "urgent",
    "title": "Urgent API Test",
    "image_data": [test_image]
}

request = factory.post('/api/field/technical/', 
                      data=json.dumps(post_data),
                      content_type='application/json')
request.user = user

response = technical_requests(request)
print(f"Response status: {response.status_code}")

if response.status_code == 201:
    created_id = response.data['id']
    print(f"✓ Created technical request with ID: {created_id}")
    print(f"  Priority: {response.data['priority']}")
else:
    print(f"✗ Error: {response.data}")

# Test GET to verify complete data is returned
print("\n2. Testing GET to verify complete image data...")
request = factory.get('/api/field/technical/')
request.user = user

response = technical_requests(request)
print(f"Response status: {response.status_code}")

if response.status_code == 200:
    # Find our created request
    for item in response.data:
        if item.get('title') == 'Urgent API Test':
            print(f"\n✓ Found our technical request:")
            print(f"  ID: {item['id']}")
            print(f"  Priority: {item['priority']}")
            print(f"  Number of images: {len(item['images'])}")
            
            if item['images']:
                image_data = item['images'][0]
                returned_url = image_data['image_data_url']
                
                # Verify complete data
                original_base64 = test_image.split(',')[1]
                returned_base64 = returned_url.split(',')[1]
                
                print(f"\n  Image data verification:")
                print(f"    MIME type: {image_data['mime_type']}")
                print(f"    Original base64 length: {len(original_base64)}")
                print(f"    Returned base64 length: {len(returned_base64)}")
                print(f"    Complete match: {'✓ YES' if original_base64 == returned_base64 else '✗ NO'}")
                
                # Show first and last 20 chars to verify start and end
                print(f"    First 20 chars match: {original_base64[:20] == returned_base64[:20]}")
                print(f"    Last 20 chars match: {original_base64[-20:] == returned_base64[-20:]}")
            break

print("\n=== API test completed successfully! ===")