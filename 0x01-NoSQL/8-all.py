#!/usr/bin/env python3
"""Module for listing all documents in a MongoDB collection"""

from pymongo.errors import ConnectionFailure

def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.
    
    Args:
    mongo_collection: pymongo collection object

    Returns:
    list: List of all documents in the collection.
          Returns an empty list if no documents are found or if there's a connection error.
    """
    try:
        return list(mongo_collection.find())
    except ConnectionFailure:
        print("Failed to connect to the MongoDB server. Please ensure it's running.")
        return []
