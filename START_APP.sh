#!/bin/bash
# Campus Event System - Quick Start Guide
# This script helps you run the application locally

echo "============================================================"
echo "CAMPUS EVENT SYSTEM - QUICK START"
echo "============================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cat << 'EOF'
The application requires Python 3.9+ with Tkinter support.

OPTION 1: Run with your system Python (RECOMMENDED)
----------------------------------------------------
If you have Python with the required packages installed globally:

    cd /Users/garinesaiajay/Desktop/CampusEventSystem
    PYTHONPATH=$(pwd) python3 frontend_tkinter/main.py

OPTION 2: Create a fresh virtualenv
----------------------------------------------------
If you encounter library compatibility issues:

    cd /Users/garinesaiajay/Desktop/CampusEventSystem
    python3 -m venv fresh_venv
    source fresh_venv/bin/activate
    pip install -r frontend_tkinter/requirements.txt
    PYTHONPATH=$(pwd) python3 frontend_tkinter/main.py

OPTION 3: Run the lightweight demos (no backend needed)
--------------------------------------------------------
To see the new modern UI widgets without the full app:

    # Modern button test:
    cd /Users/garinesaiajay/Desktop/CampusEventSystem
    PYTHONPATH=$(pwd) python3 frontend_tkinter/test_widget.py

    # Modern login demo:
    cd /Users/garinesaiajay/Desktop/CampusEventSystem
    PYTHONPATH=$(pwd) python3 frontend_tkinter/demo_login.py

TROUBLESHOOTING
---------------
If you see "macOS 26 required" error:
- This indicates a native library mismatch in the Python installation
- Try using a different Python installation (e.g., from Homebrew)
- Install Python from Homebrew: brew install python@3.11

If you see "ModuleNotFoundError":
- Install dependencies: pip3 install -r frontend_tkinter/requirements.txt
- Or use --break-system-packages flag if needed (not recommended)

BACKEND SETUP (Optional)
-------------------------
The frontend can run standalone, but to see full functionality:

1. Start the Java backend:
   cd backend_java/backend
   mvn spring-boot:run

2. The backend will run on http://localhost:8080

NEXT STEPS
----------
After the app starts:
- Login page will appear
- From menu: File → Settings → check "Use modern login page"
- Click Save to see the new modern UI design

For more details, see:
- frontend_tkinter/README.md (coming soon)
- FINAL_SCALING_PLAN.md

EOF

echo ""
echo "Press Enter to attempt auto-run, or Ctrl+C to exit and run manually..."
read -r

echo ""
echo "Attempting to run with system Python..."
echo ""

cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR"

# Try to find a working Python
for PYTHON_CMD in python3.11 python3.10 python3.9 python3 python; do
    if command -v "$PYTHON_CMD" &> /dev/null; then
        echo "Trying: $PYTHON_CMD"
        if "$PYTHON_CMD" -c "import tkinter, requests" 2>/dev/null; then
            echo "✓ Found working Python: $PYTHON_CMD"
            exec "$PYTHON_CMD" frontend_tkinter/main.py
        else
            echo "  Missing dependencies, trying next..."
        fi
    fi
done

echo ""
echo "❌ Could not find a Python installation with required packages."
echo "Please follow OPTION 1 or OPTION 2 above to install dependencies."
