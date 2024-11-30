from db_client import client


displacement = client.displacement.my_collection
displacement.create_index('timestamp')


def add(record):
    displacement.insert_one(record)


def add_batch(records):
    displacement.insert_many(records)
