-- Migration: Add missing timestamp and status fields
-- This script adds created_at timestamps and is_active flags to tables
-- Note: Uses procedure to check if columns exist before adding them

DELIMITER $$

-- Procedure to add column if not exists
DROP PROCEDURE IF EXISTS AddColumnIfNotExists$$
CREATE PROCEDURE AddColumnIfNotExists(
    IN tableName VARCHAR(64),
    IN columnName VARCHAR(64),
    IN columnDefinition VARCHAR(255)
)
BEGIN
    DECLARE col_count INT;
    
    SELECT COUNT(*) INTO col_count
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = tableName
    AND COLUMN_NAME = columnName;
    
    IF col_count = 0 THEN
        SET @sql = CONCAT('ALTER TABLE ', tableName, ' ADD COLUMN ', columnName, ' ', columnDefinition);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        SELECT CONCAT('✅ Added column ', columnName, ' to ', tableName) AS Result;
    ELSE
        SELECT CONCAT('⚠️  Column ', columnName, ' already exists in ', tableName) AS Result;
    END IF;
END$$

DELIMITER ;

-- Step 1: Add created_at to events table
CALL AddColumnIfNotExists('events', 'created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP');

-- Step 2: Add is_active and created_at to resources table
CALL AddColumnIfNotExists('resources', 'is_active', 'BOOLEAN DEFAULT TRUE');
CALL AddColumnIfNotExists('resources', 'created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP');

-- Step 3: Add created_at to bookings table
CALL AddColumnIfNotExists('bookings', 'created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP');

-- Step 4: Add indexes for performance (with safe checking)
SET @index_sql = 'CREATE INDEX idx_events_created_at ON events(created_at)';
SET @ignore_error = (SELECT COUNT(*) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'events' AND INDEX_NAME = 'idx_events_created_at');
SET @index_sql = IF(@ignore_error > 0, 'SELECT "Index idx_events_created_at already exists" AS Result', @index_sql);
PREPARE stmt FROM @index_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @index_sql = 'CREATE INDEX idx_resources_is_active ON resources(is_active)';
SET @ignore_error = (SELECT COUNT(*) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'resources' AND INDEX_NAME = 'idx_resources_is_active');
SET @index_sql = IF(@ignore_error > 0, 'SELECT "Index idx_resources_is_active already exists" AS Result', @index_sql);
PREPARE stmt FROM @index_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @index_sql = 'CREATE INDEX idx_resources_created_at ON resources(created_at)';
SET @ignore_error = (SELECT COUNT(*) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'resources' AND INDEX_NAME = 'idx_resources_created_at');
SET @index_sql = IF(@ignore_error > 0, 'SELECT "Index idx_resources_created_at already exists" AS Result', @index_sql);
PREPARE stmt FROM @index_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @index_sql = 'CREATE INDEX idx_bookings_created_at ON bookings(created_at)';
SET @ignore_error = (SELECT COUNT(*) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'bookings' AND INDEX_NAME = 'idx_bookings_created_at');
SET @index_sql = IF(@ignore_error > 0, 'SELECT "Index idx_bookings_created_at already exists" AS Result', @index_sql);
PREPARE stmt FROM @index_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Step 5: Add foreign key indexes for better performance
SET @index_sql = 'CREATE INDEX idx_bookings_event ON bookings(event_id)';
SET @ignore_error = (SELECT COUNT(*) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'bookings' AND INDEX_NAME = 'idx_bookings_event');
SET @index_sql = IF(@ignore_error > 0, 'SELECT "Index idx_bookings_event already exists" AS Result', @index_sql);
PREPARE stmt FROM @index_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @index_sql = 'CREATE INDEX idx_bookings_user ON bookings(user_id)';
SET @ignore_error = (SELECT COUNT(*) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'bookings' AND INDEX_NAME = 'idx_bookings_user');
SET @index_sql = IF(@ignore_error > 0, 'SELECT "Index idx_bookings_user already exists" AS Result', @index_sql);
PREPARE stmt FROM @index_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @index_sql = 'CREATE INDEX idx_bookings_resource ON bookings(resource_id)';
SET @ignore_error = (SELECT COUNT(*) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'bookings' AND INDEX_NAME = 'idx_bookings_resource');
SET @index_sql = IF(@ignore_error > 0, 'SELECT "Index idx_bookings_resource already exists" AS Result', @index_sql);
PREPARE stmt FROM @index_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @index_sql = 'CREATE INDEX idx_bookings_status ON bookings(status)';
SET @ignore_error = (SELECT COUNT(*) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'bookings' AND INDEX_NAME = 'idx_bookings_status');
SET @index_sql = IF(@ignore_error > 0, 'SELECT "Index idx_bookings_status already exists" AS Result', @index_sql);
PREPARE stmt FROM @index_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Clean up
DROP PROCEDURE IF EXISTS AddColumnIfNotExists;

SELECT '✅ Migration completed successfully!' AS Status;
