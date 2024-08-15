#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import redis
import requests
from functools import wraps
from typing import Callable

<<<<<<< HEAD
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
=======
# Redis connection setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_page(func: Callable) -> Callable:
    """Decorator to cache and track URL accesses."""
    @functools.wraps(func)
    def wrapper(url: str, *args, **kwargs) -> str:
        redis_key = f"cache:{url}"
        count_key = f"count:{url}"

        # Check if the URL is in the cache
        cached_page = redis_client.get(redis_key)
        
        if cached_page:
            print("Cache hit")
            redis_client.incr(count_key)
            return cached_page.decode('utf-8')

        # If not cached, fetch the page content
        print("Cache miss")
        html_content = func(url, *args, **kwargs)

        # Store the page content in the cache with an expiration time of 10 seconds
        redis_client.setex(redis_key, 10, html_content)

        # Track the number of accesses for the URL
        redis_client.incr(count_key)

        return html_content

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL."""
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Testing the get_page function
    url = (
        "http://slowwly.robertomurray.co.uk/delay/5000/url/"
        "http://www.google.com"
    )
    
    # Fetch the page content
    content = get_page(url)
    print(content[:100])  # Print the first 100 characters for brevity

    # Fetch again to test cache
    content = get_page(url)
    print(content[:100])  # Should print the same content as before
>>>>>>> a2ee7c183ca5a99c3c09ec51913cbbeb11de162f
