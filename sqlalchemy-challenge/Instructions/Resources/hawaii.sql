DROP TABLE IF EXISTS station;
DROP TABLE IF EXISTS measurements;

CREATE TABLE station(
	station VARCHAR(255) NOT NULL,
	name VARCHAR(255) NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	elevation FLOAT NOT NULL
);

CREATE TABLE measurements(
	station VARCHAR(255) NOT NULL,
	date VARCHAR(255) NOT NULL,
	prcp FLOAT,
	tobs INT
);
