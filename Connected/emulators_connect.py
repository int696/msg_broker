import configparser
import socket
import re


class ContactEmulators:

    def __init__(self, name_config):
        self.result = None
        self.power = None
        self.socket = None
        self.config = configparser.ConfigParser()
        self.sockets = []
        self.command_list = ["MEAS:VOL?", "MEAS:CUR?", "MEAS:POW?"]
        self.name_config = name_config

    def close_socket(self):
        try:
            print("closed socket ", self.socket)
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except Exception as e:
            print("Сокет закрыт", self.socket, e)

    def get_ip_port(self):
        pass

    def __connect_sockets(self, data_socket, timeout_seconds):
        print(f"Подключение к имитатору: {data_socket}")
        ip, port = data_socket
        try:
            supply_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            supply_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            supply_socket.connect((ip, port))
            # supply_socket.settimeout(timeout_seconds)

            print(f"Успешное подключение к {data_socket}")
            print(f"------------------------------------------------------------------")
            self.sockets_flag = True
            return supply_socket
        except (ConnectionRefusedError, TimeoutError) as e:
            print(f"Ошибка {e} при подключении к {data_socket}")
            print(f"------------------------------------------------------------------")
            self.sockets_flag = False
    
    def send_and_receive_command(self, msg, supply_socket):
        try:
            msg = msg + "\n"
            supply_socket.sendall(msg.encode("UTF-8"))
            buffer_size = self.config[self.name_config]["BUFFER_SIZE"]
            try:
                return re.findall(r'\d+\.\d+', supply_socket.recv(int(buffer_size)).decode())
            except TimeoutError as e:
                print(e)
        except Exception as e:
            print("send_and_receive_command", e)

    def connection_sim(self, path):
        self.config.read(path)
        ip = self.config[self.name_config]["IP"]

        port = int(self.config[self.name_config]["PORT"])
        timeout = int(self.config[self.name_config]["TIMEOUT_SECONDS"])
        self.socket = self.__connect_sockets([ip, port], timeout)

    def get_data_emulators(self):
        if self.sockets_flag:
            try:
                self.result = self.send_and_receive_command("MEAS:VOL?\nMEAS:CUR?", self.socket)
                self.power = f"{float(self.result[0]) * float(self.result[1])}"
            except TypeError:
                print(f"Выходные параметры {self.socket} являются типа None")

