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

def url_count(method: Callable) -> Callable:
    """Decorator to count how many times a URL is accessed"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function"""
        # Increment the count for this URL
        redis_client.incr(f"count:{url}")
        return method(url)
    return wrapper

def cache_with_expiration(expiration: int = 10) -> Callable:
    """Decorator to cache the result with an expiration time"""
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            """Wrapper function"""
            # Check if the result is already in cache
            cached_result = redis_client.get(f"cached:{url}")
            if cached_result:
                return cached_result.decode('utf-8')

            # If not in cache, call the method
            result = method(url)

            # Cache the result with expiration
            redis_client.setex(f"cached:{url}", expiration, result)

            return result
        return wrapper
    return decorator

@url_count
@cache_with_expiration(10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL
    Track how many times the URL was accessed
    Cache the result with an expiration time of 10 seconds
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.RequestException as e:
        return f"Error fetching {url}: {str(e)}"

if __name__ == "__main__":
    # Example usage with a more reliable URL
    url = "https://www.example.com"
    
    print("First call:")
    print(get_page(url))
    print(f"Page visits: {redis_client.get(f'count:{url}').decode('utf-8')}")
    
    print("\nSecond call (should be cached):")
    print(get_page(url))
    print(f"Page visits: {redis_client.get(f'count:{url}').decode('utf-8')}")
    
    print("\nWait 10 seconds for cache to expire...")
    import time
    time.sleep(11)
    
    print("\nThird call (cache should have expired):")
    print(get_page(url))
    print(f"Page visits: {redis_client.get(f'count:{url}').decode('utf-8')}")
