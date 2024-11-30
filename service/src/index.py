from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename, redirect
import os
import uuid
import ingestion
import job_entity

app = Flask(__name__)
CORS(app)

@app.route('/job-status/<job_id>')
def get_status(job_id):
    job = job_entity.get(job_id)
    return job['status']


@app.route('/upload', methods=['POST'])
def upload():
    job_id = str(uuid.uuid4())
    artifacts_dir = os.path.join('job_artifacts', job_id)
    job = {
        'job_id': job_id,
        'artifacts_dir': artifacts_dir,
        'status': 'TRANSFERRING'
    }
    job_entity.add(job)
    os.makedirs(artifacts_dir)

    for current_file in request.files.getlist('files[]'):
        print(current_file)
        filename = secure_filename(current_file.filename)
        current_file.save(os.path.join(artifacts_dir, filename))

    ingestion.run(job)

    return {
        'jobId': job_id
    }
