from pymongo import MongoClient

cli = MongoClient()
db = cli.get_database('cherrypie')


def main():
    db.code.create_index([("created_at", 1)], expireAfterSeconds=300)

def get_index():
    print(list(db.code.list_indexes()))

if __name__ == "__main__":
    get_index()
    # main()
