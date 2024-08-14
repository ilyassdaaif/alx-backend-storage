#!/usr/bin/env python3
"""
This module provides a Cache class that interfaces with a Redis database
to store and retrieve data using unique keys.
"""

import redis
import uuid
from typing import Union, Callable, Optional


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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a callable to it.

        :param key: The key under which the data is stored.
        :param fn: A callable function to apply to the data.
        :return: The data from Redis, optionally transformed by fn.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis.

        :param key: The key under which the data is stored.
        :return: The data as a string.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.

        :param key: The key under which the data is stored.
        :return: The data as an integer.
        """
        return self.get(key, lambda d: int(d))
