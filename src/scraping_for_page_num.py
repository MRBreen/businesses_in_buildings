import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import boto3
from bs4 import BeautifulSoup
import csv
import sys

def sleep():
    time.sleep(2.5+random.random()*1.5)

def remove_placeholder()

if __name__ == '__main__':
    #browser = webdriver.Firefox()
    browser = webdriver.PhantomJS()
    browser.get('http://bls.dor.wa.gov/')
    sleep()
    blink = browser.find_element_by_link_text('Business licenses')
    blink.click()
    sleep()
    new_window = browser.window_handles[1]
    browser.switch_to_window(new_window)
    sleep()

    #with open('data/streets1.csv', 'rb') as f:
    wirh open(sys.argv[1], 'rb')
        reader = csv.reader(f)
        streets = list(reader)

    for street in street_list:
        sleep()
        street_field = browser.find_element_by_name("c-f1")
        city_field = browser.find_element_by_name("c-i1")
        street_field.clear()
        city_field.clear()
        street_field.send_keys(street)
        city_field.send_keys("Seattle")
        search_button = browser.find_element_by_id("c-84")
        sleep()
        search_button.click()
        sleep()

        recordmax = get_maxrecord(browser)
        print "total records for street:" , recordmax
        current_page, page_max = get_current_page(browser)
        current_page = str(current_page).strip()
        page_max = str(page_max).strip()
        page_max = max_page.replace('"','')
        print "current page is" , current_page
        print "max page is " , page_max
        #write_street_page(street, page_max, recordmax)

        stage_file = make_stage_file(streets)
        
