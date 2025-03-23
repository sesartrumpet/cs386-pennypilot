INSERT IGNORE INTO userProfile VALUES ('Krqf', 'Password', 'Kyle', 'Radzvin', 'ktr66@nau.edu');

INSERT IGNORE INTO tripDestination VALUES ('France', 'college'),
                                          ('Mexico', 'school'),
                                          ('Germany', 'Technical University'),
                                          ('Japan', 'Language School'),
                                          ('Canada', 'Exchange Program'),
                                          ('Italy', 'Design Academy'),
                                          ('Brazil', 'Study Abroad'),
                                          ('Australia', 'Marine Institute'),
                                          ('South Korea', 'Tech University');

INSERT IGNORE INTO prices VALUES 
  ('France', 1000.00, 500.00, 500.00, 1500.00, 2500.00, 250.00),
  ('Mexico', 500.00, 250.00, 500.00, 1500.00, 2000.00, 250.00),
  ('Germany', 900.00, 400.00, 600.00, 1400.00, 2300.00, 200.00),
  ('Japan', 1200.00, 600.00, 700.00, 1600.00, 2600.00, 300.00),
  ('Canada', 800.00, 300.00, 550.00, 1300.00, 2200.00, 150.00),
  ('Italy', 850.00, 350.00, 600.00, 1450.00, 2400.00, 180.00),
  ('Brazil', 750.00, 300.00, 500.00, 1200.00, 2100.00, 220.00),
  ('Australia', 1300.00, 650.00, 750.00, 1700.00, 2700.00, 350.00),
  ('South Korea', 1100.00, 550.00, 650.00, 1500.00, 2500.00, 280.00);

INSERT IGNORE INTO trip VALUES ('Krqf', 'France', 24);