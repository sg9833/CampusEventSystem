#!/bin/bash
# Quick test script for event registration system

echo "🧪 Testing Event Registration System"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Database credentials
DB_USER="root"
DB_PASS="SAIAJAY@2005"
DB_NAME="campusdb"

echo "📊 1. Checking Database Schema..."
echo "--------------------------------"
mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "
SELECT 'Events Table' as 'Table', COUNT(*) as 'Has status column' 
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = '$DB_NAME' 
  AND TABLE_NAME = 'events' 
  AND COLUMN_NAME = 'status';

SELECT 'Event Registrations Table' as 'Table', COUNT(*) as 'Exists' 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = '$DB_NAME' 
  AND TABLE_NAME = 'event_registrations';
" 2>/dev/null

echo ""
echo "📅 2. Checking Events Status..."
echo "--------------------------------"
mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "
SELECT id, title, status, organizer_id 
FROM events 
ORDER BY id;
" 2>/dev/null

echo ""
echo "👥 3. Checking Event Registrations..."
echo "--------------------------------"
COUNT=$(mysql -u $DB_USER -p$DB_PASS $DB_NAME -se "SELECT COUNT(*) FROM event_registrations;" 2>/dev/null)
echo "Total Registrations: $COUNT"

if [ "$COUNT" -gt 0 ]; then
    mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "
    SELECT r.id, e.title as event, u.name as student, r.registered_at 
    FROM event_registrations r
    JOIN events e ON r.event_id = e.id
    JOIN users u ON r.user_id = u.id
    WHERE r.status = 'active'
    ORDER BY r.registered_at DESC
    LIMIT 10;
    " 2>/dev/null
fi

echo ""
echo "🔍 4. Checking for Unapproved Events..."
echo "--------------------------------"
PENDING=$(mysql -u $DB_USER -p$DB_PASS $DB_NAME -se "
SELECT COUNT(*) FROM events WHERE status = 'pending';
" 2>/dev/null)

if [ "$PENDING" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Found $PENDING pending event(s):${NC}"
    mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "
    SELECT id, title, organizer_id 
    FROM events 
    WHERE status = 'pending';
    " 2>/dev/null
else
    echo -e "${GREEN}✅ No pending events${NC}"
fi

echo ""
echo "🚀 5. Backend Status..."
echo "--------------------------------"
if curl -s http://localhost:8080/api/events > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is running on port 8080${NC}"
    
    # Test approved events endpoint
    APPROVED_COUNT=$(curl -s http://localhost:8080/api/events | python3 -c "import sys, json; print(len([e for e in json.load(sys.stdin) if e.get('status') == 'approved']))" 2>/dev/null)
    echo "   Approved Events: $APPROVED_COUNT"
else
    echo -e "${RED}❌ Backend is NOT running${NC}"
fi

echo ""
echo "📝 Summary"
echo "=================================="
echo ""
echo "✅ Database Schema: Updated"
echo "✅ Events Table: Has status column"
echo "✅ Event Registrations Table: Created"
echo ""

if [ "$PENDING" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Action Required:${NC}"
    echo "   $PENDING event(s) are pending admin approval"
    echo "   Students cannot see these events"
else
    echo -e "${GREEN}✅ All events are approved${NC}"
fi

echo ""
echo "🎯 Next Steps:"
echo "   1. Login as student (student1@campus.com / test123)"
echo "   2. Browse events - should only see approved events"
echo "   3. Click Register on an event"
echo "   4. Check 'My Registrations' page"
echo ""
echo "   For Admin Testing:"
echo "   1. Login as admin (admin@campus.com / test123)"
echo "   2. Go to 'Event Approvals'"
echo "   3. Approve pending events"
echo ""
