
import cPickle as pickle
import csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF

def reconst_mse(target, left, right):
    return (np.array(target - left.dot(right))**2).mean()

def describe_nmf_results(document_term_mat, W, H, n_top_words = 15):
    print("Reconstruction error: %f") %(reconst_mse(document_term_mat, W, H))
    for topic_num, topic in enumerate(H):
        print("Topic %d:" % topic_num)
        print(" ".join([feature_words[i] \
                for i in topic.argsort()[:-n_top_words - 1:-1]]))
    return

def my_nmf(document_term_mat, n_components=15, n_iterations=50, eps=1e-6):
    n_rows, n_cols = document_term_mat.shape
    W = rand(n_rows*n_components).reshape([n_rows, n_components])
    H = rand(n_components*n_cols).reshape([n_components, n_cols])
    # linalg.lstsq doesn't work on sparse mats
    dense_document_term_mat = document_term_mat.todense()
    for i in range(n_iterations):
        H = linalg.lstsq(W, dense_document_term_mat)[0].clip(eps)
        W = linalg.lstsq(H.T, dense_document_term_mat.T)[0].clip(eps).T
    return array(W), array(H)

if __name__ == "__main__":
    #n_features = 4000
    #for i in range(15):
    #    n_topics = 5

    filename = 'thurs_1940.pkl'
    with open(filename) as f_un:
        model_unpickled = pickle.load(f_un)

    doc_bodies=[]
    with open(filename[0:-4] + 'text_train.txt', 'rb') as f:
    #with open (filename[0:-4] + 'text_test.csv', 'w') as f:
        for i in f:
            doc_bodies.append(i)

    doc_bodies = [i.replace('\n', "") for i in doc_bodies]

    n_features = 7000
    for i in range(15):
        n_topics = i  #5
    #vectorizer = CountVectorizer(max_features=n_features)
    vectorizer = TfidfVectorizer(max_features=n_features, stop_words='english')
    document_term_mat = vectorizer.fit_transform(doc_bodies)
    feature_words = vectorizer.get_feature_names()

    print("\n\n---------\nsklearn decomposition")
    nmf = NMF(n_components=n_topics)
    W_sklearn = nmf.fit_transform(document_term_mat)
    H_sklearn = nmf.components_
    describe_nmf_results(document_term_mat, W_sklearn, H_sklearn)

    print("\n\n---------\nMy decomposition")
    W_mine, H_mine = my_nmf(document_term_mat, n_components=n_topics, n_iterations=50, eps=1e-6)
    describe_nmf_results(document_term_mat, W_mine, H_mine)
