#!/bin/bash

# Campus Event System - Status Checker
# Check if backend and frontend are running

echo "🔍 Campus Event System - Status Check"
echo "======================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check Backend
echo ""
echo "Backend Status:"
if pgrep -f "spring-boot:run" > /dev/null || pgrep -f "CampusEventSystem.*jar" > /dev/null; then
    echo -e "${GREEN}✓ Backend is running${NC}"
    
    # Check if responding
    if curl -s http://localhost:8080/actuator/health > /dev/null 2>&1 || \
       curl -s http://localhost:8080 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is responding (http://localhost:8080)${NC}"
    else
        echo -e "${YELLOW}⚠️  Backend is running but not responding yet${NC}"
    fi
else
    echo -e "${RED}✗ Backend is not running${NC}"
fi

# Check Frontend
echo ""
echo "Frontend Status:"
if pgrep -f "python.*main.py" > /dev/null; then
    echo -e "${GREEN}✓ Frontend is running${NC}"
else
    echo -e "${RED}✗ Frontend is not running${NC}"
fi

# Show PIDs if running
echo ""
echo "Process Information:"
BACKEND_PID=$(pgrep -f "spring-boot:run" || pgrep -f "CampusEventSystem.*jar")
FRONTEND_PID=$(pgrep -f "python.*main.py")

if [ ! -z "$BACKEND_PID" ]; then
    echo -e "${BLUE}Backend PID:  $BACKEND_PID${NC}"
fi

if [ ! -z "$FRONTEND_PID" ]; then
    echo -e "${BLUE}Frontend PID: $FRONTEND_PID${NC}"
fi

# Show log file info
echo ""
echo "Log Files:"
if [ -f "backend.log" ]; then
    BACKEND_SIZE=$(du -h backend.log | cut -f1)
    echo -e "${BLUE}backend.log   ($BACKEND_SIZE)${NC}"
else
    echo "backend.log   (not found)"
fi

if [ -f "frontend.log" ]; then
    FRONTEND_SIZE=$(du -h frontend.log | cut -f1)
    echo -e "${BLUE}frontend.log  ($FRONTEND_SIZE)${NC}"
else
    echo "frontend.log  (not found)"
fi

echo ""
echo "======================================"

# Exit with appropriate code
if [ ! -z "$BACKEND_PID" ] && [ ! -z "$FRONTEND_PID" ]; then
    echo -e "${GREEN}✅ System is fully operational${NC}"
    exit 0
elif [ ! -z "$BACKEND_PID" ] || [ ! -z "$FRONTEND_PID" ]; then
    echo -e "${YELLOW}⚠️  System is partially running${NC}"
    exit 1
else
    echo -e "${RED}❌ System is not running${NC}"
    exit 2
fi
