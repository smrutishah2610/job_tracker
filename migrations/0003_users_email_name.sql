-- Migration: upgrade users schema from legacy username-based auth
-- Run with: wrangler d1 execute jobtracker_db --file=./migrations/0003_users_email_name.sql

-- Add new columns expected by current app code
ALTER TABLE users ADD COLUMN email TEXT;
ALTER TABLE users ADD COLUMN name TEXT;

-- Backfill from legacy username where possible
UPDATE users
SET email = COALESCE(email, username),
    name = COALESCE(name, username)
WHERE email IS NULL OR name IS NULL;

-- Add index used by auth lookups
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);
