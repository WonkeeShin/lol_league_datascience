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
import json

# file_path = "./sample.json"

filenames = open('./LCS2020_Season.txt', 'r')
#season names

wb = openpyxl.Workbook()

sheet = wb.active

for filename in filenames:
    pagesources = open(filename.strip(), 'r')

    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}

    options.add_experimental_option("prefs", prefs)

    # options.add_argument('headless')

    options.add_argument('window-size=1920x1080')

    driver = webdriver.Chrome('./chromedriver', chrome_options=options)

    # 로그인 먼저 해보기.
    driver.get('https://matchhistory.euw.leagueoflegends.com/de/#match-details/ESPORTSTMNT05/1090936?gameHash=8500a832de148082&tab=overview')
    time.sleep(1)

    # a.riotbar-anonymous-link.riotbar-account-action => 로그인버튼
    # driver.find_element_by_css_selector('a.riotbar-anonymous-link.riotbar-account-action').click()  # 이제 로그인 페이지로 감
    # input.field__form-input[0] 이 아이디
    # input.field__form-input[1] 이 비번

    inputs = driver.find_elements_by_css_selector('input.field__form-input')

    lolid = ''
    lolpassword = ''

    inputs[0].send_keys(lolid)
    inputs[1].send_keys(lolpassword)
    driver.find_element_by_css_selector('label.signin-checkbox').click()

    driver.find_element_by_css_selector('button.mobile-button').click()
    time.sleep(2)

    for pagesource in pagesources:

        pagesource = pagesource.replace('&tab=overview', '')
        # driver.get(pagesource)

        # 타임라인 url 예시
        # https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT03/1143228/timeline?gameHash=cb582988f785f27f

        pagesource2 = pagesource[pagesource.index('E') : pagesource.index('?')]
        # http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT03/1143228?gameHash=cb582988f785f27f
        # => pagesource2 = ESPORTSTMNT03/1143228

        pagesource3 = pagesource[pagesource.index('?') :]
        # => pagesource3 = ?gameHash=cb582988f785f27f

        GameStatsUrl = "https://acs.leagueoflegends.com/v1/stats/game/" + pagesource2 + pagesource3

        error_check = 0
        while (error_check == 0):
            try:
                driver.get(GameStatsUrl)
                time.sleep(2)
                print(GameStatsUrl)
                gamestats = driver.find_element_by_css_selector('pre').text
                error_check = 1
            except:
                driver.refresh()
                wb.save('LCS2020_Spring_Timeline' + '.xlsx')


        stats_dict = json.loads(gamestats)

        team1_mem1 = []
        team1_mem2 = []
        team1_mem3 = []
        team1_mem4 = []
        team1_mem5 = []
        team1 = [team1_mem1, team1_mem2, team1_mem3, team1_mem4, team1_mem5]
        team2_mem1 = []
        team2_mem2 = []
        team2_mem3 = []
        team2_mem4 = []
        team2_mem5 = []
        team2 = [team2_mem1, team2_mem2, team2_mem3, team2_mem4, team2_mem5]

        for i in range(5):
            print(stats_dict['participantIdentities'][i]['player']['summonerName'])
            team1[i].append(stats_dict['participantIdentities'][i]['player']['summonerName'])

        print(team1)

        for i in range(5, 10):
            print(stats_dict['participantIdentities'][i]['player']['summonerName'])
            team2[i-5].append(stats_dict['participantIdentities'][i]['player']['summonerName'])

        print(team2)

        timelineurl = "https://acs.leagueoflegends.com/v1/stats/game/" + pagesource2 + '/timeline' + pagesource3

        error_check2 = 0
        while (error_check2 == 0):
            try:
                driver.get(timelineurl)
                time.sleep(2)
                print(timelineurl)
                timeline = driver.find_element_by_css_selector('pre').text
                error_check2 = 1
            except:
                driver.refresh()
                wb.save('LCS2020_Spring_Timeline' + '.xlsx')



        timeline_dict = json.loads(timeline)

        for i in range(len(timeline_dict['frames'])):
            for k in range(5):
                team1[k].append(timeline_dict['frames'][i]['participantFrames'][str(k+1)]['totalGold'])
                print(timeline_dict['frames'][i]['participantFrames'][str(k+1)]['totalGold'])
            for k in range(5, 10):
                team2[k - 5].append(timeline_dict['frames'][i]['participantFrames'][str(k+1)]['totalGold'])
                print(timeline_dict['frames'][i]['participantFrames'][str(k+1)]['totalGold'])

        for i in range(5):
            sheet.append(team1[i])

        for i in range(5):
            sheet.append(team2[i])

    wb.save('LCS2020_Spring_Timeline' + '.xlsx')

    driver.close()