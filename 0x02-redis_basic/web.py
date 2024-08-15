#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()

def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        redis_client.incr(f"count:{url}")
        return method(url)
    return wrapper

def cache_with_expiration(expiration: int = 10) -> Callable:
    """Decorator to cache the result with an expiration time"""
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url):
            """Wrapper function"""
            cached_result = redis_client.get(f"cached:{url}")
            if cached_result:
                return cached_result.decode('utf-8')
            
            result = method(url)
            redis_client.setex(f"cached:{url}", expiration, result)
            return result
        return wrapper
    return decorator

@count_calls
@cache_with_expiration()
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL
    Track how many times the URL was accessed
    Cache the result with an expiration time of 10 seconds
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    
    # First call
    print(get_page(url))
    print(f"Count: {redis_client.get(f'count:{url}').decode('utf-8')}")
    
    # Second call (should be cached)
    print(get_page(url))
    print(f"Count: {redis_client.get(f'count:{url}').decode('utf-8')}")
