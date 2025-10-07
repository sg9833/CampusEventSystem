-- sample_data.sql

USE campusdb;

INSERT INTO event (name, location, start_time, end_time, description)
VALUES 
('Tech Talk', 'Auditorium', '2025-10-15 10:00:00', '2025-10-15 12:00:00', 'A talk on latest tech trends.'),
('Workshop on AI', 'Lab 101', '2025-10-20 14:00:00', '2025-10-20 17:00:00', 'Hands-on AI workshop.'),
('Cultural Fest', 'Main Grounds', '2025-11-05 09:00:00', '2025-11-05 21:00:00', 'Annual cultural festival.');

INSERT INTO participant (name, email, event_id)
VALUES
('Ajay G', 'ajay@example.com', 1),
('Rohan K', 'rohan@example.com', 2),
('Sandali P', 'sandali@example.com', 3);
