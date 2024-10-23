#!/usr/bin/env python3
"""
This module contains functions and methods for Redis NoSQL data storage
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called

    Args:
        method (Callable): The method to be decorated
    Returns:
        Callable: The wrapped method with call counting
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Wrapper function that increments the call count in Redis
        and executes the original method.
        """
        # Increment the call count in Redis
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)

        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method in Redis

    Args:
        method (Callable): The method to be decorated
    Returns:
        Callable: The wrapped method that stores input/output history
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that records the input/output history in Redis
        """
        # Generate Redis keys for inputs and outputs
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Convert the input arguments to a str representation & store in Redis
        self._redis.rpush(input_key, str(args))

        # Call the original method and get the output
        output = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(output_key, str(output))

        # Return the original method's output
        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls for a given method.

    Args:
        method (Callable): The method for which to display the call history.
    """
    # Access the Redis instance from the Cache object
    redis_instance = method.__self__._redis

    # Get the qualified name of the method
    method_name = method.__qualname__

    # Get the number of times the method was called
    call_count = redis_instance.get(method_name)
    if call_count is None:
        print(f"{method_name} was never called")
        return

    call_count = int(call_count.decode("utf-8"))
    print(f"{method_name} was called {call_count} times:")

    # Fetch the inputs and outputs from Redis
    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    # Print the inputs and outputs in the desired format
    for inp, outp in zip(inputs, outputs):
        print(f"{method_name}(*{inp.decode('utf-8')}) -> {outp.decode('utf-8')}")


class Cache:
    """
    Represents an object that handles storing data of multiple types in Redis
    """
    def __init__(self):
        """Initialize the Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that stores the input data in Redis with a a randomly generated
        key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis
        Returns:
            str: The key under which the data is stored
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis and apply a callable to convert it to the
        desired format.

        Args:
            key (str): The key under which the data is stored in Redis
            fn (Optional[Callable]): A callable to convert the data to the
                                     desired type
        Returns:
            Union[str, bytes, int, None]: The retrieved and possibly converted
                                          data
        """
        value = self._redis.get(key)

        return fn(value) if fn is not None else value

    def get_str(self, key: str) -> str:
        """
        Returns the retrieved data as a str, or None if the key does not exist
        """
        # Use the get method with a conversion function to decode bytes to str
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Returns the retrieved data as an int, or None if the key does not exist
        """
        # Use the get method with a conversion function to convert bytes to int
        return self.get(key, lambda d: int(d))
