#!/usr/bin/env python3
""" 8-main """
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
list_all = __import__('8-all').list_all

if __name__ == "__main__":
    try:
        client = MongoClient('mongodb://127.0.0.1:27017')
        client.admin.command('ismaster')  # This will raise an exception if can't connect
        school_collection = client.my_db.school
        schools = list_all(school_collection)
        for school in schools:
            print("[{}] {}".format(school.get('_id'), school.get('name')))
    except ConnectionFailure:
        print("Failed to connect to the MongoDB server. Please ensure it's running.")
