-- Seed data into table temperatures

INSERT INTO temperatures
(state_id, year, jan, feb,mar,apr,may,jun,jul,ago, sep, oct, nov,dec )

VALUES
(1, 2000, 21.00,32.5,45.5,27.1,99.0,12.5,59.32,33.25,28.42,22.4,14.50,0);

SELECT * FROM temperatures;

DELETE FROM temperatures
WHERE state_id =1;