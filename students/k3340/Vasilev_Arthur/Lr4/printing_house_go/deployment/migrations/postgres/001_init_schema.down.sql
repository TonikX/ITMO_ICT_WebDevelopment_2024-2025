-- Rollback migrations for printing_house
BEGIN;

DROP TABLE IF EXISTS distributions CASCADE;
DROP TABLE IF EXISTS printing_runs CASCADE;
DROP TABLE IF EXISTS post_offices CASCADE;
DROP TABLE IF EXISTS printing_houses CASCADE;
DROP TABLE IF EXISTS newspapers CASCADE;

COMMIT;
