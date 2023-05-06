from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import json
from time import sleep
from PIL import Image
from glob import glob
from io import BytesIO
from easyocr import Reader
import urllib
import numpy as np
import os
from cv2 import imdecode, cvtColor, COLOR_RGB2GRAY

# don't touch
PARSER = "lxml"
url = 'https://jo.opensooq.com/en/login'
BASE_LINK = 'https://jo.opensooq.com'
reader = Reader(['en'], gpu=False)

with open('subcat2cat.json', 'r') as f:
    d = json.load(f)
        
def open_chrome(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    return driver


def login(driver, USER_Name, PASSWORD):
    #login = driver.find_element(By.CLASS_NAME, "loginSignupTab")
    #login.click()
    
    user = driver.find_element(By.ID, "loginchecktype-username")

    sleep(3)
    user.send_keys(USER_Name)
    
    log_btn = driver.find_element(By.CLASS_NAME, "fbBtnColor")
    sleep(1)
    log_btn.click()
    
    password = driver.find_element(By.ID, "loginform-password")
    sleep(1)
    password.send_keys(PASSWORD)
    
    log_btn = driver.find_element(By.CLASS_NAME, "submitButton")
    log_btn.click()
    
    sleep(5)
    
    
def select_city(driver, city_or_link):
    if len(city_or_link) < 20:
        driver.get('https://jo.opensooq.com/en/find?have_images=&allposts=&onlyPremiumAds=&onlyDonation=&onlyPrice=&onlyUrgent=&onlyShops=&onlyMemberships=&onlyBuynow=&memberId=&sort=record_posted_date.desc&term=&cat_id=&scid=59&city={}'.format(city_or_link))
    else:
        driver.get(city_or_link)
    return driver

    
    
def get_products(driver):
    soup = BeautifulSoup(driver.page_source, PARSER)
    products_list = soup.find('ul', id="gridPostListing").find_all('li', class_='rectLi relative mb15')
    return products_list


def get_product_info(product):
    d={}

    try:
        name = product.find('h2').find('a').text.strip()
    except:
        return d
    
    try:
        category_list = [i.text.strip('\xa0| ') for i in product.find('div', class_='rectCatesLinks').find_all('span')]
    except:
        category_list = []
        
    href = product.find('h2', class_='fRight').find('a')['href']
    
    product_url = BASE_LINK + href
    product_page = BeautifulSoup(requests.get(product_url).text, "html.parser")
    
    try:
        address = [i.text.strip(' \n-') for i in product_page.find('div', class_='postSideForm').find_all('span')]
    except:
        address = ['address']
    


    d['Name'] = name
    

    d['address'] = '+'.join(address[1:])
    d['category'] = '+'.join(category_list)
    d['product url'] =  product_url
    try:
        img_url = product.find('span', class_='sellerPhone popupPhone inline vMiddle').find_all('img')[-1]['src']
        req = urllib.request.urlopen(img_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = imdecode(arr, -1)
        gray = cvtColor(img, COLOR_RGB2GRAY)
        
        phone_number = reader.readtext(gray)[0][1]
        d['phone number'] = phone_number
    except Exception as e:
        print(e)
        d['phone number'] = np.nan
    
    return d


def display_phone_numbers(driver):
    for button in driver.find_elements(By.XPATH, '//span[@class="sellerPhone popupPhone inline vMiddle"]'):
        driver.execute_script("arguments[0].click();", button)
    return driver

def next_page(driver):
    next_url = BeautifulSoup(driver.find_element(By.XPATH, '//li[@class="next"]').get_attribute('innerHTML'), "html.parser").find('a')['href']
    driver.get(BASE_LINK+next_url)
    
    
def get_main_category(df):
    

    
    
    df['main category'] = df['category'].str.split('+').str[0].str.strip().map(d)
    
    return df


    
def get_master_category(df):
    
    df['main category'] = df['category'].str.split('+').str[0].str.strip().map(d)
    
