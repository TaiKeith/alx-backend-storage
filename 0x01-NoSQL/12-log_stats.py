#!/usr/bin/env python3
"""
This module contains a function that provides statistics about
Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginx_logs_stats(nginx_collection):
    """
    Prints stats about Nginx request logs
    Args:
        nginx_collection: The pymongo collection object
    """
    # Total number of logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # Print statistic for each HTTP request method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        req_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {req_count}")

    # Print number of GET requests to /status
    status_checks_count = nginx_collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_checks_count} status check")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    nginx_logs_stats(nginx_collection)
