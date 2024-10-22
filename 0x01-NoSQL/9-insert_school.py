#!/usr/bin/env python3
"""
This module contains a function that inserts a new document in a collection
based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new documents in a collection based on kwargs
    Args:
        mongo_collection: The pymongo collection object
        **kwargs: The keyword arguments
    Returns:
        the new _id of the document inserted
    """
    return mongo_collection.insert_one(kwargs).inserted_id
