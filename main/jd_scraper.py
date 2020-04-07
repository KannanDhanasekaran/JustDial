import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import sys
import traceback
import jdlogging
import jdutility
import time
from configparser import ConfigParser

from main import jdutility

# Get Logger
from urllib3.exceptions import ReadTimeoutError

logger = jdlogging.getLoggerconfig()

# Parser for property file
parser = ConfigParser()
parser.read('..//config//jd.config')

LAST_PAGE = 50
BS = "/"

MAIN_URL = parser.get('url', 'main_url')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}

# Get SOUP Function
def getsoup(URL_TO_SCRAPE):
    URL_TO_SCRAPE = URL_TO_SCRAPE
    retry = 0
    is_done = False
    max_retries = 10
    sleep_interval = 5
    while retry < max_retries and not is_done:
        try:
            logger.info("Scraping URL ---->" + URL_TO_SCRAPE)
            # Load html's plain data into a variable
            PLAIN_HTML_TEXT = requests.get(URL_TO_SCRAPE, headers=headers)
            # parse the data
            SOUP = BeautifulSoup(PLAIN_HTML_TEXT.text, "html.parser")
            is_done = True
        except ReadTimeoutError:
            retry += 1
            time.sleep(sleep_interval)
    if not is_done:
        logger.error(URL_TO_SCRAPE +' - could not be loaded')
    return SOUP


def innerHTML(element):
    return element.decode_contents(formatter="html")


def get_name(body):
    return body.find('span', {'class': 'jcn'}).a.string


def get_name_ind(body):
    return body.find('span', {'class': 'fn'}).string

def get_rating_ind(body):
    try:
        rating = body.find('span', {'class': 'value-titles'}).string
        return rating
    except:
        return ''

def get_rating_count_ind(body):
    try:
        rating_count = body.find('span', {'class': 'votes'}).string
        return rating_count.strip()
    except:
        return ''

def get_address_ind(body):
    try:
        address = body.find('span', {'class': 'adrstxtr'}).find('span', {'class': 'lng_add'}).string
        return address
    except:
        return ''

def get_phone_number_ind(body):
    try:
        phoneListtags = body.find('ul', {'class': 'comp-contact'}).find('span', {'class': 'telnowpr'}).a
        #phoneListtags = body.find('span', {'class': 'telnowpr'}).a
        print(phoneListtags)
        phoneList = []
        phoneList.append(decode_phonenumber(phoneListtags))
        #for phonetag in phoneListtags:
        #    print('Printing ')
        #    #phoneList.append(decode_phonenumber(phoneListtags))
        return phoneList
        #return body.find('p', {'class': 'contact-info'}).span.a.string
    except KeyError:
        phone = decode_phonenumber_ind(body.find('p', {'class': 'contact-info'}).span.a.b)
        return phone
    except AttributeError:
        print("Exception - Attribute Error ")
        traceback.print_exc(file=sys.stdout)
        return ''

def get_phone_number(body):
    try:
        phone = decode_phonenumber(body.find('p', {'class': 'contact-info'}).span.a)
        return phone
        #return body.find('p', {'class': 'contact-info'}).span.a.string
    except KeyError:
        phone = decode_phonenumber(body.find('p', {'class': 'contact-info'}).span.a.b)
        return phone
    except AttributeError:
        print("Exception - Attribute Error ")
        return ''

#this function uses class of html element to get phone number
def decode_phonenumber(phone):
    try:
        main_phone = ""
        for span_tag in phone:
            print(" Span Str "+ str(span_tag))
            if span_tag is None or str(span_tag).strip() == "":
                continue
            main_class = span_tag.attrs['class']
            print(main_class)
            if 'icon-dc' in main_class:
                main_phone += "+"
            if 'icon-fe' in main_class:
                main_phone += "("
            if 'icon-hg' in main_class:
                main_phone += ")"
            if 'icon-yz' in main_class:
                main_phone += "1"
            if 'icon-wx' in main_class:
                main_phone += "2"
            if 'icon-vu' in main_class:
                main_phone += "3"
            if 'icon-ts' in main_class:
                main_phone += "4"
            if 'icon-rq' in main_class:
                main_phone += "5"
            if 'icon-po' in main_class:
                main_phone += "6"
            if 'icon-nm' in main_class:
                main_phone += "7"
            if 'icon-lk' in main_class:
                main_phone += "8"
            if 'icon-ji' in main_class:
                main_phone += "9"
            if 'icon-acb' in main_class:
                main_phone += "0"
        print(main_phone)
        return main_phone
    except:
        #traceback.print_exc(file=sys.stdout)
        raise

#this function uses class of html element to get phone number
def decode_phonenumber_ind(phone):
    try:
        main_phone = ""
        for span_tag in phone:
            print(" Span Str "+ str(span_tag))
            if span_tag is None or str(span_tag).strip() == "":
                continue
            main_class = span_tag.attrs['class']
            print(main_class)
            if 'icon-ikj' in main_class:
                main_phone += "+"
            if 'icon-fe' in main_class:
                main_phone += "("
            if 'icon-hg' in main_class:
                main_phone += ")"
            if 'icon-yz' in main_class:
                main_phone += "1"
            if 'icon-ba' in main_class:
                main_phone += "2"
            if 'icon-nm' in main_class:
                main_phone += "3"
            if 'icon-ts' in main_class:
                main_phone += "4"
            if 'icon-acb' in main_class:
                main_phone += "5"
            if 'icon-po' in main_class:
                main_phone += "6"
            if 'icon-fe' in main_class:
                main_phone += "7"
            if 'icon-ji' in main_class:
                main_phone += "8"
            if 'icon-hg' in main_class:
                main_phone += "9"
            if 'icon-acb' in main_class:
                main_phone += "0"
        print(main_phone)
        return main_phone
    except:
        #traceback.print_exc(file=sys.stdout)
        raise


def get_rating(body):
    rating = 0.0
    text = body.find('span', {'class': 'star_m'})
    if text is not None:
        for item in text:
            rating += float(item['class'][0][1:]) / 10
    return rating

def get_rating_count(body):
    text = body.find('span', {'class': 'rt_count'}).string
    rating_count = ''.join(i for i in text if i.isdigit())
    return rating_count


def get_address(body):
    return body.find('span', {'class': 'mrehover'}).text.strip()


def getIndividualLink(body):
    #print(body)
    link = body.find('span', {'class': 'jcn'}).a.get('href')
    print(link)
    return link


def get_location(body):
    text = body.find('a', {'class': 'rsmap'})
    if text == None:
        return
    text_list = text['onclick'].split(",")
    latitutde = text_list[3].strip().replace("'", "")
    longitude = text_list[4].strip().replace("'", "")
    return latitutde + ", " + longitude

fields = ['Name', 'Phone', 'Rating', 'Rating Count', 'Address', 'Location', 'Category']
out_file = open('data.csv', 'w')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

def fetchDetails(services, location, category):
    for service_html in services:
        # Parse HTML to fetch data
        dict_service = {}
        name = get_name(service_html)
        phone = get_phone_number(service_html)
        rating = get_rating(service_html)
        count = get_rating_count(service_html)
        address = get_address(service_html)
        #location = get_location(service_html)
        if name != None:
            dict_service['Name'] = name
        if phone != None:
            print('getting phone number')
            dict_service['Phone'] = phone
        if rating != None:
            dict_service['Rating'] = rating
        if count != None:
            dict_service['Rating Count'] = count
        if address != None:
            dict_service['Address'] = address

        dict_service['Location'] = location
        dict_service['Category'] = category
        # Write row to CSV
        csvwriter.writerow(dict_service)

def fetchDetails(services, location, category):
    for service_html in services:
        dict_service = {}
        link = getIndividualLink(service_html)
        ind_soup = getsoup(link)
        name = get_name_ind(ind_soup)
        phone = get_phone_number_ind(ind_soup)
        print(phone)
        rating = get_rating_ind(ind_soup)
        count = get_rating_count_ind(ind_soup)
        address = get_address_ind(ind_soup)
        if name != None:
            dict_service['Name'] = name
        #if phone != None:
        #    print('getting phone number')
        #    dict_service['Phone'] = phone
        if rating != None:
            dict_service['Rating'] = rating
        if count != None:
            dict_service['Rating Count'] = count
        if address != None:
            dict_service['Address'] = address
        print(dict_service)

def start(URL, city, keyword):
    START_TIME = time.time()
    for i in range(1, 2, 1):
        URL = URL + str(i)
        SOUP = getsoup(URL)
        services = SOUP.find_all('li', {'class': 'cntanr'})
        if not services is None:
            fetchDetails(services, city, keyword)
        else:
            break
    END_TIME = time.time()
    logger.info(jdutility.getStringWithThis("*"))
    logger.info(f"Time taken to scrape the JD for {keyword} in {location} is {END_TIME - START_TIME} seconds ")
    logger.info(jdutility.getStringWithThis("*"))


#Main Entry
if __name__ == "__main__":
    cityList = jdutility.getCityList()
    keywordList = jdutility.getKeyWordList()
    category = "Grocery Stores"
    location = "Chennai"
    print(f"Scrapping for category {category} in {location} ...")
    URL = MAIN_URL + BS + location + BS + category + BS + "page-"
    start(URL, location, category)