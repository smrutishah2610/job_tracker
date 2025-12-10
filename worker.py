"""
Job Tracker - Cloudflare Python Worker with D1 Database
========================================================
URL: https://smrutishah.com/jobtracking

Routes:
  GET  /jobtracking                    → Main dashboard UI
  GET  /jobtracking/login              → Login page
  POST /jobtracking/api/auth/register  → Register user
  POST /jobtracking/api/auth/login     → Login user
  POST /jobtracking/api/auth/logout    → Logout user
  GET  /jobtracking/api/jobs           → List all jobs
  POST /jobtracking/api/jobs           → Create job
  PUT  /jobtracking/api/jobs/:id       → Update job
  DELETE /jobtracking/api/jobs/:id     → Delete job
  GET  /jobtracking/api/jobs/stats     → Get status counts
"""

from js import Response, Object
import json
import hashlib
import secrets
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_PATH = "/jobtracking"
DB = None  # D1 binding, set in on_fetch

# ============================================================================
# HTML TEMPLATES (embedded for simplicity)
# ============================================================================

LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Job Tracker - Login</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'DM Sans',sans-serif;background:#0a0a0f;min-height:100vh;display:flex}
    .left{display:none;width:45%;background:linear-gradient(160deg,#1a1a2e,#0f0f1a);padding:60px}
    @media(min-width:1024px){.left{display:flex;flex-direction:column;justify-content:center}}
    .logo{display:flex;align-items:center;gap:14px;margin-bottom:48px}
    .logo-icon{width:52px;height:52px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:14px;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 32px rgba(99,102,241,0.3)}
    .logo-icon svg{width:28px;height:28px;fill:#fff}
    .logo span{font-family:'Space Grotesk',sans-serif;font-size:26px;font-weight:700;color:#fff}
    .tagline{font-family:'Space Grotesk',sans-serif;font-size:48px;font-weight:700;color:#fff;line-height:1.15;margin-bottom:24px}
    .tagline em{font-style:normal;background:linear-gradient(135deg,#6366f1,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
    .desc{font-size:17px;color:rgba(255,255,255,0.5);line-height:1.7;max-width:400px}
    .right{flex:1;display:flex;align-items:center;justify-content:center;padding:40px 24px}
    .form-wrap{width:100%;max-width:420px}
    .mobile-logo{display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:40px}
    @media(min-width:1024px){.mobile-logo{display:none}}
    .mobile-logo .icon{width:44px;height:44px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:12px;display:flex;align-items:center;justify-content:center}
    .mobile-logo .icon svg{width:24px;height:24px;fill:#fff}
    .mobile-logo span{font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:700;color:#fff}
    .header{text-align:center;margin-bottom:36px}
    .header h1{font-family:'Space Grotesk',sans-serif;font-size:28px;font-weight:700;color:#fff;margin-bottom:10px}
    .header p{color:rgba(255,255,255,0.45);font-size:15px}
    .tabs{display:flex;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:5px;margin-bottom:32px}
    .tab{flex:1;padding:14px;border:none;background:transparent;color:rgba(255,255,255,0.5);font-family:'DM Sans',sans-serif;font-size:15px;font-weight:600;border-radius:10px;cursor:pointer;transition:all 0.25s}
    .tab.active{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;box-shadow:0 4px 20px rgba(99,102,241,0.35)}
    .alert{padding:14px 18px;border-radius:12px;margin-bottom:24px;font-size:14px;display:none}
    .alert.error{display:block;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);color:#f87171}
    .alert.success{display:block;background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.2);color:#4ade80}
    .form{display:none}
    .form.active{display:block;animation:fadeIn 0.3s ease}
    @keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
    .row{display:flex;gap:16px}
    .row .group{flex:1}
    .group{margin-bottom:20px}
    .group label{display:block;color:rgba(255,255,255,0.7);font-size:13px;font-weight:600;margin-bottom:10px}
    .group input{width:100%;padding:14px 18px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;color:#fff;font-family:'DM Sans',sans-serif;font-size:15px;transition:all 0.25s}
    .group input::placeholder{color:rgba(255,255,255,0.3)}
    .group input:focus{outline:none;border-color:#6366f1;background:rgba(99,102,241,0.05);box-shadow:0 0 0 3px rgba(99,102,241,0.1)}
    .btn{width:100%;padding:16px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border:none;border-radius:12px;color:#fff;font-family:'DM Sans',sans-serif;font-size:16px;font-weight:600;cursor:pointer;transition:all 0.3s;box-shadow:0 8px 30px rgba(99,102,241,0.3);margin-top:8px}
    .btn:hover{transform:translateY(-2px);box-shadow:0 12px 40px rgba(99,102,241,0.4)}
    footer{text-align:center;margin-top:36px;color:rgba(255,255,255,0.35);font-size:13px}
  </style>
</head>
<body>
  <div class="left">
    <div class="logo">
      <div class="logo-icon"><svg viewBox="0 0 24 24"><path d="M20 6h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-6 0h-4V4h4v2z"/></svg></div>
      <span>Job Tracker</span>
    </div>
    <h2 class="tagline">Land your<br><em>dream job</em><br>faster.</h2>
    <p class="desc">Track every application, stay organized, and never miss an opportunity.</p>
  </div>
  <div class="right">
    <div class="form-wrap">
      <div class="mobile-logo">
        <div class="icon"><svg viewBox="0 0 24 24"><path d="M20 6h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-6 0h-4V4h4v2z"/></svg></div>
        <span>Job Tracker</span>
      </div>
      <div class="header">
        <h1 id="title">Welcome back</h1>
        <p id="subtitle">Sign in to continue</p>
      </div>
      <div id="alert" class="alert"></div>
      <div class="tabs">
        <button class="tab active" onclick="showForm('login')">Sign In</button>
        <button class="tab" onclick="showForm('register')">Sign Up</button>
      </div>
      <form id="login-form" class="form active" onsubmit="login(event)">
        <div class="group"><label>Username</label><input type="text" id="l-user" placeholder="Enter username" required></div>
        <div class="group"><label>Password</label><input type="password" id="l-pass" placeholder="Enter password" required></div>
        <button type="submit" class="btn">Sign In</button>
      </form>
      <form id="register-form" class="form" onsubmit="register(event)">
        <div class="row">
          <div class="group"><label>Full Name</label><input type="text" id="r-name" placeholder="Your name" required></div>
          <div class="group"><label>Username</label><input type="text" id="r-user" placeholder="Username" required></div>
        </div>
        <div class="group"><label>Email (optional)</label><input type="email" id="r-email" placeholder="your@email.com"></div>
        <div class="row">
          <div class="group"><label>Password</label><input type="password" id="r-pass" placeholder="Min 6 chars" required></div>
          <div class="group"><label>Confirm</label><input type="password" id="r-conf" placeholder="Repeat" required></div>
        </div>
        <button type="submit" class="btn">Create Account</button>
      </form>
      <footer>© 2025 Job Tracker. Built by Smruti Shah</footer>
    </div>
  </div>
  <script>
    const B='/jobtracking';
    function showForm(t){
      document.querySelectorAll('.tab').forEach((e,i)=>e.classList.toggle('active',t==='login'?i===0:i===1));
      document.getElementById('login-form').classList.toggle('active',t==='login');
      document.getElementById('register-form').classList.toggle('active',t==='register');
      document.getElementById('title').textContent=t==='login'?'Welcome back':'Create account';
      document.getElementById('subtitle').textContent=t==='login'?'Sign in to continue':'Start your job search';
      document.getElementById('alert').className='alert';
    }
    function showAlert(m,t){const e=document.getElementById('alert');e.textContent=m;e.className='alert '+t}
    async function login(e){
      e.preventDefault();
      const u=document.getElementById('l-user').value,p=document.getElementById('l-pass').value;
      try{
        const r=await fetch(B+'/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})});
        const d=await r.json();
        if(d.success){localStorage.setItem('token',d.token);localStorage.setItem('user',JSON.stringify(d.user));window.location.href=B}
        else showAlert(d.error||'Login failed','error')
      }catch(err){showAlert('Connection error','error')}
    }
    async function register(e){
      e.preventDefault();
      const n=document.getElementById('r-name').value,u=document.getElementById('r-user').value,em=document.getElementById('r-email').value,p=document.getElementById('r-pass').value,c=document.getElementById('r-conf').value;
      if(p!==c){showAlert('Passwords do not match','error');return}
      try{
        const r=await fetch(B+'/api/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n,username:u,email:em,password:p})});
        const d=await r.json();
        if(d.success){localStorage.setItem('token',d.token);localStorage.setItem('user',JSON.stringify(d.user));window.location.href=B}
        else showAlert(d.error||'Registration failed','error')
      }catch(err){showAlert('Connection error','error')}
    }
    if(localStorage.getItem('token'))window.location.href=B;
  </script>
</body>
</html>"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Job Tracker</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    :root{--bg:#0a0a0f;--card:rgba(255,255,255,0.02);--border:rgba(255,255,255,0.06);--text:#fff;--muted:rgba(255,255,255,0.4);--accent:#6366f1}
    body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
    .nav{background:rgba(10,10,15,0.8);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:16px 0;position:sticky;top:0;z-index:1000}
    .nav-inner{max-width:1400px;margin:0 auto;padding:0 24px;display:flex;justify-content:space-between;align-items:center}
    .brand{display:flex;align-items:center;gap:12px;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.4rem;color:var(--text);text-decoration:none}
    .brand-icon{width:40px;height:40px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:12px;display:flex;align-items:center;justify-content:center}
    .brand-icon svg{width:22px;height:22px;fill:#fff}
    .user-area{display:flex;align-items:center;gap:16px}
    .user-badge{display:flex;align-items:center;gap:10px;background:var(--card);border:1px solid var(--border);padding:8px 18px;border-radius:50px;font-weight:500}
    .avatar{width:32px;height:32px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:14px}
    .logout-btn{background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);color:#f87171;padding:10px 22px;border-radius:10px;font-weight:600;cursor:pointer;transition:all 0.25s}
    .logout-btn:hover{background:rgba(239,68,68,0.2)}
    .container{max-width:1400px;margin:0 auto;padding:32px 24px}
    .page-header{text-align:center;margin-bottom:40px}
    .page-header h1{font-family:'Space Grotesk',sans-serif;font-size:36px;font-weight:700;margin-bottom:12px}
    .page-header p{color:var(--muted);font-size:16px}
    .tabs{display:flex;gap:12px;justify-content:center;margin-bottom:32px}
    .tab{padding:12px 28px;background:var(--card);border:1px solid var(--border);border-radius:12px;color:rgba(255,255,255,0.7);font-weight:600;cursor:pointer;transition:all 0.25s}
    .tab.active{background:linear-gradient(135deg,#6366f1,#8b5cf6);border-color:transparent;color:#fff}
    .filters{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:24px}
    .filter{background:var(--card);border:1px solid var(--border);color:rgba(255,255,255,0.6);padding:10px 18px;border-radius:50px;font-weight:500;font-size:14px;cursor:pointer;transition:all 0.25s;display:flex;align-items:center;gap:8px}
    .filter:hover{background:rgba(255,255,255,0.05);color:var(--text)}
    .filter.active{background:linear-gradient(135deg,#6366f1,#8b5cf6);border-color:transparent;color:#fff}
    .filter .cnt{background:rgba(255,255,255,0.15);padding:2px 8px;border-radius:20px;font-size:12px}
    .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:20px}
    .card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;cursor:pointer;transition:all 0.25s}
    .card:hover{background:rgba(255,255,255,0.04);border-color:rgba(99,102,241,0.3);transform:translateY(-2px)}
    .card-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px}
    .card-title{font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:600;margin-bottom:4px}
    .card-company{color:rgba(255,255,255,0.7);font-size:14px}
    .badge{padding:6px 12px;border-radius:50px;font-size:12px;font-weight:600;text-transform:uppercase}
    .badge-applied{background:rgba(59,130,246,0.15);color:#60a5fa}
    .badge-interview{background:rgba(245,158,11,0.15);color:#fbbf24}
    .badge-accepted{background:rgba(34,197,94,0.15);color:#4ade80}
    .badge-declined{background:rgba(239,68,68,0.15);color:#f87171}
    .badge-pending{background:rgba(107,114,128,0.15);color:#9ca3af}
    .card-meta{display:flex;gap:20px;color:var(--muted);font-size:13px}
    .empty{text-align:center;padding:80px 20px}
    .empty h3{font-family:'Space Grotesk',sans-serif;font-size:24px;margin-bottom:12px}
    .empty p{color:var(--muted);margin-bottom:24px}
    .form-panel{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:40px;display:none}
    .form-panel.active{display:block}
    .form-grid{display:grid;grid-template-columns:1fr 1fr;gap:40px}
    @media(max-width:768px){.form-grid{grid-template-columns:1fr}}
    .section h3{font-family:'Space Grotesk',sans-serif;font-size:18px;margin-bottom:24px;padding-bottom:12px;border-bottom:1px solid var(--border)}
    .field{margin-bottom:20px}
    .field label{display:block;color:rgba(255,255,255,0.7);font-size:13px;font-weight:600;margin-bottom:10px}
    .field input,.field select,.field textarea{width:100%;padding:14px 18px;background:var(--card);border:1px solid var(--border);border-radius:12px;color:var(--text);font-family:'DM Sans',sans-serif;font-size:15px;transition:all 0.25s}
    .field input:focus,.field select:focus,.field textarea:focus{outline:none;border-color:var(--accent);background:rgba(99,102,241,0.05)}
    .field select{appearance:none;background-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23888' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e");background-repeat:no-repeat;background-position:right 16px center;background-size:16px 12px}
    .field select option{background:#1a1a2e}
    .form-actions{display:flex;gap:16px;margin-top:32px;padding-top:32px;border-top:1px solid var(--border)}
    .btn-primary{padding:14px 36px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border:none;border-radius:12px;color:#fff;font-weight:600;cursor:pointer;transition:all 0.3s;box-shadow:0 8px 25px rgba(99,102,241,0.3)}
    .btn-primary:hover{transform:translateY(-2px);box-shadow:0 12px 35px rgba(99,102,241,0.4)}
    .btn-secondary{padding:14px 28px;background:transparent;border:1px solid var(--border);border-radius:12px;color:rgba(255,255,255,0.7);font-weight:600;cursor:pointer;transition:all 0.25s}
    .btn-secondary:hover{background:var(--card);color:var(--text)}
    .modal{position:fixed;top:0;left:0;right:0;bottom:0;z-index:2000;display:none;align-items:center;justify-content:center;padding:20px}
    .modal.active{display:flex}
    .modal-bg{position:absolute;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.7);backdrop-filter:blur(4px)}
    .modal-box{position:relative;background:#12121a;border:1px solid var(--border);border-radius:20px;width:100%;max-width:600px;max-height:90vh;overflow-y:auto}
    .modal-head{display:flex;justify-content:space-between;align-items:flex-start;padding:24px 28px;border-bottom:1px solid var(--border)}
    .modal-head h2{font-family:'Space Grotesk',sans-serif;font-size:22px}
    .modal-head p{color:var(--muted);margin-top:4px}
    .modal-close{background:none;border:none;color:var(--muted);font-size:28px;cursor:pointer}
    .modal-body{padding:28px}
    .detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:28px;padding-bottom:28px;border-bottom:1px solid var(--border)}
    .detail-item{display:flex;flex-direction:column;gap:6px}
    .detail-label{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase}
    .detail-value{color:rgba(255,255,255,0.85)}
    .detail-section{margin-bottom:24px}
    .detail-section h4{font-size:14px;color:var(--muted);margin-bottom:12px;text-transform:uppercase}
    .detail-content{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 20px;color:rgba(255,255,255,0.8);font-size:14px;line-height:1.7;max-height:150px;overflow-y:auto;white-space:pre-wrap}
    .modal-foot{display:flex;gap:12px;padding:20px 28px;border-top:1px solid var(--border)}
    .btn-edit{background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);padding:10px 20px;border-radius:10px;font-weight:600;cursor:pointer}
    .btn-delete{background:rgba(239,68,68,0.15);color:#f87171;border:1px solid rgba(239,68,68,0.3);padding:10px 20px;border-radius:10px;font-weight:600;cursor:pointer}
    footer{text-align:center;padding:24px;border-top:1px solid var(--border);color:var(--muted);font-size:14px;margin-top:60px}
    .hidden{display:none!important}
  </style>
</head>
<body>
  <nav class="nav">
    <div class="nav-inner">
      <a class="brand" href="/jobtracking">
        <span class="brand-icon"><svg viewBox="0 0 24 24"><path d="M20 6h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-6 0h-4V4h4v2z"/></svg></span>
        Job Tracker
      </a>
      <div class="user-area">
        <div class="user-badge"><span class="avatar" id="avatar">S</span><span id="uname">User</span></div>
        <button class="logout-btn" onclick="logout()">Logout</button>
      </div>
    </div>
  </nav>
  <div class="container">
    <div class="page-header"><h1>My Applications</h1><p>Track and manage all your job applications</p></div>
    <div class="tabs">
      <button class="tab active" onclick="showTab('list')">My Jobs</button>
      <button class="tab" onclick="showTab('add')">+ Add Job</button>
    </div>
    <div id="list-tab">
      <div class="filters" id="filters"></div>
      <div class="grid" id="jobs"></div>
      <div id="empty" class="empty hidden"><h3>No applications yet</h3><p>Start tracking by adding your first application</p><button class="btn-primary" onclick="showTab('add')">+ Add Application</button></div>
    </div>
    <div id="add-tab" class="form-panel">
      <h2 id="form-title" style="font-family:'Space Grotesk',sans-serif;font-size:24px;margin-bottom:28px;color:#fff">Add New Application</h2>
      <form id="job-form" onsubmit="submitJob(event)">
        <input type="hidden" id="edit-id">
        <div class="form-grid">
          <div class="section">
            <h3>Job Information</h3>
            <div class="field"><label>Position *</label><input type="text" id="f-position" placeholder="e.g. Software Engineer" required></div>
            <div class="field"><label>Company *</label><input type="text" id="f-company" placeholder="e.g. Google" required></div>
            <div class="field"><label>Contact</label><input type="text" id="f-contact" placeholder="e.g. John Doe - Recruiter"></div>
            <div class="field"><label>Source *</label><input type="text" id="f-source" placeholder="e.g. LinkedIn" required></div>
            <div class="field"><label>Date Applied *</label><input type="date" id="f-date" required></div>
          </div>
          <div class="section">
            <h3>Details</h3>
            <div class="field">
              <label>Status *</label>
              <select id="f-status" required>
                <option value="">Select Status</option>
                <option value="Applied">Applied</option>
                <option value="1st Round Interview">1st Round Interview</option>
                <option value="2nd Round Interview">2nd Round Interview</option>
                <option value="Offer Accepted">Offer Accepted</option>
                <option value="Application Declined">Application Declined</option>
                <option value="Offer Letter Declined">Offer Letter Declined</option>
                <option value="Need to Apply">Need to Apply</option>
              </select>
            </div>
            <div class="field"><label>Description</label><textarea id="f-desc" rows="4" placeholder="Job description..."></textarea></div>
            <div class="field"><label>Notes</label><textarea id="f-notes" rows="3" placeholder="Your notes..."></textarea></div>
          </div>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-primary" id="submit-btn">Submit</button>
          <button type="button" class="btn-secondary" onclick="resetForm()">Cancel</button>
        </div>
      </form>
    </div>
  </div>
  <div id="modal" class="modal">
    <div class="modal-bg" onclick="closeModal()"></div>
    <div class="modal-box">
      <div class="modal-head">
        <div><h2 id="m-title">Title</h2><p id="m-company">Company</p></div>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <div class="detail-grid">
          <div class="detail-item"><span class="detail-label">Status</span><span id="m-status" class="badge">Applied</span></div>
          <div class="detail-item"><span class="detail-label">Applied</span><span id="m-date" class="detail-value">-</span></div>
          <div class="detail-item"><span class="detail-label">Source</span><span id="m-source" class="detail-value">-</span></div>
          <div class="detail-item"><span class="detail-label">Contact</span><span id="m-contact" class="detail-value">-</span></div>
        </div>
        <div id="m-desc-sec" class="detail-section"><h4>Description</h4><div id="m-desc" class="detail-content"></div></div>
        <div id="m-notes-sec" class="detail-section"><h4>Notes</h4><div id="m-notes" class="detail-content"></div></div>
      </div>
      <div class="modal-foot">
        <button class="btn-edit" onclick="editCurrent()">Edit</button>
        <button class="btn-delete" onclick="deleteCurrent()">Delete</button>
        <button class="btn-secondary" onclick="closeModal()">Close</button>
      </div>
    </div>
  </div>
  <footer>© 2025 Job Tracker. Built by Smruti Shah</footer>
  <script>
    const B='/jobtracking',T=localStorage.getItem('token'),U=JSON.parse(localStorage.getItem('user')||'{}');
    let jobs=[],stats={},filter='all',currentId=null;
    if(!T){window.location.href=B+'/login'}else{document.getElementById('uname').textContent=U.name||'User';document.getElementById('avatar').textContent=(U.name||'U')[0].toUpperCase()}
    document.getElementById('f-date').valueAsDate=new Date();
    loadJobs();

    function showTab(t,isEdit){
      document.querySelectorAll('.tab').forEach((e,i)=>e.classList.toggle('active',t==='list'?i===0:i===1));
      document.getElementById('list-tab').classList.toggle('hidden',t!=='list');
      document.getElementById('add-tab').classList.toggle('active',t==='add');
      if(t==='add'&&!isEdit)resetForm();
    }
    async function loadJobs(){
      try{
        const jr=await fetch(B+'/api/jobs',{headers:{Authorization:'Bearer '+T}});
        const jd=await jr.json();
        if(jd.success){
          jobs=jd.jobs||[];
          updateStats();
        }
        renderFilters();renderJobs();
      }catch(e){console.error(e)}
    }
    function updateStats(){
      stats={All:jobs.length};
      jobs.forEach(j=>{stats[j.status]=(stats[j.status]||0)+1});
    }
    function renderFilters(){
      const s=['all','Applied','1st Round Interview','2nd Round Interview','Offer Accepted','Application Declined','Need to Apply'];
      document.getElementById('filters').innerHTML=s.map(x=>{
        const c=x==='all'?stats.All:(stats[x]||0);
        return '<button class="filter '+(filter===x?'active':'')+'" onclick="setFilter(\\''+x+'\\')">'+(x==='all'?'All':x)+' <span class="cnt">'+c+'</span></button>';
      }).join('');
    }
    function setFilter(f){filter=f;renderFilters();renderJobs()}
    function renderJobs(){
      const f=filter==='all'?jobs:jobs.filter(j=>j.status===filter);
      if(!f.length){document.getElementById('jobs').innerHTML='';document.getElementById('empty').classList.remove('hidden');return}
      document.getElementById('empty').classList.add('hidden');
      document.getElementById('jobs').innerHTML=f.map(j=>{
        if(!j.id){console.error('Job without ID:',j);return '';}
        return '<div class="card" onclick="openModal('+j.id+')"><div class="card-head"><div><div class="card-title">'+esc(j.position)+'</div><div class="card-company">'+esc(j.company_name)+'</div></div><span class="badge badge-'+badgeClass(j.status)+'">'+j.status+'</span></div><div class="card-meta"><span>📅 '+j.application_date+'</span><span>📍 '+esc(j.source)+'</span></div></div>';
      }).join('');
    }
    function badgeClass(s){if(s.includes('Interview'))return'interview';if(s.includes('Accepted'))return'accepted';if(s.includes('Declined'))return'declined';if(s.includes('Need'))return'pending';return'applied'}
    function openModal(id){
      if(!id||id===null||id===undefined){console.error('Invalid job ID:',id);return;}
      const j=jobs.find(x=>x.id===id);
      if(!j){console.error('Job not found for ID:',id);return;}
      currentId=id;
      console.log('Opening modal for job:',id,j);
      document.getElementById('m-title').textContent=j.position;
      document.getElementById('m-company').textContent=j.company_name;
      document.getElementById('m-status').textContent=j.status;
      document.getElementById('m-status').className='badge badge-'+badgeClass(j.status);
      document.getElementById('m-date').textContent=j.application_date;
      document.getElementById('m-source').textContent=j.source;
      document.getElementById('m-contact').textContent=j.contact||'-';
      document.getElementById('m-desc-sec').classList.toggle('hidden',!j.description);
      document.getElementById('m-desc').textContent=j.description||'';
      document.getElementById('m-notes-sec').classList.toggle('hidden',!j.notes);
      document.getElementById('m-notes').textContent=j.notes||'';
      document.getElementById('modal').classList.add('active');
    }
    function closeModal(){document.getElementById('modal').classList.remove('active');currentId=null}
    function editCurrent(){
      const editId=currentId;  // Save before closing modal
      const j=jobs.find(x=>x.id===editId);
      if(!j){console.error('Job not found:',editId);return;}
      closeModal();  // This sets currentId to null, but we have editId saved
      document.getElementById('edit-id').value=String(editId);
      document.getElementById('f-position').value=j.position||'';
      document.getElementById('f-company').value=j.company_name||'';
      document.getElementById('f-contact').value=j.contact||'';
      document.getElementById('f-source').value=j.source||'';
      document.getElementById('f-date').value=j.application_date||'';
      document.getElementById('f-status').value=j.status||'';
      document.getElementById('f-desc').value=j.description||'';
      document.getElementById('f-notes').value=j.notes||'';
      document.getElementById('submit-btn').textContent='Update Job';
      document.getElementById('form-title').textContent='Edit Application: '+j.position;
      console.log('Editing job:',editId,j);
      showTab('add',true);
    }
    async function deleteCurrent(){
      if(!confirm('Delete this job?'))return;
      try{
        const r=await fetch(B+'/api/jobs/'+currentId,{method:'DELETE',headers:{Authorization:'Bearer '+T}});
        const d=await r.json();
        if(d.success){
          closeModal();
          jobs=jobs.filter(j=>j.id!==currentId);
          updateStats();
          renderFilters();
          renderJobs();
        }else alert(d.error||'Failed')
      }catch(e){alert('Error')}
    }
    async function submitJob(e){
      e.preventDefault();
      const id=document.getElementById('edit-id').value.trim();
      const data={
        position:document.getElementById('f-position').value,
        company_name:document.getElementById('f-company').value,
        contact:document.getElementById('f-contact').value,
        source:document.getElementById('f-source').value,
        application_date:document.getElementById('f-date').value,
        status:document.getElementById('f-status').value,
        description:document.getElementById('f-desc').value,
        notes:document.getElementById('f-notes').value
      };
      const isUpdate=id&&id!==''&&id!=='null'&&id!=='undefined';
      console.log(isUpdate?'Updating job '+id:'Creating new job',{id,isUpdate});
      if(isUpdate&&(!id||id==='null'||id==='undefined')){
        console.error('Invalid job ID for update:',id);
        alert('Error: Invalid job ID');
        return;
      }
      try{
        const url=isUpdate?B+'/api/jobs/'+id:B+'/api/jobs';
        const r=await fetch(url,{method:isUpdate?'PUT':'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+T},body:JSON.stringify(data)});
        const d=await r.json();
        if(d.success){
          if(isUpdate){
            // Update existing job in local array
            const jobId=parseInt(id);
            const idx=jobs.findIndex(j=>j.id===jobId);
            console.log('Found job at index:',idx,'for id:',jobId);
            if(idx!==-1){
              const oldJob=jobs[idx];
              jobs[idx]={
                id:jobId,
                user_id:oldJob.user_id,
                position:data.position,
                company_name:data.company_name,
                description:data.description,
                contact:data.contact,
                source:data.source,
                application_date:data.application_date,
                status:data.status,
                notes:data.notes,
                resume_url:oldJob.resume_url,
                created_at:oldJob.created_at,
                updated_at:new Date().toISOString().replace('T',' ').split('.')[0]
              };
              console.log('Updated job:',jobs[idx]);
            }else{
              console.error('Job not found in array! Reloading...');
              await loadJobs();
            }
            updateStats();
            renderFilters();
            renderJobs();
          }else{
            // For new jobs, reload to get the ID from server
            await loadJobs();
          }
          resetForm();
          showTab('list');
        }else alert(d.error||'Failed')
      }catch(e){console.error(e);alert('Error')}
    }
    function resetForm(){
      document.getElementById('job-form').reset();
      document.getElementById('edit-id').value='';
      document.getElementById('f-date').valueAsDate=new Date();
      document.getElementById('submit-btn').textContent='Submit';
      document.getElementById('form-title').textContent='Add New Application';
    }
    function logout(){localStorage.removeItem('token');localStorage.removeItem('user');window.location.href=B+'/login'}
    function esc(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML}
  </script>
</body>
</html>"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def json_response(data, status=200):
    """Create JSON response with CORS"""
    return Response.new(
        json.dumps(data),
        status=status,
        headers=Object.fromEntries([
            ["Content-Type", "application/json"],
            ["Access-Control-Allow-Origin", "*"],
            ["Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"],
            ["Access-Control-Allow-Headers", "Content-Type, Authorization"],
        ])
    )

def html_response(html, status=200):
    """Create HTML response"""
    return Response.new(
        html,
        status=status,
        headers=Object.fromEntries([["Content-Type", "text/html; charset=utf-8"]])
    )

def error(msg, status=400):
    """Create error response"""
    return json_response({"success": False, "error": msg}, status)

def success(data=None):
    """Create success response"""
    resp = {"success": True}
    if data:
        resp.update(data)
    return json_response(resp)

def hash_password(password):
    """Hash password with SHA256 + salt"""
    salt = "jobtracker_d1_2024"
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password"""
    return hash_password(password) == hashed

def generate_token():
    """Generate session token"""
    return secrets.token_hex(32)

def parse_path(url):
    """Extract path from URL"""
    if "//" in url:
        path = "/" + url.split("//")[1].split("/", 1)[1] if "/" in url.split("//")[1] else "/"
    else:
        path = url
    return path.split("?")[0]

def get_path_param(path, prefix):
    """Extract ID from path like /jobtracking/api/jobs/123"""
    if path.startswith(prefix):
        remainder = path[len(prefix):]
        if remainder.startswith("/"):
            remainder = remainder[1:]
        parts = remainder.split("/")
        if parts and parts[0] and parts[0] != 'null' and parts[0] != 'undefined' and parts[0].isdigit():
            return int(parts[0])
    return None

# ============================================================================
# DATABASE OPERATIONS (D1)
# ============================================================================

def js_to_py(obj):
    """Convert JsProxy object to Python dict"""
    if obj is None:
        return None
    # Convert JsProxy to Python using to_py()
    if hasattr(obj, 'to_py'):
        return obj.to_py()
    return obj

async def db_execute(sql, params=None):
    """Execute SQL and return result"""
    if params:
        result = await DB.prepare(sql).bind(*params).run()
    else:
        result = await DB.prepare(sql).run()
    return result

async def db_query(sql, params=None):
    """Query SQL and return rows as Python list of dicts"""
    if params:
        result = await DB.prepare(sql).bind(*params).all()
    else:
        result = await DB.prepare(sql).all()
    
    # Convert results to Python
    if hasattr(result, 'results'):
        results = result.results
        if hasattr(results, 'to_py'):
            return results.to_py()
        return list(results) if results else []
    return []

async def db_first(sql, params=None):
    """Query SQL and return first row as Python dict"""
    if params:
        result = await DB.prepare(sql).bind(*params).first()
    else:
        result = await DB.prepare(sql).first()
    return js_to_py(result)

# ============================================================================
# AUTH HANDLERS
# ============================================================================

async def get_user_from_token(request):
    """Get user from Authorization header"""
    auth = request.headers.get("Authorization") or ""
    if not auth.startswith("Bearer "):
        return None
    token = auth[7:]
    
    session = await db_first(
        "SELECT s.user_id, u.username, u.name FROM sessions s JOIN users u ON s.user_id = u.id WHERE s.token = ?",
        [token]
    )
    return session

async def handle_register(request):
    """POST /jobtracking/api/auth/register"""
    try:
        body = json.loads(await request.text())
        username = (body.get("username") or "").strip()
        password = body.get("password") or ""
        name = (body.get("name") or "").strip()
        email = (body.get("email") or "").strip()
        
        if not username or not password or not name:
            return error("Username, password, and name are required")
        if len(password) < 6:
            return error("Password must be at least 6 characters")
        
        # Check existing user
        existing = await db_first("SELECT id FROM users WHERE username = ?", [username])
        if existing:
            return error("Username already exists")
        
        # Create user
        password_hash = hash_password(password)
        await db_execute(
            "INSERT INTO users (username, password_hash, name, email) VALUES (?, ?, ?, ?)",
            [username, password_hash, name, email]
        )
        
        # Get new user
        user = await db_first("SELECT id, username, name, email FROM users WHERE username = ?", [username])
        
        # Create session
        token = generate_token()
        await db_execute(
            "INSERT INTO sessions (user_id, token) VALUES (?, ?)",
            [user["id"], token]
        )
        
        return success({
            "token": token,
            "user": {"id": user["id"], "username": user["username"], "name": user["name"]}
        })
    except Exception as e:
        return error(str(e), 500)

async def handle_login(request):
    """POST /jobtracking/api/auth/login"""
    try:
        body = json.loads(await request.text())
        username = (body.get("username") or "").strip()
        password = body.get("password") or ""
        
        if not username or not password:
            return error("Username and password required")
        
        user = await db_first("SELECT id, username, name, password_hash FROM users WHERE username = ?", [username])
        if not user or not verify_password(password, user["password_hash"]):
            return error("Invalid username or password", 401)
        
        # Create session
        token = generate_token()
        await db_execute(
            "INSERT INTO sessions (user_id, token) VALUES (?, ?)",
            [user["id"], token]
        )
        
        return success({
            "token": token,
            "user": {"id": user["id"], "username": user["username"], "name": user["name"]}
        })
    except Exception as e:
        return error(str(e), 500)

async def handle_logout(request):
    """POST /jobtracking/api/auth/logout"""
    auth = request.headers.get("Authorization") or ""
    if auth.startswith("Bearer "):
        token = auth[7:]
        await db_execute("DELETE FROM sessions WHERE token = ?", [token])
    return success({"message": "Logged out"})

# ============================================================================
# JOB HANDLERS
# ============================================================================

async def handle_list_jobs(request):
    """GET /jobtracking/api/jobs"""
    user = await get_user_from_token(request)
    if not user:
        return error("Unauthorized", 401)
    
    try:
        jobs = await db_query(
            "SELECT * FROM jobs WHERE user_id = ? ORDER BY application_date DESC",
            [user["user_id"]]
        )
        return success({"jobs": list(jobs)})
    except Exception as e:
        return error(str(e), 500)

async def handle_create_job(request):
    """POST /jobtracking/api/jobs"""
    user = await get_user_from_token(request)
    if not user:
        return error("Unauthorized", 401)
    
    try:
        body = json.loads(await request.text())
        
        required = ["position", "company_name", "source", "application_date", "status"]
        for field in required:
            if not body.get(field):
                return error(f"{field} is required")
        
        await db_execute(
            """INSERT INTO jobs (user_id, position, company_name, description, contact, source, application_date, status, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                user["user_id"],
                body.get("position"),
                body.get("company_name"),
                body.get("description", ""),
                body.get("contact", ""),
                body.get("source"),
                body.get("application_date"),
                body.get("status"),
                body.get("notes", "")
            ]
        )
        
        return success({"message": "Job created"})
    except Exception as e:
        return error(str(e), 500)

async def handle_update_job(request, job_id):
    """PUT /jobtracking/api/jobs/:id"""
    user = await get_user_from_token(request)
    if not user:
        return error("Unauthorized", 401)
    
    try:
        # Verify ownership
        job = await db_first("SELECT id FROM jobs WHERE id = ? AND user_id = ?", [job_id, user["user_id"]])
        if not job:
            return error("Job not found", 404)
        
        body = json.loads(await request.text())
        
        await db_execute(
            """UPDATE jobs SET 
               position = ?, company_name = ?, description = ?, contact = ?, 
               source = ?, application_date = ?, status = ?, notes = ?,
               updated_at = datetime('now')
               WHERE id = ? AND user_id = ?""",
            [
                body.get("position"),
                body.get("company_name"),
                body.get("description", ""),
                body.get("contact", ""),
                body.get("source"),
                body.get("application_date"),
                body.get("status"),
                body.get("notes", ""),
                job_id,
                user["user_id"]
            ]
        )
        
        return success({"message": "Job updated"})
    except Exception as e:
        return error(str(e), 500)

async def handle_delete_job(request, job_id):
    """DELETE /jobtracking/api/jobs/:id"""
    user = await get_user_from_token(request)
    if not user:
        return error("Unauthorized", 401)
    
    try:
        result = await db_execute(
            "DELETE FROM jobs WHERE id = ? AND user_id = ?",
            [job_id, user["user_id"]]
        )
        return success({"message": "Job deleted"})
    except Exception as e:
        return error(str(e), 500)

async def handle_job_stats(request):
    """GET /jobtracking/api/jobs/stats"""
    user = await get_user_from_token(request)
    if not user:
        return error("Unauthorized", 401)
    
    try:
        # Get total count
        total = await db_first("SELECT COUNT(*) as count FROM jobs WHERE user_id = ?", [user["user_id"]])
        
        # Get counts by status
        statuses = await db_query(
            "SELECT status, COUNT(*) as count FROM jobs WHERE user_id = ? GROUP BY status",
            [user["user_id"]]
        )
        
        stats = {"All": total["count"] if total else 0}
        for s in statuses:
            stats[s["status"]] = s["count"]
        
        return success({"stats": stats})
    except Exception as e:
        return error(str(e), 500)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def on_fetch(request, env):
    """Main Worker entry point"""
    global DB
    DB = env.JOBTRACKER_DB
    
    url = request.url
    path = parse_path(url)
    method = request.method
    
    # Handle CORS preflight
    if method == "OPTIONS":
        return Response.new(
            "",
            status=204,
            headers=Object.fromEntries([
                ["Access-Control-Allow-Origin", "*"],
                ["Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"],
                ["Access-Control-Allow-Headers", "Content-Type, Authorization"],
            ])
        )
    
    # ========== HTML PAGES ==========
    
    # Dashboard
    if path == "/jobtracking" or path == "/jobtracking/":
        return html_response(DASHBOARD_HTML)
    
    # Login page
    if path == "/jobtracking/login":
        return html_response(LOGIN_HTML)
    
    # ========== AUTH API ==========
    
    if path == "/jobtracking/api/auth/register" and method == "POST":
        return await handle_register(request)
    
    if path == "/jobtracking/api/auth/login" and method == "POST":
        return await handle_login(request)
    
    if path == "/jobtracking/api/auth/logout" and method == "POST":
        return await handle_logout(request)
    
    # ========== JOBS API ==========
    
    # Stats endpoint (must be before :id matching)
    if path == "/jobtracking/api/jobs/stats" and method == "GET":
        return await handle_job_stats(request)
    
    # List / Create jobs
    if path == "/jobtracking/api/jobs":
        if method == "GET":
            return await handle_list_jobs(request)
        if method == "POST":
            return await handle_create_job(request)
    
    # Single job operations with ID
    job_id = get_path_param(path, "/jobtracking/api/jobs")
    if job_id:
        if method == "PUT":
            return await handle_update_job(request, job_id)
        if method == "DELETE":
            return await handle_delete_job(request, job_id)
    
    # ========== HEALTH CHECK ==========
    
    if path == "/jobtracking/api/health":
        return success({"status": "ok", "database": "D1"})
    
    # ========== 404 ==========
    
    return error(f"Not found: {path}", 404)
