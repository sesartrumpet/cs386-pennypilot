-- PennyPilot Database Schema
-- This script creates the database and all necessary tables for the PennyPilot application.
-- The schema is designed to support trip planning, cost tracking, and user management.

-- Create the database if it doesn't exist and select it for use
CREATE DATABASE IF NOT EXISTS pennypilot_db;
USE pennypilot_db;

-- User Profile Table
-- Stores user account information and authentication details
-- Primary Key: userName (unique identifier for each user)
CREATE TABLE IF NOT EXISTS userProfile (
	userName VARCHAR(50) NOT NULL PRIMARY KEY,    -- Unique username for login
    passwordHash VARCHAR(255) NOT NULL,           -- Hashed password for security
    firstName VARCHAR(50),                        -- User's first name
    lastName VARCHAR(50),                         -- User's last name
    nauEmail VARCHAR(50)                          -- User's NAU email address
);

-- Trip Destination Table
-- Stores available travel destinations and their associated educational institutions
-- Primary Key: location (unique identifier for each destination)
CREATE TABLE IF NOT EXISTS tripDestination (
	location VARCHAR(100) NOT NULL PRIMARY KEY,   -- Name of the destination
    university VARCHAR(100) NOT NULL              -- Associated educational institution
);

-- Price Breakdown Table
-- Stores detailed cost information for each destination
-- Primary Key: location (links to tripDestination)
-- Foreign Key: location references tripDestination(location)
CREATE TABLE IF NOT EXISTS prices (
	location VARCHAR(100) NOT NULL PRIMARY KEY,   -- Destination name
    Travelto DECIMAL(10,2) NOT NULL DEFAULT 0.00,    -- Cost to travel to destination
    Travelthere DECIMAL(10,2) NOT NULL DEFAULT 0.00, -- Cost of local transportation
    Food DECIMAL(10,2) NOT NULL DEFAULT 0.00,        -- Estimated food expenses
    Housing DECIMAL(10,2) NOT NULL DEFAULT 0.00,     -- Accommodation costs
    School DECIMAL(10,2) NOT NULL DEFAULT 0.00,      -- Educational program costs
    Misc DECIMAL(10,2) NOT NULL DEFAULT 0.00,        -- Miscellaneous expenses
    FOREIGN KEY (location) REFERENCES tripDestination(location) ON DELETE CASCADE
);

-- Trip Planning Table
-- Tracks user's planned trips and their details
-- Primary Key: userName (links to userProfile)
-- Foreign Keys: 
--   - userName references userProfile(userName)
--   - location references tripDestination(location)
CREATE TABLE IF NOT EXISTS trip (
    userName VARCHAR(50) NOT NULL PRIMARY KEY,    -- User planning the trip
    location VARCHAR(100) NOT NULL,               -- Selected destination
    timeframe INT NOT NULL,                       -- Duration in months
    FOREIGN KEY (userName) REFERENCES userProfile(userName) ON DELETE CASCADE,
    FOREIGN KEY (location) REFERENCES tripDestination(location) ON DELETE CASCADE
);

