#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate
from legal_docs.views import legal_template_handler
from building_mgmt.models import Building
import json

User = get_user_model()

# Create a test request
factory = RequestFactory()

# Test data matching the POST request format
test_data = {
    "active": True,
    "buildingType": "commercial",
    "building_id": None,  # Will be set after we check for a building
    "description": "Mandatory recharge and inspection of fire extinguishers",
    "dueMonth": "2025-09-25",
    "frequency": "monthly",
    "name": "Fire Extinguisher Recharge",
    "noticePeriod": 14,
    "requiresQuote": True,
    "responsibleEmails": "mason@gmail.com"
}

# Check if there's a building with ID 8 or get the first available
try:
    building = Building.objects.get(id=8)
    test_data["building_id"] = 8
    print(f"✓ Found building with ID 8: {building.building_name}")
except Building.DoesNotExist:
    building = Building.objects.first()
    if building:
        test_data["building_id"] = building.id
        print(f"✓ Using first available building (ID {building.id}): {building.building_name}")
    else:
        print("✗ No buildings found in database. Building field will be null.")

# Get or create a test user
user = User.objects.first()
if user:
    print(f"✓ Using user: {user.username}")
else:
    print("✗ No users found in database")
    sys.exit(1)

# Create POST request
request = factory.post(
    '/api/legal/template/',
    data=json.dumps(test_data),
    content_type='application/json'
)
# Force authenticate the request
force_authenticate(request, user=user)

print("\n--- Testing POST /api/legal/template/ ---")
print(f"Request data: {json.dumps(test_data, indent=2)}")

try:
    response = legal_template_handler(request)
    print(f"\nResponse status: {response.status_code}")
    print(f"Response data: {json.dumps(response.data, indent=2)}")

    if response.status_code == 201:
        print("\n✓ SUCCESS: Template created successfully!")
    else:
        print("\n✗ FAILED: Template creation failed")

except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()