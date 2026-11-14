-- Additional mock resources for Browse Resources (safe to re-run: skips existing names)
INSERT INTO resources (name, type, capacity, location)
SELECT * FROM (
  SELECT 'Portable PA Sound System' AS name, 'Equipment' AS type, 5 AS capacity, 'Media Center - Store Room' AS location UNION ALL
  SELECT 'DSLR Camera Kit', 'Equipment', 4, 'Media Center - Store Room' UNION ALL
  SELECT 'Wireless Microphone Set', 'Equipment', 10, 'Auditorium - Backstage' UNION ALL
  SELECT '4K Projector (Portable)', 'Equipment', 3, 'IT Building - Store Room' UNION ALL
  SELECT 'Main Auditorium', 'Auditorium', 500, 'Central Campus - Main Building' UNION ALL
  SELECT 'Mini Seminar Hall', 'Lecture Hall', 80, 'Academic Block C - 1st Floor' UNION ALL
  SELECT 'Cyber Security Lab', 'Computer Lab', 35, 'IT Building - 2nd Floor' UNION ALL
  SELECT 'Robotics & IoT Lab', 'Laboratory', 30, 'Engineering Building - 1st Floor' UNION ALL
  SELECT 'Physics Laboratory', 'Laboratory', 40, 'Science Block - 2nd Floor' UNION ALL
  SELECT 'Chemistry Laboratory', 'Laboratory', 36, 'Science Block - 3rd Floor' UNION ALL
  SELECT 'Football Ground', 'Sports Facility', 300, 'Sports Complex - Outdoor' UNION ALL
  SELECT 'Indoor Badminton Court', 'Sports Facility', 24, 'Sports Complex - Ground Floor' UNION ALL
  SELECT 'Basketball Court', 'Sports Facility', 40, 'Sports Complex - Outdoor' UNION ALL
  SELECT 'Open Air Food Court Lawn', 'Outdoor Space', 200, 'Central Quadrangle - East' UNION ALL
  SELECT 'Alumni Meeting Lounge', 'Meeting Room', 20, 'Administration Block - 1st Floor' UNION ALL
  SELECT 'Startup Incubation Hub', 'Conference Room', 45, 'Technology Center - 2nd Floor' UNION ALL
  SELECT 'Music & Dance Studio', 'Studio', 35, 'Arts Building - Ground Floor' UNION ALL
  SELECT 'Podcast Recording Booth', 'Studio', 4, 'Media Center - 1st Floor' UNION ALL
  SELECT 'Library Seminar Room', 'Study Room', 25, 'Library - 4th Floor' UNION ALL
  SELECT 'Placement Cell Interview Room', 'Meeting Room', 8, 'Administration Block - 2nd Floor'
) AS new_res
WHERE NOT EXISTS (SELECT 1 FROM resources r WHERE r.name = new_res.name);
