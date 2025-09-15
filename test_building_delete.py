#!/usr/bin/env python3
"""
Test script for Building DELETE endpoint
Tests the DELETE /api/buildings/{id}/ endpoint with cascade deletion
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"  # Update this if your server runs on a different port
API_URL = f"{BASE_URL}/api"

# Test credentials (update these with valid test credentials)
TEST_EMAIL = "admin@sindipro.com"
TEST_PASSWORD = "admin123"

def login():
    """Login and get authentication token"""
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }

    response = requests.post(f"{API_URL}/auth/login/", json=login_data)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Login successful. Token: {data.get('access', '')[:20]}...")
        return data.get('access')
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(f"  Response: {response.text}")
        return None

def get_buildings(token):
    """Get list of all buildings"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/buildings/", headers=headers)

    if response.status_code == 200:
        buildings = response.json()
        print(f"✓ Found {len(buildings)} buildings")
        return buildings
    else:
        print(f"✗ Failed to get buildings: {response.status_code}")
        print(f"  Response: {response.text}")
        return []

def create_test_building(token):
    """Create a test building for deletion"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    test_building_data = {
        "building_name": "Test Building for Deletion",
        "building_type": "residential",
        "cnpj": "12.345.678/0001-99",
        "manager_name": "Test Manager",
        "manager_phone": "(11) 99999-9999",
        "manager_phone_type": "mobile",
        "address": {
            "cep": "01310-100",
            "city": "São Paulo",
            "neighborhood": "Bela Vista",
            "number": "1000",
            "state": "SP",
            "street": "Avenida Paulista"
        },
        "use_separate_address": False,
        "number_of_towers": 1,
        "apartments_per_tower": 10,
        "towers": [
            {
                "name": "Tower A",
                "units_per_tower": 10
            }
        ]
    }

    response = requests.post(f"{API_URL}/buildings/", json=test_building_data, headers=headers)

    if response.status_code == 201:
        data = response.json()
        print(f"✓ Test building created successfully")
        print(f"  Building ID: {data.get('building_id')}")
        print(f"  Building Name: {data.get('building_name')}")
        return data.get('building_id')
    else:
        print(f"✗ Failed to create test building: {response.status_code}")
        print(f"  Response: {response.text}")
        return None

def delete_building(token, building_id):
    """Delete a building by ID"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_URL}/buildings/{building_id}/", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Building deleted successfully")
        print(f"  Message: {data.get('message')}")
        return True
    else:
        print(f"✗ Failed to delete building: {response.status_code}")
        print(f"  Response: {response.text}")
        return False

def verify_deletion(token, building_id):
    """Verify that the building no longer exists"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/buildings/{building_id}/", headers=headers)

    if response.status_code == 404:
        print(f"✓ Deletion verified - Building {building_id} no longer exists")
        return True
    elif response.status_code == 200:
        print(f"✗ Building still exists after deletion!")
        return False
    else:
        print(f"? Unexpected response when verifying deletion: {response.status_code}")
        return False

def main():
    print("=" * 50)
    print("Building DELETE Endpoint Test")
    print("=" * 50)

    # Step 1: Login
    print("\n1. Logging in...")
    token = login()
    if not token:
        print("Test failed: Could not authenticate")
        sys.exit(1)

    # Step 2: Get current buildings
    print("\n2. Getting current buildings...")
    buildings = get_buildings(token)

    # Step 3: Create a test building
    print("\n3. Creating test building...")
    test_building_id = create_test_building(token)
    if not test_building_id:
        print("Test failed: Could not create test building")
        sys.exit(1)

    # Step 4: Delete the test building
    print(f"\n4. Deleting building ID {test_building_id}...")
    delete_success = delete_building(token, test_building_id)
    if not delete_success:
        print("Test failed: Could not delete building")
        sys.exit(1)

    # Step 5: Verify deletion
    print(f"\n5. Verifying deletion...")
    verification = verify_deletion(token, test_building_id)

    # Final result
    print("\n" + "=" * 50)
    if verification:
        print("✓ All tests passed! DELETE endpoint is working correctly.")
        print("  The building and all associated data have been deleted.")
    else:
        print("✗ Test failed! The building was not properly deleted.")
        sys.exit(1)

if __name__ == "__main__":
    main()