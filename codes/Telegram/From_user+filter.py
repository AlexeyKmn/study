from telethon import TelegramClient, events, sync, connection

with TelegramClient('telethon_session', 14588077, 'c003522b86c2609e198e89b5c5539967',
                    device_model="VivoBook X570ZD", system_version="Windows 10") as client:
    user_id = 5807015533
    messages = client.get_messages('t.me/Parsinger_Telethon_Test', from_user=user_id, limit=100)
    print(len(messages))
    res = 0
    for message in messages:
        try:
            res += int(message.text)
        except:
            continue
    print(res)
