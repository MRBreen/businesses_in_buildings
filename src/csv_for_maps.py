from src.data_prep import read_mongo
import pandas as pd
import string
import cPickle as pickle
import csv
import time


if __name__=='__main__':
    """Creates a cvs file for use with google maps.
    Data from the business records are querried and merged
    with output of a model
    """

    start_file = 'model/alpha_5500.pkl' ##file to be read: _group_assignments.csv')
    file_pref = start_file[0:-4]  # keeps file names consistent

    ############  modify above  #######
    df = read_mongo('wa', 'biz', max=0)
    df = df.dropna(how='all')
    df = df[df['Bus Name'] != 'General search']
    df = df[df['Bus Name'] != 'name']
    df = df.drop_duplicates(subset='UBI')
    df = df.drop(['Filename','Addr_mail', 'Entity', 'UBI', 'status'], axis=1)
    df = df[~df['Bus Name'].isnull()]

    # merge with output from the model
    df_s = pd.read_csv(file_pref + '_group_assignments.csv')

    df['match'] = df['Bus Name'].map(str) + " " + df['Address'].\
                    map(str) + " " + df['City'].map(str)
    df = df.merge(df_s, how="inner", left_on='match', right_on='Bus Search')
    df = df[['Bus Name', 'Address', 'City', 'Zip', 'Groups']]
    df = df.drop_duplicates(subset='Bus Name')
    zip_keep = ['98101', '98102', '98102', '98134', '98121']
    df = df[df['Zip'].isin(zip_keep)]
    df["Bus Name"] = df["Bus Name"].astype(str)
    df["Bus Name"].str.replace('"','')
    df["Bus Name"].str.strip()
    df["Address"] = df["Address"].astype(str)
    df["Address"].str.replace('"','')
    df["Address"].str.strip()
    df = df.drop_duplicates(subset='Bus Name')
    for i in range(df.Groups.max() + 1):
        df[df['Groups'] == i].to_csv(file_pref + '_maps_' + str(i) + '.csv')
