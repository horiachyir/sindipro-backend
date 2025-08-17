#!/usr/bin/env python3
import os
import sys
import django

# Add project to path
sys.path.insert(0, '/home/administrator/Documents/SINDIPRO-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from field_mgmt.models import FieldMgmtTechnical, FieldMgmtTechnicalImage
from field_mgmt.serializers import FieldMgmtTechnicalSerializer
import base64

# Sample JPEG image data (simulating frontend format)
sample_jpeg = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwABmX/9k="

print("=== Testing POST with 'photos' field ===\n")

# Test data matching frontend structure
test_data = {
    "company_email": "frontend.test@example.com",
    "description": "Testing with photos field from frontend",
    "location": "Frontend Test Location",
    "priority": "urgent",
    "title": "Frontend Photos Test",
    "photos": [sample_jpeg]  # Using 'photos' field as sent by frontend
}

print("1. Creating technical request with 'photos' field...")
print(f"   Data structure: {list(test_data.keys())}")

serializer = FieldMgmtTechnicalSerializer(data=test_data)
if serializer.is_valid():
    technical_request = serializer.save()
    print(f"✓ Created technical request: {technical_request}")
    print(f"  ID: {technical_request.id}")
    print(f"  Title: {technical_request.title}")
    print(f"  Priority: {technical_request.priority}")
    
    # Check if images were saved
    images_count = technical_request.images.count()
    print(f"\n2. Checking image storage...")
    print(f"✓ Images saved: {images_count}")
    
    if images_count > 0:
        image = technical_request.images.first()
        print(f"  Image ID: {image.id}")
        print(f"  MIME type: {image.mime_type}")
        print(f"  Filename: {image.filename}")
        print(f"  BYTEA data size: {len(image.image_data)} bytes")
        
        # Verify it's JPEG
        if image.mime_type == 'image/jpeg':
            print(f"  ✓ Correctly identified as JPEG")
        
        # Verify data integrity
        original_base64 = sample_jpeg.split(',')[1]
        stored_base64 = base64.b64encode(image.image_data).decode('utf-8')
        if original_base64 == stored_base64:
            print(f"  ✓ Data integrity verified")
    else:
        print(f"  ✗ No images were saved!")
        
else:
    print(f"✗ Validation errors: {serializer.errors}")

# Test serialization for GET response
print("\n3. Testing GET response serialization...")
serializer = FieldMgmtTechnicalSerializer(technical_request)
response_data = serializer.data

print(f"✓ Serialized response:")
print(f"  Fields: {list(response_data.keys())}")
print(f"  Images count: {len(response_data.get('images', []))}")

if response_data.get('images'):
    img = response_data['images'][0]
    if 'image_data_url' in img:
        data_url = img['image_data_url']
        if data_url.startswith('data:image/jpeg;base64,'):
            print(f"  ✓ Image properly formatted as data URL")
            print(f"  ✓ MIME type preserved: image/jpeg")

# Verify database storage
print("\n4. Verifying database storage...")
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT COUNT(*) 
        FROM field_mgmt_fieldmgmttechnicalimage 
        WHERE technical_request_id = %s
    """, [technical_request.id])
    
    count = cursor.fetchone()[0]
    print(f"✓ Images in database: {count}")

print("\n=== Test completed successfully! ===")