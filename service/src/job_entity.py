from db_client import client

job = client.displacement.my_collection


def add(record):
    job.insert_one(record)


def update_status(job_id, status):
    query = {"job_id": job_id}
    job.update_one(query, {"$set": {"status": status}})


def get(job_id):
    return job.find_one({'job_id': job_id})
