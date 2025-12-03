CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(name) > 0),
    price NUMERIC NOT NULL CHECK (price > 0)
);
