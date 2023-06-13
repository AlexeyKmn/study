from telethon import TelegramClient, events, sync, connection
from telethon.tl.types import InputMessagesFilterPhotos

with TelegramClient('telethon_session', 14588077, 'c003522b86c2609e198e89b5c5539967',
                    device_model="VivoBook X570ZD", system_version="Windows 10") as client:
    messages = client.iter_messages('t.me/Parsinger_Telethon_Test', filter=InputMessagesFilterPhotos, limit=100)
    for message in messages:
        client.download_media(message.media, file='img/')
