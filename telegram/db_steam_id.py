import json
import get_script_dir as gsd


PATH_DATABASE = gsd.get_script_dir() + '/database'
PATH_STEAM_IDS = PATH_DATABASE + '/steam_ids.json'


def get_list():
    list_steam_ids = []
    with open(PATH_STEAM_IDS, encoding='utf8') as f:
        dtjson = json.load(f)

    i = 0
    for steam_id in dtjson:
        i += 1
        list_steam_ids.append('*' + str(i) + '.* `' + str(steam_id['steam_id']) + '`')

    return list_steam_ids


def add(steam_id, nickname, date, status):
    data = ({
                "steam_id": steam_id,
                "nickname": nickname,
                "status": status,
                "date": date
            },)

    with open(PATH_STEAM_IDS, encoding='utf8') as f:
        dtjson = json.load(f)

    dtjson += list(data)

    with open(PATH_STEAM_IDS, 'w', encoding='utf8') as f:
        json.dump(dtjson, f, ensure_ascii=False, indent=4, separators=(',', ': '))


def search(value, nick):
    with open(PATH_STEAM_IDS, encoding='utf8') as f:
        dtjson = json.load(f)

    list_steam_ids = []
    for steam_id in dtjson:
        if nick:
            if value in steam_id['nickname']:
                list_steam_ids.append(
                    [steam_id['steam_id'], steam_id['nickname'], steam_id['status'], steam_id['date']])
        else:
            if value in steam_id['steam_id']:
                list_steam_ids.append(
                    [steam_id['steam_id'], steam_id['nickname'], steam_id['status'], steam_id['date']])
    return list_steam_ids


def remove(steam_id):
    with open(PATH_STEAM_IDS, encoding='utf8') as f:
        dtjson = json.load(f)

    for i in range(len(dtjson)):
        if dtjson[i]['steam_id'] == steam_id:
            dtjson.pop(i)
            with open(PATH_STEAM_IDS, 'w', encoding='utf8') as f:
                json.dump(dtjson, f, ensure_ascii=False, indent=4, separators=(',', ': '))
            break
