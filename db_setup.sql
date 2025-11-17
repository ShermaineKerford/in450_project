-- db_setup.sql
-- run inside in450db (psql: \c in450db)

SET search_path TO app;

-- Example structure: adjust column names & types to match your CSV headers
CREATE TABLE IF NOT EXISTS in450a (
  id SERIAL PRIMARY KEY,
  code VARCHAR(50) NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS in450b (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS in450c (
  id SERIAL PRIMARY KEY,
  ref_id INT,
  value NUMERIC,
  note TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for optimization (create indexes on columns you will query often)
CREATE INDEX IF NOT EXISTS idx_in450a_code ON in450a(code);
CREATE INDEX IF NOT EXISTS idx_in450b_lastname ON in450b(last_name);

-- Grant minimal privileges to app_user: SELECT, INSERT, UPDATE, DELETE on these tables
GRANT USAGE ON SCHEMA app TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA app GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
