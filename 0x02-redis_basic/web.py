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
cache = redis.Redis()


# Decorator for caching
def cache_page(func: Callable) -> Callable:
    """
    Caches the output of the fetched data
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        cache.incr(f"count:{url}")
        content = cache.get(f"content:{url}")
        if content:
            return content.decode('utf-8')

        content = func(url)
        cache.set(f"count:{url}", 0)
        cache.setex(f"content:{url}", 10, content)
        return content
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response
    and tracking the request
    """
    response = requests.get(url)
    return response.text

# Test the function with the decorator
if __name__ == "__main__":
    """Test the function"""
    url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.co.uk'
    print(get_page(url))
    time.sleep(5)  # Wait and test cache hit
    print(get_page(url))  # Cache hit expected
