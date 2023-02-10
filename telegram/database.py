import json
import os
import db_profiles as profiles
import db_steam_id as steam_ids
import get_script_dir as gsd


PATH_DATABASE = gsd.get_script_dir() + '/database'
PATH_PROFILES = PATH_DATABASE + '/profiles.json'
PATH_STEAM_IDS = PATH_DATABASE + '/steam_ids.json'

def main():
    if not os.path.exists(PATH_DATABASE):
        os.makedirs(PATH_DATABASE)
    if not os.path.isfile(PATH_PROFILES):
        with open(PATH_PROFILES, 'wt') as f:
            f.write(' ')
        clear(database='profiles')
    if not os.path.isfile(PATH_STEAM_IDS):
        with open(PATH_STEAM_IDS, 'wt') as f:
            f.write(' ')
        clear(database='steam_ids')
    '''if not os.path.isfile(PATH_MODERATORS):
        with open(PATH_MODERATORS, 'wt') as f:
            f.write(' ')
        clear(database='moderators')'''


def clear(database):
    data = None
    if database == 'profiles':
        data = [{
            "id_profile": 0,
            "password": "dsfHUhgLGkJh",
            "telegram_id": 1,
            "privilege": {
                "admin": False,
                "moderator_website": False
            }
        }]
        with open(PATH_PROFILES, 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
    elif database == 'steam_ids':
        data = [{
            "steam_id": "",
            "nickname": "",
            "status": "",
            "date": "00.00.0000"
        }, ]
        with open(PATH_STEAM_IDS, 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
    '''elif database == 'moderators':
        data = ({
                    "WEBSITE_A": [],
                    "WEBSITE_B": []
                },)

        with open(PATH_MODERATORS, 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
'''

