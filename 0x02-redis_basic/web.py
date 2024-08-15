#!/usr/bin/env python3
""" web.py """
import redis
import requests
import functools
from typing import Callable

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
