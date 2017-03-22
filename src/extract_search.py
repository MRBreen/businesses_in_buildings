from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import string
import os
import boto3
import botocore

class bing_data(object):
    """holds extracted values
    """
    def __init__(self):
        self.soup = None
        self.namesearch = None
        self.num_results = None
        self.links = None
        self.text = None

    def create_soup(self, key):
        """ creates the object and connects to folder
        """
        self.filename = key.key
        #with open (filename) as pagefile:
        page_source = key.get(self.filename)['Body']
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def get_namesearch(self):
        """ gets the search term which begins with the name
        """
        self.namesearch = self.soup.find(id = "sb_form_q")['value'].encode('utf-8')


    def get_num_results(self):
        """ gets the number of results
        """
        r = self.soup.find('span',{'class':'sb_count'}).contents
        if len(r)>0:
            self.num_results = r[0].split(" results")[0].replace(',','').encode('utf-8')
            #self.num_results = r.split(" results")[0].replace(',','').encode('utf-8')

    def get_links(self):
        """ gets links
        """
        linka = self.soup.find_all('div', 'b_attribution')
        linkb = [i.get_text().encode('utf-8') for i in linka]
        links = []
        for i, link in enumerate(linkb):  #may need to shorten to end at -1
            if link != 'Ad':
                if v[0:8] == 'https://':
                    v = v[8:]
                if v[0:7] == 'http://':
                    v = v[7:]
                links.append([i,v])
        self.links = links

    def get_text(self):
        """ gets text
        """
        data = self.soup.findAll('p')
        texta = [b.get_text().encode('utf-8') for b in data]
        text=[]
        for i, textc in enumerate(textb):
            if textc != 'Ad':
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
            "Bus Search" : self.namesearch,
            "Results" : self.num_results,
            "Links" : self.links,
            "Text" : self.text
        })


if __name__ == '__main__':
    """code processes all html files and
    saves fields to records in mongoDB.
    s3 biz-in-buildings-search -> db.wa.bing
    """
    db_cilent = MongoClient()
    db = db_cilent['wa']
    collection = db.bing

    s3 = boto3.resource('s3')
    b = s3.Bucket('biz-in-buildings-search')
    #bo = b.objects

    filenames = [key.key for key in b.objects.all()]
    #filenames = [b.key.encode('utf-8') for b in bo.iterator()]

    print "DB and collection is:" , collection.full_name
    print "Initial record count:" , collection.count()
    #for file in os.listdir('../data/'):  #for local

    for key in b.objects.all():
        extracted = bing_data()
        extracted.build(key)
        if db.biz.find( { "Filename" : key.key} ).count() < 1:
            extracted.db_add(collection)
    print "Final record count:" , collection.count()
