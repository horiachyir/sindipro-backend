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

def test_delete_endpoint():
    print("Testing DELETE /api/legal/template/{id} endpoint...")
    print("IMPORTANT: This test will NOT delete any user data from auth_system_user table!")
    
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
    
    print(f"Created test users: {User.objects.count()} users in database")
    
    # Create test templates
    template1 = LegalTemplate.objects.create(
        name='Template to Delete',
        description='This template will be deleted',
        building_types=['residential'],
        frequency='annual',
        active=True,
        created_by=user1
    )
    
    template2 = LegalTemplate.objects.create(
        name='User1 Template 2',
        description='Another template for user1',
        building_types=['commercial'],
        frequency='monthly',
        active=True,
        created_by=user1
    )
    
    template3 = LegalTemplate.objects.create(
        name='User2 Template',
        description='Template belonging to user2',
        building_types=['residential'],
        frequency='annual',
        active=True,
        created_by=user2
    )
    
    print(f"Created test templates: {LegalTemplate.objects.count()} templates in database")
    print(f"User1 has {LegalTemplate.objects.filter(created_by=user1).count()} templates")
    print(f"User2 has {LegalTemplate.objects.filter(created_by=user2).count()} templates")
    
    client = APIClient()
    
    # Test 1: Delete own template (user1 deleting template1)
    print("\n=== Test 1: Delete own template ===")
    client.force_authenticate(user=user1)
    
    response = client.delete(f'/api/legal/template/{template1.id}/')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS: Template deleted successfully")
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
        
        # Verify the template was deleted from database
        try:
            LegalTemplate.objects.get(id=template1.id)
            print("❌ FAILED: Template still exists in database")
        except LegalTemplate.DoesNotExist:
            print("✅ SUCCESS: Template properly removed from database")
            
        # Verify user data is still intact
        if User.objects.filter(id=user1.id).exists():
            print("✅ SUCCESS: User1 data preserved in auth_system_user table")
        else:
            print("❌ CRITICAL ERROR: User1 data was deleted! This should not happen!")
            
        if User.objects.filter(id=user2.id).exists():
            print("✅ SUCCESS: User2 data preserved in auth_system_user table")
        else:
            print("❌ CRITICAL ERROR: User2 data was deleted! This should not happen!")
        
        # Verify other templates are still there
        remaining_templates = LegalTemplate.objects.count()
        print(f"Remaining templates in database: {remaining_templates}")
        
        if LegalTemplate.objects.filter(id=template2.id).exists():
            print("✅ SUCCESS: Other user1 templates preserved")
        else:
            print("❌ FAILED: Other user1 templates were deleted")
            
        if LegalTemplate.objects.filter(id=template3.id).exists():
            print("✅ SUCCESS: User2 templates preserved")
        else:
            print("❌ FAILED: User2 templates were deleted")
            
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(f"Response: {response.content.decode()}")
    
    # Test 2: Try to delete another user's template
    print("\n=== Test 2: Try to delete another user's template ===")
    response = client.delete(f'/api/legal/template/{template3.id}/')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 404:
        print("✅ SUCCESS: Correctly denied access to other user's template")
        
        # Verify user2's template was NOT deleted
        if LegalTemplate.objects.filter(id=template3.id).exists():
            print("✅ SUCCESS: User2's template was NOT deleted (security working)")
        else:
            print("❌ SECURITY BREACH: User2's template was deleted!")
            
    else:
        print(f"❌ SECURITY ISSUE: Should have returned 404, got {response.status_code}")
    
    # Test 3: Try to delete non-existent template
    print("\n=== Test 3: Try to delete non-existent template ===")
    response = client.delete('/api/legal/template/99999/')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 404:
        print("✅ SUCCESS: Correctly handled non-existent template")
    else:
        print(f"❌ FAILED: Should have returned 404, got {response.status_code}")
    
    # Test 4: Unauthenticated delete request
    print("\n=== Test 4: Unauthenticated delete request ===")
    client.force_authenticate(user=None)  # Remove authentication
    
    response = client.delete(f'/api/legal/template/{template2.id}/')
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ SUCCESS: Correctly requires authentication")
        
        # Verify template was NOT deleted
        if LegalTemplate.objects.filter(id=template2.id).exists():
            print("✅ SUCCESS: Template was NOT deleted without authentication")
        else:
            print("❌ SECURITY BREACH: Template was deleted without authentication!")
    else:
        print(f"❌ SECURITY ISSUE: Should require authentication, got {response.status_code}")
    
    # Final verification: Check user count is unchanged
    print("\n=== Final Verification ===")
    final_user_count = User.objects.count()
    print(f"Final user count: {final_user_count}")
    
    if final_user_count == 2:
        print("✅ SUCCESS: All user data preserved - no users deleted")
    else:
        print(f"❌ CRITICAL ERROR: User count changed! Started with 2, now have {final_user_count}")
    
    print(f"Final template count: {LegalTemplate.objects.count()}")
    
    # Clean up test data (but keep this explicit and controlled)
    print("\nCleaning up test data...")
    LegalTemplate.objects.all().delete()
    User.objects.all().delete()
    print("Test data cleaned up successfully")
    
    print("\nAll tests completed!")

if __name__ == '__main__':
    test_delete_endpoint()