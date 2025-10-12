-- Migration script to add username column to users table
-- Run this if you have an existing database

-- Add username column (allow NULL temporarily for existing records)
ALTER TABLE users ADD COLUMN username VARCHAR(50) AFTER email;

-- Add created_at column if it doesn't exist
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- For existing users, set username to a temporary value based on email
-- This assumes you'll update them manually or through the application
UPDATE users SET username = SUBSTRING_INDEX(email, '@', 1) WHERE username IS NULL;

-- Now make username NOT NULL and UNIQUE
ALTER TABLE users MODIFY COLUMN username VARCHAR(50) NOT NULL;
ALTER TABLE users ADD UNIQUE KEY unique_username (username);

-- Verify the changes
DESCRIBE users;
