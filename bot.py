import telebot
from data import load_user_data, save_user_data
from secret_santa import welcome_message, resources_str, shuffle_users

# todo: считывать токен из ввода
TOKEN = input("Вставьте свой токен: ")
# TOKEN = "TOKEN"
bot = telebot.TeleBot(TOKEN)

# todo: считывать количество участников из ввода
users_total = int(input("Введите количество участников: "))
# users_total = 6



data_path = "users.json"
user_data = load_user_data(data_path)

def count_gifts(user_data):
    users_sent_gift = 0
    for user_id, user in user_data.items():
        if user["gift_id"] != "":
            users_sent_gift += 1
    return users_sent_gift



print(count_gifts(user_data))
users_sent_gift = count_gifts(user_data)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("/start", "Зарегистрироваться в игре!"),
        telebot.types.BotCommand("/resources", "Где можно сгенерировать подарок?"),
    ],
)


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    # Отправляем приветственное сообщение
    bot.send_message(message.chat.id, welcome_message)

    # Отправляем сообщение с вопросом о предпочтениях
    bot.send_message(message.chat.id,
                     "Чтобы твоему санте было легче сгенерировать открытку, "
                     "перечисли в ответном сообщении минимум три вещи, которые тебе нравятся.\n"
                     "Это может быть твоя любимая еда, любимый цвет, любимый испольнитель "
                     "или что-то другое (фильмы, книги, компьютерные игры, животные, предметы и т.д.)")
    bot.register_next_step_handler(message, get_preferences)


def get_preferences(message):
    global user_data
    # Инициализируем данные пользователя
    user_data[message.chat.id] = {"name": message.from_user.first_name,
                                  "preferences": message.text,
                                  "send_to": None, "gift_id": "", "gift_type": ""}

    # Сохраняем данные пользователя
    save_user_data(user_data, data_path)

    print(user_data)

    bot.send_message(message.chat.id, "Спасибо за ответы! Теперь ждём всех участников!\n"
                                      "А пока ты можешь ознакомиться с ресурсами, "
                                      "которые помогут тебе сгенерировать подарок. Напиши /resources")
    if len(user_data) == users_total:
        user_data = shuffle_users(user_data)
        # Сохраняем данные пользователя
        save_user_data(user_data, data_path)
        # Отправляем сообщение с информацией о том, кому кто дарит подарок
        send_info(user_data)


def send_info(user_data):
    for user_id, user in user_data.items():
        bot.send_message(user_id, f"Итак, {user['name']}, \n"
                                  f"У меня для тебя хорошие новости.\n"
                                  f"Все участники зарегистрированы, начинаем розыгрыш!")
        bot.send_message(user_id, f"Твой счастливчик - {user_data[user['send_to']]['name']}!\n"
                                  f"Вот что он(а) любит: {user_data[user['send_to']]['preferences']}\n"
                                  f"Тебе нужно отправить подарок ответным сообщением.\n"
                                  f"Это может быть картинка, аудио или даже видео!\n"
                                  f"Постарайся учесть как можно больше предпочтений.")

if len(user_data) == users_total:
    user_not_assigned = False
    for user_id, user in user_data.items():
        if user["send_to"] == None:
            user_not_assigned = True
    if user_not_assigned:
        user_data = shuffle_users(user_data)
        # Сохраняем данные пользователя
        save_user_data(user_data, data_path)
    # Отправляем сообщение с информацией о том, кому кто дарит подарок
    send_info(user_data)

# Обработчик команды /resources
@bot.message_handler(commands=["resources"])
def resources(message):
    bot.send_message(message.chat.id, resources_str, parse_mode='HTML')


# Команда для отправки медиа-файлов
@bot.message_handler(content_types=['photo', 'video', 'audio'])
def handle_media_files(message):
    global user_data, users_sent_gift
    chat_id = str(message.chat.id)
    print(chat_id)
    if chat_id in user_data:
        print(f"Пришёл подарок от {message.from_user.first_name}")
        print(message.content_type)
        file_id = message.document.file_id if message.content_type == "document" else message.audio.file_id if message.content_type == "audio" else message.video.file_id if message.content_type == "video" else message.photo[0].file_id
        user_data[chat_id]['gift_id'] = file_id
        user_data[chat_id]['gift_type'] = message.content_type
        print(user_data)
        save_user_data(user_data, data_path)
        bot.send_message(chat_id, "Медиа-файл принят!")
        users_sent_gift = count_gifts(user_data)
        if users_sent_gift == users_total:
            send_media_files(user_data)


def send_media_files(user_data):
    for user_id, user in user_data.items():
        recipient_id = user['send_to']
        file_id = user['gift_id']
        file_type = user['gift_type']
        bot.send_message(recipient_id, f"Привет, {user_data[recipient_id]['name']}!\n"
                                       f"Тебе тут открытка от твоего секретного санты!")
        if file_type == 'photo':
            bot.send_photo(recipient_id, file_id)
        elif file_type == 'video':
            bot.send_video(recipient_id, file_id)
        elif file_type == 'audio':
            bot.send_audio(recipient_id, file_id)
    save_user_data(dict(), data_path)


# Запуск бота
bot.infinity_polling()
