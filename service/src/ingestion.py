import os
import shutil
import threading
from vendor.sd_file_parser import main as sd_parser
from csv_parser import CSVParser
import displacement_entity
import location_entity
import job_entity


def run(job):
    thread = threading.Thread(target=worker, args=[job])
    thread.start()


def worker(job):
    artifacts_dir = job['artifacts_dir']
    job_id = job['job_id']
    job_entity.update_status(job_id, 'PROCESSING')
    sd_parser(path=artifacts_dir, outpath=artifacts_dir)

    job_entity.update_status(job_id, 'INGESTING_DISPLACEMENT')
    csv_parser = CSVParser(os.path.join(artifacts_dir, 'displacement.csv'))
    for record in csv_parser.records():
        record['job_id'] = job_id
        displacement_entity.add(record)

    job_entity.update_status(job_id, 'INGESTING_LOCATION')
    csv_parser = CSVParser(os.path.join(artifacts_dir, 'location.csv'))
    for record in csv_parser.records():
        record['job_id'] = job_id
        location_entity.add(record)

    job_entity.update_status(job_id, 'CLEANING_UP')
    shutil.rmtree(artifacts_dir, ignore_errors=True)

    job_entity.update_status(job_id, 'SUCCESS')
