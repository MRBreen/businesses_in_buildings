
import cPickle as pickle
import csv
import pandas as pd
import numpy as np
from numpy.random import rand
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
from nltk.tokenize.moses import MosesTokenizer
import time


def reconst_mse(target, left, right):
    return (np.array(target - left.dot(right))**2).mean()

def describe_nmf_results(doc_term_mat, W, H, n_top_words = 15):
    print("Reconstruction error: %f") %(reconst_mse(doc_term_mat, W, H))
    with open (file_pref + '_' + str(H.shape[0]) + '_describe_results.txt', 'w') as f:
        f.write("")
    for topic_num, topic in enumerate(H):
        a = "Topic %d:" % topic_num
        b = (" ".join([feature_words[i] \
                for i in topic.argsort()[:-n_top_words - 1:-1]]))
        with open (file_pref + '_' + str(H.shape[0]) + '_describe_results.txt', 'a') as f:
            f.write(a + b)
        print a
        print b
    return

def my_nmf(doc_term_mat, n_components, n_iterations=50, eps=1e-6):
    n_rows, n_cols = doc_term_mat.shape
    W = rand(n_rows*n_components).reshape([n_rows, n_components])
    H = rand(n_components*n_cols).reshape([n_components, n_cols])
    # linalg.lstsq doesn't work on sparse mats
    dense_doc_term_mat = doc_term_mat.todense()
    for i in range(n_iterations):
        H = np.linalg.lstsq(W, dense_doc_term_mat)[0].clip(eps)
        W = np.linalg.lstsq(H.T, dense_doc_term_mat.T)[0].clip(eps).T
    return np.array(W), np.array(H)

if __name__ == "__main__":
    n_features = 15000
    n_topics = 5
    start = time.time()

    file_pref = 'model/sea_5000'
    with open(file_pref + '_vectorizer_links.pkl') as f:
        vectorizer_pkl = pickle.load(f)
    with open(file_pref + '_links_list.pkl') as f:
        documents = pickle.load(f)
    with open(file_pref + '_doc_term_mat_links.pkl') as f:
        doc_term_mat = pickle.load(f)
    with open(file_pref + '_cos_links.pkl') as f:
        cos = pickle.load(f)

    print 'start up:' , time.time() - start

    for n_topics in range(1,4):
        feature_words = vectorizer_pkl.get_feature_names()
        print 'Time for Features:' , time.time() - start

        print("\n\n---------\nsklearn decomposition")
        nmf = NMF(n_components=n_topics)
        W_sklearn = nmf.fit_transform(doc_term_mat)
        H_sklearn = nmf.components_
        print 'Time for fit transform:' ,  time.time() - start

        print("\n\n---------\nMy decomposition")
        W_mine, H_mine = my_nmf(doc_term_mat, n_components=n_topics, n_iterations=50, eps=1e-6)
        describe_nmf_results(doc_term_mat, W_mine, H_mine)
        print 'Time for fit transform:' , time.time() - start
