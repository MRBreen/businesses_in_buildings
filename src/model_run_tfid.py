# code template from Galvanize repo
import pandas as pd
from src.data_prep import read_mongo
from src.data_prep import clean_df
from src.data_prep import remove_non_ascii
from src.data_prep import clean_links
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.tokenize.moses import MosesTokenizer
import cPickle as pickle
import csv
import time


if __name__=='__main__':


    source = 'mongo'
    documents = 'links'  # to be explicit on which data set is being used
    file_pref = 'model/se_10102'  #

    if source =='mongo':
        df = read_mongo('wa', 'bing', max=0)
        df = clean_df(df)
        df_train, df_test = train_test_split(df, test_size=0)

        text = [x for x in df_train['Text'].values[0]]
        #for i in range(df_train['Text'].shape[0]):
        #text.append(df_train['Text'].iloc[i] + " ")
        text = remove_non_ascii(text)

        #text_test = [x for x in df_test['Text'].values[0]]
        #text_test =[]
        #for i in range(df_test['Text'].shape[0]):
        #     text_test.append(df_test['Text'].iloc[i])
        #text_test = [remove_non_ascii(str(t)) for t in text_test]

        links = [x for x in df_train['Links'].values]
        links = [remove_non_ascii(link) for link in links]
        links = clean_links(links)
        #links = [x.decode('ascii') for x in links]
        #links_test = clean_links(df_test[['Links']])
        #links_test = unlist_links(links_test)
        df_train.to_csv(file_pref + '_all_train.csv')
        df_test.to_csv(file_pref + '_all_test.csv')
        with open(file_pref + '_text_list.pkl', 'wb') as fp:
            pickle.dump(text, fp)
        with open(file_pref + '_links_list.pkl', 'wb') as fp:
            pickle.dump(links, fp)
        #with open (file_pref + '_text.txt', 'w') as f:
        #    [f.write(i + "\n") for i in text]
        #with open (file_pref + '_links.txt', 'w') as f:
        #    [f.write(i) for i in links]

    if source != 'mongo':
        filename = sys.argv(1)    #'llinks_fr_0053.pkl'
        df_train = pd.read_csv(file_pref + '_train.csv')
        df_test = pd.read_csv(file_pref + '_test.csv')

    documents = links

    print "Number of docs: " , len(links)

    print "Date is cleaned, and 5 files written...starting model"

    if source != 'mongo':
        df_train.to_csv(file_pref + '_all_train.csv')
        df_test.to_csv(file_pref + '_all_test.csv')

    #if ext, the tokenizer has minimum of 4 letters, else default of 2 letters.
    start = time.time()
    if documents == text:
        vectorizer = TfidfVectorizer(decode_error='ignore', token_pattern=r'\b\w[a-zA-Z]{2,}\w+\b', stop_words='english')
    else:
        vectorizer = TfidfVectorizer(decode_error='ignore', stop_words='english')

    with open(file_pref + 'vect.pkl', 'w') as f:
        pickle.dump(vectorizer, f)
    print 'vect:' , time.time() - start

    tfidf_docs = vectorizer.fit_transform(documents)
    print "tfid finished"
    feature_words = vectorizer.get_feature_names()

    cos_sims = linear_kernel(tfidf_docs)
    print "cosine similarity finished"
    print 'Cos + vect:' , time.time() - start

    with open(file_pref + '_cos.pkl', 'w') as f:
        pickle.dump(cos_sims, f)
