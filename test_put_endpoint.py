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
from rest_framework.test import APIClient
import json

def test_put_endpoint():
    print("Testing PUT /api/legal/template/{id} endpoint...")
    
    User = get_user_model()
    
    # Create test users
    user1 = User.objects.create_user(
        username='testuser1',
        email='test1@example.com',
        password='testpass123'
    )
    
    user2 = User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123'
    )
    
    # Create a test template for user1
    template = LegalTemplate.objects.create(
        name='Original Template',
        description='Original description',
        building_types=['residential'],
        frequency='annual',
        conditions='Original conditions',
        days_before_expiry=30,
        requires_quote=False,
        active=True,
        created_by=user1
    )
    
    # Create a template for user2 (should not be updatable by user1)
    other_template = LegalTemplate.objects.create(
        name='Other User Template',
        description='Other user description',
        building_types=['commercial'],
        frequency='monthly',
        active=True,
        created_by=user2
    )
    
    client = APIClient()
    
    # Test 1: Update template as the owner (user1)
    print("\n=== Test 1: Update template as owner ===")
    client.force_authenticate(user=user1)
    
    update_data = {
        'name': 'Updated Template Name',
        'description': 'Updated description',
        'buildingTypes': ['residential', 'commercial'],
        'frequency': 'quarterly',
        'conditions': 'Updated conditions',
        'daysBeforeExpiry': 45,
        'requiresQuote': True
    }
    
    response = client.put(f'/api/legal/template/{template.id}/', 
                         data=json.dumps(update_data), 
                         content_type='application/json')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS: Template updated successfully")
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
        
        # Verify the template was actually updated in the database
        updated_template = LegalTemplate.objects.get(id=template.id)
        print(f"Updated name: {updated_template.name}")
        print(f"Updated description: {updated_template.description}")
        print(f"Updated building_types: {updated_template.building_types}")
        print(f"Updated frequency: {updated_template.frequency}")
        print(f"Updated days_before_expiry: {updated_template.days_before_expiry}")
        print(f"Updated requires_quote: {updated_template.requires_quote}")
        
        if (updated_template.name == 'Updated Template Name' and 
            updated_template.description == 'Updated description' and
            updated_template.building_types == ['residential', 'commercial'] and
            updated_template.frequency == 'quarterly' and
            updated_template.days_before_expiry == 45 and
            updated_template.requires_quote == True):
            print("✅ SUCCESS: All fields updated correctly in database")
        else:
            print("❌ FAILED: Some fields not updated correctly")
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(f"Response: {response.content.decode()}")
    
    # Test 2: Try to update another user's template (should fail)
    print("\n=== Test 2: Try to update another user's template ===")
    response = client.put(f'/api/legal/template/{other_template.id}/', 
                         data=json.dumps(update_data), 
                         content_type='application/json')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 404:
        print("✅ SUCCESS: Correctly denied access to other user's template")
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
    else:
        print(f"❌ SECURITY ISSUE: Should have returned 404, got {response.status_code}")
        print(f"Response: {response.content.decode()}")
    
    # Test 3: Try to update non-existent template
    print("\n=== Test 3: Try to update non-existent template ===")
    response = client.put('/api/legal/template/99999/', 
                         data=json.dumps(update_data), 
                         content_type='application/json')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 404:
        print("✅ SUCCESS: Correctly handled non-existent template")
    else:
        print(f"❌ FAILED: Should have returned 404, got {response.status_code}")
    
    # Test 4: Try with invalid data
    print("\n=== Test 4: Update with invalid data ===")
    invalid_data = {
        'name': '',  # Empty name should be invalid
        'buildingTypes': [],  # Empty building types should be invalid
    }
    
    response = client.put(f'/api/legal/template/{template.id}/', 
                         data=json.dumps(invalid_data), 
                         content_type='application/json')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 400:
        print("✅ SUCCESS: Correctly handled invalid data")
        response_data = response.json()
        print(f"Validation errors: {json.dumps(response_data, indent=2)}")
    else:
        print(f"❌ FAILED: Should have returned 400, got {response.status_code}")
    
    # Test 5: Partial update (only some fields)
    print("\n=== Test 5: Partial update ===")
    partial_update = {
        'name': 'Partially Updated Name',
        'daysBeforeExpiry': 60
    }
    
    response = client.put(f'/api/legal/template/{template.id}/', 
                         data=json.dumps(partial_update), 
                         content_type='application/json')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS: Partial update worked")
        # Verify only specified fields were updated
        updated_template = LegalTemplate.objects.get(id=template.id)
        if (updated_template.name == 'Partially Updated Name' and
            updated_template.days_before_expiry == 60 and
            updated_template.description == 'Updated description'):  # Should remain from previous update
            print("✅ SUCCESS: Partial update preserved other fields")
        else:
            print("❌ FAILED: Partial update didn't work correctly")
    else:
        print(f"❌ FAILED: Partial update failed with status {response.status_code}")
    
    print("\n=== Test 6: Unauthenticated request ===")
    client.force_authenticate(user=None)  # Remove authentication
    
    response = client.put(f'/api/legal/template/{template.id}/', 
                         data=json.dumps(update_data), 
                         content_type='application/json')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ SUCCESS: Correctly requires authentication")
    else:
        print(f"❌ SECURITY ISSUE: Should require authentication, got {response.status_code}")
    
    # Clean up
    User.objects.all().delete()
    LegalTemplate.objects.all().delete()
    
    print("\nAll tests completed!")

if __name__ == '__main__':
    test_put_endpoint()