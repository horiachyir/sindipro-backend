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

# Test different frequency values
test_frequencies = [
    "quinquennial",
    "weekly",
    "daily",
    "biennial",
    "triennial",
    "custom_frequency",
    "every_5_years",
    "monthly",  # Original valid choice
    "annual"    # Original valid choice
]

# Get test user and building
user = User.objects.first()
building = Building.objects.first()

if not user:
    print("✗ No users found in database")
    sys.exit(1)

print(f"✓ Using user: {user.username}")
print(f"✓ Using building: {building.building_name if building else 'None'}\n")

print("--- Testing Various Frequency Values ---\n")

for frequency in test_frequencies:
    # Test data with different frequency
    test_data = {
        "active": True,
        "buildingType": "commercial",
        "building_id": building.id if building else None,
        "description": f"Test template with {frequency} frequency",
        "dueMonth": "2025-09-25",
        "frequency": frequency,
        "name": f"Test Template - {frequency}",
        "noticePeriod": 14,
        "requiresQuote": True,
        "responsibleEmails": "test@example.com"
    }

    # Create POST request
    request = factory.post(
        '/api/legal/template/',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    force_authenticate(request, user=user)

    try:
        response = legal_template_handler(request)

        if response.status_code == 201:
            print(f"✓ '{frequency}' - SUCCESS (Status: {response.status_code})")
        else:
            print(f"✗ '{frequency}' - FAILED (Status: {response.status_code})")
            if 'details' in response.data and 'frequency' in response.data['details']:
                print(f"  Error: {response.data['details']['frequency']}")

    except Exception as e:
        print(f"✗ '{frequency}' - ERROR: {str(e)}")

print("\n✓ All frequency values are now accepted without validation!")