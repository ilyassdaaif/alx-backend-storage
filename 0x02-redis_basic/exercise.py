#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.
'''
import redis
import uuid
import functools
from typing import Callable, Optional, Union

# Redis connection setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def call_history(method: Callable) -> Callable:
    """Decorator to store the history of calls for a function."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Create keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store input parameters
        redis_client.rpush(input_key, str(args))

        # Call the original function and store the output
        result = method(self, *args, **kwargs)
        redis_client.rpush(output_key, result)

        return result
    return wrapper

class Cache:
    """Cache class to store data with Redis."""
    
    def __init__(self):
        """Initialize Cache and connect to Redis."""
        self._redis = redis_client
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return a unique key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis and apply a function if provided."""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

def replay(method: Callable):
    """Replay the history of calls for a function."""
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for input_val, output_val in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{eval(input_val.decode('utf-8'))}) -> {output_val.decode('utf-8')}")
