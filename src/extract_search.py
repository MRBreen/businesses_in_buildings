from bs4 import BeautifulSoup
import sys
import requests
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import os

db_cilent = MongoClient('mongodb://localhost:27017/')
db = db_cilent['WBS']
collections = db.biz



class search_page(object):
    """Holds extracted values
    """
    def __init__(self):
        self.soup = None
        self.name = None
        self.addr_results = None
        self.addr_link = None
        self.city_results = None
        self.city_link = None
        self.city_results_pres = None
        self.city_link_pres = None
        self.city_results_hista = None
        self.city_link_hista = None

    def create_soup(self, filename):
        folder = ('../data_from_chrome/')
        with open (folder+filename) as pagefile:
            page_source = pagefile.read()
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def get_num_results(self):
        """ Gets the number of results
        """
        resultstats = self.soup.find_all(id="resultStats")
        if len(resultstats)>0:
            resultstat = resultstats[0]
            self.addr_results = resultstat.contents[0].split()[0]

    def get_links(self):
        index=[]
        for i, link in enumerate(self.soup.find_all('a')):
            if (link.get('href')) == '#':
                index.append(i+2)
        links = []
        for i in index[:-1]:
            links.append(self.soup.find_all('a')[i])
        self.addr_link = links


    def build(self, filename):
        """Calls subfunction which create values for the parameters
        arg: filename is html file to be extracted
        """
        self.create_soup(filename)
        self.get_num_results()
        self.get_links()

    def db_add(self, collection):
        collection.insert_one({
            "Bus_Name" : self.soup.title.text.split(' seattle - Google')[0],
            "Name_city_returns" : self.addr_results,
            "Name_city_links" : self.addr_link,
        })

if __name__ == '__main__':
    """code processes all html files in data folder and
    saves fields to records in mongoDB.
    collection name is defined at the top of the code.
    """
    collection = db.biz
    print "DB and collection is:" , collection.full_name
    print "Initial record count:" , collection.count()
    for file in os.listdir('../data_from_chrome/'):
        if '.htm' in file:
            print file
            page_values = search_page()
            page_values.build(file)
            page_values.db_add(collection)
    print "Final record count:" , collection.count()
