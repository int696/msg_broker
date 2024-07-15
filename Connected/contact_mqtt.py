import paho.mqtt.client as mqtt
from utils.create_file_and_path import Util


async def callback_data(self, topic="mpei/command_operator/em"):
    self.mqttc.message_callback_add(topic, self.get_data)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Подключение к MQTT прошло успешно")
        print("------------------------------------------------------------------")
        client.subscribe('#')
    else:
        print("Ошибка при подключении к MQTT")


def connection():
    config = Util().config_pars('setting.ini')

    user = config["MQTT"]["USER"]
    password = config["MQTT"]["PASSWORD"]
    host = config["MQTT"]["MQTT_HOST"]
    port = int(config["MQTT"]["MQTT_PORT"])
    interval = int(config["MQTT"]["MQTT_KEEPALIVE_INTERVAL"])
    mqttc = mqtt.Client()
    mqttc.username_pw_set(username=user, password=password)
    mqttc.on_connect = on_connect
    mqttc.connect(host, port, interval)
    mqttc.loop_start()
    return mqttc
