#!/usr/bin/env python3
"""
This module contains a function that uses the requests module to obtain
the HTML content of a particular URL and returns it.
"""
import requests
import redis
from functools import wraps
from typing import Callable
import time


# Redis setup
cache = redis.Redis(host='localhost', port=6379, db=0)


# Decorator for caching
def cache_page(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        try:
            # Check if the result is in the cache
            cached_page = cache.get(f"content:{url}")
            if cached_page:
                print(f"Cache hit for URL: {url}")
                return cached_page.decode('utf-8')

            # Fetch and store if not in cache
            content = func(url)
            cache.setex(f"content:{url}", 10, content)
            cache.incr(f"count:{url}")
            return content

        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            return "An error occurred while fetching the page."

    return wrapper

@cache_page
def get_page(url: str) -> str:
    print(f"Cache miss for URL: {url}. Fetching from the web...")
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.text

# Test the function with the decorator
if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.co.uk'
    print(get_page(url))
    time.sleep(5)  # Wait and test cache hit
    print(get_page(url))  # Cache hit expected
