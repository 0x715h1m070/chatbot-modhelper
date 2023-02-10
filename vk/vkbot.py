import  vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


token = "TOKEN"
vk = vk_api.VkApi(token=token)
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, 00000000)
peer_id = 2000000000