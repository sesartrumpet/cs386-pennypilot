-- PennyPilot Database Initialization Script
-- This script populates the database with initial data for testing and development.
-- All INSERT statements use IGNORE to prevent duplicate key errors.

-- Insert initial user profiles
-- Format: (username, passwordHash, firstName, lastName, nauEmail)
INSERT IGNORE INTO userProfile VALUES 
    ('Krqf', '123455', 'Kyle', 'Radzvin', 'ktr66@nau.edu'),  -- Test user account
    ('admin', 'password', 'Admin', 'User', 'admin@nau.edu');  -- Admin account

-- Insert available trip destinations
-- Format: (location, programType)
-- programType indicates the type of educational program at the destination
INSERT IGNORE INTO tripDestination VALUES
    ('France', 'Sorbonne University'),                      -- College program in France
    ('Mexico', 'National Autonomous University of Mexico'), -- School program in Mexico
    ('Germany', 'Technical University of Munich'),          -- Technical university program
    ('Japan', 'KAI Japanese Language School'),              -- Language school program
    ('Canada', 'University of British Columbia'),           -- Exchange program
    ('Italy', 'Domus Academy'),                             -- Design academy program
    ('Brazil', 'Pontifical Catholic University of Rio de Janeiro'), -- General study abroad program
    ('Australia', 'Australian Maritime College'),           -- Marine studies program
    ('South Korea', 'Korea Advanced Institute of Science and Technology'); -- Technology university program


-- Insert price breakdowns for each destination
-- Format: (location, Travelto, Travelthere, Food, Housing, School, Misc)
-- All amounts are in USD
INSERT IGNORE INTO prices VALUES 
    -- France: High-end destination with comprehensive program
    ('France', 1000.00, 500.00, 500.00, 1500.00, 2500.00, 250.00),
    -- Mexico: Budget-friendly option
    ('Mexico', 500.00, 250.00, 500.00, 1500.00, 2000.00, 250.00),
    -- Germany: Technical focus with moderate costs
    ('Germany', 900.00, 400.00, 600.00, 1400.00, 2300.00, 200.00),
    -- Japan: Premium destination with language focus
    ('Japan', 1200.00, 600.00, 700.00, 1600.00, 2600.00, 300.00),
    -- Canada: Affordable North American option
    ('Canada', 800.00, 300.00, 550.00, 1300.00, 2200.00, 150.00),
    -- Italy: Cultural and design focus
    ('Italy', 850.00, 350.00, 600.00, 1450.00, 2400.00, 180.00),
    -- Brazil: South American experience
    ('Brazil', 750.00, 300.00, 500.00, 1200.00, 2100.00, 220.00),
    -- Australia: Premium destination with marine focus
    ('Australia', 1300.00, 650.00, 750.00, 1700.00, 2700.00, 350.00),
    -- South Korea: Technology-focused program
    ('South Korea', 1100.00, 550.00, 650.00, 1500.00, 2500.00, 280.00);


