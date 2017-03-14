import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string

def sleep():
    time.sleep(5+random.random()*5)

# from http://programminghistorian.org/lessons/output-data-as-html-file
def write_html(street, serial):
    '''Writes HTML to a file in the data folder
    '''
    street = street
    filename = '../data/' + street + '_' + serial '.html'
    f = open(filename, 'w')
    f.write('../data/' + details.encode('utf-8'))


def street_scrape(street_list)
    '''Scrapes data from list of street
    '''
    for street in street_list:
        street_field = browser.find_element_by_name("c-f1")
        city_field = browser.find_element_by_name("c-i1")
        street_field.send_keys(street)
        city_field.send_keys("Seattle")
        search_button = browser.find_element_by_id("c-84")
        sleep()
        search_button.click()
        page = 0
        # address_scrape()
        #### might make another function here
        links = browser.find_elements_by_css_selector("a.DocFieldLink")
        links = links[2:52]
        links = filter(None, links)
        for link in links:
            if link[i] != "":
                links = browser.find_elements_by_css_selector("a.DocFieldLink")
                links = links[2:52]   ##exclude links 0 and 1
                links = filter(None, links)
                links[i].click()
                sleep()
                details = browser.page_source
                serial = page*50 + i
                write_html (details, serial)
                browser.back()

    return None

if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.get('http://bls.dor.wa.gov/')
    blink = browser.find_element_by_link_text('Business licenses')
    blink.click()
    new_window = browser.window_handles[1]
    browser.switch_to_window(new_window)
    street_scrape('['jackson']')  # can point to data file of csv
