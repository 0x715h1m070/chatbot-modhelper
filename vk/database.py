import sqlite3
import vkbot


db = sqlite3.connect('root/bot/database.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS WEBSITE_A_bans(
    url_ban TEXT,
    nickname TEXT
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS WEBSITE_B_bans(
    url_ban TEXT,
    nickname TEXT
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS off_ids(
    id BIGINT
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS steam_ids(
    id TEXT
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS moders_WEBSITE_A(
    id_login BIGINT,
    id_vk BIGINT,
    login TEXT,
    razban BIGINT,
    nerazban BIGINT
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS moders_WEBSITE_B(
    id_login BIGINT,
    id_vk BIGINT,
    login TEXT,
    razban BIGINT,
    nerazban BIGINT
)""")

db.commit()

def add_steam_id():
    sql.execute("DROP TABLE IF EXISTS steam_ids")
    sql.execute("""CREATE TABLE IF NOT EXISTS steam_ids(
        id TEXT
    )""")
    db.commit()

    BaseSteamID = open('BlackListSteamID.txt', 'r')
    TextBaseSteamID = BaseSteamID.read().split()
    BaseSteamID.close()
    for SteamID in TextBaseSteamID:
        if SteamID:
            sql.execute("SELECT id FROM steam_ids WHERE id = '"+str(SteamID)+"'")
            if sql.fetchone() is None:
                sql.execute("INSERT INTO steam_ids VALUES ('"+str(SteamID)+"')")
                db.commit()


def clear_top():
    sql.execute("DROP TABLE IF EXISTS moders_WEBSITE_A")
    sql.execute("""CREATE TABLE IF NOT EXISTS moders_WEBSITE_A(
        id_login BIGINT,
        id_vk BIGINT,
        login TEXT,
        razban BIGINT,
        nerazban BIGINT
    )""")
    sql.execute("DROP TABLE IF EXISTS moders_WEBSITE_B")
    sql.execute("""CREATE TABLE IF NOT EXISTS moders_WEBSITE_B(
        id_login BIGINT,
        id_vk BIGINT,
        login TEXT,
        razban BIGINT,
        nerazban BIGINT
    )""")
    db.commit()

def check_profiles():
    sql.execute("DROP TABLE IF EXISTS admins_id")
    sql.execute("DROP TABLE IF EXISTS users_id")

    sql.execute("""CREATE TABLE IF NOT EXISTS admins_id(
        id BIGINT
    )""")
    sql.execute("""CREATE TABLE IF NOT EXISTS users_id(
        id BIGINT
    )""")
    db.commit()


    count = vkbot.vk.method("messages.getConversationMembers", {"peer_id": vkbot.peer_id})["count"]
    for i in range(int(count)):
        id_profile = vkbot.vk.method("messages.getConversationMembers", {"peer_id": vkbot.peer_id})["items"][i]["member_id"]
        try:
            admin = vkbot.vk.method("messages.getConversationMembers", {"peer_id": vkbot.peer_id})["items"][i]["is_admin"]
        except:
            admin = False
        if admin:
            if int(id_profile) > 0:
                sql.execute("SELECT id FROM admins_id WHERE id = '"+str(id_profile)+"'")
                if sql.fetchone() is None:
                    sql.execute("INSERT INTO admins_id VALUES ('"+str(id_profile)+"')")
                    db.commit()
        else:
            if int(id_profile) > 0:
                sql.execute("SELECT id FROM users_id WHERE id = '"+str(id_profile)+"'")
                if sql.fetchone() is None:
                    sql.execute("INSERT INTO users_id VALUES ('"+str(id_profile)+"')")
                    db.commit()

        # print(id_profile,admin)
