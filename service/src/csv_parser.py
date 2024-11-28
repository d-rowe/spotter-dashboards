from datetime import datetime

class CSVParser:
    def __init__(self, file: str):
        self.headers = []
        self.file = file

    def records(self):
        with open(self.file, 'r') as file:
            line_num = 0
            headers = []
            for line in file:
                if line_num == 0:
                    tmp = line.replace('# ', '').split(',')
                    for column_name in tmp:
                        headers += [column_name.strip()]
                    self.headers = headers
                else:
                    record = {}
                    items = line.split(',')
                    for index, item in enumerate(items):
                        record[headers[index]] = coerce(item.strip())
                    yield format_timestamp(record)
                line_num += 1

def coerce(val):
    val = val.strip()
    try:
        i = int(val)
        return i
    except:
        pass
    try:
        f = float(val)
        return f
    except:
        pass

    return val

# consolidate date time fields into single timestamp
def format_timestamp(record):
    dt = datetime(
        record['year'],
        record['month'],
        record['day'],
        record['hour'],
        record['min'],
        record['sec'],
        # millisecond to microsecond conversion
        record['msec'] * 1000,
    )
    record['timestamp'] = int(dt.timestamp() * 1000)
    # cleanup prior date time fields
    del record['year']
    del record['month']
    del record['day']
    del record['hour']
    del record['min']
    del record['sec']
    del record['msec']
    return record