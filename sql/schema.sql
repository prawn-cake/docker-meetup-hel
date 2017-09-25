-- Database schema

-- Create users and databases
CREATE USER worker WITH PASSWORD 'worker';
CREATE DATABASE meetup OWNER 'worker';
GRANT ALL PRIVILEGES ON DATABASE meetup to worker;

-- Tables

-- Connect to the database first (needed for docker-compose automation)
\connect meetup

CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    data JSONB
);


-- Grant permissions for the worker user
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO worker;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO worker;