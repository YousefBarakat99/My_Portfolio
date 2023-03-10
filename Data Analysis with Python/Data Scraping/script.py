from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe", chrome_options=options)
driver.get('https://www.findahome.hu/ingatlanok/?search=all')

page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')
posts = soup.find_all('div', class_='ingatlan-cont grid-23 mobile-grid-100 tablet-grid-23')
listings = []

#* Finding all visible posts and scraping them for price, size, rooms, address and links
for ls in posts:
    price = ls.find('div', class_='ar').text[:-4].strip()
    size = ls.find('div', class_='meret').text[7:].strip()
    rooms = ls.find('div', class_='szobalista').text.replace('\n', '').strip()[:-1]
    address = ls.find('div', class_='cim').text.strip()
    link = ls.find('a', class_='ingatlan_link')
    listings.append([price, size, rooms, address, link['href']])

#* Finding all hidden posts and scraping them for price, size, rooms, address and links
hidden = soup.find_all('div', class_='ingatlan-cont grid-23 mobile-grid-100 tablet-grid-23 invisible')
for ls in hidden:
    price = ls.find('div', class_='ar').text[:-4].strip()
    size = ls.find('div', class_='meret').text[7:].strip()
    rooms = ls.find('div', class_='szobalista').text.replace('\n', '').strip()[:-1]
    address = ls.find('div', class_='cim').text.strip()
    link = ls.find('a', class_='ingatlan_link')
    listings.append([price, size, rooms, address, link['href']])

#* Going to a new website
driver.execute_script("window.open('about:blank', 'secondtab');")
driver.switch_to.window("secondtab")
driver.get('https://greatforest.hu/properties?f-business=rent&f-location=&f-room=&f-price-min=&f-price-max=&f-size-min=&f-size-max=&f-exclusive=&f-tag-catalogid=&f-tag-description=&f-keyword=&price-type=eft')
time.sleep(1.5)

#* Going through the different pages (1 to 9)
for i in range(1, 4):
    page2 = driver.page_source
    soup = BeautifulSoup(page2, 'html.parser')
    posts2 = soup.find_all('article', class_='hentry')
    #* Finding all visible posts and scraping them for price, size, rooms, links
    for ls in posts2:
        price = ls.find('span', attrs={'style': 'top: 3px; font-size:16px; text-align: left;'})
        if price:
            price = price.text[:-3].strip()
        else:
            price = None
        
        size = ls.find('div', class_='size')
        if size:
            size = size.text.replace('\n','').strip()
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
    driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[2]/div/div/div[1]/div/div[1]/div[2]/nav/ul/nav/ul/li[{2+i}]/a').click()
        
for i in range(6):
    page2 = driver.page_source
    soup = BeautifulSoup(page2, 'html.parser')
    posts2 = soup.find_all('article', class_='hentry')
    #* Finding all visible posts and scraping them for price, size, rooms and address
    for ls in posts2:
        price = ls.find('span', attrs={'style': 'top: 3px; font-size:16px; text-align: left;'})
        if price:
            price = price.text[:-3].strip()
        else:
            price = None
        
        size = ls.find('div', class_='size')
        if size:
            size = size.text.replace('\n','').strip()
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
    driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[2]/div/div/div[1]/div/div[1]/div[2]/nav/ul/nav/ul/li[5]/a').click()

#* Creating a dataframe to store the data in a better format
df = pd.DataFrame(listings)

#* Exporting to an excel file
df.to_excel(r'C:\Users\youse\Desktop\Data Analysis Portfolio\Python\Data Scraping\housesTRIAL.xlsx', index=False, header=['Price (HUF)', 'Size', 'Rooms', 'Address', 'Link'])
