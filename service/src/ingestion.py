import os
import shutil
import threading
import logging
import db_client
from vendor.sd_file_parser import main as sd_parser
from csv_parser import CSVParser
import job_entity


def run(job):
    thread = threading.Thread(target=worker, args=[job])
    thread.start()


def worker(job):
    artifacts_dir = job['artifacts_dir']
    job_id = job['job_id']
    sd_parser(path=artifacts_dir, outpath=artifacts_dir)

    job_entity.update_status(job_id, 'INGESTING_DISPLACEMENT')
    csv_parser = CSVParser(os.path.join(artifacts_dir, 'displacement.csv'))

    for record in csv_parser.records():
        db_client.write('displacement', record)
        job_entity.increase_rows(job_id)

    job_entity.update_status(job_id, 'INGESTING_LOCATION')
    csv_parser = CSVParser(os.path.join(artifacts_dir, 'location.csv'))

    for record in csv_parser.records():
        db_client.write('location', record)
        job_entity.increase_rows(job_id)

    job_entity.update_status(job_id, 'CLEANING_UP')
    db_client.flush()
    shutil.rmtree(artifacts_dir, ignore_errors=True)

    job_entity.update_status(job_id, 'SUCCESS')
