
-- Create and enter database
CREATE DATABASE IF NOT EXISTS pennypilot_db;
USE pennypilot_db;

CREATE TABLE IF NOT EXISTS userProfile (
	userName VARCHAR(50) NOT NULL PRIMARY KEY,
    passwordHash VARCHAR(255) NOT NULL,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    nauEmail VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS tripDestination (
	location VARCHAR(100) NOT NULL PRIMARY KEY,
    university VARCHAR(100) NOT NULL
);

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

CREATE TABLE IF NOT EXISTS trip (
    userName VARCHAR(50) NOT NULL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    timeframe INT NOT NULL, -- in months
    FOREIGN KEY (userName) REFERENCES userProfile(userName) ON DELETE CASCADE,
    FOREIGN KEY (location) REFERENCES tripDestination(location) ON DELETE CASCADE
);

