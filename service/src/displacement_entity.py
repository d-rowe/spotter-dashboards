from db_client import client
from bson.json_util import dumps


displacement = client.displacement.my_collection


def add(record):
    displacement.insert_one(record)


def get():
    items = []
    for item in displacement.find({}):
        del item['_id']
        items.append(item)
    return items
