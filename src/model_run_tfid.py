# code template from Galvanize repo
import pandas as pd
from src.data_prep import read_mongo
from src.data_prep import clean_df
from src.data_prep import remove_non_ascii
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import tokenize
import cPickle as pickle
import csv

if __name__=='__main__':
    df = read_mongo('wa', 'bing', max=100)
    df = clean_df(df)

    df_train, df_test = train_test_split(df, test_size=.3)

    text = [(v[0][0][1]) for v in df_train[['Text']].values]
    text = [remove_non_ascii(x) for x in text]
    text_test = [(v[0][0][1]) for v in df_test[['Text']].values]
    text_test = [remove_non_ascii(x) for x in text_test]
    links = [(v[0][0][1]) for v in df_train[['Links']].values]
    #links = [l for v in df_train[['Links']].values)]
    links = [remove_non_ascii(x) for x in links]
    links_test = [(v[0][0][1]) for v in df_test[['Links']].values]
    links_test = [remove_non_ascii(x) for x in links_test]

    documents = links

    print "Number of docs: " , len(text)
    documents = [remove_non_ascii(x) for x in documents]

    vectorizer = TfidfVectorizer(decode_error='ignore', stop_words='english')
    tfidf_docs = vectorizer.fit_transform(documents)
    cos_sims = linear_kernel(tfidf_docs)

    filename = 'thurs_1940.pkl'
    with open(filename, 'w') as f:
        pickle.dump(cos_sims, f)

    with open (filename[0:-4] + 'text_train.txt', 'w') as f:
         [f.write(i + "\n") for i in text]
    with open (filename[0:-4] + 'text_test.txt', 'w') as f:
        [f.write(i) for i in text_test]
    with open (filename[0:-4] + 'links_train.txt', 'w') as f:
        [f.write(i) for i in links]
    with open (filename[0:-4] + 'links_test.txt', 'w') as f:
        [f.write(i) for i in links_test]
