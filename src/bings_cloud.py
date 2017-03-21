from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import datetime
import boto3

def sleep():
    time.sleep(3.7+random.random()*2.5)

def get_search_text(collection):
    """gets search text from mongoDB biz collection and updates the record status to 1
    """
    record = collection.find_one({'Entity' : { "$in": [ "Profit Corporation",
                                          "Corporation",
                                          "Limited Liability Company",
                                          "Professional Limited Liability Company",
                                         "Joint Venture"] } ,
                            'status' : { "$nin" : ["1","2"] } } )
    search = (record['Bus Name'] + " " + record['Address'] + " " + record['City']).encode('utf-8')
    db.biz.update_many({'Bus Name' : record['Bus Name'], 'Address' : record['Address']}, { '$set' : {'status' : 1}})
    return (search, record)

def write_html(details, filename):
    '''Writes HTML to a file in the data folder
    '''
    f = open(filename, 'w')
    f.write('../data/' + details.encode('utf-8'))

def write_to_s3(details, filename):
    """Write HTML to file save in S3
    """
    s3 = boto3.resource('s3')
    b = s3.Bucket('biz-in-buildings-search')
    b.put_object(Key=filename, Body=details)



if __name__ == '__main__':
    db_cilent = MongoClient('mongodb://localhost:27017/') # may soft code later
    db = db_cilent['wa']
    collection = db.biz

    loops = 3
    print "length of sys.argv is: " , len(sys.argv)
    if len(sys.argv) == 2:
        loops = int(sys.argv[1])

    for i in range(loops):     #words = sys.argv[1]
        #browser = webdriver.Firefox()
        browser = webdriver.PhantomJS()
        browser.get('http://bing.com/')
        sleep()
        searchbox = browser.find_element_by_class_name("b_searchbox")

        words, record = get_search_text(collection)
        searchbox.send_keys(words)
        searchbox.send_keys(Keys.RETURN)

        sleep()
        t = datetime.datetime.now()
        filename = str(t.year)+str(t.month)+str(t.day)+"_"+str(t.hour)+str(t.minute)+str(t.second)+"_"+words[0:4]+'.html'
        details = browser.page_source
        write_to_s3(details, filename)
        db.biz.update_one({"_id" : record['_id']}, { '$set' : {'status' : 2}})
        browser.close()
        print "success" , filename
    print "Done"
