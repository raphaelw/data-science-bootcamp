-- SQL for PostgreSQL --

CREATE TABLE IF NOT EXISTS tweets (
    'id'        SERIAL PRIMARY KEY,
    'user'      VARCHAR(100),
    'text'      VARCHAR(500),
    'timestamp' NUMERIC,
    'sentiment' NUMERIC
);
