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

    maxrecord = get_maxrecord(browser)
    placeholder_files = make_placeholder_files(streets,maxrecord)

    processed_files = get_processed_files()

    queue = set(placeholder_files)-set(processed_files[0:-2])

    for filename in queue:
        filename = filename.decode('utf-8')
        b.put_object(Key=filename)

    print "closing successfully"
