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
    #browser = webdriver.Firefox()
    browser = webdriver.PhantomJS()
    browser.get('http://bing.com/')
    sleep()
    searchbox = browser.find_element_by_class_name("b_searchbox")

    words = sys.argv[1]
    searchbox.send_keys(words)
    searchbox.send_keys(Keys.RETURN)

    sleep()
    t = datetime.datetime.now()
    filename = str(t.year)+str(t.month)+str(t.day)+"_"+str(t.hour)+str(t.minute)+str(t.second)+"_"+words[0:4]+'.html'
    details = browser.page_source
    write_to_s3(details, filename)


    print "success" , filename
