#!/usr/bin/env python3
"""
Test script to demonstrate correct registration data format
"""

import requests
import json

# Base URL - adjust if your server runs on a different port
BASE_URL = "http://localhost:8000"

# Example registration data - all required fields
registration_data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPassword123!",
    "confirmPassword": "TestPassword123!",
    "phone": "+1234567890",  # Optional
    "role": "readonly"  # Optional, defaults to 'readonly'
}

print("Required fields for registration:")
print("- username: unique username")
print("- email: unique email address")
print("- first_name: user's first name")
print("- last_name: user's last name")
print("- password: strong password")
print("- confirmPassword: must match password")
print("\nOptional fields:")
print("- phone: phone number")
print("- role: user role (defaults to 'readonly')")

print("\nExample registration data:")
print(json.dumps(registration_data, indent=2))

# Uncomment below to test the actual endpoint
"""
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/register/",
        json=registration_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nResponse status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 400:
        print("\nError details:")
        error_data = response.json()
        if "errors" in error_data:
            for field, error in error_data["errors"].items():
                print(f"- {field}: {error}")
                
except Exception as e:
    print(f"\nError making request: {e}")
"""