#!/usr/bin/env python3
"""
This module provides a Cache class that interfaces with a Redis database
to store and retrieve data using unique keys.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for storing and retrieving data in Redis.
    """

    def __init__(self):
        """
        Initialize the Cache class, connecting to Redis
        and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis and return the key as a string.

        :param data: The data to store (str, bytes, int, or float).
        :return: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
