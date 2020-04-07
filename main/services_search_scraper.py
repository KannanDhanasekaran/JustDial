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
from urllib3.exceptions import ReadTimeoutError
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.chrome.service import Service

#service = Service('../driver')
#service.start()

# Get Logger
logger = jdlogging.getLoggerconfig()

# Parser for property file
parser = ConfigParser()
parser.read('..//config//jd.config')

# Properties
BS = "/"
LAST_PAGE = int(parser.get('url', 'last_page'))
MAIN_URL = parser.get('url', 'main_url')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}

# Get SOUP Function
def getsoup1(URL_TO_SCRAPE, PAGE):
    driver = webdriver.Chrome("../driver/chromedriver")
    driver.get(URL_TO_SCRAPE+str(PAGE))
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    return soup

# Get SOUP Function
def getsoup(URL_TO_SCRAPE, PAGE):
    URL_TO_SCRAPE = URL_TO_SCRAPE + str(PAGE)
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

# Get Name
def get_Name(body):
    return body.find('span', {'class': 'jcn'}).a.string

# Get Phone Number
def get_Phone_Number(body):
    contactbody = body.find('p', {'class': 'contact-info'})
    if contactbody is None:
        contactbody = body.find('p', {'class': 'contact-info '})
    #print(contactbody)
    try:
        phone = decrypt_phonenumber(contactbody.span.a)
        return phone
    except KeyError:
        phone = decrypt_phonenumber(contactbody.span.a.b)
        return phone
    except AttributeError:
        logger.error("Exception - Attribute Error "+ str(body))
        #logger.error(traceback.print_exc(file=sys.stdout))
        logger.error(traceback.format_exc())
        #print(body)
        #sys.exit(1)
        return ''

#Decode phone number from span elements
def decrypt_phonenumber(phone):
    try:
        main_phone = ""
        for span_tag in phone:
            main_class = span_tag.attrs['class']
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
        #print(main_phone)
        return main_phone
    except:
        #traceback.print_exc(file=sys.stdout)
        raise

# Get Rating
def get_Rating(body):
    rating = 0.0
    text = body.find('span', {'class': 'star_m'})
    if text is not None:
        for item in text:
            rating += float(item['class'][0][1:]) / 10
    return rating

# Get Rating Count
def get_Rating_Count(body):
    try:
        text = body.find('span', {'class': 'rt_count'}).string
        rating_count = ''.join(i for i in text if i.isdigit())
        return rating_count
    except:
        return ''


# Get Address
def get_address(body):
    return body.find('span', {'class': 'mrehover'}).text.strip()

fields = ['Name', 'Phone', 'Rating', 'Rating Count', 'Address', 'Location', 'Category']
#out_file = open('SearchResult.csv', 'w')
#csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

def writeHeader(csvwriter):
    dict_service = {}
    dict_service['Name'] = "NAME"
    dict_service['Phone'] = "CONTACT NO"
    dict_service['Rating'] = "RATING"
    dict_service['Rating Count'] = "RATING COUNT"
    dict_service['Address'] = "ADDRESS"
    dict_service['Location'] = "LOCATION"
    dict_service['Category'] = "CATEGORY"
    csvwriter.writerow(dict_service)

def fetchDetails(services, location, category, csvwriter):
    for service_html in services:
        # Parse HTML to fetch data
        dict_service = {}
        name = get_Name(service_html)
        phone = get_Phone_Number(service_html)
        rating = get_Rating(service_html)
        count = get_Rating_Count(service_html)
        address = get_address(service_html)
        if name != None:
            dict_service['Name'] = name
        if phone != None:
            dict_service['Phone'] = phone
        if rating != None:
            dict_service['Rating'] = rating
        if count != None:
            dict_service['Rating Count'] = count
        if address != None:
            dict_service['Address'] = address

        dict_service['Location'] = location
        dict_service['Category'] = category
        print(dict_service)
        # Write row to CSV
        csvwriter.writerow(dict_service)

def start(URL, location, category, csvwriter):
    START_TIME = time.time()
    for i in range(1, LAST_PAGE, 1):
        SOUP = getsoup(URL, i)
        services = SOUP.find_all('li', {'class': 'cntanr'})
        if services is None or len(services) == 0:
            break
        else:
            fetchDetails(services, location, category, csvwriter)
    END_TIME = time.time()
    logger.info(jdutility.getStringWithThis("*"))
    logger.info(f"Time taken to scrape the JD for {category} in {location} is {END_TIME - START_TIME} seconds ")
    logger.info(jdutility.getStringWithThis("*"))


#Main Entry
if __name__ == "__main__":
    START_TIME = time.time()
    cityList = jdutility.getCityList()
    keywordList = jdutility.getKeyWordList()
    #Write Header
    #writeHeader()
    #nct-10237947/page-1
    #URL = MAIN_URL + BS + "Bangalore" + BS + "Organic Stores" + BS + "page-"
    #start(URL, "Bangalore", "Grocery Stores")
    #out_file.close()
    #sys.exit(1)
    for location in cityList:
        out_file = open('SearchResult_' + location + '.csv', 'w')
        csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
        writeHeader(csvwriter)
        for category in keywordList:
            logger.info(f"Scrapping for category {category} in {location} ...")
            URL = MAIN_URL + BS + location + BS + category + BS + "page-"
            start(URL, location, category, csvwriter)
    out_file.close()
    END_TIME = time.time()
    logger.info(jdutility.getStringWithThis("*"))
    logger.info(f"Time taken to scrape the complete information from JD is {END_TIME - START_TIME} seconds ")
    logger.info(jdutility.getStringWithThis("*"))