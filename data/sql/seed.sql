-- Seed data into tables

INSERT INTO states
(state_name, latitud, longitud)
VALUES
	('NE', 41.256538, -95.934502),
	('IA', 41.586834, -93.624962),
	('IL', 38.317610, -88.904730);

INSERT INTO crop_name
(crop_name)
VALUES
	('corn'),
	('soybean'),
	('wheat');

SELECT * FROM crop_name;