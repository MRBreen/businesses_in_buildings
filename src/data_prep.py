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
    list_array = np.array(df[['Links']]).tolist()
    df_links = pd.DataFrame()
    #for r in range(df.shape[0]):
    list_links = []
    links = ""

    for i in range(5):
        link = list_array[7][0][i*2][1]
        links += link + " "
