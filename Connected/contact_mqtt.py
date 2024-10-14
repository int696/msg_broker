import paho.mqtt.client as mqtt  # Импортируем библиотеку paho-mqtt для работы с MQTT
from utils.create_file_and_path import Util  # Импортируем утилиту для работы с файлами и путями


# Функция, вызываемая при подключении к MQTT брокеру
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # Если код возврата 0, подключение прошло успешно
        print("Подключение к MQTT прошло успешно")
        print("------------------------------------------------------------------")
        client.subscribe('#')  # Подписываемся на все темы
    else:
        # В случае ошибки выводим сообщение
        print("Ошибка при подключении к MQTT")


# Функция для установки соединения с MQTT брокером
def connection():
    # Загружаем конфигурацию из файла 'setting.ini'
    config = Util().config_pars('setting.ini')

    # Получаем параметры подключения из конфигурационного файла
    user = config["MQTT"]["USER"]
    password = config["MQTT"]["PASSWORD"]
    host = config["MQTT"]["MQTT_HOST"]
    port = int(config["MQTT"]["MQTT_PORT"])  # по умолчанию порт 1883 занимает MQTT брокер
    interval = int(config["MQTT"]["MQTT_KEEPALIVE_INTERVAL"])

    # Создаем MQTT клиента
    mqttc = mqtt.Client()
    # Устанавливаем имя пользователя и пароль для подключения
    mqttc.username_pw_set(username=user, password=password)
    # Назначаем функцию обратного вызова при подключении
    mqttc.on_connect = on_connect
    # Подключаемся к MQTT брокеру с указанными параметрами
    mqttc.connect(host, port, interval)
    # Запускаем цикл обработки сообщений
    mqttc.loop_start()

    return mqttc  # Возвращаем объект MQTT клиента иными словами подключение к MQTT брокеру

