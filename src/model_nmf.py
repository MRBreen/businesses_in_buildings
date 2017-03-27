
import cPickle as pickle
import csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import time


def reconst_mse(target, left, right):
    return (np.array(target - left.dot(right))**2).mean()

def describe_nmf_results(feature_words, H, file_pref, top_words = 15):
    print("Reconstruction error: %f") %(reconst_mse(doc_term_mat, W, H))
    c = []
    with open (file_pref + '_' + str(H.shape[0]) + '_describe_results.txt', 'w+') as f:
        f.write("")
    for topic_num, topic in enumerate(H):
        a = "Topic %d: " % topic_num
        b = (" ".join([feature_words[i] \
                for i in topic.argsort()[:-top_words - 1:-1]]))
        c = a + b + ' \n'
        print c
        f = open (file_pref + '_' + str(H.shape[0]) + '_describe_results.txt', 'a+')
        f.write(a + b + ' \n')
        f.close()
    return


if __name__ == "__main__":

n_features = 15000
start = time.time()

#file_pref = 'model/sea_5000'
    file_pref = 'model/mini_100'
    with open(file_pref + '_links_list.pkl') as f:
        documents = pickle.load(f)
    #with open(file_pref + '_vectorizer_links.pkl') as f:
    #    vectorizer_pkl = pickle.load(f)
    #with open(file_pref + '_doc_term_mat_links.pkl') as f:
    #    doc_term_mat = pickle.load(f)

    print 'Files loaded in:' , time.time() - start

    vectorizer = TfidfVectorizer(decode_error='ignore', max_features=n_features, stop_words='english')
    doc_term_mat = vectorizer.fit_transform(documents)
    print 'Time for Features:' , time.time() - start


    for n_topics in range(7,8):

        print("\n\n---------\nsklearn decomposition")
        nmf = NMF(n_components=n_topics, random_state=73, alpha=.1,
            l1_ratio=.5).fit(doc_term_mat)

        W = nmf.transform(doc_term_mat)
        with open(file_pref + '_links_nmf_fit_trans_' + str(n_topics) + '.pkl', 'wb') as fp:
            pickle.dump(W, fp)
        H = nmf.components_
        print 'Time for fit transform:' ,  time.time() - start
        feature_words = vectorizer.get_feature_names()
        describe_nmf_results(feature_words, H, file_pref, top_words = 15)
        with open(file_pref + '_links_nmf_fit_trans_' + str(n_topics) + '.pkl', 'wb') as fp:
            pickle.dump(W, fp)
        group_nmf = W.argmax(axis=1)
        df = pd.read_csv(file_pref + '_all_train.csv')
        df[['Groups']] = pd.DataFrame(data=group_nmf)
        df.to_csv(file_pref + '_group_assingments')
