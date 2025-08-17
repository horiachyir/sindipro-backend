#!/usr/bin/env python3
import os
import sys
import django

# Add project to path
sys.path.insert(0, '/home/administrator/Documents/SINDIPRO-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from field_mgmt.models import FieldMgmtTechnical, FieldMgmtTechnicalImage
from django.core.files.base import ContentFile
import base64

# Test data
test_data = {
    "company_email": "sergeiromanoff.job@gmail.com",
    "description": "Hello",
    "location": "test2",
    "priority": "medium",
    "title": "Test 1"
}

# Create a technical request
print("Creating technical request...")
technical_request = FieldMgmtTechnical.objects.create(**test_data)
print(f"Created: {technical_request}")

# Add an image
image_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
if image_data.startswith('data:image'):
    format, imgstr = image_data.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name=f'technical_{technical_request.id}_0.{ext}')
    image = FieldMgmtTechnicalImage.objects.create(
        technical_request=technical_request,
        image=data
    )
    print(f"Created image: {image}")

# Query the data
print("\nQuerying all technical requests:")
all_requests = FieldMgmtTechnical.objects.all()
for req in all_requests:
    print(f"- {req.title} ({req.company_email}) - {req.images.count()} images")

print("\nTest completed successfully!")