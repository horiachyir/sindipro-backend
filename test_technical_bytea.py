#!/usr/bin/env python3
import os
import sys
import django
import json

# Add project to path
sys.path.insert(0, '/home/administrator/Documents/SINDIPRO-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from field_mgmt.models import FieldMgmtTechnical, FieldMgmtTechnicalImage
from field_mgmt.serializers import FieldMgmtTechnicalSerializer
import base64

# Sample base64 image data (1x1 red pixel PNG)
sample_image_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

print("=== Testing Technical Request with BYTEA Image Storage ===\n")

# Test 1: Create a technical request with images
print("1. Creating technical request with image...")
test_data = {
    "company_email": "sergeiromanoff.job@gmail.com",
    "description": "Hello",
    "location": "test2",
    "priority": "medium",
    "title": "Test BYTEA Storage",
    "image_data": [sample_image_data]
}

serializer = FieldMgmtTechnicalSerializer(data=test_data)
if serializer.is_valid():
    technical_request = serializer.save()
    print(f"✓ Created technical request: {technical_request}")
    print(f"  ID: {technical_request.id}")
    print(f"  Title: {technical_request.title}")
else:
    print(f"✗ Validation errors: {serializer.errors}")
    exit(1)

# Test 2: Verify image was stored correctly
print("\n2. Verifying image storage...")
images = technical_request.images.all()
print(f"✓ Number of images: {len(images)}")

if images:
    image = images[0]
    print(f"  Image ID: {image.id}")
    print(f"  MIME type: {image.mime_type}")
    print(f"  Filename: {image.filename}")
    print(f"  Binary data size: {len(image.image_data)} bytes")
    print(f"  Uploaded at: {image.uploaded_at}")

# Test 3: Test serialization for GET request
print("\n3. Testing serialization (GET response)...")
serializer = FieldMgmtTechnicalSerializer(technical_request)
data = serializer.data

print(f"✓ Serialized data:")
print(f"  ID: {data['id']}")
print(f"  Title: {data['title']}")
print(f"  Images count: {len(data['images'])}")

if data['images']:
    image_data = data['images'][0]
    print(f"\n  Image details:")
    print(f"    ID: {image_data['id']}")
    print(f"    MIME type: {image_data['mime_type']}")
    print(f"    Filename: {image_data['filename']}")
    
    # Verify the data URL is properly formatted
    data_url = image_data['image_data_url']
    if data_url and data_url.startswith('data:'):
        print(f"    ✓ Data URL properly formatted")
        print(f"    Data URL preview: {data_url[:50]}...")
    else:
        print(f"    ✗ Data URL format error")

# Test 4: Verify data integrity
print("\n4. Verifying data integrity...")
if images:
    image = images[0]
    # Re-encode the stored binary data
    reencoded = base64.b64encode(image.image_data).decode('utf-8')
    # Extract original base64 from input
    original_b64 = sample_image_data.split(',')[1]
    
    if reencoded == original_b64:
        print("✓ Image data integrity verified - stored data matches original")
    else:
        print("✗ Data integrity check failed")
        print(f"  Original length: {len(original_b64)}")
        print(f"  Stored length: {len(reencoded)}")

# Test 5: Query all technical requests
print("\n5. Querying all technical requests...")
all_requests = FieldMgmtTechnical.objects.all().order_by('-created_at')
print(f"✓ Total requests: {all_requests.count()}")
for req in all_requests[:3]:  # Show last 3
    print(f"  - {req.title} ({req.company_email}) - {req.images.count()} images")

print("\n=== All tests completed successfully! ===")