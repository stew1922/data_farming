DROP TABLE IF EXISTS states;

CREATE TABLE states (
	state_id SERIAL PRIMARY KEY
	, state_name CHAR(2)
);

SELECT * FROM states;