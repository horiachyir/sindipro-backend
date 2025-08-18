#!/usr/bin/env python3
"""
Direct test of contacts_mgmt models and views without HTTP requests
"""
import os
import sys
import django
from datetime import datetime

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from contacts_mgmt.models import ContactsEvent
from contacts_mgmt.serializers import ContactsEventSerializer
from auth_system.models import User

def test_model_creation():
    """Test ContactsEvent model creation"""
    print("Testing ContactsEvent model...")
    
    # Create a test user first
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("Creating test user...")
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    # Test data
    event_data = {
        'title': 'Test Meeting',
        'event_type': 'meetingEvent',
        'date_time': datetime.now(),
        'condominium': 'Test Building',
        'people_involved': ['Person 1', 'Person 2'],
        'comments': 'Test comment'
    }
    
    # Create ContactsEvent
    event = ContactsEvent.objects.create(
        created_by=user,
        **event_data
    )
    
    print(f"✅ Created event: {event}")
    print(f"Event ID: {event.id}")
    print(f"Table name: {event._meta.db_table}")
    
    return event

def test_serializer():
    """Test ContactsEventSerializer"""
    print("\nTesting ContactsEventSerializer...")
    
    # Test with generalAssemblyEvent
    event_data_1 = {
        "title": "General Assembly Meeting",
        "event_type": "generalAssemblyEvent", 
        "date_time": "2025-08-18T06:53:00Z",
        "condominium": "Edifício Central",
        "people_involved": ["John Doe", "Jane Smith"],
        "comments": "Annual general assembly"
    }
    
    serializer1 = ContactsEventSerializer(data=event_data_1)
    
    if serializer1.is_valid():
        print("✅ generalAssemblyEvent serializer is valid")
        print("Validated data:", serializer1.validated_data)
    else:
        print("❌ generalAssemblyEvent serializer validation failed")
        print("Errors:", serializer1.errors)
    
    # Test with custom event type
    event_data_2 = {
        "title": "Custom Event",
        "event_type": "customEventType", 
        "date_time": "2025-08-18T06:53:00Z",
        "condominium": "Test Building",
        "people_involved": ["Person 1"],
        "comments": "Custom event type test"
    }
    
    serializer2 = ContactsEventSerializer(data=event_data_2)
    
    if serializer2.is_valid():
        print("✅ customEventType serializer is valid")
        print("Validated data:", serializer2.validated_data)
    else:
        print("❌ customEventType serializer validation failed")
        print("Errors:", serializer2.errors)

def test_database_table():
    """Check if table exists in database"""
    print("\nChecking database table...")
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'contacts_mgmt_event';
        """)
        result = cursor.fetchone()
        
        if result:
            print(f"✅ Table '{result[0]}' exists in database")
            
            # Check table structure
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'contacts_mgmt_event'
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            
            print("Table structure:")
            for col_name, data_type in columns:
                print(f"  - {col_name}: {data_type}")
        else:
            print("❌ Table does not exist")

if __name__ == "__main__":
    try:
        print("=== Testing Contacts Management Implementation ===\n")
        
        test_serializer()
        test_database_table()
        
        # Skip record creation in automated test
        print("\nSkipping record creation in automated test")
            
        print("\n🎉 All tests completed!")
        print("\nAPI endpoint available at: POST /api/contacts/event/")
        print("Expected data format:")
        print("""{
  "title": "Event Title",
  "event_type": "meetingEvent",
  "date_time": "2025-08-18T06:53:00Z",
  "condominium": "Building Name", 
  "people_involved": ["person1", "person2"],
  "comments": "Optional comments"
}""")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()