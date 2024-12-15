from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel, User

api_id = 11111111  # API ID
api_hash = ''  # API Hash
phone_number = '+89999999999'  # number phone

# Подключаемся к клиенту
client = TelegramClient('session_name', api_id, api_hash)


async def parse_chat(chat_username, message_limit=100000):
    # Подключаемся к аккаунту
    await client.start(phone_number)

    # Получаем информацию о чате
    chat = await client.get_entity(chat_username)

    # Счетчик сообщений
    message_count = 0
    total_messages = 0
    last_message_id = None  # ID последнего сообщения для пагинации

    # Множество для уникальных username
    unique_usernames = set()

    # Список для всех username
    all_usernames = []

    while total_messages < message_limit:
        if last_message_id:
            messages = await client.get_messages(chat, limit=1000, max_id=last_message_id)
        else:
            messages = await client.get_messages(chat, limit=1000)

        if not messages:
            break

        for message in messages:
            sender = await message.get_sender()

            if isinstance(sender, User):  # Check user
                username = sender.username if sender.username else "Без username"

                # Добавляем username в множество (для уникальных)
                unique_usernames.add(username)


                first_name = sender.first_name if sender.first_name else "Без имени"
                print(f"Сообщение #{message_count + 1} от {first_name} {username}: {message.text}")
            elif isinstance(sender, PeerChannel):  # Если отправитель — канал
                print(
                    f"Сообщение #{message_count + 1}: От канала {sender.title} (без имени пользователя). Текст: {message.text}")
            else:
                print(
                    f"Сообщение #{message_count + 1}: Без имени пользователя (вероятно, бот или аноним). Текст: {message.text}")

            message_count += 1
            total_messages += 1

        # Redresh ID
        last_message_id = messages[-1].id

        # Pause
        if message_count % 100 == 0:
            print(f"Обработано {message_count} сообщений...")

    # Вывод уникальных username
    print(f"Уникальные username: {unique_usernames}", len(unique_usernames))

    print(f"Всего обработано {message_count} сообщений.")


with client:
    client.loop.run_until_complete(parse_chat('username_chat'))
