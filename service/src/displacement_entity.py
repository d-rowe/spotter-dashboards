from db_client import client


displacement = client.displacement.my_collection


def add(record):
    displacement.insert_one(record)
