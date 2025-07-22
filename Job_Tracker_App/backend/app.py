from flask import Flask, render_template, request, redirect, url_for, send_file
from pymongo import MongoClient
from bson import ObjectId
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


Connection_String = "mongodb+srv://smruti2610:smruti2610@cluster0.digxvgs.mongodb.net/"
client = MongoClient(Connection_String)
db = client['jobTracker']
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
        "description": data['description'],
        "posting_date": data['posting_date'],
        "last_date": data['last_date'],
        "contact": data['contact'],
        "source": data['source'],
        "application_date": data['application_date'],
        "resume_path": filepath
    }
    collection.insert_one(job_data)
    return redirect(url_for("view_jobs"))

@app.route("/view")
def view_jobs():
    jobs = list(collection.find())
    return render_template("view.html", jobs=jobs)

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
            "description": request.form['description'],
            "posting_date": request.form['posting_date'],
            "last_date": request.form['last_date'],
            "contact": request.form['contact'],
            "source": request.form['source'],
            "application_date": request.form['application_date'],
            "resume_path": job['resume_path']  # keep existing resume
        }
        collection.update_one({"_id": ObjectId(job_id)}, {"$set": updated_data})
        return redirect(url_for('view_jobs'))
    return render_template("index.html", job=job, editing=True, job_id=job_id)

@app.route("/delete/<job_id>")
def delete_job(job_id):
    collection.delete_one({"_id": ObjectId(job_id)})
    return redirect(url_for("view_jobs"))


if __name__ == "__main__":
    app.run(debug=True)
