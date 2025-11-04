@echo off
REM ###############################################################################
REM Campus Event System - Client Delivery Cleanup Script (Windows)
REM This script prepares the repository for client delivery
REM Run this BEFORE packaging or pushing to client repository
REM ###############################################################################

echo.
echo =========================================
echo   Campus Event System
echo   Client Delivery Cleanup
echo =========================================
echo.

REM Confirmation
echo WARNING: This will remove machine-specific files and sensitive data.
echo.
echo This script will:
echo   - Remove build artifacts (target/, __pycache__, etc.)
echo   - Remove log files
echo   - Remove test scripts
echo   - Remove sensitive configuration files
echo   - Remove Python bytecode
echo   - Clean up development files
echo.
set /p CONFIRM="Do you want to continue? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo Starting cleanup process...
echo.

REM 1. Remove build artifacts
echo Removing build artifacts...
if exist "backend_java\backend\target" (
    rmdir /s /q "backend_java\backend\target"
    echo [OK] Removed: backend_java\backend\target
)
if exist "backend_java\backend\.github" (
    rmdir /s /q "backend_java\backend\.github"
    echo [OK] Removed: backend_java\backend\.github
)
if exist "frontend_tkinter\__pycache__" (
    rmdir /s /q "frontend_tkinter\__pycache__"
    echo [OK] Removed: frontend_tkinter\__pycache__
)
if exist "frontend_tkinter\.pytest_cache" (
    rmdir /s /q "frontend_tkinter\.pytest_cache"
    echo [OK] Removed: frontend_tkinter\.pytest_cache
)
if exist "frontend_tkinter\htmlcov" (
    rmdir /s /q "frontend_tkinter\htmlcov"
    echo [OK] Removed: frontend_tkinter\htmlcov
)
if exist "frontend_tkinter\venv" (
    rmdir /s /q "frontend_tkinter\venv"
    echo [OK] Removed: frontend_tkinter\venv
)
if exist "frontend_tkinter\cache" (
    rmdir /s /q "frontend_tkinter\cache"
    echo [OK] Removed: frontend_tkinter\cache
)

REM Remove all __pycache__ directories
for /d /r "frontend_tkinter" %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
echo [OK] Removed Python cache directories

REM 2. Remove log files
echo.
echo Removing log files...
if exist "backend.log" del /q "backend.log"
if exist "frontend.log" del /q "frontend.log"
if exist "backend_error.log" del /q "backend_error.log"
if exist "backend_java\backend\backend.log" del /q "backend_java\backend\backend.log"
if exist "backend_java\backend\backend_error.log" del /q "backend_java\backend\backend_error.log"
if exist ".backend.pid" del /q ".backend.pid"
if exist ".frontend.pid" del /q ".frontend.pid"

REM Remove all .log files
for /r %%f in (*.log) do @del /q "%%f" 2>nul
echo [OK] Removed log files

REM 3. Remove test and debug scripts
echo.
echo Removing test/debug scripts...
if exist "test_api_token_fix.py" del /q "test_api_token_fix.py"
if exist "test_button_colors.py" del /q "test_button_colors.py"
if exist "test_create_event.py" del /q "test_create_event.py"
if exist "test_jwt.sh" del /q "test_jwt.sh"
if exist "test_my_bookings_fixes.sh" del /q "test_my_bookings_fixes.sh"
if exist "test_my_events_fix.py" del /q "test_my_events_fix.py"
if exist "test_register_labels.py" del /q "test_register_labels.py"
if exist "test_registration_system.sh" del /q "test_registration_system.sh"
if exist "test_session_diagnostic.py" del /q "test_session_diagnostic.py"
if exist "update_button_styles.py" del /q "update_button_styles.py"
if exist "frontend_tkinter\test_widget.py" del /q "frontend_tkinter\test_widget.py"
if exist "frontend_tkinter\test_data_setup.py" del /q "frontend_tkinter\test_data_setup.py"
if exist "frontend_tkinter\test_email_notifications.py" del /q "frontend_tkinter\test_email_notifications.py"
if exist "frontend_tkinter\demo_config.py" del /q "frontend_tkinter\demo_config.py"
if exist "frontend_tkinter\demo_login.py" del /q "frontend_tkinter\demo_login.py"
if exist "frontend_tkinter\SAFE_MIGRATION_EXAMPLE.py" del /q "frontend_tkinter\SAFE_MIGRATION_EXAMPLE.py"
echo [OK] Removed test scripts

REM 4. Remove sensitive configuration files
echo.
echo Removing sensitive configuration files...
if exist "CREDENTIALS_QUICK_REF.txt" del /q "CREDENTIALS_QUICK_REF.txt"

REM Create template if needed
if exist "backend_java\backend\src\main\resources\application.properties" (
    echo [WARN] Found application.properties with potentially sensitive data
    
    if not exist "backend_java\backend\src\main\resources\application.properties.template" (
        echo Creating application.properties.template...
        (
            echo # MySQL Database Configuration
            echo # Replace these values with your own
            echo spring.datasource.url=jdbc:mysql://localhost:3306/campusdb
            echo spring.datasource.username=root
            echo spring.datasource.password=YOUR_MYSQL_ROOT_PASSWORD_HERE
            echo spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
            echo.
            echo # JPA / Hibernate
            echo spring.jpa.hibernate.ddl-auto=update
            echo spring.jpa.show-sql=true
            echo spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect
            echo.
            echo # Server Configuration
            echo server.port=8080
            echo.
            echo # JWT Configuration
            echo jwt.secret=your-256-bit-secret-key-change-this-in-production-minimum-32-characters-for-security
            echo jwt.expiration=86400000
            echo.
            echo # Logging
            echo logging.level.root=INFO
            echo logging.level.com.campuscoord=DEBUG
        ) > "backend_java\backend\src\main\resources\application.properties.template"
        echo [OK] Created application.properties.template
    )
    
    del /q "backend_java\backend\src\main\resources\application.properties"
    echo [OK] Removed application.properties
)

REM Remove environment files
if exist "frontend_tkinter\.env.development" del /q "frontend_tkinter\.env.development"
if exist "frontend_tkinter\.env.production" del /q "frontend_tkinter\.env.production"

REM 5. Remove Python bytecode
echo.
echo Removing Python bytecode...
for /r %%f in (*.pyc) do @del /q "%%f" 2>nul
for /r %%f in (*.pyo) do @del /q "%%f" 2>nul
for /r %%f in (*.pyd) do @del /q "%%f" 2>nul
echo [OK] Removed Python bytecode files

REM 6. Remove OS-specific files
echo.
echo Removing OS-specific files...
for /r %%f in (.DS_Store) do @del /q "%%f" 2>nul
for /r %%f in (Thumbs.db) do @del /q "%%f" 2>nul
for /r %%f in (desktop.ini) do @del /q "%%f" 2>nul
echo [OK] Removed OS-specific files

REM 7. Summary
echo.
echo =========================================
echo   Cleanup Summary
echo =========================================
echo.
echo Cleanup completed successfully!
echo.

REM 8. Create checklist
echo Creating DELIVERY_CHECKLIST.txt...
(
    echo Campus Event System - Pre-Delivery Checklist
    echo =============================================
    echo.
    echo Before delivering to client, verify:
    echo.
    echo Infrastructure:
    echo [ ] Cleanup script has been run
    echo [ ] No build artifacts remain
    echo [ ] No log files remain
    echo [ ] No test scripts remain
    echo.
    echo Sensitive Data:
    echo [ ] No personal passwords in any files
    echo [ ] No hardcoded absolute paths
    echo [ ] No API keys or secrets
    echo [ ] application.properties has been removed ^(template exists^)
    echo.
    echo Documentation:
    echo [ ] CLIENT_SETUP_GUIDE.md exists and is complete
    echo [ ] WINDOWS_SETUP_GUIDE.md exists
    echo [ ] MACOS_SETUP_GUIDE.md exists
    echo [ ] TROUBLESHOOTING_GUIDE.md exists
    echo [ ] README.md is up to date
    echo.
    echo Configuration:
    echo [ ] application.properties.template exists
    echo [ ] All templates have placeholder values
    echo.
    echo Testing:
    echo [ ] Tested setup on clean machine ^(if possible^)
    echo [ ] All startup scripts work
    echo [ ] Database schema loads correctly
    echo.
    echo Packaging:
    echo [ ] Decided on delivery method
    echo [ ] Created package/repository
    echo [ ] Verified package contents
    echo.
    echo Final Steps:
    echo [ ] Delete this checklist before delivery
    echo [ ] Send package to client
    echo.
) > "DELIVERY_CHECKLIST.txt"

echo.
echo =========================================
echo   Important Next Steps
echo =========================================
echo.
echo Before delivering to client:
echo.
echo   1. [X] Run this script ^(you just did!^)
echo   2. [ ] Verify CLIENT_SETUP_GUIDE.md exists
echo   3. [ ] Verify application.properties.template exists
echo   4. [ ] Test on a clean machine if possible
echo   5. [ ] Update README.md with final notes
echo   6. [ ] Check for remaining personal information
echo   7. [ ] Package the repository
echo   8. [ ] Include LICENSE file
echo.
echo Review DELIVERY_CHECKLIST.txt before final delivery
echo.
echo All done!
echo.

pause
