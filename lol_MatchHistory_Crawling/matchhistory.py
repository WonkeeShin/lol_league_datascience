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



filenames = open('./LCK2019_Season_temp.txt', 'r')
#season names

for filename in filenames:
    pagesources = open(filename.strip(), 'r')

    wb = openpyxl.Workbook()

    sheet = wb.active

    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}

    options.add_experimental_option("prefs", prefs)

    # options.add_argument('headless')

    options.add_argument('window-size=1920x1080')

    driver = webdriver.Chrome('./chromedriver', chrome_options=options)

    i = 0

    # 로그인 먼저 해보기.
    driver.get('https://matchhistory.euw.leagueoflegends.com/de/#match-details/ESPORTSTMNT05/1090936?gameHash=8500a832de148082&tab=overview')
    time.sleep(0.5)

    # a.riotbar-anonymous-link.riotbar-account-action => 로그인버튼
    driver.find_element_by_css_selector('a.riotbar-anonymous-link.riotbar-account-action').click()  # 이제 로그인 페이지로 감
    time.sleep(0.5)
    # input.field__form-input[0] 이 아이디
    # input.field__form-input[1] 이 비번
    inputs = driver.find_elements_by_css_selector('input.field__form-input')

    lolid = ''
    lolpassword = ''

    inputs[0].send_keys(lolid)
    inputs[1].send_keys(lolpassword)
    driver.find_element_by_css_selector('label.signin-checkbox').click()

    driver.find_element_by_css_selector('button.mobile-button').click()
    time.sleep(5)


    for pagesource in pagesources:
        i = i+1

        pagesource = pagesource.replace('&tab=overview', '')

        pagesource = pagesource + '&tab=overview'


        while True:

            teamlist = []
            team1list = []
            team2list = []

            team1top = []
            team1jg = []
            team1mid = []
            team1ad = []
            team1sp = []
            team1 = [team1top, team1jg, team1mid, team1ad, team1sp]

            team2top = []
            team2jg = []
            team2mid = []
            team2ad = []
            team2sp = []
            team2 = [team2top, team2jg, team2mid, team2ad, team2sp]

            try:
                driver.get(pagesource)
                time.sleep(1)
                containers = driver.find_elements_by_css_selector('div.section-wrapper-content-wrapper div#main div.classic.details > div')
                # head , body , tail 전의 제일 큰 컨테이너

                ## head 부분에서 경기 날짜, 시간 가져오기
                head = containers[0].find_element_by_css_selector('div.gs-container')
                gameduration = head.find_element_by_css_selector('span.map-header-duration').text
                gamedate = head.find_element_by_css_selector('span.map-header-date').text
                print(gamedate, gameduration)
                teamlist.append(gamedate)
                teamlist.append(gameduration)

                ## body 부분에서 경기 내용 가져오기.
                body = containers[1].find_elements_by_css_selector('div.scoreboard > div > div > div > div')

                ###################### blue team
                    # 전반적 승/패 골드 킬
                team_header = body[0].find_element_by_css_selector('div > header')

                team_result = team_header.find_element_by_css_selector('div.game-conclusion').text.strip()
                team_gold = team_header.find_element_by_css_selector('div.gold').text.strip()
                team_kills = team_header.find_element_by_css_selector('div.kills').text.strip()
                # print(team_result, team_gold, team_kills)
                team1list.append(team_result)
                team1list.append(team_gold)
                team1list.append(team_kills)



                    # 챔피언 소환사주문 선수이름
                team_bodys = body[0].find_elements_by_css_selector('ul.grid-list > li')
                        # 선수 1명
                        # 1번 탑 선수 기준
                # print('team_bodys counts')
                # print(len(team_bodys))

                for teamplayer in team_bodys:
                    # print()
                    index = team_bodys.index(teamplayer)

                    player_name_container = teamplayer.find_element_by_css_selector('div.name')
                                # 챔피언 이름, 챔피언 레벨
                    champion_name = player_name_container.find_element_by_css_selector('div.champion-icon > div')
                    champ_name = champion_name.get_attribute('data-rg-id')
                    champ_ver = champion_name.get_attribute('data-rg-name')
                    champ_level = player_name_container.find_element_by_css_selector('span.champion-nameplate-level div.binding').text

                    # print(champ_ver, champ_name, champ_level)

                                # 선수 이름
                    player_name = player_name_container.find_element_by_css_selector('div.champion-nameplate-name > div').text
                    # print(player_name)
                    team1[index].append(player_name)
                    team1[index].append(champ_ver)
                    team1[index].append(champ_name)
                    team1[index].append(champ_level)

                                # 소환사 주문
                    champion_spells = player_name_container.find_elements_by_css_selector('div.spell-book > div')
                    for spell in champion_spells:
                        champion_spells2 = spell.find_element_by_css_selector('div')
                        champion_spell_ver = champion_spells2.get_attribute('data-rg-name')
                        champion_spell = champion_spells2.get_attribute('data-rg-id')
                        # print(champion_spell_ver, champion_spell)
                        team1[index].append(champion_spell_ver)
                        team1[index].append(champion_spell)

                    # 밴, 타워킬, 억제기킬, 바론킬, 드래곤킬, 전령킬
                team_footer = body[0].find_element_by_css_selector('div > footer div.gs-container')

                        # 밴
                team_bans = team_footer.find_elements_by_css_selector('div.champion-nameplate')
                # print()
                # print('bans')


                for ban in team_bans:
                    ban = ban.find_element_by_css_selector('div.champion-icon div')
                    ban_name = ban.get_attribute('data-rg-id')
                    # print(ban_name)
                    team1list.append(ban_name)

                # print()
                        # 타워킬
                team_towerkill = team_footer.find_element_by_css_selector('div.tower-kills').text.strip()
                        # 억제기 킬
                team_inhibitorkill = team_footer.find_element_by_css_selector('div.inhibitor-kills').text.strip()
                        # 바론 킬
                team_baronkill = team_footer.find_element_by_css_selector('div.baron-kills').text.strip()
                        # 드래곤 킬
                team_dragonkill = team_footer.find_element_by_css_selector('div.dragon-kills').text.strip()
                        # 전령 킬
                team_riftkill = team_footer.find_element_by_css_selector('div.rift-herald-kills').text.strip()

                # print('타워킬', team_towerkill)
                # print('억제기 킬', team_inhibitorkill)
                # print('바론 킬', team_baronkill)
                # print('드래곤 킬', team_dragonkill)
                # print('전령 킬', team_riftkill)
                team1list.append(team_towerkill)
                team1list.append(team_inhibitorkill)
                team1list.append(team_baronkill)
                team1list.append(team_dragonkill)
                team1list.append(team_riftkill)

                ####################################### red team
                    # 전반적 승/패 골드 킬
                team_header = body[1].find_element_by_css_selector('div > header')

                team_result = team_header.find_element_by_css_selector('div.game-conclusion').text.strip()
                team_gold = team_header.find_element_by_css_selector('div.gold').text.strip()
                team_kills = team_header.find_element_by_css_selector('div.kills').text.strip()
                # print()
                # print(team_result, team_gold, team_kills)
                team2list.append(team_result)
                team2list.append(team_gold)
                team2list.append(team_kills)

                    # 챔피언 소환사주문 선수이름
                team_bodys = body[1].find_elements_by_css_selector('ul.grid-list > li')
                        # 선수 1명
                        # 1번 탑 선수 기준
                # print('team_bodys counts')
                # print(len(team_bodys))

                for teamplayer in team_bodys:
                    # print()
                    index = team_bodys.index(teamplayer)

                    player_name_container = teamplayer.find_element_by_css_selector('div.name')
                                # 챔피언 이름, 챔피언 레벨
                    champion_name = player_name_container.find_element_by_css_selector('div.champion-icon > div')
                    champ_name = champion_name.get_attribute('data-rg-id')
                    champ_ver = champion_name.get_attribute('data-rg-name')
                    champ_level = player_name_container.find_element_by_css_selector('span.champion-nameplate-level div.binding').text

                    # print(champ_ver, champ_name, champ_level)


                                # 선수 이름

                    player_name = player_name_container.find_element_by_css_selector('div.champion-nameplate-name > div').text
                    # print(player_name)


                    team2[index].append(player_name)
                    team2[index].append(champ_ver)
                    team2[index].append(champ_name)
                    team2[index].append(champ_level)


                                # 소환사 주문
                    champion_spells = player_name_container.find_elements_by_css_selector('div.spell-book > div')
                    for spell in champion_spells:
                        champion_spells2 = spell.find_element_by_css_selector('div')
                        champion_spell_ver = champion_spells2.get_attribute('data-rg-name')
                        champion_spell = champion_spells2.get_attribute('data-rg-id')
                        # print(champion_spell_ver, champion_spell)
                        team2[index].append(champion_spell_ver)
                        team2[index].append(champion_spell)


                team_footer = body[1].find_element_by_css_selector('div > footer div.gs-container')

                        # 밴
                team_bans = team_footer.find_elements_by_css_selector('div.champion-nameplate')
                # print()
                # print('bans')
                for ban in team_bans:
                    ban = ban.find_element_by_css_selector('div.champion-icon div')
                    ban_name = ban.get_attribute('data-rg-id')
                    # print(ban_name)
                    team2list.append(ban_name)

                # print()
                        # 타워킬
                team_towerkill = team_footer.find_element_by_css_selector('div.tower-kills').text.strip()
                        # 억제기 킬
                team_inhibitorkill = team_footer.find_element_by_css_selector('div.inhibitor-kills').text.strip()
                        # 바론 킬
                team_baronkill = team_footer.find_element_by_css_selector('div.baron-kills').text.strip()
                        # 드래곤 킬
                team_dragonkill = team_footer.find_element_by_css_selector('div.dragon-kills').text.strip()
                        # 전령 킬
                team_riftkill = team_footer.find_element_by_css_selector('div.rift-herald-kills').text.strip()

                # print('타워킬', team_towerkill)
                # print('억제기 킬', team_inhibitorkill)
                # print('바론 킬', team_baronkill)
                # print('드래곤 킬', team_dragonkill)
                # print('전령 킬', team_riftkill)
                team2list.append(team_towerkill)
                team2list.append(team_inhibitorkill)
                team2list.append(team_baronkill)
                team2list.append(team_dragonkill)
                team2list.append(team_riftkill)
            except:
                print('오류')
                wb.save(filename.strip().replace('.txt','.xlsx'))
                driver.refresh()
                time.sleep(2)
                continue
            break

        pagesource = pagesource.replace('overview', 'stats')
        while True:
            try:

                # driver.implicitly_wait(10)
                time.sleep(1)
                driver.get(pagesource)

                time.sleep(1)

                containers2 = driver.find_element_by_css_selector('div.section-wrapper-content-wrapper div#main div.classic.details div.tab-panel-body')
                # head , body , tail 전의 제일 큰 컨테이너

                tail_stats = containers2.find_element_by_css_selector('tbody#stats-body')
                # 통계 tail

                tail_trs = tail_stats.find_elements_by_css_selector('tr.grid-row')

                for tr in tail_trs:
                    tdindex = 0
                    for td in tr.find_elements_by_css_selector('td > div'):
                        # print('tdindex')
                        # print(tdindex)
                        # print(td.text.strip())
                        tdtext = td.text.strip()
                        # tdindex = tr.find_elements_by_css_selector('td div').index(td)
                        if tdindex == 0:
                            pass
                        elif tdindex >= 1 and tdindex <= 5:
                            team1[tdindex-1].append(tdtext)
                        elif tdindex >= 6 and tdindex <= 10:
                            team2[tdindex-6].append(tdtext)
                        tdindex = tdindex + 1

            except:
                print('오류')
                wb.save(filename.strip().replace('.txt','.xlsx'))
                driver.refresh()
                time.sleep(2)
                continue
            break

        while True:
            team11list = []
            team22list = []
            try:
                team11list = teamlist + ['blue'] + team1list
                # sheet.append(teamlist)
                # sheet.append(team1list)
                for player in team1:
                    player = team11list + player
                    sheet.append(player)
                # sheet.append(team2list)
                team22list = teamlist + ['red'] + team2list
                for player in team2:
                    player = team22list + player
                    sheet.append(player)

                print(i)
            except:
                print('오류')
                wb.save(filename.strip().replace('.txt','.xlsx'))
                driver.quit()
                continue
            break

        if i // 5 == 0:
            wb.save(filename.strip().replace('.txt','.xlsx'))

    pagesources.close()

    wb.save(filename.strip().replace('.txt','.xlsx'))

    driver.quit()

filenames.close()

