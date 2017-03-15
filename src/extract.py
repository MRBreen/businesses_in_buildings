from bs4 import BeautifulSoup

"""from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid


# Define the MongoDB database and table
db_cilent = MongoClient()
db = db_cilent['WBLS']
table = db['meta']"""


class extract(object):
    """An object which holds extracted values using BeautifulSoup
    """
    def __init__(self):
        self._BeautifulSoup =
        self.address_one = None

    def address_one(soup)
        address_one = soup.find(id='caption2_c-u')
        if address_one is not None:
            address_one = address_one.contents[0].encode('utf-8').strip()
        else:
            address_one=""
        return(address_one)


##if __name__ == '__main__':
##    pass
