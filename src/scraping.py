from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid


# Define the MongoDB database and table
db_cilent = MongoClient()
db = db_cilent['WBLS']
table = db['meta']

if __name__ == '__main__':
    pass
