#!/usr/bin/env python3
"""
Script to convert all tk.Button instances with bg parameter to canvas-based buttons.
This fixes macOS rendering issues where tk.Button ignores custom bg colors.
"""

import os
import re
from pathlib import Path

# Button type mapping based on colors
BUTTON_TYPE_MAP = {
    '#27AE60': 'create_success_button',  # Green - success
    '#E74C3C': 'create_danger_button',   # Red - danger
    '#3498DB': 'create_primary_button',  # Blue - primary
    '#F39C12': 'create_warning_button',  # Orange - warning
    '#6B7280': 'create_secondary_button', # Gray - secondary
    '#F3F4F6': 'create_secondary_button', # Light gray - secondary
    '#E5E7EB': 'create_secondary_button', # Light gray - secondary
}

def get_button_creator(bg_color):
    """Determine which canvas button creator to use based on bg color"""
    for color, creator in BUTTON_TYPE_MAP.items():
        if color.lower() in bg_color.lower():
            return creator
    # Default to secondary for unknown colors
    return 'create_secondary_button'

def needs_canvas_import(content):
    """Check if file already has canvas_button imports"""
    return 'from utils.canvas_button import' not in content

def add_canvas_imports(content):
    """Add canvas_button imports to file"""
    # Find the import section (after existing imports)
    import_pattern = r'(from utils\..*?import.*?\n)'
    matches = list(re.finditer(import_pattern, content))
    
    if matches:
        # Add after last utils import
        last_match = matches[-1]
        insert_pos = last_match.end()
        import_line = 'from utils.canvas_button import create_primary_button, create_secondary_button, create_success_button, create_danger_button, create_warning_button\n'
        content = content[:insert_pos] + import_line + content[insert_pos:]
    else:
        # Add after tkinter imports
        tk_import_pattern = r'(from tkinter import.*?\n)'
        match = re.search(tk_import_pattern, content)
        if match:
            insert_pos = match.end()
            import_line = '\nfrom utils.canvas_button import create_primary_button, create_secondary_button, create_success_button, create_danger_button, create_warning_button\n'
            content = content[:insert_pos] + import_line + content[insert_pos:]
    
    return content

def convert_button_to_canvas(match_obj):
    """Convert a tk.Button instance to canvas button"""
    full_match = match_obj.group(0)
    
    # Extract bg color
    bg_match = re.search(r"bg\s*=\s*['\"]([^'\"]+)['\"]", full_match)
    if not bg_match:
        bg_match = re.search(r"bg\s*=\s*self\.colors\.get\(['\"](\w+)['\"]", full_match)
        if bg_match:
            color_key = bg_match.group(1)
            # Map color keys to actual colors
            color_map = {'success': '#27AE60', 'danger': '#E74C3C', 'secondary': '#3498DB', 'warning': '#F39C12', 'primary': '#2C3E50'}
            bg_color = color_map.get(color_key, '#6B7280')
        else:
            return full_match  # Can't determine color, skip
    else:
        bg_color = bg_match.group(1)
    
    # Extract text
    text_match = re.search(r"text\s*=\s*['\"]([^'\"]+)['\"]", full_match)
    if not text_match:
        return full_match  # No text, skip
    text = text_match.group(1)
    
    # Extract command
    command_match = re.search(r"command\s*=\s*([^,\)]+)", full_match)
    if not command_match:
        command = "None"
    else:
        command = command_match.group(1).strip()
    
    # Determine button creator function
    creator_func = get_button_creator(bg_color)
    
    # Extract variable assignment if exists
    var_match = re.match(r'(\s*)(\w+)\s*=\s*tk\.Button', full_match)
    if var_match:
        indent = var_match.group(1)
        var_name = var_match.group(2)
        # Multi-line assignment
        return f'{indent}{var_name} = {creator_func}(parent, text="{text}", command={command})'
    
    # Extract parent
    parent_match = re.search(r'tk\.Button\(([^,\)]+)', full_match)
    if not parent_match:
        return full_match
    parent = parent_match.group(1).strip()
    
    # Check if .pack() is on same line
    has_pack = '.pack(' in full_match
    
    # Get indent
    indent_match = re.match(r'(\s*)', full_match)
    indent = indent_match.group(1) if indent_match else ''
    
    if has_pack:
        # Extract pack arguments
        pack_match = re.search(r'\.pack\(([^\)]*)\)', full_match)
        pack_args = pack_match.group(1) if pack_match else ''
        return f'{indent}{creator_func}({parent}, text="{text}", command={command}).pack({pack_args})'
    else:
        return f'{indent}{creator_func}({parent}, text="{text}", command={command})'

def process_file(file_path):
    """Process a single Python file"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Add imports if needed
    if 'tk.Button' in content and 'bg=' in content:
        if needs_canvas_import(content):
            content = add_canvas_imports(content)
    
    # Find and convert all tk.Button instances with bg parameter
    # Pattern: tk.Button(...bg=...)
    pattern = r'tk\.Button\([^)]+bg\s*=\s*[^)]+\)(?:\.pack\([^)]*\))?'
    
    # Count matches
    matches = list(re.finditer(pattern, content))
    if matches:
        print(f"  Found {len(matches)} tk.Button instances with bg parameter")
        # Note: Conversion is complex, manual review recommended
        # For now, just report what was found
    
    return len(matches)

def main():
    """Main function"""
    pages_dir = Path('/Users/garinesaiajay/Desktop/CampusEventSystem/frontend_tkinter/pages')
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    total_buttons = 0
    files_with_buttons = []
    
    for py_file in pages_dir.glob('*.py'):
        count = process_file(py_file)
        if count > 0:
            total_buttons += count
            files_with_buttons.append((py_file.name, count))
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total tk.Button instances with bg: {total_buttons}")
    print(f"  Files affected: {len(files_with_buttons)}")
    print(f"\nFiles with buttons:")
    for filename, count in sorted(files_with_buttons, key=lambda x: x[1], reverse=True):
        print(f"  {filename}: {count} buttons")

if __name__ == '__main__':
    main()
