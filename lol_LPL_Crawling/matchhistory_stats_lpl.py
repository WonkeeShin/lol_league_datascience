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


pagesource = 'https://lpl.qq.com/es/stats.shtml?bmid=5655'

options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}

# options.add_experimental_option("prefs", prefs)

# options.add_argument('headless')

options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome('./chromedriver', chrome_options=options)

driver.get(pagesource)
time.sleep(1)

matchs = driver.find_elements_by_css_selector('ul.data-mode1-season > li')

for match in matchs:
    if matchs.index(match) == 0:
        pass
    else:
        match.click()

    time.sleep(0.3)

    driver.find_element_by_css_selector('div.n-data-mode1-data > a:nth-of-type(1)').click()
    time.sleep(0.3)
    try:
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

            # try:
            ## head 부분에서 팀 정보 가져오기. 팀 승리, 오브젝트, 킬 수, 골드 수, 밴밴
            head = driver.find_element_by_css_selector('div.data-season')

            ## 블루 팀
            # 팀 골드 / 팀 킬 수
            team_golds = head.find_elements_by_css_selector('ul.data-main-m li.data-main-m-w2 span.disli')
            team_gold = team_golds[0].text.strip()
            team_kills = head.find_element_by_css_selector('div.data-main-sz p.killnum1').text.strip()
            # print(team_gold, team_kills)

            team1list.append(team_gold)
            team1list.append(team_kills)

            # 팀 밴
            two_bans = head.find_elements_by_css_selector('div.data-main-b')
            blue_bans = two_bans[0].find_elements_by_css_selector('img')
            for blue_ban in blue_bans:
            # 밴
                ban_name = blue_ban.get_attribute('src').strip()
                ban_name = ban_name.replace('https://game.gtimg.cn/images/lol/act/img/champion/','').replace('.png', '')
                # print(ban_name)
                team1list.append(ban_name)

            # 오브젝트 수
            team_container = head.find_elements_by_css_selector('ul.data-main-m li.data-main-m-w1 div.disul > span')
            team_baronkill = team_container[0].text.strip()
            team_dragonkill = team_container[1].text.strip()
            team_towerkill = team_container[2].text.strip()

            # print('타워킬', team_towerkill)
            # print('바론 킬', team_baronkill)
            # print('드래곤 킬', team_dragonkill)
            team1list.append(team_towerkill)
            team1list.append(team_baronkill)
            team1list.append(team_dragonkill)

            team_bodys = driver.find_elements_by_css_selector('tr.nr-battle-item')
            # 라인 별 선수 데이터 // 총 5개

            for teamplayer in team_bodys:
                index = team_bodys.index(teamplayer)
                # print(index)

                player_name = teamplayer.find_element_by_css_selector('div.data-tab-ply1 >p').text.strip()   # 선수 이름
                champion_names_container = teamplayer.find_elements_by_css_selector('div.data-tab-skill') # 챔피언 이름 컨테이너
                champion_names = champion_names_container[0].find_element_by_css_selector('img.out') # 챔피언 초상화
                champion_name = champion_names.get_attribute('src').strip() # 챔피언 초상화 주소
                champ_name = champion_name.replace('https://game.gtimg.cn/images/lol/act/img/champion/','')[:-4] # 챔피언 이름

                # print(player_name, champ_name)
                team1[index].append(player_name)
                team1[index].append(champ_name)

                # 소환사 주문
                champion_spells_container = champion_names_container[0].find_element_by_css_selector('div.nr-img-frame')
                champion_spells = champion_spells_container.find_elements_by_css_selector('img')
                for spell in champion_spells:
                    champion_spell_img = spell.get_attribute('src').strip()
                    champion_spell = champion_spell_img.replace("https://ossweb-img.qq.com/images/lol/img/spell/", '')[:-4]
                    # print(champion_spell)
                    team1[index].append(champion_spell)

            print()
            ## 레트 팀
            # 팀 골드 / 팀 킬 수
            red_team_container = head.find_element_by_css_selector('div.data-main.fr')

            team_gold = red_team_container.find_element_by_css_selector('ul.data-main-m li.data-main-m-w2 span.disli').text.strip()
            team_kills = head.find_element_by_css_selector('div.data-main-sz p.killnum2').text.strip()
            # print(team_gold, team_kills)

            team2list.append(team_gold)
            team2list.append(team_kills)

            # 팀 밴
            red_bans = red_team_container.find_elements_by_css_selector('div.data-main-b img')
            for red_ban in red_bans:
                # 밴
                ban_name = red_ban.get_attribute('src').strip()
                ban_name = ban_name.replace('https://game.gtimg.cn/images/lol/act/img/champion/', '').replace('.png', '')
                # print(ban_name)
                team2list.append(ban_name)

            # 오브젝트 수
            team_container = red_team_container.find_elements_by_css_selector('ul.data-main-m li.data-main-m-w1 div.disul > span')
            team_baronkill = team_container[0].text.strip()
            team_dragonkill = team_container[1].text.strip()
            team_towerkill = team_container[2].text.strip()

            # print('타워킬', team_towerkill)
            # print('바론 킬', team_baronkill)
            # print('드래곤 킬', team_dragonkill)
            team2list.append(team_towerkill)
            team2list.append(team_baronkill)
            team2list.append(team_dragonkill)

            team_bodys = driver.find_elements_by_css_selector('tr.nr-battle-item')
            # 라인 별 선수 데이터 // 총 5개

            for teamplayer in team_bodys:
                index = team_bodys.index(teamplayer)
                # print(index)

                player_name = teamplayer.find_element_by_css_selector('div.data-tab-ply2 >p').text.strip()  # 선수 이름
                champion_names_container = teamplayer.find_elements_by_css_selector('div.data-tab-skill')  # 챔피언 이름 컨테이너
                champion_names = champion_names_container[1].find_element_by_css_selector('img.out')  # 챔피언 초상화
                champion_name = champion_names.get_attribute('src').strip()  # 챔피언 초상화 주소
                champ_name = champion_name.replace('https://game.gtimg.cn/images/lol/act/img/champion/', '')[:-4]  # 챔피언 이름

                # print(player_name, champ_name)
                team2[index].append(player_name)
                team2[index].append(champ_name)

                # 소환사 주문
                champion_spells_container = champion_names_container[1].find_element_by_css_selector('div.nr-img-frame')
                champion_spells = champion_spells_container.find_elements_by_css_selector('img')
                for spell in champion_spells:
                    champion_spell_img = spell.get_attribute('src').strip()
                    champion_spell = champion_spell_img.replace("https://ossweb-img.qq.com/images/lol/img/spell/", '')[:-4]
                    # print(champion_spell)
                    team2[index].append(champion_spell)
            break
    except:
        driver.refresh()
        time.sleep(2)


    try:
        while True:
            # detail informaiton tab
            driver.find_element_by_css_selector('div.n-data-mode1-data > a:nth-of-type(2)').click()
            time.sleep(1)

            # clicked data reset.
            if matchs.index(match) == 0:
                driver.find_element_by_css_selector('dl.damage-dl dd:nth-of-type(1)').click()
                time.sleep(0.3)

            # Blue KDA, spree, multi
            kda_container = driver.find_elements_by_css_selector('dl.fight-dl > dd')
            for n in range(5):
                kda_container[n].click()

                blue_data_container = driver.find_elements_by_css_selector('div.value-show.fl li.value-wid-li > p')
                for i in range(len(blue_data_container)):
                    team1[i].append(blue_data_container[i].text.strip())
                    # print(blue_data_container[i].text.strip())
                # print(team1)

            # Red KDA, spree, multi

                red_data_container = driver.find_elements_by_css_selector('div.value-show.fr li.value-wid-li > p')
                for i in range(len(red_data_container)):
                    team2[i].append(red_data_container[i].text.strip())
                    # print(red_data_container[i].text.strip())
                # print(team2)
                kda_container[n].click()

            # firstblood
            firstblood_img = driver.find_element_by_css_selector('div.first-blood > img')
            firstblood_img_src = firstblood_img.get_attribute('src')
            firstblood = firstblood_img_src.replace('https://game.gtimg.cn/images/lol/act/img/champion/', '').replace('.png', '')
            # print('firstblood', firstblood)

            for i in range(5):
                if firstblood == team1[i][1]:
                    team1[i].append('●')
                else:
                    team1[i].append('○')

                if firstblood == team2[i][1]:
                    team2[i].append('●')
                else:
                    team2[i].append('○')


            # damage tab
            # total Damage to Champ , ad damage to Champ, ap damage to Champ, Total Damage, Ad damage , Ap damage, Largest critical damage
            damage_tab_container = driver.find_elements_by_css_selector('dl.damage-dl > dd')
            for n in range(len(damage_tab_container)):
                # fold the data
                damage_tab_container[n].click()

                blue_data_container = driver.find_elements_by_css_selector('div.value-show.fl li.value-wid-li > p')
                for i in range(len(blue_data_container)):
                    team1[i].append(blue_data_container[i].text.strip())
                    # print(blue_data_container[i].text.strip())

                red_data_container = driver.find_elements_by_css_selector('div.value-show.fr li.value-wid-li > p')
                for i in range(len(red_data_container)):
                    team2[i].append(red_data_container[i].text.strip())

                # unfold the data
                damage_tab_container[n].click()

            # taken damage, heal tab
            # Heal, TakenDamage, AdDamage, ApDamage
            taken_tab_container = driver.find_elements_by_css_selector('dl.treatment-dl > dd')
            for n in range(len(taken_tab_container)):
                # fold the data
                taken_tab_container[n].click()

                blue_data_container = driver.find_elements_by_css_selector('div.value-show.fl li.value-wid-li > p')
                for i in range(len(blue_data_container)):
                    team1[i].append(blue_data_container[i].text.strip())

                red_data_container = driver.find_elements_by_css_selector('div.value-show.fr li.value-wid-li > p')
                for i in range(len(red_data_container)):
                    team2[i].append(red_data_container[i].text.strip())

                # unfold the data
                taken_tab_container[n].click()

            # others
            # Money, Towerkill, Minions, TimeDeath, Level
            other_tab_container = driver.find_elements_by_css_selector('dl.other-dl > dd')
            for n in range(len(other_tab_container)):
                # fold the data
                other_tab_container[n].click()

                blue_data_container = driver.find_elements_by_css_selector('div.value-show.fl li.value-wid-li > p')
                for i in range(len(blue_data_container)):
                    team1[i].append(blue_data_container[i].text.strip())

                red_data_container = driver.find_elements_by_css_selector('div.value-show.fr li.value-wid-li > p')
                for i in range(len(red_data_container)):
                    team2[i].append(red_data_container[i].text.strip())

                # unfold the data
                other_tab_container[n].click()

            print(team1)
            print(team2)

            break
    except:
        driver.refresh()
        time.sleep(2)
# except:
    #     print('오류')
#
#                     # 밴, 타워킬, 억제기킬, 바론킬, 드래곤킬, 전령킬
#                 team_footer = body[0].find_element_by_css_selector('div > footer div.gs-container')
#

#
#                 # print()
#                         # 타워킬
#                 team_towerkill = team_footer.find_element_by_css_selector('div.tower-kills').text.strip()
#                         # 억제기 킬
#                 team_inhibitorkill = team_footer.find_element_by_css_selector('div.inhibitor-kills').text.strip()
#                         # 바론 킬
#                 team_baronkill = team_footer.find_element_by_css_selector('div.baron-kills').text.strip()
#                         # 드래곤 킬
#                 team_dragonkill = team_footer.find_element_by_css_selector('div.dragon-kills').text.strip()
#                         # 전령 킬
#                 team_riftkill = team_footer.find_element_by_css_selector('div.rift-herald-kills').text.strip()
#
#                 # print('타워킬', team_towerkill)
#                 # print('억제기 킬', team_inhibitorkill)
#                 # print('바론 킬', team_baronkill)
#                 # print('드래곤 킬', team_dragonkill)
#                 # print('전령 킬', team_riftkill)
#                 team1list.append(team_towerkill)
#                 team1list.append(team_inhibitorkill)
#                 team1list.append(team_baronkill)
#                 team1list.append(team_dragonkill)
#                 team1list.append(team_riftkill)
#
#                 ####################################### red team
#                     # 전반적 승/패 골드 킬
#                 team_header = body[1].find_element_by_css_selector('div > header')
#
#                 team_result = team_header.find_element_by_css_selector('div.game-conclusion').text.strip()
#                 team_gold = team_header.find_element_by_css_selector('div.gold').text.strip()
#                 team_kills = team_header.find_element_by_css_selector('div.kills').text.strip()
#                 # print()
#                 # print(team_result, team_gold, team_kills)
#                 team2list.append(team_result)
#                 team2list.append(team_gold)
#                 team2list.append(team_kills)
#
#                     # 챔피언 소환사주문 선수이름
#                 team_bodys = body[1].find_elements_by_css_selector('ul.grid-list > li')
#                         # 선수 1명
#                         # 1번 탑 선수 기준
#                 # print('team_bodys counts')
#                 # print(len(team_bodys))
#
#                 for teamplayer in team_bodys:
#                     # print()
#                     index = team_bodys.index(teamplayer)
#
#                     player_name_container = teamplayer.find_element_by_css_selector('div.name')
#                                 # 챔피언 이름, 챔피언 레벨
#                     champion_name = player_name_container.find_element_by_css_selector('div.champion-icon > div')
#                     champ_name = champion_name.get_attribute('data-rg-id')
#                     champ_ver = champion_name.get_attribute('data-rg-name')
#                     champ_level = player_name_container.find_element_by_css_selector('span.champion-nameplate-level div.binding').text
#
#                     # print(champ_ver, champ_name, champ_level)
#
#
#                                 # 선수 이름
#
#                     player_name = player_name_container.find_element_by_css_selector('div.champion-nameplate-name > div').text
#                     # print(player_name)
#
#
#                     team2[index].append(player_name)
#                     team2[index].append(champ_ver)
#                     team2[index].append(champ_name)
#                     team2[index].append(champ_level)
#
#
#                                 # 소환사 주문
#                     champion_spells = player_name_container.find_elements_by_css_selector('div.spell-book > div')
#                     for spell in champion_spells:
#                         champion_spells2 = spell.find_element_by_css_selector('div')
#                         champion_spell_ver = champion_spells2.get_attribute('data-rg-name')
#                         champion_spell = champion_spells2.get_attribute('data-rg-id')
#                         # print(champion_spell_ver, champion_spell)
#                         team2[index].append(champion_spell_ver)
#                         team2[index].append(champion_spell)
#
#
#                 team_footer = body[1].find_element_by_css_selector('div > footer div.gs-container')
#
#                         # 밴
#                 team_bans = team_footer.find_elements_by_css_selector('div.champion-nameplate')
#                 # print()
#                 # print('bans')
#                 for ban in team_bans:
#                     ban = ban.find_element_by_css_selector('div.champion-icon div')
#                     ban_name = ban.get_attribute('data-rg-id')
#                     # print(ban_name)
#                     team2list.append(ban_name)
#
#                 # print()
#                         # 타워킬
#                 team_towerkill = team_footer.find_element_by_css_selector('div.tower-kills').text.strip()
#                         # 억제기 킬
#                 team_inhibitorkill = team_footer.find_element_by_css_selector('div.inhibitor-kills').text.strip()
#                         # 바론 킬
#                 team_baronkill = team_footer.find_element_by_css_selector('div.baron-kills').text.strip()
#                         # 드래곤 킬
#                 team_dragonkill = team_footer.find_element_by_css_selector('div.dragon-kills').text.strip()
#                         # 전령 킬
#                 team_riftkill = team_footer.find_element_by_css_selector('div.rift-herald-kills').text.strip()
#
#                 # print('타워킬', team_towerkill)
#                 # print('억제기 킬', team_inhibitorkill)
#                 # print('바론 킬', team_baronkill)
#                 # print('드래곤 킬', team_dragonkill)
#                 # print('전령 킬', team_riftkill)
#                 team2list.append(team_towerkill)
#                 team2list.append(team_inhibitorkill)
#                 team2list.append(team_baronkill)
#                 team2list.append(team_dragonkill)
#                 team2list.append(team_riftkill)
#             except:
#                 print('오류')
#                 wb.save(season.strip() + '.xlsx')
#                 driver.refresh()
#                 time.sleep(2)
#                 continue
#             break
#
#         statsbuttons = driver.find_elements_by_css_selector('div.n-data-mode1-data a')
#         statsbuttons[1].click()
#
#         time.sleep(1)
#         pagesource = pagesource.replace('overview', 'stats')
#         while True:
#             try:
#
#                 # driver.implicitly_wait(10)
#                 time.sleep(1)
#                 driver.get(pagesource)
#
#                 time.sleep(1)
#
#                 containers2 = driver.find_element_by_css_selector('div.section-wrapper-content-wrapper div#main div.classic.details div.tab-panel-body')
#                 # head , body , tail 전의 제일 큰 컨테이너
#
#                 tail_stats = containers2.find_element_by_css_selector('tbody#stats-body')
#                 # 통계 tail
#
#                 tail_trs = tail_stats.find_elements_by_css_selector('tr.grid-row')
#
#                 for tr in tail_trs:
#                     tdindex = 0
#                     for td in tr.find_elements_by_css_selector('td > div'):
#                         # print('tdindex')
#                         # print(tdindex)
#                         # print(td.text.strip())
#                         tdtext = td.text.strip()
#                         # tdindex = tr.find_elements_by_css_selector('td div').index(td)
#                         if tdindex == 0:
#                             pass
#                         elif tdindex >= 1 and tdindex <= 5:
#                             team1[tdindex-1].append(tdtext)
#                         elif tdindex >= 6 and tdindex <= 10:
#                             team2[tdindex-6].append(tdtext)
#                         tdindex = tdindex + 1
#
#             except:
#                 print('오류')
#                 wb.save(season.strip() + '.xlsx')
#                 driver.refresh()
#                 time.sleep(2)
#                 continue
#             break
#
#         while True:
#             team11list = []
#             team22list = []
#             try:
#                 team11list = teamlist + [season] + [filename.replace("url_", '').replace(season, '').replace('.txt', '')] + ['blue'] + team1list
#                 # sheet.append(teamlist)
#                 # sheet.append(team1list)
#                 for player in team1:
#                     player = team11list + player
#                     sheet.append(player)
#                 # sheet.append(team2list)
#                 team22list = teamlist + [season] + [filename.replace("url_", '').replace(season, '').replace('.txt', '')] + ['red'] + team2list
#                 for player in team2:
#                     player = team22list + player
#                     sheet.append(player)
#
#                 print(i)
#             except:
#                 print('오류')
#                 wb.save(season.strip() + '.xlsx')
#                 driver.quit()
#                 continue
#             break
#
#         if i // 5 == 0:
#             wb.save(season.strip() + '.xlsx')
#
#     pagesources.close()
#
#
#
#     driver.quit()
#
# wb.save(season.strip() + '.xlsx')
#
# filenames.close()
#