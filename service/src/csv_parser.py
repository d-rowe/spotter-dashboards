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
                        record[headers[index]] = self.format_value(item.strip())
                    yield record
                line_num += 1

    def format_value(self, val):
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
