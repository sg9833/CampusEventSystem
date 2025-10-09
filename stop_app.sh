#!/bin/bash
# Script to stop all Campus Event System processes

echo "Stopping Campus Event System..."

# Stop backend (find and kill Maven/Spring Boot process)
echo "Stopping backend server..."
pkill -f "spring-boot:run"
pkill -f "CampusCoordApplication"

# Stop frontend (find and kill Python GUI process)
echo "Stopping frontend application..."
pkill -f "frontend_tkinter/main.py"

echo "All processes stopped!"
echo ""
echo "To restart:"
echo "  Backend:  cd backend_java/backend && mvn spring-boot:run"
echo "  Frontend: python3 frontend_tkinter/main.py"
