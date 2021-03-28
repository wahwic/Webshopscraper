import time
import xml.etree.ElementTree as ET

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # keyboard keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#init
options = Options()
options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
options = webdriver.ChromeOptions()
options.headless = True
#options.page_load_strategy = 'eager'
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')

driverpath = "C:/Users/skucs/Documents/programming/Python/chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=driverpath)
XMLroot = ET.parse('shops.xml', ET.XMLParser(encoding="utf-8")).getroot()

def getShop(XMLshopname):
    XMLsearchContent = XMLroot.find(".//shop[@name='{0}']/searchContent".format(XMLshopname)).text
    XMLitems = XMLroot.find(".//shop[@name='{0}']/items".format(XMLshopname)).text
    XMLname = XMLroot.find(".//shop[@name='{0}']/ProductName".format(XMLshopname)).text
    XMLprice = XMLroot.find(".//shop[@name='{0}']/ProductPrice".format(XMLshopname)).text
    getNameAndPrice(XMLshopname, XMLsearchContent, XMLitems, XMLname, XMLprice)

def getNameAndPrice(XMLshopname, XMLsearchContent, XMLitems, XMLname, XMLprice):
    searchContent = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, XMLsearchContent)))
    items = searchContent.find_elements_by_css_selector(XMLitems)
    for item in items:
        name = item.find_element_by_css_selector(XMLname)
        try:
            price = item.find_element_by_css_selector(XMLprice)
            price = fixPriceString(price)
        except NoSuchElementException:
            price = "Out of stock"
        print(datetime.now().strftime("%H:%M:%S") + ' ' + XMLshopname + ': ' + name.text.split('\n')[0] + ' ->',price,'{currency}'.format(currency='€!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' if type(price) == type(1.1) else ''))

def goThroughtXmlFile():
    for XMLshop in XMLroot.findall('./shop'):
        XMLurl = XMLshop.find('./url').text
        XMLshopname = XMLshop.find('./shopname').text
        try:
            driver.get(XMLurl)
            time.sleep(5)
            print("Processing shop: " + XMLshopname)
            getShop(XMLshopname)
            print("Finished processing " + XMLshopname)
        except Exception:
            print("Something's fucky with " + XMLshopname)

def fixPriceString(price):
    price = price.text.replace(' ','')
    price = price.replace(',','.')
    price = price.replace('€','')
    return float(price)

def fixNameString(nameString):
    print()

if __name__ == '__main__':
    try:
        print('Processing started at '+datetime.now().strftime("%H:%M:%S"))
        while True:
            goThroughtXmlFile()
            time.sleep(30)
    except KeyboardInterrupt:
        pass
    print('Processing ended at '+datetime.now().strftime("%H:%M:%S"))
    driver.quit() 