#!/usr/bin/env python3
"""Return the list of school having a specific topic."""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic.

    Args:
        mongo_collection: The pymongo collection object.
        topic (str): The topic to search for.

    Returns:
        List of dictionaries representing the schools with the given topic.
    """
    return list(mongo_collection.find({"topics": topic}))
