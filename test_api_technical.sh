#!/bin/bash

# Test Technical API endpoint with BYTEA storage

echo "=== Testing Technical API Endpoint ==="
echo ""

# First, get a token (you'll need to update these credentials)
echo "1. Getting authentication token..."
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@gmail.com",
    "password": "testpassword"
  }')

# For testing without auth, we'll skip token extraction
echo "   Note: Authentication would be required in production"
echo ""

# Test POST request
echo "2. Testing POST /api/field/technical/"
echo "   Sending technical request with base64 image..."

# Using a small red pixel PNG image
RESPONSE=$(curl -s -X POST http://localhost:8000/api/field/technical/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_email": "sergeiromanoff.job@gmail.com",
    "description": "Testing BYTEA storage via API",
    "location": "Server Room B",
    "priority": "high",
    "title": "API Test - BYTEA Storage",
    "image_data": [
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    ]
  }')

echo "   Response: $RESPONSE"
echo ""

# Test GET request
echo "3. Testing GET /api/field/technical/"
GET_RESPONSE=$(curl -s -X GET http://localhost:8000/api/field/technical/)

# Pretty print the response using Python
echo "   Response (formatted):"
echo "$GET_RESPONSE" | python3 -m json.tool 2>/dev/null | head -20

echo ""
echo "=== Test completed ==="