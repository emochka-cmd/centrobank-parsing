CREATE TABLE dollar_by_data(
    id SERIAL PRIMARY KEY,
    d_date DATE NOT NULL,
    dollar_rate NUMERIC (8, 3) NOT NULL
);