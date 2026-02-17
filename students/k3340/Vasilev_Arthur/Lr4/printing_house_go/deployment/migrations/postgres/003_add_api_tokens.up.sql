-- Add API tokens table for Bearer token authentication
BEGIN;

CREATE TABLE IF NOT EXISTS api_tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Index for token lookup (used in authentication)
CREATE INDEX idx_api_tokens_token ON api_tokens(token);
CREATE INDEX idx_api_tokens_is_active ON api_tokens(is_active);
CREATE INDEX idx_api_tokens_expires_at ON api_tokens(expires_at);

-- Insert default test token (valid for 365 days from 2026-02-16)
-- Token: test_token_12345678901234567890123456789012
-- This is for testing purposes - should be changed in production
INSERT INTO api_tokens (token, name, expires_at, is_active) VALUES
('test_token_12345678901234567890123456789012', 'Test Token', NOW() + INTERVAL '365 days', TRUE),
('admin_token_98765432109876543210987654321098', 'Admin Token', NOW() + INTERVAL '365 days', TRUE);

COMMIT;
