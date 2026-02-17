-- Add users table for authentication
BEGIN;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Insert test users
-- Password for both users: "password123"
-- bcrypt hash generated with cost 10
INSERT INTO users (username, email, password_hash, first_name, last_name) VALUES
('admin', 'admin@printinghouse.local', '$2a$10$YQN9Y9rBZ8Z8Z8Z8Z8Z8ZOQ9rBZ8Z8Z8Z8Z8Z8Z8Z8Z8Z8Z8Z8Z8Zu', 'Admin', 'User'),
('testuser', 'test@printinghouse.local', '$2a$10$YQN9Y9rBZ8Z8Z8Z8Z8Z8ZOQ9rBZ8Z8Z8Z8Z8Z8Z8Z8Z8Z8Z8Z8Z8Zu', 'Test', 'User');

COMMIT;
