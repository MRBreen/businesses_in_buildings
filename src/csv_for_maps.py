# code template from Galvanize repo
import pandas as pd
from src.data_prep import read_mongo
from src.data_prep import clean_df
from src.data_prep import get_y_labels
from src.data_prep import remove_non_ascii
from src.data_prep import clean_links
import string
from sklearn.model_selection import train_test_split
import cPickle as pickle
import csv
import time


if __name__=='__main__':


    source = 'bing'
    documents = 'links'  # to be explicit on which data set is being used
    file_pref = 'model/sea_5300.pkl' #

    if source =='bing':
        df = read_mongo('wa', 'bing', max=0)
        df = clean_df(df)
        df_merged = get_y_labels(df)
        df_merged.drop(['Text'], axis=1)
        df_train, df_test = train_test_split(df, test_size=0)

        links = [x for x in df_train['Links'].values]
        links = [remove_non_ascii(link) for link in links]
        links = clean_links(links)

        df_train.to_csv(file_pref + '_all_train.csv')

        with open(file_pref + '_links_list.pkl', 'wb') as fp:
            pickle.dump(links, fp)

    if source =='biz':
        df = read_mongo('wa', 'biz', max=0)
        df = df.dropna(how='all')
        df = df[df['Bus Name'] != 'General search']
        df = df[df['Bus Name'] != 'name']
        df = df.drop_duplicates(subset='UBI')
        df = df.drop(['Filename','Addr_mail', 'Entity', 'UBI', 'status'], axis=1)
        df = df[~df['Bus Name'].isnull()]

        # merge with output from the model
        file_pref = 'model/sea_5000'
        df_s = pd.read_csv(file_pref + '_group_assignments.csv')

        df['match'] = df['Bus Name'].map(str) + " " + df['Address'].map(str) + " " + df['City'].map(str)
        df = df.merge(df_s, how="inner", left_on='match', right_on='Bus Search')
        df = df[['Bus Name', 'Address', 'City', 'Zip', 'Groups']]
        df = df.drop_duplicates(subset='Bus Name')
        zip_keep = ['98101', '98102', '98102', '98134', '98121']
        df = df[df['Zip'].isin(zip_keep)]
        df["Bus Name"] = df["Bus Name"].astype(str)
        df["Bus Name"] = df["Bus Name"].map(lambda x: x.replace('"',''))
        df["Bus Name"] = df["Bus Name"].map(str.strip)
        df["Address"] = df["Address"].astype(str)
        df["Address"] = df["Address"].map(lambda x: x.replace('"',''))
        df["Address"] = df["Address"].map(str.strip)
        df = df.drop_duplicates(subset='Bus Name')
        for i in range(df.Groups.max() + 1):
            df[df['Groups'] == i].to_csv(file_pref + '_maps_' + str(i) + '.csv')
