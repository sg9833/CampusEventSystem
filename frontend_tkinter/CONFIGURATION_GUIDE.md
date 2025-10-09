# 🔧 Configuration & Setup Guide
# Campus Event & Resource Coordination System v2.0.0

**Complete guide to configuring and running the application**

---

## 📋 Quick Start Checklist

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] config.ini reviewed
- [ ] .env file created (copy from .env.example)
- [ ] Backend API URL configured
- [ ] Logs directory created (auto-created)
- [ ] Cache directory created (auto-created)
- [ ] Run application: `python main.py`

---

## ⚙️ Configuration Files

### 1. config.ini (Main Configuration)

**Location:** `config.ini`

**Key Sections:**

```ini
[API]
base_url = http://localhost:8080/api
timeout = 30

[LOGGING]
level = INFO
log_dir = logs

[UI]
default_theme = light
window_width = 1200
window_height = 700

[CACHE]
enabled = true
ttl = 300
```

**Configuration Priority:**
1. Environment Variables (highest)
2. config.ini
3. Default values (lowest)

---

### 2. .env (Environment Variables)

**Setup:**
```bash
cp .env.example .env
nano .env
```

**Essential Variables:**
```bash
# Environment Type
ENVIRONMENT=development

# API Configuration
API_BASE_URL=http://localhost:8080/api

# Logging Level
LOG_LEVEL=INFO

# Security
SECRET_KEY=your-secret-key-here
```

**Environment-Specific Examples:**

**Development:**
```bash
ENVIRONMENT=development
API_BASE_URL=http://localhost:8080/api
LOG_LEVEL=DEBUG
DEBUG=true
VERBOSE_LOGGING=true
```

**Staging:**
```bash
ENVIRONMENT=staging
API_BASE_URL=https://staging-api.campusevents.edu/api
LOG_LEVEL=INFO
DEBUG=false
```

**Production:**
```bash
ENVIRONMENT=production
API_BASE_URL=https://api.campusevents.edu/api
LOG_LEVEL=WARNING
DEBUG=false
SECRET_KEY=secure-production-key-here
```

---

## 🚀 Running the Application

### Basic Run

```bash
python main.py
```

### With Environment Override

```bash
# Development mode
ENVIRONMENT=development python main.py

# Production mode with custom API
ENVIRONMENT=production API_BASE_URL=https://api.example.com/api python main.py

# Debug mode
LOG_LEVEL=DEBUG python main.py
```

### Using Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

## 📂 Directory Structure

### Auto-Created Directories

The following directories are created automatically:

```
frontend_tkinter/
├── logs/          # Log files (app.log, error.log, api.log, audit.log)
├── cache/         # Cache storage (local_cache.db, images)
└── config/        # Configuration storage (preferences.json)
```

### Manual Creation (Optional)

If needed, create manually:

```bash
mkdir -p logs cache config
chmod 755 logs cache config
```

---

## 📝 Logging Configuration

### Log Files

| File | Purpose | Level |
|------|---------|-------|
| `logs/app.log` | All application logs | INFO+ |
| `logs/error.log` | Errors only | ERROR+ |
| `logs/api.log` | API requests/responses | INFO+ |
| `logs/audit.log` | User actions | INFO+ |

### Log Levels

```ini
# config.ini
[LOGGING]
level = DEBUG    # All messages
level = INFO     # Info and above (recommended)
level = WARNING  # Warnings and above
level = ERROR    # Errors only
level = CRITICAL # Critical only
```

### Viewing Logs

```bash
# Real-time monitoring
tail -f logs/app.log

# View errors
tail -f logs/error.log

# Search logs
grep "ERROR" logs/app.log
grep "john_doe" logs/audit.log
```

### Log Rotation

- **Max File Size:** 10 MB per file
- **Backup Count:** 5 backups
- **Total Size:** ~60 MB per log type
- **Automatic rotation** when size limit reached

---

## 💾 Cache Configuration

### Cache Settings

```ini
[CACHE]
enabled = true
ttl = 300              # Time to live (5 minutes)
max_size = 50          # Max cache size (50 MB)
cache_dir = cache
```

### Cache Types

1. **API Response Cache**
   - Stores GET request responses
   - Default TTL: 5 minutes
   - Invalidated on POST/PUT/DELETE

2. **Image Cache**
   - Stores downloaded images
   - Max size: 100 MB
   - LRU eviction

3. **Database Cache**
   - SQLite for structured data
   - Auto-cleanup of expired entries

### Cache Management

```bash
# Check cache size
du -sh cache/

# Clear all cache
rm -rf cache/*

# Clear specific cache
rm cache/local_cache.db
```

---

## 🔐 Security Configuration

### Session Settings

```ini
[SECURITY]
session_timeout = 30          # Minutes
max_login_attempts = 5
lockout_duration = 15         # Minutes
csrf_protection = true
rate_limiting = true
password_encryption = true
```

### Secret Key

**Generate a secure secret key:**

```python
import secrets
secret_key = secrets.token_hex(32)
print(f"SECRET_KEY={secret_key}")
```

**Set in .env:**
```bash
SECRET_KEY=your-generated-key-here
```

---

## 🎨 UI Configuration

### Theme Settings

```ini
[UI]
default_theme = light        # light, dark, high_contrast
font_scale = 1.0             # 0.8 - 2.0
window_width = 1200
window_height = 700
animations_enabled = true
```

### Changing Theme

**Via config.ini:**
```ini
[UI]
default_theme = dark
```

**Via Environment:**
```bash
UI_DEFAULT_THEME=dark python main.py
```

**At Runtime:**
- Menu: View → Theme → [Light/Dark/High Contrast]
- Keyboard: `Ctrl+H` (toggle high contrast)

---

## ♿ Accessibility Configuration

### Settings

```ini
[ACCESSIBILITY]
enabled = true
keyboard_navigation = true
screen_reader = true
high_contrast_available = true
font_scaling = true
min_font_scale = 0.8
max_font_scale = 2.0
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt + Left/Right` | Navigate back/forward |
| `F1` | Show keyboard shortcuts |
| `Ctrl + +` | Increase font size |
| `Ctrl + -` | Decrease font size |
| `Ctrl + 0` | Reset font size |
| `Ctrl + H` | Toggle high contrast |
| `Tab` | Navigate between elements |
| `Enter` | Activate focused element |
| `Escape` | Close dialogs |

---

## 🔌 API Configuration

### Backend Setup

**1. Ensure backend is running:**
```bash
# Check backend health
curl http://localhost:8080/api/health
```

**2. Configure frontend:**

**Option 1: Environment Variable (Recommended)**
```bash
export API_BASE_URL=http://localhost:8080/api
python main.py
```

**Option 2: config.ini**
```ini
[API]
base_url = http://localhost:8080/api
timeout = 30
```

**Option 3: .env file**
```bash
API_BASE_URL=http://localhost:8080/api
```

### API Settings

```ini
[API]
base_url = http://localhost:8080/api
timeout = 30              # Request timeout (seconds)
retry_attempts = 3        # Retry failed requests
retry_delay = 1           # Delay between retries (seconds)
```

### Testing API Connection

```python
# Test script
python -c "
from config import config
print(f'API URL: {config.get_api_base_url()}')
print(f'Environment: {config.get_environment()}')
"
```

---

## 🧪 Development Configuration

### Development Mode

```ini
[DEVELOPMENT]
debug = true
show_performance_metrics = true
verbose_logging = true
hot_reload = false
```

### Enable Development Features

```bash
# .env file
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
VERBOSE_LOGGING=true
```

---

## 📊 Performance Configuration

### Settings

```ini
[PERFORMANCE]
lazy_loading = true
performance_monitoring = true
page_size = 20
image_cache_size = 100
async_image_loading = true
```

### Tuning for Low-End Devices

```ini
[PERFORMANCE]
lazy_loading = true
animations_enabled = false
image_cache_size = 50
page_size = 10

[CACHE]
max_size = 25
```

### Tuning for High-End Devices

```ini
[PERFORMANCE]
lazy_loading = true
animations_enabled = true
image_cache_size = 200
page_size = 50

[CACHE]
max_size = 100
```

---

## 🔔 Notification Configuration

### Settings

```ini
[NOTIFICATIONS]
desktop_notifications = true
in_app_notifications = true
check_interval = 60          # Seconds
retention_days = 30
```

---

## 📖 Configuration Examples

### Example 1: Local Development

```ini
# config.ini
[ENVIRONMENT]
environment = development

[API]
base_url = http://localhost:8080/api
timeout = 30

[LOGGING]
level = DEBUG

[DEVELOPMENT]
debug = true
verbose_logging = true
```

```bash
# .env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DEBUG=true
```

### Example 2: Production Deployment

```ini
# config.ini
[ENVIRONMENT]
environment = production

[API]
base_url = https://api.campusevents.edu/api
timeout = 30
retry_attempts = 3

[LOGGING]
level = WARNING

[DEVELOPMENT]
debug = false
verbose_logging = false

[SECURITY]
session_timeout = 30
csrf_protection = true
rate_limiting = true
```

```bash
# .env
ENVIRONMENT=production
API_BASE_URL=https://api.campusevents.edu/api
LOG_LEVEL=WARNING
DEBUG=false
SECRET_KEY=production-secret-key-here
```

### Example 3: Staging Server

```ini
# config.ini
[ENVIRONMENT]
environment = staging

[API]
base_url = https://staging-api.campusevents.edu/api

[LOGGING]
level = INFO
```

```bash
# .env
ENVIRONMENT=staging
API_BASE_URL=https://staging-api.campusevents.edu/api
LOG_LEVEL=INFO
```

---

## 🛠️ Troubleshooting Configuration

### Issue: Configuration not loading

**Check:**
1. config.ini exists in project root
2. File permissions: `chmod 644 config.ini`
3. No syntax errors in INI file
4. Check logs: `grep CONFIG logs/app.log`

### Issue: Environment variables not working

**Check:**
1. .env file exists and is named correctly (not .env.txt)
2. Export variables: `export API_BASE_URL=...`
3. Verify: `echo $API_BASE_URL`
4. Check priority: ENV vars override config.ini

### Issue: Logs not created

**Check:**
1. Logs directory exists: `ls -la logs/`
2. Write permissions: `chmod 755 logs/`
3. LOG_LEVEL is set
4. Check console for errors

### Issue: Cache not working

**Check:**
1. CACHE_ENABLED=true in config
2. Cache directory exists: `ls -la cache/`
3. Sufficient disk space: `df -h`
4. Check cache size: `du -sh cache/`

---

## 📚 Configuration API Usage

### Python Code Examples

**Loading configuration:**
```python
from config import config

# Get API URL
api_url = config.get_api_base_url()

# Get log level
log_level = config.get_log_level()

# Get environment
env = config.get_environment()

# Check environment
if config.is_production():
    # Production code
    pass
elif config.is_development():
    # Development code
    pass
```

**Getting specific values:**
```python
# Get string value
theme = config.get('UI', 'default_theme', 'light')

# Get integer
timeout = config.get_int('API', 'timeout', 30)

# Get float
font_scale = config.get_float('UI', 'font_scale', 1.0)

# Get boolean
debug = config.get_bool('DEVELOPMENT', 'debug', False)

# Get entire section
api_config = config.get_section('API')
```

---

## ✅ Configuration Validation

### Validation Script

```python
# validate_config.py

from config import config
import os

print("=" * 60)
print("Configuration Validation")
print("=" * 60)

# Check environment
print(f"Environment: {config.get_environment()}")

# Check API
api_url = config.get_api_base_url()
print(f"API URL: {api_url}")

# Check directories
print(f"\nDirectories:")
print(f"  logs/: {'✓' if os.path.exists('logs') else '✗'}")
print(f"  cache/: {'✓' if os.path.exists('cache') else '✗'}")
print(f"  config/: {'✓' if os.path.exists('config') else '✗'}")

# Check log level
log_level = config.get_log_level()
print(f"\nLog Level: {log_level}")

# Check cache
cache_enabled = config.get_bool('CACHE', 'enabled')
print(f"Cache Enabled: {cache_enabled}")

print("\n" + "=" * 60)
print("Validation Complete")
print("=" * 60)
```

**Run:**
```bash
python validate_config.py
```

---

## 📞 Support

For configuration issues:

1. Check this guide
2. Review logs: `logs/app.log`, `logs/error.log`
3. Check environment: `python validate_config.py`
4. Contact support: support@campusevents.edu

---

**Configuration Guide v2.0.0**  
*Campus Event & Resource Coordination System*
