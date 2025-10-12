-- sample_data.sql
USE campusdb;

-- Password for all test accounts: test123
-- BCrypt hash: $2a$10$xphqVNq9W7tyXH/kiDBjzO1FpBqcdyvwdcvBMmM.J74pUDBc2wd02
INSERT INTO users (name, email, password_hash, role) VALUES
('Admin User', 'admin@campus.com', '$2a$10$xphqVNq9W7tyXH/kiDBjzO1FpBqcdyvwdcvBMmM.J74pUDBc2wd02', 'admin'),
('Organizer One', 'organizer1@campus.com', '$2a$10$xphqVNq9W7tyXH/kiDBjzO1FpBqcdyvwdcvBMmM.J74pUDBc2wd02', 'organizer'),
('Student One', 'student1@campus.com', '$2a$10$xphqVNq9W7tyXH/kiDBjzO1FpBqcdyvwdcvBMmM.J74pUDBc2wd02', 'student');

INSERT INTO events (title, description, organizer_id, start_time, end_time, venue) VALUES
('Tech Talk', 'A talk on latest tech trends.', 2, '2025-10-15 10:00:00', '2025-10-15 12:00:00', 'Auditorium'),
('Workshop on AI', 'Hands-on AI workshop.', 2, '2025-10-20 14:00:00', '2025-10-20 17:00:00', 'Lab 101');

INSERT INTO resources (name, type, capacity, location) VALUES
('Projector', 'Equipment', 1, 'Auditorium'),
('Laptops', 'Equipment', 20, 'Lab 101');

INSERT INTO bookings (event_id, user_id, resource_id, start_time, end_time, status) VALUES
(1, 3, 1, '2025-10-15 10:00:00', '2025-10-15 12:00:00', 'approved'),
(2, 3, 2, '2025-10-20 14:00:00', '2025-10-20 17:00:00', 'pending');
