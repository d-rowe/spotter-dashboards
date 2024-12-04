import os
import uuid
import data_pipeline
import job_entity
from werkzeug.utils import secure_filename

def upload(file_list):
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

    for current_file in file_list:
        filename = secure_filename(current_file.filename)
        current_file.save(os.path.join(artifacts_dir, filename))

    data_pipeline.start(job)

    return job_id