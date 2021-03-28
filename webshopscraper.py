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

def getShop(shop):
    ItemsContainer = shop.find('ItemsContainer').text
    ItemsList = shop.find('ItemsList').text
    ProductName = shop.find('ProductName').text
    ProductPrice = shop.find('ProductPrice').text
    Stock = shop.find('Stock')
    getNameAndPrice(shop.attrib.get('name'), ItemsContainer, ItemsList, ProductName, ProductPrice, Stock)

def getNameAndPrice(shopName, ItemsContainer, ItemsList, ProductName, ProductPrice, Stock):
    allItemsContainer = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ItemsContainer)))
    itemsForSale = allItemsContainer.find_elements_by_css_selector(ItemsList)
    for item in itemsForSale:
        if(checkAvailability(item, Stock)):
            name = item.find_element_by_css_selector(ProductName)
            try:
                price = item.find_element_by_css_selector(ProductPrice)
                price = fixPriceString(price)
            except NoSuchElementException:
                price = "Out of stock"
            print(datetime.now().strftime("%H:%M:%S") + ' ' + shopName + ': ' + name.text.split('\n')[0] + ' ->',price,'{currency}'.format(currency='€!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' if type(price) == type(1.1) else ''))

def processXmlFile():
    for shop in XMLroot.findall('shop'):
        shopName = shop.attrib.get('name')
        shopUrl = shop.find('url').text
        try:
            driver.get(shopUrl)
            time.sleep(5)
            print("Processing shop: " + shopName)
            getShop(shop)
            print("Finished processing " + shopName)
        except Exception:
            print("Something's fucky with " + shopName)

def fixPriceString(price):
    price = price.text.replace(' ','')
    price = price.replace(',','.')
    price = price.replace('€','')
    return float(price)

def fixNameString(nameString):
    print()

def checkAvailability(product, Stock):
    stockContainer = Stock.find('Container').text
    stockAvailabilityClass = Stock.find('IsAvailable').text
    isAvailable = product.find_elements_by_css_selector(stockAvailabilityClass)

    if(isAvailable != None):
        return 1
    else:
        return 0

if __name__ == '__main__':
    try:
        print('Processing started at ' + datetime.now().strftime("%H:%M:%S"))
        while True:
            processXmlFile()
            time.sleep(30)
    except KeyboardInterrupt:
        pass
    print('Processing ended at ' + datetime.now().strftime("%H:%M:%S"))
    driver.quit() 