#!/usr/bin/env python3
"""
Script to update all tk.Button instances to use ButtonStyles across all pages.
This ensures consistent, high-contrast button styling throughout the application.
"""

import os
import re

# Directory containing page files
PAGES_DIR = "/Users/garinesaiajay/Desktop/CampusEventSystem/frontend_tkinter/pages"

# Files to process
FILES_TO_UPDATE = [
    "browse_events.py",
    "browse_resources.py",
    "create_event.py",
    "manage_resources.py",
    "manage_users.py",
    "my_bookings.py",
    "my_events.py",
    "event_approvals.py",
    "booking_approvals.py",
    "analytics_page.py",
    "notifications_page.py",
    "profile_page.py",
    "book_resource.py"
]

def add_import_if_missing(content):
    """Add ButtonStyles import if not present"""
    if "from utils.button_styles import ButtonStyles" in content:
        return content
    
    # Find the last utils import
    import_pattern = r"(from utils\.\w+ import [^\n]+)\n"
    matches = list(re.finditer(import_pattern, content))
    
    if matches:
        last_match = matches[-1]
        insert_pos = last_match.end()
        return content[:insert_pos] + "from utils.button_styles import ButtonStyles\n" + content[insert_pos:]
    
    return content

def update_file(filepath):
    """Update a single file with ButtonStyles"""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return False
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Add import
        content = add_import_if_missing(content)
        
        # Common button patterns to replace
        replacements = [
            # Simple action buttons with bg color
            (
                r"tk\.Button\(([^,]+),\s*text=(['\"])([^'\"]+)\2,\s*command=([^,]+),\s*bg=[^,]+\.get\(['\"]secondary['\"],\s*['\"][^'\"]+['\"]\),\s*fg=['\"]white['\"],[^)]*\)",
                r"ButtonStyles.create_button(\1, text=\2\3\2, command=\4, variant='primary', height=1)"
            ),
            # Notification/icon buttons
            (
                r"tk\.Button\(([^,]+),\s*text=(['\"])🔔\2,\s*[^)]+command=([^)]+)\)",
                r"ButtonStyles.create_icon_button(\1, text='🔔', command=\3)"
            ),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"✅ Updated: {os.path.basename(filepath)}")
            return True
        else:
            print(f"ℹ️  No changes: {os.path.basename(filepath)}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 60)
    print("Button Styles Update Script")
    print("=" * 60)
    print()
    
    updated_count = 0
    for filename in FILES_TO_UPDATE:
        filepath = os.path.join(PAGES_DIR, filename)
        if update_file(filepath):
            updated_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ Updated {updated_count} files")
    print("=" * 60)

if __name__ == "__main__":
    main()
