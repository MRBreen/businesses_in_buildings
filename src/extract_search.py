from bs4 import BeautifulSoup
import sys
import requests
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import os

class bing_data(object):
    """Holds extracted values
    """
    def __init__(self):
        self.soup = None
        self.name = None
        self.num_results = None
        self.links = None
        self.text = None

    def create_soup(self, filename):
        folder = ('')
        with open (folder+filename) as pagefile:
            page_source = pagefile.read()
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def get_num_results(self):
        """ Gets the number of results
        """
        r = self.soup.find('span',{'class':'sb_count'}).text
        if len(r)>0:
            self.num_results = r.split(" results")[0].replace(',','').encode('utf-8')

    def get_links(self):
        """get links
        """
        linka = self.soup.find_all('div', 'b_attribution')
        linkb = [i.text.split()[0] for i in linka]
        links = []
        for i, link in enumerate(linkb[:-1]):
            if link.encode('utf-8') != 'Ad':
                v = link.encode('utf-8')
                if v[0:8] == 'https://':
                    v = v[8:]
                if v[0:7] == 'http://':
                    v = v[7:]
                links.append([i,v])
        self.links = links

    def get_text(self):
        """get text
        """
        data = self.soup.findAll('p')
        texta = [b.get_text() for b in data]
        textb = [t.encode('utf-8') for t in texta]
        text=[]
        for i, textc in enumerate(textb[:-1]):
            if textc.encode('utf-8') != 'Ad':
                v = textc.encode('utf-8')
                text.append([i,v])
        self.text = text

    def build(self, filename):
        """Calls subfunction which create values for the parameters
        arg: filename is html file to be extracted
        """
        self.create_soup(filename)
        self.get_num_results()
        self.get_links()
        self.get_text()

    def db_add(self, collection):
        collection.insert_one({
            "Bus Name" : self.name,
            "Results" : self.num_results,
            "Links" : self.links,
            "Text" : self.text
        })


if __name__ == '__main__':
    """code processes all html files in data folder and
    saves fields to records in mongoDB.
    collection name is defined at the top of the code.
    """
    db_cilent = MongoClient('mongodb://localhost:27017/') # may soft code later
    db = db_cilent['wa']
    collection = db.bing
    print "DB and collection is:" , collection.full_name
    print "Initial record count:" , collection.count()
    #for file in ['databing/2017319_122723_ABC.html']:
    for file in os.listdir('../datb/'):
        if '.htm' in file:
            print file
            bing_data = bing_data()
            bing_data.build(file)
            bing_data.db_add(collection)
    print "Final record count:" , collection.count()
