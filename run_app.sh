#!/bin/bash

echo "=========================================="
echo "  Campus Event System Launcher"
echo "=========================================="
echo ""

# Check if backend is running
echo "🔍 Checking backend server..."
if curl -s http://localhost:8080/api/events > /dev/null 2>&1; then
    echo "✅ Backend server is already running"
else
    echo "⚠️  Backend server is not running!"
    echo "📝 Starting backend server..."
    cd "/Users/garinesaiajay/Desktop/CampusEventSystem/backend_java/backend"
    nohup mvn spring-boot:run > /dev/null 2>&1 &
    echo "✅ Backend started in background"
    echo ""
    echo "⏳ Waiting for backend to be ready (15 seconds)..."
    sleep 15
fi

echo ""
echo "🚀 Starting frontend application..."
cd "/Users/garinesaiajay/Desktop/CampusEventSystem/frontend_tkinter"
/opt/homebrew/bin/python3.11 main.py

echo ""
echo "👋 Application closed"
