import threading
from vendor.sd_file_parser import main
from csv_parser import CSVParser

def run():
    thread = threading.Thread(target=ingestion_worker)
    thread.start()


def ingestion_worker():
    main(path='../input', outpath='../output')
    csv_parser = CSVParser('../output/displacement.csv')
    for record in csv_parser.records():
        # TODO: ingest into mongodb
        print(record)
