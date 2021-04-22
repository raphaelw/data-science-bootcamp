-- SQL for PostgreSQL --

CREATE TABLE IF NOT EXISTS tweets (
    id        SERIAL PRIMARY KEY,
    user      VARCHAR(100),
    text      VARCHAR(500),
    sentiment NUMERIC
    -- ADD DATETIME !!!
);

-- Trigger to NOTIFY listeners --

