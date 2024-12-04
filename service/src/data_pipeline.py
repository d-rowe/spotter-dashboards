import os
import shutil
import subprocess
import threading
import logging
import db_client
from vendor.sd_file_parser import main as sd_parser
from csv_parser import CSVParser
import job_entity

# Measures we want to ultimately ingest
measures = [
    {'name': 'displacement', 'file': 'displacement.csv'},
    {'name': 'location', 'file': 'location.csv'},
    {'name': 'wave', 'file': 'bulkparameters.csv'}
]

def start(job):
    thread = threading.Thread(target=main_worker, args=[job])
    thread.start()


def main_worker(job):
    artifacts_dir = job['artifacts_dir']
    job_id = job['job_id']
    sd_parser(path=artifacts_dir, outpath=artifacts_dir)


    total_rows = 0
    for m in measures:
        total_rows += count_rows(os.path.join(artifacts_dir, m['file']))
    job_entity.set_total_rows(job_id, total_rows)
    job_entity.update_status(job_id, 'INGESTING')

    child_threads = []

    for m in measures:
        ingestion_worker({
            'artifacts_dir': artifacts_dir,
            'job_id': job_id,
            'filename': m['file'],
            'measure': m['name'],
        })


    db_client.flush()
    job_entity.update_status(job_id, 'CLEANING_UP')
    shutil.rmtree(artifacts_dir, ignore_errors=True)

    job_entity.update_status(job_id, 'SUCCESS')

def ingestion_worker(args):
    csv_parser = CSVParser(os.path.join(args['artifacts_dir'], args['filename']))
    for record in csv_parser.records():
        db_client.write(args['measure'], record)
        job_entity.increase_rows(args['job_id'])

def count_rows(filename):
    result = subprocess.run(['wc', '-l', filename], stdout=subprocess.PIPE)
    row_count = int(result.stdout.decode('utf-8').split()[0])
    return row_count
