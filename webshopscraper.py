import time
import xml.etree.ElementTree as ET

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
driverpath = "C:/Users/skucs/Documents/programming/Python/chromedriver.exe"
driver = webdriver.Chrome(chrome_options=options, executable_path=driverpath)
XMLroot = ET.parse('shops.xml', ET.XMLParser(encoding="utf-8")).getroot()

#get Alza content
def Alzascrape():
    try:
        searchContent = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME, "browsingitemcontainer")))
        items = searchContent.find_elements_by_css_selector('div.browsingitem')
        for item in items:
            name = item.find_element_by_css_selector('div.fb>a.name')
            try:
                price = item.find_element_by_css_selector('div.priceInner>span.c2')
                price = price.text.split(' ')[0]
                price = float(price.replace(',','.'))
            except NoSuchElementException:
                price = "Out of stock"
            print('Alza: '+ name.text.split('\n')[0] + ' -> ',price,'{currency}'.format(currency='€!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' if type(price) == type(1.1) else ''))
    finally:
        driver.quit()

#open page
for XMLurl in XMLroot.findall('./shop/url'):
    driver.get(XMLurl.text)
    time.sleep(5)
    Alzascrape()