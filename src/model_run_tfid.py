# code template from Galvanize repo
import pandas as pd
from src.data_prep import read_mongo
from src.data_prep import clean_df
from src.data_prep import remove_non_ascii
from src.data_prep import clean_links
from src.data_prep import compress_links
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk import tokenize
import cPickle as pickle
import csv

if __name__=='__main__':


    #df = read_mongo('wa', 'bing', max=0)
    #df = clean_df(df)

    #df_test, df_train = train_test_split(df, test_size=.3)

    filename = 'links_fr_0053.pkl'
    df_train = pd.read_csv(filename[0:-4] + '_train.csv')

    text =[]
    for i in range(df_train['Text'].shape[0]):
        text.append((df_train['Text'].iloc[i]))
    text = [remove_non_ascii(str(t)) for t in text]
    """
    text_test =[]
    for i in range(df_test['Text'].shape[0]):
         text_test.append(df_test['Text'].iloc[i])
    text_test = [remove_non_ascii(str(t)) for t in text]

    links = clean_links(df_train[['Links']])
    links = compress_links(links)
    links_test = clean_links(df_test[['Links']])
    links_test = compress_links(links_test)
    """
    documents = text  # to be explicit on which data set is being used
    filename = 'text_fr_0053.pkl'  #


    print "Number of docs: " , len(text)

    """
    with open (filename[0:-4] + 'text_train.txt', 'w') as f:
        [f.write(i + "\n") for i in text]
    with open (filename[0:-4] + 'text_test.txt', 'w') as f:
        [f.write(i) for i in text_test]
    with open (filename[0:-4] + 'links_train.txt', 'w') as f:
        [f.write(i) for i in links]
    with open (filename[0:-4] + 'links_test.txt', 'w') as f:
        [f.write(i) for i in links_test]
    df_train.to_csv(filename[0:-4] + '_train.csv')
    df_train.to_csv(filename[0:-4] + '_test.csv')
    """
    print "6 files written..."

    vectorizer = TfidfVectorizer(decode_error='ignore', stop_words='english')
    tfidf_docs = vectorizer.fit_transform(documents)
    cos_sims = linear_kernel(tfidf_docs)


    with open(filename, 'w') as f:
        pickle.dump(cos_sims, f)
