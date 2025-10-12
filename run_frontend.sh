#!/bin/bash
# Campus Event System - Frontend Launcher
# Runs the Tkinter desktop application

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "CAMPUS EVENT SYSTEM - FRONTEND LAUNCHER"
echo "============================================================"
echo ""

# Check if backend is running (optional - app will prompt if not)
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✓ Backend detected on port 8080"
else
    echo "⚠ Warning: Backend not detected on port 8080"
    echo "  The app will prompt you when it starts."
fi

echo ""
echo "Starting Tkinter application..."
echo ""

# Check for virtualenv first (has dependencies pre-installed)
VENV_PYTHON="$SCRIPT_DIR/frontend_tkinter/venv/bin/python"
if [ -f "$VENV_PYTHON" ]; then
    echo "Using virtualenv: $VENV_PYTHON"
    PYTHON_CMD="$VENV_PYTHON"
else
    # Fallback to system python3
    echo "Virtualenv not found, using system Python"
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        PYTHON_CMD="python"
    fi
fi

echo ""

# Run the app
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR"
exec "$PYTHON_CMD" frontend_tkinter/main.py
