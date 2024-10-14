import json


class Publish:

    def __init__(self, mqttc):
        """
        Инициализация объекта Publish.

        :param mqttc: Объект клиента MQTT для публикации сообщений.
        """
        self.mqttc = mqttc

    def publish_data_emulators(self, emulator):
        """
        Публикация данных эмулятора в MQTT-топики.

        :param emulator: Объект эмулятора, содержащий данные для публикации.
        """
        if emulator.sockets_flag:
            try:
                # Публикуем данные о напряжении, токе и мощности эмулятора
                self.mqttc.publish(
                    f'mpei/Emulator_{emulator.socket.getpeername()}/Volt',
                    payload=json.dumps({"value": emulator.result[0]})
                )
                self.mqttc.publish(
                    f'mpei/Emulator_{emulator.socket.getpeername()}/Current',
                    payload=json.dumps({"value": emulator.result[1]})
                )
                self.mqttc.publish(
                    f'mpei/Emulator_{emulator.socket.getpeername()}/Power',
                    payload=json.dumps({"value": emulator.power})
                )
            except TypeError:
                print(f"Ошибка: выходные параметры {emulator.socket} являются типа None")
        else:
            # Если данные отсутствуют, публикуем нулевые значения
            self.mqttc.publish(
                f'mpei/Emulator_{emulator.socket.getpeername()}/Volt',
                payload=json.dumps({"value": 0})
            )
            self.mqttc.publish(
                f'mpei/Emulator_{emulator.socket.getpeername()}/Current',
                payload=json.dumps({"value": 0})
            )
            self.mqttc.publish(
                f'mpei/Emulator_{emulator.socket.getpeername()}/Power',
                payload=json.dumps({"value": 0})
            )

    def push_name_socket(self, em, name):
        """
        Публикация имени сокета эмулятора в MQTT-топик.
        Необходимо вынести в базу данных.

        :param em: Объект эмулятора.
        :param name: Имя для публикации.
        """
        msg = em.socket.getpeername()
        self.mqttc.publish(f"mpei/info/{name}", f"{msg}")