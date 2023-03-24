import datetime
import socket

import pymongo

from .utils_config import mongo_client_info_for_dynamic_ip


class Mongo(object):

    def __init__(self):
        # Client
        self.client = pymongo.MongoClient(mongo_client_info_for_dynamic_ip)
        # Database
        self.db_base = self.client["base"]
        # Collection
        self.coll_cache = self.db_base["cache"]


mongo = Mongo()


def update_url():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    url = "http://%s:5000" % ip
    update_result = mongo.coll_cache.update_many(
        {"name": "cuhkszce.link"}, 
        {"$set": {
            "data.url": url, 
            "time": datetime.datetime.now()
        }}
    )
    assert update_result.modified_count == 1, "update_result.modified_count=%s" % update_result.modified_count
    return url


if __name__ == "__main__":
    """
python -m utils.dynamic_ip_sender
    """

    url = update_url()
    print("[UPDATE] %s" % url)
