import json
import datetime
from functools import partial


class VictronCommand:
    def __init__(self, mqttc):
        """
        Инициализация объекта VictronCommand.

        :param mqttc: Объект клиента MQTT для публикации и получения сообщений.
        """
        self.parsed_data = None  # Хранение распарсенных данных
        self.flag_parsed_data = False  # Флаг, указывающий на то, что данные распарсены
        self.dictionary = None  # Словарь для хранения данных
        self.flag_get_data = False  # Флаг, указывающий на то, что данные получены
        self.dict_msg = {
            "ac_consumption_L1_power": 0,
            "ac_consumption_L2_power": 0,
            "ac_consumption_L3_power": 0,
            "ac_out_L1_active_power": 0,
            "ac_out_L2_active_power": 0,
            "ac_out_L3_active_power": 0,
            "ac_out_L1_current": 0,
            "ac_out_L2_current": 0,
            "ac_out_L3_current": 0,
            "battery_current": 0,
            "battery_power": 0,
            "battery_SOC": 0,
            "battery_voltage": 0,
            "F": 0
        }  # Словарь для хранения различных данных, полученных от устройства
        self.mqttc = mqttc  # Сохранение объекта клиента MQTT

    def survey_victron(self):
        """
        Отправка сообщения для проверки связи с Victron.
        """
        # Публикация сообщения для проверки связи
        self.mqttc.publish('R/d436391ea13a/keepalive/', 'empty')

    def get_data(self, client, userdata, data, key):
        """
        Обработка данных, полученных от MQTT, для конкретного ключа.

        :param client: Клиент MQTT.
        :param userdata: Данные пользователя.
        :param data: Полученные данные.
        :param key: Ключ для обновления значения в dict_msg.
        """
        try:
            # Декодирование и распарсивание данных из JSON
            parsed_data = json.loads(data.payload.decode("utf-8", "ignore"))
            self.dictionary = parsed_data  # Сохранение распарсированных данных в словарь
            # Обновление значения в словаре с данными
            self.dict_msg[key] = self.dictionary.get('value', 0)
            self.validate_data(data)  # Проверка данных на корректность
            if self.flag_get_data:
                self.parsed_data = parsed_data  # Сохранение распарсированных данных
                self.flag_parsed_data = True  # Установка флага, что данные распарсены
            else:
                print("Получена пустая полезная нагрузка:", data.topic)  # Вывод сообщения в случае пустых данных
        except json.JSONDecodeError as e:
            # Обработка ошибки декодирования JSON
            print("Ошибка декодирования JSON:", e)

    def callback_data_all(self, log_victron, topic="N/d436391ea13a/#"):
        """
        Настройка callback-функции для обработки данных по всем топикам.

        :param log_victron: Функция для записи данных в лог.
        :param topic: Топик для подписки.
        """
        self.log_victron = log_victron  # Сохранение функции для логирования
        # Добавление функции обратного вызова для обработки данных по указанному топику
        self.mqttc.message_callback_add(topic, self.get_data_all)

    def get_data_all(self, client, userdata, data):
        """
        Обработка данных, полученных по топику, и запись в лог.

        :param client: Клиент MQTT.
        :param userdata: Данные пользователя.
        :param data: Полученные данные.
        """
        try:
            # Декодирование и распарсивание данных из JSON
            parsed_data = json.loads(data.payload.decode("utf-8", "ignore"))
            self.validate_data(data)  # Проверка данных на корректность
            if self.flag_get_data:
                # Запись данных в лог
                self.log_victron('log_victron.csv', 'a', [data.topic, parsed_data, f"time {datetime.datetime.now()}"])
            else:
                print("Получена пустая полезная нагрузка:", data.topic)  # Вывод сообщения в случае пустых данных
        except json.JSONDecodeError as e:
            # Обработка ошибки декодирования JSON
            print("Ошибка декодирования JSON:", e, data.topic)

    def callback_data(self, topic):
        """
        Настройка callback-функции для обработки данных по указанным топикам.

        :param topic: Словарь с топиками и соответствующими ключами.
        """
        # Для каждого ключа и топика добавляем обработчик данных
        for key, item in topic.items():
            self.mqttc.message_callback_add(item, partial(self.get_data, key=key))

    def publish_topic(self, topics_client):
        """
        Публикация данных по указанным топикам.

        :param topics_client: Словарь с топиками и значениями для публикации.
        """
        # Для каждого ключа и значения публикуем данные по соответствующему топику
        for key, item in self.dict_msg.items():
            self.mqttc.publish(
                topics_client.get(key), item
            )

    def validate_data(self, data):
        """
        Проверка данных на корректность.

        :param data: Данные для проверки.
        :return: True если данные корректны, иначе False.
        """
        if data:
            self.flag_get_data = True  # Установка флага, что данные получены
            return True
        return False