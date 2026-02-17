-- Fix password hashes for test users
-- Password: password123

-- Delete existing users
DELETE FROM users WHERE username IN ('admin', 'testuser');

-- Insert users with correct bcrypt hashes
-- Hash 1: $2a$10$RVBXnxZaKRYfJ4GFnm2ile2FRM9yDuRSA5YVfYsnKaZc6aSz/NzM6
-- Hash 2: $2a$10$lowrW7TKE2v5nrA2/SeLB.dVDtlyDJkNWT.FRYM86sHBgVjkVUW0K

INSERT INTO users (username, email, password_hash, first_name, last_name, is_active, created_at, updated_at)
VALUES 
  ('admin', 'admin@printinghouse.local', '$2a$10$RVBXnxZaKRYfJ4GFnm2ile2FRM9yDuRSA5YVfYsnKaZc6aSz/NzM6', 'Admin', 'User', true, NOW(), NOW()),
  ('testuser', 'test@printinghouse.local', '$2a$10$lowrW7TKE2v5nrA2/SeLB.dVDtlyDJkNWT.FRYM86sHBgVjkVUW0K', 'Test', 'User', true, NOW(), NOW());

-- Verify
SELECT 
  username, 
  email, 
  CASE 
    WHEN LENGTH(password_hash) = 60 THEN '✓ OK (60 chars)'
    ELSE '✗ WRONG (' || LENGTH(password_hash) || ' chars)'
  END as hash_status
FROM users 
WHERE username IN ('admin', 'testuser');
