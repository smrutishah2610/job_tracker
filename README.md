# Job Tracker

A modern job application tracking system built as a **Cloudflare Python Worker** with **D1 SQLite database**.

🔗 **Live URL**: [https://smrutishah.com/jobtracking](https://smrutishah.com/jobtracking)

---

## ✨ Features

- 🔐 **User Authentication** - Register & login with secure sessions
- 📋 **Track Applications** - Add, edit, delete job applications
- 📄 **Resume Management** - Upload and view resumes for each job application
- 🏷️ **Status Filtering** - Filter by Applied, Interview, Accepted, Declined
- 🌙 **Dark Theme UI** - Modern, responsive design
- ⚡ **D1 Database** - Cloudflare's serverless SQLite
- 📄 **Base64 Storage** - Resumes stored directly in database (free, no additional services)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Runtime | Cloudflare Workers (Python) |
| Database | Cloudflare D1 (SQLite) |
| Storage | Base64 in D1 (free, no R2 needed) |
| Frontend | Vanilla JS (embedded) |
| Auth | Token-based sessions |

---

## 📁 Project Structure

```
job_tracker/
├── worker.py              # Main Python Worker
├── wrangler.toml          # Cloudflare configuration
├── migrations/
│   └── 0001_init.sql      # D1 database schema
├── requirements.txt       # (no external deps)
├── README.md              # This file
└── _legacy_flask/         # Archived Flask version
```

---

## 🚀 Quick Start

### Prerequisites

1. [Cloudflare Account](https://dash.cloudflare.com/sign-up)
2. [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/)

```bash
npm install -g wrangler
```

### Setup

```bash
# 1. Login to Cloudflare
wrangler login

# 2. Create D1 database
wrangler d1 create jobtracker_db

# 3. Copy the database_id and update wrangler.toml
# Replace REPLACE_WITH_YOUR_DATABASE_ID with the actual ID

# 4. Run migrations to create tables
wrangler d1 execute jobtracker_db --file=./migrations/0001_init.sql

# 5. Add resume_data column (for base64 storage)
wrangler d1 execute jobtracker_db --file=./migrations/0002_add_resume_data.sql

# 6. Test locally
wrangler dev

# 7. Deploy
wrangler deploy
```

### Add Route in Cloudflare Dashboard

After deploying, add this route in your Cloudflare Dashboard:

```
smrutishah.com/jobtracking* → job-tracker
```

---

## 🔌 API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/jobtracking` | Dashboard UI |
| GET | `/jobtracking/login` | Login page |
| POST | `/jobtracking/api/auth/register` | Register user |
| POST | `/jobtracking/api/auth/login` | Login user |
| POST | `/jobtracking/api/auth/logout` | Logout user |
| GET | `/jobtracking/api/jobs` | List all jobs |
| POST | `/jobtracking/api/jobs` | Create job |
| PUT | `/jobtracking/api/jobs/:id` | Update job |
| DELETE | `/jobtracking/api/jobs/:id` | Delete job |
| GET | `/jobtracking/api/jobs/stats` | Status counts |
| POST | `/jobtracking/api/jobs/:id/resume` | Upload resume (PDF) |
| GET | `/jobtracking/api/jobs/:id/resume` | View/download resume |

---

## 📊 Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | TEXT | Unique username |
| password_hash | TEXT | Hashed password |
| name | TEXT | Display name |
| email | TEXT | Email (optional) |
| created_at | TEXT | Timestamp |

### Jobs Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key to users |
| position | TEXT | Job title |
| company_name | TEXT | Company |
| description | TEXT | Job description |
| contact | TEXT | Recruiter/contact |
| source | TEXT | Where found (LinkedIn, etc) |
| application_date | TEXT | Date applied |
| status | TEXT | Application status |
| notes | TEXT | Personal notes |
| resume_url | TEXT | Resume URL (for compatibility) |
| resume_data | TEXT | Base64-encoded PDF content |
| created_at | TEXT | Timestamp |
| updated_at | TEXT | Timestamp |

---

## 🏷️ Status Values

- `Applied`
- `1st Round Interview`
- `2nd Round Interview`
- `Offer Accepted`
- `Application Declined`
- `Offer Letter Declined`
- `Need to Apply`

---

## 🔧 Local Development

```bash
# Start local dev server
wrangler dev

# Access at: http://localhost:8787/jobtracking
```

---

## 📝 Useful Commands

```bash
# Check D1 databases
wrangler d1 list

# Execute SQL
wrangler d1 execute jobtracker_db --command="SELECT * FROM users"

# View logs
wrangler tail
```

---

## 👤 Author

**Smruti Shah**

- Website: [smrutishah.com](https://smrutishah.com)
- GitHub: [@smrutishah](https://github.com/smrutishah)

---

## 📄 License

MIT License - feel free to use for your own job tracking!
