from selenium import webdriver
# import chromedriver_binary
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

listings = []


def scrape_findahome():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get('https://www.findahome.hu/ingatlanok/?search=all')
    time.sleep(0.5)
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'ingatlan-cont grid-23 mobile-grid-100 tablet-grid-23')))
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    posts = soup.find_all(
        'div', class_='ingatlan-cont grid-23 mobile-grid-100 tablet-grid-23')
    hidden = soup.find_all(
        'div', class_='ingatlan-cont grid-23 mobile-grid-100 tablet-grid-23 invisible')
    all_posts = posts + hidden

    # * Finding all visible posts and scraping them for price, size, rooms and address
    for ls in all_posts:
        price = ls.find('div', class_='ar').text[:-4].strip()
        size = ls.find('div', class_='meret').text[7:-3].strip()
        rooms = ls.find('div', class_='szobalista').text.replace(
            '\n', '').strip()[:-1]
        address = ls.find('div', class_='cim').text.strip()
        link = ls.find('a', class_='ingatlan_link')
        listings.append([price, size, rooms, address, link['href']])
    driver.quit()
    return listings


def scrape_greatforest():
    # * Going to a new website
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    driver.get('https://greatforest.hu/properties?f-business=rent&f-location=&f-room=&f-price-min=&f-price-max=&f-size-min=&f-size-max=&f-exclusive=&f-tag-catalogid=&f-tag-description=&f-keyword=&price-type=eft')
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'hentry')))
    time.sleep(1)

    # * Going through the different pages (1 to 9)
    for i in range(1, 4):
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'hentry')))
        time.sleep(0.5)
        page2 = driver.page_source
        soup = BeautifulSoup(page2, 'html.parser')
        posts2 = soup.find_all('article', class_='hentry')
        # * Finding all visible posts and scraping them for price, size, rooms and address
        for ls in posts2:
            price = ls.find(
                'span', attrs={'style': 'top: 3px; font-size:16px; text-align: left;'})
            if price:
                price = price.text[:-3].strip()
            else:
                price = None

            size = ls.find('div', class_='size')
            if size:
                size = size.text[:-3].replace('\n', '').strip()
            else:
                size = None

            rooms = ls.find('span', attrs={'style': 'padding-left: 10px;'})
            if rooms:
                rooms = rooms.text[7:].strip()
            else:
                rooms = None

            link = ls.find('a', attrs={'target': '_blank'})
            if link:
                link_new = f'https://www.greatforest.hu{link["href"]}'
            else:
                link_new = None
            listings.append([price, size, rooms, None, link_new])
        driver.find_element(
            By.XPATH, f'//*[@id="main-content"]/div[2]/div/div/div[1]/div/div[1]/div[2]/nav/ul/nav/ul/li[{2+i}]/a').click()

    for i in range(6):
        time.sleep(0.2)
        page2 = driver.page_source
        soup = BeautifulSoup(page2, 'html.parser')
        posts2 = soup.find_all('article', class_='hentry')
        # * Finding all visible posts and scraping them for price, size, rooms and address
        for ls in posts2:
            price = ls.find(
                'span', attrs={'style': 'top: 3px; font-size:16px; text-align: left;'})
            if price:
                price = price.text[:-3].strip()
            else:
                price = None

            size = ls.find('div', class_='size')
            if size:
                size = size.text[:-3].replace('\n', '').strip()
            else:
                size = None

            rooms = ls.find('span', attrs={'style': 'padding-left: 10px;'})
            if rooms:
                rooms = rooms.text[7:].strip()
            else:
                rooms = None

            link = ls.find('a', attrs={'target': '_blank'})
            if link:
                link_new = f'https://www.greatforest.hu{link["href"]}'
            else:
                link_new = None
            listings.append([price, size, rooms, None, link_new])
        driver.find_element(
            By.XPATH, f'//*[@id="main-content"]/div[2]/div/div/div[1]/div/div[1]/div[2]/nav/ul/nav/ul/li[5]/a').click()
    driver.quit()
    return listings


def scrape_debrent():
    # * Going to a new website
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    driver.get('https://debrecenrent.hu/')
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, re.compile('property'))))
    actions = ActionChains(driver)
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="search-form"]/fieldset[2]')))
    time.sleep(1)
    element = driver.find_element(
        By.XPATH, '//*[@id="search-form"]/fieldset[2]')
    actions.click(element)
    footer_element = driver.find_element(By.TAG_NAME, "footer")
    for i in range(50):
        if footer_element.location['y'] < driver.execute_script("return window.innerHeight"):
            break
        for i in range(35):
            actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(1.3)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    posts = soup.find_all('article', class_=re.compile('property'))
    for ls in posts:
        type = ls.find('span', class_='property-type').text
        rent = ls.find('div', class_='flags').text[:9].strip()
        if ((type == 'flat') or (type == 'house')) and (rent == 'for rent'):
            price = ls.find('h4', class_='price')
            if price:
                price = price.text[:-7].strip()
            else:
                price = None
            size = ls.find('li', class_='attribute attribute-size')
            if size:
                size = size.text[:-3].strip()
            else:
                size = None
            bed = ls.find('li', class_='attribute attribute-bedrooms')
            if bed:
                bed = bed.text.replace('\n', '').strip()
            else:
                bed = None
            bath = ls.find('li', class_='attribute attribute-bathrooms')
            if bath:
                bath = bath.text.replace('\n', '').strip()
            else:
                bath = None
            address = ls.find('h5', class_='location')
            if address:
                address = address.text.strip()
            else:
                address = None
            link = ls.find('a')
            if (bed == None) and (bath == None):
                rooms = None
            else:
                rooms = bed + ', ' + bath
            listings.append([price, size, rooms, address, link['href']])
        else:
            continue
    driver.quit()
    return listings


scrape_findahome()
scrape_greatforest()
scrape_debrent()
# * Creating a dataframe to store the data in a better format
df = pd.DataFrame(listings, columns=[
    'Price (HUF)', 'Size', 'Rooms', 'Address', 'Link'])
print(len(df))
# * Exporting to an excel file
df.to_excel('housesv2.xlsx', index=False, header=[
            'Price (HUF)', 'Size', 'Rooms', 'Address', 'Link'])
