# Напишите приветственное сообщение
welcome_message = "О-хо-хо! Добро пожаловать в секретный сантабот!\n" \
                    "Я - Санта, и я помогу вам организовать новогодний подаркообмен!\n" \


# Напишите функцию, которая будет перемешивать пользователей
def shuffle_users(user_data):
    """
    Функция, перемешивающая пользователей.
    Принимает на вход словарь с данными пользователей.
    Возвращает словарь с данными пользователей, в котором каждому пользователю
    присвоен id другого пользователя, которому он должен сделать подарок.
    """
    import random
    users = list(user_data.keys())
    random.shuffle(users)
    for i, user in enumerate(users):
        user_data[user]["send_to"] = users[(i + 1) % len(users)]
    return user_data


