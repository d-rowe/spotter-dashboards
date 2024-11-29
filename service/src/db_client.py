import pymongo

client = pymongo.MongoClient(
    "mongodb://database:27017/",
    username="root",
    password="password",
)
