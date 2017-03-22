import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as

def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ read from Mongo and Store into DataFrame
    """
    client = MongoClient()
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db]

    cursor = db[collection].find(query)
    df =  pd.DataFrame(list(cursor))

    if no_id:
        del df['_id']

    return df

def get_link_array(df):
    """ returns an array of links from a dataframe
    """
    df = dfbing[['Links']]
    newlist = data.tolist()
    links = [newlist[0][0][i][1].encode('utf-8') for i in range(len(newlist[0][0]))]
    return (np.array(links))

    
