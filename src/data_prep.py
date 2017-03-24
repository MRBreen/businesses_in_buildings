import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
import unicodedata
import string

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

from gensim import corpora, models, similarities

from string import punctuation

def read_mongo(db, collection, max=0, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ read from Mongo and Store into DataFrame
    """
    client = MongoClient()
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db]

    cursor = db[collection].find(query).limit(max)
    df =  pd.DataFrame(list(cursor))

    if no_id:
        del df['_id']
    return df

def clean_df(df):
    """ cleans up df for all models
    """
    df = df.dropna()
    return df

def remove_non_ascii(text):
    CHARSET = set(string.lowercase + string.digits + string.uppercase + string.whitespace + '.')
    #return ''.join(c for c in text if c in CHARSET)

    line =''
    for c in text:
        if c in CHARSET:
            d = c
        else:
            d = ' '
        line = ''.join(d)
    return line

def tokenize_and_normalize(chunks):
    """Returns stripped down words
    """
    words = [ word_tokenize(sent) for sent in sent_tokenize(chunks) ]
    flatten = [ inner for sublist in words for inner in sublist ]
    stripped = []

    for word in flatten:
        if word not in stopwords.words('english'):
            try:
                stripped.append(word.encode('latin-1').decode('utf8').lower())
            except:
                #print "Cannot encode: " + word
                pass

    return [ word for word in stripped if len(word) > 1 ]
