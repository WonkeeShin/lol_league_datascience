from selenium import webdriver
import time
# import openpyxl
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



driver = webdriver.Chrome('./chromedriver')
# 실제 브라우저, 브라우저 조종 권한 생김.
url_base = 'https://lol.gamepedia.com/'
url = 'https://lol.gamepedia.com/LEC/2019_Season'

driver.get(url)
# 2019년 lck 리그 정보 overview

time.sleep(3)

## spring , spring_playoff , summor, summor_playoff 들어있는 리스트 가져오기.
season_list = driver.find_elements_by_css_selector('div.tabheader-top div.tabheader-tab a')
season_url_list = []

f = open(url.replace(url_base, '').replace('/', '') + '.txt', 'w')

for season_url in season_list:
    # print(season_url.get_attribute('href'))
    season_url_list.append(season_url.get_attribute('href'))

for season in season_url_list[1:]:

    f.write('url_' + season.replace(url_base, '').replace('/', '') + '.txt')
    f.write('\n')

    t = open('url_' + season.replace(url_base, '').replace('/', '') + '.txt', 'w')

    driver.get(season)

    time.sleep(2)

    vodlinks = driver.find_element_by_css_selector('span.mdv-showbuttons').click()

    containers = driver.find_elements_by_css_selector('div.mw-parser-output table#md-table tbody tr')

    for container in containers[3:]:
        tds_a = container.find_elements_by_css_selector('td a')
        for a in tds_a:
            if a.text == 'Link' and 'matchhistory' in a.get_attribute('href'):
                print(a.get_attribute('href'))
                t.write(a.get_attribute('href'))
                t.write('\n')

    t.close()

f.close()