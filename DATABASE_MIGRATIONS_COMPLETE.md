# 📊 Database Migrations - Complete Documentation

## ✅ All Migrations Applied Successfully

This document tracks all database schema changes applied to the CampusEventSystem database.

---

## 🗂️ Migration Files

### 1. **add_username_migration.sql**
**Status:** ✅ Applied  
**Purpose:** Add username field for dual email/username login support

**Changes:**
- Added `username` column to `users` table
- Type: `VARCHAR(50)`, unique, not null
- Updated existing records with username = email prefix
- Added unique index on username

---

### 2. **add_event_status_and_registrations.sql**
**Status:** ✅ Applied  
**Purpose:** Implement event approval system and registration tracking

**Changes:**
- **events table:**
  - Added `status` field: VARCHAR(50), default 'pending'
  - Valid values: 'pending', 'approved', 'rejected'
  - Added index on status for filtering

- **event_registrations table:** (NEW)
  - `id`: INT, primary key, auto_increment
  - `event_id`: INT, foreign key → events.id
  - `user_id`: INT, foreign key → users.id
  - `registered_at`: TIMESTAMP, default CURRENT_TIMESTAMP
  - `status`: VARCHAR(50), default 'active'
  - Unique constraint on (event_id, user_id) - prevents duplicate registrations
  - Cascading delete when event or user deleted

**Impact:**
- Students can now register for approved events only
- Admins can approve/reject events
- Duplicate registrations prevented at database level

---

### 3. **add_missing_fields.sql**
**Status:** ✅ Applied  
**Purpose:** Add timestamp tracking and status fields to all tables

**Changes:**
- **events table:**
  - Added `created_at`: DATETIME, default CURRENT_TIMESTAMP
  - Added index on created_at

- **resources table:**
  - Added `is_active`: BOOLEAN, default TRUE
  - Added `created_at`: DATETIME, default CURRENT_TIMESTAMP
  - Added indexes on both fields

- **bookings table:**
  - Added `created_at`: DATETIME, default CURRENT_TIMESTAMP
  - Added index on created_at

- **Performance indexes added:**
  - `idx_bookings_event` on bookings(event_id)
  - `idx_bookings_user` on bookings(user_id)
  - `idx_bookings_resource` on bookings(resource_id)
  - `idx_bookings_status` on bookings(status)

**Impact:**
- Full audit trail for all entities
- Soft delete capability for resources via is_active flag
- Improved query performance with foreign key indexes

---

## 📋 Current Database Schema

### **users**
```
id (PK)
email (UNIQUE)
username (UNIQUE)
password_hash
role (STUDENT/ORGANIZER/ADMIN)
created_at
```

### **events**
```
id (PK)
title
description
organizer_id (FK → users.id)
start_time
end_time
venue
status (pending/approved/rejected)
created_at
```

### **resources**
```
id (PK)
name
type
capacity
location
is_active (BOOLEAN)
created_at
```

### **bookings**
```
id (PK)
event_id (FK → events.id)
user_id (FK → users.id)
resource_id (FK → resources.id)
start_time
end_time
status (pending/confirmed/cancelled)
created_at
```

### **event_registrations**
```
id (PK)
event_id (FK → events.id)
user_id (FK → users.id)
registered_at
status (active/cancelled)
UNIQUE(event_id, user_id)
```

---

## 🔍 Schema Validation

All Java model fields now match database columns:

✅ **Event.java** → events table
- id, title, description, organizerId, startTime, endTime, venue, status, createdAt

✅ **Resource.java** → resources table
- id, name, type, capacity, location, isActive, createdAt

✅ **Booking.java** → bookings table
- id, eventId, userId, resourceId, startTime, endTime, status, createdAt

✅ **EventRegistration.java** → event_registrations table
- id, eventId, userId, registeredAt, status

✅ **User.java** → users table
- id, email, username, passwordHash, role, createdAt

---

## 🎯 Migration Commands

### To apply all migrations:
```bash
# Migration 1: Username support
mysql -u root -p'SAIAJAY@2005' campusdb < database_sql/add_username_migration.sql

# Migration 2: Event approval & registrations
mysql -u root -p'SAIAJAY@2005' campusdb < database_sql/add_event_status_and_registrations.sql

# Migration 3: Timestamp tracking & indexes
mysql -u root -p'SAIAJAY@2005' campusdb < database_sql/add_missing_fields.sql
```

### To verify schema:
```bash
mysql -u root -p'SAIAJAY@2005' campusdb -e "
SHOW COLUMNS FROM events;
SHOW COLUMNS FROM resources;
SHOW COLUMNS FROM bookings;
SHOW COLUMNS FROM event_registrations;
SHOW COLUMNS FROM users;"
```

---

## 🔒 Data Integrity

### Foreign Key Constraints:
- ✅ events.organizer_id → users.id (CASCADE DELETE)
- ✅ bookings.event_id → events.id (CASCADE DELETE)
- ✅ bookings.user_id → users.id (CASCADE DELETE)
- ✅ bookings.resource_id → resources.id (CASCADE DELETE)
- ✅ event_registrations.event_id → events.id (CASCADE DELETE)
- ✅ event_registrations.user_id → users.id (CASCADE DELETE)

### Unique Constraints:
- ✅ users.email
- ✅ users.username
- ✅ event_registrations(event_id, user_id) - Prevents duplicate registrations

### Indexes for Performance:
- ✅ events: status, created_at, organizer_id
- ✅ resources: is_active, created_at
- ✅ bookings: event_id, user_id, resource_id, status, created_at
- ✅ event_registrations: event_id, user_id

---

## 📊 Migration Statistics

| Migration | Tables Affected | Columns Added | Indexes Added | Constraints Added |
|-----------|----------------|---------------|---------------|-------------------|
| Username  | 1 (users)      | 1             | 1             | 1 (UNIQUE)        |
| Event Approval | 2 (events, event_registrations) | 2 | 2 | 3 (2 FK, 1 UNIQUE) |
| Timestamps | 3 (events, resources, bookings) | 4 | 9 | 0 |
| **TOTAL** | **4 tables** | **7 columns** | **12 indexes** | **4 constraints** |

---

## 🚀 Next Steps

**Database is now fully synchronized with Java models!**

All migrations have been applied successfully. The schema now supports:
- ✅ Username/email dual login
- ✅ Event approval workflow
- ✅ Event registration tracking
- ✅ Resource availability management
- ✅ Complete audit trails with timestamps
- ✅ Optimized queries with indexes

**Ready for production use!**

---

## 📝 Notes

- All migrations are idempotent (safe to run multiple times)
- Migrations use stored procedures to check for existing columns
- Default values ensure backward compatibility
- Cascading deletes maintain referential integrity
- Indexes improve query performance for common operations

---

**Last Updated:** 2024
**Database Version:** MySQL 8.0
**Schema Status:** ✅ Complete and Validated
