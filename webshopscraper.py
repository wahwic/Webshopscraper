import time
import xml.etree.ElementTree as ET
import undetected_chromedriver as uc

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # keyboard keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from colorama import Fore, Style

#init
#options = Options()
#options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
options = uc.ChromeOptions()
options.headless = True
#options.add_argument('--headless')
#options.add_argument('--window-size=800,600')
#options.page_load_strategy = 'eager'
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driverpath = "C:/Users/skucs/Documents/programming/Python/chromedriver.exe"
#driver = webdriver.Chrome(options=options, executable_path=driverpath)
driver = uc.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'})

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
        name = fixNameString(item, ProductName)
        if checkAvailability(item, Stock):
            price = fixPriceString(item, ProductPrice)
            productUrl = item.find_element_by_css_selector(ProductName).get_attribute('href')
            print(Fore.GREEN + datetime.now().strftime("%H:%M:%S") + ' ' + shopName + ': ' + '{:<60}'.format(name) + ' ->',price,'€ -> ' + productUrl + Style.RESET_ALL)
        else:
            print(Fore.RED + datetime.now().strftime("%H:%M:%S") + ' ' + shopName + ': ' + '{:<60}'.format(name) + ' -> Out of stock.' + Style.RESET_ALL)

def processXmlFile():
    for shop in XMLroot.findall('shop'):
        shopName = shop.attrib.get('name')
        shopUrl = shop.find('url').text
        try:
            driver.get(shopUrl)
            print("Processing shop: " + shopName)
            time.sleep(6)
            getShop(shop)
            print("Finished processing " + shopName)
        except Exception:
            print("Something's fucky with " + shopName)

def fixPriceString(item, ProductPrice):
    price = item.find_element_by_css_selector(ProductPrice)
    price = price.text
    price = price.split('€', 1)[0]
    price = price.replace(' ','')
    if price[len(price)-3] != '.':
        price = price.replace('.','')
    price = price.replace(',','.')
    return float(price)

def fixNameString(item, ProductName):
    name = item.find_element_by_css_selector(ProductName)
    name = name.text.split('\n')[0]
    return name

def checkAvailability(product, Stock):
    #stockContainer = Stock.find('Container').text
    stockAvailabilityClass = Stock.find('IsAvailable').text
    isAvailable = product.find_elements_by_css_selector(stockAvailabilityClass) 

    if not isAvailable: # if list is empty, return not available
        return 0 
    else:
        return 1

if __name__ == '__main__':
    try:
        print('Processing started at ' + datetime.now().strftime("%H:%M:%S"))
        while True:
            processXmlFile()
            print('Waiting 15 seconds for next round')
            time.sleep(15)
    except KeyboardInterrupt:
        pass
    print('Processing ended at ' + datetime.now().strftime("%H:%M:%S"))
    driver.quit() 