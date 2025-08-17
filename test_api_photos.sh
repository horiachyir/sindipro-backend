#!/bin/bash

echo "=== Testing Technical API with 'photos' field ==="
echo ""

# Test data with photos field as sent by frontend
echo "1. Testing POST /api/field/technical/ with 'photos' field"
echo "   Sending request with JPEG image..."

curl -X POST http://localhost:8000/api/field/technical/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_email": "api.photos@example.com",
    "description": "API test with photos field",
    "location": "Server Room",
    "priority": "urgent",
    "title": "API Photos Field Test",
    "photos": [
      "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwABmX/9k="
    ]
  }' \
  -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "Note: This will return 401 (Unauthorized) without authentication,"
echo "but the server logs will show if the 'photos' field was received correctly."
echo ""
echo "=== Test completed ==="