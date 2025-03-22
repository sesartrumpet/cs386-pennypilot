INSERT INTO userProfile VALUES ('Krqf', 'Password', 'Kyle', 'Radzvin', 'ktr66@nau.edu');

INSERT INTO tripDestination VALUES ('France', 'college'),
								   ('Mexico', 'school');

INSERT INTO prices VALUES ('France', 1000.00, 500.00, 500.00, 1500.00, 2500.00, 250.00),
						  ('Mexico', 500.00, 250.00, 500.00, 1500.00, 2000.00, 250.00);

INSERT INTO trip VALUES ('Krqf', 'France', 24);

SELECT * FROM userProfile;
SELECT * FROM tripDestination;
SELECT * FROM prices;
SELECT * FROM trip;
DESCRIBE userProfile;