from datetime import datetime
from influxdb_client import InfluxDBClient, WriteOptions, Point

client = InfluxDBClient(
    url='http://database:8086',
    token='my-token',
    org='default',
)
write_options = WriteOptions(
    batch_size=500,
    flush_interval=100
)

write_api = client.write_api(write_options=write_options)


def write(measurement, record):
    timestamp = record['timestamp']
    dt = datetime.fromtimestamp(timestamp).isoformat()
    del record['timestamp']
    for k, v in record.items():
        p = Point(measurement).time(dt).field(k, v)
        write_api.write(bucket='default', org='default', record=p)


def flush():
    write_api.close()
