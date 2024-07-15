import csv
import json
import os
from sys import platform
import logging
import configparser


class Util:

    @staticmethod
    def get_data_path(name_file):
        current_script_path = os.path.abspath(__file__)
        if platform == 'win32' or platform == 'win64':
            return os.path.dirname(os.path.dirname(current_script_path)) + f"\\utils\\{name_file}"
        elif platform == 'linux' or platform == 'linux2':
            return os.path.dirname(os.path.dirname(current_script_path)) + f"/utils/{name_file}"

    @staticmethod
    def get_data_path_log(name_file):
        current_script_path = os.path.abspath(__file__)
        if platform == 'win32' or platform == 'win64':
            return os.path.dirname(os.path.dirname(current_script_path)) + f"\\log\\{name_file}"
        elif platform == 'linux' or platform == 'linux2':
            return os.path.dirname(os.path.dirname(current_script_path)) + f"/log/{name_file}"

    def open_json(self, name_file):
        try:
            path = self.get_data_path(name_file)
            with open(path, 'r') as json_file:
                data = json.load(json_file)
            return data
        except Exception as e:
            print(f"Ошибка открытия {name_file}: {e}")

    def create_json(self, name_file, data):
        try:
            path = self.get_data_path(name_file)
            with open(path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        except Exception as e:
            print(f"Ошибка создания {name_file}: {e}")

    def open_csv(self, name_file, mode, data):

        path = self.get_data_path(name_file)
        with open(path, mode=mode, encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            data_to_add = data
            writer.writerow(data_to_add)

    def create_log(self, mode):
        path = self.get_data_path_log("py_log_mqtt.log")
        logging.basicConfig(level=logging.INFO, filename=path, filemode=mode,
                            format="%(asctime)s %(levelname)s %(message)s")

    def config_pars(self, name):
        config = configparser.ConfigParser()
        project_root_path = self.get_data_path(name)
        config.read(project_root_path)
        return config

