import json
import get_script_dir as gsd

PATH_DATABASE = gsd.get_script_dir() + '/database'
PATH_PROFILES = PATH_DATABASE + '/profiles.json'


def auth(id_profile, password, telegram_id):
    with open(PATH_PROFILES, encoding='utf8') as f:
        dtjson = json.load(f)
    login = False
    for profile in range(len(dtjson)):
        if int(id_profile) == dtjson[profile]['id_profile'] and password == dtjson[profile]['password'] or int(
                telegram_id) == dtjson[profile]['telegram_id']:
            if dtjson[profile]['telegram_id'] == 0 or int(telegram_id) == dtjson[profile]['telegram_id']:
                dtjson[profile]['telegram_id'] = int(telegram_id)
                with open(PATH_PROFILES, 'w', encoding='utf8') as f:
                    json.dump(dtjson, f, ensure_ascii=False, indent=4, separators=(',', ': '))
                login = True
            break
    return login


def get_profile(telegram_id):
    with open(PATH_PROFILES, encoding='utf8') as f:
        dtjson = json.load(f)
    for profile in dtjson:
        if int(telegram_id) == profile['telegram_id']:
            return profile
            break
