#!/bin/bash

# Campus Event System - Stop Script
# This script stops both the backend and frontend

echo "🛑 Stopping Campus Event System..."
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_BACKEND="$SCRIPT_DIR/.backend.pid"
PID_FRONTEND="$SCRIPT_DIR/.frontend.pid"

# Function to stop a process by PID
stop_by_pid() {
    local pid_file=$1
    local name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid 2>/dev/null
            sleep 1
            if ps -p $pid > /dev/null 2>&1; then
                kill -9 $pid 2>/dev/null
            fi
            echo -e "${GREEN}✓ Stopped $name (PID: $pid)${NC}"
        else
            echo -e "${YELLOW}⚠️  $name process not found${NC}"
        fi
        rm -f "$pid_file"
    fi
}

# Stop frontend
echo "Stopping Frontend..."
stop_by_pid "$PID_FRONTEND" "Frontend"
pkill -f "python.*main.py" 2>/dev/null

# Stop backend
echo "Stopping Backend..."
stop_by_pid "$PID_BACKEND" "Backend"
pkill -f "spring-boot:run" 2>/dev/null
pkill -f "CampusEventSystem.*jar" 2>/dev/null

echo ""
echo -e "${GREEN}✅ Campus Event System stopped${NC}"
