import pymongo

from .utils_config import mongo_client_info


class Mongo(object):

    def __init__(self):
        # Client
        self.client = pymongo.MongoClient(mongo_client_info)
        # Database
        self.db_cuhksz_ce         = self.client["cuhksz-ce"]
        # Collection
        self.coll_cache           = self.db_cuhksz_ce["coll_cache"]
        self.coll_auth_info       = self.db_cuhksz_ce["coll_auth_info"]
        self.coll_user_info       = self.db_cuhksz_ce["coll_user_info"]
        self.coll_course_info     = self.db_cuhksz_ce["coll_course_info"]
        self.coll_course_record   = self.db_cuhksz_ce["coll_course_record"]
        self.coll_activity_info   = self.db_cuhksz_ce["coll_activity_info"]
        self.coll_activity_record = self.db_cuhksz_ce["coll_activity_record"]


mongo = Mongo()


if __name__ == "__main__":
    """
python utils/mongo.py
    """

    print(mongo.client.list_database_names())
    print(mongo.db_cuhksz.list_collection_names())
