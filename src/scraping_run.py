from scraping_subroutine import get_fifty
from scraping_subroutine import sleep
from scraping_subroutine import next_page
from scraping_subroutine import get_current_page
from scraping_subroutine import search_street
import csv
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string

def sleep():
    time.sleep(5.1+random.random()*2.5)

if __name__ == '__main__':
    """scrapes based on street name and page number.  An example call:
    python scraping_run.py Jackson 4 7
    """

    browser = webdriver.Firefox()
    #browser = webdriver.PhantomJS()
    browser.get('http://bls.dor.wa.gov/')
    sleep()
    blink = browser.find_element_by_link_text('Business licenses')
    blink.click()
    sleep()
    new_window = browser.window_handles[1]
    browser.switch_to_window(new_window)
    sleep()

    street = sys.argv[1]
    active_page = 1
    if len(sys.argv) > 2:
        active_page = int(sys.argv[2])
    stop_page = 1000
    if len(sys.argv) > 3:
        stop_page = int(sys.argv[3])
    current_page = 1
    page_max = 0

    search_street(browser, street)

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
    for _i in range(stop_page):
        print "current job: " , street, current_page
        if current_page == 0:
            print "not getting browser responses. quit."
            quit()
        get_fifty(browser, street, current_page)
        next_page(browser)
    print "closing successfully"
