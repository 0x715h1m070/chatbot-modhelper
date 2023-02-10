import telebot
import re
import database as db
import web_scraping as scraping
from telebot import types

API_TOKEN = 'API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)
chat_id = '-437742961'


@bot.message_handler(commands=['start'])
def start(message, ):
    global chat_id
    telegram_id = message.from_user.id
    if message.chat.id > 0:
        if db.profiles.auth(0, 0, telegram_id):
            auth(message)
        else:
            bot.send_message(message.chat.id, "Введите команду: `/login <id> <password>`\nПример: `/login 1 pass12345`",
                             parse_mode='Markdown')


@bot.message_handler(commands=['login'])
def login(message):
    if message.chat.id > 0:
        telegram_id = message.from_user.id
        try:
            id_profile = message.text.split()[1]
            password = message.text.split()[2]
            if db.profiles.auth(id_profile, password, telegram_id):
                auth(message)
                bot.send_message(message.chat.id, 'Вы вошли в профиль!')
            else:
                bot.send_message(message.chat.id, 'ID или Password неверный!')
        except:
            bot.send_message(message.chat.id, 'ID или Password неверный!')


@bot.message_handler(commands=['add'])
def add_steam_id(message):
    if message.chat.id > 0:
        telegram_id = message.from_user.id
        if db.profiles.auth(0, 0, telegram_id):
            profile = db.profiles.get_profile(telegram_id)
            if profile['privilege']['moderator_website']:
                try:
                    url = message.text.split(' ', 2)[1]
                    if 'https://bans.WEBSITE_A/bans/' in url:
                        status = message.text.split(' ', 2)[-1]
                        scraping.add_steam_id(url, status)
                    else:
                        bot.send_message(message.chat.id, 'Заполните все данные!')
                except:
                    bot.send_message(message.chat.id, 'Заполните все данные!')
                else:
                    bot.send_message(message.chat.id, 'Steam ID добавлен в список!')
            else:
                bot.send_message(message.chat.id, 'У вас недостаточно прав!')
        else:
            bot.send_message(message.chat.id, "Введите команду: `/login <id> <password>`\nПример: `/login 1 pass12345`",
                             parse_mode='Markdown')


@bot.message_handler(commands=['remove'])
def remove_steam_id(message):
    if message.chat.id > 0:
        telegram_id = message.from_user.id
        if db.profiles.auth(0, 0, telegram_id):
            profile = db.profiles.get_profile(telegram_id)
            if profile['privilege']['moderator_website']:
                try:
                    value = message.text.split()[1]
                    steam_id = re.findall(r'(STEAM_\d:\d:\d+)', value)

                    if steam_id:
                        db.steam_ids.remove(steam_id[0])
                        bot.send_message(message.chat.id, '❗ ' + str(steam_id[0]) + ' удалён из списка!')
                    else:
                        bot.send_message(message.chat.id, 'Введите Steam ID!')
                except:
                    bot.send_message(message.chat.id, 'Заполните все данные!')
            else:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, 'У вас недостаточно прав!')
        else:
            bot.send_message(message.chat.id, "Введите команду: `/login <id> <password>`\nПример: `/login 1 pass12345`",
                             parse_mode='Markdown')


@bot.message_handler(commands=['search'])
def search_steam_id(message):
    if message.chat.id > 0:
        telegram_id = message.from_user.id
        if db.profiles.auth(0, 0, telegram_id):
            profile = db.profiles.get_profile(telegram_id)
            if profile['privilege']['moderator_website']:
                try:
                    value = message.text.split()[1]
                    steam_id = re.findall(r'(STEAM_\d:\d:\d+)', value)

                    if steam_id:
                        list_steam_ids = db.steam_ids.search(steam_id[0], False)
                        value = 'стим айди: ' + str(value)
                    else:
                        list_steam_ids = db.steam_ids.search(value, True)
                        value = 'нику: ' + str(value)

                    if list_steam_ids:
                        text = ''
                        for steam_id in list_steam_ids:
                            text += '\n🆔 STEAM ID: ' + str(steam_id[0]) + '\n✏ Ник: ' + str(
                                steam_id[1]) + '\n🏷 Статус: ' + \
                                    steam_id[2] + '\n📆 Дата добавления: ' + str(steam_id[3] + '\n')
                        bot.send_message(message.chat.id, 'Поиск по ' + str(value) + '\n' + str(text))
                    else:
                        bot.send_message(message.chat.id, 'Поиск по ' + str(value) + '\n\nНичего не найдено!')
                except:
                    bot.send_message(message.chat.id, 'Заполните все данные!')
            else:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, 'У вас недостаточно прав!')
        else:
            bot.send_message(message.chat.id, "Введите команду: `/login <id> <password>`\nПример: `/login 1 pass12345`",
                             parse_mode='Markdown')


def auth(message):
    if message.chat.id > 0:
        telegram_id = message.from_user.id
        profile = db.profiles.get_profile(telegram_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # btn_profile = types.KeyboardButton('👤 Профиль')
        # btn_settings = types.KeyboardButton('⚙ Настройки')
        # markup.add(btn_settings)
        if profile['privilege']['moderator_website']:
            btn_moderator_website = types.KeyboardButton('🕶 Инструменты модер. сайта')
            markup.add(btn_moderator_website)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Главное меню", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.chat.id > 0:
        telegram_id = message.from_user.id
        if db.profiles.auth(0, 0, telegram_id):
            if message.text in ['🕶 Инструменты модер. сайта', '📄 Список', '🛎 Команды для модер. сайта', '📤 Экспорт списка']:
                profile = db.profiles.get_profile(telegram_id)
                if profile['privilege']['moderator_website']:
                    if message.text == '🕶 Инструменты модер. сайта':
                        tools_moderator_website(message)
                    elif message.text == '📄 Список':
                        list_steam_ids = db.steam_ids.get_list()
                        if len(list_steam_ids) > 50:
                            pass
                        bot.send_message(message.chat.id, "Список:\n" + '\n'.join(list_steam_ids),
                                         parse_mode='Markdown')
                    elif message.text == '📤 Экспорт списка':
                        with open(db.PATH_STEAM_IDS, encoding='utf8') as f:
                            bot.send_document(message.chat.id,f)

                    elif message.text == '🛎 Команды для модер. сайта':
                        bot.send_message(message.chat.id, '*Команды для модер. сайта:*'
                                                          '\n`/add <ссылка> <статус>`'
                                                          '\n`/remove <steam_id>`'
                                                          '\n`/search <ник/steam_id>`',
                                         parse_mode='Markdown')
                        pass
                else:
                    bot.send_message(message.chat.id, 'У вас недостаточно прав!')

            elif message.text == '🔙 Назад':
                auth(message)
        else:
            bot.send_message(message.chat.id, "Введите команду: `/login <id> <password>`\nПример: `/login 1 pass12345`",
                             parse_mode='Markdown')


def tools_moderator_website(message):
    if message.chat.id > 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_list_steam_id = types.KeyboardButton('📄 Список')
        btn_commands = types.KeyboardButton('🛎 Команды для модер. сайта')
        btn_export = types.KeyboardButton('📤 Экспорт списка')
        btn_back = types.KeyboardButton('🔙 Назад')
        markup.add(btn_list_steam_id, btn_commands, btn_export)
        markup.add(btn_back)
        bot.send_message(message.chat.id, "Инструменты модер. сайта", reply_markup=markup)


def send_mess(text):
    bot.send_message(chat_id, text, parse_mode='Markdown')


def start_scraping():
    scraping.start()


def start_bot():
    bot.polling()


if __name__ == "__main__":
    start_bot()
    # threading.Thread(target=start_scraping).start()
