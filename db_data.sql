INSERT INTO car_model (name) VALUES
('Седан'),
('Хэтчбек'),
('Кроссовер');

INSERT INTO car (model_id, number, color, release_year, insurence_cost) VALUES
(1, 'ABC1234', 'Красный', '2021-01-15', 500.00),
(2, 'DEF5678', 'Синий', '2020-05-20', 450.00),
(3, 'GHI9101', 'Чёрный', '2019-07-25', 300.00);

INSERT INTO client (lastname, firstname, patronymic, series_passport, number_passport) VALUES
('Иванов', 'Иван', 'Иванович', 1234, 567890),
('Петров', 'Петр', 'Петрович', 2345, 678901),
('Сидоров', 'Сидор', 'Сидорович', 3456, 789012);

INSERT INTO rental (day_cost, start_date, days_quantity, car_id, client_id) VALUES
(100.00, '2024-12-01', 5, 1, 1),
(150.00, '2024-12-05', 3, 2, 2),
(125.00, '2024-12-10', 7, 3, 3);
