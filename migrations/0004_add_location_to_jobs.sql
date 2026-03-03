-- Migration: add location field to jobs
-- Run with: wrangler d1 execute jobtracker_db --file=./migrations/0004_add_location_to_jobs.sql

ALTER TABLE jobs ADD COLUMN location TEXT;
