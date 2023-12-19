import json


def load_user_data(data_path):
    """Функция, которая загружает данные пользователей из файла и возвращает словарь.
    Если файла нет, то возвращается пустой словарь.
    :param data_path: путь к файлу с данными
    :return: словарь с данными пользователей
    """
    try:
        with open(data_path, "r") as file:
            return json.load(file)
    except:
        return {}


def save_user_data(user_data, data_path):
    """Функция, которая сохраняет данные пользователей в файл.
    :param user_data: словарь с данными пользователей
    :param data_path: путь к файлу с данными
    """
    with open(data_path, "w") as file:
        json.dump(user_data, file)
