import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import time
import database as db
import main

session = requests.session()
STATUS_CLASS = '.text-warning'
# .text-warning | .text-success
checking_url = []
checking_url_WEBSITE_B = []


def add_steam_id(url, status):
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for _ in range(5):
        try:
            steam_id = soup.select_one('#yw0 > tr:nth-child(1) > td').text
            nickname = soup.select_one('#yw0 > tr:nth-child(2) > td').text
            moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
            date = str(moscow_time.day) + '.' + str(moscow_time.month) + '.' + str(moscow_time.year)
            db.steam_ids.add(steam_id, nickname, date, status)
        except:
            time.sleep(3)
        else:
            break


def check_web():
    page = session.get('https://WEBSITE_A/bans')
    soup = BeautifulSoup(page.content, 'html.parser')
    for _ in range(5):
        try:
            status = soup.select_one(STATUS_CLASS)

            if status is None:
                pass
            else:
                trs = soup.select('tr')
                for tr in trs:
                    if not tr.select_one(STATUS_CLASS) is None:
                        url = 'https://WEBSITE_A/bans/ban?id=' + \
                              tr.select_one('a').get('href').split('../bans/ban?id=')[-1]
                        check(url)

            for url in checking_url:
                time.sleep(1)
                check(url)
        except:
            time.sleep(3)
        else:
            break

    page = session.get('https://WEBSITE_B/bans')
    soup = BeautifulSoup(page.content, 'html.parser')
    for _ in range(5):
        try:
            status = soup.select_one(STATUS_CLASS)

            if status is None:
                pass
            else:
                trs = soup.select('tr')
                for tr in trs:
                    if not tr.select_one(STATUS_CLASS) is None:
                        url = 'https://WEBSITE_B/bans/ban?id=' + \
                              tr.select_one('a').get('href').split('../bans/ban?id=')[-1]
                        check_WEBSITE_B(url)

            for url in checking_url_WEBSITE_B:
                time.sleep(1)
                check_WEBSITE_B(url)
        except:
            time.sleep(3)
        else:
            break


def check_WEBSITE_B(url):
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for _ in range(5):
        try:
            status = soup.select_one('#status').text
            if status == 'Не рассмотрена':
                if url not in checking_url_WEBSITE_B:

                    token = soup.select_one('#token').get('value')
                    num_ban = soup.select_one('#search_ban').get('value')
                    num_server = \
                        soup.select_one('div.block:nth-child(2) > button:nth-child(3)').get('onclick').split(
                            'search_ban_application(')[-1].split(')')[0]

                    data = {
                        "phpaction": 1,
                        "search_ban": 1,
                        "token": token,
                        "ban": num_ban,
                        "server": num_server
                    }

                    page = session.post('https://WEBSITE_B/ajax/actions.php', data=data)
                    soup = BeautifulSoup(page.content, 'html.parser')

                    steam_id = soup.select_one('.table > tr:nth-child(3) > td:nth-child(2)').text
                    nickname = soup.select_one('.table > tr:nth-child(4) > td:nth-child(2)').text
                    reason = soup.select_one('.table > tr:nth-child(6) > tr:nth-child(1) > td:nth-child(2)').text

                    if db.steam_ids.search(steam_id, False):
                        '''vk.send_message( '&#10071;ВНИМАНИЕ: SteamID пользователя находится в 
                        ЧС&#10071;\n&#128204;SteamID: ' + str( steam_id) + '\n&#10133;Появилась новая заявка на 
                        странице разбана WEBSITE_B: \n&#128100;Ник: ' + str( nickname) + '\n&#9888;Причина: ' + 
                        str(reason) + '\n&#128225;' + str( server) + '\nСсылка - ' + str(url) + " " + str(''.join(
                        db.return_participants())), 0, 'doc-189671096_530350405') '''
                        main.send_mess(
                            '❗*ВНИМАНИЕ: SteamID пользователя находится в ЧС*❗\nSteamID: `' + str(steam_id) + '`\n\n' +
                            'Появилась новая заявка на сайте *WEBSITE_B*' +
                            '\n👤 Ник: `' + str(nickname) +
                            '`\n🏷 Причина: `' + str(reason) +
                            '`\n📎 Ссылка - ' + str(url))

                    else:
                        '''vk.send_message(
                            '&#10133;Появилась новая заявка на странице разбана WEBSITE_B: \n&#128100;Ник: ' + str(
                                nickname) + '\n&#9888; Причина: ' + str(reason) + '\n&#128225;' + str(
                                server) + '\nСсылка - ' + str(url) + " " + str(''.join(db.return_participants())), 0,
                            'doc-189671096_530350405')'''
                        main.send_mess(
                            '*Появилась новая заявка на сайте WEBSITE_B*' +
                            '\n👤 Ник: `' + str(nickname) +
                            '`\n🏷 Причина: `' + str(reason) +
                            '`\n📎 Ссылка - ' + str(url))

                    checking_url_WEBSITE_B.append(url)

            else:
                page = session.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                nickname = soup.select_one('.active').text.split('Заявка от ')[-1]
                print(nickname)
                url_profile = 'https://WEBSITE_B/profile?id=' + \
                              soup.select('div.ban-application > p a')[-1].get('href').split('../profile?id=')[-1]
                print(url_profile)
                page = session.get(url_profile)
                soup = BeautifulSoup(page.content, 'html.parser')

                group = soup.select_one('table.table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > '
                                        'td:nth-child(2) > span:nth-child(1)').text

                nickname_moderator = soup.select_one('.active').text
                if group == 'Модератор разбанов':
                    id_acc = soup.select_one('table.table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > '
                                             'td:nth-child(2)').text
                    vk_id = soup.select_one('a#vk_user').get('href').split('http://vk.com/')[-1]

                    if not db.moderators.search_moderator('WEBSITE_B', id_acc):
                        db.moderators.add_moderator('WEBSITE_B', id_acc, nickname_moderator, vk_id)
                    db.moderators.edit_checked_request_moderator('WEBSITE_B', id_acc, status)

                if str(status) == "Разбанен":
                    status = "✅" + str(status)
                elif str(status) == "Не разбанен":
                    status = "❌" + str(status)

                    '''vk.send_message('&#9745;Рассмотрели заявку от игрока "' + str(
                        nickname) + '" на WEBSITE_A:\n&#128100; Рассмотрел: ' + str(
                        nickname_moderator) + '\n&#128204; Статус: ' + str(status) + '\nСсылка - ' + str(url), 0,
                                    'doc-189671096_530350405')'''
                main.send_mess(
                    '*Рассмотрели заявку от игрока* `' + str(nickname) + '` *на WEBSITE_B*\n👤 Рассмотрел: `' +
                    str(nickname_moderator) + '`\n📌 Статус: `' + str(status) +
                    '`\n📎 Ссылка - ' + str(url))

                checking_url_WEBSITE_B.remove(url)
        except Exception as ex:
            print(ex)
            time.sleep(3)
        else:
            break


def check(url):
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for _ in range(5):
        try:
            status = soup.select_one('#status').text
            if status == 'Не рассмотрена':
                if url not in checking_url:
                    # server = soup.select_one('.overflow > p:nth-child(4)').text

                    token = soup.select_one('#token').get('value')
                    num_ban = soup.select_one('#search_ban').get('value')
                    num_server = \
                        soup.select_one('.btn-info').get('onclick').split('search_ban_application(')[-1].split(')')[0]

                    data = {
                        "phpaction": 1,
                        "search_ban": 1,
                        "token": token,
                        "ban": num_ban,
                        "server": num_server
                    }

                    page = session.post('https://WEBSITE_A/ajax/actions.php', data=data)
                    soup = BeautifulSoup(page.content, 'html.parser')

                    steam_id = soup.select_one('.table > tr:nth-child(3) > td:nth-child(2)').text
                    nickname = soup.select_one('.table > tr:nth-child(4) > td:nth-child(2)').text
                    reason = soup.select_one('.table > tr:nth-child(6) > tr:nth-child(1) > td:nth-child(2)').text

                    if db.steam_ids.search(steam_id, False):
                        '''vk.send_message( '&#10071;ВНИМАНИЕ: SteamID пользователя находится в 
                        ЧС&#10071;\n&#128204;SteamID: ' + str( steam_id) + '\n&#10133;Появилась новая заявка на 
                        странице разбана WEBSITE_A: \n&#128100;Ник: ' + str( nickname) + '\n&#9888;Причина: ' + 
                        str(reason) + '\n&#128225;' + str( server) + '\nСсылка - ' + str(url) + " " + str(''.join(
                        db.return_participants())), 0, 'doc-189671096_530350405') '''
                        main.send_mess(
                            '❗*ВНИМАНИЕ: SteamID пользователя находится в ЧС*❗\nSteamID: `' + str(steam_id) + '`\n\n' +
                            'Появилась новая заявка на сайте *WEBSITE_A*' +
                            '\n👤 Ник: `' + str(nickname) +
                            '`\n🏷 Причина: `' + str(reason) +
                            '`\n📎 Ссылка - ' + str(url))

                    else:
                        '''vk.send_message(
                            '&#10133;Появилась новая заявка на странице разбана WEBSITE_A: \n&#128100;Ник: ' + str(
                                nickname) + '\n&#9888;Причина: ' + str(reason) + '\n&#128225;' + str(
                                server) + '\nСсылка - ' + str(url) + " " + str(''.join(db.return_participants())), 0,
                            'doc-189671096_530350405')'''
                        main.send_mess(
                            '*Появилась новая заявка на сайте WEBSITE_A*' +
                            '\n👤 Ник: `' + str(nickname) +
                            '`\n🏷 Причина: `' + str(reason) +
                            '`\n📎 Ссылка - ' + str(url))

                    checking_url.append(url)

            else:
                page = session.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                nickname = soup.select_one('li.d-i-b:nth-child(3)').text.split('Заявка от ')[-1]
                url_profile = 'https://WEBSITE_A/profile?id=' + \
                              soup.select('.overflow > p > a')[-1].get('href').split('../profile?id=')[-1]

                page = session.get(url_profile)
                soup = BeautifulSoup(page.content, 'html.parser')

                group = soup.select_one('table.table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > '
                                        'td:nth-child(2) > i:nth-child(1)').text

                nickname_moderator = soup.select_one('li.d-i-b:nth-child(3)').text
                if group == 'Модератор разбанов':
                    id_acc = soup.select_one('table.table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > '
                                             'td:nth-child(2)').text
                    vk_id = soup.select_one('#vk_user2').get('href').split('http://vk.com/')[-1]

                    if not db.moderators.search_moderator('WEBSITE_A', id_acc):
                        db.moderators.add_moderator('WEBSITE_A', id_acc, nickname_moderator, vk_id)
                    db.moderators.edit_checked_request_moderator('WEBSITE_A', id_acc, status)

                if str(status) == "Разбанен":
                    status = "✅" + str(status)
                elif str(status) == "Не разбанен":
                    status = "❌" + str(status)

                    '''vk.send_message('&#9745;Рассмотрели заявку от игрока "' + str(
                        nickname) + '" на WEBSITE_A:\n&#128100;Рассмотрел: ' + str(
                        nickname_moderator) + '\n&#128204;Статус: ' + str(status) + '\nСсылка - ' + str(url), 0,
                                    'doc-189671096_530350405')'''
                main.send_mess(
                    '*Рассмотрели заявку от игрока* `' + str(nickname) + '` *на WEBSITE_A*\n👤 Рассмотрел: `' +
                    str(nickname_moderator) + '`\n📌 Статус: `' + str(status) +
                    '`\n📎 Ссылка - ' + str(url))

                checking_url.remove(url)
        except Exception as ex:
            print(ex)
            time.sleep(3)
        else:
            break


def start():
    main.send_mess('start')
    while True:
        try:
            check_web()
        except:
            pass
        time.sleep(3)


if __name__ == '__main__':
    start()
