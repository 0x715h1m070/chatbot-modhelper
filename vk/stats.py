import database, time, requests

database.clear_top()

def scan():
    number = 28019
    numberez = 1483

    num_error = 0
    while int(number) <= 100000000:
        time.sleep(0.400)
        print('=')
        try:
            url = 'https://WEBSITE_A/bans/ban?id=' + str(number)
            r = requests.get(url).text
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r,'lxml')
            error = soup.find('div', class_='block pd-15').find('li', class_='d-i-b active').text.strip()
        except:
            pass
        else:
            if error != "Ошибка" and num_error < 15:
                print('==')
                try:
                    ban = soup.find('div', class_='r_block_c overflow').find('span', class_='label').text.strip()
                    moder_id = soup.find('div', class_='r_block_c overflow').find_all('a')[-1].get('href').split('=')[1]
                except:
                    pass
                else:
                    print('===')
                    try:
                        url_akk = 'https://WEBSITE_A/profile?id=' + str(moder_id)
                        r = requests.get(url_akk).text
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(r,'lxml')
                        error_akk = soup.find('div', class_='block pd-15').find('li', class_='d-i-b active').text.strip()
                    except:
                        pass
                    else:
                        if error_akk != "Ошибка":
                            print('====')
                            if ban == "Разбанен":
                                num_error = 0
                            elif ban == "Не разбанен":
                                num_error = 0


                            ok = True
                            for value in database.sql.execute("SELECT * FROM moders_WEBSITE_A"):
                                if int(value[0]) == int(moder_id):
                                    ok = False
                                    break

                            if ok:
                                try:
                                    url = 'https://WEBSITE_A/profile?id=' + str(moder_id)
                                    r = requests.get(url).text
                                    from bs4 import BeautifulSoup
                                    soup = BeautifulSoup(r,'lxml')
                                    moder_name = soup.find_all('div', class_='block-title')[2].text.strip()
                                    group = soup.find('div', class_='block-content overflow').find('i').text.strip()
                                except:
                                    pass
                                else:
                                    if group == 'Модератор разбанов':
                                        while True:
                                            number_scan = 5
                                            while True:
                                                vk_id = soup.find('div', class_='block-content overflow').find_all('tr')[-number_scan]
                                                if number_scan == 10:
                                                    break
                                                elif "://vk.com/id" in str(vk_id):
                                                    vk_id = vk_id.find('a').get('href').split('/')[3]
                                                    moder_id_vk = vk_id
                                                    break
                                                number_scan += 1
                                            database.sql.execute("INSERT INTO moders_WEBSITE_A VALUES (?, ?, ?, ?, ?)",(moder_id, moder_id_vk, moder_name, 0, 0))
                                            database.db.commit()
                                            break

                                        # print(str(moder_name)+' | Добавлен в БАЗУ!')

                            for value in database.sql.execute("SELECT * FROM moders_WEBSITE_A"):
                                if int(value[0]) == int(moder_id):
                                    if ban == "Разбанен":
                                        database.sql.execute('UPDATE moders_WEBSITE_A SET razban = "'+str(1+value[3])+'" WHERE id_login = "'+str(moder_id)+'"')
                                        database.db.commit()
                                    elif ban == "Не разбанен":
                                        database.sql.execute('UPDATE moders_WEBSITE_A SET nerazban = "'+str(1+value[4])+'" WHERE id_login = "'+str(moder_id)+'"')
                                        database.db.commit()
                                    else:
                                        pass

            elif num_error >= 15:
                number = 100000000000
            else:
                num_error +=1
                # print(url +" [САЙТ С ОШИБКОЙ] [" + str(num_error) + "/5]")
            number = int(number)  + 1

    num_error = 0
    while int(numberez) <= 100000000:
        time.sleep(0.400)
        print('=')
        try:
            urlez = 'https://WEBSITE_B/bans/ban?id=' + str(numberez)
            r = requests.get(urlez).text
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r,'lxml')
            errorez = soup.find('div', class_='navigation').find('li', class_='active').text.strip()
        except:
            pass
        else:
            if errorez != "Ошибка" and num_error < 15:
                print('==')
                try:
                    ban = soup.find('div', class_='block ban-application ban-information').find('span', class_='label').text.strip()
                    moder_id = soup.find('div', class_='block ban-application ban-information').find_all('a')[-1].get('href').split('=')[1]
                except:
                    pass
                else:
                    print('===')
                    try:
                        url_akk = 'https://WEBSITE_B/profile?id=' + str(moder_id)
                        r = requests.get(url_akk).text
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(r,'lxml')
                        errorez_akk = soup.find('div', class_='navigation').find('li', class_='active').text.strip()
                    except:
                        pass
                    else:
                        if errorez_akk != "Ошибка":
                            print('====')
                            if ban == "Разбанен":
                                num_error = 0
                                # print(urlez + " Разбанен ["+moder_id_ez+"]")
                            elif ban == "Не разбанен":
                                # print(urlez + " Не разбанен ["+moder_id_ez+"]")
                                num_error = 0

                            ok = True
                            for value in database.sql.execute("SELECT * FROM moders_WEBSITE_B"):
                                if int(value[0]) == int(moder_id):
                                    ok = False
                                    break

                            if ok:
                                try:
                                    urlez = 'https://WEBSITE_B/profile?id=' + str(moder_id)
                                    r = requests.get(urlez).text
                                    from bs4 import BeautifulSoup
                                    soup = BeautifulSoup(r,'lxml')
                                    moder_name = soup.find('div', class_='navigation').find('li', class_='active').text.strip()
                                    group = soup.find('table', class_='table mb-0').find_all('td')[4].text.strip()
                                except:
                                    pass
                                else:
                                    if group == 'Модератор разбанов':
                                        while True:
                                            number_scan = 5
                                            while True:
                                                vk_id = soup.find('div', class_='col-lg-8').find_all('tr')[-number_scan]
                                                if number_scan == 10:
                                                    break
                                                elif "://vk.com/id" in str(vk_id):
                                                    vk_id =  vk_id.find('a').get('href').split('/')[3]
                                                    moder_id_vk = vk_id
                                                    break
                                                number_scan += 1
                                            database.sql.execute("INSERT INTO moders_WEBSITE_B VALUES (?, ?, ?, ?, ?)",(moder_id, moder_id_vk, moder_name, 0, 0))
                                            database.db.commit()
                                            break

                                        # print(str(moder_name)+' | Добавлен в БАЗУ!')

                            for value in database.sql.execute("SELECT * FROM moders_WEBSITE_B"):
                                if int(value[0]) == int(moder_id):
                                    if ban == "Разбанен":
                                        database.sql.execute('UPDATE moders_WEBSITE_B SET razban =  "'+str(1+value[3])+'" WHERE id_login = "'+str(moder_id)+'"')
                                        database.db.commit()
                                    elif ban == "Не разбанен":
                                        database.sql.execute('UPDATE moders_WEBSITE_B SET nerazban =  "'+str(1+value[4])+'" WHERE id_login = "'+str(moder_id)+'"')
                                        database.db.commit()
                                    else:
                                        pass


            elif num_error >= 15:
                numberez = 100000000000
            else:
                num_error +=1
                # print(urlez +" [САЙТ С ОШИБКОЙ] [" + str(num_error) + "/5]")
            numberez = int(numberez) + 1
            # print(moders_ez)


scan()
