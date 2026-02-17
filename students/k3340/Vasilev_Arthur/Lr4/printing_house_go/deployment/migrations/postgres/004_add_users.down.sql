-- Rollback users table
BEGIN;

DROP TABLE IF EXISTS users;

COMMIT;
