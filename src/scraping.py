import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import sys

def sleep():
    time.sleep(3+random.random()*1.5)

# from http://programminghistorian.org/lessons/output-data-as-html-file
def write_html(details, street, serial=0):
    '''Writes HTML to a file in the data folder
    '''
    street = street
    filename = '../data/' + street + '_' + serial + '.html'
    f = open(filename, 'w')
    f.write('../data/' + details.encode('utf-8'))

def get_pages(browser):
    """Gets total number of pages from the records table.
    """
    total_records = browser.find_elements_by_css_selector("span.TablePageInfo")
    total_records = [total_record for total_record in total_records if total_record.text]
    total_record = total_records[0]
    recordtext = total_record.text.encode('utf-8')
    recordtext = recordtext.encode('utf-8')
    _text, recordmax = recordtext.strip().split("of")
    recordmax = int(recordmax.strip().replace(',', ''))
    return((recordmax-1)/50)

def on_lookup(browser):
    """Returns True if the scraper in on the Lookup Page
    """
    lookup = browser.find_elements_by_class_name("FastTitlebarCaption")
    lookup = [look for look in lookup if look.is_displayed() ]
    if len(lookup) != 0:
        lookpage = lookup[0]
        if (len(lookpage.text) == 23):
            return True

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

def get_lookup_link(browser):
    """Returns list of links...not very robust
    """
    links = browser.find_elements_by_css_selector("a.DocFieldLink")
    links = filter(None, links)
    links = links[2:52]   ##exclude links 0 and 1
    return(links)

def get_good_links(browser):
    """Returns good link on the Lookup Page...has logic to validate and retry
    """
    links = get_lookup_link(browser)
    if on_lookup(browser) == False:
        print "not on lookup page, refresh - get_good_links"
        sleep()
        browser.refresh()
        links = get_lookup_link(browser)
        if on_lookup(browser) == False:
            print "not on lookup page, back - get_good_links"
            browser.back()
            links = get_lookup_link(browser)
            if on_lookup(browser) == False:
                print "not on lookup page, hard back - get_good_links"
                browser.execute_script("window.history.go(-1)")
                sleep()
                links = get_lookup_link(browser)
    if len(links) < 2:
        print "len less than 2 - refresh get_good_links"
        browser.refresh()
        sleep()
        links = get_lookup_link(browser)
        if len(links) < 2:
            print "len less than 2 - hard back get_good_links"
            browser.execute_script("window.history.go(-1)")
            sleep()
            links = get_lookup_link(browser)
    return links


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
            sleep()
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
    browser.get('http://bls.dor.wa.gov/')
    sleep()
    blink = browser.find_element_by_link_text('Business licenses')
    blink.click()
    sleep()
    new_window = browser.window_handles[1]
    browser.switch_to_window(new_window)
    sleep()
    street_list = ['2nd',
    '3rd',
    '4th',
    '5th',
    '6th',
    '7th',
    '8th',
    '9th',
    '1st',
    'Alaskan',
    'Boren',
    'Boylston',
    'Convention',
    'Court',
    'Eastlake',
    'Elliott',
    'Howell',
    'Hubbell',
    'Loos',
    'Minor',
    'Olive',
    'Pike',
    'Pine',
    'Post',
    'Priantat',
    'Seneca',
    'Stewart',
    'Summit',
    'Terry',
    'Union',
    'University',
    'Virginia',
    'Western',
    'Westlake',
    'Yale'
    'Community Club']
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

        pages = get_pages(browser)
        print "pages:" , pages
        for page in range(pages):
             get_fifty(browser, street, page)
             next_page(browser)
