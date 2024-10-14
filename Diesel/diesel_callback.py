from datetime import datetime  # Импортируем модуль для работы с датой и временем


class DieselCallbackBD:

    def __init__(self, diesel):
        # Инициализация объекта класса
        self.flag = True  # Флаг для управления состоянием
        self.diesel = diesel  # Объект для работы с дизельным генератором
        self.old_command = 0  # Переменная для хранения предыдущей команды
        self.old_list_command = []  # Список для хранения предыдущих команд

    def checking_work_status(self, address=3, count=1, slave=2):
        # Проверка статуса работы дизельного генератора
        status = self.diesel.get_data_bool(address, count, slave)  # Получаем статус работы
        print("Статус работы:", status)  # Выводим статус работы

    def ready_auto_launch(self, address=31, count=1, slave=2):
        # Проверка готовности дизельного генератора к автоматическому запуску
        status = self.diesel.get_data_bool(address, count, slave)  # Получаем статус готовности
        # Здесь статус готовности можно использовать для дальнейших действий

    def get_power_current(self):
        # Получение текущей мощности дизельного генератора
        power = self.diesel.command_read_input_registers(address=519, count=1, slave=3)  # Чтение регистра мощности
        print(f"Мощность ДЭС {power}")  # Вывод мощности на экран

    def on_off(self, available_dgu, slave, value=True):
        # Включение или выключение дизельного генератора
        if available_dgu:
            address = 0  # Адрес для включения генератора
        else:
            address = 3  # Адрес для выключения генератора
        self.diesel.command_write_coil(address, value, slave)  # Отправка команды на включение/выключение
        print(f"Отправлена команда на slave {slave} address {address} {datetime.now()}")  # Логирование команды с указанием времени

    def command_processing_diesel(self, available_dgu):
        # Обработка команд для дизельного генератора
        print(available_dgu)  # Вывод списка доступных генераторов
        for dgu in available_dgu:
            if dgu not in self.old_list_command:  # Проверяем, если команда не была выполнена ранее
                self.on_off(dgu['control_dgu'], slave=dgu['slave'])  # Выполняем команду включения/выключения
        self.old_list_command = available_dgu  # Обновляем список команд

    def get_power_dgu(self, slave):
        # Получение данных о мощности для конкретного генератора
        power = self.diesel.command_read_input_registers(address=516, count=3, slave=slave)  # Чтение регистров мощности
        return power  # Возвращаем значение мощности

    def get_current_dgu(self, slave):
        # Получение данных о текущем для конкретного генератора
        current = self.diesel.command_read_input_registers(address=513, count=3, slave=slave)  # Чтение регистров тока
        return current  # Возвращаем значение тока