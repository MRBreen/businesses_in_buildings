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
    """Creates excel document of cleaned data and pickle files
    """
    source = 'mongo'
    doc_source = 'text'  # 'links' else defaults to text
    file_pref = 'model/mini_100.pkl' #

    if source =='mongo':
        df = read_mongo('wa', 'bing', max=50)
        df = clean_df(df)
        df = tracking_labels(df)

        links_raw = [x for x in df['Links'].values]
        print 'links in lambda' ,links_raw
        links = map(clean_links, links_raw)
        print '\nclean \n' ,links
        print "type(links) " ,type(links)
        print "type(links[4]) ", type(links[4])

        text = df['Text']
        text = map(flatten, text)
        print 'type(text)' , type(text)
        print 'type(text[4])' ,type(text[4])

        df.to_csv(file_pref + '_all.csv')
        with open(file_pref + '_text_list.pkl', 'wb') as fp:
            pickle.dump(text, fp)
        with open(file_pref + '_links_list.pkl', 'wb') as fp:
            pickle.dump(links, fp)
        print "Number of docs: " , len(links)
        print "Date is cleaned, and 4 files written...starting model"

    if source != 'mongo':
        filename = sys.argv(1)
        df = pd.read_csv(file_pref + '_train.csv')

    #if text, the tokenizer has minimum of 4 letters, else default of 2 letters.
    start = time.time()
    if doc_source == 'links':
        documents = links
        vectorizer = TfidfVectorizer(decode_error='ignore', stop_words='english')
        print vectorizer.idf_
    else:
        documents = text
        vectorizer = TfidfVectorizer(decode_error='ignore', token_pattern=r'\b\w[a-zA-Z]{2,}\w+\b', stop_words='english')

    print 'Vectorizer model instance ready: ' , time.time() - start
    #print documents
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
    print 'done. saved to pkl: ' , time.time() - start
