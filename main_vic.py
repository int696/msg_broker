import asyncio
from asyncio import CancelledError  # Импортируем ошибку для обработки отмены задач
from Connected.contact_mqtt import connection  # Импортируем функцию для подключения к MQTT
from Victron.victron_contact import VictronCommand  # Импортируем команду для работы с Victron
from utils.create_file_and_path import Util  # Импортируем утилиту для работы с файлами и путями
from Connected.connection_db import add_user  # Импортируем функцию для добавления пользователя в базу данных
from Request.command_operator import Command  # Импортируем класс для обработки команд

# Асинхронная функция для регулярного опроса данных Victron с интервалом в 15 секунд
async def delay(victron):
    while True:
        victron.survey_victron()  # Выполняем опрос данных от Victron
        await asyncio.sleep(15)  # Приостанавливаем выполнение на 15 секунд

# Асинхронная функция для инициализации и запуска основного цикла программы
async def init_start():
    mqttc = connection()  # Устанавливаем соединение с MQTT-брокером
    connect = add_user()  # Добавляем пользователя в базу данных
    operator = Command(mqttc, connect)  # Создаем объект для обработки команд

    data_path = Util()  # Инициализируем объект для работы с файловыми путями и данными
    victron = VictronCommand(mqttc)  # Создаем объект для работы с командами Victron

    # Загружаем и устанавливаем данные для обратного вызова Victron из JSON файла
    victron.callback_data(data_path.open_json("data_topics_victron.json"))

    # Создаем асинхронную задачу для регулярного опроса данных от Victron
    survey = asyncio.create_task(delay(victron))

    # Основной цикл программы: обновляем параметры Victron в базе данных
    while not survey.done():  # Пока задача опроса не завершена
        operator.update_param_victron(
            list(victron.dict_msg.keys()), list(victron.dict_msg.values()))  # Обновляем параметры в базе данных

        await asyncio.sleep(1)  # Приостанавливаем выполнение на 1 секунду

    try:
        await survey  # Ожидаем завершения задачи опроса
    except CancelledError:  # Обрабатываем случай, если задача была отменена
        print('Задача survey была снята')

if __name__ == '__main__':
    asyncio.run(init_start())  # Запускаем асинхронную функцию init_start в качестве основной

