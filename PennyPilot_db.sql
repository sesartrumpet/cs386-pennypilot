
-- Create and enter database
CREATE DATABASE IF NOT EXISTS pennypilot_db;
USE pennypilot_db;

-- Creates a userProfile table
CREATE TABLE IF NOT EXISTS userProfile (
	userName VARCHAR(50) NOT NULL PRIMARY KEY,
    passwordHash VARCHAR(255) NOT NULL,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    nauEmail VARCHAR(50)
);

-- A list of potential destinations a user can plan trips to, mapped to universities.
CREATE TABLE IF NOT EXISTS tripDestination (
	location VARCHAR(100) NOT NULL PRIMARY KEY,
    university VARCHAR(100) NOT NULL
);

-- travel costs per destination 
CREATE TABLE IF NOT EXISTS prices (
	location VARCHAR(100) NOT NULL PRIMARY KEY,
    Travelto DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    Travelthere DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    Food DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    Housing DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    School DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    Misc DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (location) REFERENCES tripDestination(location) ON DELETE CASCADE
);

-- Tracks the actual trip a user is planning
CREATE TABLE IF NOT EXISTS trip (
    userName VARCHAR(50) NOT NULL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    timeframe INT NOT NULL, -- in months
    FOREIGN KEY (userName) REFERENCES userProfile(userName) ON DELETE CASCADE,
    FOREIGN KEY (location) REFERENCES tripDestination(location) ON DELETE CASCADE
);

-- This is the simple login user table your login form connects to:
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- inserts your default test account
INSERT IGNORE INTO users (username, password) VALUES ('admin', 'password');

