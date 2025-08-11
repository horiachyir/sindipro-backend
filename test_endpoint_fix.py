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

from django.test import Client
from django.contrib.auth import get_user_model
from legal_docs.models import LegalTemplate
import json

def test_endpoint_fix():
    print("Testing GET /api/legal/template/ endpoint fix...")
    
    User = get_user_model()
    client = Client()
    
    # Create a test user
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    
    # Login the user
    client.login(username='testuser', password='testpass123')
    
    # Create a test template
    template = LegalTemplate.objects.create(
        name='Test Template',
        description='Test description',
        building_types=['residential'],
        frequency='annual',
        active=True,
        created_by=user
    )
    
    # Test GET request
    response = client.get('/api/legal/template/')
    
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {dict(response.items())}")
    
    if response.status_code == 200:
        print("✅ SUCCESS: GET request working - no 405 error!")
        data = response.json()
        print(f"Response data: {json.dumps(data, indent=2)}")
        
        if 'templates' in data and len(data['templates']) > 0:
            print("✅ SUCCESS: Template data returned correctly")
        else:
            print("❌ WARNING: No templates in response")
    elif response.status_code == 405:
        print("❌ FAILED: Still getting 405 Method Not Allowed")
    elif response.status_code == 401:
        print("❌ AUTHENTICATION ISSUE: 401 Unauthorized")
    else:
        print(f"❌ UNEXPECTED STATUS: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
    
    # Test POST request to ensure it still works
    print("\nTesting POST request...")
    post_data = {
        'name': 'New Template',
        'description': 'New test template',
        'buildingTypes': ['commercial'],
        'frequency': 'monthly',
        'daysBeforeExpiry': 15,
        'requiresQuote': False
    }
    
    response = client.post('/api/legal/template/', 
                          data=json.dumps(post_data), 
                          content_type='application/json')
    
    print(f"POST response status code: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ SUCCESS: POST request still working")
    else:
        print(f"❌ POST ISSUE: Status {response.status_code}")
        print(f"Response content: {response.content.decode()}")
    
    # Clean up
    User.objects.all().delete()
    LegalTemplate.objects.all().delete()
    
    print("\nTest completed!")

if __name__ == '__main__':
    test_endpoint_fix()