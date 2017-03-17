import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import sys
import extract
from bs4 import BeautifulSoup

def sleep():
    time.sleep(2.5+random.random()*1.5)

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

def write_index(street, page, i):
    row = street + ',' + str(page) + ',' + str(i) + ','
    with open('../data/records_index.csv','a') as myfile:
        myfile.write(row)

def get_index():
    with open("records_index.csv", "rb") as myfile:
        b = myfile.read()
    b = b.split(',')
    b = b[-4:-1]
    return (b[0], b[1], b[2][:-2])

def get_ubi(browser):
    '''Gets ubi for later validatation
    arg: browser
    '''
    self.ubi = self.soup.find(id='caption2_c-i')
    if self.ubi is not None:
        self.ubi = self.ubi.contents[0].encode('utf-8').strip()
    else:
        self.ubi=""

def validation_ubi(browser):
    """Uses BeautifulSoup to validate successful scrape
    arg: browser
    """
    page_values = search_page()
    page_values.build(file)
    soup = BeautifulSoup()
    soup = soup(browser, 'html.parser')
    return get_ubi(browser)


def get_fifty(browser, street, page):
    """Scrapes up to 50 pages and saves as html files
    """
    for i in range(50):
        sleep()
        links = get_good_links(browser)
        print "length of links" , len(links)
        print "i = " , i
        if i < len(links):
            sleep()
            links[i].click()
            sleep()
            details = browser.page_source
            serial = str(page*50 + i)
            print "serial: ", serial
            write_html(details, street, serial)
            write_index(street, page, i)
            browser.back()
            sleep()
            if on_lookup(browser) == False:
                print "not on expected page, refresh"
                browser.refresh()
                sleep()
                if on_lookup(browser) == False:
                    print "not on expected page, back"
                    browser.execute_script("window.history.go(-1)")

def next_page(browser):
    """Get and validates data for next page
    """
    nextpages = browser.find_elements_by_css_selector("a.TablePageLinkNext")
    nextpages = [nextpage for nextpage in nextpages if nextpage.is_displayed()]
    if len(nextpages) == 0:
        sleep()
        browser.refresh
        sleep()
        nextpages = browser.find_elements_by_css_selector("a.TablePageLinkNext")
        nextpages = [nextpage for nextpage in nextpages if nextpage.is_displayed()]
        if len(nextpages) == 0:
            browser.execute_script("window.history.go(-1)")
            #browser.back()
            sleep()
            nextpages = browser.find_elements_by_css_selector("a.TablePageLinkNext")
            nextpages = [nextpage for nextpage in nextpages if nextpage.is_displayed()]
    if len(nextpages) != 0:
        nextpages[0].click()




if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.get('http://www.bing.com/')
    sleep()

    name_address = [""

    for street in street_list:
        sleep()
        street_field = browser.find_element_by_name("c-f1")
        city_field = browser.find_element_by_name("c-i1")
        street_field.clear()
        city_field.clear()
        street_field.send_keys(street)
        city_field.send_keys("Seattle")
        search_button = browser.find_element_by_id("c-84")

        print "pages:" , pages
        for page in range(pages):
             get_fifty(browser, street, page)
             next_page(browser)
