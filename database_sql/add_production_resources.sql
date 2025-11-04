-- Add 20 Production-Level Sample Resources
-- Run this script to populate the database with diverse resources
-- Usage: mysql -u root -p campusdb < add_production_resources.sql

USE campusdb;

-- Delete existing sample resources (optional - comment out if you want to keep them)
-- DELETE FROM resources WHERE id IN (1, 2);

-- Conference Rooms & Meeting Spaces (Large Capacity)
INSERT INTO resources (name, type, capacity, location) VALUES
('Grand Conference Hall', 'Conference Room', 200, 'Main Building - 3rd Floor'),
('Executive Board Room', 'Meeting Room', 25, 'Administration Block - 5th Floor'),
('Innovation Hub Conference Center', 'Conference Room', 150, 'Technology Center - Ground Floor'),
('Senate Hall', 'Auditorium', 300, 'Central Campus - Main Building'),

-- Classrooms & Lecture Halls (Medium Capacity)
('Smart Classroom 301', 'Classroom', 60, 'Academic Block A - 3rd Floor'),
('Lecture Hall B-204', 'Lecture Hall', 120, 'Academic Block B - 2nd Floor'),
('Interactive Learning Space', 'Classroom', 40, 'Learning Center - 1st Floor'),

-- Computer Labs & Technical Spaces
('Computer Lab 101', 'Computer Lab', 50, 'IT Building - 1st Floor'),
('AI & Machine Learning Lab', 'Computer Lab', 30, 'Research Center - 2nd Floor'),
('Multimedia Production Studio', 'Studio', 15, 'Media Center - Basement'),

-- Specialized Event Spaces
('Outdoor Amphitheater', 'Outdoor Space', 250, 'Central Quadrangle'),
('Student Activity Center', 'Multi-Purpose Hall', 100, 'Student Union Building'),
('Innovation Maker Space', 'Workshop', 25, 'Engineering Building - Ground Floor'),

-- Small Meeting Rooms & Study Spaces
('Study Room Alpha', 'Study Room', 8, 'Library - 2nd Floor'),
('Collaboration Pod Beta', 'Meeting Room', 6, 'Library - 3rd Floor'),
('Focus Room Gamma', 'Study Room', 4, 'Library - 1st Floor'),

-- Special Purpose Venues
('Research Presentation Theater', 'Theater', 80, 'Research Building - 4th Floor'),
('Wellness & Yoga Studio', 'Studio', 30, 'Sports Complex - 2nd Floor'),
('Art Exhibition Gallery', 'Gallery', 60, 'Arts Building - 1st Floor'),
('Debate & Moot Court Room', 'Specialized Room', 40, 'Law Building - 2nd Floor');

-- Display success message
SELECT 'Successfully added 20 production-level resources!' as Status;
SELECT COUNT(*) as 'Total Resources' FROM resources;

