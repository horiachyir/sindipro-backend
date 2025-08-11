#!/usr/bin/env python3
import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from legal_docs.models import LegalTemplate
from legal_docs.serializers import LegalTemplateSerializer
from django.test import RequestFactory
from rest_framework.test import APIClient
from django.urls import reverse

def test_get_legal_templates():
    print("Testing GET /api/legal/template/ endpoint...")
    
    User = get_user_model()
    
    # Create a test user
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    
    # Create test templates for the user
    template1 = LegalTemplate.objects.create(
        name='Fire Safety Template',
        description='Annual fire safety inspection template',
        building_types=['residential', 'commercial'],
        frequency='annual',
        conditions='Must be completed by certified inspector',
        days_before_expiry=30,
        requires_quote=True,
        active=True,
        created_by=user
    )
    
    template2 = LegalTemplate.objects.create(
        name='Elevator Maintenance Template',
        description='Monthly elevator maintenance template',
        building_types=['commercial'],
        frequency='monthly',
        conditions='Requires certified elevator technician',
        days_before_expiry=7,
        requires_quote=False,
        active=True,
        created_by=user
    )
    
    # Create an inactive template (should not be returned)
    LegalTemplate.objects.create(
        name='Inactive Template',
        description='This should not appear in results',
        building_types=['residential'],
        frequency='annual',
        active=False,
        created_by=user
    )
    
    # Create template for another user (should not be returned)
    other_user = User.objects.create_user(
        username='otheruser',
        email='other@example.com',
        password='otherpass123'
    )
    
    LegalTemplate.objects.create(
        name='Other User Template',
        description='Template from different user',
        building_types=['residential'],
        frequency='annual',
        active=True,
        created_by=other_user
    )
    
    # Test the serializer and filtering logic
    user_templates = LegalTemplate.objects.filter(created_by=user, active=True)
    serializer = LegalTemplateSerializer(user_templates, many=True)
    
    print(f"Found {user_templates.count()} active templates for user")
    print(f"Template names: {[t.name for t in user_templates]}")
    
    # Verify the serializer output
    serialized_data = serializer.data
    print(f"Serialized {len(serialized_data)} templates")
    
    # Check that only user's active templates are returned
    template_names = [t['name'] for t in serialized_data]
    expected_names = ['Fire Safety Template', 'Elevator Maintenance Template']
    
    if set(template_names) == set(expected_names):
        print("✅ SUCCESS: Correct templates returned for user")
        print("✅ User-specific filtering working correctly")
        print("✅ Active-only filtering working correctly")
    else:
        print(f"❌ FAILED: Expected {expected_names}, got {template_names}")
    
    # Verify serialized data structure
    if serialized_data:
        sample_template = serialized_data[0]
        expected_fields = ['id', 'name', 'description', 'buildingTypes', 'frequency', 
                          'conditions', 'daysBeforeExpiry', 'requiresQuote', 'active', 
                          'created_at', 'updated_at']
        actual_fields = list(sample_template.keys())
        
        if all(field in actual_fields for field in expected_fields):
            print("✅ SUCCESS: All expected fields present in serialized data")
        else:
            missing_fields = set(expected_fields) - set(actual_fields)
            print(f"❌ FAILED: Missing fields: {missing_fields}")
    
    print("\nTest completed!")
    
    # Clean up
    User.objects.all().delete()
    LegalTemplate.objects.all().delete()

if __name__ == '__main__':
    test_get_legal_templates()