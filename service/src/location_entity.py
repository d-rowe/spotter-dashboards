from db_client import client


location = client.location.my_collection
location.create_index('timestamp')


def add(record):
    location.insert_one(record)


def add_batch(records):
    location.insert_many(records)
