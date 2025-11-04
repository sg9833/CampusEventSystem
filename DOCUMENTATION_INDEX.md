# 📚 Documentation Index - Campus Event System

**Your complete guide to setting up and running the Campus Event System**

---

## 🎯 Start Here

### For New Clients (First Time Setup)

**Follow these documents in order:**

1. **[CLEANUP_BEFORE_SETUP.md](CLEANUP_BEFORE_SETUP.md)** ⚠️ **MANDATORY FIRST STEP**
   - Delete unnecessary developer files
   - Edit configuration with YOUR passwords
   - Estimated time: 10-15 minutes
   - **YOU MUST DO THIS BEFORE ANYTHING ELSE!**

2. **[CLIENT_SETUP_GUIDE.md](CLIENT_SETUP_GUIDE.md)** ⭐ **THEN DO THIS**
   - Complete step-by-step setup for beginners
   - Works for both Windows and macOS
   - Estimated time: 60-75 minutes

3. **Choose Your Platform (Optional - for more details):**
   - **Windows users**: [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md)
   - **macOS users**: [MACOS_SETUP_GUIDE.md](MACOS_SETUP_GUIDE.md)
   
   These provide platform-specific detailed instructions.

4. **Having Issues?** → [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)

---

## 📖 All Documentation

### Setup & Installation

| Document | Purpose | Who Needs It |
|----------|---------|--------------|
| **[CLIENT_SETUP_GUIDE.md](CLIENT_SETUP_GUIDE.md)** | Main setup guide for new clients | ⭐ Everyone (start here) |
| **[WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md)** | Windows-specific detailed instructions | Windows users |
| **[MACOS_SETUP_GUIDE.md](MACOS_SETUP_GUIDE.md)** | macOS-specific detailed instructions | Mac users |
| **[TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)** | Solutions to common problems | When you have issues |

### Preparation (For Sellers)

| Document | Purpose | Who Needs It |
|----------|---------|--------------|
| **[CLEAN_FOR_CLIENT.md](CLEAN_FOR_CLIENT.md)** | How to prepare repository for delivery | Sellers only |

### Usage & Reference

| Document | Purpose | Who Needs It |
|----------|---------|--------------|
| **[README.md](README.md)** | Feature overview, API documentation | Everyone (reference) |
| **[STARTUP_GUIDE.md](STARTUP_GUIDE.md)** | Daily usage, how to start/stop app | Everyone (daily use) |

---

## 🗺️ Setup Journey Map

```
┌─────────────────────────────────────────────────────────┐
│  START: You just purchased/received the project         │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  READ: CLIENT_SETUP_GUIDE.md                            │
│  • Understand what you're getting                       │
│  • Check system requirements                            │
│  • See overview of installation steps                   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
                  Are you on...
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
┌──────────────────┐          ┌──────────────────┐
│  Windows 10/11?  │          │     macOS?       │
│  ↓               │          │     ↓            │
│  READ:           │          │  READ:           │
│  WINDOWS_SETUP   │          │  MACOS_SETUP     │
│  _GUIDE.md       │          │  _GUIDE.md       │
└──────────────────┘          └──────────────────┘
         │                               │
         └───────────────┬───────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│  INSTALL: All required software                         │
│  • Java 17                                              │
│  • Maven 3.8+                                           │
│  • Python 3.11                                          │
│  • MySQL 8.0                                            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  SETUP: Database and configuration                      │
│  • Create campusdb database                             │
│  • Load schema and sample data                          │
│  • Configure application.properties                     │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  RUN: Start the application                             │
│  • Backend: mvn spring-boot:run                         │
│  • Frontend: python main.py                             │
│  • Login with test accounts                             │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  SUCCESS! Application is running                        │
│  • Explore features                                     │
│  • Read README.md for full documentation                │
│  • Customize for your needs                             │
└─────────────────────────────────────────────────────────┘
                         │
                  Having issues?
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  HELP: TROUBLESHOOTING_GUIDE.md                         │
│  • Common issues and solutions                          │
│  • Platform-specific fixes                              │
│  • Diagnostic commands                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Quick Setup Cheat Sheet

### ⚡ For Experienced Developers

If you're familiar with Java/Python/MySQL development:

```bash
# 1. Install prerequisites
# - Java 17+, Maven 3.8+, Python 3.11+, MySQL 8.0+

# 2. Clone repository
git clone <repository-url>
cd CampusEventSystem

# 3. Setup database
mysql -u root -p
CREATE DATABASE campusdb;
USE campusdb;
SOURCE database_sql/schema.sql;
SOURCE database_sql/sample_data.sql;
EXIT;

# 4. Configure backend
# Edit: backend_java/backend/src/main/resources/application.properties
# Update: spring.datasource.password=YOUR_PASSWORD

# 5. Install dependencies
cd backend_java/backend
mvn clean install
cd ../../frontend_tkinter
pip install -r requirements.txt

# 6. Run (in separate terminals)
# Terminal 1:
cd backend_java/backend
mvn spring-boot:run

# Terminal 2:
cd frontend_tkinter
python3.11 main.py

# 7. Login
# Email: admin@campus.com
# Password: test123
```

---

## 🎓 Learning Path

### Day 1: Setup
- [ ] Read CLIENT_SETUP_GUIDE.md
- [ ] Install all software
- [ ] Set up database
- [ ] Run the application
- [ ] Test with admin account

### Day 2: Explore
- [ ] Read README.md
- [ ] Try all three user roles (Admin, Organizer, Student)
- [ ] Create test events
- [ ] Book resources
- [ ] Test approval workflows

### Day 3: Understand
- [ ] Explore database structure
- [ ] Read API documentation in README.md
- [ ] Test API endpoints with curl
- [ ] Understand authentication (JWT)

### Day 4: Customize
- [ ] Change default passwords
- [ ] Add your own data
- [ ] Customize frontend (images, colors)
- [ ] Configure email notifications (optional)

### Week 2+: Deploy
- [ ] Plan production deployment
- [ ] Set up secure passwords
- [ ] Configure production database
- [ ] Test thoroughly
- [ ] Document your changes

---

## 🔍 Finding Specific Information

### "How do I install...?"
→ Platform-specific guide (WINDOWS_SETUP_GUIDE.md or MACOS_SETUP_GUIDE.md)

### "Something isn't working"
→ TROUBLESHOOTING_GUIDE.md

### "How do I use the API?"
→ README.md (API Testing section)

### "How do I start the app daily?"
→ STARTUP_GUIDE.md

### "What features are available?"
→ README.md (Features section)

### "I'm preparing to sell/deliver this"
→ CLEAN_FOR_CLIENT.md

### "Error with database"
→ TROUBLESHOOTING_GUIDE.md → Database Issues

### "Port 8080 in use"
→ TROUBLESHOOTING_GUIDE.md → Network Issues

### "Can't login"
→ TROUBLESHOOTING_GUIDE.md → Authentication Issues

---

## 📊 Documentation Comparison

### CLIENT_SETUP_GUIDE.md
- **Level**: Beginner
- **Length**: Comprehensive (~8,000 words)
- **Covers**: Both Windows and macOS
- **Best for**: First-time setup, complete beginners

### WINDOWS_SETUP_GUIDE.md
- **Level**: Beginner to Intermediate
- **Length**: Detailed (~6,000 words)
- **Covers**: Windows 10/11 only
- **Best for**: Windows users who want step-by-step instructions

### MACOS_SETUP_GUIDE.md
- **Level**: Beginner to Intermediate
- **Length**: Detailed (~5,500 words)
- **Covers**: macOS 10.15+ only
- **Best for**: Mac users, includes Homebrew setup

### TROUBLESHOOTING_GUIDE.md
- **Level**: All levels
- **Length**: Comprehensive (~5,000 words)
- **Covers**: All platforms
- **Best for**: When you have problems

### README.md
- **Level**: Intermediate to Advanced
- **Length**: Extensive (~10,000 words)
- **Covers**: Features, API, architecture
- **Best for**: Understanding the system, API reference

---

## 💡 Tips for Success

### ✅ Do This

1. **Follow the guides in order** - Don't skip ahead
2. **Copy commands exactly** - Small typos can cause errors
3. **Write down passwords** - You'll need them!
4. **Check prerequisites** - Ensure software versions match
5. **Read error messages** - They often tell you what's wrong
6. **Use the troubleshooting guide** - Most issues are covered

### ❌ Avoid This

1. **Don't skip steps** - Each step is important
2. **Don't mix guides** - Choose one and stick with it
3. **Don't use old software versions** - Use Java 17+, not Java 8
4. **Don't ignore warnings** - Address them before continuing
5. **Don't forget to save changes** - Save config files!

---

## 🆘 Support Resources

### Built-in Help

1. **Test accounts** - Pre-configured for testing
2. **Sample data** - Example events, resources, users
3. **Startup scripts** - Automated start/stop (run.sh, stop.sh)
4. **Health checks** - Verify services are running

### Documentation Structure

```
CampusEventSystem/
├── CLIENT_SETUP_GUIDE.md          ⭐ START HERE
├── WINDOWS_SETUP_GUIDE.md         (Windows users)
├── MACOS_SETUP_GUIDE.md           (Mac users)
├── TROUBLESHOOTING_GUIDE.md       (When issues arise)
├── CLEAN_FOR_CLIENT.md            (Sellers only)
├── README.md                      (Reference, features, API)
├── STARTUP_GUIDE.md               (Daily usage)
└── documentaries/                 (Internal dev notes)
    └── ... (many detailed docs)
```

---

## 📞 Common Questions

**Q: Which guide should I read first?**  
A: Start with CLIENT_SETUP_GUIDE.md

**Q: I'm on Windows, do I need the Windows guide?**  
A: The CLIENT_SETUP_GUIDE covers both platforms. Use WINDOWS_SETUP_GUIDE for more detailed Windows-specific instructions.

**Q: Where are the test account passwords?**  
A: All test accounts use password: `test123`

**Q: How long does setup take?**  
A: 30-60 minutes for complete setup

**Q: Can I skip the database setup?**  
A: No, the database is required for the application to work

**Q: Do I need to know programming?**  
A: No programming knowledge needed for setup. Just follow the guides.

**Q: What if I can't figure something out?**  
A: Check TROUBLESHOOTING_GUIDE.md - it covers most common issues

**Q: Can I customize the application?**  
A: Yes! Once it's running, you can modify code, add features, change styling, etc.

---

## 🎯 Success Checklist

After setup, you should be able to:

- [ ] Start backend successfully
- [ ] Start frontend successfully  
- [ ] Login with test accounts
- [ ] See the dashboard
- [ ] Browse events
- [ ] Create an event (as Organizer)
- [ ] Approve events (as Admin)
- [ ] Book resources
- [ ] View bookings
- [ ] Access all features based on role

---

## 📚 Additional Resources

### Inside the Repository

- **database_sql/** - Database schemas and sample data
- **backend_java/** - Java Spring Boot backend source
- **frontend_tkinter/** - Python Tkinter frontend source
- **documentaries/** - Detailed development notes (optional reading)

### External Resources

- **Java**: https://adoptium.net/
- **Maven**: https://maven.apache.org/
- **Python**: https://www.python.org/
- **MySQL**: https://dev.mysql.com/
- **Spring Boot**: https://spring.io/projects/spring-boot
- **Tkinter**: https://docs.python.org/3/library/tkinter.html

---

## 🔄 Keeping Updated

If you receive updates to the project:

1. **Backup your database**:
   ```bash
   mysqldump -u root -p campusdb > backup.sql
   ```

2. **Backup your config**:
   - Copy `application.properties`
   - Copy any custom changes

3. **Pull updates**:
   ```bash
   git pull
   ```

4. **Rebuild**:
   ```bash
   cd backend_java/backend
   mvn clean install
   cd ../../frontend_tkinter
   pip install -r requirements.txt --upgrade
   ```

5. **Restore your config** if needed

---

## 🎉 You're Ready!

You now have all the documentation you need to:

✅ Set up the Campus Event System  
✅ Run it on your machine  
✅ Troubleshoot any issues  
✅ Understand all features  
✅ Customize for your needs  

**Start with [CLIENT_SETUP_GUIDE.md](CLIENT_SETUP_GUIDE.md) and you'll be up and running in about an hour!**

---

**Document Version**: 1.0  
**Last Updated**: November 4, 2025  
**Purpose**: Documentation index and navigation guide
