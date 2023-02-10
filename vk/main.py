import requests, time
import database, vkbot
from bs4 import BeautifulSoup


r = requests.Session()

# Проверяем статус заявки
def check_WEBSITE_A(url_ban, nick):
    try:
        # Получаем страницу заявки
        url = r.get(str(url_ban))
        url_bs = BeautifulSoup(url.content, 'html.parser')
        error = url_bs.select('.block.pd-15 li.d-i-b.active')[0].text
    except:
        pass
    else:
        if error != "Ошибка":
            try:
                # Проверяем статус заявки
                status = url_bs.select('.r_block_c.overflow span.label')[0].text
            except:
                pass
            else:
                # Если заявка рассмотрена, то проверяем Разбан или Не разбан
                if str(status) != "Не рассмотрена":
                    try:
                        moder = url_bs.select('.r_block_c.overflow a')[-1].text
                        moder_id = url_bs.select('.r_block_c.overflow a')[-1]['href'].split('=')[-1]
                    except:
                        pass
                    else:
                        # Проверяем есть ли модератор в базе, если нет, то добавляем
                        database.sql.execute("SELECT id_login FROM moders_WEBSITE_A WHERE id_login = '"+str(moder_id)+"'")
                        if database.sql.fetchone() is None:
                            while True:
                                try:
                                    url_moder = r.get('https://WEBSITE_A/profile?id='+str(moder_id))
                                    url_moder_bs = BeautifulSoup(url_moder.content, 'html.parser')
                                    group = url_moder_bs.select('.table.user_profile_info i')[0].text
                                    moder_id_vk = url_moder_bs.select('.table.user_profile_info a[id=vk_user2]')[0]['href'].split('/')[-1]
                                    moder_name = url_moder_bs.select('.block.pd-15 li.d-i-b.active')[0].text
                                except:
                                    pass
                                else:
                                    if str(group) == 'Модератор разбанов':
                                        database.sql.execute("INSERT INTO moders_WEBSITE_A VALUES (?, ?, ?, ?, ?)",(moder_id, moder_id_vk, moder_name, 0, 0))
                                        database.db.commit()
                                    break
                                time.sleep(1)

                        # Добавляем в статистику рассмотренную заявку
                        for value in database.sql.execute("SELECT * FROM moders_WEBSITE_A"):
                            if int(value[0]) == int(moder_id):
                                if str(status) == "Разбанен":
                                    database.sql.execute('UPDATE moders_WEBSITE_A SET razban = "'+str(1+value[3])+'" WHERE id_login = "'+str(moder_id)+'"')
                                    database.db.commit()
                                    status = str(" &#9989;") + str(status)
                                elif str(status) == "Не разбанен":
                                    database.sql.execute('UPDATE moders_WEBSITE_A SET nerazban = "'+str(1+value[4])+'" WHERE id_login = "'+str(moder_id)+'"')
                                    database.db.commit()
                                    status = str(" &#10060;") + str(status)

                        # Отправляем сообщение в беседу
                        vkbot.vk.method("messages.send", {"peer_id": vkbot.peer_id,
                                                    "message": '&#9745;Рассмотрели заявку от игрока "'+str(nick)+'" на WEBSITE_A:\n&#128100;Рассмотрел: '+str(moder)+'\n&#128204;Статус: '+str(status)+'\nСсылка - '+str(url_ban),
                                                    "attachment": "doc-189671096_530350405",
                                                    "random_id":  0})

                        # Удаляем заявки из базы проверки статуса
                        database.sql.execute("DELETE FROM WEBSITE_A_bans WHERE url_ban = '"+str(url_ban)+"'")
                        database.db.commit()

def check_WEBSITE_B(url_ban, nick):
    try:
        url = r.get(str(url_ban))
        url_bs = BeautifulSoup(url.content, 'html.parser')
        error = url_bs.select('.navigation li.active')[0].text
    except:
        pass
    else:
        if error != "Ошибка":
            try:
                status = url_bs.select('.block.ban-application.ban-information span.label')[0].text
            except:
                pass
            else:
                if str(status) != "Не рассмотрена":
                    try:
                        moder = url_bs.select('.block.ban-application.ban-information a')[-1].text
                        moder_id = url_bs.select('.block.ban-application.ban-information a')[-1]['href'].split('=')[-1]
                    except:
                        pass
                    else:
                        database.sql.execute("SELECT id_login FROM moders_WEBSITE_B WHERE id_login = '"+str(moder_id)+"'")
                        if database.sql.fetchone() is None:
                            while True:
                                try:
                                    url_moder = r.get('https://WEBSITE_B/profile?id='+str(moder_id))
                                    url_moder_bs = BeautifulSoup(url_moder.content, 'html.parser')
                                    group = url_moder_bs.select('.table.mb-0 span')[0].text
                                    moder_id_vk = url_moder_bs.select('.table.mb-0 a[id=vk_user]')[0]['href'].split('/')[-1]
                                    moder_name = url_moder_bs.select('.navigation li.active')[0].text
                                except:
                                    pass
                                else:
                                    if str(group) == 'Модератор разбанов':
                                        database.sql.execute("INSERT INTO moders_WEBSITE_B VALUES (?, ?, ?, ?, ?)",(moder_id, moder_id_vk, moder_name, 0, 0))
                                        database.db.commit()
                                    break
                                time.sleep(1)

                        for value in database.sql.execute("SELECT * FROM moders_WEBSITE_B"):
                            if int(value[0]) == int(moder_id):
                                if str(status) == "Разбанен":
                                    database.sql.execute('UPDATE moders_WEBSITE_B SET razban = "'+str(1+value[3])+'" WHERE id_login = "'+str(moder_id)+'"')
                                    database.db.commit()
                                    status = str(" &#9989;") + str(status)
                                elif str(status) == "Не разбанен":
                                    database.sql.execute('UPDATE moders_WEBSITE_B SET nerazban = "'+str(1+value[4])+'" WHERE id_login = "'+str(moder_id)+'"')
                                    database.db.commit()
                                    status = str(" &#10060;") + str(status)

                        vkbot.vk.method("messages.send", {"peer_id": vkbot.peer_id,
                                                    "message": '&#9745;Рассмотрели заявку от игрока "'+str(nick)+'" на WEBSITE_A:\n&#128100;Рассмотрел: '+str(moder)+'\n&#128204;Статус: '+str(status)+'\nСсылка - '+str(url_ban),
                                                    "attachment": "doc-189671096_530351833",
                                                    "random_id":  0})

                        database.sql.execute("DELETE FROM WEBSITE_B_bans WHERE url_ban = '"+str(url_ban)+"'")
                        database.db.commit()

# Добавление заявки в базу, оповещение в беседе
def post_request_WEBSITE_A(url_ban):
    try:
        # Получаем страницу заявки и всю инфу о бане
        url = r.get(str(url_ban))
        url_bs = BeautifulSoup(url.content, 'html.parser')
        url_ban_token = url_bs.select('input[id=token]')[0]['value']
        url_ban_ban = url_bs.select('input[id=search_ban]')[0]['value']
        url_ban_server = str(url_bs.select('.btn-info')[0]).split()[5].split('search_ban_application(')[1].split(')')[0]

        payload  = {
            'phpaction': '1',
            'search_ban': '1',
            'token': url_ban_token,
            'ban': url_ban_ban,
            'server': url_ban_server
            }

        url = r.post('https://WEBSITE_A/ajax/actions.php', data = payload)
        url_bs = BeautifulSoup(url.content, 'html.parser')

        SteamID = url_bs.select('td')[5].text # стим айди
        nick = url_bs.select('td')[7].text # ник забаненного
        server = url_bs.select('td')[19].text.split('-')[0] # сервер
        reason = url_bs.select('td')[11].text # причина
    except:
        pass
    else:
        # Добавляем заявку в базу
        database.sql.execute("INSERT INTO WEBSITE_A_bans VALUES (?,?)",(str(url_ban), str(nick)))
        database.db.commit()
        database.check_profiles()

        # Проверяем SteamID в черном списке
        database.sql.execute("SELECT id FROM steam_ids WHERE id = '"+str(SteamID)+"'")
        # Составление списка айди для оповещения
        # В черном списке - оповещение одминов
        # Обычный - оповещение модеров
        if database.sql.fetchone() is None:
            ids = []
            for value in database.sql.execute("SELECT * FROM users_id"):
                ids.append(value[0])

            # Не помещать в список оповещения, если выключены уведомления командой /off
            id_for_send = []
            for id in range(len(ids)):
                database.sql.execute("SELECT id FROM off_ids WHERE id = '"+str(ids[id])+"'")
                if database.sql.fetchone() is None:
                    id_for_send.append("@id"+str(ids[id])+"(&#8300;)")

            id_for_send = ''.join(id_for_send)
            vkbot.vk.method("messages.send", {"peer_id": vkbot.peer_id, "message": '&#10133;Появилась новая заявка на странице разбана WEBSITE_A: \n&#128100;Ник: '+str(nick)+'\n&#9888;Причина: '+str(reason)+'\n&#128225;Сервер: '+str(server)+'\nСсылка - ' + str(url_ban)+" "+str(id_for_send),"attachment": "doc-189671096_530350405", "random_id":  0})
        else:
            ids = []
            for value in database.sql.execute("SELECT * FROM admins_id"):
                ids.append(value[0])

            # Не помещать в список оповещения, если выключены уведомления командой /off
            id_for_send = []
            for id in range(len(ids)):
                database.sql.execute("SELECT id FROM off_ids WHERE id = '"+str(ids[id])+"'")
                if database.sql.fetchone() is None:
                    id_for_send.append("@id"+str(ids[id])+"(&#8300;)")

            id_for_send = ''.join(id_for_send)
            vkbot.vk.method("messages.send", {"peer_id": vkbot.peer_id, "message": '&#10071;ВНИМАНИЕ: SteamID пользователя находится в ЧС&#10071;\n&#128204;SteamID: '+str(SteamID)+'\n&#10133;Появилась новая заявка на странице разбана WEBSITE_A: \n&#128100;Ник: '+str(nick)+'\n&#9888;Причина: '+str(reason)+'\n&#128225;Сервер: '+str(server)+'\nСсылка - ' + str(url_ban)+" "+str(id_for_send), "attachment": "doc-189671096_530350405", "disable_mentions": 0, "random_id":  0})

def post_request_WEBSITE_B(url_ban):
    try:
        url = r.get(str(url_ban))
        url_bs = BeautifulSoup(url.content, 'html.parser')
        url_ban_token = url_bs.select('input[id=token]')[0]['value']
        url_ban_ban = url_bs.select('input[id=search_ban]')[0]['value']
        url_ban_server = str(url_bs.select('.btn-primary')[3]).split()[3].split('search_ban_application(')[1].split(')')[0]

        payload  = {
            'phpaction': '1',
            'search_ban': '1',
            'token': url_ban_token,
            'ban': url_ban_ban,
            'server': url_ban_server
            }

        url = r.post('https://WEBSITE_B/ajax/actions.php', data = payload)
        url_bs = BeautifulSoup(url.content, 'html.parser')

        SteamID = url_bs.select('td')[5].text # стим айди
        nick = url_bs.select('td')[7].text # ник забаненного
        server = url_bs.select('td')[19].text.split('-')[0] # сервер
        reason = url_bs.select('td')[11].text # причина
    except:
        pass
    else:
        database.sql.execute("INSERT INTO WEBSITE_B_bans VALUES (?,?)",(str(url_ban), str(nick)))
        database.db.commit()
        database.check_profiles()

        database.sql.execute("SELECT id FROM steam_ids WHERE id = '"+str(SteamID)+"'")
        if database.sql.fetchone() is None:
            ids = []
            for value in database.sql.execute("SELECT * FROM users_id"):
                ids.append(value[0])

            id_for_send = []
            for id in range(len(ids)):
                database.sql.execute("SELECT id FROM off_ids WHERE id = '"+str(ids[id])+"'")
                if database.sql.fetchone() is None:
                    id_for_send.append("@id"+str(ids[id])+"(&#8300;)")

            id_for_send = ''.join(id_for_send)
            vkbot.vk.method("messages.send", {"peer_id": vkbot.peer_id, "message": '&#10133;Появилась новая заявка на странице разбана WEBSITE_B: \n&#128100;Ник: '+str(nick)+'\n&#9888;Причина: '+str(reason)+'\n&#128225;Сервер: '+str(server)+'\nСсылка - ' + str(url_ban)+" "+str(id_for_send),"attachment": "doc-189671096_530351833", "random_id":  0})
        else:
            ids = []
            for value in database.sql.execute("SELECT * FROM admins_id"):
                ids.append(value[0])

            id_for_send = []
            for id in range(len(ids)):
                database.sql.execute("SELECT id FROM off_ids WHERE id = '"+str(ids[id])+"'")
                if database.sql.fetchone() is None:
                    id_for_send.append("@id"+str(ids[id])+"(&#8300;)")

            id_for_send = ''.join(id_for_send)
            vkbot.vk.method("messages.send", {"peer_id": vkbot.peer_id, "message": '&#10071;ВНИМАНИЕ: SteamID пользователя находится в ЧС&#10071;\n&#128204;SteamID: '+str(SteamID)+'\n&#10133;Появилась новая заявка на странице разбана WEBSITE_B: \n&#128100;Ник: '+str(nick)+'\n&#9888;Причина: '+str(reason)+'\n&#128225;Сервер: '+str(server)+'\nСсылка - ' + str(url_ban)+" "+str(id_for_send), "attachment": "doc-189671096_530351833", "disable_mentions": 0, "random_id":  0})

# Опрос страницы с заявками на разбан каждые 60 секунд
def main():
    while True:
        time.sleep(10)
        try:
            # Получаем страницу заявок
            url = r.get('https://WEBSITE_A/bans')
            url_bs = BeautifulSoup(url.content, 'html.parser')
            bans_count = url_bs.select('#bans tr')
        except:
            pass
        else:
            for bans in range(len(bans_count)):
                try:
                    # Получаем ссылку на заявку
                    url_ban = 'https://WEBSITE_A'+str(bans_count[bans]).split('td')[1].split('"')[1].split('..')[1]
                    status = str(bans_count[bans]).split('td')[-6].split('>')[2].split('<')[0]
                except:
                    pass
                else:
                    # Проверяем статус заявки
                    if str(status) == "Не рассмотрена":
                        continuation = True
                        # Проверяем есть ли заявка в базе
                        for value in database.sql.execute("SELECT * FROM WEBSITE_A_bans"):
                            if str(value[0]) == str(url_ban):
                                continuation = False

                        # Если заявки нет в базе, то добавляем в базу и делаем оповещение в беседе
                        if continuation:
                            post_request_WEBSITE_A(str(url_ban))

                    # Проверяем все заявки в базе
                    for value in database.sql.execute("SELECT * FROM WEBSITE_A_bans"):
                        time.sleep(1)
                        check_WEBSITE_A(value[0], value[1])
                break


        try:
            url = r.get('https://WEBSITE_B/bans')
            url_bs = BeautifulSoup(url.content, 'html.parser')
            bans_count = url_bs.select('#bans tr')
        except:
            pass
        else:
            for bans in range(len(bans_count)):
                try:
                    url_ban = 'https://WEBSITE_B'+str(bans_count[bans]).split('td')[1].split('"')[1].split('..')[1]
                    status = str(bans_count[bans]).split('td')[-6].split('>')[2].split('<')[0]
                except:
                    pass
                else:
                    if str(status) == "Не рассмотрена":
                        continuation = True
                        for value in database.sql.execute("SELECT * FROM WEBSITE_B_bans"):
                            if str(value[0]) == str(url_ban):
                                continuation = False

                        if continuation:
                            post_request_WEBSITE_B(str(url_ban))

                    for value in database.sql.execute("SELECT * FROM WEBSITE_B_bans"):
                        time.sleep(1)
                        check_WEBSITE_B(value[0], value[1])
                break

if __name__ == '__main__':
    database.sql.execute("DROP TABLE IF EXISTS WEBSITE_A_bans")
    database.db.commit()
    database.sql.execute("""CREATE TABLE IF NOT EXISTS WEBSITE_A_bans(
        url_ban TEXT,
        nickname TEXT
    )""")
    database.db.commit()
    database.sql.execute("DROP TABLE IF EXISTS WEBSITE_B_bans")
    database.db.commit()
    database.sql.execute("""CREATE TABLE IF NOT EXISTS WEBSITE_B_bans(
        url_ban TEXT,
        nickname TEXT
    )""")
    database.db.commit()
    main()
