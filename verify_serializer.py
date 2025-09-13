import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from field_mgmt.models import FieldMgmtTechnical
from field_mgmt.serializers import FieldMgmtTechnicalSerializer

print("Testing serializer includes code field")
print("=" * 50)

# Create a test record
record = FieldMgmtTechnical.objects.create(
    company_email='serializer_test@example.com',
    title='Serializer Test',
    description='Testing serializer code field',
    location='Test Location',
    priority='medium'
)

print(f"Created record: ID={record.id}, Code={record.code}")

# Test serializer
serializer = FieldMgmtTechnicalSerializer(record)
serialized_data = serializer.data

print(f"\nSerialized data fields: {list(serialized_data.keys())}")
print(f"Code in serialized data: {'code' in serialized_data}")
print(f"Code value: {serialized_data.get('code')}")

print(f"\nFull serialized data:")
for key, value in serialized_data.items():
    print(f"  {key}: {value}")

# Test creating via serializer
print(f"\n" + "="*50)
print("Testing creation via serializer")

create_data = {
    'company_email': 'serializer_create@example.com',
    'title': 'Serializer Create Test',
    'description': 'Testing creation via serializer',
    'location': 'Test Location',
    'priority': 'high'
}

create_serializer = FieldMgmtTechnicalSerializer(data=create_data)
if create_serializer.is_valid():
    created_record = create_serializer.save()
    print(f"✓ Created via serializer: ID={created_record.id}, Code={created_record.code}")

    # Serialize the created record
    created_serialized = FieldMgmtTechnicalSerializer(created_record).data
    print(f"Code in created record serialized data: {created_serialized.get('code')}")

    # Clean up
    created_record.delete()
else:
    print(f"✗ Serializer validation failed: {create_serializer.errors}")

# Clean up original record
record.delete()
print(f"\n✓ Test records cleaned up")
print("Test completed!")