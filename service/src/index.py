from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename, redirect
import os
import uuid
import ingestion
import job_entity
import displacement_entity

app = Flask(__name__)


@app.route('/')
def root():
    return '<input type="file" id="avatar" name="avatar" accept="image/png, image/jpeg" />'

@app.route('/job-status/<job_id>')
def get_status(job_id):
    job = job_entity.get(job_id)
    return job['status']


@app.route('/displacement')
def get_displacement():
    return jsonify(displacement_entity.get())


@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return redirect(request.url)

    job_id = str(uuid.uuid4());
    artifacts_dir = os.path.join('.', 'job_artifacts', job_id)
    job = {
        'job_id': job_id,
        'artifacts_dir': artifacts_dir,
        'status': 'TRANSFERRING'
    }
    job_entity.add(job)
    os.makedirs(artifacts_dir)
    for current_file in request.files.getlist('file'):
        if current_file.filename != '':
            filename = secure_filename(current_file.filename)
            current_file.save(os.path.join(artifacts_dir, filename))

    ingestion.run(job);
    return job_id
