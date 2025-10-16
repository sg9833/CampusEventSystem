-- Migration: Add event approval system and event registrations
-- This script adds status field to events table and creates event_registrations table

-- Step 1: Add status column to events table
ALTER TABLE events 
ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'pending' AFTER venue;

-- Update existing events to 'approved' status (backward compatibility)
UPDATE events SET status = 'approved' WHERE status = 'pending';

-- Step 2: Create event_registrations table
CREATE TABLE IF NOT EXISTS event_registrations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_registration (event_id, user_id)
);

-- Add indexes for better query performance
CREATE INDEX idx_event_registrations_event ON event_registrations(event_id);
CREATE INDEX idx_event_registrations_user ON event_registrations(user_id);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_organizer ON events(organizer_id);
