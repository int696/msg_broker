import configparser  # Импортируем модуль для работы с конфигурационными файлами

import pymysql  # Импортируем модуль для работы с MySQL
from pymysql.cursors import DictCursor  # Импортируем DictCursor для работы с результатами запросов как с словарями


def add_user():
    # Создаем объект ConfigParser для чтения конфигурационного файла
    config = configparser.ConfigParser()
    config.read("utils/setting.ini")  # Читаем конфигурационный файл

    # Закомментированные строки ниже могут быть использованы для получения параметров подключения из файла
    # host = config['BD']['HOST']
    # user = config['BD']['USER']
    # password = config['BD']['PASSWORD']
    # BD = config['BD']['BD_NAME']

    try:
        # Устанавливаем соединение с базой данных с использованием предоставленных данных
        connect = pymysql.connect(
            host='10.2.173.169',  # Адрес сервера базы данных
            port=3306,  # Порт для подключения по умолчанию этот порт занимает БД
            user='user1',  # Имя пользователя
            password="123",  # Пароль пользователя
            cursorclass=DictCursor,  # Используем DictCursor для получения данных в виде словарей
            database='test',  # Название базы данных
            autocommit=True  # Включаем автоматическое подтверждение транзакций
        )

        return connect  # Возвращаем объект подключения

    except Exception as e:  # Вызываем исключения при неудачном подключении
        print("Подключение не удалось")  # Сообщаем о неудачном подключении
        print(e)  # Выводим информацию об ошибке

