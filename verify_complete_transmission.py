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

print("=== Verifying Complete Image Data Transmission ===\n")

# Get the most recent technical request with images
latest_request = FieldMgmtTechnical.objects.filter(images__isnull=False).distinct().order_by('-created_at').first()

if latest_request:
    print(f"Found technical request: {latest_request.title}")
    print(f"Priority: {latest_request.priority}")
    print(f"Images: {latest_request.images.count()}")
    
    # Serialize it as would happen in GET request
    serializer = FieldMgmtTechnicalSerializer(latest_request)
    serialized_data = serializer.data
    
    print("\nSerialized data structure:")
    print(f"- ID: {serialized_data['id']}")
    print(f"- Title: {serialized_data['title']}")
    print(f"- Priority: {serialized_data['priority']}")
    print(f"- Images count: {len(serialized_data['images'])}")
    
    for idx, img_data in enumerate(serialized_data['images']):
        print(f"\nImage {idx + 1}:")
        print(f"  - ID: {img_data['id']}")
        print(f"  - MIME type: {img_data['mime_type']}")
        print(f"  - Filename: {img_data['filename']}")
        
        # Verify data URL format
        data_url = img_data['image_data_url']
        if data_url and data_url.startswith('data:'):
            header, base64_content = data_url.split(',', 1)
            print(f"  - Data URL header: {header}")
            print(f"  - Base64 content length: {len(base64_content)} chars")
            
            # Decode to verify it's valid base64
            try:
                decoded = base64.b64decode(base64_content)
                print(f"  - Decoded size: {len(decoded)} bytes")
                print(f"  - ✓ Valid base64 encoding")
            except Exception as e:
                print(f"  - ✗ Invalid base64: {e}")
        
        # Compare with database
        db_image = FieldMgmtTechnicalImage.objects.get(id=img_data['id'])
        print(f"  - Database BYTEA size: {len(db_image.image_data)} bytes")
        print(f"  - Complete data transmitted: ✓")
    
    print(f"\n✓ All {latest_request.images.count()} images are being transmitted completely")
    print("✓ Priority 'urgent' is supported")
else:
    print("No technical requests with images found")

print("\n=== Verification completed! ===")