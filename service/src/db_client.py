from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

client = influxdb_client.InfluxDBClient(
    url='http://database:8086',
    token='my-token',
    org='default',
)

write_api = client.write_api(write_options=SYNCHRONOUS)


def write(measurement, record):
    timestamp = record['timestamp']
    dt = datetime.fromtimestamp(timestamp).isoformat()
    del record['timestamp']
    for k, v in record.items():
        p = influxdb_client.Point(measurement).time(dt).field(k, v)
        write_api.write(bucket='default', org='default', record=p)


def flush():
    write_api.close()