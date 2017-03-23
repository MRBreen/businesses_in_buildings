#  Credits: Code attibuted to Jean-Francois Omhover a.k.a Jeff

import os               # for environ variables
from nlp_pipeline import extract_bow_from_raw_text
import json
from collections import Counter
import numpy as np
#docs = []
#with open('./reviews.json', 'r') as data_file:
#    for line in data_file:
#        docs.append(json.loads(line))

def get_bows(df_list):
    #bows = list(map(lambda row: extract_bow_from_raw_text(df)))

    bows = list(map(lambda row: extract_bow_from_raw_text(row),df_list))
    return(bows)

def term_occ(bow):
    """ term occurence = counting distinct words in each bag
    """
    return(list(map(lambda bow : Counter(bow), bows)))

# term frequency = occurences over length of bag
def get_term_frequency(docs):

    term_freq = list()
    for i in range(len(docs)):
        term_freq.append( {k: (v / float(len(bows[i])))
                       for k, v in term_occ[i].items()} )
    return (term_freq)
