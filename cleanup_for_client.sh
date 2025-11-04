#!/bin/bash

###############################################################################
# Campus Event System - Client Delivery Cleanup Script
# This script prepares the repository for client delivery
# Run this BEFORE packaging or pushing to client repository
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo "========================================="
echo "  Campus Event System"
echo "  Client Delivery Cleanup"
echo "========================================="
echo ""

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Confirmation
echo -e "${YELLOW}WARNING: This will remove machine-specific files and sensitive data.${NC}"
echo ""
echo "This script will:"
echo "  • Remove build artifacts (target/, __pycache__, etc.)"
echo "  • Remove log files"
echo "  • Remove test scripts"
echo "  • Remove sensitive configuration files"
echo "  • Remove Python bytecode"
echo "  • Clean up development files"
echo ""
read -p "Do you want to continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Cleanup cancelled."
    exit 0
fi

echo ""
print_info "Starting cleanup process..."
echo ""

# Counter for removed items
REMOVED_COUNT=0

# Function to remove file or directory
remove_item() {
    local item=$1
    if [ -e "$item" ]; then
        rm -rf "$item"
        print_success "Removed: $item"
        ((REMOVED_COUNT++))
    fi
}

# 1. Remove build artifacts
print_info "Removing build artifacts..."
remove_item "backend_java/backend/target"
remove_item "backend_java/backend/.github"
remove_item "frontend_tkinter/__pycache__"
remove_item "frontend_tkinter/.pytest_cache"
remove_item "frontend_tkinter/htmlcov"
remove_item "frontend_tkinter/venv"
remove_item "frontend_tkinter/cache"

# Find and remove all __pycache__ directories
find frontend_tkinter -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
print_success "Removed Python cache directories"

# 2. Remove log files
print_info "Removing log files..."
remove_item "backend.log"
remove_item "frontend.log"
remove_item "backend_error.log"
remove_item "backend_java/backend/backend.log"
remove_item "backend_java/backend/backend_error.log"
remove_item ".backend.pid"
remove_item ".frontend.pid"

# Remove all .log files
find . -name "*.log" -type f -delete 2>/dev/null || true
print_success "Removed log files"

# 3. Remove test and debug scripts
print_info "Removing test/debug scripts..."
remove_item "test_api_token_fix.py"
remove_item "test_button_colors.py"
remove_item "test_create_event.py"
remove_item "test_jwt.sh"
remove_item "test_my_bookings_fixes.sh"
remove_item "test_my_events_fix.py"
remove_item "test_register_labels.py"
remove_item "test_registration_system.sh"
remove_item "test_session_diagnostic.py"
remove_item "update_button_styles.py"
remove_item "frontend_tkinter/test_widget.py"
remove_item "frontend_tkinter/test_data_setup.py"
remove_item "frontend_tkinter/test_email_notifications.py"
remove_item "frontend_tkinter/demo_config.py"
remove_item "frontend_tkinter/demo_login.py"
remove_item "frontend_tkinter/SAFE_MIGRATION_EXAMPLE.py"

# 4. Remove sensitive configuration files
print_info "Removing sensitive configuration files..."
remove_item "CREDENTIALS_QUICK_REF.txt"

# Backup and remove application.properties if it exists
if [ -f "backend_java/backend/src/main/resources/application.properties" ]; then
    print_warning "Found application.properties with potentially sensitive data"
    
    # Create template if it doesn't exist
    if [ ! -f "backend_java/backend/src/main/resources/application.properties.template" ]; then
        print_info "Creating application.properties.template..."
        cat > "backend_java/backend/src/main/resources/application.properties.template" << 'EOF'
# MySQL Database Configuration
# Replace these values with your own
spring.datasource.url=jdbc:mysql://localhost:3306/campusdb
spring.datasource.username=root
spring.datasource.password=YOUR_MYSQL_ROOT_PASSWORD_HERE
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA / Hibernate
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect

# Server Configuration
server.port=8080

# JWT Configuration
# Generate a secure random key for production
jwt.secret=your-256-bit-secret-key-change-this-in-production-minimum-32-characters-for-security
jwt.expiration=86400000

# Logging
logging.level.root=INFO
logging.level.com.campuscoord=DEBUG
logging.level.org.springframework.web=INFO
logging.level.org.springframework.security=DEBUG
EOF
        print_success "Created application.properties.template"
    fi
    
    remove_item "backend_java/backend/src/main/resources/application.properties"
fi

# Create .env.template if it doesn't exist
if [ ! -f "frontend_tkinter/.env.template" ] && [ -f "frontend_tkinter/.env.example" ]; then
    cp "frontend_tkinter/.env.example" "frontend_tkinter/.env.template"
    print_success "Created .env.template from .env.example"
fi

# Remove environment files with potential secrets
remove_item "frontend_tkinter/.env.development"
remove_item "frontend_tkinter/.env.production"

# 5. Remove Python bytecode and cache
print_info "Removing Python bytecode..."
find . -name "*.pyc" -type f -delete 2>/dev/null || true
find . -name "*.pyo" -type f -delete 2>/dev/null || true
find . -name "*.pyd" -type f -delete 2>/dev/null || true
print_success "Removed Python bytecode files"

# 6. Remove OS-specific files
print_info "Removing OS-specific files..."
find . -name ".DS_Store" -type f -delete 2>/dev/null || true
find . -name "Thumbs.db" -type f -delete 2>/dev/null || true
find . -name "desktop.ini" -type f -delete 2>/dev/null || true
print_success "Removed OS-specific files"

# 7. Remove IDE files (optional)
print_info "Checking for IDE files..."
if [ -d ".idea" ] || [ -d ".vscode" ] || ls *.iml 1> /dev/null 2>&1; then
    read -p "Remove IDE files (.idea, .vscode, *.iml)? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        remove_item ".idea"
        remove_item ".vscode"
        find . -name "*.iml" -type f -delete 2>/dev/null || true
        print_success "Removed IDE files"
    else
        print_info "Keeping IDE files"
    fi
fi

# 8. Git history (optional)
print_info "Checking Git repository..."
if [ -d ".git" ]; then
    echo ""
    print_warning "Found .git directory"
    echo "  Options:"
    echo "    1) Keep .git (client gets full history)"
    echo "    2) Remove .git (clean start for client)"
    echo "    3) Skip (decide later)"
    read -p "  Choose (1/2/3): " -n 1 -r
    echo ""
    
    case $REPLY in
        1)
            print_info "Keeping .git directory"
            ;;
        2)
            remove_item ".git"
            print_success "Removed .git directory"
            ;;
        *)
            print_info "Skipping .git decision"
            ;;
    esac
fi

# 9. Summary
echo ""
echo "========================================="
echo "  Cleanup Summary"
echo "========================================="
echo ""
print_success "Removed $REMOVED_COUNT items"
echo ""

# 10. Create README for client
print_info "Checking documentation..."

if [ ! -f "CLIENT_SETUP_GUIDE.md" ]; then
    print_warning "CLIENT_SETUP_GUIDE.md not found!"
    print_warning "Make sure to include setup documentation for the client."
fi

# 11. Final checks and recommendations
echo ""
echo "========================================="
echo "  Important Next Steps"
echo "========================================="
echo ""

print_warning "Before delivering to client:"
echo ""
echo "  1. ✓ Run this script (you just did!)"
echo "  2. ☐ Verify CLIENT_SETUP_GUIDE.md exists"
echo "  3. ☐ Verify application.properties.template exists"
echo "  4. ☐ Test the setup on a clean machine if possible"
echo "  5. ☐ Update README.md with any final notes"
echo "  6. ☐ Check for any remaining personal information:"
echo "       - Hardcoded passwords"
echo "       - Personal email addresses"
echo "       - Absolute paths (e.g., /Users/yourname/...)"
echo "       - API keys or secrets"
echo "  7. ☐ Package the repository (ZIP or Git)"
echo "  8. ☐ Include LICENSE file if applicable"
echo ""

# Check for common issues
print_info "Checking for potential issues..."
echo ""

# Check for hardcoded paths
if grep -r "/Users/garinesaiajay" . --exclude-dir=.git --exclude="*.md" 2>/dev/null; then
    print_warning "Found hardcoded paths that may need to be fixed"
fi

# Check for password patterns
if grep -ri "password.*=.*[^Y]" backend_java frontend_tkinter --exclude-dir=.git --exclude="*.md" 2>/dev/null | grep -v "YOUR_" | grep -v "password_hash" | grep -v "password_field" | head -5; then
    print_warning "Found potential hardcoded passwords"
fi

echo ""
print_success "Cleanup completed successfully!"
echo ""
print_info "You can now:"
echo "  • Create a ZIP file: zip -r CampusEventSystem.zip ."
echo "  • Or push to a new Git repository for client access"
echo ""
print_info "Package command:"
echo "  zip -r CampusEventSystem-v1.0.zip . -x '*.git*' '*node_modules*' '*.DS_Store'"
echo ""

# Optional: Create a delivery checklist file
cat > "DELIVERY_CHECKLIST.txt" << 'EOF'
Campus Event System - Pre-Delivery Checklist
=============================================

Before delivering to client, verify:

Infrastructure:
[ ] Cleanup script has been run (cleanup_for_client.sh)
[ ] No build artifacts remain (target/, __pycache__, etc.)
[ ] No log files remain
[ ] No test scripts remain

Sensitive Data:
[ ] No personal passwords in any files
[ ] No hardcoded absolute paths (/Users/yourname/...)
[ ] No API keys or secrets
[ ] No personal email addresses
[ ] application.properties has been removed (template exists)

Documentation:
[ ] CLIENT_SETUP_GUIDE.md exists and is complete
[ ] WINDOWS_SETUP_GUIDE.md exists
[ ] MACOS_SETUP_GUIDE.md exists
[ ] TROUBLESHOOTING_GUIDE.md exists
[ ] DOCUMENTATION_INDEX.md exists
[ ] README.md is up to date
[ ] LICENSE file included (if applicable)

Configuration:
[ ] application.properties.template exists
[ ] .env.template exists (if applicable)
[ ] All templates have placeholder values (YOUR_PASSWORD_HERE, etc.)

Testing:
[ ] Tested setup on clean Windows machine (if possible)
[ ] Tested setup on clean macOS machine (if possible)
[ ] All startup scripts work (run.sh, stop.sh)
[ ] Database schema loads correctly
[ ] Sample data loads correctly

Packaging:
[ ] Decided on delivery method (ZIP, Git repository, etc.)
[ ] Created package/repository
[ ] Verified package contents
[ ] Prepared delivery email with instructions

Final Steps:
[ ] Delete this checklist before delivery
[ ] Send package to client
[ ] Include link to CLIENT_SETUP_GUIDE.md in email

Notes:
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

EOF

print_success "Created DELIVERY_CHECKLIST.txt for your reference"
echo ""
print_info "Review DELIVERY_CHECKLIST.txt before final delivery"
echo ""

print_success "All done! 🎉"
echo ""
