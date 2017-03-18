import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import sys
import boto3
from bs4 import BeautifulSoup
import csv

def sleep():
    time.sleep(2.5+random.random()*1.5)

# from http://programminghistorian.org/lessons/output-data-as-html-file
def write_html(details, street, serial=0):
    '''Writes HTML to a file in the data folder
    '''
    street = street
    filename = '../data/' + street + '_' + str(serial) + '.html'
    f = open(filename, 'w')
    f.write('../data/' + details.encode('utf-8'))

def write_to_s3(details, street, serial):
    """Write HTML to file save in S3
    """
    filename = street + '_' + str(serial) + '.html'
    s3 = boto3.resource('s3')
    b = s3.Bucket('biz-in-buildings')
    b.put_object(Key=filename, Body=details)

def get_maxrecord(browser):
    """Gets total records
    """
    recordmax =0
    total_records = browser.find_elements_by_css_selector("span.TablePageInfo")
    total_records = [total_record for total_record in total_records if total_record.text]
    if len(total_records) > 0:
        total_record = total_records[0]
        recordtext = total_record.text.encode('utf-8')
        recordtext = recordtext.encode('utf-8')
        _text, recordmax = recordtext.strip().split("of")
    return recordmax

def get_current_page(browser):
    """Gets current page number the records table.
    """
    num_pages_raw = browser.find_elements_by_css_selector("a.TablePageLink")
    if type(num_pages_raw) != None:
        num_pages = [num_pages_r for num_pages_r in num_pages_raw if num_pages_r.text]
    if len(num_pages) > 0:
        max_page = num_pages[2]
        max_page = max_page.text.encode('utf-8')
        current_page, page_max = max_page.split(" of ")
        page_max = page_max.replace(',' , '').strip()
        return int(current_page), int(page_max)
    else:
        return 0, 0

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

def write_street_page(street, page, recordmax):
    with open('./street_page.csv','a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([street, str(page), str(recordmax)])

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
            #write_html(details, street, serial)
            write_to_s3(details, street, serial)
            #write_to_s3_tracker(details, street, serial=0)
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
    if len(nextpages) > 0:
        pageclick=[nextpage for nextpage in nextpages if nextpage.is_displayed()]
    if len(nextpages) <= 0:
        sleep()
        browser.refresh
        sleep()
        nextpages = browser.find_elements_by_css_selector("a.TablePageLinkNext")
        pageclick=[nextpage for nextpage in nextpages if nextpage.is_displayed()]
        if len(nextpages) <= 0:
            browser.execute_script("window.history.go(-1)")
            #browser.back()
            sleep()
            nextpages = browser.find_elements_by_css_selector("a.TablePageLinkNext")
            pageclick=[nextpage for nextpage in nextpages if nextpage.is_displayed()]
    if len(nextpages) > 0:
        pageclick[0].click()


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
    street_list = [
    'Alaskan',
    'Alder',
    'Boren',
    'Boylston',
    'Canton',
    'Cherry',
    'Columbia',
    'Jackson',
    'James',
    'Jefferson',
    'King',
    'Lane',
    'Madison',
    'Main',
    'Marion',
    'Maynard',
    'Minor',
    'Occidental',
    'Post',
    'Prefontaine',
    'Railroad',
    'Restrai',
    'Spring',
    'Spruce',
    'Stadium',
    'Terrace',
    'Terry',
    'Washington',
    'Weller',
    'Western',
    'Yesler',
    '10th',
    '11th',
    '1st',
    '2nd',
    '2nd',
    '3rd',
    '4th',
    '5th',
    '6th',
    '7th',
    '8th',
    '9th']

    #(last_street = b[0], last_page = b[1], last_record) = get_index()

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
        print "current page is" , current_page
        print "max page is " , page_max
        write_street_page(street, page_max, recordmax)
