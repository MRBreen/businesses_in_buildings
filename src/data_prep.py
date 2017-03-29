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
    """Returns a DataFrame"""
    client = MongoClient()
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db]

    cursor = db[collection].find(query).limit(max)
    df =  pd.DataFrame(list(cursor))

    if no_id:
        del df['_id']
    return df

def clean_df(df):
    """Returns a dataframe without n/a and duplicates."""
    df = df.dropna()
    df = df.drop_duplicates(subset='Bus Search')
    delete_close_duplicates = ['UPSIDE COMMERCE, INC. 111 S JACKSON ST #451', 'UPSIDE 111 s Jackson',
               '3DISCOVERED, INC.111 S JACKSON ST.98104',
              'ALGOSNAP INC.111 S JACKSON ST98104']
    for d in delete_close_duplicates:
        df = df[df['Bus Search'].str.contains(d) != True]
    return df

def get_y_labels(df):
    """Creates identification labels, pseudo-y, to track preselected Companies."""
    interest_group = pd.read_csv('data/interest_group.csv', header=0)
    df_i = interest_group[['Bus Search']]
    df_i.drop(['Bus Search'] == 'BRICKMAN SOUTH JACKSON LLC 111 S JACKSON Seattle')
    df_i['Tech Company']  = 1
    df_merged = pd.merge(df, df_i, how='left')
    df_merged = df_merged.fillna(0)
    return(df_merged)

def remove_non_ascii(text):
    """Steps through every character and replaces non_ascii with white space."""
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
    """Parces a long link down to the first non-www part of the address."""
    flatten = [item for sublist in links for item in sublist]
    flatten = str(flatten)
    text = string.replace(flatten, '\\' ,  "/" )
    clean = []
    for i in range(10):
        next_start = text.find("]")
        url = text[:text.find('/')]
        try:
            split_number = url.count('.')
        except:
                pass
        try:
            source = (url.split('.')[split_number-1])
        except:
                pass
        if source not in ["u'Ad", "Ad"]:
            clean.append(source)
        text = text[text.find(", u'")+4:]
    return(" ".join(clean))

def flatted(text):
    """Removes lists inside the data for other functions to use. """
    flat = []
    for page in text:
        a = []
        for row in page:
            a.append(row[1])
        flat.append(" ".join(a))
    return(flat)

def tokenize_and_normalize(chunks):
    """Returns stripped down words."""
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
