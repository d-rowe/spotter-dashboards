jobs = {}

def add(record):
    job_id = record['job_id']
    jobs[job_id] = record


def update_status(job_id, status):
    jobs[job_id]['status'] = status

def increase_rows(job_id):
    jobs[job_id]['rows_ingested'] += 1


def get(job_id):
    return jobs[job_id]

