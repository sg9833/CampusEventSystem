-- schema.sql

CREATE DATABASE IF NOT EXISTS campusdb;
USE campusdb;

CREATE TABLE IF NOT EXISTS event (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    start_time DATETIME,
    end_time DATETIME,
    description TEXT
);

-- If you later want to create Participant table
CREATE TABLE IF NOT EXISTS participant (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    event_id BIGINT,
    FOREIGN KEY (event_id) REFERENCES event(id)
);
