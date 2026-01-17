-- secure_roles.sql
-- Creates least-privilege users/roles for the app tables in schema app

-- 1) Create roles/users
CREATE ROLE in450a LOGIN PASSWORD 'ChangeMeA!';
CREATE ROLE in450b LOGIN PASSWORD 'ChangeMeB!';
CREATE ROLE in450c LOGIN PASSWORD 'ChangeMeC!';

-- 2) Allow schema usage
GRANT USAGE ON SCHEMA app TO in450a, in450b, in450c;

-- 3) Grant table read permissions
GRANT SELECT ON app.in450a TO in450a;
GRANT SELECT ON app.in450b TO in450a;
GRANT SELECT ON app.in450c TO in450a;

GRANT SELECT ON app.in450b TO in450b;
GRANT SELECT ON app.in450c TO in450c;
