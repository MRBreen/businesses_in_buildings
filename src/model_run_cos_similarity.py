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
    """Runs cosine similarity and saves results to a file
    """

    doc_source = 'text' # if not 'links', program defaults to text
    start_file = 'model/alpha_5500.pkl'

    ############  modify above  #######
    file_pref = start_file[0:-4] # keeps file names consistent

    start = time.time()
    if doc_source == 'links':
        with open(file_pref + '_links_list.pkl') as f:
            documents = pickle.load(f)
    else:
        with open(file_pref + '_text_list.pkl') as f:
            documents = pickle.load(f)

    print 'Files loaded in:' , time.time() - start

    #if text, the tokenizer accepts a minimum of 4 letters, else default of 2 letters.
    if doc_source == 'links':
        vectorizer = TfidfVectorizer(decode_error='ignore',
                                    max_features=n_features,
                                    stop_words='english')
    else:
        vectorizer = TfidfVectorizer(decode_error='ignore',
                                max_features=n_features,
                                token_pattern=r'\b\w[a-zA-Z]{2,}\w+\b',
                                stop_words='english')

    doc_term_mat = vectorizer.fit_transform(documents)
    print 'Vectorizer model instance ready: ' , time.time() - start

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
