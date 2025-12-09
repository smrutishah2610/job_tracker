from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from collections import Counter
import bcrypt

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Connection_String = "mongodb+srv://smruti2610:smruti2610@cluster0.digxvgs.mongodb.net/"
client = MongoClient(Connection_String)
db = client['jobTracker']
collection = db['joblist']
users_collection = db['users']

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data.get('email', '')
        self.name = user_data.get('name', self.username)


@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template("login.html")
        
        user_data = users_collection.find_one({"username": username})
        
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
            user = User(user_data)
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validation
        if not username or not password or not name:
            flash('Username, password, and name are required.', 'error')
            return render_template("login.html", show_register=True)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template("login.html", show_register=True)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template("login.html", show_register=True)
        
        # Check if username exists
        if users_collection.find_one({"username": username}):
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template("login.html", show_register=True)
        
        # Hash password and create user
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            "username": username,
            "password": hashed_password,
            "name": name,
            "email": email
        }
        result = users_collection.insert_one(user_data)
        
        # Auto login after registration
        user_data['_id'] = result.inserted_id
        user = User(user_data)
        login_user(user)
        flash(f'Account created successfully! Welcome, {name}!', 'success')
        return redirect(url_for('home'))
    
    return render_template("login.html", show_register=True)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
@login_required
def submit():
    data = request.form
    file = request.files['resume']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    job_data = {
        "position": data['position'],
        "company_name": data['company_name'],
        "description": data['description'],
        "contact": data['contact'],
        "source": data['source'],
        "application_date": data['application_date'],
        "resume_path": filepath,
        "status": data['status'],
        "notes": data.get('notes', ''),
        "user_id": current_user.id  # Associate job with current user
    }
    collection.insert_one(job_data)
    return redirect(url_for("view_jobs"))


@app.route("/view")
@login_required
def view_jobs():
    sort_by = request.args.get('sort_by', 'application_date')
    status_filter = request.args.get('status_filter')

    # Only fetch jobs for the current user
    query = {"user_id": current_user.id}
    if status_filter and status_filter != 'All':
        query['status'] = status_filter

    jobs_cursor = collection.find(query)

    if sort_by == 'position':
        jobs_cursor = jobs_cursor.sort("position", 1)
    elif sort_by == 'company_name':
        jobs_cursor = jobs_cursor.sort("company_name", 1)
    elif sort_by == 'application_date':
        jobs_cursor = jobs_cursor.sort("application_date", -1)

    jobs = list(jobs_cursor)

    # Calculate status counts for current user only
    all_statuses = ["Applied", "1st Round Interview", "2nd Round Interview", "Offer Accepted", "Application Declined", "Offer Letter Declined", "Need to Apply"]
    status_counts = {'All': collection.count_documents({"user_id": current_user.id})}
    for status in all_statuses:
        status_counts[status] = collection.count_documents({'status': status, "user_id": current_user.id})

    return render_template("view.html", jobs=jobs, status_counts=status_counts, current_status_filter=status_filter)


@app.route("/resume/<job_id>")
@login_required
def view_resume(job_id):
    # Only allow viewing resume if job belongs to current user
    job = collection.find_one({"_id": ObjectId(job_id), "user_id": current_user.id})
    if job:
        return send_file(job['resume_path'], as_attachment=False)
    return "Resume not found", 404


@app.route("/edit/<job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    # Only allow editing if job belongs to current user
    job = collection.find_one({"_id": ObjectId(job_id), "user_id": current_user.id})
    if not job:
        flash('Job not found or access denied.', 'error')
        return redirect(url_for('view_jobs'))
    
    if request.method == "POST":
        updated_data = {
            "position": request.form['position'],
            "company_name": request.form['company_name'],
            "description": request.form['description'],
            "contact": request.form['contact'],
            "source": request.form['source'],
            "application_date": request.form['application_date'],
            "resume_path": job['resume_path'],
            "status": request.form['status'],
            "notes": request.form.get('notes', ''),
            "user_id": current_user.id  # Preserve user association
        }
        collection.update_one({"_id": ObjectId(job_id), "user_id": current_user.id}, {"$set": updated_data})
        return redirect(url_for('view_jobs'))
    return render_template("index.html", job=job, editing=True, job_id=job_id)


@app.route("/delete/<job_id>")
@login_required
def delete_job(job_id):
    # Only allow deleting if job belongs to current user
    collection.delete_one({"_id": ObjectId(job_id), "user_id": current_user.id})
    return redirect(url_for("view_jobs"))


@app.route("/delete_multiple", methods=["POST"])
@login_required
def delete_multiple_jobs():
    job_ids = request.json.get('ids', [])
    if not job_ids:
        return jsonify({'success': False, 'error': 'No job IDs provided.'}), 400

    object_ids = [ObjectId(job_id) for job_id in job_ids]
    # Only delete jobs belonging to current user
    result = collection.delete_many({'_id': {'$in': object_ids}, 'user_id': current_user.id})

    if result.deleted_count > 0:
        return jsonify({'success': True, 'deleted_count': result.deleted_count})
    else:
        return jsonify({'success': False, 'error': 'No jobs found for the provided IDs.'}), 404


if __name__ == "__main__":
    app.run(debug=True)
