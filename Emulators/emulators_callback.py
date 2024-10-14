import json

class EmCallback:

    def __init__(self, mqttc, em, em_command):
        # Инициализация объекта класса EmCallback
        # mqttc - объект MQTT-клиента
        # em - объект, представляющий эмулятор
        # em_command - объект для отправки команд эмулятору
        self.flag_get_data = None
        self.em = em
        self.mqttc = mqttc
        self.em_command = em_command

        self.flag = True
        # Словарь для хранения предыдущих команд, отправленных эмулятору
        self.old_command = {
            "OUTPUT, ": 0,
            "SYST:INT:SIM:SET TPV,": None,
            "SYST:INT:SIM:SET GPV,": None
        }

    def callback_data(self, topic="mpei/command_operator/em"):
        # Метод для подписки на определённую тему MQTT и назначения callback-функции
        # topic - тема, на которую происходит подписка
        self.mqttc.message_callback_add(topic, self.get_data)

    def get_data(self, client, userdata, data):
        # Метод для обработки входящих сообщений от MQTT
        # client - MQTT-клиент
        # userdata - пользовательские данные (не используются здесь)
        # data - сообщение MQTT
        parsed_data = json.loads(data.payload.decode("utf-8", "ignore"))
        # Валидация полученных данных
        self.validate_data(data)
        # Если данные прошли валидацию, отправляем команду эмулятору
        if self.flag_get_data:
            self.push_command(parsed_data)

    def validate_data(self, data):
        # Метод для валидации полученных данных
        # Устанавливаем флаг успешной валидации, если данные не пустые
        if data:
            self.flag_get_data = True

    def command_out(self, msg):
        # Метод для отправки команд эмулятору
        # msg - словарь с командами для отправки
        for key, value in msg.items():
            command = f"{key}{value}"
            self.em_command.send_command(command)

    def push_command(self, msg):
        # Метод для отправки набора команд эмулятору
        # msg - словарь с командами для отправки
        self.em_command.set_prog_source_v("eth")
        self.em_command.set_prog_source_i("eth")
        for key, value in msg.items():
            command = f"{key}{value}"
            self.em_command.send_command(command)
        self.em_command.set_prog_source_v("slot4")
        self.em_command.set_prog_source_i("slot4")

    def command_processing_em(self, start_stop_em, command, value):
        # Метод для обработки команд start/stop и их отправки эмулятору
        # start_stop_em - флаг для запуска/остановки эмулятора
        # command - команда для эмулятора
        # value - значение команды
        if start_stop_em:
            # Если эмулятор должен быть запущен и команда изменилась с последнего раза
            if self.old_command[command] != value:
                self.command_out({
                    command: value,
                })
                # Обновляем сохранённую команду
                self.old_command[command] = value
                # Включаем выход
                self.command_out({
                    "OUTPUT, ": 1,
                })
                self.old_command["OUTPUT, "] = 1
                print(f"Команда {command}{value} на {self.em.socket.getpeername()}")

        else:
            # Если эмулятор должен быть остановлен и команда изменилась с последнего раза
            if self.old_command[command] != value:
                self.command_out({
                    command: value,
                })
                # Отключаем выход
                self.command_out({
                    "OUTPUT, ": 0,
                })
                self.old_command[command] = value
                print(f"Команда {command}{value} на {self.em.socket.getpeername()}")


