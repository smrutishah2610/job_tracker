from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from collections import Counter

app = Flask(__name__)
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


Connection_String = "mongodb+srv://smruti2610:smruti2610@cluster0.digxvgs.mongodb.net/"
client = MongoClient(Connection_String)
db = client['demo_db']
collection = db['applications']


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
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
        "notes": data.get('notes', '') # New optional field
    }
    collection.insert_one(job_data)
    return redirect(url_for("view_jobs"))

@app.route("/view")
def view_jobs():
    sort_by = request.args.get('sort_by', 'application_date')
    status_filter = request.args.get('status_filter')

    query = {}
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

    # Calculate status counts
    all_statuses = ["Applied", "1st Round Interview", "2nd Round Interview", "Offer Accepted", "Application Declined", "Offer Letter Declined", "Need to Apply"]
    status_counts = {'All': collection.count_documents({})}
    for status in all_statuses:
        status_counts[status] = collection.count_documents({'status': status})

    return render_template("view.html", jobs=jobs, status_counts=status_counts, current_status_filter=status_filter)

@app.route("/resume/<job_id>")
def view_resume(job_id):
    job = collection.find_one({"_id": ObjectId(job_id)})
    if job:
        return send_file(job['resume_path'], as_attachment=False)
    return "Resume not found", 404

@app.route("/edit/<job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    job = collection.find_one({"_id": ObjectId(job_id)})
    if request.method == "POST":
        updated_data = {
            "position": request.form['position'],
            "company_name": request.form['company_name'],
            "description": request.form['description'],
            "contact": request.form['contact'],
            "source": request.form['source'],
            "application_date": request.form['application_date'],
            "resume_path": job['resume_path'],  # keep existing resume
            "status": request.form['status'],
            "notes": request.form.get('notes', '') # New optional field
        }
        collection.update_one({"_id": ObjectId(job_id)}, {"$set": updated_data})
        return redirect(url_for('view_jobs'))
    return render_template("index.html", job=job, editing=True, job_id=job_id)

@app.route("/delete/<job_id>")
def delete_job(job_id):
    collection.delete_one({"_id": ObjectId(job_id)})
    return redirect(url_for("view_jobs"))

@app.route("/delete_multiple", methods=["POST"])
def delete_multiple_jobs():
    job_ids = request.json.get('ids', [])
    if not job_ids:
        return jsonify({'success': False, 'error': 'No job IDs provided.'}), 400

    object_ids = [ObjectId(job_id) for job_id in job_ids]
    result = collection.delete_many({'_id': {'$in': object_ids}})

    if result.deleted_count > 0:
        return jsonify({'success': True, 'deleted_count': result.deleted_count})
    else:
        return jsonify({'success': False, 'error': 'No jobs found for the provided IDs.'}), 404

if __name__ == "__main__":
    app.run(debug=True)
