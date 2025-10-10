#!/bin/bash

# Campus Event System - Startup Script
# This script starts both the backend (Java Spring Boot) and frontend (Python Tkinter)

echo "🚀 Starting Campus Event System..."
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend_java/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend_tkinter"

# Log files
BACKEND_LOG="$SCRIPT_DIR/backend.log"
FRONTEND_LOG="$SCRIPT_DIR/frontend.log"

# Function to check if a process is running
check_process() {
    local pid=$1
    if ps -p $pid > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to stop existing processes
stop_existing() {
    echo -e "${YELLOW}🔍 Checking for existing processes...${NC}"
    
    # Stop frontend
    pkill -f "python.*main.py" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${YELLOW}   Stopped existing frontend${NC}"
    fi
    
    # Stop backend (Spring Boot)
    pkill -f "spring-boot:run" 2>/dev/null || pkill -f "CampusEventSystem.*jar" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${YELLOW}   Stopped existing backend${NC}"
    fi
    
    sleep 2
}

# Function to start backend
start_backend() {
    echo ""
    echo -e "${BLUE}📦 Starting Backend (Spring Boot)...${NC}"
    
    if [ ! -d "$BACKEND_DIR" ]; then
        echo -e "${RED}❌ Backend directory not found: $BACKEND_DIR${NC}"
        return 1
    fi
    
    cd "$BACKEND_DIR"
    
    # Check if Maven wrapper exists
    if [ -f "./mvnw" ]; then
        echo -e "${BLUE}   Using Maven Wrapper...${NC}"
        chmod +x ./mvnw
        nohup ./mvnw spring-boot:run > "$BACKEND_LOG" 2>&1 &
        BACKEND_PID=$!
    elif command -v mvn &> /dev/null; then
        echo -e "${BLUE}   Using system Maven...${NC}"
        nohup mvn spring-boot:run > "$BACKEND_LOG" 2>&1 &
        BACKEND_PID=$!
    else
        echo -e "${RED}❌ Maven not found. Please install Maven or use Maven Wrapper.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
    echo -e "${BLUE}   Log file: $BACKEND_LOG${NC}"
    echo -e "${BLUE}   Waiting for backend to initialize...${NC}"
    
    # Wait for backend to start (check for up to 60 seconds)
    for i in {1..30}; do
        if curl -s http://localhost:8080/actuator/health > /dev/null 2>&1 || \
           curl -s http://localhost:8080 > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Backend is ready!${NC}"
            return 0
        fi
        sleep 2
        echo -n "."
    done
    
    echo ""
    echo -e "${YELLOW}⚠️  Backend is starting (may take a few more seconds)${NC}"
    return 0
}

# Function to start frontend
start_frontend() {
    echo ""
    echo -e "${BLUE}🖥️  Starting Frontend (Tkinter)...${NC}"
    
    if [ ! -d "$FRONTEND_DIR" ]; then
        echo -e "${RED}❌ Frontend directory not found: $FRONTEND_DIR${NC}"
        return 1
    fi
    
    cd "$FRONTEND_DIR"
    
    # Check if Python 3.11 is available
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        echo -e "${RED}❌ Python 3 not found. Please install Python 3.${NC}"
        return 1
    fi
    
    # Check if main.py exists
    if [ ! -f "main.py" ]; then
        echo -e "${RED}❌ main.py not found in frontend directory${NC}"
        return 1
    fi
    
    echo -e "${BLUE}   Using Python: $PYTHON_CMD${NC}"
    nohup $PYTHON_CMD main.py > "$FRONTEND_LOG" 2>&1 &
    FRONTEND_PID=$!
    
    sleep 2
    
    # Check if frontend is still running
    if check_process $FRONTEND_PID; then
        echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
        echo -e "${BLUE}   Log file: $FRONTEND_LOG${NC}"
        return 0
    else
        echo -e "${RED}❌ Frontend failed to start. Check log: $FRONTEND_LOG${NC}"
        return 1
    fi
}

# Function to display status
show_status() {
    echo ""
    echo "=================================="
    echo -e "${GREEN}✅ Campus Event System is running!${NC}"
    echo "=================================="
    echo ""
    echo "📍 Backend:  http://localhost:8080"
    echo "📍 Frontend: GUI Application"
    echo ""
    echo "📄 Logs:"
    echo "   Backend:  $BACKEND_LOG"
    echo "   Frontend: $FRONTEND_LOG"
    echo ""
    echo "🛑 To stop the application:"
    echo "   ./stop.sh"
    echo "   or manually: pkill -f 'spring-boot:run' && pkill -f 'python.*main.py'"
    echo ""
}

# Main execution
main() {
    # Stop any existing processes
    stop_existing
    
    # Start backend
    if ! start_backend; then
        echo -e "${RED}❌ Failed to start backend${NC}"
        exit 1
    fi
    
    # Start frontend
    if ! start_frontend; then
        echo -e "${RED}❌ Failed to start frontend${NC}"
        echo -e "${YELLOW}⚠️  Backend is still running. Stopping it...${NC}"
        pkill -f "spring-boot:run"
        exit 1
    fi
    
    # Show status
    show_status
    
    # Save PIDs to file for stop script
    echo "$BACKEND_PID" > "$SCRIPT_DIR/.backend.pid"
    echo "$FRONTEND_PID" > "$SCRIPT_DIR/.frontend.pid"
}

# Run main function
main
