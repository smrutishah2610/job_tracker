-- Migration: Add resume_data column and migrate from resume_url
-- Run with: wrangler d1 execute jobtracker_db --file=./migrations/0002_add_resume_data.sql

-- Add resume_data column to store base64-encoded PDF
ALTER TABLE jobs ADD COLUMN resume_data TEXT;

-- Note: resume_url column is kept for backward compatibility but will not be used
-- The resume_data column will store the base64-encoded PDF content

