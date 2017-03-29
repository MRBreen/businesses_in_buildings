
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
    """Creates a text file which lists the top words by frequency for
    each of the latent feautures.
    """
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
    """Performs NMF model.
    To optimize the model, the number of latent features can be interated through.

    File outputs use the same prefix as the pickle file used to load data:
    _nmf_fit_trans_W_.pkl - W matrix
    _nmf_fit_trans_H.pkl - H matrix
    _describe_results.tx - Each latent feature's most frequent words
    group_assignments.csv - assigns group to the original data based on argmax
    """
    n_features = 15000
    doc_source = 'text' # if not 'links', program defaults to text
    start_file = 'model/alpha_5500.pkl'
    file_pref = start_file[0:-4] # keeps file names consistent

    ############  modify above  #######
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
    print 'Time for Features:' , time.time() - start

    #can perform multiple n_topics or just one
    for n_topics in range(7,8):
        print("\n---------\nBeginning sklearn decomposition")
        nmf = NMF(n_components=n_topics, random_state=73, alpha=.1,
                                l1_ratio=.5).fit(doc_term_mat)
        print 'Time for fit transform:' ,  time.time() - start
        W = nmf.transform(doc_term_mat)
        with open(file_pref + '_nmf_fit_trans_W_' + str(n_topics) + '.pkl', 'wb') as fp:
            pickle.dump(W, fp)
        H = nmf.components_
        with open(file_pref + '_nmf_fit_trans_H_' + str(n_topics) + '.pkl', 'wb') as fp:
            pickle.dump(H, fp)

        feature_words = vectorizer.get_feature_names()
        describe_nmf_results(feature_words, H, file_pref, top_words = 20)

        group_nmf = W.argmax(axis=1)
        df = pd.read_csv(file_pref + '_all.csv')
        df[['Groups']] = pd.DataFrame(data=group_nmf)
        df.to_csv(file_pref + '_group_assignments.csv')
