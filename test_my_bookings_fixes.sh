#!/bin/bash

# Quick Test Script for My Bookings Fixes
# Tests both critical issues: layout spacing and macOS button visibility

echo "=========================================="
echo "🧪 Testing My Bookings Critical Fixes"
echo "=========================================="
echo ""

echo "✅ Issue 1: Layout Spacing"
echo "   - Fixed grid row configuration (row 0 → row 1)"
echo "   - Header stays fixed, content expands properly"
echo ""

echo "✅ Issue 2: macOS Button Visibility"
echo "   - Replaced tk.Button with Canvas-based buttons"
echo "   - All tab buttons now visible on macOS"
echo ""

echo "📋 Test Checklist:"
echo "   1. Resize window - verify no huge space between header and tabs"
echo "   2. Check tab buttons are visible (Pending, Approved, Completed, Rejected)"
echo "   3. Click each tab - verify active state changes (blue background)"
echo "   4. Hover over inactive tabs - verify light gray hover effect"
echo ""

echo "🚀 Starting Frontend..."
echo ""

cd /Users/garinesaiajay/Desktop/CampusEventSystem/frontend_tkinter
python3 main.py
