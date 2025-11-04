# 🍎 macOS Setup Guide - Campus Event System

**Complete step-by-step guide for setting up the Campus Event System on macOS**

---

## 📋 What You Need

- macOS 10.15 (Catalina) or later
- Administrator access
- Internet connection
- About 45 minutes

---

## Table of Contents

1. [Install Homebrew](#1-install-homebrew)
2. [Install Git](#2-install-git)
3. [Install Java 17](#3-install-java-17)
4. [Install Maven](#4-install-maven)
5. [Install Python 3.11](#5-install-python-311)
6. [Install MySQL 8.0](#6-install-mysql-80)
7. [Download the Project](#7-download-the-project)
8. [Set Up Database](#8-set-up-database)
9. [Configure Application](#9-configure-application)
10. [Install Dependencies](#10-install-dependencies)
11. [Run the Application](#11-run-the-application)
12. [macOS-Specific Tips](#12-macos-specific-tips)

---

## 1. Install Homebrew

**Homebrew** is a package manager for macOS that makes installing software easy.

### Install Homebrew

1. **Open Terminal**:
   - Press `Cmd + Space`
   - Type "Terminal"
   - Press Enter

2. **Install Homebrew**:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Follow the prompts**:
   - Press Enter when prompted
   - Enter your Mac password when asked
   - Wait for installation (5-10 minutes)

4. **Add Homebrew to PATH** (Apple Silicon Macs only):
   
   If you have an **M1/M2/M3 Mac**, run these commands:
   ```bash
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```

5. **Verify Installation**:
   ```bash
   brew --version
   ```
   Should show: `Homebrew 4.x.x`

✅ **Done!** Homebrew is installed.

---

## 2. Install Git

Git is usually pre-installed on macOS, but let's verify:

### Verify or Install Git

1. **Check if Git is installed**:
   ```bash
   git --version
   ```

2. **If not installed**:
   ```bash
   brew install git
   ```

3. **Verify**:
   ```bash
   git --version
   ```
   Should show: `git version 2.x.x`

✅ **Done!** Git is installed.

---

## 3. Install Java 17

### Install via Homebrew

1. **Install OpenJDK 17**:
   ```bash
   brew install openjdk@17
   ```

2. **Add Java to PATH**:
   ```bash
   echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```
   
   **For Intel Macs**, use:
   ```bash
   echo 'export PATH="/usr/local/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Set JAVA_HOME** (optional but recommended):
   ```bash
   # For Apple Silicon (M1/M2/M3)
   echo 'export JAVA_HOME="/opt/homebrew/opt/openjdk@17"' >> ~/.zshrc
   
   # For Intel Macs
   echo 'export JAVA_HOME="/usr/local/opt/openjdk@17"' >> ~/.zshrc
   
   source ~/.zshrc
   ```

4. **Verify Installation**:
   ```bash
   java -version
   ```
   Should show:
   ```
   openjdk version "17.0.x"
   ```

   Also check:
   ```bash
   echo $JAVA_HOME
   ```
   Should show the Java installation path.

✅ **Done!** Java 17 is installed.

---

## 4. Install Maven

### Install via Homebrew

1. **Install Maven**:
   ```bash
   brew install maven
   ```

2. **Verify Installation**:
   ```bash
   mvn -version
   ```
   Should show:
   ```
   Apache Maven 3.9.x
   Maven home: /opt/homebrew/Cellar/maven/...
   Java version: 17.0.x
   ```

✅ **Done!** Maven is installed.

---

## 5. Install Python 3.11

### Install via Homebrew

1. **Install Python 3.11**:
   ```bash
   brew install python@3.11
   ```

2. **Add Python to PATH**:
   ```bash
   echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```
   
   **For Intel Macs**:
   ```bash
   echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Create aliases** (optional but helpful):
   ```bash
   echo 'alias python=python3.11' >> ~/.zshrc
   echo 'alias pip=pip3.11' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **Verify Installation**:
   ```bash
   python3.11 --version
   ```
   Should show: `Python 3.11.x`

   Also check pip:
   ```bash
   pip3.11 --version
   ```

✅ **Done!** Python 3.11 is installed.

---

## 6. Install MySQL 8.0

### Install via Homebrew

1. **Install MySQL**:
   ```bash
   brew install mysql
   ```

2. **Start MySQL**:
   ```bash
   brew services start mysql
   ```

3. **Secure MySQL Installation**:
   ```bash
   mysql_secure_installation
   ```
   
   **Follow the prompts**:
   - Would you like to setup VALIDATE PASSWORD component? → **Y** (or N for simple passwords)
   - Please set the password for root: → **Enter your password**
   - ⚠️ **WRITE IT DOWN**: __________________________
   - Re-enter new password: → **Confirm password**
   - Remove anonymous users? → **Y**
   - Disallow root login remotely? → **Y**
   - Remove test database? → **Y**
   - Reload privilege tables? → **Y**

4. **Verify Installation**:
   ```bash
   mysql --version
   ```
   Should show: `mysql Ver 8.0.x`

5. **Test Login**:
   ```bash
   mysql -u root -p
   ```
   - Enter your root password
   - You should see: `mysql>`
   - Type: `EXIT;` to quit

### Managing MySQL Service

```bash
# Start MySQL
brew services start mysql

# Stop MySQL
brew services stop mysql

# Restart MySQL
brew services restart mysql

# Check status
brew services list
```

✅ **Done!** MySQL is installed and running.

---

## 7. Download the Project

### Option A: Using Git (Recommended)

1. **Navigate to where you want to install**:
   ```bash
   cd ~/Documents
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/CampusEventSystem.git
   cd CampusEventSystem
   ```

### Option B: Download ZIP

1. Download ZIP from GitHub
2. Extract to desired location
3. Open Terminal and navigate:
   ```bash
   cd ~/Documents/CampusEventSystem
   ```

✅ **Done!** Project is downloaded.

---

## 8. Set Up Database

### Create Database and Load Data

1. **Make sure you're in the project directory**:
   ```bash
   cd ~/Documents/CampusEventSystem
   ```

2. **Login to MySQL**:
   ```bash
   mysql -u root -p
   ```
   - Enter your root password

3. **Create database and load schema**:
   ```sql
   CREATE DATABASE campusdb;
   USE campusdb;
   SOURCE database_sql/schema.sql;
   SOURCE database_sql/sample_data.sql;
   ```
   
   If `SOURCE` doesn't work, use full path:
   ```sql
   SOURCE /Users/YourName/Documents/CampusEventSystem/database_sql/schema.sql;
   SOURCE /Users/YourName/Documents/CampusEventSystem/database_sql/sample_data.sql;
   ```

4. **Verify tables were created**:
   ```sql
   SHOW TABLES;
   ```
   Should show: `users`, `events`, `resources`, `bookings`, etc.

5. **Exit MySQL**:
   ```sql
   EXIT;
   ```

✅ **Done!** Database is ready.

---

## 9. Configure Application

### Update Database Password

1. **Navigate to backend config**:
   ```bash
   cd backend_java/backend/src/main/resources
   ```

2. **Edit application.properties**:
   ```bash
   nano application.properties
   ```
   
   Or use your preferred editor:
   ```bash
   open -a TextEdit application.properties
   # Or
   code application.properties  # if you have VS Code
   ```

3. **Find and update this line**:
   
   **Change from**:
   ```properties
   spring.datasource.password=SAIAJAY@2005
   ```
   
   **To** (use YOUR MySQL root password):
   ```properties
   spring.datasource.password=YOUR_MYSQL_ROOT_PASSWORD
   ```

4. **Save the file**:
   - If using nano: Press `Ctrl + X`, then `Y`, then Enter
   - If using TextEdit: `Cmd + S`

5. **Return to project root**:
   ```bash
   cd ~/Documents/CampusEventSystem
   ```

✅ **Done!** Configuration updated.

---

## 10. Install Dependencies

### Backend Dependencies

1. **Navigate to backend**:
   ```bash
   cd backend_java/backend
   ```

2. **Build with Maven** (downloads dependencies):
   ```bash
   mvn clean install
   ```
   
   First time takes 3-5 minutes. You should see: `BUILD SUCCESS`

### Frontend Dependencies

3. **Navigate to frontend**:
   ```bash
   cd ../../frontend_tkinter
   ```

4. **Install Python packages**:
   ```bash
   pip3.11 install -r requirements.txt
   ```
   
   Or if you set up the alias:
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs all required packages.

5. **Return to project root**:
   ```bash
   cd ..
   ```

✅ **Done!** All dependencies installed.

---

## 11. Run the Application

### Option A: Quick Start Script (Recommended)

From the project root:

```bash
chmod +x run.sh  # Make script executable (first time only)
./run.sh
```

This will:
- Start the backend
- Wait for it to be ready
- Start the frontend
- Show you the status

**To stop everything**:
```bash
./stop.sh
```

### Option B: Manual Start (2 Terminal Windows)

**Terminal 1 - Backend:**

```bash
cd ~/Documents/CampusEventSystem/backend_java/backend
mvn spring-boot:run
```

Wait until you see:
```
Started CampusEventSystemApplication in X.XXX seconds
```

**Keep this terminal open!**

**Terminal 2 - Frontend:**

Open a NEW terminal window:

```bash
cd ~/Documents/CampusEventSystem/frontend_tkinter
python3.11 main.py
```

The GUI application should open!

### Test the Application

1. **Login with test account**:
   - Email: `admin@campus.com`
   - Password: `test123`

2. **Explore the features**!

✅ **Success!** Application is running.

---

## 12. macOS-Specific Tips

### Python Version Management

macOS comes with Python 2.7 pre-installed. Always use `python3.11`:

```bash
# Check versions
python --version    # System Python (probably 2.7)
python3 --version   # Default Python 3
python3.11 --version  # Our installed version

# Always use python3.11 for this project
python3.11 main.py
pip3.11 install <package>
```

### Fixing "App Can't Be Opened" Error

If macOS blocks the app from running:

1. Go to **System Preferences** → **Security & Privacy**
2. You'll see a message about blocked software
3. Click **"Open Anyway"**

Or disable Gatekeeper temporarily:
```bash
sudo spctl --master-disable
# Run your app
sudo spctl --master-enable  # Re-enable after
```

### macOS Button Appearance Issue

**Issue**: Buttons may appear grey due to macOS Big Sur+ changes.

**Solution**: Already fixed! The app uses Canvas-based buttons for consistent appearance. See `frontend_tkinter/MACOS_BUTTON_FIX.md` for details.

### Managing Processes

```bash
# Find what's using port 8080
lsof -i :8080

# Kill process on port 8080
lsof -ti:8080 | xargs kill -9

# Find Java processes
ps aux | grep java

# Kill all Java processes (careful!)
pkill -f java
```

### MySQL Management

```bash
# Start MySQL at login (optional)
brew services start mysql

# Stop MySQL service
brew services stop mysql

# MySQL data location
/opt/homebrew/var/mysql  # Apple Silicon
/usr/local/var/mysql     # Intel Macs
```

### Homebrew Maintenance

```bash
# Update Homebrew
brew update

# Upgrade installed packages
brew upgrade

# Clean up old versions
brew cleanup

# Check for issues
brew doctor
```

### Shell Configuration

macOS uses **zsh** by default (since Catalina). Configuration file:

```bash
# Edit your shell config
nano ~/.zshrc

# Reload configuration
source ~/.zshrc

# View current shell
echo $SHELL
```

### Useful Keyboard Shortcuts

- `Cmd + Space` → Spotlight (search apps, files)
- `Cmd + Tab` → Switch between apps
- `Cmd + ~` → Switch between windows of same app
- `Cmd + Q` → Quit application
- `Cmd + W` → Close window

### Recommended Tools

**Text Editors**:
- **TextEdit** (built-in)
- **Visual Studio Code**: `brew install --cask visual-studio-code`
- **Sublime Text**: `brew install --cask sublime-text`

**Database GUI**:
- **MySQL Workbench**: `brew install --cask mysqlworkbench`
- **Sequel Pro**: `brew install --cask sequel-pro` (free)

**Terminal Enhancements**:
- **iTerm2**: `brew install --cask iterm2`
- **Oh My Zsh**: https://ohmyz.sh/

---

## 🎉 You're Done!

### Quick Reference

| Component | Command to Start |
|-----------|------------------|
| **Backend** | `cd backend_java/backend && mvn spring-boot:run` |
| **Frontend** | `cd frontend_tkinter && python3.11 main.py` |
| **MySQL** | `brew services start mysql` |
| **Check Backend** | `curl http://localhost:8080/actuator/health` |

### Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@campus.com` | `test123` |
| Organizer | `organizer1@campus.com` | `test123` |
| Student | `student1@campus.com` | `test123` |

### Useful Commands

```bash
# Quick start everything
./run.sh

# Stop everything
./stop.sh

# Check status
./status.sh

# View backend logs
tail -f backend.log

# Restart MySQL
brew services restart mysql
```

### Next Steps

1. ✅ Change default passwords
2. ✅ Explore the application
3. ✅ Read [README.md](README.md) for features
4. ✅ Customize for your needs

---

## 🆘 Common macOS Issues

### Issue: "command not found: brew"

**Solution**: Homebrew not in PATH
```bash
# For Apple Silicon
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile

# For Intel Macs
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile
```

### Issue: "java: command not found"

**Solution**: Java not in PATH
```bash
# For Apple Silicon
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc

# For Intel Macs
echo 'export PATH="/usr/local/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc

source ~/.zshrc
```

### Issue: "Port 8080 already in use"

**Solution**: Kill the process
```bash
lsof -ti:8080 | xargs kill -9
```

### Issue: "MySQL won't start"

**Solutions**:

1. **Check status**:
   ```bash
   brew services list
   ```

2. **Restart MySQL**:
   ```bash
   brew services restart mysql
   ```

3. **Check logs**:
   ```bash
   tail -f /opt/homebrew/var/mysql/*.err
   ```

4. **Reinstall if needed**:
   ```bash
   brew services stop mysql
   brew uninstall mysql
   brew install mysql
   brew services start mysql
   ```

### Issue: "Permission denied" errors

**Solution**: Check file permissions
```bash
# Make scripts executable
chmod +x run.sh stop.sh status.sh

# Fix MySQL data directory (if needed)
sudo chown -R $(whoami) /opt/homebrew/var/mysql
```

### Issue: Python packages won't install

**Solution**: Upgrade pip first
```bash
pip3.11 install --upgrade pip
pip3.11 install -r requirements.txt
```

---

## 📚 Additional Resources

- **Homebrew Documentation**: https://docs.brew.sh/
- **MySQL on macOS**: https://dev.mysql.com/doc/mysql-getting-started/en/
- **Python.org**: https://www.python.org/downloads/macos/
- **Java on macOS**: https://adoptium.net/installation/macOS/

---

**Document Version**: 1.0  
**Platform**: macOS 10.15+  
**Last Updated**: November 4, 2025
