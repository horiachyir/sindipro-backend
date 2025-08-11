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
from equipment_mgmt.models import Equipment
from equipment_mgmt.serializers import EquipmentSerializer
from rest_framework.test import APIClient
import json

def test_equipment_post():
    print("Testing POST /api/equipment/ endpoint with new structure...")
    
    User = get_user_model()
    
    # Create test user (or get existing)
    user, created = User.objects.get_or_create(
        username='equipmentuser',
        defaults={
            'email': 'equipment@example.com',
            'password': 'testpass123'
        }
    )
    
    client = APIClient()
    client.force_authenticate(user=user)
    
    # Test data matching the required structure
    equipment_data = {
        "condominium": "Residencial Park",
        "contractorName": "SINDIPRO",
        "contractorPhone": "23343234344",
        "location": "Machine Room",
        "maintenanceFrequency": "monthly",
        "name": "Elevator",
        "purchaseDate": "2025-08-04",
        "status": "operational",
        "type": "Social"
    }
    
    print("Test data:")
    print(json.dumps(equipment_data, indent=2))
    
    # Test 1: Create equipment with valid data
    print("\n=== Test 1: Create equipment with valid data ===")
    
    response = client.post('/api/equipment/', 
                          data=json.dumps(equipment_data), 
                          content_type='application/json')
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ SUCCESS: Equipment created successfully")
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
        
        # Verify the equipment was saved to database
        equipment_id = response_data.get('equipment_id')
        if equipment_id:
            try:
                equipment = Equipment.objects.get(id=equipment_id)
                print(f"✅ Equipment found in database:")
                print(f"   ID: {equipment.id}")
                print(f"   Name: {equipment.name}")
                print(f"   Condominium: {equipment.condominium}")
                print(f"   Type: {equipment.type}")
                print(f"   Location: {equipment.location}")
                print(f"   Purchase Date: {equipment.purchase_date}")
                print(f"   Status: {equipment.status}")
                print(f"   Maintenance Frequency: {equipment.maintenance_frequency}")
                print(f"   Contractor Name: {equipment.contractor_name}")
                print(f"   Contractor Phone: {equipment.contractor_phone}")
                print(f"   Created By: {equipment.created_by.username}")
                
                # Verify all fields match
                if (equipment.condominium == "Residencial Park" and
                    equipment.name == "Elevator" and
                    equipment.type == "Social" and
                    equipment.location == "Machine Room" and
                    str(equipment.purchase_date) == "2025-08-04" and
                    equipment.status == "operational" and
                    equipment.maintenance_frequency == "monthly" and
                    equipment.contractor_name == "SINDIPRO" and
                    equipment.contractor_phone == "23343234344"):
                    print("✅ SUCCESS: All fields saved correctly")
                else:
                    print("❌ FAILED: Some fields don't match")
                    
            except Equipment.DoesNotExist:
                print("❌ FAILED: Equipment not found in database")
        else:
            print("❌ FAILED: No equipment_id in response")
            
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(f"Response: {response.content.decode()}")
    
    # Test 2: Test with missing required field
    print("\n=== Test 2: Test with missing required field ===")
    
    invalid_data = equipment_data.copy()
    del invalid_data['condominium']  # Remove required field
    
    response = client.post('/api/equipment/', 
                          data=json.dumps(invalid_data), 
                          content_type='application/json')
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 400:
        print("✅ SUCCESS: Correctly rejected missing required field")
        response_data = response.json()
        print(f"Validation error: {json.dumps(response_data, indent=2)}")
    else:
        print(f"❌ FAILED: Should have returned 400, got {response.status_code}")
    
    # Test 3: Test with invalid date format
    print("\n=== Test 3: Test with invalid date format ===")
    
    invalid_date_data = equipment_data.copy()
    invalid_date_data['purchaseDate'] = "invalid-date"
    
    response = client.post('/api/equipment/', 
                          data=json.dumps(invalid_date_data), 
                          content_type='application/json')
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 400:
        print("✅ SUCCESS: Correctly rejected invalid date format")
        response_data = response.json()
        print(f"Validation error: {json.dumps(response_data, indent=2)}")
    else:
        print(f"❌ FAILED: Should have returned 400, got {response.status_code}")
    
    # Test 4: Test unauthenticated request
    print("\n=== Test 4: Test unauthenticated request ===")
    
    client.force_authenticate(user=None)  # Remove authentication
    
    response = client.post('/api/equipment/', 
                          data=json.dumps(equipment_data), 
                          content_type='application/json')
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ SUCCESS: Correctly requires authentication")
    else:
        print(f"❌ SECURITY ISSUE: Should require authentication, got {response.status_code}")
    
    # Test 5: Test serializer field mapping
    print("\n=== Test 5: Test serializer field mapping ===")
    
    # Re-authenticate
    client.force_authenticate(user=user)
    
    # Test that camelCase fields are properly mapped
    different_case_data = {
        "condominium": "Test Building",
        "contractorName": "Test Contractor",  # camelCase
        "contractorPhone": "1234567890",      # camelCase  
        "location": "Test Location",
        "maintenanceFrequency": "quarterly",  # camelCase
        "name": "Test Equipment",
        "purchaseDate": "2025-01-01",        # camelCase
        "status": "maintenance",
        "type": "Test Type"
    }
    
    response = client.post('/api/equipment/', 
                          data=json.dumps(different_case_data), 
                          content_type='application/json')
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ SUCCESS: camelCase field mapping works correctly")
        
        # Verify the mapping worked
        equipment_id = response.json().get('equipment_id')
        equipment = Equipment.objects.get(id=equipment_id)
        
        if (equipment.contractor_name == "Test Contractor" and
            equipment.contractor_phone == "1234567890" and
            equipment.maintenance_frequency == "quarterly" and
            str(equipment.purchase_date) == "2025-01-01"):
            print("✅ SUCCESS: Field mapping from camelCase to snake_case working")
        else:
            print("❌ FAILED: Field mapping not working correctly")
    else:
        print(f"❌ FAILED: Field mapping test failed with status {response.status_code}")
    
    # Clean up
    Equipment.objects.all().delete()
    User.objects.all().delete()
    
    print(f"\nFinal equipment count: {Equipment.objects.count()}")
    print("All tests completed!")

if __name__ == '__main__':
    test_equipment_post()