#!/bin/bash

# JWT Authentication Test Script
# Run this after starting the backend server

echo "==================================="
echo "JWT Authentication Testing"
echo "==================================="
echo ""

# Test 1: Register a new user
echo "Test 1: Register new user..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"JWT Test User","email":"jwttest@test.com","password":"test123","role":"student"}')

echo "Response: $REGISTER_RESPONSE"
echo ""

# Extract token from response
TOKEN=$(echo $REGISTER_RESPONSE | grep -o '"token":"[^"]*' | sed 's/"token":"//')

if [ ! -z "$TOKEN" ]; then
    echo "✅ SUCCESS: User registered and token received!"
    echo "Token: ${TOKEN:0:50}..."
else
    echo "❌ FAILED: No token received"
    exit 1
fi

echo ""
echo "-----------------------------------"
echo ""

# Test 2: Try to access protected endpoint WITHOUT token
echo "Test 2: Access /api/events WITHOUT token (should fail)..."
RESPONSE_NO_TOKEN=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/events)

if [ "$RESPONSE_NO_TOKEN" = "401" ]; then
    echo "✅ SUCCESS: Got 401 Unauthorized (as expected)"
else
    echo "❌ FAILED: Expected 401, got $RESPONSE_NO_TOKEN"
fi

echo ""
echo "-----------------------------------"
echo ""

# Test 3: Access protected endpoint WITH token
echo "Test 3: Access /api/events WITH token (should succeed)..."
RESPONSE_WITH_TOKEN=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/events \
  -H "Authorization: Bearer $TOKEN")

if [ "$RESPONSE_WITH_TOKEN" = "200" ]; then
    echo "✅ SUCCESS: Got 200 OK with valid token"
else
    echo "Response code: $RESPONSE_WITH_TOKEN"
    if [ "$RESPONSE_WITH_TOKEN" = "403" ]; then
        echo "⚠️  Got 403 Forbidden - token valid but might need role permissions"
    else
        echo "❌ FAILED: Expected 200, got $RESPONSE_WITH_TOKEN"
    fi
fi

echo ""
echo "-----------------------------------"
echo ""

# Test 4: Login with existing user
echo "Test 4: Login with existing user..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jwttest@test.com","password":"test123"}')

echo "Response: $LOGIN_RESPONSE"
echo ""

NEW_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"token":"[^"]*' | sed 's/"token":"//')

if [ ! -z "$NEW_TOKEN" ]; then
    echo "✅ SUCCESS: Login successful and new token received!"
else
    echo "❌ FAILED: No token received"
fi

echo ""
echo "-----------------------------------"
echo ""

# Test 5: Refresh token
echo "Test 5: Refresh token..."
REFRESH_RESPONSE=$(curl -s -X POST http://localhost:8080/api/auth/refresh \
  -H "Authorization: Bearer $TOKEN")

echo "Response: $REFRESH_RESPONSE"
echo ""

REFRESHED_TOKEN=$(echo $REFRESH_RESPONSE | grep -o '"token":"[^"]*' | sed 's/"token":"//')

if [ ! -z "$REFRESHED_TOKEN" ]; then
    echo "✅ SUCCESS: Token refreshed!"
else
    echo "❌ FAILED: Token refresh failed"
fi

echo ""
echo "==================================="
echo "Testing Complete!"
echo "==================================="
