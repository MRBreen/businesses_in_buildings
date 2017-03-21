from scraping_subroutine import decompose_filename
from scraping_subroutine import get_specific
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

    filename = sys.argv[1]
    street, page , item = decompose_filename(filename)

    active_page = page
    current_page = 1
    page_max = 0

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
    for p in range(active_page-1):
        next_page(browser)
        sleep()
    current_page, page_max = get_current_page(browser)
    for i in range(current_page - active_page):
        print "Pages to go: " , i
        next_page(browser)
        sleep()
        current_page, page_max = get_current_page(browser)
    print "current job: " , street, current_page
    if current_page == 0:
        print "not getting browser responses. quit."
        quit()
    get_specific(browser, street, page, item)
    print "closing successfully"
