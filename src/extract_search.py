from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import string
import os
import boto3
import botocore
import datetime

class BingData(object):
    """Holds extracted values"""
    def __init__(self):
        self.soup = None
        self.namesearch = None
        self.num_results = None
        self.links = None
        self.text = None
        self.filename = None

    def create_soup(self, key):
        """Creates the object and connects to folder"""
        self.filename = key.key
        page_source = key.get(self.filename)['Body']
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def get_namesearch(self):
        """Returns thes earch term"""
        try:
            self.namesearch = self.soup.find(id = "sb_form_q")['value'].encode('utf-8')
        except:
            self.namesearch = ''

    def get_num_results(self):
        """Returns the number of results"""
        ra = self.soup.find('span',{'class':'sb_count'})
        if ra is None:
            return
        r = ra.contents
        if len(r)>0:
            self.num_results = r[0].split(" results")[0].replace(',','').encode('utf-8')

    def get_links(self):
        """Returns links and text - both field in one function to filter out ads"""
        linka = self.soup.find_all('div', 'b_attribution')
        if linka is None:
            return
        linkb = [i.get_text().encode('utf-8') for i in linka]
        links = []
        texta = self.soup.find_all('p')
        text = []
        for i, link in enumerate(linkb):  #may need to shorten to end at -1
            if i < 10:
                if link[0:4] != 'Ad ':
                    if link[0:8] == 'https://':
                        link = link[8:]
                    if link[0:7] == 'http://':
                        link = link[7:]
                    links.append([i,link])
                    if len(texta) > i :
                        text.append([i, texta[i].get_text().encode('utf-8') ])
        self.links = links
        self.text = text

    def build(self, filename):
        """Calls subfunction which create values for the parameters

        Keyword arguments:
        filename -- html file to be extracted
        """
        self.create_soup(filename)
        self.get_namesearch()
        self.get_num_results()
        self.get_links()

    def db_add(self, collection):
        """Creates record of namesearch, num_results, links, text
        in the named collection.

        Keyword arguments:
        collection -- name of collection for the record
        """
        collection.insert_one({
            "Bus Search" : self.namesearch,
            "Results" : self.num_results,
            "Links" : self.links,
            "Text" : self.text
        })



if __name__ == '__main__':
    """Processes an html files and
    saves fields to a recordsin mongoDB.
    s3 biz-in-buildings-search -> db.wa.bing
    """
    db_cilent = MongoClient()
    db = db_cilent['wa']
    collection = db.bing

    s3 = boto3.resource('s3')
    b = s3.Bucket('biz-in-buildings-search')

    filenames = [key.key for key in b.objects.all()]

    print "DB and collection is:" , collection.full_name
    print "Initial record count:" , collection.count()
    
    i = 0
    for key in b.objects.all():
        i+=1
        extracted = BingData()
        extracted.build(key)
        if db.biz.find( { "Filename" : key.key} ).count() < 1:
            extracted.db_add(collection)
        if i%1000 == 0:
            print "htmls files read:" , i
    print "Final record count:" , collection.count()
