DROP TABLE IF EXISTS states CASCADE;
DROP TABLE IF EXISTS temperatures  CASCADE;
DROP TABLE IF EXISTS crop_name CASCADE;
DROP TABLE IF EXISTS crop_production_total CASCADE;

CREATE TABLE states (
	state_id SERIAL PRIMARY KEY
	, state_name CHAR(2)
);

SELECT * FROM states;

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


CREATE TABLE crop_name (
	crop_id SERIAL PRIMARY KEY
	, crop_name VARCHAR(255) 
);

SELECT * FROM crop_name;

CREATE TABLE crop_production_total (
	crop_id INT NOT NULL,
	FOREIGN KEY (crop_id) REFERENCES crop_name(crop_id),
	year DATE,
	march_1st BIGINT,
	jun_1st BIGINT,
	sep_1st BIGINT,
	dec_1st BIGINT
);
SELECT * FROM crop_production_total;

CREATE TABLE precipitations (
	state_id INT NOT NULL,
	FOREIGN KEY (state_id) REFERENCES states(state_id)
	, year INT NOT NULL
	, jan DEC(10,6) NOT NULL
	, feb DEC(10,6) NOT NULL
	, mar DEC(10,6) NOT NULL
	, apr DEC(10,6) NOT NULL
	, may DEC(10,6) NOT NULL
	, jun DEC(10,6) NOT NULL
	, jul DEC(10,6) NOT NULL
	, ago DEC(10,6) NOT NULL
	, sep DEC(10,6) NOT NULL
	, oct DEC(10,6) NOT NULL
	, nov DEC(10,6) NOT NULL
	, dec DEC(10,6) NOT NULL
);

SELECT * FROM precipitations;