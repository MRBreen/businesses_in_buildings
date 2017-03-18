from scraping_subroutine import get_fifty
from scraping_subroutine import sleep
from scraping_subroutine import next_page
from scraping_subroutine import get_current_page
import csv
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import sys
import extract

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

    street = sys.argv[1]
    active_page = int(sys.argv[2])
    current_page = 0
    page_max = 0

    #(last_street = b[0], last_page = b[1], last_record) = get_index()

    #with open('street_page_list.csv', newline='') as f:
    #    reader = csv.reader(f)
    #    row1 = next(reader)

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

    #recordmax = get_maxrecord(browser)
    #print "total records for street:" , recordmax
    #current_page, page_max = get_current_page(browser)
    #print "current page is" , current_page
    #print "max page is " , page_max
    #last_page = 0  # commenting out
    for p in range(active_page):
        next_page(browser)
        sleep()
    current_page, page_max = get_current_page(browser)
    for i in range(current_page - active_page):
        print "Pages to go: " , i
        next_page(browser)
        sleep()
        current_page, page_max = get_current_page(broswer)
    get_fifty(browser, street, current_page)
    print "closing successfully"
