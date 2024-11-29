from db_client import client


location = client.location.my_collection


def add(record):
    location.insert_one(record)


def log():
    for item in location.find():
        print(item)