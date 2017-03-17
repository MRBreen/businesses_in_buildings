from bs4 import BeautifulSoup
import sys
import requests
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid


db_cilent = MongoClient('mongodb://localhost:27017/')
db = db_cilent['WBS']
collections = db.biz

def number_results(soup):
resultstats = soup.find_all(id="resultStats")
resultstat = resultstats[0]
results_returned = resultstat.contents[0].split()[0]

soup = BeautifulSoup(open(file), 'lxml')


index=[]
for i, link in enumerate(soup.find_all('a')):
    if (link.get('href')) == '#':
        index.append(i+2)

links = []
for i in index[:-1]:
    links.append(soup.find_all('a')[i])


    db.biz.insert_one({
            "Bus_Name" : soup.title.text.split(' seattle - Google')[0],
            "Name_city_returns" : results_returned,
            "Name_city_links" : [x.get('href') for x in links],
        })
