from selenium import webdriver
import time
import openpyxl
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By
# WebDriverWait는 Selenium 2.4.0 이후 부터 사용 가능합니다.
from selenium.webdriver.support.ui import WebDriverWait
# expected_conditions는 Selenium 2.26.0 이후 부터 사용 가능합니다.
from selenium.webdriver.support import expected_conditions as EC
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

wb = openpyxl.Workbook()

sheet = wb.active

pagesource = 'http://lol.qq.com/match/match_data.shtml?bmid=6052'


options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}

options.add_experimental_option("prefs", prefs)

# options.add_argument('headless')

options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome('./chromedriver', chrome_options=options)

driver.get(pagesource)

time.sleep(1)

#이번 매치 총 경기 수 // 이 경기 수 만큼 반복문을 돌아서 각 경기 데이터 수집
games = driver.find_elements_by_css_selector('ul.tab > li')

for game in games:
    tab_button = game.find_element_by_css_selector('a') # 각 경기 정보를 볼 수 있는 탭 버튼.
    tab_button.click()

    time.sleep(1)

    match_info_container = driver.find_element_by_css_selector('div.match-info')
    match_blue = match_info_container.find_element_by_css_selector('div.blue p.team-name').text
    match_red = match_info_container.find_element_by_css_selector('div.red p.team-name').text
    match_info_date = driver.find_element_by_css_selector('div.info p span#game-date').text
    match_info_period = driver.find_element_by_css_selector('div.info p span#game-period').text

    print(match_blue)
    print(match_red)
    print(match_info_date)
    print(match_info_period)
