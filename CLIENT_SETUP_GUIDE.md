# 🎓 Campus Event System - Complete Client Setup Guide

**Welcome! This guide will help you set up and run the Campus Event System on your machine.**

> 📘 **For:** New clients who purchased this project  
> 💻 **Platforms:** Windows 10/11 and macOS (10.15+)  
> ⏱️ **Setup Time:** 60-75 minutes (includes cleanup)  
> 🎯 **Difficulty:** Beginner-friendly (no prior experience required)

---

## ⚠️ CRITICAL: Read CLEANUP_BEFORE_SETUP.md First!

**Before following this guide, you MUST clean up developer files!**

**→ Go to [CLEANUP_BEFORE_SETUP.md](CLEANUP_BEFORE_SETUP.md) and complete all cleanup steps first.**

This includes:
- Deleting test scripts (`test_*.py`, `test_*.sh`, etc.)
- Deleting log files and build artifacts
- **EDITING application.properties to replace developer's password `SAIAJAY@2005` with YOUR password**

**Do NOT proceed until cleanup is complete!**

---

## 📋 Table of Contents

1. [What You're Getting](#what-youre-getting)
2. [System Requirements](#system-requirements)
3. [Step 1: Download the Repository](#step-1-download-the-repository)
4. [Step 2: Install Required Software](#step-2-install-required-software)
   - [Windows Installation](#windows-installation)
   - [macOS Installation](#macos-installation)
5. [Step 3: Set Up the Database](#step-3-set-up-the-database)
6. [Step 4: Configure the Application](#step-4-configure-the-application)
7. [Step 5: Install Project Dependencies](#step-5-install-project-dependencies)
8. [Step 6: Run the Application](#step-6-run-the-application)
9. [Step 7: First Login](#step-7-first-login)
10. [Troubleshooting Common Issues](#troubleshooting-common-issues)
11. [Next Steps](#next-steps)

---

## What You're Getting

This is a **complete campus event and resource management system** with:

- ✅ **Backend**: Java Spring Boot (REST API)
- ✅ **Frontend**: Python Tkinter (Desktop Application)
- ✅ **Database**: MySQL
- ✅ **Features**: 
  - User management (Students, Organizers, Admins)
  - Event creation and registration
  - Resource booking system
  - Admin approval workflows
  - Email notifications
  - Dark mode support
  - And much more!

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 10/11 (64-bit) or macOS 10.15+ |
| **RAM** | 4 GB minimum, 8 GB recommended |
| **Storage** | 2 GB free space |
| **Internet** | Required for initial setup |
| **Display** | 1280x720 minimum resolution |

### Software You'll Install (Don't worry, we'll guide you!)

1. **Git** - To download the repository
2. **Java 17 or later** - For the backend
3. **Maven 3.8+** - To build the backend
4. **Python 3.11+** - For the frontend
5. **MySQL 8.0+** - For the database

---

## Step 1: Download the Repository

### Option A: Using Git (Recommended)

1. **Open Terminal/Command Prompt**
   - **Windows**: Press `Win + R`, type `cmd`, press Enter
   - **macOS**: Press `Cmd + Space`, type `terminal`, press Enter

2. **Navigate to where you want to install**
   ```bash
   # Windows
   cd C:\Users\YourName\Documents
   
   # macOS
   cd ~/Documents
   ```

3. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/CampusEventSystem.git
   cd CampusEventSystem
   ```

### Option B: Download ZIP

1. Go to the GitHub repository page
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to your desired location
5. Remember this location - you'll need it!

---

## Step 2: Install Required Software

### Windows Installation

#### 2.1 Install Git (if not already installed)

1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use default settings (just keep clicking "Next")
4. **Verify installation**: Open Command Prompt and type:
   ```bash
   git --version
   ```
   You should see something like `git version 2.x.x`

#### 2.2 Install Java 17 (OpenJDK)

1. **Download Java 17 (OpenJDK)**:
   - Go to: https://adoptium.net/
   - Click **"Download"** for Java 17 (LTS)
   - Choose **Windows x64** installer

2. **Install Java**:
   - Run the downloaded `.msi` file
   - ✅ Check **"Add to PATH"** during installation
   - ✅ Check **"Set JAVA_HOME variable"**
   - Click "Install"

3. **Verify installation**:
   Open a **NEW** Command Prompt and type:
   ```bash
   java -version
   ```
   You should see: `openjdk version "17.x.x"`

#### 2.3 Install Maven

1. **Download Maven**:
   - Go to: https://maven.apache.org/download.cgi
   - Download **Binary zip archive** (apache-maven-3.9.x-bin.zip)

2. **Install Maven**:
   - Extract to `C:\Program Files\Apache\maven`
   - **Add to PATH**:
     1. Press `Win + X`, select "System"
     2. Click "Advanced system settings"
     3. Click "Environment Variables"
     4. Under "System variables", find `Path`, click "Edit"
     5. Click "New", add: `C:\Program Files\Apache\maven\bin`
     6. Click "OK" on all windows

3. **Verify installation**:
   Open a **NEW** Command Prompt and type:
   ```bash
   mvn -version
   ```
   You should see Maven version information.

#### 2.4 Install Python 3.11+

1. **Download Python**:
   - Go to: https://www.python.org/downloads/
   - Download **Python 3.11** or later

2. **Install Python**:
   - Run the installer
   - ⚠️ **IMPORTANT**: Check ✅ **"Add Python to PATH"**
   - Click "Install Now"

3. **Verify installation**:
   ```bash
   python --version
   ```
   Should show: `Python 3.11.x` or later

#### 2.5 Install MySQL 8.0

1. **Download MySQL**:
   - Go to: https://dev.mysql.com/downloads/installer/
   - Download **MySQL Installer** (mysql-installer-community)

2. **Install MySQL**:
   - Run the installer
   - Choose **"Developer Default"**
   - Click "Execute" to install components
   - **Set ROOT password** (remember this!): 
     - ⚠️ **Write this down**: _________________________
   - Use default settings for everything else
   - Complete the installation

3. **Verify installation**:
   Open Command Prompt:
   ```bash
   mysql --version
   ```
   Should show: `mysql  Ver 8.0.x`

---

### macOS Installation

#### 2.1 Install Homebrew (Package Manager)

1. Open Terminal
2. Install Homebrew:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Follow the instructions to add Homebrew to your PATH
4. Verify:
   ```bash
   brew --version
   ```

#### 2.2 Install Git (Usually Pre-installed)

```bash
git --version
```
If not installed, Homebrew will prompt you to install it.

#### 2.3 Install Java 17

```bash
# Install Java 17
brew install openjdk@17

# Add to PATH (copy and paste this exactly)
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
java -version
```
Should show: `openjdk version "17.x.x"`

#### 2.4 Install Maven

```bash
# Install Maven
brew install maven

# Verify
mvn -version
```

#### 2.5 Install Python 3.11

```bash
# Install Python 3.11
brew install python@3.11

# Verify
python3.11 --version
```

#### 2.6 Install MySQL 8.0

```bash
# Install MySQL
brew install mysql

# Start MySQL
brew services start mysql

# Secure installation (set root password)
mysql_secure_installation
```

**During mysql_secure_installation:**
- Set root password (⚠️ **Write this down**: _________________________)
- Answer "Y" to other questions

**Verify:**
```bash
mysql --version
```

---

## Step 3: Set Up the Database

### 3.1 Access MySQL

**Windows:**
```bash
mysql -u root -p
```

**macOS:**
```bash
mysql -u root -p
```

Enter the root password you set during installation.

### 3.2 Create the Database

In the MySQL prompt, run these commands **one at a time**:

```sql
CREATE DATABASE campusdb;
USE campusdb;
SOURCE database_sql/schema.sql;
SOURCE database_sql/sample_data.sql;
EXIT;
```

**⚠️ Important Notes:**
- Replace `database_sql/schema.sql` with the **full path** if the command fails
- **Windows example**: `SOURCE C:/Users/YourName/Documents/CampusEventSystem/database_sql/schema.sql;`
- **macOS example**: `SOURCE /Users/YourName/Documents/CampusEventSystem/database_sql/schema.sql;`

### 3.3 Verify Database Setup

Log back into MySQL:
```bash
mysql -u root -p
```

Check if tables were created:
```sql
USE campusdb;
SHOW TABLES;
EXIT;
```

You should see tables like: `users`, `events`, `resources`, `bookings`, etc.

✅ **Success!** Database is ready.

---

## Step 4: Configure the Application

### 4.1 Configure Backend (Database Connection)

1. **Navigate to backend configuration**:
   ```bash
   cd backend_java/backend/src/main/resources
   ```

2. **Open `application.properties` file** in a text editor:
   - **Windows**: Use Notepad or Notepad++
   - **macOS**: Use TextEdit or any text editor

3. **Update the following lines**:

   **Find these lines:**
   ```properties
   spring.datasource.url=jdbc:mysql://localhost:3306/campusdb
   spring.datasource.username=root
   spring.datasource.password=SAIAJAY@2005
   ```

   **Change to** (use YOUR MySQL root password):
   ```properties
   spring.datasource.url=jdbc:mysql://localhost:3306/campusdb
   spring.datasource.username=root
   spring.datasource.password=YOUR_MYSQL_PASSWORD_HERE
   ```

4. **Save the file**

⚠️ **IMPORTANT**: Replace `YOUR_MYSQL_PASSWORD_HERE` with the actual password you set for MySQL root user!

### 4.2 Configure Frontend (API Connection)

The frontend is already configured to connect to `http://localhost:8080/api` (the backend).

**Only change this if you're running the backend on a different machine or port.**

To change frontend config:
1. Open: `frontend_tkinter/config.py`
2. Update `API_BASE_URL` if needed (default is fine for most users)

---

## Step 5: Install Project Dependencies

### 5.1 Backend Dependencies (Maven will download automatically)

Navigate to the backend directory:
```bash
cd backend_java/backend
```

**Build the project** (this downloads all dependencies):
```bash
# This will take 2-5 minutes the first time
mvn clean install
```

You should see: `BUILD SUCCESS`

### 5.2 Frontend Dependencies (Python packages)

Navigate to the frontend directory:
```bash
cd ../../frontend_tkinter
```

**Install Python dependencies**:

**Windows:**
```bash
pip install -r requirements.txt
```

**macOS:**
```bash
pip3 install -r requirements.txt
```

This will install all required Python packages (requests, Pillow, matplotlib, etc.)

---

## Step 6: Run the Application

You have two options:

### Option A: Quick Start (Recommended)

From the **project root directory**:

**macOS/Linux:**
```bash
./run.sh
```

**Windows:**
```bash
# You'll need to run backend and frontend separately (see Option B)
```

This script will:
- Start the backend (Spring Boot)
- Wait for it to be ready
- Start the frontend (Tkinter GUI)

### Option B: Manual Start (Works on all platforms)

**Terminal/Command Prompt 1 - Start Backend:**
```bash
cd backend_java/backend
mvn spring-boot:run
```

Wait until you see:
```
Started CampusEventSystemApplication in X.XXX seconds
```

**Terminal/Command Prompt 2 - Start Frontend:**

Open a **NEW** terminal/command prompt:

**Windows:**
```bash
cd frontend_tkinter
python main.py
```

**macOS:**
```bash
cd frontend_tkinter
python3.11 main.py
```

The GUI application should open!

---

## ✅ Step 7: Test the Application

### Login with Demo Accounts

The system comes with 3 pre-configured test accounts (from `database_sql/sample_data.sql`):

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@campus.com | test123 |
| Organizer | organizer1@campus.com | test123 |
| Student | student1@campus.com | test123 |

### Test Each Role:

**1. Test Admin Account:**
- Login as admin@campus.com / test123
- You should see: Dashboard with Admin panel
- Try: Approve a booking, manage users

**2. Test Organizer Account:**
- Login as organizer1@campus.com / test123
- You should see: Dashboard with event management
- Try: Create an event, view registrations

**3. Test Student Account:**
- Login as student1@campus.com / test123
- You should see: Dashboard with browsing options
- Try: Browse events, book a resource

### ⚠️ IMPORTANT: Change Default Passwords

After testing, you should change these default passwords for security:

```sql
-- Connect to MySQL
mysql -u root -p

-- Use the database
USE campusdb;

-- Change passwords (password will be 'newpass123' after bcrypt hashing)
-- Generate new bcrypt hash at: https://bcrypt-generator.com/

UPDATE users SET password_hash = '$2a$10$YOUR_NEW_BCRYPT_HASH_HERE' 
WHERE email = 'admin@campus.com';

UPDATE users SET password_hash = '$2a$10$YOUR_NEW_BCRYPT_HASH_HERE' 
WHERE email = 'organizer1@campus.com';

UPDATE users SET password_hash = '$2a$10$YOUR_NEW_BCRYPT_HASH_HERE' 
WHERE email = 'student1@campus.com';
```

---

---

## Troubleshooting Common Issues

### Issue 1: "Port 8080 already in use"

**Problem**: Another application is using port 8080.

**Solution**:

**Windows:**
```bash
# Find what's using port 8080
netstat -ano | findstr :8080

# Kill the process (replace PID with the number from above)
taskkill /PID <PID> /F
```

**macOS:**
```bash
# Find and kill process on port 8080
lsof -ti:8080 | xargs kill -9
```

---

### Issue 2: "MySQL Connection Failed"

**Problem**: Can't connect to MySQL database.

**Solutions**:

1. **Verify MySQL is running**:
   - **Windows**: Check Services (search "services.msc"), look for MySQL80
   - **macOS**: `brew services list` should show mysql as "started"

2. **Start MySQL if stopped**:
   - **Windows**: In Services, right-click MySQL80 → Start
   - **macOS**: `brew services start mysql`

3. **Check password in application.properties**:
   - Open: `backend_java/backend/src/main/resources/application.properties`
   - Verify the password matches your MySQL root password

4. **Test MySQL connection manually**:
   ```bash
   mysql -u root -p
   ```
   If this doesn't work, your MySQL installation may have issues.

---

### Issue 3: "Java command not found"

**Problem**: Java is not installed or not in PATH.

**Solution**:

1. **Verify Java installation**:
   ```bash
   java -version
   ```

2. **If not found**:
   - Reinstall Java (see Step 2)
   - Make sure to check "Add to PATH" during installation
   - Restart your terminal/command prompt

3. **Manually add to PATH** (if needed):
   
   **Windows**:
   - Find Java installation (usually `C:\Program Files\Java\jdk-17`)
   - Add `C:\Program Files\Java\jdk-17\bin` to System PATH
   
   **macOS**:
   ```bash
   echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

---

### Issue 4: "Python module not found"

**Problem**: Required Python packages are missing.

**Solution**:
```bash
cd frontend_tkinter
pip install -r requirements.txt --upgrade
```

**macOS**:
```bash
pip3 install -r requirements.txt --upgrade
```

---

### Issue 5: "Cannot connect to backend"

**Problem**: Frontend can't reach the backend API.

**Solutions**:

1. **Verify backend is running**:
   - Check Terminal 1 for backend logs
   - Visit: http://localhost:8080/actuator/health
   - Should show: `{"status":"UP"}`

2. **Check firewall**:
   - Allow Java through firewall
   - **Windows**: Windows Defender Firewall → Allow an app
   - **macOS**: System Preferences → Security & Privacy → Firewall

3. **Verify backend port**:
   - Backend should be on port 8080
   - Check `backend_java/backend/src/main/resources/application.properties`

---

### Issue 6: Frontend window is blank or crashes

**Problem**: Tkinter display issues.

**Solutions**:

1. **Update Python**:
   ```bash
   python --version  # Should be 3.11+
   ```

2. **Reinstall Tkinter** (if needed):
   
   **macOS**:
   ```bash
   brew install python-tk@3.11
   ```
   
   **Windows**: Tkinter is included with Python installer

3. **Check Python packages**:
   ```bash
   cd frontend_tkinter
   pip install -r requirements.txt --force-reinstall
   ```

---

### Issue 7: Buttons appear grey on macOS

**Problem**: macOS Big Sur+ changed button appearance.

**Solution**: This is already fixed in the code! If you still see grey buttons:
- Check `frontend_tkinter/MACOS_BUTTON_FIX.md` for details
- The app uses Canvas-based buttons for consistent appearance

---

### Issue 8: Maven build fails

**Problem**: Maven can't build the project.

**Solutions**:

1. **Clear Maven cache**:
   ```bash
   mvn clean
   mvn clean install -U
   ```

2. **Check internet connection**: Maven downloads dependencies

3. **Verify Maven installation**:
   ```bash
   mvn -version
   ```

4. **Use Maven Wrapper** (included in project):
   ```bash
   cd backend_java/backend
   ./mvnw clean install   # macOS/Linux
   mvnw.cmd clean install # Windows
   ```

---

## Next Steps

### 1. Change Default Passwords

⚠️ **IMPORTANT FOR PRODUCTION**: The default test accounts have simple passwords (`test123`). You should:

1. **Login as Admin**: `admin@campus.com` / `test123`
2. Go to **User Management**
3. Change passwords for all default accounts
4. Create your own admin account
5. Delete or disable the default test accounts

### 2. Customize the Application

- **Logo**: Replace images in `frontend_tkinter/images/`
- **Colors**: Edit `frontend_tkinter/styles/` (if exists)
- **Database**: Add your own events, resources, users

### 3. Read Additional Documentation

- **[README.md](README.md)** - Overview and features
- **[STARTUP_GUIDE.md](STARTUP_GUIDE.md)** - Detailed startup instructions
- **[API_TESTING_GUIDE.md](README.md#-api-testing-guide)** - Test the backend API
- **[frontend_tkinter/README.md](frontend_tkinter/README.md)** - Frontend documentation

### 4. Backup Your Database

```bash
mysqldump -u root -p campusdb > campusdb_backup.sql
```

### 5. Development Workflow

```bash
# Start everything
./run.sh

# Make changes to code...

# Restart services
./stop.sh
./run.sh
```

---

## 📞 Support and Resources

### Quick Reference

| Item | Value |
|------|-------|
| **Backend URL** | http://localhost:8080 |
| **Backend Health Check** | http://localhost:8080/actuator/health |
| **Database Name** | campusdb |
| **Database User** | root |
| **Default Port** | 8080 (backend), MySQL: 3306 |

### Log Files

If something goes wrong, check these files:

- **Backend logs**: `backend_java/backend/backend.log`
- **Frontend logs**: `frontend_tkinter/frontend.log` (if running with run.sh)
- **MySQL logs**: Varies by OS

### Useful Commands

```bash
# Check if backend is running
curl http://localhost:8080/actuator/health

# Check if port 8080 is in use
# Windows:
netstat -ano | findstr :8080

# macOS:
lsof -i:8080

# View backend logs (while running)
# macOS:
tail -f backend.log

# Windows:
type backend.log
```

---

## 🎉 Congratulations!

You've successfully set up the Campus Event System!

### What You Can Do Now:

✅ Create and manage events  
✅ Book resources  
✅ Register for events  
✅ Manage users (as Admin)  
✅ Approve bookings and events  
✅ And much more!

### Explore the Features:

- 📚 Browse the extensive **[README.md](README.md)** for all features
- 🧪 Try the **API endpoints** with curl or Postman
- 🎨 Customize the application for your needs
- 📊 Add your own events and resources

**Happy organizing!** 🚀

---

**Document Version**: 1.0  
**Last Updated**: November 4, 2025  
**Support**: Check README.md and existing documentation files
