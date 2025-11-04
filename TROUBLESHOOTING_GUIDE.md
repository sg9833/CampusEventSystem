# 🔧 Comprehensive Troubleshooting Guide

**This guide helps you resolve common issues when setting up or running the Campus Event System.**

---

## 📋 Quick Diagnostic Checklist

Before diving into specific issues, run through this checklist:

- [ ] Java 17+ is installed: `java -version`
- [ ] Maven 3.8+ is installed: `mvn -version`
- [ ] Python 3.11+ is installed: `python --version` or `python3.11 --version`
- [ ] MySQL 8.0+ is running: `mysql --version`
- [ ] Database `campusdb` exists and has tables
- [ ] Backend configuration has correct MySQL password
- [ ] Port 8080 is available
- [ ] Port 3306 (MySQL) is available
- [ ] Internet connection is working (for first-time setup)

---

## 🔍 Common Issues by Category

### 🗄️ Database Issues

#### Issue 1: "Can't connect to MySQL server"

**Symptoms**:
- Backend fails to start
- Error: `CommunicationsException: Communications link failure`

**Causes**:
1. MySQL is not running
2. Wrong port (not 3306)
3. Incorrect password
4. Database doesn't exist

**Solutions**:

**Check if MySQL is running:**

Windows:
```cmd
# Check service
sc query MySQL80

# Start if stopped
net start MySQL80
```

macOS:
```bash
brew services list
brew services start mysql
```

Linux:
```bash
sudo systemctl status mysql
sudo systemctl start mysql
```

**Test MySQL connection:**
```bash
mysql -u root -p
```

**Verify database exists:**
```sql
SHOW DATABASES;
USE campusdb;
SHOW TABLES;
```

**Check port:**
```sql
SHOW VARIABLES LIKE 'port';
```

**Fix password in application.properties:**
```properties
# backend_java/backend/src/main/resources/application.properties
spring.datasource.password=YOUR_ACTUAL_MYSQL_PASSWORD
```

---

#### Issue 2: "Unknown database 'campusdb'"

**Solution**: Create the database

```bash
mysql -u root -p
```

```sql
CREATE DATABASE campusdb;
USE campusdb;
SOURCE /path/to/database_sql/schema.sql;
SOURCE /path/to/database_sql/sample_data.sql;
EXIT;
```

---

#### Issue 3: "Table doesn't exist"

**Solution**: Reload the schema

```bash
mysql -u root -p campusdb
```

```sql
DROP DATABASE campusdb;
CREATE DATABASE campusdb;
USE campusdb;
SOURCE /path/to/database_sql/schema.sql;
SOURCE /path/to/database_sql/sample_data.sql;
EXIT;
```

---

#### Issue 4: "Access denied for user 'root'@'localhost'"

**Solutions**:

1. **Wrong password**: Double-check the password in `application.properties`

2. **Reset MySQL root password**:

   macOS/Linux:
   ```bash
   sudo mysql
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
   FLUSH PRIVILEGES;
   EXIT;
   ```

   Windows:
   ```cmd
   mysql -u root
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
   FLUSH PRIVILEGES;
   EXIT;
   ```

---

### ☕ Java/Backend Issues

#### Issue 5: "java: command not found"

**Solution**: Java is not installed or not in PATH

**Verify installation:**
```bash
java -version
```

**Install Java** (if missing):

Windows:
- Download from https://adoptium.net/
- During install, check "Add to PATH"

macOS:
```bash
brew install openjdk@17
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Linux:
```bash
sudo apt update
sudo apt install openjdk-17-jdk
```

**Manually add to PATH** (Windows):
1. Find Java installation (e.g., `C:\Program Files\Java\jdk-17`)
2. Add `C:\Program Files\Java\jdk-17\bin` to System PATH
3. Restart Command Prompt

---

#### Issue 6: "mvn: command not found"

**Solution**: Maven is not installed or not in PATH

**Verify installation:**
```bash
mvn -version
```

**Install Maven**:

Windows:
- Download from https://maven.apache.org/download.cgi
- Extract to `C:\Program Files\Apache\maven`
- Add `C:\Program Files\Apache\maven\bin` to PATH

macOS:
```bash
brew install maven
```

Linux:
```bash
sudo apt update
sudo apt install maven
```

**Alternative**: Use Maven Wrapper (included in project):

```bash
cd backend_java/backend

# macOS/Linux
./mvnw spring-boot:run

# Windows
mvnw.cmd spring-boot:run
```

---

#### Issue 7: "Port 8080 is already in use"

**Symptoms**:
- Backend fails to start
- Error: `Port 8080 was already in use`

**Solution**: Kill the process using port 8080

**Windows:**
```cmd
# Find process
netstat -ano | findstr :8080

# Kill process (replace PID)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Find and kill
lsof -ti:8080 | xargs kill -9

# Or find first, then kill
lsof -i:8080
kill -9 <PID>
```

**Change port** (alternative):

Edit `backend_java/backend/src/main/resources/application.properties`:
```properties
server.port=8081  # Or any available port
```

Also update frontend config:
```python
# frontend_tkinter/config.py
API_BASE_URL = "http://localhost:8081/api"
```

---

#### Issue 8: "Maven build fails"

**Symptoms**:
- `mvn clean install` fails
- Dependency download errors

**Solutions**:

1. **Check internet connection** (Maven downloads dependencies)

2. **Clear Maven cache**:
   ```bash
   cd backend_java/backend
   mvn clean
   rm -rf ~/.m2/repository
   mvn clean install -U
   ```

3. **Check Maven settings**:
   ```bash
   mvn -version
   ```
   Verify Java version is 17+

4. **Use Maven Wrapper**:
   ```bash
   ./mvnw clean install  # macOS/Linux
   mvnw.cmd clean install  # Windows
   ```

5. **Check for proxy issues** (if behind corporate firewall):
   
   Edit `~/.m2/settings.xml`:
   ```xml
   <settings>
     <proxies>
       <proxy>
         <id>myproxy</id>
         <active>true</active>
         <protocol>http</protocol>
         <host>proxy.company.com</host>
         <port>8080</port>
       </proxy>
     </proxies>
   </settings>
   ```

---

#### Issue 9: Backend starts but crashes immediately

**Solution**: Check backend logs

```bash
# In the backend directory
cat backend.log
# or
tail -f backend.log
```

**Common causes**:
- Database connection error (check MySQL)
- Missing configuration
- Port already in use
- Invalid application.properties

**Check application.properties**:
- Correct database URL
- Correct username/password
- Valid JWT secret

---

### 🐍 Python/Frontend Issues

#### Issue 10: "python: command not found"

**Solution**: Python is not installed or not in PATH

**Verify installation:**
```bash
python --version
python3 --version
python3.11 --version
```

**Install Python**:

Windows:
- Download from https://www.python.org/downloads/
- **Must check** "Add Python to PATH" during installation

macOS:
```bash
brew install python@3.11
```

Linux:
```bash
sudo apt update
sudo apt install python3.11
```

---

#### Issue 11: "ModuleNotFoundError: No module named 'requests'"

**Solution**: Python dependencies not installed

```bash
cd frontend_tkinter
pip install -r requirements.txt

# Or on macOS/Linux
pip3 install -r requirements.txt
pip3.11 install -r requirements.txt
```

**Upgrade pip first**:
```bash
pip install --upgrade pip
```

**Force reinstall**:
```bash
pip install -r requirements.txt --force-reinstall
```

---

#### Issue 12: Frontend window is blank or crashes

**Symptoms**:
- GUI opens but shows nothing
- Immediate crash on startup
- Error about tkinter

**Solutions**:

1. **Check Python version** (must be 3.11+):
   ```bash
   python --version
   ```

2. **Install tkinter** (if missing):
   
   **macOS:**
   ```bash
   brew install python-tk@3.11
   ```
   
   **Linux:**
   ```bash
   sudo apt install python3-tk
   ```
   
   **Windows:** Tkinter is included with Python installer

3. **Check backend is running**:
   ```bash
   curl http://localhost:8080/actuator/health
   ```

4. **Check frontend logs**:
   ```bash
   cd frontend_tkinter
   python main.py 2>&1 | tee frontend.log
   ```

5. **Reinstall dependencies**:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

---

#### Issue 13: "Connection refused" in frontend

**Symptoms**:
- Can't login
- Error: "Failed to connect to backend"

**Solutions**:

1. **Verify backend is running**:
   ```bash
   curl http://localhost:8080/actuator/health
   ```
   Should return: `{"status":"UP"}`

2. **Check firewall**:
   - Windows: Allow Java through Windows Firewall
   - macOS: System Preferences → Security & Privacy → Firewall
   - Linux: `sudo ufw allow 8080`

3. **Verify API URL in config**:
   ```python
   # frontend_tkinter/config.py
   API_BASE_URL = "http://localhost:8080/api"
   ```

4. **Test API manually**:
   ```bash
   curl http://localhost:8080/api/events
   ```

---

#### Issue 14: Buttons appear grey on macOS

**Solution**: Already fixed in the codebase!

The application uses Canvas-based buttons for consistent appearance across all macOS versions.

If you still see issues:
1. Check you're on the latest code
2. See `frontend_tkinter/MACOS_BUTTON_FIX.md`

---

### 🌐 Network/Connection Issues

#### Issue 15: "Connection timeout" errors

**Solutions**:

1. **Check if backend is actually running**:
   ```bash
   # Should show Java process
   # macOS/Linux:
   ps aux | grep java
   
   # Windows:
   tasklist | findstr java
   ```

2. **Check port is listening**:
   ```bash
   # macOS/Linux:
   lsof -i:8080
   
   # Windows:
   netstat -ano | findstr :8080
   ```

3. **Test localhost**:
   ```bash
   ping localhost
   curl http://localhost:8080
   ```

4. **Disable VPN** (temporarily) - VPNs can block localhost

5. **Check hosts file**:
   
   Windows: `C:\Windows\System32\drivers\etc\hosts`
   macOS/Linux: `/etc/hosts`
   
   Should have:
   ```
   127.0.0.1 localhost
   ```

---

### 🔐 Authentication/Login Issues

#### Issue 16: "Invalid credentials" when logging in

**Solutions**:

1. **Use default test accounts**:
   - Email: `admin@campus.com`
   - Password: `test123`

2. **Verify users exist in database**:
   ```bash
   mysql -u root -p campusdb
   ```
   ```sql
   SELECT * FROM users;
   ```

3. **Reload sample data**:
   ```sql
   SOURCE /path/to/database_sql/sample_data.sql;
   ```

4. **Check password hashing**:
   - Passwords should be BCrypt hashed
   - Sample data includes pre-hashed passwords

---

#### Issue 17: "403 Forbidden" or "401 Unauthorized"

**Symptoms**:
- Can login but can't access features
- API returns 403/401 errors

**Solutions**:

1. **Check user role**:
   ```sql
   SELECT email, role FROM users WHERE email = 'your@email.com';
   ```

2. **Verify JWT token is included in requests**:
   - Check browser developer console (Network tab)
   - Authorization header should be present

3. **Check JWT secret**:
   ```properties
   # application.properties
   jwt.secret=your-256-bit-secret-key...
   ```

4. **Clear application cache** and login again

---

### 💾 Data/Performance Issues

#### Issue 18: Application is slow

**Solutions**:

1. **Check database connections**:
   ```sql
   SHOW PROCESSLIST;
   ```

2. **Optimize database**:
   ```sql
   OPTIMIZE TABLE users, events, bookings, resources;
   ```

3. **Increase connection pool**:
   ```properties
   # application.properties
   spring.datasource.hikari.maximum-pool-size=20
   ```

4. **Check system resources**:
   ```bash
   # macOS/Linux
   top
   
   # Windows
   taskmgr
   ```

---

#### Issue 19: "Out of memory" errors

**Solutions**:

1. **Increase JVM heap**:
   ```bash
   # When starting backend
   mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Xmx2048m"
   ```

2. **For packaged JAR**:
   ```bash
   java -Xmx2048m -jar backend-0.0.1-SNAPSHOT.jar
   ```

3. **Close unnecessary applications**

---

### 🖥️ Platform-Specific Issues

#### macOS: "Operation not permitted"

**Solution**: Grant permissions

1. System Preferences → Security & Privacy → Privacy
2. Full Disk Access → Add Terminal/iTerm
3. Restart terminal

---

#### macOS: Homebrew issues

**Solution**: Update and fix

```bash
brew update
brew doctor
brew upgrade
```

---

#### Windows: PowerShell execution policy

**Solution**: Allow script execution

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

#### Linux: Permission denied

**Solution**: Fix file permissions

```bash
chmod +x run.sh stop.sh
chmod +x backend_java/backend/mvnw
```

---

## 🧪 Testing Your Setup

### Health Check Commands

```bash
# 1. Check Java
java -version

# 2. Check Maven
mvn -version

# 3. Check Python
python --version

# 4. Check MySQL
mysql --version
mysql -u root -p -e "SHOW DATABASES;"

# 5. Check backend (while running)
curl http://localhost:8080/actuator/health

# 6. Check API
curl http://localhost:8080/api/events

# 7. Check ports
# macOS/Linux:
lsof -i:8080
lsof -i:3306

# Windows:
netstat -ano | findstr :8080
netstat -ano | findstr :3306
```

---

## 📞 Getting Additional Help

### Collecting Information for Support

If you need help, collect this information:

1. **System Info**:
   ```bash
   # macOS/Linux
   uname -a
   
   # Windows
   systeminfo
   ```

2. **Software Versions**:
   ```bash
   java -version
   mvn -version
   python --version
   mysql --version
   ```

3. **Backend Logs**:
   ```bash
   cat backend_java/backend/backend.log
   ```

4. **Frontend Errors**:
   - Copy any error messages from terminal

5. **Database State**:
   ```sql
   SHOW DATABASES;
   USE campusdb;
   SHOW TABLES;
   SELECT COUNT(*) FROM users;
   ```

### Log Locations

- **Backend**: `backend_java/backend/backend.log`
- **Frontend**: Terminal output or `frontend.log`
- **MySQL**: Varies by OS
  - macOS: `/opt/homebrew/var/mysql/*.err`
  - Windows: MySQL data directory
  - Linux: `/var/log/mysql/error.log`

---

## ✅ Preventive Measures

### Before Making Changes

1. **Backup database**:
   ```bash
   mysqldump -u root -p campusdb > backup.sql
   ```

2. **Commit code changes** (if using Git):
   ```bash
   git add .
   git commit -m "Before making changes"
   ```

3. **Test in development** before production

### Regular Maintenance

```bash
# Update packages
pip install --upgrade -r requirements.txt

# Update Homebrew packages (macOS)
brew update && brew upgrade

# Clean Maven cache (if issues)
mvn clean

# Optimize database
mysql -u root -p campusdb -e "OPTIMIZE TABLE users, events, bookings, resources;"
```

---

## 🎯 Still Having Issues?

If you've tried everything:

1. ✅ Check this guide thoroughly
2. ✅ Review [CLIENT_SETUP_GUIDE.md](CLIENT_SETUP_GUIDE.md)
3. ✅ Read platform-specific guides:
   - [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md)
   - [MACOS_SETUP_GUIDE.md](MACOS_SETUP_GUIDE.md)
4. ✅ Try setup on a different machine (to isolate issues)
5. ✅ Check GitHub Issues (if repository is public)

---

**Document Version**: 1.0  
**Last Updated**: November 4, 2025  
**Covers**: Windows, macOS, Linux
