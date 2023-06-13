from telethon import TelegramClient, events, sync, connection
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputMessagesFilterPhotos

with TelegramClient('telethon_session', 14588077, 'c003522b86c2609e198e89b5c5539967',
                    device_model="VivoBook X570ZD", system_version="Windows 10") as client:
    # парсим фото пользователя
    # all_user_group = client.get_participants('t.me/Parsinger_Telethon_Test')
    # for user in all_user_group:
    #     for iter_photo in client.iter_profile_photos(user):
    #         client.download_media(iter_photo, file='img/')

    # парсим профиль пользователя (нужен импорт GetFullUserRequest)
    # lst = ['Anthony_Hills']
    # users = client.iter_participants('Parsinger_Telethon_Test')
    # res = 0
    # for user in users:
    #     if f'{user.first_name}_{user.last_name}' in lst:
    #         user_full_about = client(GetFullUserRequest(user))
    #         res += int(user_full_about.full_user.about)

    # парсим из канала медиа
    all_message = client.get_messages('https://t.me/python_parsing', filter=InputMessagesFilterPhotos, limit=100)
    for message in all_message:
        client.download_media(message)
