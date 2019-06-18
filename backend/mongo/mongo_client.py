from pymongo import MongoClient

client = MongoClient(
    'mongodb://localhost:27017/',
    connect=True,  # Connect straight to DB, do not wait for 1st request
    serverSelectionTimeoutMS=3000  # Client timeout
)

DB = client['documentation']  # use the documentation database