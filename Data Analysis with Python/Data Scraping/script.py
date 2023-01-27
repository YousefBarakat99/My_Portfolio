from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe", chrome_options=options)
driver.get('https://www.findahome.hu/ingatlanok/?search=all')

page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')
posts = soup.find_all('div', class_='ingatlan-cont grid-23 mobile-grid-100 tablet-grid-23')
listings = []

#* Finding all visible posts and scraping them for price, size, rooms and address
for ls in posts:
    price = ls.find('div', class_='ar').text[:-4].strip()
    size = ls.find('div', class_='meret').text[7:].strip()
    rooms = ls.find('div', class_='szobalista').text.replace('\n', '').strip()[:-1]
    address = ls.find('div', class_='cim').text.strip()
    listings.append([price, size, rooms, address])

#* Finding all hidden posts and scraping them for price, size, rooms and address
hidden = soup.find_all('div', class_='ingatlan-cont grid-23 mobile-grid-100 tablet-grid-23 invisible')
for ls in hidden:
    price = ls.find('div', class_='ar').text[:-4].strip()
    size = ls.find('div', class_='meret').text[7:].strip()
    rooms = ls.find('div', class_='szobalista').text.replace('\n', '').strip()[:-1]
    address = ls.find('div', class_='cim').text.strip()
    listings.append([price, size, rooms, address])

#* Creating a dataframe to store the data in a better format
df = pd.DataFrame(listings)

#* Exporting to an excel file
df.to_excel(r'C:\Users\youse\Desktop\scrape_practice\houses.xlsx', index=False, header=['Price (HUF)', 'Size', 'Rooms', 'Address'])





