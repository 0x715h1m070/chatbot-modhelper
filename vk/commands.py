import database, vkbot, re, operator


root = ['0000000',
        '0000000',
        '0000000',
        '0000000',
        '0000000']

while True:
    try:
        for vkbot.event in vkbot.longpoll.listen():
            if vkbot.event.object.peer_id == vkbot.peer_id:
                if vkbot.event.type == vkbot.VkBotEventType.MESSAGE_NEW:
                    first_name = vkbot.vk.method("users.get", {"user_ids": vkbot.event.object.from_id})[0]["first_name"]
                    if "/add_steam_id" in str(vkbot.event.object.text.lower().split()[0]):
                        database.sql.execute("SELECT id FROM admins_id WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if database.sql.fetchone() is None:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071; @id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас недостаточно прав!', "random_id":  0})
                        else:
                            message_steamID = vkbot.event.object.text.split()[1]
                            SteamID = re.findall( r'(STEAM_\d:\d:\d+)', message_steamID)
                            if SteamID:
                                database.sql.execute("SELECT id FROM steam_ids WHERE id = '"+str(SteamID[0])+"'")
                                if database.sql.fetchone() is None:
                                    database.sql.execute("INSERT INTO steam_ids VALUES ('"+str(SteamID[0])+"')")
                                    database.db.commit()
                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#9989;"'+str(message_steamID)+'" добавлен в чёрный список!\n&#128211;Для просмотра «ЧС» напишите «/list».', "random_id":  0})
                                else:
                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;Такой SteamID уже есть в чёрном списке!\n&#128211; Для просмотра «ЧС» напишите «/list».', "random_id":  0})

                    elif "/delete_steam_id" in str(vkbot.event.object.text.lower().split()[0]):
                        database.sql.execute("SELECT id FROM admins_id WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if database.sql.fetchone() is None:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071; @id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас недостаточно прав!', "random_id":  0})
                        else:
                            message_steamID = vkbot.event.object.text.split()[1]
                            SteamID = re.findall( r'(STEAM_\d:\d:\d+)', message_steamID)
                            if SteamID:
                                database.sql.execute("SELECT id FROM steam_ids WHERE id = '"+str(SteamID[0])+"'")
                                if database.sql.fetchone() is None:
                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;Такого SteamID нету в чёрном списке!\n&#128211;Для просмотра «ЧС» напишите «/list».', "random_id":  0})
                                else:
                                    database.sql.execute("DELETE FROM steam_ids WHERE id = '"+str(SteamID[0])+"'")
                                    database.db.commit()
                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10060;"'+str(message_steamID)+'" удалён из чёрного списка!\n&#128211;Для просмотра «ЧС» напишите «/list».', "random_id":  0})

                    elif "/WEBSITE_A_edit_razban" in str(vkbot.event.object.text.lower().split()[0]):
                        database.sql.execute("SELECT id FROM admins_id WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if str(vkbot.event.object.from_id) in root:
                            moder_name = str(vkbot.event.object.text.split('<')[1].split('>')[0])
                            database.sql.execute("SELECT login FROM moders_WEBSITE_A WHERE login = '"+str(moder_name)+"'")
                            if database.sql.fetchone() is None:
                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": "&#10071;Такого логина нету.", "random_id":  0})
                            else:
                                new_value = str(vkbot.event.object.text.lower().split('>')[-1])
                                if str(new_value.split("+")[-1]).lower().isdigit() or str(new_value.split("-")[-1]).lower().isdigit():
                                    for value in database.sql.execute("SELECT * FROM moders_WEBSITE_A"):
                                        if str(value[2]) == str(moder_name):
                                            if "+" in str(new_value):
                                                new_value = int(new_value.split("+")[-1])
                                                database.sql.execute('UPDATE moders_WEBSITE_A SET razban = "'+str(int(new_value)+value[3])+'" WHERE login = "'+str(moder_name)+'"')
                                                database.db.commit()
                                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10133;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') добавил &#9989;'+str(str(new_value).split("+")[-1])+' разб. модеру @'+str(value[1])+'('+str(value[2])+') на WEBSITE_A.',  "random_id":  0})
                                            elif "-" in str(new_value):
                                                new_value = int(new_value.split("-")[-1])
                                                if int(value[3]) > int(new_value):
                                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') забрал &#9989;'+str(str(new_value).split("-")[-1])+' разб. у модера @'+str(value[1])+'('+str(value[2])+') с WEBSITE_A.',  "random_id":  0})
                                                    new_value = int(value[3]) - int(new_value)
                                                else:
                                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') забрал &#9989;'+str(value[3])+' разб. у модера @'+str(value[1])+'('+str(value[2])+') с WEBSITE_A.',  "random_id":  0})
                                                    new_value = 0

                                                database.sql.execute('UPDATE moders_WEBSITE_A SET razban = "'+str(new_value)+'" WHERE login = "'+str(moder_name)+'"')
                                                database.db.commit()
                                            else:
                                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), вы не указали действие(+/-)!',  "random_id":  0})
                                else:
                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), вы не указали количество!',  "random_id":  0})
                        else:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас недостаточно прав!', "random_id":  0})

                    elif "/WEBSITE_A_edit_nerazban" in str(vkbot.event.object.text.lower().split()[0]):
                        database.sql.execute("SELECT id FROM admins_id WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if str(vkbot.event.object.from_id) in root:
                            moder_name = str(vkbot.event.object.text.split('<')[1].split('>')[0])
                            database.sql.execute("SELECT login FROM moders_WEBSITE_A WHERE login = '"+str(moder_name)+"'")
                            if database.sql.fetchone() is None:
                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": "&#10071;Такого логина нету.", "random_id":  0})
                            else:
                                new_value = str(vkbot.event.object.text.lower().split('>')[-1])
                                if str(new_value.split("+")[-1]).lower().isdigit() or str(new_value.split("-")[-1]).lower().isdigit():
                                    for value in database.sql.execute("SELECT * FROM moders_WEBSITE_A"):
                                        if str(value[2]) == str(moder_name):
                                            if "+" in str(new_value):
                                                new_value = int(new_value.split("+")[-1])
                                                database.sql.execute('UPDATE moders_WEBSITE_A SET nerazban = "'+str(int(new_value)+value[4])+'" WHERE login = "'+str(moder_name)+'"')
                                                database.db.commit()
                                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10133;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') добавил &#10060;'+str(str(new_value).split("+")[-1])+' неразб. модеру @'+str(value[1])+'('+str(value[2])+') на WEBSITE_A.',  "random_id":  0})
                                            elif "-" in str(new_value):
                                                new_value = int(new_value.split("-")[-1])
                                                if int(value[4]) >= int(new_value):
                                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') забрал &#10060;'+str(str(new_value).split("-")[-1])+' неразб. у модера @'+str(value[1])+'('+str(value[2])+') с WEBSITE_A.',  "random_id":  0})
                                                    new_value = int(value[4]) - int(new_value)
                                                else:
                                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') забрал &#10060;'+str(value[4])+' неразб. у модера @'+str(value[1])+'('+str(value[2])+') с WEBSITE_A.',  "random_id":  0})
                                                    new_value = 0

                                                database.sql.execute('UPDATE moders_WEBSITE_A SET nerazban = "'+str(new_value)+'" WHERE login = "'+str(moder_name)+'"')
                                                database.db.commit()
                                            else:
                                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), вы не указали действие(+/-)!',  "random_id":  0})
                                else:
                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), вы не указали количество!',  "random_id":  0})
                        else:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас недостаточно прав!', "random_id":  0})

                    elif "/WEBSITE_B_edit_razban" in str(vkbot.event.object.text.lower().split()[0]):
                        database.sql.execute("SELECT id FROM admins_id WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if str(vkbot.event.object.from_id) in root:
                            moder_name = str(vkbot.event.object.text.split('<')[1].split('>')[0])
                            database.sql.execute("SELECT login FROM moders_WEBSITE_B WHERE login = '"+str(moder_name)+"'")
                            if database.sql.fetchone() is None:
                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": "&#10071;Такого логина нету.", "random_id":  0})
                            else:
                                new_value = str(vkbot.event.object.text.lower().split('>')[-1])
                                if str(new_value.split("+")[-1]).lower().isdigit() or str(new_value.split("-")[-1]).lower().isdigit():
                                    for value in database.sql.execute("SELECT * FROM moders_WEBSITE_B"):
                                        if str(value[2]) == str(moder_name):
                                            if "+" in str(new_value):
                                                new_value = int(new_value.split("+")[-1])
                                                database.sql.execute('UPDATE moders_WEBSITE_B SET razban = "'+str(int(new_value)+value[3])+'" WHERE login = "'+str(moder_name)+'"')
                                                database.db.commit()
                                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10133;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') добавил &#9989;'+str(str(new_value).split("+")[-1])+' разб. модеру @'+str(value[1])+'('+str(value[2])+') на WEBSITE_B.',  "random_id":  0})
                                            elif "-" in str(new_value):
                                                new_value = int(new_value.split("-")[-1])
                                                if int(value[3]) > int(new_value):
                                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') забрал &#9989;'+str(str(new_value).split("-")[-1])+' разб. у модера @'+str(value[1])+'('+str(value[2])+') с WEBSITE_B.',  "random_id":  0})
                                                    new_value = int(value[3]) - int(new_value)
                                                else:
                                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') забрал &#9989;'+str(value[3])+' разб. у модера @'+str(value[1])+'('+str(value[2])+') с WEBSITE_B.',  "random_id":  0})
                                                    new_value = 0

                                                database.sql.execute('UPDATE moders_WEBSITE_B SET razban = "'+str(new_value)+'" WHERE login = "'+str(moder_name)+'"')
                                                database.db.commit()
                                            else:
                                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), вы не указали действие(+/-)!',  "random_id":  0})
                                else:
                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), вы не указали количество!',  "random_id":  0})
                        else:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас недостаточно прав!', "random_id":  0})

                    elif "/WEBSITE_B_edit_nerazban" in str(vkbot.event.object.text.lower().split()[0]):
                        database.sql.execute("SELECT id FROM admins_id WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if str(vkbot.event.object.from_id) in root:
                            moder_name = str(vkbot.event.object.text.split('<')[1].split('>')[0])
                            database.sql.execute("SELECT login FROM moders_WEBSITE_B WHERE login = '"+str(moder_name)+"'")
                            if database.sql.fetchone() is None:
                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": "&#10071;Такого логина нету.", "random_id":  0})
                            else:
                                new_value = str(vkbot.event.object.text.lower().split('>')[-1])
                                if str(new_value.split("+")[-1]).lower().isdigit() or str(new_value.split("-")[-1]).lower().isdigit():
                                    for value in database.sql.execute("SELECT * FROM moders_WEBSITE_B"):
                                        if str(value[2]) == str(moder_name):
                                            if "+" in str(new_value):
                                                new_value = int(new_value.split("+")[-1])
                                                database.sql.execute('UPDATE moders_WEBSITE_B SET nerazban = "'+str(int(new_value)+value[4])+'" WHERE login = "'+str(moder_name)+'"')
                                                database.db.commit()
                                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10133;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') добавил &#10060;'+str(str(new_value).split("+")[-1])+' неразб. модеру @'+str(value[1])+'('+str(value[2])+') на WEBSITE_B.',  "random_id":  0})
                                            elif "-" in str(new_value):
                                                new_value = int(new_value.split("-")[-1])
                                                if int(value[4]) >= int(new_value):
                                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') забрал &#10060;'+str(str(new_value).split("-")[-1])+' неразб. у модера @'+str(value[1])+'('+str(value[2])+') с WEBSITE_B.',  "random_id":  0})
                                                    new_value = int(value[4]) - int(new_value)
                                                else:
                                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') забрал &#10060;'+str(value[4])+' неразб. у модера @'+str(value[1])+'('+str(value[2])+') с WEBSITE_B.',  "random_id":  0})
                                                    new_value = 0

                                                database.sql.execute('UPDATE moders_WEBSITE_B SET nerazban = "'+str(new_value)+'" WHERE login = "'+str(moder_name)+'"')
                                                database.db.commit()
                                            else:
                                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), вы не указали действие(+/-)!',  "random_id":  0})
                                else:
                                    vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), вы не указали количество!',  "random_id":  0})
                        else:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас недостаточно прав!', "random_id":  0})

                    elif "/WEBSITE_A_remove_moder" in str(vkbot.event.object.text.lower().split()[0]):
                        database.sql.execute("SELECT id FROM admins_id WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if str(vkbot.event.object.from_id) in root:
                            moder_name = str(vkbot.event.object.text.split('/WEBSITE_A_remove_moder')[1].split('<')[1].split('>')[0])
                            database.sql.execute("SELECT login FROM moders_WEBSITE_A WHERE login = '"+str(moder_name)+"'")
                            if database.sql.fetchone() is None:
                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": "&#10071;Такого логина нету.", "random_id":  0})
                            else:
                                for value in database.sql.execute("SELECT * FROM moders_WEBSITE_A"):
                                    if str(value[2]) == str(moder_name):
                                        vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') удалил модера @'+str(value[1])+'('+str(value[2])+') из топа на WEBSITE_A.', "random_id":  0})
                                        database.sql.execute("DELETE FROM moders_WEBSITE_A WHERE login = '"+str(moder_name)+"'")
                                        database.db.commit()
                        else:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас недостаточно прав!', "random_id":  0})

                    elif "/WEBSITE_B_remove_moder" in str(vkbot.event.object.text.lower().split()[0]):
                        database.sql.execute("SELECT id FROM admins_id WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if str(vkbot.event.object.from_id) in root:
                            moder_name = str(vkbot.event.object.text.split('/WEBSITE_A_remove_moder')[1].split('<')[1].split('>')[0])
                            database.sql.execute("SELECT login FROM moders_WEBSITE_B WHERE login = '"+str(moder_name)+"'")
                            if database.sql.fetchone() is None:
                                vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": "&#10071;Такого логина нету.", "random_id":  0})
                            else:
                                for value in database.sql.execute("SELECT * FROM moders_WEBSITE_B"):
                                    if str(value[2]) == str(moder_name):
                                        vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10134;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') удалил модера @'+str(value[1])+'('+str(value[2])+') из топа на WEBSITE_B.', "random_id":  0})
                                        database.sql.execute("DELETE FROM moders_WEBSITE_B WHERE login = '"+str(moder_name)+"'")
                                        database.db.commit()
                        else:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас недостаточно прав!', "random_id":  0})

                    elif vkbot.event.object.text.lower() == "/list":
                        vk_message_base_steam_id = []
                        i = 0
                        for value in database.sql.execute("SELECT * FROM steam_ids"):
                            i+=1
                            vk_message_base_steam_id.append(str(i)+". "+str(value[0]))
                        vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": "&#128211;Чёрный список SteamID:\n"+str('\n'.join(vk_message_base_steam_id)), "random_id":  0})

                    elif vkbot.event.object.text.lower() == "/help":
                        vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#128221;Список команд: https://vk.cc/axvNX2', "random_id":  0})

                    elif vkbot.event.object.text.lower() == "/bot_stats":
                        database.sql.execute("SELECT * FROM moders_WEBSITE_A")
                        if database.sql.fetchone() is None:
                            top_WEBSITE_A = ['Список пуст']
                        else:
                            mas_moders_WEBSITE_A = []
                            for value in database.sql.execute("SELECT * FROM moders_WEBSITE_A"):
                                mas_moders_WEBSITE_A.append([[str(value[1]), int(value[0])],
                                    [int(value[3]) ,int(value[4]), str(value[2])]])

                            a = sorted(mas_moders_WEBSITE_A, key=operator.itemgetter([1][0]), reverse = True)
                            top_WEBSITE_A = []
                            for i in range(len(a)):
                                top_WEBSITE_A.append(str(i+1)+". @"+str(a[i][0][0])+"("+str(a[i][1][2])+") - [&#9989;"+str(a[i][1][0])+" | &#10060;"+str(a[i][1][1])+"]")

                        database.sql.execute("SELECT * FROM moders_WEBSITE_B")
                        if database.sql.fetchone() is None:
                            top_WEBSITE_B = ['Список пуст']
                        else:
                            mas_moders_WEBSITE_B = []
                            for value in database.sql.execute("SELECT * FROM moders_WEBSITE_B"):
                                mas_moders_WEBSITE_B.append([[str(value[1]), int(value[0])],
                                    [int(value[3]) ,int(value[4]), str(value[2])]])

                            a = sorted(mas_moders_WEBSITE_B, key=operator.itemgetter([1][0]), reverse = True)
                            top_WEBSITE_B = []
                            for i in range(len(a)):
                                top_WEBSITE_B.append(str(i+1)+". @"+str(a[i][0][0])+"("+str(a[i][1][2])+") - [&#9989;"+str(a[i][1][0])+" | &#10060;"+str(a[i][1][1])+"]")

                        vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#127942;Топ по рассмотрению заявок на WEBSITE_A:\n'+str('\n'.join(top_WEBSITE_A))+'\n\n&#127942;Топ по рассмотрению заявок на WEBSITE_B:\n'+str('\n'.join(top_WEBSITE_B)), "disable_mentions": 1, "random_id":  0})

                    elif vkbot.event.object.text.lower() == "/on":
                        database.sql.execute("SELECT id FROM off_ids WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if database.sql.fetchone() is None:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id,
                            "message": '&#128276;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас уже включены уведомления!', "random_id":  0})
                        else:
                            database.sql.execute("DELETE FROM off_ids WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                            database.db.commit()
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id,
                            "message": '&#128276;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), уведомления включены!', "random_id":  0})

                    elif vkbot.event.object.text.lower() == "/off":
                        database.sql.execute("SELECT id FROM off_ids WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if database.sql.fetchone() is None:
                            database.sql.execute("INSERT INTO off_ids VALUES ('"+str(vkbot.event.object.from_id)+"')")
                            database.db.commit()
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id,
                            "message": '&#128277;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), уведомления выключены!', "random_id":  0})
                        else:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id,
                            "message": '&#128277;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас уже выключены уведомления!', "random_id":  0})

                    elif vkbot.event.object.text.lower() == "/clear_top":
                        database.sql.execute("SELECT id FROM admins_id WHERE id = '"+str(vkbot.event.object.from_id)+"'")
                        if not database.sql.fetchone() is None and str(vkbot.event.object.from_id) in root:
                            database.clear_top()
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+') полностью очистил топ по рассмотрению заявок!', "random_id":  0})
                        else:
                            vkbot.vk.method("messages.send", {"peer_id": vkbot.event.object.peer_id, "message": '&#10071;@id'+str(vkbot.event.object.from_id)+'('+str(first_name)+'), у вас недостаточно прав!', "random_id":  0})
    except:
        pass
