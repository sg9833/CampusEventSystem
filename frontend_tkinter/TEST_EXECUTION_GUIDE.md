# 🧪 Test Execution Guide
# Campus Event & Resource Coordination System v2.0.0

## 🎯 Quick Start for QA Team

This guide walks you through executing all 24 test cases documented in `TEST_CASES.md`.

---

## 📋 Pre-Testing Checklist

### ✅ Environment Setup

**Step 1: Verify Backend is Running**
```bash
# Navigate to backend directory
cd /Users/garinesaiajay/Desktop/CampusEventSystem/backend_java/backend

# Start backend server
mvn spring-boot:run

# Verify server is up
# Should see: "Application started on port 8080"
```

**Step 2: Verify Database is Populated**
```bash
# Check if sample data exists
cd /Users/garinesaiajay/Desktop/CampusEventSystem/database_sql

# If needed, run:
# mysql -u root -p campus_events < schema.sql
# mysql -u root -p campus_events < sample_data.sql
```

**Step 3: Setup Frontend Environment**
```bash
# Navigate to frontend
cd /Users/garinesaiajay/Desktop/CampusEventSystem/frontend_tkinter

# Verify Python environment
python --version  # Should be Python 3.8+

# Install/verify dependencies
pip install -r requirements.txt

# Verify config file exists
ls -la config.ini
```

**Step 4: Create Test Accounts (if not exist)**

You need 3 test accounts:
- **Student:** `student@test.com` / `Student123!`
- **Organizer:** `organizer@test.com` / `Organizer123!`
- **Admin:** `admin@test.com` / `Admin123!`

---

## 🚀 Test Execution Order

### Phase 1: Critical Path (High Priority) - 2 hours

Execute these tests first as they represent core functionality:

#### Session 1 - Authentication (30 min)
1. ✅ **AUTH-001** - Valid Login (Student)
2. ✅ **AUTH-002** - Invalid Login
3. ✅ **AUTH-003** - Registration
4. ✅ **AUTH-004** - Logout
5. ✅ **AUTH-005** - Session Persistence

**What to Record:**
- Login time (should be <2 seconds)
- Error message clarity
- Password validation behavior
- Session token storage

---

#### Session 2 - Student Core Workflow (45 min)
1. ✅ **STU-001** - Browse Events
2. ✅ **STU-002** - Register for Event
3. ✅ **STU-004** - Book Resource

**What to Record:**
- Page load times
- Filter/search accuracy
- Registration confirmation
- Capacity validation
- Booking confirmation

---

#### Session 3 - Admin Approval Flow (45 min)
1. ✅ **ADM-001** - Approve Event
2. ✅ **ADM-002** - Approve Booking
3. ✅ **ORG-001** - Create Event (as Organizer)

**What to Record:**
- Approval notification
- Status changes
- Email notifications (if implemented)
- Admin dashboard updates

---

### Phase 2: Standard Workflows - 3 hours

#### Session 4 - Remaining Student Tests (45 min)
1. ✅ **STU-003** - Cancel Registration
2. ✅ **STU-005** - View Bookings

#### Session 5 - Organizer Tests (1 hour)
1. ✅ **ORG-002** - Edit Event
2. ✅ **ORG-003** - View Registrations
3. ✅ **ORG-004** - Cancel Event

#### Session 6 - Remaining Admin Tests (1 hour 15 min)
1. ✅ **ADM-003** - Manage Resources
2. ✅ **ADM-004** - Manage Users
3. ✅ **ADM-005** - View Analytics

---

### Phase 3: Edge Cases - 2 hours

#### Session 7 - Error Handling (2 hours)
1. ✅ **EDGE-001** - Network Failure
2. ✅ **EDGE-002** - Invalid Token
3. ✅ **EDGE-003** - Concurrent Booking
4. ✅ **EDGE-004** - Form Validation
5. ✅ **EDGE-005** - API Timeout

**Special Setup for Edge Cases:**
- EDGE-001: Use Network Link Conditioner or stop backend
- EDGE-002: Manually expire token or wait for timeout
- EDGE-003: Open 2 browser/app instances
- EDGE-004: Test all validation rules systematically
- EDGE-005: Add delay in backend or use slow network

---

## 📝 How to Execute a Test Case

### Step-by-Step Process

**1. Open Test Documentation**
```bash
# Open TEST_CASES.md in editor
code TEST_CASES.md
# OR
open TEST_CASES.md
```

**2. Select Test Case**
- Choose test from appropriate category
- Note the Test ID (e.g., AUTH-001)
- Read Prerequisites section

**3. Prepare Test Data**
- Review "Test Data" section in test case
- Ensure required data exists in database
- Prepare any test accounts needed

**4. Execute Test Steps**
- Follow numbered steps exactly as written
- Don't skip steps
- Take screenshots of key moments
- Note any deviations from expected behavior

**5. Record Results**
- Fill in "Actual Results" section
- Check ✅ Pass or ❌ Fail
- Add notes about observations
- Include date and tester name

**6. Handle Failures**
- If test fails, log issue in "Issues Found" section
- Include:
  - Test ID
  - Severity (Critical/High/Medium/Low)
  - Steps to reproduce
  - Screenshots
  - Expected vs Actual behavior
- Create GitHub issue if needed

---

## 📊 Recording Test Results

### In TEST_CASES.md

For each test, update:

```markdown
**Actual Results:**
- Status: ✅ Passed / ❌ Failed / ⚠️ Blocked
- Date Tested: [Date]
- Tester: [Your Name]
- Notes: [Any observations]
- Screenshots: [Link to screenshots folder]

**Pass/Fail:** ✅ Passed
```

### Example of Good Test Notes:

```markdown
**Actual Results:**
- Status: ✅ Passed
- Date Tested: October 9, 2025
- Tester: Jane Doe
- Notes: 
  - Login successful in 1.2 seconds
  - Dashboard loaded correctly
  - Welcome message displayed: "Welcome, John Student"
  - Navigation sidebar showed all expected options
  - Session token stored in session_manager
  - Logout button visible and functional
- Screenshots: screenshots/auth-001-success.png

**Pass/Fail:** ✅ Passed
```

### Example of Failed Test:

```markdown
**Actual Results:**
- Status: ❌ Failed
- Date Tested: October 9, 2025
- Tester: Jane Doe
- Notes:
  - Login succeeded but dashboard did not load
  - Stuck on loading screen for 10+ seconds
  - Console shows error: "Cannot read property 'name' of undefined"
  - Session token was created
  - Manual navigation to dashboard works
- Issue Logged: #BUG-001
- Screenshots: screenshots/auth-001-failure.png

**Pass/Fail:** ❌ Failed
```

---

## 🐛 Bug Reporting Template

When you find a bug, add to "Issues Found" section:

```markdown
**Issue #1: Dashboard Fails to Load After Login**
- **Test ID:** AUTH-001
- **Severity:** Critical
- **Priority:** P0
- **Description:** After successful login, dashboard fails to load. User stuck on loading screen.
- **Environment:** 
  - OS: macOS 14.0
  - Python: 3.11.5
  - Backend Version: 1.0.0
- **Steps to Reproduce:**
  1. Launch application
  2. Enter credentials: student@test.com / Student123!
  3. Click Login button
  4. Observe loading screen appears
  5. Wait 10+ seconds - dashboard never loads
- **Expected:** Dashboard loads within 2-3 seconds
- **Actual:** Loading screen persists indefinitely
- **Console Errors:** 
  ```
  TypeError: Cannot read property 'name' of undefined
  at StudentDashboard.__init__() line 45
  ```
- **Screenshots:** 
  - screenshots/bug-001-loading-screen.png
  - screenshots/bug-001-console-error.png
- **Workaround:** Manually navigate using menu: Dashboard > Student Dashboard
- **Status:** Open
- **Assigned To:** Dev Team
- **Created:** October 9, 2025
- **Updated:** October 9, 2025
```

---

## 📸 Screenshots Best Practices

**Create screenshots folder:**
```bash
mkdir -p frontend_tkinter/test_screenshots
```

**Naming Convention:**
- `[test-id]-[description]-[pass/fail].png`
- Examples:
  - `auth-001-login-success.png`
  - `auth-002-invalid-credentials-error.png`
  - `bug-001-loading-screen-stuck.png`

**What to Capture:**
- Initial state
- Each step if critical
- Error messages (full screen)
- Success confirmations
- Final state

---

## 📋 Test Session Template

At the start of each testing session, fill this out:

```markdown
### Test Session #1: Authentication Tests
**Date:** October 9, 2025
**Time:** 2:00 PM - 4:00 PM
**Tester:** Jane Doe
**Environment:** 
- OS: macOS 14.0
- Frontend Version: 2.0.0
- Backend Version: 1.0.0
- Database: MySQL 8.0

**Backend Status:** ✅ Running on http://localhost:8080
**Test Data:** ✅ All test accounts created

**Tests Planned (5):**
- [ ] AUTH-001 - Valid Login
- [ ] AUTH-002 - Invalid Login
- [ ] AUTH-003 - Registration
- [ ] AUTH-004 - Logout
- [ ] AUTH-005 - Session Persistence

**Pre-Testing Notes:**
- Backend started successfully
- All dependencies installed
- Test accounts verified in database

---

**Tests Executed:** 5/5
**Passed:** 4
**Failed:** 1
**Blocked:** 0
**Pass Rate:** 80%

**Issues Found:** 1
- BUG-001: Dashboard loading issue (Critical)

**Post-Testing Notes:**
- Most authentication flows work correctly
- Critical issue with dashboard loading needs immediate fix
- Session management works as expected
- Password validation is thorough

**Next Steps:**
- Fix BUG-001
- Re-run AUTH-001 after fix
- Proceed to Student workflow tests
```

---

## 🎯 Success Criteria

### For Individual Test:
- ✅ All expected results matched actual results
- ✅ No unexpected errors or warnings
- ✅ Performance meets requirements (load time, response time)
- ✅ UI displays correctly
- ✅ Data persists correctly
- ✅ Error handling works as designed

### For Complete Test Suite:
- ✅ 100% test execution (24/24 tests run)
- ✅ 95%+ pass rate (≥23 tests pass)
- ✅ 0 critical issues
- ✅ ≤3 high priority issues
- ✅ All critical paths working
- ✅ Documentation complete

---

## 🔄 Regression Testing

After bug fixes, re-run affected tests:

**Example Regression Plan:**

If BUG-001 (Dashboard loading) is fixed:
```markdown
**Regression Tests Required:**
- [ ] AUTH-001 - Valid Login (primary affected test)
- [ ] AUTH-005 - Session Persistence (uses dashboard)
- [ ] STU-001 - Browse Events (loads from dashboard)
- [ ] ORG-001 - Create Event (loads from dashboard)
- [ ] ADM-001 - Approve Event (loads from dashboard)

**Smoke Tests:**
- [ ] Login as Student - verify dashboard
- [ ] Login as Organizer - verify dashboard
- [ ] Login as Admin - verify dashboard
- [ ] Navigate all main menu items
- [ ] Verify no new errors in console
```

---

## 📊 Test Metrics Dashboard

Track these metrics during testing:

```markdown
## Test Execution Metrics

### Overall Progress
- **Total Tests:** 24
- **Executed:** 0/24 (0%)
- **Passed:** 0/24 (0%)
- **Failed:** 0/24 (0%)
- **Blocked:** 0/24 (0%)
- **Pass Rate:** 0%

### By Category
| Category | Total | Executed | Passed | Failed | Pass Rate |
|----------|-------|----------|--------|--------|-----------|
| Authentication | 5 | 0 | 0 | 0 | 0% |
| Student | 5 | 0 | 0 | 0 | 0% |
| Organizer | 4 | 0 | 0 | 0 | 0% |
| Admin | 5 | 0 | 0 | 0 | 0% |
| Edge Cases | 5 | 0 | 0 | 0 | 0% |

### By Priority
| Priority | Total | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
| High | 14 | 0 | 0 | 0% |
| Medium | 10 | 0 | 0 | 0% |

### Issue Summary
- **Critical:** 0
- **High:** 0
- **Medium:** 0
- **Low:** 0
- **Total:** 0

### Time Tracking
- **Estimated Time:** 8 hours
- **Actual Time:** 0 hours
- **Efficiency:** 0%
```

Update this after each session!

---

## ✅ Final Sign-Off Checklist

Before declaring testing complete:

### Test Execution
- [ ] All 24 tests executed
- [ ] All tests documented with actual results
- [ ] All screenshots captured
- [ ] All issues logged

### Pass Criteria
- [ ] Pass rate ≥95% (≥23/24 tests)
- [ ] 0 critical issues open
- [ ] ≤3 high priority issues open
- [ ] All critical paths working

### Documentation
- [ ] TEST_CASES.md fully updated
- [ ] All actual results recorded
- [ ] Test metrics calculated
- [ ] Issues documented with details
- [ ] Screenshots organized

### Regression
- [ ] All fixed bugs retested
- [ ] No new issues introduced
- [ ] Smoke tests passed

### Final Review
- [ ] QA Lead review complete
- [ ] Dev team notified of issues
- [ ] Stakeholder signoff obtained
- [ ] Release notes prepared

---

## 🎓 Tips for Effective Testing

### Do's ✅
- ✅ Follow test steps exactly
- ✅ Test with fresh data
- ✅ Clear cache between tests
- ✅ Take detailed notes
- ✅ Capture screenshots of failures
- ✅ Report issues immediately
- ✅ Test edge cases thoroughly
- ✅ Verify error messages
- ✅ Check console for errors
- ✅ Test with different user roles

### Don'ts ❌
- ❌ Skip steps
- ❌ Assume behavior
- ❌ Test multiple things at once
- ❌ Use production data
- ❌ Ignore warnings
- ❌ Skip documentation
- ❌ Forget to logout between tests
- ❌ Test with unstable backend
- ❌ Rush through tests
- ❌ Ignore minor issues

---

## 📞 Support

**Questions during testing?**
- Review TEST_CASES.md for detailed steps
- Check CONFIGURATION_GUIDE.md for setup issues
- Review API_DOCUMENTATION.md for backend questions
- Check logs in `logs/` directory

**Found a blocker?**
- Log as Critical issue
- Notify dev team immediately
- Mark subsequent tests as Blocked
- Continue with unrelated tests

---

## 🎉 Testing Complete!

Once all tests are executed and documented:

1. **Calculate final metrics**
2. **Create test summary report**
3. **Get QA Lead sign-off**
4. **Notify stakeholders**
5. **Prepare release notes**
6. **Archive test results**

---

**Ready to Begin?** Start with Phase 1 Session 1 (Authentication Tests)! 🚀

**Good luck with testing!** 🧪✨

---

*Test Execution Guide v1.0*  
*Campus Event & Resource Coordination System v2.0.0*  
*Created: October 9, 2025*
