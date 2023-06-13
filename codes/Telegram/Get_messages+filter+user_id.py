from telethon import TelegramClient, events, sync, connection
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputMessagesFilterPinned

with TelegramClient('telethon_session', 14588077, 'c003522b86c2609e198e89b5c5539967',
                    device_model="VivoBook X570ZD", system_version="Windows 10") as client:
    message = client.get_messages('t.me/Parsinger_Telethon_Test', filter=InputMessagesFilterPinned)  # возвращает LIST!!
    id_user = message[0].from_id.user_id
    print(id_user, client.get_entity(id_user).username)
