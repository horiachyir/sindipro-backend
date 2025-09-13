import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindipro_backend.settings')
django.setup()

from field_mgmt.models import FieldMgmtTechnical

# Test the unique code generation
print("Testing unique code generation in FieldMgmtTechnical model")
print("=" * 60)

# Create a few test records to verify unique code generation
print("Creating test records...")

records_created = []
for i in range(5):
    record = FieldMgmtTechnical.objects.create(
        company_email=f"test{i}@example.com",
        title=f"Test Request {i+1}",
        description=f"Test description for request {i+1}",
        location=f"Test Location {i+1}",
        priority="medium"
    )
    records_created.append(record)
    print(f"Record {i+1}: ID={record.id}, Code={record.code}")

# Check if all codes are unique
codes = [r.code for r in records_created]
unique_codes = set(codes)

print(f"\nGenerated codes: {codes}")
print(f"Unique codes: {len(unique_codes)}")
print(f"Total records: {len(records_created)}")

if len(unique_codes) == len(records_created):
    print("✓ All codes are unique!")
else:
    print("✗ Duplicate codes found!")

# Test that codes are 8 characters and alphanumeric
print(f"\nCode format validation:")
for record in records_created:
    code = record.code
    is_8_chars = len(code) == 8
    is_alnum = code.isalnum()
    is_upper = code.isupper()
    print(f"  {code}: Length=8: {is_8_chars}, Alphanumeric: {is_alnum}, Uppercase: {is_upper}")

print("\nTest completed!")

# Clean up the test records
print("\nCleaning up test records...")
for record in records_created:
    record.delete()
print("✓ Test records deleted")