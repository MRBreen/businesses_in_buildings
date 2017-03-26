# code template from Galvanize repo
import pandas as pd
from src.data_prep import read_mongo
from src.data_prep import clean_df
from src.data_prep import remove_non_ascii
from src.data_prep import clean_links
from src.data_prep import unlist_links
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.tokenize.moses import MosesTokenizer
import cPickle as pickle
import csv

if __name__=='__main__':


    source = 'mongo'


    if source =='mongo':
        df = read_mongo('wa', 'bing', max=10)
        df = clean_df(df)
        df_train, df_test = train_test_split(df, test_size=0)

        text = [x for x in df_train['Text'].values[0]]
        #for i in range(df_train['Text'].shape[0]):
        #text.append(df_train['Text'].iloc[i] + " ")
        text = [remove_non_ascii(t) for t in text]

        #text_test = [x for x in df_test['Text'].values[0]]
        #text_test =[]
        #for i in range(df_test['Text'].shape[0]):
        #     text_test.append(df_test['Text'].iloc[i])
        #text_test = [remove_non_ascii(str(t)) for t in text_test]

        links = [x for x in df_train['Links'].values[0]]
        links = [remove_non_ascii(link) for link in links]
        links = clean_links(links)
        links = unlist_links(links)
        #links_test = clean_links(df_test[['Links']])
        #links_test = unlist_links(links_test)

    if source != 'mongo':
        filename = sys.argv(1)    #'llinks_fr_0053.pkl'
        df_train = pd.read_csv(filename[0:-4] + '_train.csv')
        df_test = pd.read_csv(filename[0:-4] + '_test.csv')


    documents = links  # to be explicit on which data set is being used
    filename = 'model/sat_100_text_.pkl'  #


    print "Number of docs: " , len(text)

    if source == 'mongo':
        df_train.to_csv(filename[0:-4] + '_all_train.csv')
        df_test.to_csv(filename[0:-4] + '_all_test.csv')
        with open (filename[0:-4] + 'text_train.txt', 'w') as f:
            [f.write(i + "\n") for i in text]
        #with open (filename[0:-4] + 'text_test.txt', 'w') as f:
        #    [f.write(i) for i in text_test]
        with open (filename[0:-4] + 'links_train.txt', 'w') as f:
            [f.write(i) for i in links]
        #with open (filename[0:-4] + 'links_test.txt', 'w') as f:
        #    [f.write(i) for i in links_test]


    print "Date is cleaned, and 5 files written...starting model"

    if source != 'mongo':
        df_train.to_csv(filename[0:-4] + '_all_train.csv')
        df_test.to_csv(filename[0:-4] + '_all_test.csv')

    vectorizer = TfidfVectorizer(decode_error='ignore', token_pattern='.*\([a-z|A-Z]\{4,\}\)', stop_words='english')
    tfidf_docs = vectorizer.fit_transform(documents)
    print "tfid finished"
    feature_words = vectorizer.get_feature_names()

    cos_sims = linear_kernel(tfidf_docs)
    print "cosine similarity finished"

    with open(filename, 'w') as f:
        pickle.dump(cos_sims, f)
