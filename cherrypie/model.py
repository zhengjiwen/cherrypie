from .helper import get_function
from pymongo import MongoClient


class Database(object):
    def __init__(self, db, collections):
        self.db = db
        self.register(collections)

    def register(self, collections):
        self.collections_map = {}
        for i in collections:
            f, f_name = get_function(i)
            self.collections_map[f_name] = f

    def __getattr__(self, item):
        return self.collections_map[item](self.db, self)


def get_db(collections, db_name, host=None,
           port=None,
           document_class=dict,
           tz_aware=None,
           connect=None,
           **kwargs):
    client = MongoClient(host=host,
                         port=port,
                         document_class=document_class,
                         tz_aware=tz_aware,
                         connect=connect,
                         **kwargs)

    return Database(client.get_database(db_name), collections)
