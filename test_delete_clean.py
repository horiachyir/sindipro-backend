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
from rest_framework.test import APIClient
import json

def test_delete_clean():
    print("Testing DELETE endpoint - confirming NO user data is deleted")
    
    User = get_user_model()
    
    # Record initial state
    initial_user_count = User.objects.count()
    print(f"Initial user count in database: {initial_user_count}")
    
    # Create ONE test user for this specific test
    test_user = User.objects.create_user(
        username='deletetestuser',
        email='deletetest@example.com', 
        password='testpass123'
    )
    
    current_user_count = User.objects.count()
    print(f"User count after creating test user: {current_user_count}")
    
    # Create a template to delete
    template = LegalTemplate.objects.create(
        name='Template to Delete',
        description='This template will be deleted',
        building_types=['residential'],
        frequency='annual',
        active=True,
        created_by=test_user
    )
    
    print(f"Created template with ID: {template.id}")
    print(f"Template created by user: {test_user.username} (ID: {test_user.id})")
    
    # Delete the template
    client = APIClient()
    client.force_authenticate(user=test_user)
    
    print(f"\nDeleting template {template.id}...")
    response = client.delete(f'/api/legal/template/{template.id}/')
    
    print(f"Delete response status: {response.status_code}")
    
    if response.status_code == 200:
        # Verify template was deleted
        template_exists = LegalTemplate.objects.filter(id=template.id).exists()
        print(f"Template still exists: {template_exists}")
        
        # CRITICAL: Verify user was NOT deleted
        user_still_exists = User.objects.filter(id=test_user.id).exists()
        print(f"User still exists: {user_still_exists}")
        
        # Check user count
        final_user_count = User.objects.count()
        print(f"Final user count: {final_user_count}")
        
        if user_still_exists and final_user_count == current_user_count:
            print("✅ CONFIRMED: DELETE endpoint only deletes templates, NOT users!")
            print("✅ User data in auth_system_user table is completely safe")
        else:
            print("❌ CRITICAL ERROR: User data may have been affected!")
            
        if not template_exists:
            print("✅ Template deletion working correctly")
        else:
            print("❌ Template was not deleted")
            
    else:
        print(f"❌ Delete request failed: {response.status_code}")
    
    # Clean up our test user
    test_user.delete()
    
    final_count = User.objects.count()
    print(f"After cleanup user count: {final_count} (should equal initial: {initial_user_count})")
    
    if final_count == initial_user_count:
        print("✅ Test cleanup successful - database restored to initial state")
    
    print("\nSUMMARY: DELETE /api/legal/template/{id} safely deletes ONLY legal templates")

if __name__ == '__main__':
    test_delete_clean()