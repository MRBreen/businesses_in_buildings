import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string

def sleep():
    time.sleep(5+random.random()*2.2)

# from http://programminghistorian.org/lessons/output-data-as-html-file
def write_html(details, street, serial=0):
    '''Writes HTML to a file in the data folder
    '''
    street = street
    filename = '../data/' + street + '_' + serial + '.html'
    f = open(filename, 'w')
    f.write('../data/' + details.encode('utf-8'))


def street_scrape(street):
    '''Scrapes data from street
    '''
    sleep()
    street_field = browser.find_element_by_name("c-f1")
    city_field = browser.find_element_by_name("c-i1")
    street_field.send_keys(street)
    city_field.send_keys("Seattle")
    search_button = browser.find_element_by_id("c-84")
    sleep()
    search_button.click()


def get_fifty(browser, street, page):
    """Scrapes up to 50 pages and saves as html files
    """
    sleep()
    links = browser.find_elements_by_css_selector("a.DocFieldLink")
    links = links[2:52]
    links = filter(None, links)
    stop = len(links)
    print "Length is" , stop
    for i in range(48, stop):
        sleep()
        links = browser.find_elements_by_css_selector("a.DocFieldLink")
        links = links[2:52]   ##exclude links 0 and 1
        links = filter(None, links)
        sleep()
        print i
        print "length of links: " , len(links)
        links[i].click()
        sleep()
        details = browser.page_source
        serial = str(page*50 + i)
        print serial
        write_html(details, street, serial)
        sleep()
        browser.back()
        sleep()
        i+=1

def next_page(browser):
    nextpages = browser.find_elements_by_css_selector(
    "a.TablePageLinkNext")
    nextpages = [nextpage for nextpage in nextpages if nextpage.is_displayed()]
    nextpages[0].click()

    return None

if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.get('http://bls.dor.wa.gov/')
    sleep()
    blink = browser.find_element_by_link_text('Business licenses')
    blink.click()
    sleep()
    new_window = browser.window_handles[1]
    browser.switch_to_window(new_window)
    sleep()
    street_list = ['jackson']
    for street in street_list:
        street_scrape(street)  # can point to data file of csv
        page = 0
        get_fifty(browser, street, page)
        for pages in range(13):
             next_page(browser)
             page += 1
             get_fifty(browser, street, page)
