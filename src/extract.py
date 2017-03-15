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
        self.soup = None
        self.business_name = None
        self.address_one = None
        self.address_one = None
        self.address_mailing = None
        self.ubi = None

    def create_soup(self, filename):
        folder = ('../data/')
        with open (folder+filename) as pagefile:
            page_source = pagefile.read()
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def get_buisiness_name(self):
        self.business_name = self.soup.find(id='caption2_c-e')
        if self.business_name is not None:
            self.business_name = self.business_name.contents[0].encode('utf-8').strip()
        else:
            self.business_name=""

    def get_address_one(self):
        self.address_one = self.soup.find(id='caption2_c-u')
        if self.address_one is not None:
            if len(self.address_one.contents) != 0:
                self.address_one = self.address_one.contents[0].encode('utf-8').strip()
        else:
            self.address_one=""

    def get_address_mailing(self):
        self.address_mailing = self.soup.find(id='caption2_c-01')
        if self.address_mailing is not None:
            if len(self.address_mailing.contents) != 0:
                self.address_mailing = self.address_mailing.contents[0].encode('utf-8').strip()
        else:
            self.address_mailing=""

    def get_ubi(self):
        self.ubi = self.soup.find(id='caption2_c-i')
        if self.ubi is not None:
            self.ubi = self.ubi.contents[0].encode('utf-8').strip()
        else:
            self.ubi=""

    def build(self, filename):
        self.create_soup(filename)
        self.get_buisiness_name()
        self.get_address_one()
        #self.get_address_mailing()
        self.get_ubi()

    def write_json(self):
        pass


##if __name__ == '__main__':
##    pass
