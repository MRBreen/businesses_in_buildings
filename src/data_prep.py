import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd

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

def clean_df(df):
    """ cleans up df for all models
    """
    df = df.dropna()
    df.reset_index()
    return df

def get_array_from_list(df):
    """ returns an array of links from a dataframe
        works for links and text as well
        parameters:
        df - dataframe
        col should be either 'Text' or 'Link'
    """
    slinks = pd.Series()
    list_links = []
    for index, row in df.iterrows():
        list_links = []
        links = ""
        for i in range(10):
            link = row[0][0][1]
            links += link + " "
        slink = pd.Series(links)
        slinks = slinks.append(slink)
    return slinks
