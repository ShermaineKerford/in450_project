-- IN450_Unit3_ShermaineKerford.sql
-- Security roles and permissions for in450db

-- 1) Use the correct database
\c in450db

-- 2) Make sure we use the app schema
SET search_path TO app;

-- 3) Optional: lock things down a bit from PUBLIC
REVOKE ALL ON SCHEMA app FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA app FROM PUBLIC;

-- 4) Drop roles if they already exist (for reruns)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'in450a') THEN
        REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA app FROM in450a;
        REVOKE USAGE ON SCHEMA app FROM in450a;
        REVOKE CONNECT ON DATABASE in450db FROM in450a;
        DROP ROLE in450a;
    END IF;

    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'in450b') THEN
        REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA app FROM in450b;
        REVOKE USAGE ON SCHEMA app FROM in450b;
        REVOKE CONNECT ON DATABASE in450db FROM in450b;
        DROP ROLE in450b;
    END IF;

    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'in450c') THEN
        REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA app FROM in450c;
        REVOKE USAGE ON SCHEMA app FROM in450c;
        REVOKE CONNECT ON DATABASE in450db FROM in450c;
        DROP ROLE in450c;
    END IF;
END
$$;

-- 5) Create roles (users) with passwords
CREATE ROLE in450a LOGIN PASSWORD 'DR$mith2007a';
CREATE ROLE in450b LOGIN PASSWORD 'DR$mith2007b';
CREATE ROLE in450c LOGIN PASSWORD 'DR$mith2007c';

-- 6) Allow them to connect to the database
GRANT CONNECT ON DATABASE in450db TO in450a, in450b, in450c;

-- 7) Allow them to use the app schema
GRANT USAGE ON SCHEMA app TO in450a, in450b, in450c;

-- 8) Table-level permissions
-- in450a user: can see ALL tables
GRANT SELECT ON app.in450a TO in450a;
GRANT SELECT ON app.in450b TO in450a;
GRANT SELECT ON app.in450c TO in450a;

-- in450b user: can only see in450b
GRANT SELECT ON app.in450b TO in450b;

-- in450c user: can only see in450c
GRANT SELECT ON app.in450c TO in450c;
