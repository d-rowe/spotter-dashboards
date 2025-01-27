from flask import Flask, request
from flask_cors import CORS
from werkzeug.utils import secure_filename, redirect
import os
import uuid
import data_pipeline
import job_entity
from services import upload_service, dashboard_service
import os

app = Flask(__name__)
CORS(app)

@app.route('/job/<job_id>')
def get_status(job_id):
    return job_entity.get(job_id)

@app.route('/embed-url')
def get_embed_url():
    return dashboard_service.get_embed_url()


@app.route('/upload', methods=['POST'])
def upload():
    job_id = str(uuid.uuid4())
    artifacts_dir = os.path.join('job_artifacts', job_id)
    job = {
        'job_id': job_id,
        'artifacts_dir': artifacts_dir,
        'status': 'TRANSFERRING',
        'rows_ingested': 0,
    }
    job_entity.add(job)
    os.makedirs(artifacts_dir)

    for current_file in request.files.getlist('files[]'):
        filename = secure_filename(current_file.filename)
        current_file.save(os.path.join(artifacts_dir, filename))

    data_pipeline.start(job)

    return {
        'jobId': job_id
    }
