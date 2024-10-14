from datetime import datetime  # Импортируем класс для работы с датой и временем
import requests  # Импортируем библиотеку для отправки HTTP-запросов
import pandas as pd  # Импортируем Pandas для работы с данными
from utils.create_file_and_path import Util  # Импортируем утилиты для работы с файлами и путями


class WeatherForecast:

    def __init__(self):
        """
        Инициализация объекта WeatherForecast.
        """

        self.__params = None  # Приватная переменная для хранения параметров запроса
        self.__headers = None  # Приватная переменная для хранения заголовков запроса
        self.set_param()  # Устанавливаем параметры по умолчанию
        self.name_file = Util()  # Инициализируем объект утилиты для работы с файлами

    def set_param(self, station='1', var_station='mpei', var_nwp_provider='icon'):
        """
        Устанавливаем параметры для запроса погоды.

        :param station: Идентификатор станции.
        :param var_station: Название станции.
        :param var_nwp_provider: Поставщик прогноза погоды.
        """
        self.__headers = {
            'accept': 'application/json',  # Заголовок указывает, что мы ожидаем получить данные в формате JSON
        }

        # Параметры запроса включают идентификатор станции, название станции и провайдера прогноза погоды
        self.__params = {
            'orgId': station,
            'var-station': var_station,
            'var-nwp_provider': var_nwp_provider,
        }

    def get_json(self):
        """
        Выполняем запрос к серверу и сохраняем полученные данные в формате JSON.
        """
        # Формируем URL для запроса на основе параметров
        address = f"http://62.109.30.150:81/stations/" \
                  f"{self.__params['var-station']}/" \
                  f"{self.__params['var-nwp_provider']}"

        # Выполняем GET-запрос на сервер
        response = requests.get(address, headers=self.__headers)
        if response.status_code == 200:  # Проверяем, успешен ли запрос
            try:
                print(200)  # Выводим статус-код 200 (OK) для отладки
                json_data = response.json()  # Получаем данные в формате JSON
                data = self.__get_data()  # Определяем текущий час для выборки данных
                # Создаем и сохраняем JSON-файл с данными прогноза на следующие 24 часа
                self.name_file.create_json("weather.json", json_data[data:24 + data])
            except ValueError:
                # Обработка ошибки, если данные не могут быть преобразованы в JSON
                print("Сервер вернул некорректный JSON")
        else:
            # Обработка ошибки, если сервер вернул неуспешный статус-код
            print(f"Запрос завершился с кодом ошибки {response.status_code}")

    @staticmethod
    def __get_data():
        """
        Определяем текущий час для выборки данных.

        :return: Текущий час в виде целого числа.
        """
        return int(datetime.now().strftime("%H"))  # Получаем текущий час в формате 24-часового времени

    @staticmethod
    def get_param_weather(hour=1, *param):
        """
        Получаем параметры прогноза погоды из сохраненного JSON-файла.

        :param hour: Время в часах для выборки прогноза.
        :param param: Параметры погоды, которые необходимо получить.
        :return: DataFrame или Series с выбранными параметрами погоды.
        """
        data_json = Util().open_json("weather.json")  # Открываем сохраненный JSON-файл с прогнозом погоды
        if param:
            # Если переданы параметры, возвращаем только выбранные параметры для указанного часа
            df = pd.json_normalize(data_json).iloc[hour].loc[list(param)]
        else:
            # Если параметры не переданы, возвращаем все данные для указанного часа
            df = pd.json_normalize(data_json).iloc[hour]
        return df  # Возвращаем данные в формате DataFrame или Series