# 🧹 CLEANUP BEFORE SETUP - READ THIS FIRST!

## ⚠️ CRITICAL: You Received the Developer's Repository

This repository contains files and configurations specific to the developer's machine. **You MUST clean these up before you can run the application on your machine.**

---

## 🎯 What This Document Covers

1. **Files to DELETE** - Developer's test scripts, logs, build artifacts
2. **Files to EDIT** - Configuration files with hardcoded passwords/paths
3. **Why This Matters** - What breaks if you don't clean up
4. **Quick Cleanup Commands** - Copy-paste commands for fast cleanup

---

## 🚨 Files You MUST Delete

### Test Scripts (Not Needed)
These are developer's personal testing scripts - **DELETE THEM ALL**:

```
❌ test_api_token_fix.py
❌ test_button_colors.py
❌ test_create_event.py
❌ test_jwt.sh
❌ test_my_bookings_fixes.sh
❌ test_my_events_fix.py
❌ test_register_labels.py
❌ test_registration_system.sh
❌ test_session_diagnostic.py
❌ update_button_styles.py
```

### Credentials File (Contains Hardcoded Paths)
```
❌ CREDENTIALS_QUICK_REF.txt    # Has developer's machine path
```

### Log Files (Contains Developer's Session Data)
```
❌ *.log (all .log files in root)
❌ backend_java/backend/*.log
❌ frontend_tkinter/*.log
```

### Build Artifacts (Will Be Regenerated)
```
❌ backend_java/backend/target/    # Maven build output
❌ **/__pycache__/                 # Python bytecode
❌ **/*.pyc                        # Python compiled files
```

### OS Files (Not Needed)
```
❌ .DS_Store      # macOS file system metadata
❌ Thumbs.db      # Windows thumbnail cache
```

### IDE Files (Optional - Delete if you use different IDE)
```
❌ .vscode/       # VS Code settings
❌ .idea/         # IntelliJ IDEA settings
❌ *.iml          # IntelliJ project files
```

---

## ✏️ Files You MUST Edit

### 1. Backend Configuration File ⚠️ CRITICAL

**File**: `backend_java/backend/src/main/resources/application.properties`

**Problem**: Contains developer's MySQL password: `SAIAJAY@2005`

**What to change**:
```properties
# Line 4 - BEFORE (developer's password):
spring.datasource.password=SAIAJAY@2005

# Line 4 - AFTER (your password):
spring.datasource.password=YOUR_MYSQL_ROOT_PASSWORD
```

**Why**: The application won't connect to your MySQL database with the developer's password!

### 2. Frontend Configuration (Usually OK)

**File**: `frontend_tkinter/config.py`

**Check this line**:
```python
API_BASE_URL = "http://localhost:8080/api"
```

**Change ONLY if**:
- You changed the backend port in `application.properties`
- Example: If you set `server.port=8081`, change to `http://localhost:8081/api`

---

## 🤖 Quick Cleanup Commands

### Option 1: macOS/Linux (Bash/Zsh)

Copy and paste this entire block:

```bash
#!/bin/bash
echo "🧹 Starting cleanup..."

# Delete test scripts
echo "Deleting test scripts..."
rm -f test_*.py test_*.sh test_*.bat update_button_styles.py

# Delete credentials file
echo "Deleting credentials file..."
rm -f CREDENTIALS_QUICK_REF.txt

# Delete log files
echo "Deleting log files..."
rm -f *.log
rm -f backend_java/backend/*.log
rm -f frontend_tkinter/*.log

# Delete Python cache
echo "Deleting Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Delete Java build artifacts
echo "Deleting Java build artifacts..."
rm -rf backend_java/backend/target/

# Delete OS files
echo "Deleting OS files..."
find . -name ".DS_Store" -delete 2>/dev/null
find . -name "Thumbs.db" -delete 2>/dev/null

# Optional: Delete IDE files
echo "Deleting IDE files (optional)..."
rm -rf .vscode/ .idea/ *.iml 2>/dev/null

echo "✅ Cleanup complete!"
echo ""
echo "⚠️  NEXT STEP: Edit application.properties"
echo "    File: backend_java/backend/src/main/resources/application.properties"
echo "    Change: spring.datasource.password=SAIAJAY@2005"
echo "    To:     spring.datasource.password=YOUR_PASSWORD"
```

**Run it**:
```bash
# Copy the above script, then:
bash  # Paste and press Enter
```

---

### Option 2: Windows (PowerShell)

Copy and paste this entire block:

```powershell
Write-Host "🧹 Starting cleanup..." -ForegroundColor Green

# Delete test scripts
Write-Host "Deleting test scripts..." -ForegroundColor Yellow
Remove-Item test_*.py, test_*.sh, test_*.bat, update_button_styles.py -Force -ErrorAction SilentlyContinue

# Delete credentials file
Write-Host "Deleting credentials file..." -ForegroundColor Yellow
Remove-Item CREDENTIALS_QUICK_REF.txt -Force -ErrorAction SilentlyContinue

# Delete log files
Write-Host "Deleting log files..." -ForegroundColor Yellow
Remove-Item *.log -Force -ErrorAction SilentlyContinue
Remove-Item backend_java\backend\*.log -Force -ErrorAction SilentlyContinue
Remove-Item frontend_tkinter\*.log -Force -ErrorAction SilentlyContinue

# Delete Python cache
Write-Host "Deleting Python cache..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

# Delete Java build artifacts
Write-Host "Deleting Java build artifacts..." -ForegroundColor Yellow
Remove-Item backend_java\backend\target\ -Recurse -Force -ErrorAction SilentlyContinue

# Delete OS files
Write-Host "Deleting OS files..." -ForegroundColor Yellow
Get-ChildItem -Recurse -File -Filter ".DS_Store" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "Thumbs.db" | Remove-Item -Force -ErrorAction SilentlyContinue

# Optional: Delete IDE files
Write-Host "Deleting IDE files (optional)..." -ForegroundColor Yellow
Remove-Item .vscode, .idea -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -File -Filter "*.iml" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  NEXT STEP: Edit application.properties" -ForegroundColor Red
Write-Host "    File: backend_java\backend\src\main\resources\application.properties"
Write-Host "    Change: spring.datasource.password=SAIAJAY@2005"
Write-Host "    To:     spring.datasource.password=YOUR_PASSWORD"
```

**Run it**: Right-click in PowerShell and paste

---

### Option 3: Manual Deletion

**If commands don't work**, delete these manually using File Explorer/Finder:

1. **Root directory**: Delete all files starting with `test_`
2. **Root directory**: Delete `CREDENTIALS_QUICK_REF.txt`
3. **Root directory**: Delete all `*.log` files
4. **backend_java/backend/**: Delete `target` folder
5. **Everywhere**: Delete `__pycache__` folders
6. **Everywhere**: Delete `.DS_Store` and `Thumbs.db` files

---

## 🔍 Verification Checklist

After cleanup, verify these:

```bash
# 1. Test scripts should be gone
ls test_*.py test_*.sh 2>/dev/null
# Should show: "No such file or directory"

# 2. Credentials file should be gone
ls CREDENTIALS_QUICK_REF.txt 2>/dev/null
# Should show: "No such file or directory"

# 3. Log files should be gone
ls *.log 2>/dev/null
# Should show: "No such file or directory"

# 4. Target folder should be gone
ls backend_java/backend/target 2>/dev/null
# Should show: "No such file or directory"

# 5. __pycache__ folders should be gone
find . -name "__pycache__" 2>/dev/null
# Should show: (nothing)
```

**On Windows** (PowerShell):
```powershell
# Check if files are gone
Test-Path test_*.py, CREDENTIALS_QUICK_REF.txt, *.log
# Should show: False
```

---

## ✅ After Cleanup Checklist

- [ ] All test scripts deleted (test_*.py, test_*.sh, etc.)
- [ ] CREDENTIALS_QUICK_REF.txt deleted
- [ ] All .log files deleted
- [ ] backend_java/backend/target/ folder deleted
- [ ] All __pycache__/ folders deleted
- [ ] All .pyc files deleted
- [ ] .DS_Store and Thumbs.db files deleted (if present)
- [ ] Edited application.properties with YOUR MySQL password
- [ ] (Optional) Edited config.py if you changed backend port

---

## 🚨 Why This Cleanup Matters

### If You DON'T Clean Up:

❌ **Application won't start** - Wrong MySQL password  
❌ **Build errors** - Corrupted cache in target/ and __pycache__/  
❌ **Confusion** - Test scripts might interfere with your testing  
❌ **Security risk** - Developer's credentials exposed  
❌ **Disk space wasted** - Build artifacts take up space  

### After You Clean Up:

✅ **Application works** - Uses your MySQL password  
✅ **Clean builds** - Fresh compilation with your environment  
✅ **No confusion** - Only essential files remain  
✅ **Secure** - No hardcoded credentials  
✅ **Organized** - Easy to navigate  

---

## 📚 What to Keep

**DO NOT DELETE these essential files**:

✅ **Source Code**:
- `backend_java/backend/src/` - Java application code
- `frontend_tkinter/` - Python GUI code (except __pycache__)

✅ **Database Files**:
- `database_sql/schema.sql` - Database structure
- `database_sql/sample_data.sql` - Demo accounts and data

✅ **Configuration Templates**:
- `backend_java/backend/pom.xml` - Maven dependencies
- `frontend_tkinter/requirements.txt` - Python dependencies

✅ **Startup Scripts**:
- `run.sh` - Start application (macOS/Linux)
- `run_app.sh`, `run_frontend.sh` - Individual component scripts
- `stop.sh`, `stop_app.sh` - Stop application scripts
- `START_APP.sh` - Alternative startup script

✅ **Documentation**:
- `README.md` - Project overview and features
- `STARTUP_GUIDE.md` - Quick start guide
- `CLIENT_SETUP_GUIDE.md` - Complete setup instructions
- `TROUBLESHOOTING_GUIDE.md` - Problem solving
- All other .md files in root

✅ **Database Scripts**:
- `migrate_db.sh` - Database migration helper

---

## 🎯 Next Steps

After completing this cleanup:

1. **Follow CLIENT_SETUP_GUIDE.md** - Complete setup instructions
2. **Or follow WINDOWS_SETUP_GUIDE.md** - Windows-specific guide
3. **Or follow MACOS_SETUP_GUIDE.md** - macOS-specific guide

---

## 💡 Pro Tips

### Tip 1: Use Git (Optional)
If you want to track your changes:
```bash
git init
git add .
git commit -m "Initial client setup after cleanup"
```

### Tip 2: Backup Configuration
After editing `application.properties`:
```bash
cp backend_java/backend/src/main/resources/application.properties \
   backend_java/backend/src/main/resources/application.properties.backup
```

### Tip 3: Document Your Password
Store your MySQL password somewhere safe (not in the repo):
```bash
echo "MySQL root password: YOUR_PASSWORD" > ~/mysql_password.txt
chmod 600 ~/mysql_password.txt  # Make it readable only by you
```

### Tip 4: Verify Before Building
Before running the application, check:
```bash
# Verify MySQL password is changed
grep "password=" backend_java/backend/src/main/resources/application.properties
# Should show YOUR password, not SAIAJAY@2005
```

---

## 🆘 Need Help?

If cleanup fails or you're unsure:

1. **See TROUBLESHOOTING_GUIDE.md** - Common issues and solutions
2. **Check platform-specific guide**:
   - Windows: WINDOWS_SETUP_GUIDE.md
   - macOS: MACOS_SETUP_GUIDE.md
3. **Verify permissions**: Make sure you have write access to all files

---

## 📊 Cleanup Summary

After cleanup, your repository should:
- **Be ~80% smaller** (no build artifacts)
- **Have no test scripts** (cleaner root directory)
- **Use YOUR credentials** (application.properties edited)
- **Be ready to build** (clean state)

**Typical size reduction**:
- Before: ~150-200 MB (with target/ and logs)
- After: ~30-40 MB (source code only)

---

## ✅ Cleanup Complete Checklist

Print this and check off as you go:

```
[ ] Ran cleanup commands (or deleted files manually)
[ ] Verified test scripts are gone
[ ] Verified CREDENTIALS_QUICK_REF.txt is gone
[ ] Verified log files are gone
[ ] Verified target/ folder is gone
[ ] Verified __pycache__/ folders are gone
[ ] Edited application.properties with MY MySQL password
[ ] Verified password change (grep command)
[ ] (Optional) Checked config.py for correct API URL
[ ] Ready to proceed with CLIENT_SETUP_GUIDE.md
```

---

**Created**: 4 November 2025  
**Version**: 1.0  
**Purpose**: Client cleanup instructions before setup

---

## 🚀 Ready to Continue?

Once cleanup is complete, proceed to:

**→ CLIENT_SETUP_GUIDE.md** (Main setup guide)

Or platform-specific:
- **→ WINDOWS_SETUP_GUIDE.md** (Windows 10/11)
- **→ MACOS_SETUP_GUIDE.md** (macOS 10.15+)

**Time to next step**: 5 minutes after cleanup
