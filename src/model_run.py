import tfid_model
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from data_prep import read_mongo
from data_prep import clean_df
from data_prep import get_array_from_list
from nlp_pipeline import extract_bow_from_raw_text
from tf_idf_vector import get_bows
from collections import Counter


if __name__=='__main__':
    df = read_mongo('wa', 'bing', max=10)
    df = clean_df(df)
    df_link = get_array_from_list(df[['Links']])
    dt_text = get_array_from_list(df[['Text']])
    df_text_train, df_text_test = train_test_split(dt_text, test_size=.7)

    print "Size: " , df_text_train.size
    print "Getting Bag Of Words...."
    df_list = df_text_train #.tolist()
    print "Len of list: " , df_list.size
    print "A sample list:" , df_list[3:4]
    bows = get_bows(df_list)

    for i in range(len(df_list)):
        print("\n--- review: {}".format(df_list[i]))
        print("--- bow: {}".format(bows[i]))

    print "Getting Term Occurence..."

    tem_occ = list(map(lambda bow : Counter(bow), bows))

    term_freq = list()
    for i in range(len(docs)):
        term_freq.append( {k: (v / float(len(bows[i])))
                           for k, v in term_occ[i].items()} )

    for i in range(4,8):
        print("\n--- review: {}".format(docs[i]['reviewText']))
        print("--- bow: {}".format(bows[i]))
        print("--- term_occ: {}".format(term_occ[i]))
        print("--- term_freq: {}".format(term_freq[i]))
