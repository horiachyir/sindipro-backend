#!/bin/bash

# Example curl command to test the legal template endpoint
# Note: You need to obtain a valid JWT token first

echo "POST /api/legal/template endpoint test"
echo "======================================="
echo ""
echo "First, get an authentication token:"
echo 'curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d \'{"email": "your_email@example.com", "password": "your_password"}\''
echo ""
echo "Then use the access token to create a legal template:"
echo ""
echo "curl -X POST http://localhost:8000/api/legal/template/ \\"
echo "  -H \"Authorization: Bearer YOUR_ACCESS_TOKEN\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"active\": true,"
echo "    \"buildingTypes\": [\"residential\"],"
echo "    \"conditions\": \"Test\","
echo "    \"daysBeforeExpiry\": 30,"
echo "    \"description\": \"Hello!\","
echo "    \"frequency\": \"annual\","
echo "    \"name\": \"Test Obligation\","
echo "    \"requiresQuote\": true"
echo "  }'"