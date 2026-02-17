-- Rollback: Remove API tokens table
BEGIN;

DROP INDEX IF EXISTS idx_api_tokens_expires_at;
DROP INDEX IF EXISTS idx_api_tokens_is_active;
DROP INDEX IF EXISTS idx_api_tokens_token;
DROP TABLE IF EXISTS api_tokens;

COMMIT;
