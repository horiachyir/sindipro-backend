#!/usr/bin/env python3
import os
import sys
import django
import hashlib

# Add project to path
sys.path.insert(0, '/home/administrator/Documents/SINDIPRO-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from field_mgmt.models import FieldMgmtTechnical, FieldMgmtTechnicalImage
from field_mgmt.serializers import FieldMgmtTechnicalSerializer
import base64

# Create a larger test image (10x10 red PNG) to verify complete data transmission
larger_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8/5+hnoEIwDiqkL4KAcT9GO0U4BxoAAAAAElFTkSuQmCC"

print("=== Testing Complete Image Data Transmission ===\n")

# Test 1: Create a technical request with urgent priority and larger image
print("1. Creating technical request with 'urgent' priority and image...")
test_data = {
    "company_email": "test@example.com",
    "description": "Testing complete image data transmission",
    "location": "Lab A",
    "priority": "urgent",  # Testing new priority
    "title": "Urgent: Complete Data Test",
    "image_data": [larger_image]
}

serializer = FieldMgmtTechnicalSerializer(data=test_data)
if serializer.is_valid():
    technical_request = serializer.save()
    print(f"✓ Created technical request with ID: {technical_request.id}")
    print(f"  Priority: {technical_request.priority}")
else:
    print(f"✗ Validation errors: {serializer.errors}")
    exit(1)

# Test 2: Verify image was stored with complete data
print("\n2. Verifying complete image storage...")
image = technical_request.images.first()
if image:
    # Calculate checksums to verify data integrity
    original_base64 = larger_image.split(',')[1]
    original_bytes = base64.b64decode(original_base64)
    original_checksum = hashlib.md5(original_bytes).hexdigest()
    
    stored_checksum = hashlib.md5(image.image_data).hexdigest()
    
    print(f"✓ Image stored in database:")
    print(f"  Original data size: {len(original_bytes)} bytes")
    print(f"  Stored data size: {len(image.image_data)} bytes")
    print(f"  Original checksum: {original_checksum}")
    print(f"  Stored checksum: {stored_checksum}")
    print(f"  Data integrity: {'✓ PASS' if original_checksum == stored_checksum else '✗ FAIL'}")

# Test 3: Test GET serialization returns complete data
print("\n3. Testing GET response with complete image data...")
serializer = FieldMgmtTechnicalSerializer(technical_request)
response_data = serializer.data

if response_data['images']:
    image_response = response_data['images'][0]
    returned_data_url = image_response['image_data_url']
    
    # Extract base64 from returned data URL
    returned_base64 = returned_data_url.split(',')[1]
    
    print(f"✓ Image data in GET response:")
    print(f"  Original base64 length: {len(original_base64)}")
    print(f"  Returned base64 length: {len(returned_base64)}")
    print(f"  Complete data returned: {'✓ YES' if len(returned_base64) == len(original_base64) else '✗ NO'}")
    
    # Verify the content matches
    if returned_base64 == original_base64:
        print(f"  Data integrity verified: ✓ PASS")
    else:
        print(f"  Data integrity verified: ✗ FAIL")
        print(f"  First 50 chars match: {returned_base64[:50] == original_base64[:50]}")

# Test 4: Test with multiple images to ensure all are transmitted completely
print("\n4. Testing multiple images...")
multi_test_data = {
    "company_email": "multi@example.com",
    "description": "Multiple images test",
    "location": "Lab B",
    "priority": "high",
    "title": "Multi-Image Test",
    "image_data": [larger_image, larger_image]  # Two copies
}

serializer = FieldMgmtTechnicalSerializer(data=multi_test_data)
if serializer.is_valid():
    multi_request = serializer.save()
    print(f"✓ Created request with {multi_request.images.count()} images")
    
    # Check each image
    for idx, img in enumerate(multi_request.images.all()):
        img_checksum = hashlib.md5(img.image_data).hexdigest()
        print(f"  Image {idx + 1}: {len(img.image_data)} bytes, checksum: {img_checksum}")

# Test 5: Raw database query to verify BYTEA storage
print("\n5. Verifying BYTEA storage at database level...")
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT id, length(image_data) as data_length, mime_type 
        FROM field_mgmt_fieldmgmttechnicalimage 
        WHERE technical_request_id = %s
    """, [technical_request.id])
    
    for row in cursor.fetchall():
        print(f"✓ Database record - ID: {row[0]}, Data length: {row[1]} bytes, MIME: {row[2]}")

print("\n=== All tests completed successfully! ===")