import json


class Publish:

    def __init__(self, mqttc):
        self.mqttc = mqttc

    def publish_data_emulators(self, emulator):
        if emulator.sockets_flag:
            try:
                self.mqttc.publish(f'mpei/Emulator_{emulator.socket.getpeername()}/Volt',
                                   payload=json.dumps({"value": emulator.result[0]}))
                self.mqttc.publish(f'mpei/Emulator_{emulator.socket.getpeername()}/Current',
                                   payload=json.dumps({"value": emulator.result[1]}))
                self.mqttc.publish(f'mpei/Emulator_{emulator.socket.getpeername()}/Power',
                                   payload=json.dumps({"value": emulator.power}))
            except TypeError:
                print(f"Выходные параметры {emulator.socket} являются типа None")
        else:
            self.mqttc.publish(f'mpei/Emulator{emulator.socket.getpeername()}/Volt',
                               payload=json.dumps({"value": 0}))
            self.mqttc.publish(f'mpei/Emulator{emulator.socket.getpeername()}/Current',
                               payload=json.dumps({"value": 0}))
            self.mqttc.publish(f'mpei/Emulator_{emulator.socket.getpeername()}/Power',
                               payload=json.dumps({"value": 0}))


    def push_name_socket(self, em, name):

        """НУЖНО ВЫНЕСТИ В БД!!!!!!!!!!!!!!!!!!!!!!"""

        msg = em.socket.getpeername()
        self.mqttc.publish(f"mpei/info/{name}", f"{msg}")