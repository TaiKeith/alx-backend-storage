#!/usr/bin/env python3
"""
This module contains a function that returns all studnts sorted by
average score
"""


def top_students(mongo_collection):
    """
    Returns all students from the collection sorted by average score.
    Each student returned will include their name and average score,
    with the average score included under the key 'averageScore'.

    Args:
        mongo_collection (pymongo.collection.Collection): The pymongo collection object
            representing the students' data.
    Returns:
        list: A list of dictionaries, each containing:
            - '_id': The student's unique identifier.
            - 'name': The student's name.
            - 'averageScore': The average score calculated from the student's topics.
    """
    return list(mongo_collection.aggregate([
        {
            "$project": {
                '_id': 1,
                "name": "$name",
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]))
