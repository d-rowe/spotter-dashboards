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
measures = ['displacement', 'location', 'bulkparameters']

def start(job):
    thread = threading.Thread(target=main_worker, args=[job])
    thread.start()


def main_worker(job):
    artifacts_dir = job['artifacts_dir']
    job_id = job['job_id']
    sd_parser(path=artifacts_dir, outpath=artifacts_dir)


    total_rows = 0
    for m in measures:
        total_rows += count_rows(os.path.join(artifacts_dir, f'{m}.csv'))
    job_entity.set_total_rows(job_id, total_rows)
    job_entity.update_status(job_id, 'INGESTING')

    child_threads = []

    for m in measures:
        child_threads.append(threading.Thread(target=ingestion_worker, args=[{
            'CSVParser': CSVParser,
            'artifacts_dir': artifacts_dir,
            'job_id': job_id,
            'job_entity': job_entity,
            'filename': f'{m}.csv',
            'measure': m,
            'db_client': db_client,
            'os': os,
        }]))

    for t in child_threads:
        t.start()

    for t in child_threads:
        t.join()

    job_entity.update_status(job_id, 'CLEANING_UP')
    db_client.flush()
    shutil.rmtree(artifacts_dir, ignore_errors=True)

    job_entity.update_status(job_id, 'SUCCESS')

def ingestion_worker(args):
    csv_parser = args['CSVParser'](args['os'].path.join(args['artifacts_dir'], args['filename']))
    for record in csv_parser.records():
        args['db_client'].write(args['measure'], record)
        args['job_entity'].increase_rows(args['job_id'])

def count_rows(filename):
    result = subprocess.run(['wc', '-l', filename], stdout=subprocess.PIPE)
    row_count = int(result.stdout.decode('utf-8').split()[0])
    return row_count
