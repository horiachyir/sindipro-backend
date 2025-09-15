#!/usr/bin/env python3

import json

# Test data structure matching the new POST request format
test_data = {
    "active": True,
    "buildingType": "commercial",
    "building_id": 8,
    "description": "Mandatory recharge and inspection of fire extinguishers",
    "dueMonth": "2025-09-25",
    "frequency": "monthly",
    "name": "Fire Extinguisher Recharge",
    "noticePeriod": 14,
    "requiresQuote": True,
    "responsibleEmails": "mason@gmail.com"
}

print("Test data structure for POST /api/legal/template/:")
print(json.dumps(test_data, indent=2))

print("\nField mappings:")
print("- buildingType -> building_type")
print("- dueMonth -> due_month (now DateField)")
print("- noticePeriod -> notice_period")
print("- requiresQuote -> requires_quote")
print("- responsibleEmails -> responsible_emails")
print("- building_id -> building_id (new ForeignKey field)")

print("\nModel changes made:")
print("1. Added building_id as ForeignKey to Building")
print("2. Added notice_period as IntegerField with default=14")
print("3. Changed due_month from CharField with month choices to DateField")
print("4. Updated serializer to handle camelCase field names from frontend")