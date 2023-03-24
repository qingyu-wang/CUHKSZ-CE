"""
https://cloud.mongodb.com
"""

import json

import pymongo
import requests

from .utils_config import mongo_client_info_for_dynamic_ip, mongo_api_key_for_dynamic_ip


class Mongo(object):

    def __init__(self):
        # Client
        self.client = pymongo.MongoClient(mongo_client_info_for_dynamic_ip)
        # Database
        self.db_base = self.client["base"]
        # Collection
        self.coll_cache = self.db_base["cache"]


mongo = Mongo()


def fetch_dynamic_ip():
    """
    只需要建立一次链接
    """
    find_data = mongo.coll_cache.find_one({"name": "cuhkszce.link"}, {"_id": 0})
    url = find_data["data"]["url"]
    return url


def fetch_dynamic_ip_http():
    """
    每次请求都要建立链接
    """
    url = "https://data.mongodb-api.com/app/data-pegrf/endpoint/data/v1/action/findOne"
    payload = json.dumps({
        "dataSource": "Cluster0",
        "database": "base",
        "collection": "cache",
        "filter": {
            "name": "cuhkszce.link"
        },
        "projection": {
            "_id": 0
        }
    })
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": mongo_api_key_for_dynamic_ip, 
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    url = data["document"]["data"]["url"]
    return url


if __name__ == "__main__":
    """
python -m utils.dynamic_ip_fetcher
    """

    url = fetch_dynamic_ip()
    print("fetch_dynamic_ip:      %s" % url)
    url = fetch_dynamic_ip_http()
    print("fetch_dynamic_ip_http: %s" % url)
