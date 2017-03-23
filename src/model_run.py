import tfid_model
import numpy as np
import pandas as pd



if __name__=='__main__':
    df = read_mongo('wa', 'bing')
    df = clean_df(df)
    df_link = get_link_array(df)
