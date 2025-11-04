# 🪟 Windows Setup Guide - Campus Event System

**Complete step-by-step guide for setting up the Campus Event System on Windows 10/11**

---

## 📋 What You Need

- Windows 10 or Windows 11 (64-bit)
- Administrator access
- Internet connection
- About 60 minutes

---

## Table of Contents

1. [Install Git](#1-install-git)
2. [Install Java 17](#2-install-java-17)
3. [Install Maven](#3-install-maven)
4. [Install Python 3.11](#4-install-python-311)
5. [Install MySQL 8.0](#5-install-mysql-80)
6. [Download the Project](#6-download-the-project)
7. [Set Up Database](#7-set-up-database)
8. [Configure Application](#8-configure-application)
9. [Install Dependencies](#9-install-dependencies)
10. [Run the Application](#10-run-the-application)
11. [Windows-Specific Tips](#11-windows-specific-tips)

---

## 1. Install Git

### Download and Install

1. **Download Git**:
   - Go to: https://git-scm.com/download/win
   - Download "64-bit Git for Windows Setup"

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - Use these settings (just click Next for most):
     - ✅ "Git Bash Here" context menu
     - ✅ "Git from the command line and also from 3rd-party software"
     - ✅ "Use the OpenSSL library"
     - ✅ "Checkout Windows-style, commit Unix-style line endings"
     - ✅ "Use MinTTY"
     - ✅ Default for everything else

3. **Verify Installation**:
   - Press `Win + R`, type `cmd`, press Enter
   - Type:
     ```cmd
     git --version
     ```
   - Should show: `git version 2.x.x`

✅ **Done!** Git is installed.

---

## 2. Install Java 17

### Download Java (Adoptium Eclipse Temurin)

1. **Download Java 17**:
   - Go to: https://adoptium.net/
   - Click **Download** for Java 17 (LTS)
   - Choose: **Windows x64** (MSI installer)

2. **Run the Installer**:
   - Double-click the downloaded `.msi` file
   - **IMPORTANT**: During installation:
     - ✅ Check **"Set JAVA_HOME variable"**
     - ✅ Check **"JavaSoft (Oracle) registry keys"**
     - ✅ Check **"Add to PATH"**
   - Click "Install"
   - Click "Finish"

3. **Verify Installation**:
   - Open a **NEW** Command Prompt (Win + R → `cmd`)
   - Type:
     ```cmd
     java -version
     ```
   - Should show:
     ```
     openjdk version "17.0.x"
     ```

   Also check:
   ```cmd
   echo %JAVA_HOME%
   ```
   Should show path like: `C:\Program Files\Eclipse Adoptium\jdk-17.x.x.x-hotspot\`

### Troubleshooting: JAVA_HOME Not Set

If `echo %JAVA_HOME%` shows nothing:

1. Press `Win + X` → "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", click "New":
   - Variable name: `JAVA_HOME`
   - Variable value: `C:\Program Files\Eclipse Adoptium\jdk-17.0.9.9-hotspot` (your version)
5. Find "Path" in System variables, click "Edit"
6. Click "New", add: `%JAVA_HOME%\bin`
7. Click OK on all windows
8. **Restart Command Prompt** and test again

✅ **Done!** Java is installed.

---

## 3. Install Maven

### Download and Extract

1. **Download Maven**:
   - Go to: https://maven.apache.org/download.cgi
   - Download: **Binary zip archive** (`apache-maven-3.9.x-bin.zip`)

2. **Extract Maven**:
   - Right-click the downloaded ZIP file → "Extract All"
   - Extract to: `C:\Program Files\Apache\`
   - You should have: `C:\Program Files\Apache\apache-maven-3.9.5\`

### Add Maven to PATH

1. **Open Environment Variables**:
   - Press `Win + X` → "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"

2. **Create MAVEN_HOME** (optional but recommended):
   - Under "System variables", click "New"
   - Variable name: `MAVEN_HOME`
   - Variable value: `C:\Program Files\Apache\apache-maven-3.9.5`

3. **Add Maven to PATH**:
   - Find "Path" in System variables, click "Edit"
   - Click "New"
   - Add: `C:\Program Files\Apache\apache-maven-3.9.5\bin`
   - Click OK on all windows

4. **Verify Installation**:
   - Open a **NEW** Command Prompt
   - Type:
     ```cmd
     mvn -version
     ```
   - Should show:
     ```
     Apache Maven 3.9.5
     Maven home: C:\Program Files\Apache\apache-maven-3.9.5
     Java version: 17.0.9
     ```

✅ **Done!** Maven is installed.

---

## 4. Install Python 3.11

### Download and Install

1. **Download Python**:
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.11.x"

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - ⚠️ **CRITICAL**: At the bottom, check ✅ **"Add Python 3.11 to PATH"**
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation**:
   - Open a **NEW** Command Prompt
   - Type:
     ```cmd
     python --version
     ```
   - Should show: `Python 3.11.x`

   Also check pip:
   ```cmd
   pip --version
   ```
   Should show pip version.

### Troubleshooting: Python Not Found

If `python --version` doesn't work:

1. Press `Win + R`, type `%LOCALAPPDATA%\Programs\Python`
2. Find your Python installation folder (e.g., `Python311`)
3. Copy this path
4. Add to System PATH:
   - Win + X → System → Advanced → Environment Variables
   - Edit "Path"
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311`
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts`
5. Restart Command Prompt

✅ **Done!** Python is installed.

---

## 5. Install MySQL 8.0

### Download MySQL Installer

1. **Download MySQL Installer**:
   - Go to: https://dev.mysql.com/downloads/installer/
   - Download: **MySQL Installer** (mysql-installer-community-8.0.x.x.msi)
   - You may need to create a free Oracle account (or click "No thanks, just start my download")

### Install MySQL

2. **Run the Installer**:
   - Double-click the downloaded `.msi` file
   - Choose **"Developer Default"** setup type
   - Click "Next"

3. **Install Components**:
   - Click "Execute" to download and install all components
   - Wait for all components to install (green checkmarks)
   - Click "Next"

4. **Configure MySQL Server**:
   
   **Type and Networking**:
   - Use defaults (Development Computer, Port 3306)
   - Click "Next"
   
   **Authentication Method**:
   - Use recommended: "Use Strong Password Encryption"
   - Click "Next"
   
   **Accounts and Roles**:
   - Set **ROOT PASSWORD**: Enter a password
   - ⚠️ **WRITE IT DOWN**: __________________________
   - Confirm the password
   - (Optional) Add additional MySQL user accounts
   - Click "Next"
   
   **Windows Service**:
   - ✅ Configure MySQL Server as Windows Service
   - ✅ Start MySQL Server at System Startup
   - Click "Next"
   
   **Server File Permissions**:
   - Use defaults
   - Click "Next"
   
   **Apply Configuration**:
   - Click "Execute"
   - Wait for configuration to complete
   - Click "Finish"

5. **Complete Installation**:
   - Click "Next" → "Finish"
   - You may need to do this for multiple components

### Verify MySQL Installation

6. **Test MySQL**:
   - Open Command Prompt
   - Type:
     ```cmd
     mysql --version
     ```
   - Should show: `mysql Ver 8.0.x`

7. **Test Login**:
   ```cmd
   mysql -u root -p
   ```
   - Enter your root password
   - You should see: `mysql>`
   - Type: `EXIT;` to quit

✅ **Done!** MySQL is installed and running.

---

## 6. Download the Project

### Option A: Using Git (Recommended)

1. **Choose Installation Directory**:
   - Open Command Prompt
   - Navigate to where you want to install:
     ```cmd
     cd C:\Users\YourName\Documents
     ```

2. **Clone Repository**:
   ```cmd
   git clone https://github.com/YOUR_USERNAME/CampusEventSystem.git
   cd CampusEventSystem
   ```

### Option B: Download ZIP

1. Go to GitHub repository
2. Click green "Code" button → "Download ZIP"
3. Right-click ZIP → "Extract All"
4. Extract to: `C:\Users\YourName\Documents\CampusEventSystem`

✅ **Done!** Project is downloaded.

---

## 7. Set Up Database

### Create Database and Tables

1. **Open Command Prompt in Project Directory**:
   ```cmd
   cd C:\Users\YourName\Documents\CampusEventSystem
   ```

2. **Login to MySQL**:
   ```cmd
   mysql -u root -p
   ```
   - Enter your root password

3. **Create Database**:
   ```sql
   CREATE DATABASE campusdb;
   USE campusdb;
   ```

4. **Load Schema**:
   ```sql
   SOURCE database_sql/schema.sql;
   ```
   
   If you get an error, use the full path:
   ```sql
   SOURCE C:/Users/YourName/Documents/CampusEventSystem/database_sql/schema.sql;
   ```
   
   ⚠️ **Note**: Use **forward slashes** (`/`) not backslashes in SQL!

5. **Load Sample Data**:
   ```sql
   SOURCE database_sql/sample_data.sql;
   ```
   Or with full path:
   ```sql
   SOURCE C:/Users/YourName/Documents/CampusEventSystem/database_sql/sample_data.sql;
   ```

6. **Verify Tables Were Created**:
   ```sql
   SHOW TABLES;
   ```
   You should see: `users`, `events`, `resources`, `bookings`, etc.

7. **Exit MySQL**:
   ```sql
   EXIT;
   ```

✅ **Done!** Database is ready.

---

## 8. Configure Application

### Update Database Connection

1. **Navigate to Backend Config**:
   ```cmd
   cd backend_java\backend\src\main\resources
   ```

2. **Open application.properties**:
   - Right-click → "Edit with Notepad"
   - Or use Notepad++, VS Code, etc.

3. **Update These Lines**:
   
   **Find**:
   ```properties
   spring.datasource.password=SAIAJAY@2005
   ```
   
   **Change to** (use YOUR MySQL root password):
   ```properties
   spring.datasource.password=YOUR_MYSQL_ROOT_PASSWORD
   ```

4. **Save the file**

5. **Return to project root**:
   ```cmd
   cd ..\..\..\..\..
   ```
   Or just:
   ```cmd
   cd C:\Users\YourName\Documents\CampusEventSystem
   ```

✅ **Done!** Configuration updated.

---

## 9. Install Dependencies

### Backend Dependencies

1. **Navigate to Backend**:
   ```cmd
   cd backend_java\backend
   ```

2. **Build with Maven** (downloads all dependencies):
   ```cmd
   mvn clean install
   ```
   
   This will:
   - Download all Java dependencies (first time takes 3-5 minutes)
   - Compile the code
   - Run tests
   
   You should see: `BUILD SUCCESS`

### Frontend Dependencies

3. **Navigate to Frontend**:
   ```cmd
   cd ..\..\frontend_tkinter
   ```

4. **Install Python Packages**:
   ```cmd
   pip install -r requirements.txt
   ```
   
   This installs:
   - requests (API calls)
   - Pillow (images)
   - matplotlib (charts)
   - tkcalendar (calendar widget)
   - And more...

5. **Return to Project Root**:
   ```cmd
   cd ..
   ```

✅ **Done!** All dependencies installed.

---

## 10. Run the Application

### Start Backend (Terminal 1)

1. **Open Command Prompt #1**:
   ```cmd
   cd C:\Users\YourName\Documents\CampusEventSystem
   cd backend_java\backend
   ```

2. **Start Backend**:
   ```cmd
   mvn spring-boot:run
   ```

3. **Wait for it to start**:
   - You'll see lots of log messages
   - Wait until you see:
     ```
     Started CampusEventSystemApplication in X.XXX seconds
     ```
   - **Keep this terminal open!**

### Start Frontend (Terminal 2)

4. **Open Command Prompt #2** (NEW window):
   ```cmd
   cd C:\Users\YourName\Documents\CampusEventSystem
   cd frontend_tkinter
   ```

5. **Start Frontend**:
   ```cmd
   python main.py
   ```

6. **GUI Should Open!**:
   - The application window should appear
   - You should see the login screen

### Test Login

7. **Login with Test Account**:
   - Email: `admin@campus.com`
   - Password: `test123`
   - Click "Login"

✅ **Success!** Application is running.

---

## 11. Windows-Specific Tips

### Firewall Warning

When you first run the backend, Windows may show a firewall warning:
- Click **"Allow access"**
- This allows the backend to accept connections

### Running in Background

To run backend in background:
```cmd
start /b mvn spring-boot:run
```

### Checking Ports

To see what's using port 8080:
```cmd
netstat -ano | findstr :8080
```

To kill a process on port 8080:
```cmd
# Get PID from netstat output, then:
taskkill /PID <PID_NUMBER> /F
```

### Path Issues

Windows uses backslashes (`\`), but:
- In SQL commands, use forward slashes (`/`)
- In Java properties, use forward slashes (`/`)

### Command Prompt Shortcuts

- `Win + R` → `cmd` - Open Command Prompt
- `Win + X` → "Windows Terminal" - Open Terminal (Windows 11)
- Right-click folder while holding Shift → "Open Command Window Here"

### Text Editors

Recommended editors for editing config files:
- **Notepad++**: https://notepad-plus-plus.org/
- **VS Code**: https://code.visualstudio.com/
- **Sublime Text**: https://www.sublimetext.com/

### MySQL GUI Tools (Optional)

For easier database management:
- **MySQL Workbench**: https://dev.mysql.com/downloads/workbench/
- Included with MySQL Installer

---

## 🎉 You're Done!

### Quick Reference

| Component | Command to Start |
|-----------|------------------|
| **Backend** | `cd backend_java\backend` then `mvn spring-boot:run` |
| **Frontend** | `cd frontend_tkinter` then `python main.py` |
| **MySQL** | Automatically runs as Windows service |
| **Check Backend** | Visit: http://localhost:8080/actuator/health |

### Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@campus.com` | `test123` |
| Organizer | `organizer1@campus.com` | `test123` |
| Student | `student1@campus.com` | `test123` |

### Next Steps

1. ✅ Change default passwords
2. ✅ Explore the application features
3. ✅ Read the main [README.md](README.md) for API documentation
4. ✅ Customize for your needs

---

## 🆘 Common Windows Issues

### Issue: "mvn is not recognized"

**Solution**: Maven not in PATH
1. Verify Maven installation: `C:\Program Files\Apache\apache-maven-3.9.5`
2. Add to PATH (see Step 3 above)
3. Restart Command Prompt

### Issue: "Python is not recognized"

**Solution**: Python not in PATH
1. Find Python: Usually in `C:\Users\YourName\AppData\Local\Programs\Python\Python311`
2. Add to PATH
3. Restart Command Prompt

### Issue: "Access denied" when installing software

**Solution**: Run installer as Administrator
- Right-click installer → "Run as administrator"

### Issue: Port 8080 already in use

**Solution**: Kill the process
```cmd
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Issue: MySQL won't start

**Solution**: Start MySQL service
1. Press `Win + R`, type `services.msc`
2. Find "MySQL80"
3. Right-click → "Start"

---

**Document Version**: 1.0  
**Platform**: Windows 10/11  
**Last Updated**: November 4, 2025
