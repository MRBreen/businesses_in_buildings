# code template from Galvanize repo
import pandas as pd
from src.data_prep import read_mongo
from src.data_prep import clean_df
from src.data_prep import get_y_labels
from src.data_prep import remove_non_ascii
from src.data_prep import clean_links
from src.model_nmf import describe_nmf_results
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
    doc_source = 'links'  # 'links' else defaults to text
    file_pref = 'model/mini_100.pkl' #

    if source =='mongo':
        df = read_mongo('wa', 'bing', max=0)
        df = clean_df(df)
        df = get_y_labels(df)
        df_train, df_test = train_test_split(df, test_size=0)

        links = [x for x in df_train['Links'].values]
        links = [remove_non_ascii(link) for link in links]
        links = clean_links(links)

        text = [x for x in df_train['Text'].values[0]]
        text = remove_non_ascii(text)

        df_train.to_csv(file_pref + '_all_train.csv')
        df_test.to_csv(file_pref + '_all_test.csv')
        with open(file_pref + '_text_list.pkl', 'wb') as fp:
            pickle.dump(text, fp)
        with open(file_pref + '_links_list.pkl', 'wb') as fp:
            pickle.dump(links, fp)

    if source != 'mongo':
        filename = sys.argv(1)
        df_train = pd.read_csv(file_pref + '_train.csv')
        df_test = pd.read_csv(file_pref + '_test.csv')

    if doc_source == 'links':
        documents = links
    else:
        documents = text

    print "Number of docs: " , len(links)

    print "Date is cleaned, and 5 files written...starting model"

    if source != 'mongo':
        df_train.to_csv(file_pref + '_all_train.csv')
        df_test.to_csv(file_pref + '_all_test.csv')

    #if text, the tokenizer has minimum of 4 letters, else default of 2 letters.
    start = time.time()
    if documents == text:
        vectorizer = TfidfVectorizer(decode_error='ignore', token_pattern=r'\b\w[a-zA-Z]{2,}\w+\b', stop_words='english')
    else:
        vectorizer = TfidfVectorizer(decode_error='ignore', stop_words='english')
    print 'vect finished: ' , time.time() - start

    doc_term_mat = vectorizer.fit_transform(documents)
    with open(file_pref + '_doc_term_mat_links.pkl', 'w') as f:
        pickle.dump(doc_term_mat, f)
    print "doc term fit finished: " , time.time() - start

    with open(file_pref + '_vectorizer_links.pkl', 'w') as f:
        pickle.dump(vectorizer, f)

    cos_sims = linear_kernel(doc_term_mat)
    print 'cos similarity finished...dumping to pkl: ' , time.time() - start
    with open(file_pref + '_cos_links.pkl', 'w') as f:
        pickle.dump(cos_sims, f)
    print 'done. daved to pkl: ' , time.time() - start
