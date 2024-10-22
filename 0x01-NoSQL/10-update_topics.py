#!/usr/bin/env python3
"""
This module contains a function that changes all topics of a school document
in a collection based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name
    Args:
        mongo_collection: The pymongo collection object
        name (str): The school name to update
        topics (List[str]): The list of topics approached in the school
    """
    mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
            )
