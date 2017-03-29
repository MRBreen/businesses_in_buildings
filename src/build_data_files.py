# code template from Galvanize repo
import pandas as pd
from src.data_prep import read_mongo
from src.data_prep import clean_df
from src.data_prep import tracking_labels
from src.data_prep import clean_links
from src.data_prep import flatten
from src.model_nmf import describe_nmf_results
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import cPickle as pickle
import csv
import time


if __name__=='__main__':
    """Gets data from MongoDB and outputs
    Excel document of cleaned data of links and text
    pickle files
    """

    doc_source = 'text'  # 'links' else defaults to text
    start_file = 'model/alpha_6100_text.pkl' #
    file_pref = start_file[0:-4] # keeps file names consistent

    print "Doc source: ", doc_source
    print "Start file: " , start_file

    df = read_mongo('wa', 'bing', max=0)
    df = clean_df(df)
    df = tracking_labels(df)

    links_raw = [x for x in df['Links'].values]
    links = map(clean_links, links_raw)

    text = df['Text']
    text = map(flatten, text)

    df.to_csv(file_pref + '_all.csv')
    with open(file_pref + '_text_list.pkl', 'wb') as fp:
        pickle.dump(text, fp)
    with open(file_pref + '_links_list.pkl', 'wb') as fp:
        pickle.dump(links, fp)
    print "Number of docs: " , len(links)
    print "Date is cleaned, and 2 files written...starting model"
