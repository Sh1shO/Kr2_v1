CREATE TABLE car_model(
	id SERIAL PRIMARY KEY,
	name VARCHAR(50)	
);

CREATE TABLE car(
	id SERIAL PRIMARY KEY,
	model_id INT REFERENCES car_model(id),
	number VARCHAR(50),
	color VARCHAR(50),
	release_year DATE,
	insurence_cost MONEY
);

CREATE TABLE client(
	id SERIAL PRIMARY KEY,
	lastname VARCHAR(50),
	firstname VARCHAR(50),
	patronymic VARCHAR(50),
	series_passport INT,
	number_passport INT
);

CREATE TABLE rental(
	id SERIAL PRIMARY KEY,
	day_cost MONEY,
	start_date DATE,
	days_quantity INT,
	car_id INT REFERENCES car(id),
	client_id INT REFERENCES client(id)
);


