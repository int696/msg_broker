import configparser  # Импортируем модуль для работы с конфигурационными файлами
import socket  # Импортируем модуль для работы с сетевыми сокетами
import re  # Импортируем модуль для работы с регулярными выражениями


class ContactEmulators:

    def __init__(self, name_config):
        # Инициализация переменных класса
        self.result = None  # Переменная для хранения результатов измерений
        self.power = None  # Переменная для хранения рассчитанной мощности
        self.socket = None  # Переменная для хранения объекта сокета
        self.config = configparser.ConfigParser()  # Создаем объект для работы с конфигурационными файлами
        self.sockets = []  # Список для хранения сокетов
        self.command_list = ["MEAS:VOL?", "MEAS:CUR?", "MEAS:POW?"]  # Список команд для эмулятора
        self.name_config = name_config  # Имя конфигурационного файла или секции

    def close_socket(self):
        try:
            # Попытка корректно закрыть сокетное соединение
            print("closed socket ", self.socket)
            self.socket.shutdown(socket.SHUT_RDWR)  # Завершаем передачу и прием данных
            self.socket.close()  # Закрываем сокет
        except Exception as e:
            # Обработка исключений при закрытии сокета
            print("Сокет закрыт", self.socket, e)

    def __connect_sockets(self, data_socket, timeout_seconds):
        print(f"Подключение к имитатору: {data_socket}")
        ip, port = data_socket  # Получаем IP и порт из переданных данных
        try:
            # Создаем TCP/IP сокет
            supply_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Разрешаем повторное использование адреса сокета
            supply_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Подключаемся к эмулятору
            supply_socket.connect((ip, port))
            # Устанавливаем флаг успешного подключения
            print(f"Успешное подключение к {data_socket}")
            print(f"------------------------------------------------------------------")
            self.sockets_flag = True
            return supply_socket  # Возвращаем сокет для дальнейшего использования
        except (ConnectionRefusedError, TimeoutError) as e:
            # Обработка исключений при неудачном подключении
            print(f"Ошибка {e} при подключении к {data_socket}")
            print(f"------------------------------------------------------------------")
            self.sockets_flag = False

    def send_and_receive_command(self, msg, supply_socket):
        try:
            # Отправляем команду эмулятору
            msg = msg + "\n"
            supply_socket.sendall(msg.encode("UTF-8"))
            # Получаем размер буфера для получения данных из конфигурации
            buffer_size = self.config[self.name_config]["BUFFER_SIZE"]
            try:
                """Принимаем и декодируем ответ, извлекая числовые значения с помощью регулярных выражений
                шаблон r'\d+\.\d+' ищет подстроки, которые представляют собой числа с десятичной точкой
                \d+ означает "одна или более цифр".
                \. соответствует символу точки.
                \d+ после точки снова означает "одна или более цифр"."""

                return re.findall(r'\d+\.\d+', supply_socket.recv(int(buffer_size)).decode())
            except TimeoutError as e:
                # Обработка исключения при таймауте получения данных
                print(e)
        except Exception as e:
            # Обработка исключений при отправке или получении данных
            print("send_and_receive_command", e)

    def connection_sim(self, path):
        # Чтение конфигурационного файла для получения настроек подключения
        self.config.read(path)
        ip = self.config[self.name_config]["IP"]  # Получаем IP адрес из конфигурации
        port = int(self.config[self.name_config]["PORT"])  # Получаем порт из конфигурации по умолчанию 8462 в эмуляторе
        timeout = int(self.config[self.name_config]["TIMEOUT_SECONDS"])  # Получаем таймаут из конфигурации
        # Устанавливаем соединение с эмулятором через сокет
        self.socket = self.__connect_sockets([ip, port], timeout)

    def get_data_emulators(self):
        # Получаем данные от эмулятора, если сокет успешно подключен
        if self.sockets_flag:
            try:
                # Отправляем команды на измерение напряжения и тока
                self.result = self.send_and_receive_command("MEAS:VOL?\nMEAS:CUR?", self.socket)
                # Рассчитываем мощность на основе полученных данных
                self.power = f"{float(self.result[0]) * float(self.result[1])}"
            except TypeError:
                # Обработка ситуации, когда данные не были получены
                print(f"Выходные параметры {self.socket} являются типа None")
