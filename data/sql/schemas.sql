DROP TABLE IF EXISTS states CASCADE;

CREATE TABLE states (
	state_id SERIAL PRIMARY KEY
	, state_name CHAR(2)
);

SELECT * FROM states;

DROP TABLE IF EXISTS temperatures  CASCADE;

CREATE TABLE temperatures (
	state_id INT NOT NULL,
	FOREIGN KEY (state_id) REFERENCES states(state_id)
	, year INT NOT NULL
	, jan FLOAT NOT NULL
	, feb FLOAT NOT NULL
	, mar FLOAT NOT NULL
	, apr FLOAT NOT NULL
	, may FLOAT NOT NULL
	, jun FLOAT NOT NULL
	, jul FLOAT NOT NULL
	, ago FLOAT NOT NULL
	, sep FLOAT NOT NULL
	, oct FLOAT NOT NULL
	, nov FLOAT NOT NULL
	, dec FLOAT NOT NULL
);

SELECT * FROM temperatures;

DROP TABLE IF EXISTS crop_name CASCADE;

CREATE TABLE crop_name (
	crop_id SERIAL PRIMARY KEY
	, crop_name VARCHAR(255) 
);

SELECT * FROM crop_name;