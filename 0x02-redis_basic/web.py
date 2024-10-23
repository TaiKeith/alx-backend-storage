#!/usr/bin/env python3
"""
This module contains a function that uses the requests module to obtain
the HTML content of a particular URL and returns it.
"""
import requests
import redis
from functools import wraps
from typing import Callable


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

        # Log a cache miss
        print(f"Cache miss for URL: {url}. Fetching from the web...")

        content = func(url)
        cache.setex(f"content:{url}", 60, content)  # Cache expiration set to 60 seconds
        return content
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response
    and tracking the request
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.RequestException as e:
        return f"Error fetching the page: {e}"
