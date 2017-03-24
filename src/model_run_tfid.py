# code template from Galvanize repo
import pandas as pd
from src.data_prep import read_mongo
from src.data_prep import clean_df
from src.data_prep import remove_non_ascii
from src.data_prep import tokenize_and_normalize
import string
from src.nlp_pipeline import extract_bow_from_raw_text
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.stem.snowball import SnowballStemmer
from nltk import tokenize
from nltk.corpus import stopwords
from src.data_prep import tokenize_and_normalize
from gensim import corpora, models, similarities
from nltk import word_tokenize
from string import punctuation
import cPickle as pickle
import csv

if __name__=='__main__':
    df = read_mongo('wa', 'bing', max=250)
    df = clean_df(df)

    df_train, df_test = train_test_split(df, test_size=.7)

    text = [(v[0][0][1]) for v in df_train[['Text']].values]
    text = [remove_non_ascii(x) for x in text]
    text_test = [(v[0][0][1]) for v in df_test[['Text']].values]
    text_test = [remove_non_ascii(x) for x in text_test]
    links = [(v[0][0][1]) for v in df_train[['Links']].values]
    links = [remove_non_ascii(x) for x in links]
    links_test = [(v[0][0][1]) for v in df_test[['Links']].values]
    links_test = [remove_non_ascii(x) for x in links_test]

    documents = text

    print "Number of docs: " , len(text)
    documents = [remove_non_ascii(x) for x in documents]

    #documents = [tokenize_and_normalize(x) for x in documents]git

    vectorizer = TfidfVectorizer(decode_error='ignore', stop_words='english')
    tfidf_docs = vectorizer.fit_transform(documents)
    cos_sims = linear_kernel(tfidf_docs)

    filename = 'thurs_1740.pkl'
    with open(filename, 'w') as f:
        pickle.dump(cos_sims, f)

    with open (filename[0:-4] + 'text_train.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(text)
    with open (filename[0:-4] + 'text_test.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(text_test)
    with open (filename[0:-4] + 'links_train.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(links)
    with open (filename[0:-4] + 'links_test.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(links_test)
