DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS merchants;
DROP TABLE IF EXISTS tags;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    budget INT
);

CREATE TABLE merchants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    amount INT,
    user_id INT REFERENCES users(id),
    merchant_id INT REFERENCES merchants(id),
    tag_id INT REFERENCES tags(id)
);

