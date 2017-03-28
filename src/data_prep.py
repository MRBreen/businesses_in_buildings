import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
import unicodedata
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
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
    df = df.drop_duplicates(subset='Bus Search')
    delete_close_duplicates = ['UPSIDE COMMERCE, INC. 111 S JACKSON ST #451', 'UPSIDE 111 s Jackson',
               '3DISCOVERED, INC.111 S JACKSON ST.98104',
              'ALGOSNAP INC.111 S JACKSON ST98104']
    for d in delete_close_duplicates:
        df = df[df['Bus Search'].str.contains(d) != True]
    return df

def get_y_labels(df):
    """Creates identification labels, pseudo-y, to track preselected Companies"""
    interest_group = pd.read_csv('data/interest_group.csv', header=0)
    df_i = interest_group[['Bus Search']]
    df_i.drop(['Bus Search'] == 'BRICKMAN SOUTH JACKSON LLC 111 S JACKSON Seattle')
    df_i['Tech Company']  = 1
    df_merged = pd.merge(df, df_i, how='left')
    df_merged = df_merged.fillna(0)
    return(df_merged)

def remove_non_ascii(text):
    """Steps through every character and replaces non_ascii with white space"""
    CHARSET = set(string.lowercase + string.uppercase + string.whitespace + '.')
    out_row = []
    for sublist in text:
        a = ''
        for c in sublist:
            if c in CHARSET:
                a += c
            else:
                a += ' '
        out_row.append(a.decode('ascii'))
    return(out_row)

def clean_links(links):
    """Parces a long link down to the first non-www part of the address"""
    clean = []
    for sublist in links:
        a = ''
        links_company = ''
        for link in sublist:
            x = str(link).split('w.')
            if len(x) > 1:
                core = x[1]
            else:
                core = x[0]

            if '.' in str(link):
                core = core.split('.')[0]
            links_company += core + ' '
        clean.append(links_company.decode('ascii'))
    return(clean)

def tokenize_and_normalize(chunks):
    """Returns stripped down words"""
    words = [ word_tokenize(sent) for sent in sent_tokenize(chunks) ]
    flatten = [ inner for sublist in words for inner in sublist ]
    stripped = []
    for word in flatten:
        if word not in stopwords.words('english'):
            try:
                stripped.append(word.encode('latin-1').decode('utf8').lower())
            except:
                pass
    return [ word for word in stripped if len(word) > 1 ]
