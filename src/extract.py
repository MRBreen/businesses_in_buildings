from bs4 import BeautifulSoup
#import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import string
import os
import boto3



class extract(object):
    """object holds extracted values using BeautifulSoup
    """
    def __init__(self):
        self.soup = None
        self.business_name = None
        self.address_one = None
        self.address_mailing = None
        self.ubi = None
        self.city = 'Seattle'
        self.zip_code = None
        self.entity = None
        self.filename = None

    def create_soup(self, filename):
        """creates the object and connects to folder
        """
        self.filename = filename
        #with open (filename) as pagefile:
        page_source = b.get(filename)['Body']
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def get_buisiness_name(self):
        """gets business_name .... all other get_ functions work similarly
        """
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
        else:
            self.address_one=""

    def get_address_mailing(self):
        self.address_mailing = self.soup.find(id='caption2_c-01')
        if self.address_mailing is not None:
            if len(self.address_mailing.contents) != 0:
                self.address_mailing = self.address_mailing.contents[0].encode('utf-8').strip()
            else:
                self.address_mailing=""
        else:
            self.address_mailing=""

    def get_zip_code(self):
        self.zip_code = self.soup.find(id='caption2_c-v')
        if self.zip_code is not None:
            if len(self.zip_code.contents) != 0:
                zipfield = self.zip_code.contents[0].encode('utf-8').strip()
                self.zip_code = zipfield[-5:]
            else:
                self.zip_code=""
        else:
            self.zip_code=""

    def get_ubi(self):
        self.ubi = self.soup.find(id='caption2_c-i')
        if self.ubi is not None:
            self.ubi = self.ubi.contents[0].encode('utf-8').strip()
        else:
            self.ubi=""

    def get_entity(self):
        """gets entity type
        """
        self.entity = self.soup.find(id='caption2_c-g')
        if self.entity is not None:
            self.entity = self.entity.contents[0].encode('utf-8').strip()
        else:
            self.entity=""

    def build(self, filename):
        """Calls subfunction which create values for the parameters
        arg: filename is html file to be extracted
        """
        self.create_soup(filename)
        self.get_buisiness_name()
        self.get_address_one()
        self.get_address_mailing()
        self.get_ubi()
        self.get_zip_code()
        self.get_entity()

    def db_add(self, collection):
        collection.insert_one({
                "Bus Name" : self.business_name,
                "Address" : self.address_one,
                "Addr_mail" : self.address_mailing,
                "UBI" : self.ubi,
                "City" : self.city,
                "Zip" : self.zip_code,
                "Entity" : self.entity,
                "Filename" : self.filename
            })

if __name__ == '__main__':
    """code processes all html files in data folder and
    saves fields to records in mongoDB.
    collection name is defined at the top of the code.
    """
    #Define the MongoDB database and collection
    db_cilent = MongoClient()
    db = db_cilent['wa']
    collection = db.biz

    s3 = boto3.resource('s3')
    b = s3.Bucket('biz-in-buildings')
    bo = b.objects
    filenames = [b.key.encode('utf-8') for b in bo.iterator()]

    print "DB and collection is:" , collection.full_name
    print "Initial record count:" , collection.count()
    #for file in os.listdir('../data/'):  #for local
    for filename in filenames:
            extracted = extract()
            extracted.build(filename)
            extracted.db_add(collection)
    print "Final record count:" , collection.count()
