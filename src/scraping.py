import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

def sleep():
    time.sleep(5+random.random()*5)

def 

if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.get('http://bls.dor.wa.gov/')
    blink = browser.find_element_by_link_text('Business licenses')
    blink.click()
    new_window = browser.window_handles[1]
    browser.switch_to_window(new_window)

    street_field = browser.find_element_by_name("c-f1")
    city_field = browser.find_element_by_name("c-i1")
    street_field.send_keys("jackson")
    city_field.send_keys("Seattle")
    search_button = browser.find_element_by_id("c-84")
    search_button.click()
    links = browser.find_elements_by_css_selector("a.DocFieldLink")
    links = links[2:52]   ##exclude links 0 and 1
    links[0].click()
    details = browser.page_source
    details[:50]
    browser.back()
    links = browser.find_elements_by_css_selector("a.DocFieldLink")
    links = links[2:52]
    links[1].click()
    links[1].text
    browser.page_source

sleep()
