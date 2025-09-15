#!/bin/bash

echo "=================================================="
echo "Building DELETE Endpoint Test Using CURL"
echo "=================================================="

# Configuration
BASE_URL="http://localhost:8000/api"

# Test with a sample building ID (update this with an actual ID from your database)
BUILDING_ID=1

echo ""
echo "Testing DELETE endpoint for building ID: $BUILDING_ID"
echo ""

# Note: You'll need to provide a valid authentication token
# You can get one by logging in through your frontend or using the login endpoint
echo "To test the DELETE endpoint, you need to:"
echo "1. Get an authentication token by logging in"
echo "2. Run the following command with your token:"
echo ""
echo "curl -X DELETE \\"
echo "  ${BASE_URL}/buildings/${BUILDING_ID}/ \\"
echo "  -H 'Authorization: Bearer YOUR_AUTH_TOKEN_HERE' \\"
echo "  -H 'Content-Type: application/json'"
echo ""
echo "Expected response on success:"
echo '{"message": "Building \"BUILDING_NAME\" and all associated data have been successfully deleted"}'
echo ""
echo "The DELETE endpoint will:"
echo "- Delete the building from building_mgmt_building table"
echo "- Cascade delete all related records:"
echo "  * Addresses (building_mgmt_address)"
echo "  * Towers (building_mgmt_tower)"
echo "  * Tower unit distributions (building_mgmt_towerunitdistribution)"
echo "  * Units (building_mgmt_unit)"
echo "  * Legal documents and obligations"
echo "  * Financial records (budgets, expenses, revenues)"
echo "  * Consumption readings"
echo "  * Reports and schedules"
echo "  * Field requests and surveys"
echo "  * User access records"
echo ""